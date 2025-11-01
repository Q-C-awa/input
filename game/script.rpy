image csauchas = "cg/CG6_3.jpg"

# 定义广告图片
image ad_1 = "ad_1.png"
image ad_2 = "ad_2.png"
image ad_3 = "ad_3.png"
image ad_4 = "ad_4.png"

init -99 python:
    class Adlist:
        def __init__(self, image_name, url):
            self.image = image_name  # 存储图片名称
            self.url = url

# 广告列表
default ad_list = [
    Adlist("ad_1", "https://space.bilibili.com/582755147"),
    Adlist("ad_2", "https://space.bilibili.com/378904108"), 
    Adlist("ad_3", "https://space.bilibili.com/1733740438"),
    Adlist("ad_4", "https://space.bilibili.com/402102137")
]

screen ad_screen():
    tag menu 
    zorder 100
    
    # 在屏幕内随机选择广告
    default current_ad = renpy.random.choice(ad_list)
    
    # 全屏按钮，点击任意位置跳转
    button:
        action [
            OpenURL(current_ad.url),
            Return("ad_clicked")
        ]
        
        # 使用vbox排列文本和图片
        vbox:
            align (0.5, 0.5)
            spacing 20
            
            text "{size=50}点击继续！{/size}":
                align (0.5, 0.5)
                color "#FFFFFF"
                outlines [(2, "#000000", 0, 0)]
            
            # 这里改为使用 current_ad.image
            add current_ad.image:
                zoom 0.7
                align (0.5, 0.5)



init python:
    def show_code(func):
        import inspect
        print(inspect.getsource(func))
label input_test:
    "输入1"
    python:
        input_1 = renpy.input("请输入内容1：", length=20)
    "输入的内容1是：[input_1]"

    python:
        input_2 = renpy.input("请输入内容2：", length=20)
    "输入的内容2是：[input_2]"
    "输入测试3"
    python:
        input_3 = renpy.input("请输入内容3：", length=20)
    "输入的内容3是：[input_3]"
    "输入测试4"
    python:
        input_4 = renpy.input("请输入内容4：", length=20)
    "输入的内容4是：[input_4]"
    "输入测试5"
    python:
        input_5 = renpy.input("请输入内容5：", length=20)
    "输入的内容5是：[input_5]"
    "输入测试6"
    python:
        input_6 = renpy.input("请输入内容6：", length=20)
    "输入的内容6是：[input_6]"
    "输入测试7"
    python:
        input_7 = renpy.input("请输入内容7：", length=20)
    "输入的内容7是：[input_7]"
label splashscreen:
    # 存储权限
    $ renpy.request_permission("android.permission.READ_EXTERNAL_STORAGE")
    $ renpy.request_permission("android.permission.WRITE_EXTERNAL_STORAGE")
    $ renpy.request_permission("android.permission.MANAGE_EXTERNAL_STORAGE")
    
    # 相机权限
    $ renpy.request_permission("android.permission.CAMERA")

label request_all_permissions:
    "正在请求所有必要权限..."
    
    # 存储权限
    $ renpy.request_permission("android.permission.READ_EXTERNAL_STORAGE")
    $ renpy.request_permission("android.permission.WRITE_EXTERNAL_STORAGE")
    $ renpy.request_permission("android.permission.MANAGE_EXTERNAL_STORAGE")
    
    # 相机权限
    $ renpy.request_permission("android.permission.CAMERA")
    
    "所有权限请求完成！"
    
    return
