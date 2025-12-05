init python:
    import ctypes
    Notifybox = ctypes.windll.user32.MessageBoxW
    def notify_windows(box_text="none",box_title="Renpy"):
        MB_OK = 0x0
        MB_OKCXL = 0x01
        MB_YESNOCXL = 0x03
        MB_YESNO = 0x04
        MB_HELP = 0x4000
        ICON_EXLAIM = 0x30
        ICON_INFO = 0x40
        ICON_STOP = 0x10
        Notifybox(0, f"{box_text}",f"{box_title}", MB_OK|ICON_INFO)
    
    
