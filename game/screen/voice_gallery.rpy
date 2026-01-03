
init -99 python:
    import json,os 
    voice_data_json = os.path.join(config.gamedir, "voice_data.json")
    def load_json():
        if os.path.exists(voice_data_json):
            try:
                with open(voice_data_json,'r',encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        else:
            with open(voice_data_json,'w',encoding='utf-8') as f:
                json.dump({},f,ensure_ascii=False,indent=4)
            return {}
    def get_voice_data(name):
        data=load_json()
        if name not in data:
            return None
        voice_file=data.get(name)
        if voice_file=="" or voice_file is None:
            return None
        return voice_file
    def save_voice_data(name,voice_file):
        data=load_json()
        data[name]=voice_file
        with open(voice_data_json,'w',encoding='utf-8') as f:
            json.dump(data,f,ensure_ascii=False,indent=4)
screen voice_gallery(voice_file=None):
    tag menu
    add "bg"
    hbox:
        align(0.5,0.5)
        for num in range(0,10):
            $ slot_name = "slot_{}".format(num)
            $ slot_voice = get_voice_data(slot_name)
            imagebutton:
                idle "audio_set"
                hover "audio_set_2"
                selected_idle "audio_set_2"
                selected_hover "audio_set_2"
                if voice_file is None and slot_voice !=None: # 如果访问没有携带参数并且访问处有音频
                    action Play("voice",slot_voice)
                elif voice_file is None and slot_voice == None: # 如果访问没有携带参数并且访问处无音频
                    action NullAction()
                elif voice_file is not None and slot_voice != None: # 如果访问携带参数并且访问处有音频
                    action Confirm("是否覆盖此处音频？",yes=Function(save_voice_data,name=slot_name,voice_file=voice_file),no=NullAction())
                elif voice_file is not None and slot_voice == None: # 如果访问处携带参数并且访问处无音频
                    action Function(save_voice_data,name=slot_name,voice_file=voice_file)
    textbutton "退出" action Return() xalign 0.0 yalign 1.0
