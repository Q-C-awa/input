image locked = Composite((1920,1080),(0, 0), Solid("#f1c5c5"))
init -99 python:
    # 代码本身就是注释
    class Ga_cg():
        def __init__(self,tag,images,condition=None,transform=Dissolve(0.25)):
            self.images = images
            self.condition = condition
            self.transform = transform
            self.tag = tag
    CG_list = [
        Ga_cg(tag="p1", images=["CG1_1", "CG1_2", "CG1_3", "CG1_4", "CG1_5", "CG1_6", "CG1_7", "CG1_8"]),
        Ga_cg(tag="p2", images=["CG2_1", "CG2_2"]),
        Ga_cg(tag="p3", images=["CG3_1"]),
        Ga_cg(tag="p4", images=["CG4_1"]),
        Ga_cg(tag="p5", images=["CG5_1", "CG5_2", "CG5_3"]),
        Ga_cg(tag="p6", images=["CG6_0", "CG6_1", "CG6_2", "CG6_3"]),
        Ga_cg(tag="p7", images=["CG7_1", "CG7_2"]),
        Ga_cg(tag="p8", images=["CG8_1", "CG8_2"]),
        Ga_cg(tag="p9", images=["CG9_1"]),
        Ga_cg(tag="p10", images=["CG10_1", "CG10_2"]),
        Ga_cg(tag="p11", images=["CG11_1", "CG11_2"]),
        Ga_cg(tag="p12", images=["CG12_1", "CG12_2"]),
        Ga_cg(tag="p13", images=["CG13_1", "CG13_2"]),
        Ga_cg(tag="p14", images=["CG14_1", "CG14_2"]),
        Ga_cg(tag="p15", images=["CG15_1", "CG15_2", "CG15_3"]),
        Ga_cg(tag="p16", images=["CG16_1", "CG16_2", "CG16_3"])
        ]
    ga = Gallery()
    ga.locked_button = Composite((1920,1080), (0, 0), Solid("#f5f5f5"), (0, 0), "locked")
    for CG_num in CG_list:
        ga.button(CG_num.tag)
        if CG_num.condition is not None:
            ga.condition(f"{str(CG_num.condition)}")
        for image_num in CG_num.images:
            ga.unlock(image_num)
        for image_num in CG_num.images:
            ga.image(image_num)
        if CG_num.transform is not None:
            ga.transition = CG_num.transform
    ga.button("locked")
    ga.unlock_image("locked")
    def page_next():
        global gallery_page_index, start_page, end_page
        (gallery_page_index := gallery_page_index + 1) if (gallery_page_index + 1) * per_button < len(CG_list) else (gallery_page_index := 0)
    def page_last():
        global gallery_page_index
        (gallery_page_index := gallery_page_index - 1) if gallery_page_index > 0 else (gallery_page_index := (len(CG_list) - 1) // per_button)
    ga.locked_button = Composite((1920,1080),(0, 0), Solid("#f5f5f5"),(0, 0), "locked")
init python:
    gallery_page_index = 0
    CG_list_index = 0
    Gallery_gird_width = 3
    Gallery_gird_hight = 2
    per_button = Gallery_gird_hight*Gallery_gird_width
screen gallery():
    tag menu 
    add "cg/CG9_1.jpg"
    $ start_page = gallery_page_index * per_button
    $ end_page = min(start_page+per_button,len(CG_list))
    grid Gallery_gird_width Gallery_gird_hight:
        xfill True
        yfill True
        spacing 25
        for CG_list_index in range(start_page, end_page):
            add ga.make_button(name=CG_list[CG_list_index].tag,unlocked=CG_list[CG_list_index].images[0],xalign=0.5, yalign=0.5):
                zoom 0.3
    vbox:
        spacing 50
        textbutton _("下一页") action Function(page_next)
        text _("[gallery_page_index+1]页"):
            color "#000000"
        textbutton _("上一页") action Function(page_last)
        textbutton _("退出") action Return()
