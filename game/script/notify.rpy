init python:
    def notify_windows(box_text="none",box_title="Renpy"):
        try:
            import ctypes
            Notifybox = ctypes.windll.user32.MessageBoxW
            MB_OK = 0x0
            MB_OKCXL = 0x01
            MB_YESNOCXL = 0x03
            MB_YESNO = 0x04
            MB_HELP = 0x4000
            ICON_EXLAIM = 0x30
            ICON_INFO = 0x40
            ICON_STOP = 0x10
            Notifybox(0, f"{box_text}",f"{box_title}", MB_OK|ICON_INFO)
        except Exception as e:
            renpy.notify(f"{str(e)}\n非windows平台，无法导入api或module")
# 以针对 Windows 系统的通知弹窗功能
    def AndroidNotify(title_text="Ren’py", box_text="这是一条来自Ren’py的通知", channel_id="renpy_channel"):
        try:
            import jnius
            if not renpy.android:
                return False
            try:
                PythonSDLActivity = jnius.autoclass("org.renpy.android.PythonSDLActivity")
                activity = PythonSDLActivity.mActivity
                if activity is None:
                    renpy.notify("无活动")
                    return False
                activity.AndroidNotifyBox(title_text, box_text)
                return True
            except Exception as e:
                print(None, f"发送通知失败: {str(e)}")
                return False
        except Exception as e:
            renpy.notify(f"{str(e)}\n非安卓平台，无法导入api或module")
# 以针对 Android 系统的通知功能