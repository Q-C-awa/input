init -99 python:
    class Image_list:
        def __init__(self,name=None,images=None,tag=None):
            self.images = images
            self.name = name
            self.tag = tag
    Character_list = [
        Image_list(name="狩叶",images="lh/狩叶.png",tag="Character"),
        Image_list(name="音理",images="lh/音理 (1).png",tag="Character"),
        Image_list(name="音理",images="lh/音理 (2).png",tag="Character"),
        Image_list(name="真白",images="lh/真白.png",tag="Character"),
        Image_list(name="小忆",images="lh/小忆-连衣裙.png",tag="Character"),
        Image_list(name="小忆",images="lh/小忆-旅行.png",tag="Character"),
        Image_list(name="小忆",images="lh/小忆-浴衣.png",tag="Character"),
        Image_list(name="言叶",images="lh/言叶-餐服.png",tag="Character"),
        Image_list(name="言叶",images="lh/言叶-连衣裙(2).png",tag="Character"),
        Image_list(name="言叶",images="lh/言叶-连衣裙（3）.png",tag="Character"),
        Image_list(name="言叶",images="lh/言叶-浴衣.png",tag="Character"),
        Image_list(name="言叶",images="lh/言叶-餐服.png",tag="Character"),
                ]
    BG_list = [
        Image_list(name="街道",images="bg/de.png",tag="BackGround"),
        Image_list(name="医院—下午",images="bg/hospital_a.jpg",tag="BackGround"),
        Image_list(name="医院—下午",images="bg/hospital_room_a.jpg",tag="BackGround"),
        Image_list(name="医院—早上",images="bg/hospital_room_m.jpg",tag="BackGround"),
        Image_list(name="医院—夜晚",images="bg/hospital_room_n.jpg",tag="BackGround"),
        Image_list(name="房间——下午",images="bg/nvfe_room_a.png",tag="BackGround"),
        Image_list(name="房间——早上",images="bg/nvfe_room_m.png",tag="BackGround"),
        Image_list(name="房间——晚上",images="bg/nvfe_room_w.png",tag="BackGround"),
        Image_list(name="办公室",images="bg/office.jpg",tag="BackGround"),
        Image_list(name="街道—1",images="bg/outdoor_1.jpg",tag="BackGround"),
        Image_list(name="街道—2",images="bg/outdoor_2 .jpg",tag="BackGround"),
        Image_list(name="街道—3",images="bg/outdoor_3.jpg",tag="BackGround"),
        Image_list(name="街道—4",images="bg/outdoor_4.jpg",tag="BackGround"),
        Image_list(name="街道—5",images="bg/outdoor_5.jpg",tag="BackGround"),
        Image_list(name="街道—6",images="bg/outdoor_5.jpg",tag="BackGround"),
        Image_list(name="街道—7",images="bg/outdoor_6.png",tag="BackGround"),
        Image_list(name="街道—8",images="bg/outdoor_7.jpg",tag="BackGround"),
        Image_list(name="街道—9",images="bg/outdoor_8.jpg",tag="BackGround"),
        Image_list(name="街道—10",images="bg/outdoor_9.jpg",tag="BackGround"),
        Image_list(name="餐厅—1",images="bg/restaurant_m.jpg",tag="BackGround"),
        Image_list(name="餐厅—2",images="bg/restaurant_m_2.jpg",tag="BackGround"),
        ]
    def increase_index(index,list):
        if index+1<=(len(list)-1):
            return index+1
        else:
            return 0
    def decrease_index(index,list):
        if index-1>=0:
            return index-1
        else:
            return len(list)-1
image bg:
    size(1920,1080)
    Solid("#17ffb2")
default Character_list_index = 0
default BG_list_index = 0
default zoom_move = 1.5
screen Character_Art_Appreciation():
    tag menu
    add BG_list[BG_list_index].images
    drag:
        align(0.5,0.5)
        drag_handle(0.5, 0.5, 1920, 1080)
        vbox:    
            add Character_list[Character_list_index].images:
                    zoom zoom_move
            key "mousedown_4" action SetVariable("zoom_move",zoom_move+0.01)
            key "mousedown_5" action SetVariable("zoom_move",zoom_move-0.01)     
    hbox:
        spacing 20
        vbox:
            text Character_list[Character_list_index].name
            spacing 20
            text"角色立绘调整"
            textbutton "+1" action SetVariable("Character_list_index",increase_index(Character_list_index,Character_list))
            textbutton "-1" action SetVariable("Character_list_index",decrease_index(Character_list_index,Character_list))
        vbox:
            text BG_list[BG_list_index].name
            spacing 20
            text"背景调整"
            textbutton "+1" action SetVariable("BG_list_index",increase_index(BG_list_index,BG_list))
            textbutton "-1" action SetVariable("BG_list_index",decrease_index(BG_list_index,BG_list))
    textbutton "退出" action Return() xalign 0.0 yalign 1.0
    
