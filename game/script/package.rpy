init -999 python:
    class pac_items():
        def __init__(self,name,pic,effects):
            self.name = name
            self.pic = pic
            self.effects = effects
        def adding(name):
            for i in range(5):
                if len(ownlist[i]) < 5:
                    ownlist[i].append(name)
                    break
        def list_debug():
            print(ownlist)
            
define line1 = ["aaa","bbb","ccc"]
define line2 = ["aaa"]
define line3 = []
define line4 = []
define line5 = ["aaa"]
define ownlist = [line1,line2,line3,line4,line5]
    
screen package_qc():
    tag menu
    modal True
    frame:
        xysize(1920,1080)
        background Solid("#ffffff")
        add "11_movie"
        vbox: # 树向排列
            spacing 20
            at truecenter
            for per_y in ownlist: # 每一行的数目,per_y是ownlist里面的子列表
                hbox: # 横向排列
                    spacing 20
                    for per_x in range(len(ownlist)): # per_x是ownlist里面的子列表的内容
                        $ content = ownlist[ownlist.index(per_y)][per_x] if per_x < len(ownlist[ownlist.index(per_y)]) else None # 获取对应位置的列表的内容，如果没用内容就是None
                        if content != None:
                            imagebutton:
                                idle Solid("#00ff37")
                                xysize (50,50)
                                action Function(pac_items.adding, "new_item")
                        else:
                            imagebutton:
                                idle Solid("#ff0000")
                                xysize (50,50)
                                action Function(pac_items.adding, "new_item")
    vbox:
        spacing 50
        at left
        textbutton "测试" action Function(pac_items.list_debug)
        textbutton "退出" action Return()