
label start:
    scene gete:
        align(0.5, 0.5)
        zoom 0.75
    $ renpy.request_permission("android.permission.POST_NOTIFICATIONS")
    menu:
        "色环插件测试":
            jump sehuan 
        "通知测试1(Hello World!)":
            if not renpy.variant("small"):
                $ notify_windows(box_text = "Hello World!")
            jump start
        "通知测试2(windows)":
            $ notify_windows(box_text = "这是一条来自Ren'Py的Windows系统通知", box_title="Ren'Py通知测试")
            jump start
        "通知测试3":
            $ AndroidNotify(title_text = "测试通知", box_text = "这是一条来自Ren'Py的通知")
            jump start
        "自动下载原神":
            call screen dow_ys
        "视频":
            jump vm_text
        "退出":
            call screen quit_screen_qc
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