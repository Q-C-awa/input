
define nvfe = Character("夜涟",callback = nvfe_sound_machine)
init -99 python:
    renpy.music.register_channel("Typewriter_channel","Typewriter",loop=True)
    def nvfe_sound_machine(event, interact=True, **kwargs):
        if event == "begin":
        # 在对话开始时播放循环音效
            renpy.sound.play("audio/O1.ogg", loop=True, channel="Typewriter_channel")
        elif event == "slow_done" or event == "end":
            # 在对话结束时停止音效
            renpy.sound.stop(channel="Typewriter_channel")
label start:
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
        "多语言测试":
            jump multi_language_test
        "退出":
            call screen quit_screen_qc
label multi_language_test:
    menu:
        "语音":
            voice "1_1.wav"
            nvfe "是雪融玲兰的香气，对吧？"
            voice "1_2.wav"
            nvfe "哦？你好？"
            voice "1_3.wav"
            nvfe "心跳加速，瞳孔扩张，饲养员的惊吓反应，比预测的更加夸张呢。"
            voice "1_4.wav"
            nvfe "根据人类社交礼仪--"
            jump multi_language_test
