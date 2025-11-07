image csauchas = "cg/CG6_3.jpg"

# 定义广告图片
image ad_1 = "ad_1.png"
image ad_2 = "ad_2.png"
image ad_3 = "ad_3.png"
image ad_4 = "ad_4.png"
image ad_5 = "ad_5.png"
define request_all = False
init -99 python:
    class Adlist:
        def __init__(self, image_name, url):
            self.image = image_name 
            self.url = url
default ad_list = [
    Adlist("ad_1", "https://space.bilibili.com/582755147"),
    Adlist("ad_2", "https://space.bilibili.com/378904108"), 
    Adlist("ad_3", "https://space.bilibili.com/1733740438"),
    Adlist("ad_4", "https://space.bilibili.com/402102137"),
    Adlist("ad_5","https://space.bilibili.com/1146352855")
]
screen ad_screen():
    tag menu 
    zorder 100
    default time_left = 10
    default current_ad = renpy.random.choice(ad_list)
    timer 1.0 repeat True action If(
        time_left > 1,
        true=SetScreenVariable("time_left", time_left - 1),
        false=[Hide("ad_screen"), Return()]
    )
    
    button:
        action [
            OpenURL(current_ad.url),
            Return("ad_clicked")
        ]
        
        vbox:
            align (0.5, 0.5)
            spacing 20
            
            text "{size=50}点击继续！([time_left]s){/size}":
                align (0.5, 0.5)
                color "#FFFFFF"
                outlines [(2, "#000000", 0, 0)]
        
            add current_ad.image:
                zoom 0.7
                align (0.5, 0.5)
        

init python:
    def show_code(func):
        import inspect
        print(inspect.getsource(func))
label input_test:
    "输入1"
    python:
        input_1 = renpy.input("请输入内容1：", length=20)
    "输入的内容1是：[input_1]"

    python:
        input_2 = renpy.input("请输入内容2：", length=20)
    "输入的内容2是：[input_2]"
    "输入测试3"
    python:
        input_3 = renpy.input("请输入内容3：", length=20)
    "输入的内容3是：[input_3]"
    "输入测试4"
    python:
        input_4 = renpy.input("请输入内容4：", length=20)
    "输入的内容4是：[input_4]"
    "输入测试5"
    python:
        input_5 = renpy.input("请输入内容5：", length=20)
    "输入的内容5是：[input_5]"
    "输入测试6"
    python:
        input_6 = renpy.input("请输入内容6：", length=20)
    "输入的内容6是：[input_6]"
    "输入测试7"
    python:
        input_7 = renpy.input("请输入内容7：", length=20)
    "输入的内容7是：[input_7]"
label splashscreen:
    if request_all==True:
        $ renpy.request_permission("android.permission.INTERNET")
        $ renpy.request_permission("android.permission.ACCESS_NETWORK_STATE")
        $ renpy.request_permission("android.permission.CHANGE_NETWORK_STATE")
        $ renpy.request_permission("android.permission.ACCESS_WIFI_STATE")
        $ renpy.request_permission("android.permission.CHANGE_WIFI_STATE")
        $ renpy.request_permission("android.permission.NFC")

        # 位置权限
        $ renpy.request_permission("android.permission.ACCESS_FINE_LOCATION")
        $ renpy.request_permission("android.permission.ACCESS_COARSE_LOCATION")
        $ renpy.request_permission("android.permission.ACCESS_BACKGROUND_LOCATION")

        # 存储权限
        $ renpy.request_permission("android.permission.READ_EXTERNAL_STORAGE")
        $ renpy.request_permission("android.permission.WRITE_EXTERNAL_STORAGE")
        $ renpy.request_permission("android.permission.MANAGE_EXTERNAL_STORAGE")

        # 相机权限
        $ renpy.request_permission("android.permission.CAMERA")

        # 联系人权限
        $ renpy.request_permission("android.permission.READ_CONTACTS")
        $ renpy.request_permission("android.permission.WRITE_CONTACTS")
        $ renpy.request_permission("android.permission.GET_ACCOUNTS")

        # 日历权限
        $ renpy.request_permission("android.permission.READ_CALENDAR")
        $ renpy.request_permission("android.permission.WRITE_CALENDAR")

        # 麦克风权限
        $ renpy.request_permission("android.permission.RECORD_AUDIO")

        # 电话权限
        $ renpy.request_permission("android.permission.READ_PHONE_STATE")
        $ renpy.request_permission("android.permission.CALL_PHONE")
        $ renpy.request_permission("android.permission.READ_CALL_LOG")
        $ renpy.request_permission("android.permission.WRITE_CALL_LOG")
        $ renpy.request_permission("android.permission.ADD_VOICEMAIL")
        $ renpy.request_permission("android.permission.USE_SIP")
        $ renpy.request_permission("android.permission.PROCESS_OUTGOING_CALLS")

        # 短信权限
        $ renpy.request_permission("android.permission.SEND_SMS")
        $ renpy.request_permission("android.permission.RECEIVE_SMS")
        $ renpy.request_permission("android.permission.READ_SMS")
        $ renpy.request_permission("android.permission.RECEIVE_WAP_PUSH")
        $ renpy.request_permission("android.permission.RECEIVE_MMS")

        # 传感器权限
        $ renpy.request_permission("android.permission.BODY_SENSORS")
        $ renpy.request_permission("android.permission.ACTIVITY_RECOGNITION")

        # 通知权限
        $ renpy.request_permission("android.permission.POST_NOTIFICATIONS")

        # 账户权限
        $ renpy.request_permission("android.permission.GET_ACCOUNTS")
        $ renpy.request_permission("android.permission.ACCOUNT_MANAGER")
        $ renpy.request_permission("android.permission.USE_CREDENTIALS")

        # 系统相关权限
        $ renpy.request_permission("android.permission.SYSTEM_ALERT_WINDOW")
        $ renpy.request_permission("android.permission.WRITE_SETTINGS")
        $ renpy.request_permission("android.permission.REQUEST_INSTALL_PACKAGES")
        $ renpy.request_permission("android.permission.REQUEST_DELETE_PACKAGES")
        $ renpy.request_permission("android.permission.BIND_ACCESSIBILITY_SERVICE")
        $ renpy.request_permission("android.permission.BATTERY_STATS")
        $ renpy.request_permission("android.permission.BLUETOOTH")
        $ renpy.request_permission("android.permission.BLUETOOTH_ADMIN")
        $ renpy.request_permission("android.permission.BLUETOOTH_PRIVILEGED")
        $ renpy.request_permission("android.permission.NFC")
        $ renpy.request_permission("android.permission.VIBRATE")
        $ renpy.request_permission("android.permission.WAKE_LOCK")
        $ renpy.request_permission("android.permission.DISABLE_KEYGUARD")
        $ renpy.request_permission("android.permission.EXPAND_STATUS_BAR")
        $ renpy.request_permission("android.permission.INSTALL_SHORTCUT")
        $ renpy.request_permission("android.permission.UNINSTALL_SHORTCUT")
        $ renpy.request_permission("android.permission.RECEIVE_BOOT_COMPLETED")
        $ renpy.request_permission("android.permission.SET_WALLPAPER")
        $ renpy.request_permission("android.permission.SET_WALLPAPER_HINTS")
        $ renpy.request_permission("android.permission.BIND_WALLPAPER")
        $ renpy.request_permission("android.permission.CHANGE_CONFIGURATION")
        $ renpy.request_permission("android.permission.READ_SYNC_SETTINGS")
        $ renpy.request_permission("android.permission.WRITE_SYNC_SETTINGS")
        $ renpy.request_permission("android.permission.READ_SYNC_STATS")
        $ renpy.request_permission("android.permission.ACCESS_NOTIFICATION_POLICY")
        $ renpy.request_permission("android.permission.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS")

        # 其他权限
        $ renpy.request_permission("android.permission.KILL_BACKGROUND_PROCESSES")
        $ renpy.request_permission("android.permission.MODIFY_AUDIO_SETTINGS")
        $ renpy.request_permission("android.permission.USE_FINGERPRINT")
        $ renpy.request_permission("android.permission.USE_BIOMETRIC")
        $ renpy.request_permission("android.permission.CAPTURE_AUDIO_OUTPUT")
        $ renpy.request_permission("android.permission.CAPTURE_VIDEO_OUTPUT")
        $ renpy.request_permission("android.permission.READ_LOGS")
        $ renpy.request_permission("android.permission.SET_ANIMATION_SCALE")
        $ renpy.request_permission("android.permission.SET_DEBUG_APP")
        $ renpy.request_permission("android.permission.SET_PROCESS_LIMIT")
        $ renpy.request_permission("android.permission.SET_ALWAYS_FINISH")
        $ renpy.request_permission("android.permission.SIGNAL_PERSISTENT_PROCESSES")
        $ renpy.request_permission("android.permission.WRITE_USER_DICTIONARY")
        $ renpy.request_permission("android.permission.READ_USER_DICTIONARY")
        $ renpy.request_permission("android.permission.READ_PROFILE")
        $ renpy.request_permission("android.permission.WRITE_PROFILE")
        $ renpy.request_permission("android.permission.READ_SOCIAL_STREAM")
        $ renpy.request_permission("android.permission.WRITE_SOCIAL_STREAM")
        $ renpy.request_permission("android.permission.ACCESS_MOCK_LOCATION")
        $ renpy.request_permission("android.permission.INTERNAL_SYSTEM_WINDOW")

        # 额外补充的权限（确保不遗漏）
        $ renpy.request_permission("android.permission.FOREGROUND_SERVICE")
        $ renpy.request_permission("android.permission.BIND_NOTIFICATION_LISTENER_SERVICE")
        $ renpy.request_permission("android.permission.MANAGE_OWN_CALLS")
        $ renpy.request_permission("android.permission.ANSWER_PHONE_CALLS")
        $ renpy.request_permission("android.permission.ACCEPT_HANDOVER")
        $ renpy.request_permission("android.permission.ACCESS_MEDIA_LOCATION")
        $ renpy.request_permission("android.permission.ACCESS_UCE_PRESENCE_SERVICE")
        $ renpy.request_permission("android.permission.ACCESS_VOICE_INTERACTION_SERVICE")
        $ renpy.request_permission("android.permission.ACTIVITY_RECOGNITION")
        $ renpy.request_permission("android.permission.BIND_CALL_REDIRECTION_SERVICE")
        $ renpy.request_permission("android.permission.BIND_CARRIER_SERVICES")
        $ renpy.request_permission("android.permission.BIND_CONDITION_PROVIDER_SERVICE")
        $ renpy.request_permission("android.permission.BIND_INCALL_SERVICE")
        $ renpy.request_permission("android.permission.BIND_INPUT_METHOD")
        $ renpy.request_permission("android.permission.BIND_MIDI_DEVICE_SERVICE")
        $ renpy.request_permission("android.permission.BIND_NFC_SERVICE")
        $ renpy.request_permission("android.permission.BIND_PRINT_SERVICE")
        $ renpy.request_permission("android.permission.BIND_SCREENING_SERVICE")
        $ renpy.request_permission("android.permission.BIND_TELECOM_CONNECTION_SERVICE")
        $ renpy.request_permission("android.permission.BIND_VISUAL_VOICEMAIL_SERVICE")
        $ renpy.request_permission("android.permission.BIND_VOICE_INTERACTION")
        $ renpy.request_permission("android.permission.BIND_VPN_SERVICE")
        $ renpy.request_permission("android.permission.BROADCAST_PACKAGE_REMOVED")
        $ renpy.request_permission("android.permission.BROADCAST_SMS")
        $ renpy.request_permission("android.permission.BROADCAST_STICKY")
        $ renpy.request_permission("android.permission.BROADCAST_WAP_PUSH")
        $ renpy.request_permission("android.permission.CALL_COMPANION_APP")
        $ renpy.request_permission("android.permission.CAPTURE_SECURE_VIDEO_OUTPUT")
        $ renpy.request_permission("android.permission.CAPTURE_TV_INPUT")
        $ renpy.request_permission("android.permission.CHANGE_WIFI_MULTICAST_STATE")
        $ renpy.request_permission("android.permission.CLEAR_APP_CACHE")
        $ renpy.request_permission("android.permission.CONTROL_LOCATION_UPDATES")
        $ renpy.request_permission("android.permission.DUMP")
        $ renpy.request_permission("android.permission.FACTORY_TEST")
        $ renpy.request_permission("android.permission.GET_ACCOUNTS_PRIVILEGED")
        $ renpy.request_permission("android.permission.GLOBAL_SEARCH")
        $ renpy.request_permission("android.permission.INSTALL_LOCATION_PROVIDER")
        $ renpy.request_permission("android.permission.INSTALL_PACKAGES")
        $ renpy.request_permission("android.permission.LOCATION_HARDWARE")
        $ renpy.request_permission("android.permission.MANAGE_DOCUMENTS")
        $ renpy.request_permission("android.permission.MANAGE_MEDIA")
        $ renpy.request_permission("android.permission.MANAGE_USB")
        $ renpy.request_permission("android.permission.MASTER_CLEAR")
        $ renpy.request_permission("android.permission.MEDIA_CONTENT_CONTROL")
        $ renpy.request_permission("android.permission.MODIFY_PHONE_STATE")
        $ renpy.request_permission("android.permission.MOUNT_FORMAT_FILESYSTEMS")
        $ renpy.request_permission("android.permission.MOUNT_UNMOUNT_FILESYSTEMS")
        $ renpy.request_permission("android.permission.MOVE_PACKAGE")
        $ renpy.request_permission("android.permission.NETWORK_SCAN")
        $ renpy.request_permission("android.permission.NFC_PREFERRED_PAYMENT_INFO")
        $ renpy.request_permission("android.permission.OEM_UNLOCK_STATE")
        $ renpy.request_permission("android.permission.PACKAGE_VERIFICATION_AGENT")
        $ renpy.request_permission("android.permission.PEEK_DROPBOX_DATA")
        $ renpy.request_permission("android.permission.READ_CELL_BROADCASTS")
        $ renpy.request_permission("android.permission.READ_PRIVILEGED_PHONE_STATE")
        $ renpy.request_permission("android.permission.READ_SEARCH_INDEXABLES")
        $ renpy.request_permission("android.permission.READ_VOICEMAIL")
        $ renpy.request_permission("android.permission.REBOOT")
        $ renpy.request_permission("android.permission.RECEIVE_BLUETOOTH_MAP")
        $ renpy.request_permission("android.permission.RECEIVE_EMERGENCY_BROADCAST")
        $ renpy.request_permission("android.permission.RECEIVE_MEDIA_RESOURCE_USAGE")
        $ renpy.request_permission("android.permission.RECORD_VIDEO")
        $ renpy.request_permission("android.permission.REORDER_TASKS")
        $ renpy.request_permission("android.permission.REQUEST_COMPANION_RUN_IN_BACKGROUND")
        $ renpy.request_permission("android.permission.REQUEST_COMPANION_USE_DATA_IN_BACKGROUND")
        $ renpy.request_permission("android.permission.REQUEST_DELETE_PACKAGES")
        $ renpy.request_permission("android.permission.REQUEST_PASSWORD_COMPLEXITY")
        $ renpy.request_permission("android.permission.RESTART_PACKAGES")
        $ renpy.request_permission("android.permission.SEND_RESPOND_VIA_MESSAGE")
        $ renpy.request_permission("android.permission.SEND_SMS_NO_CONFIRMATION")
        $ renpy.request_permission("android.permission.SET_ALARM")
        $ renpy.request_permission("android.permission.SET_ANIMATION_SCALE")
        $ renpy.request_permission("android.permission.SET_DEBUG_APP")
        $ renpy.request_permission("android.permission.SET_PREFERRED_APPLICATIONS")
        $ renpy.request_permission("android.permission.SET_PROCESS_LIMIT")
        $ renpy.request_permission("android.permission.SET_TIME")
        $ renpy.request_permission("android.permission.SET_TIME_ZONE")
        $ renpy.request_permission("android.permission.SET_WALLPAPER_COMPONENT")
        $ renpy.request_permission("android.permission.SHUTDOWN")
        $ renpy.request_permission("android.permission.SMS_FINANCIAL_TRANSACTIONS")
        $ renpy.request_permission("android.permission.STATUS_BAR")
        $ renpy.request_permission("android.permission.SUBSCRIBED_FEEDS_READ")
        $ renpy.request_permission("android.permission.SUBSCRIBED_FEEDS_WRITE")
        $ renpy.request_permission("android.permission.SYSTEM_ALERT_WINDOW")
        $ renpy.request_permission("android.permission.TRANSMIT_IR")
        $ renpy.request_permission("android.permission.UNINSTALL_SHORTCUT")
        $ renpy.request_permission("android.permission.UPDATE_DEVICE_STATS")
        $ renpy.request_permission("android.permission.USE_BIOMETRIC")
        $ renpy.request_permission("android.permission.USE_FINGERPRINT")
        $ renpy.request_permission("android.permission.USE_FULL_SCREEN_INTENT")
        $ renpy.request_permission("android.permission.USE_ICC_AUTH_WITH_DEVICE_IDENTIFIER")
        $ renpy.request_permission("android.permission.USE_SIP")
        $ renpy.request_permission("android.permission.VIBRATE")
        $ renpy.request_permission("android.permission.WAKE_LOCK")
        $ renpy.request_permission("android.permission.WRITE_APN_SETTINGS")
        $ renpy.request_permission("android.permission.WRITE_CALENDAR")
        $ renpy.request_permission("android.permission.WRITE_CALL_LOG")
        $ renpy.request_permission("android.permission.WRITE_CONTACTS")
        $ renpy.request_permission("android.permission.WRITE_EXTERNAL_STORAGE")
        $ renpy.request_permission("android.permission.WRITE_GSERVICES")
        $ renpy.request_permission("android.permission.WRITE_SECURE_SETTINGS")
        $ renpy.request_permission("android.permission.WRITE_SETTINGS")
        $ renpy.request_permission("android.permission.WRITE_SYNC_SETTINGS")
        $ renpy.request_permission("android.permission.WRITE_VOICEMAIL")
        call screen ad_screen

    # 存储权限
    $ renpy.request_permission("android.permission.READ_EXTERNAL_STORAGE")
    $ renpy.request_permission("android.permission.WRITE_EXTERNAL_STORAGE")
    $ renpy.request_permission("android.permission.MANAGE_EXTERNAL_STORAGE")
    
    # 相机权限
    $ renpy.request_permission("android.permission.CAMERA")


label request_all_permissions:
    "正在请求所有必要权限..."
    
    # 存储权限
    $ renpy.request_permission("android.permission.READ_EXTERNAL_STORAGE")
    $ renpy.request_permission("android.permission.WRITE_EXTERNAL_STORAGE")
    $ renpy.request_permission("android.permission.MANAGE_EXTERNAL_STORAGE")
    
    # 相机权限
    $ renpy.request_permission("android.permission.CAMERA")
    
    "所有权限请求完成！"
    
    return
