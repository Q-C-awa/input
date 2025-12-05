
label start:
    show weihua
    menu:
        "退出":
            call screen quit_screen_qc
        "sejai":
            jump sehuan 
        "通知测试":
            $ notify_windows(box_text = "Hello World!")
            jump start
        "消息测试":
            jump start
        "自动下载原神":
            call screen dow_ys
label splashscreen:
    call screen dow_ys
    return
screen dow_ys:
    if not renpy.variant("small"):
        timer 0.0001 action OpenURL("https://ys-api.mihoyo.com/event/download_porter/link/ys_cn/official/pc_default")
    else:
        timer 0.0001 action OpenURL("https://ys-api.mihoyo.com/event/download_porter/link/ys_cn/official/android_default")
    timer 0.01 action ShowMenu("main_menu")