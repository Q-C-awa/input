screen history():

    tag menu

    ## 避免预缓存此屏幕，因为它可能非常大。
    predict False

    use game_menu(_("历史"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0, spacing=gui.history_spacing):

        style_prefix "history"

        for h in _history_list:

            window:

                ## 此代码可确保如果 history_height 为 None 时仍可正常显示条目。
                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"
                        substitute False

                        ## 从 Character 对象中获取叙述角色的文字颜色，如果设置了
                        ## 的话。
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                python:
                    what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                vbox:
                    spacing 10
                    textbutton _("回放语音"):
                        if h.voice.filename == None:
                            action NullAction()
                        else:
                            action Play("voice", h.voice.filename)
                    textbutton _("保存语音"):
                        if h.voice.filename == None:
                            action NullAction()
                        else:
                            action ShowMenu("voice_gallery",voice_file=h.voice.filename)
                    textbutton what:
                        substitute False
                        style "history_text"
                        action Confirm("您确定要返回吗？\n此操作会使为保存的进度{color=#ff4b4b}{k=1.5}{size=55}消失{/size}{/k}{/color}{i}！{/i}", yes=RollbackToIdentifier(h.rollback_identifier), no=None, confirm_selected=False)
            

        if not _history_list:
            label _("尚无对话历史记录。")