image csauchas = "cg/CG6_3.jpg"

label start:
    show csauchas at random_motion
    menu:
        "输入测试1":
            jump input_test
        "权限调用测试":
            jump permission_test
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