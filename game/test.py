import ctypes
from ctypes import wintypes
import time
import threading
from enum import IntEnum

# 定义常量
NIM_ADD = 0x00000000
NIM_MODIFY = 0x00000001
NIM_DELETE = 0x00000002
NIM_SETVERSION = 0x00000004

NIF_MESSAGE = 0x00000001
NIF_ICON = 0x00000002
NIF_TIP = 0x00000004
NIF_STATE = 0x00000008
NIF_INFO = 0x00000010
NIF_GUID = 0x00000020

NIIF_NONE = 0x00000000
NIIF_INFO = 0x00000001
NIIF_WARNING = 0x00000002
NIIF_ERROR = 0x00000003
NIIF_USER = 0x00000004
NIIF_NOSOUND = 0x00000010
NIIF_LARGE_ICON = 0x00000020
NIIF_RESPECT_QUIET_TIME = 0x00000080

WM_USER = 0x0400
WM_MOUSEMOVE = 0x0200
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
WM_LBUTTONDBLCLK = 0x0203
WM_RBUTTONDOWN = 0x0204
WM_RBUTTONUP = 0x0205
WM_RBUTTONDBLCLK = 0x0206
WM_MBUTTONDOWN = 0x0207
WM_MBUTTONUP = 0x0208
WM_MBUTTONDBLCLK = 0x0209

# 定义消息类型枚举
class NotificationType(IntEnum):
    INFO = NIIF_INFO
    WARNING = NIIF_WARNING
    ERROR = NIIF_ERROR
    NOSOUND = NIIF_NOSOUND | NIIF_INFO
    LARGE_ICON = NIIF_LARGE_ICON | NIIF_INFO

# 定义鼠标事件枚举
class MouseEvent(IntEnum):
    MOVE = WM_MOUSEMOVE
    LBUTTON_DOWN = WM_LBUTTONDOWN
    LBUTTON_UP = WM_LBUTTONUP
    LBUTTON_DBLCLK = WM_LBUTTONDBLCLK
    RBUTTON_DOWN = WM_RBUTTONDOWN
    RBUTTON_UP = WM_RBUTTONUP
    RBUTTON_DBLCLK = WM_RBUTTONDOWN

# 定义结构体
class NOTIFYICONDATA(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("hWnd", wintypes.HWND),
        ("uID", wintypes.UINT),
        ("uFlags", wintypes.UINT),
        ("uCallbackMessage", wintypes.UINT),
        ("hIcon", wintypes.HANDLE),
        ("szTip", wintypes.WCHAR * 128),
        ("dwState", wintypes.DWORD),
        ("dwStateMask", wintypes.DWORD),
        ("szInfo", wintypes.WCHAR * 256),
        ("uVersion", wintypes.UINT),
        ("szInfoTitle", wintypes.WCHAR * 64),
        ("dwInfoFlags", wintypes.DWORD),
        ("guidItem", wintypes.GUID),
        ("hBalloonIcon", wintypes.HANDLE),
    ]

# 创建系统托盘通知类
class SystemTrayNotification:
    def __init__(self, tooltip="Python Notification"):
        self.hwnd = None
        self.tooltip = tooltip
        self.icon_id = 1000
        self.callback_msg = WM_USER + 1
        self.callbacks = {}
        
        # 创建隐藏窗口
        self._create_window()
        
        # 添加图标到系统托盘
        self._add_tray_icon()
    
    def _create_window(self):
        """创建隐藏窗口用于接收消息"""
        wc = wintypes.WNDCLASS()
        wc.lpfnWndProc = self._wnd_proc
        wc.hInstance = ctypes.windll.kernel32.GetModuleHandleW(None)
        wc.lpszClassName = "PythonNotificationClass"
        
        # 注册窗口类
        atom = ctypes.windll.user32.RegisterClassW(ctypes.byref(wc))
        if not atom:
            raise WindowsError("无法注册窗口类")
        
        # 创建窗口
        self.hwnd = ctypes.windll.user32.CreateWindowExW(
            0,
            wc.lpszClassName,
            "Notification Window",
            0,
            0, 0, 0, 0,
            None, None,
            wc.hInstance,
            None
        )
        
        if not self.hwnd:
            raise WindowsError("无法创建窗口")
    
    def _wnd_proc(self, hwnd, msg, wparam, lparam):
        """窗口消息处理函数"""
        if msg == self.callback_msg:
            # 处理托盘图标消息
            if lparam == WM_RBUTTONDOWN:
                self._on_right_click()
            elif lparam == WM_LBUTTONDOWN:
                self._on_left_click()
            elif lparam == WM_LBUTTONDBLCLK:
                self._on_double_click()
            elif lparam == WM_RBUTTONDBLCLK:
                self._on_right_double_click()
        
        # 调用默认窗口过程
        return ctypes.windll.user32.DefWindowProcW(hwnd, msg, wparam, lparam)
    
    def _add_tray_icon(self):
        """添加图标到系统托盘"""
        nid = NOTIFYICONDATA()
        nid.cbSize = ctypes.sizeof(NOTIFYICONDATA)
        nid.hWnd = self.hwnd
        nid.uID = self.icon_id
        nid.uFlags = NIF_MESSAGE | NIF_ICON | NIF_TIP
        nid.uCallbackMessage = self.callback_msg
        
        # 加载默认图标
        nid.hIcon = ctypes.windll.user32.LoadIconW(
            None, 
            ctypes.cast(32512, ctypes.c_void_p)  # IDI_APPLICATION
        )
        
        # 设置工具提示
        nid.szTip = self.tooltip
        
        # 添加到托盘
        result = ctypes.windll.shell32.Shell_NotifyIconW(NIM_ADD, ctypes.byref(nid))
        if not result:
            raise WindowsError("无法添加托盘图标")
    
    def show_notification(self, title, message, 
                         notification_type=NotificationType.INFO,
                         timeout=5000):
        """
        显示通知
        
        参数:
            title: 通知标题
            message: 通知内容
            notification_type: 通知类型 (INFO, WARNING, ERROR等)
            timeout: 显示时间（毫秒）
        """
        nid = NOTIFYICONDATA()
        nid.cbSize = ctypes.sizeof(NOTIFYICONDATA)
        nid.hWnd = self.hwnd
        nid.uID = self.icon_id
        nid.uFlags = NIF_INFO
        
        # 设置通知内容
        nid.szInfoTitle = title[:63]  # 限制长度
        nid.szInfo = message[:255]    # 限制长度
        nid.dwInfoFlags = notification_type
        
        # 显示通知
        result = ctypes.windll.shell32.Shell_NotifyIconW(NIM_MODIFY, ctypes.byref(nid))
        
        if not result:
            raise WindowsError("无法显示通知")
        
        # 设置超时自动移除
        if timeout > 0:
            def remove_notification():
                time.sleep(timeout / 1000)
                nid.uFlags = NIF_INFO
                nid.szInfoTitle = ""
                nid.szInfo = ""
                ctypes.windll.shell32.Shell_NotifyIconW(NIM_MODIFY, ctypes.byref(nid))
            
            threading.Thread(target=remove_notification, daemon=True).start()
        
        return result
    
    def update_icon(self, icon_path=None):
        """更新托盘图标"""
        nid = NOTIFYICONDATA()
        nid.cbSize = ctypes.sizeof(NOTIFYICONDATA)
        nid.hWnd = self.hwnd
        nid.uID = self.icon_id
        nid.uFlags = NIF_ICON
        
        if icon_path:
            # 从文件加载图标
            nid.hIcon = ctypes.windll.user32.LoadImageW(
                None,
                icon_path,
                1,  # IMAGE_ICON
                0, 0,
                0x00000010  # LR_LOADFROMFILE
            )
        else:
            # 使用默认图标
            nid.hIcon = ctypes.windll.user32.LoadIconW(
                None, 
                ctypes.cast(32512, ctypes.c_void_p)
            )
        
        ctypes.windll.shell32.Shell_NotifyIconW(NIM_MODIFY, ctypes.byref(nid))
    
    def update_tooltip(self, tooltip):
        """更新工具提示"""
        nid = NOTIFYICONDATA()
        nid.cbSize = ctypes.sizeof(NOTIFYICONDATA)
        nid.hWnd = self.hwnd
        nid.uID = self.icon_id
        nid.uFlags = NIF_TIP
        nid.szTip = tooltip
        
        ctypes.windll.shell32.Shell_NotifyIconW(NIM_MODIFY, ctypes.byref(nid))
    
    def set_callback(self, event, callback):
        """设置事件回调"""
        self.callbacks[event] = callback
    
    def _on_left_click(self):
        if MouseEvent.LBUTTON_DOWN in self.callbacks:
            self.callbacks[MouseEvent.LBUTTON_DOWN]()
    
    def _on_right_click(self):
        if MouseEvent.RBUTTON_DOWN in self.callbacks:
            self.callbacks[MouseEvent.RBUTTON_DOWN]()
    
    def _on_double_click(self):
        if MouseEvent.LBUTTON_DBLCLK in self.callbacks:
            self.callbacks[MouseEvent.LBUTTON_DBLCLK]()
    
    def _on_right_double_click(self):
        if MouseEvent.RBUTTON_DBLCLK in self.callbacks:
            self.callbacks[MouseEvent.RBUTTON_DBLCLK]()
    
    def cleanup(self):
        """清理资源"""
        nid = NOTIFYICONDATA()
        nid.cbSize = ctypes.sizeof(NOTIFYICONDATA)
        nid.hWnd = self.hwnd
        nid.uID = self.icon_id
        
        # 从系统托盘移除图标
        ctypes.windll.shell32.Shell_NotifyIconW(NIM_DELETE, ctypes.byref(nid))
        
        # 销毁窗口
        if self.hwnd:
            ctypes.windll.user32.DestroyWindow(self.hwnd)
    
    def __del__(self):
        self.cleanup()

# 高级通知管理器
class NotificationManager:
    def __init__(self):
        self.notifications = {}
        self.next_id = 1
    
    def show(self, title, message, 
             notification_type=NotificationType.INFO,
             timeout=5000,
             callback=None):
        """
        显示通知（简化版）
        
        参数:
            title: 通知标题
            message: 通知内容
            notification_type: 通知类型
            timeout: 显示时间
            callback: 点击回调函数
        """
        # 创建临时通知对象
        notification = SystemTrayNotification(f"Notification #{self.next_id}")
        
        if callback:
            notification.set_callback(MouseEvent.LBUTTON_DOWN, callback)
        
        notification.show_notification(title, message, notification_type, timeout)
        
        # 保存引用
        self.notifications[self.next_id] = notification
        self.next_id += 1
        
        # 自动清理
        def auto_cleanup(notif_id):
            time.sleep((timeout + 1000) / 1000)  # 等待通知显示完成
            if notif_id in self.notifications:
                self.notifications[notif_id].cleanup()
                del self.notifications[notif_id]
        
        threading.Thread(target=auto_cleanup, 
                        args=(self.next_id - 1,),
                        daemon=True).start()
        
        return self.next_id - 1
    
    def close_all(self):
        """关闭所有通知"""
        for notif in self.notifications.values():
            notif.cleanup()
        self.notifications.clear()

# 使用示例
if __name__ == "__main__":
    # 示例1：使用SystemTrayNotification类（持久化通知）
    print("示例1：持久化系统托盘通知")
    print("-" * 50)
    
    def on_notification_click():
        print("通知被点击了！")
    
    def on_right_click():
        print("右键点击了托盘图标")
    
    try:
        # 创建持久化通知
        tray = SystemTrayNotification("我的应用通知")
        
        # 设置回调
        tray.set_callback(MouseEvent.LBUTTON_DOWN, on_notification_click)
        tray.set_callback(MouseEvent.RBUTTON_DOWN, on_right_click)
        
        # 显示不同类型的通知
        print("显示信息通知...")
        tray.show_notification(
            "信息通知",
            "这是一个信息类型的通知消息",
            NotificationType.INFO,
            3000
        )
        time.sleep(2)
        
        print("显示警告通知...")
        tray.show_notification(
            "警告通知",
            "这是一个警告类型的通知消息",
            NotificationType.WARNING,
            3000
        )
        time.sleep(2)
        
        print("显示错误通知...")
        tray.show_notification(
            "错误通知",
            "这是一个错误类型的通知消息",
            NotificationType.ERROR,
            3000
        )
        time.sleep(2)
        
        print("显示无声通知...")
        tray.show_notification(
            "无声通知",
            "这个通知没有声音",
            NotificationType.NOSOUND,
            3000
        )
        
        print("\n尝试点击通知或托盘图标测试回调功能...")
        print("按Enter键继续...")
        input()
        
    finally:
        # 清理资源
        tray.cleanup()
    
    # 示例2：使用NotificationManager类（快速通知）
    print("\n\n示例2：快速通知管理器")
    print("-" * 50)
    
    manager = NotificationManager()
    
    def quick_callback():
        print("快速通知被点击！")
    
    # 快速显示多个通知
    print("显示一系列快速通知...")
    
    manager.show(
        "任务完成",
        "您的文件已下载完成",
        NotificationType.INFO,
        2000,
        quick_callback
    )
    
    time.sleep(1)
    
    manager.show(
        "系统警告",
        "磁盘空间不足，请及时清理",
        NotificationType.WARNING,
        3000
    )
    
    time.sleep(1)
    
    manager.show(
        "操作失败",
        "无法连接到服务器，请检查网络连接",
        NotificationType.ERROR,
        4000
    )
    
    print("所有通知已发送，等待几秒钟查看效果...")
    time.sleep(5)
    
    # 清理所有通知
    manager.close_all()
    
    # 示例3：模拟常见应用场景
    print("\n\n示例3：模拟应用场景")
    print("-" * 50)
    
    def download_complete():
        print("下载完成回调执行")
    
    def new_message():
        print("新消息回调执行")
    
    def system_alert():
        print("系统警告回调执行")
    
    # 模拟下载完成
    manager.show(
        "下载管理器",
        "文件 'python_installer.exe' 下载完成",
        NotificationType.INFO,
        5000,
        download_complete
    )
    
    # 模拟新消息
    manager.show(
        "即时通讯",
        "Alice: 你好，今晚有空吗？",
        NotificationType.INFO,
        5000,
        new_message
    )
    
    # 模拟系统警告
    manager.show(
        "系统安全",
        "检测到可疑程序，建议立即扫描",
        NotificationType.WARNING,
        5000,
        system_alert
    )
    
    print("应用场景模拟完成，等待几秒钟查看通知...")
    time.sleep(6)
    manager.close_all()
    
    print("\n所有示例完成！")