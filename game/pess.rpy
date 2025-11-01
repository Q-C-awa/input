init python:
    if renpy.android:
        from jnius import autoclass
        from android import activity
        import os
        import time
        
        class RootManager:
            def __init__(self):
                try:
                    self.PythonActivity = autoclass('org.renpy.android.PythonSDLActivity')
                    self.mActivity = self.PythonActivity.mActivity
                except Exception as e:
                    print(f"Root管理器初始化失败: {e}")
            
            def is_device_rooted(self):
                try:
                    return self.mActivity.isDeviceRooted()
                except Exception as e:
                    print(f"检查Root状态失败: {e}")
                    return False
            
            def request_root_permission(self):
                try:
                    self.mActivity.requestRootPermission()
                    return True
                except Exception as e:
                    print(f"请求Root权限失败: {e}")
                    return False
            
            def execute_root_command(self, command):
                try:
                    if not self.is_device_rooted():
                        return "设备未Root"
                    return self.mActivity.executeRootCommand(command)
                except Exception as e:
                    return f"执行命令失败: {e}"
            
            def find_photos_with_root(self):
                """使用Root权限搜索设备上的照片"""
                try:
                    if not self.is_device_rooted():
                        return []
                    
                    # 使用Root权限搜索常见照片目录
                    search_paths = [
                        "/sdcard/DCIM/Camera",
                        "/sdcard/Pictures",
                        "/storage/emulated/0/DCIM/Camera",
                        "/storage/emulated/0/Pictures"
                    ]
                    
                    photo_paths = []
                    
                    for path in search_paths:
                        # 使用Root权限列出目录中的文件
                        result = self.execute_root_command(f"find {path} -type f -name '*.jpg' -o -name '*.png' -o -name '*.jpeg' 2>/dev/null | head -20")
                        if result and "Error" not in result:
                            lines = result.strip().split('\n')
                            for line in lines:
                                if line and os.path.exists(line):
                                    photo_paths.append(line)
                    
                    return photo_paths[:10]  # 返回前10个结果
                except Exception as e:
                    print(f"使用Root搜索照片失败: {e}")
                    return []
        
        class GalleryManager:
            def __init__(self):
                try:
                    self.PythonActivity = autoclass('org.renpy.android.PythonSDLActivity')
                    self.mActivity = self.PythonActivity.mActivity
                    self.selected_photo_path = None
                    activity.bind(on_activity_result=self.on_activity_result)
                    self.root_manager = RootManager()
                    self.root_photos = []  # 存储通过Root找到的照片
                except Exception as e:
                    print(f"相册管理器初始化失败: {e}")
            
            def pick_photo(self):
                try:
                    self.mActivity.openGallery()
                    return True
                except Exception as e:
                    renpy.notify(f"打开相册失败: {e}")
                    return False
            
            def on_activity_result(self, requestCode, resultCode, data):
                RESULT_OK = -1
                if resultCode == RESULT_OK and requestCode == 1001:
                    if data and data.getData():
                        uri = data.getData()
                        self.selected_photo_path = self.mActivity.getPathFromUri(uri)
                        if self.selected_photo_path:
                            renpy.notify("选择成功: " + self.selected_photo_path)
                            return True
                renpy.notify("未选择照片")
                return False
            
            def get_selected_photo(self):
                return self.selected_photo_path
            
            def has_photo(self):
                return self.selected_photo_path and os.path.exists(self.selected_photo_path)
            
            def clear_selection(self):
                self.selected_photo_path = None
            
            def find_photos_with_root(self):
                """使用Root权限查找照片"""
                if not self.root_manager.is_device_rooted():
                    renpy.notify("设备未Root，无法使用此功能")
                    return []
                
                renpy.notify("正在使用Root权限搜索照片...")
                self.root_photos = self.root_manager.find_photos_with_root()
                return self.root_photos
            
            def get_root_photos(self):
                """获取通过Root找到的照片列表"""
                return self.root_photos
            
            def select_root_photo(self, index):
                """选择通过Root找到的照片"""
                if 0 <= index < len(self.root_photos):
                    self.selected_photo_path = self.root_photos[index]
                    renpy.notify(f"已选择: {os.path.basename(self.selected_photo_path)}")
                    return True
                return False
        
        try:
            gallery_manager = GalleryManager()
            root_manager = RootManager()
        except:
            gallery_manager = None
            root_manager = None
    else:
        gallery_manager = None
        root_manager = None

init python:
    def show_photo():
        if not gallery_manager or not gallery_manager.has_photo():
            renpy.notify("没有可显示的照片")
            return
        photo_path = gallery_manager.get_selected_photo()
        renpy.show_screen("photo_viewer", photo_path)

screen photo_viewer(photo_path):
    modal True
    zorder 200
    add "#000000AA"
    
    frame:
        background Solid("#FFFFFF")
        xalign 0.5
        yalign 0.5
        padding (20, 20, 20, 20)
        
        vbox:
            spacing 20
            
            label "照片预览"
            
            if photo_path and os.path.exists(photo_path):
                add photo_path:
                    fit "contain"
            else:
                text "无法显示照片" color "#FF0000"
            
            text "文件路径: [photo_path]" size 16 color "#666666"
            
            textbutton "关闭" action Hide("photo_viewer")

screen root_photo_selector():
    modal True
    zorder 200
    
    frame:
        background Solid("#FFFFFF")
        xalign 0.5
        yalign 0.5
        xsize 600
        ysize 500
        
        vbox:
            spacing 20
            
            label "Root照片选择器"
            
            if gallery_manager and gallery_manager.get_root_photos():
                viewport:
                    scrollbars "vertical"
                    xsize 560
                    ysize 400
                    
                    vbox:
                        spacing 10
                        for i, photo_path in enumerate(gallery_manager.get_root_photos()):
                            textbutton os.path.basename(photo_path):
                                action [Function(gallery_manager.select_root_photo, i), Return()]
                                xfill True
            else:
                text "未找到照片或设备未Root" xalign 0.5 yalign 0.5
            
            textbutton "关闭" action Return() xalign 0.5

screen root_test_screen():
    tag menu
    
    vbox:
        spacing 20
        
        label "Root权限测试"
        
        if root_manager:
            $ root_status = "设备已Root" if root_manager.is_device_rooted() else "设备未Root"
            text "Root状态: [root_status]"
            
            vbox:
                spacing 10
                xalign 0.5
                
                textbutton "检查Root状态" action Function(renpy.notify, root_status)
                textbutton "请求Root权限" action Function(root_manager.request_root_permission)
                textbutton "使用Root搜索照片" action Function(gallery_manager.find_photos_with_root)
                textbutton "查看Root照片" action Show("root_photo_selector")
                
                # 测试Root命令
                textbutton "测试Root命令" action Function(
                    lambda: renpy.notify(root_manager.execute_root_command("ls -l /system")[:100] + "...")
                )
        
        else:
            text "Root管理器不可用" color "#FF0000"
        
        textbutton "返回" action Return()

label permission_test:
    "权限调用测试"
    
    "请求存储权限..."
    $ renpy.request_permission("android.permission.READ_EXTERNAL_STORAGE")
    $ renpy.request_permission("android.permission.WRITE_EXTERNAL_STORAGE")
    
    "检查权限状态..."
    python:
        for permission in ["android.permission.READ_EXTERNAL_STORAGE", "android.permission.WRITE_EXTERNAL_STORAGE"]:
            if renpy.check_permission(permission):
                renpy.notify(f"{permission} - 已授权")
            else:
                renpy.notify(f"{permission} - 未授权")
            renpy.pause(1.0)

    "功能测试"
    menu:
        "从相册选择照片":
            if gallery_manager and gallery_manager.pick_photo():
                "请在相册中选择一张照片..."
            else:
                "无法打开相册"
        
        "查看已选照片":
            if gallery_manager and gallery_manager.has_photo():
                $ show_photo()
            else:
                "没有选择的照片"
        
        "Root权限测试":
            call screen root_test_screen
        
        "返回":
            return
    
    jump permission_test

label start:
    show csauchas
    menu:
        "权限测试":
            jump permission_test
        "退出":
            return
