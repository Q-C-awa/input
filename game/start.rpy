
define nvfe = Character("夜涟",callback = nvfe_sound_machine)
init -99 python:
    renpy.music.register_channel("Typewriter_channel","Typewriter",loop=True)
    def nvfe_sound_machine(event, interact=True, **kwargs):
        print(_get_voice_info().__dict__)
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
        "相册调用测试":
            jump album_test
        "多文本测试":
            jump more
        "界面转场":
            jump 界面转场
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

label more:
    "我怕死，但不讨厌死亡。"
    "太空中比死亡可怕的事情多的去了。"
    "比如把人的意识囚禁起来，使其永远无法死去的刑罚。"
    "那种东西，光是想想就让人不寒而栗。"
    "死亡不一样，死亡是一种解脱。"
    "只是…"
    "就这样死在一个看不到人的角落实在太窝囊了。"
    "我不想就这样死掉。"
    "我还有好多事情想做。"
    "我还孤身一人。"
    "我还没有明白真正的人生为何物。"
    "明明好不容易才逃离那个地方。"
    "不想就这样死掉啊……"
    "……"
    "…"
    "不知过了多久，我的耳畔响起了心跳声。"
    "这是谁的心跳声？"
    "是我的心跳么？"
    "不，我应该已经死了才对。"
    "可是，这里还会有谁呢？"
    "似乎是身体为了回应我的疑惑，温度逐渐涌上心头。"
    "这是我的身体。"
    "这是我的心跳。"
    "这是我的余温。"
    "我醒了，我的意识正在恢复。"
    "我没有死在永夜的银河之中。"
    "我出于本能地睁开双眼。"
    jump start
label 界面转场:
    scene baihua:
        zoom 0.4
    "界面转场测试show"
    show screen_switch_2
    pause 
    "界面转场测试hide"
    hide screen_switch_2
    pause 
    "界面转场测试show"
    show screen_switch
    pause 
    "界面转场测试hide"
    hide screen_switch
    pause 
    "界面转场测试show"
    show screen_switch_2
    pause 
    "界面转场测试hide"
    hide screen_switch_2
    pause 
    "界面转场测试show"
    show screen_switch
    pause 
    "界面转场测试hide"
    hide screen_switch
    pause
    "界面转场测试show"
    show screen_switch_2
    pause 
    "界面转场测试hide"
    hide screen_switch_2
    pause 
    "界面转场测试show"
    show screen_switch
    pause 
    "界面转场测试hide"
    hide screen_switch
    jump start
