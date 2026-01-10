screen history():
    tag menu
    predict False
    use game_menu(_("历史"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0, spacing=gui.history_spacing):
        style_prefix "history"
        for h in _history_list:
            window:
                has fixed:
                    yfit True
                vbox:
                    $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
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
                    textbutton _("跳转此处"):
                        action Confirm("您确定要返回吗？\n此操作会使为保存的进度{color=#ff4b4b}{k=1.5}{size=55}消失{/size}{/k}{/color}{i}！{/i}", 
                                        yes=RollbackToIdentifier(h.rollback_identifier), 
                                        no=None, confirm_selected=False)
                if h.who:
                    label h.who:
                        style "history_name"
                        substitute False
                        if "color" in h.who_args:
                            text_color h.who_args["color"]
                text what:
                    substitute False
                    style "history_text"
        if not _history_list:
            label _("尚无对话历史记录。")