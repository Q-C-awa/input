
label start:
    show weihua
    $ renpy.request_permission("android.permission.POST_NOTIFICATIONS")
    menu:
        "退出":
            call screen quit_screen_qc
        "sejai":
            jump sehuan 
        "通知测试":
            if not renpy.variant("small"):
                $ notify_windows(box_text = "Hello World!")
            jump start
        "消息测试":
            jump start
        "自动下载原神":
            call screen dow_ys
        "视频":
            jump vm_text
        "安卓通知测试":
            $ AndroidNotify(title_text="测试通知", box_text="这是一个来自Ren'Py的安卓通知")
image da_movie_movie = Movie(play="v1.webm")
label vm_text:
    show da_movie_movie
    "cuhiuch"
label splashscreen:
    # call screen dow_ys
    return
screen dow_ys:
    if not renpy.variant("small"):
        on "show":
            action OpenURL("https://ys-api.mihoyo.com/event/download_porter/link/ys_cn/official/pc_default")
    else:
        on "show":
            action OpenURL("https://ys-api.mihoyo.com/event/download_porter/link/ys_cn/official/android_default")
    on "show":
        action ShowMenu("main_menu")