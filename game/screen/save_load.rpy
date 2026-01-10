screen save():
    tag menu
    use file_slots(_("保存"))
screen load():
    tag menu
    use file_slots(_("读取游戏"))
default n = 0
screen file_slots(title):
    default page_name_value = FilePageNameInputValue(pattern=_("第 {} 页"), auto=_("自动存档"), quick=_("快速存档"))
    use game_menu(title):
        fixed:
            ## 此代码确保输入控件在任意按钮执行前可以获取 enter 事件。
            order_reverse True
            ## 页面名称，可以通过单击按钮进行编辑。
            button:
                style "page_label"
                key_events True
                xalign 0.5
                action page_name_value.Toggle()
                input:
                    style "page_label_text"
                    value page_name_value
            ## 存档位网格。
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"
                xalign 0.5
                yalign 0.5
                spacing gui.slot_spacing
                $ say_what = _last_say_what or ""
                $ display_text = say_what[:15] + "..." if len(say_what) > 15 else say_what
                for i in range(gui.file_slot_cols * gui.file_slot_rows):
                    $ slot = i + 1
                    button:
                        action [SetVariable("save_name", display_text),FileAction(slot)]
                        vbox:
                            add FileScreenshot(slot) xalign 0.5
                            text FileTime(slot, format=_("{#file_time}%Y-%m-%d %H:%M"), empty=_("空存档位")):
                                style "slot_time_text"
                            text FileSaveName(slot):
                                style "slot_name_text"
                            key "save_delete" action FileDelete(slot)
            ## 用于访问其他页面的按钮。
            vbox:
                style_prefix "page"
                xalign 0.5
                yalign 1.0
                hbox:
                    xalign 0.5
                    spacing gui.page_spacing
                    textbutton _("<") action FilePagePrevious()
                    key "save_page_prev" action FilePagePrevious()
                    if config.has_autosave:
                        textbutton _("{#auto_page}A") action FilePage("auto")
                    if config.has_quicksave:
                        textbutton _("{#quick_page}Q") action FilePage("quick")
                    ## range(1, 10) 给出 1 到 9 之间的数字。
                    for page in range(1, 10):
                        textbutton "[page]" action FilePage(page)
                    textbutton _(">") action FilePageNext()
                    key "save_page_next" action FilePageNext()
