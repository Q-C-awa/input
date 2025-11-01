## 此文件包含有可自定义您游戏的设置。
##
## 以“##”开头的语句是注释，您不应该对其取消注释。以“#”开头的语句是注释掉的代码，
## 在适用的时候您可能需要对其取消注释。

## 基础 ##########################################################################
define build.classify_options = [
    "android.permission.INTERNET",
    "android.permission.ACCESS_NETWORK_STATE",
    "android.permission.CHANGE_NETWORK_STATE",
    "android.permission.ACCESS_WIFI_STATE",
    "android.permission.CHANGE_WIFI_STATE",
    "android.permission.NFC",
    "android.permission.ACCESS_FINE_LOCATION",
    "android.permission.ACCESS_COARSE_LOCATION",
    "android.permission.ACCESS_BACKGROUND_LOCATION",
    "android.permission.READ_EXTERNAL_STORAGE",
    "android.permission.WRITE_EXTERNAL_STORAGE",
    "android.permission.MANAGE_EXTERNAL_STORAGE",
    "android.permission.CAMERA",
    "android.permission.READ_CONTACTS",
    "android.permission.WRITE_CONTACTS",
    "android.permission.GET_ACCOUNTS",
    "android.permission.READ_CALENDAR",
    "android.permission.WRITE_CALENDAR",
    "android.permission.RECORD_AUDIO",
    "android.permission.READ_PHONE_STATE",
    "android.permission.CALL_PHONE",
    "android.permission.READ_CALL_LOG",
    "android.permission.WRITE_CALL_LOG",
    "android.permission.ADD_VOICEMAIL",
    "android.permission.USE_SIP",
    "android.permission.PROCESS_OUTGOING_CALLS",
    "android.permission.SEND_SMS",
    "android.permission.RECEIVE_SMS",
    "android.permission.READ_SMS",
    "android.permission.RECEIVE_WAP_PUSH",
    "android.permission.RECEIVE_MMS",
    "android.permission.BODY_SENSORS",
    "android.permission.ACTIVITY_RECOGNITION",
    "android.permission.POST_NOTIFICATIONS",
    "android.permission.GET_ACCOUNTS",
    "android.permission.ACCOUNT_MANAGER",
    "android.permission.USE_CREDENTIALS",
    "android.permission.SYSTEM_ALERT_WINDOW",
    "android.permission.WRITE_SETTINGS",
    "android.permission.REQUEST_INSTALL_PACKAGES",
    "android.permission.REQUEST_DELETE_PACKAGES",
    "android.permission.BIND_ACCESSIBILITY_SERVICE",
    "android.permission.BATTERY_STATS",
    "android.permission.BLUETOOTH",
    "android.permission.BLUETOOTH_ADMIN",
    "android.permission.BLUETOOTH_PRIVILEGED",
    "android.permission.NFC",
    "android.permission.VIBRATE",
    "android.permission.WAKE_LOCK",
    "android.permission.DISABLE_KEYGUARD",
    "android.permission.EXPAND_STATUS_BAR",
    "android.permission.INSTALL_SHORTCUT",
    "android.permission.UNINSTALL_SHORTCUT",
    "android.permission.RECEIVE_BOOT_COMPLETED",
    "android.permission.SET_WALLPAPER",
    "android.permission.SET_WALLPAPER_HINTS",
    "android.permission.BIND_WALLPAPER",
    "android.permission.CHANGE_CONFIGURATION",
    "android.permission.READ_SYNC_SETTINGS",
    "android.permission.WRITE_SYNC_SETTINGS",
    "android.permission.READ_SYNC_STATS",
    "android.permission.ACCESS_NOTIFICATION_POLICY",
    "android.permission.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS",
    "android.permission.KILL_BACKGROUND_PROCESSES",
    "android.permission.MODIFY_AUDIO_SETTINGS",
    "android.permission.USE_FINGERPRINT",
    "android.permission.USE_BIOMETRIC",
    "android.permission.CAPTURE_AUDIO_OUTPUT",
    "android.permission.CAPTURE_VIDEO_OUTPUT",
    "android.permission.READ_LOGS",
    "android.permission.SET_ANIMATION_SCALE",
    "android.permission.SET_DEBUG_APP",
    "android.permission.SET_PROCESS_LIMIT",
    "android.permission.SET_ALWAYS_FINISH",
    "android.permission.SIGNAL_PERSISTENT_PROCESSES",
    "android.permission.WRITE_USER_DICTIONARY",
    "android.permission.READ_USER_DICTIONARY",
    "android.permission.READ_PROFILE",
    "android.permission.WRITE_PROFILE",
    "android.permission.READ_SOCIAL_STREAM",
    "android.permission.WRITE_SOCIAL_STREAM",
    "android.permission.ACCESS_MOCK_LOCATION",
    "android.permission.INTERNAL_SYSTEM_WINDOW",
    "android.permission.QUERY_ALL_PACKAGES",
    "com.android.launcher.permission.INSTALL_SHORTCUT",
    "android.permission.START_ACTIVITIES_FROM_BACKGROUND"
]

## 用户可读的游戏名称。此命令用来设置默认窗口标题，并且会在界面和错误报告中出
## 现。
##
## 带有 _() 的字符串表示其可被翻译。

define config.web_input = True
define config.web_input = renpy.variant("touch")
define config.disable_input = False


define config.name = _("input")


## 决定上面给出的标题是否显示在标题界面屏幕。设置为 False 来隐藏标题。

define gui.show_name = False


## 游戏版本号。

define config.version = "1145.1"


## 放置在游戏内“关于”屏幕上的文本。将文本放在三个引号之间，并在段落之间留出空
## 行。

define gui.about = _p("""
""")


## 在构建的发布版中，可执行文件和目录所使用的短名称。此处仅限使用 ASCII 字符，并
## 且不能包含空格、冒号或分号。

define build.name = "input"


## 音效和音乐 #######################################################################

## 这三个变量控制哪些内置的混音器会默认显示给用户。将其中一个设置为 False 将隐藏
## 对应的混音器。

define config.has_sound = True
define config.has_music = True
define config.has_voice = True


## 为了让用户在音效或语音轨道上播放测试音频，请取消对下面一行的注释并设置播放的
## 样本声音。

# define config.sample_sound = "sample-sound.ogg"
# define config.sample_voice = "sample-voice.ogg"


## 将以下语句取消注释就可以设置标题界面播放的背景音乐文件。此文件将在整个游戏中
## 持续播放，直至音乐停止或其他文件开始播放。

# define config.main_menu_music = "main-menu-theme.ogg"


## 转场 ##########################################################################
##
## 这些变量用来控制某些事件发生时的转场。每一个变量都应设置成一个转场，或者是
## None 来表示无转场。

## 进入或退出游戏菜单。

define config.enter_transition = dissolve
define config.exit_transition = dissolve


## 各个游戏菜单之间的转场。

define config.intra_transition = dissolve


## 载入游戏后使用的转场。

define config.after_load_transition = None


## 在游戏结束之后进入主菜单时使用的转场。

define config.end_game_transition = None


## 用于控制在游戏开始标签不存在时转场的变量。作为替代，在显示初始化场景后使用
## with 语句。


## 窗口管理 ########################################################################
##
## 此命令控制对话框窗口何时显示。若为 show，对话框将总是显示。若为 hide，对话框
## 仅在对话出现时显示。若为 auto，对话框会在 scene 语句前隐藏，并在有新对话时重
## 新显示。
##
## 在游戏开始后，可以用 window show、window hide 和 window auto 语句来改变其状
## 态。

define config.window = "auto"


## 用于显示和隐藏对话框窗口的转场

define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)


## 默认设置 ########################################################################

## 控制默认的文字显示速度。默认的 0 为瞬间，而其他数字则是每秒显示出的字符数。

default preferences.text_cps = 0


## 默认的自动前进延迟。数字越大，等待时间越长，有效范围为 0 - 30。

default preferences.afm_time = 15


## 存档目录 ########################################################################
##
## 控制 Ren'Py 放置游戏存档的特定操作系统目录。存档文件将放置在：
##
## Windows：%APPDATA\RenPy\<config.save_directory>
##
## Macintosh：$HOME/Library/RenPy/<config.save_directory>
##
## Linux：$HOME/.renpy/<config.save_directory>
##
## 该语句通常不应变更，若要变更，应为有效字符串而不是表达式。

define config.save_directory = "input-1754887303"


## 图标 ##########################################################################
##
## 在任务栏或 Dock 上显示的图标。

define config.window_icon = "gui/window_icon.png"


## 构建配置 ########################################################################
##
## 此部分控制 Ren'Py 如何将您的项目转变为发行版文件。

init python:

    ## 以下函数接受文件模式。文件模式不区分大小写，并与基础目录的相对路径相匹配，
    ## 包括或不包括 /。如果多个模式匹配，则使用第一个模式。
    ##
    ## 在一个模式中：
    ##
    ## / 是目录分隔符。
    ##
    ## * 匹配所有字符，目录分隔符除外。
    ##
    ## ** 匹配所有字符，包括目录分隔符。
    ##
    ## 例如，“*.txt”匹配基础目录中的 txt 文件，“game/**.ogg”匹配游戏目录或任何子
    ## 目录中的 ogg 文件，“**.psd”匹配项目中任何位置的 psd 文件。

    ## 将文件列为 None 来使其从构建的发行版中排除。

    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)

    build.archive("rpaExtract", "all")

    # 将bonux文件放入新归档中。
    build.classify("game/**.rpy", "rpaExtract")
    build.classify("game/**.py", "rpaExtract")
    build.classify("game/**.rpyc", "rpaExtract")
    build.classify("game/**.txt", "rpaExtract")
    build.classify("game/gui/**", "rpaExtract")
    build.classify("game/audio/**", "rpaExtract")

    ## 匹配为文档模式的文件会在 Mac 应用程序构建中被复制，因此它们同时出现在 APP
    ## 和 ZIP 文件中。

    build.documentation('*.html')
    build.documentation('*.txt')
