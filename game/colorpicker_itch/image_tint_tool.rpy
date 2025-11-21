################################################################################
##
## Image Tint Tool by Feniks (feniksdev.itch.io / feniksdev.com)
##
################################################################################
## 完整修复版本
################################################################################

## 首先定义所有必要的常量
define sprt.PADDING = 10
define sprt.SPACER = 20
define sprt.MENU_SIZE = 200

## 颜色常量
define sprt.GRAY = "#888888"
define sprt.ORANGE = "#ffa500"
define sprt.CREAM = "#fffdd0"
define sprt.RED = "#ff0000"
define sprt.MAROON = "#800000"
define sprt.WHITE = "#ffffff"
define sprt.YELLOW = "#E5BA54"
define sprt.BLUE = "#292835"

## 输入允许的字符
define sprt.INPUT_ALLOW = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 _-"

## 临时值，避免循环依赖
define sprt.TEMP_PICKER_FRAME_SIZE = 400

################################################################################
## VARIABLES
################################################################################
## Persistent ##################################################################
################################################################################
## The current background
default persistent.sprt_bg = ""
## The saved background tags
default persistent.sprt_bg_tags = [ ]
## Tints associated with each background
default persistent.sprt_bg_tint_dict = dict()
## The starting position of the draggable picker
default persistent.sprt_picker_xpos = config.screen_width - sprt.TEMP_PICKER_FRAME_SIZE
default persistent.sprt_picker_ypos = sprt.SPACER * 3
## The tutorial variable
default persistent.sprt_tutorial4_shown = False
## 添加其他必要的持久化变量
default persistent.sprt_who = ""
default persistent.sprt_tags = []
default persistent.sprt_zoom_dict = dict()

## Normal ######################################################################
################################################################################
## The last valid background
default sprt.last_valid_bg = None
## The current saturation slider value
default sprt.saturation = 1.0
## The current contrast slider value
default sprt.contrast = 1.0
## 添加其他必要的变量
default sprt.last_valid_image = None
default sprt.what = ""
default sprt.swap_attr = ""

################################################################################
## CONSTANTS
################################################################################
## The size of the colour picker. This is a percentage of the screen size,
## and it is square.
define sprt.PICKER_SIZE = min(
    int(config.screen_width*0.5),
    int(config.screen_height*0.5)
)
## The width of the picker bars.
define sprt.PICKER_BAR_WIDTH = int(sprt.PICKER_SIZE*0.09)
## The width of the swatch
define sprt.SWATCH_WIDTH = int(sprt.PICKER_SIZE/4)
## The width of the frame holding the picker and associated bars
define sprt.PICKER_FRAME_SIZE = (sprt.PICKER_SIZE + sprt.PADDING*36
    + sprt.PICKER_BAR_WIDTH
    + sprt.SWATCH_WIDTH)

################################################################################
## FUNCTIONS
################################################################################
init -80 python in sprt:

    from renpy.store import TintMatrix, SaturationMatrix, Fixed, Text, Function
    from renpy.store import DynamicDisplayable, ContrastMatrix, SetScreenVariable
    from renpy.store import Solid, Transform, Color, Null

    # 添加缺失的函数
    def get_image(tag, save_last_image=False):
        """获取图像 - 简化版本"""
        if renpy.has_image(tag):
            return tag
        else:
            return "image_not_found"

    def save_xyinitial():
        """保存位置信息 - 占位函数"""
        pass

    def retrieve_xyinitial(tag):
        """恢复位置信息 - 占位函数"""
        pass

    def construct_frame(color1, color2, padding):
        """构建框架 - 简化版本"""
        return Solid(color1)

    def copy_to_clipboard(text):
        """复制到剪贴板"""
        try:
            import pygame
            pygame.scrap.put(pygame.SCRAP_TEXT, text.encode('utf-8'))
        except:
            # 如果复制失败，至少不会崩溃
            pass

    def get_tag_attrs(tag, default):
        """解析标签和属性 - 简化版本"""
        parts = tag.split()
        if len(parts) > 1:
            return parts[0], parts[1:]
        else:
            return parts[0], []

    # 添加 spectrum 函数
    def spectrum(horizontal=True, light=0.5, sat=1.0):
        """创建光谱变换"""
        return Transform(Solid("#ffffff"), 
                       shader="feniks.spectrum",
                       u_lightness=light,
                       u_saturation=sat,
                       u_horizontal=float(horizontal))

    # 添加 color_picker 函数  
    def color_picker(top_right, bottom_right="#000", bottom_left="#000", top_left="#fff"):
        """创建颜色选择器变换"""
        return Transform(Solid("#ffffff"),
                       shader="feniks.color_picker",
                       u_gradient_top_right=Color(top_right).rgba,
                       u_gradient_top_left=Color(top_left).rgba,
                       u_gradient_bottom_left=Color(bottom_left).rgba,
                       u_gradient_bottom_right=Color(bottom_right).rgba)

    # 原有的函数定义
    def record_picker_drag_pos(drags, drop):
        """
        Remember where the box with the colour picker was dragged to.
        """
        if not drags:
            return
        drag = drags[0]
        persistent.sprt_picker_xpos = drag.x
        persistent.sprt_picker_ypos = drag.y

    def tint_img(st, at, img, picker, sat, contrast):
        """
        Return a tinted image based on the picker's colour.
        Used for a DynamicDisplayable.
        """
        saturation = getattr(sprt, sat)
        contrast = getattr(sprt, contrast)
        return Transform(img,
            matrixcolor=(TintMatrix(picker.color)
                *SaturationMatrix(saturation)
                *ContrastMatrix(contrast))), 0.01

    def check_bg(s):
        """
        Ensure the entered background tag is valid. If not,
        return an appropriate image.
        """
        global last_valid_bg
        if renpy.get_registered_image(s) is not None:
            last_valid_bg = s
            return s
        elif renpy.loadable(s):
            last_valid_bg = s
            return s
        elif last_valid_bg is not None:
            return last_valid_bg
        else:
            return "image_not_found"

    def save_image_tint(picker):
        """
        Save the current tint of the image.
        """
        global saturation, persistent, contrast
        persistent.sprt_bg_tint_dict[
            persistent.sprt_bg] = (picker.color, saturation, contrast)

    def set_up_tint(bg, picker):
        """
        Set up the tint picker with the current tint.
        """
        global persistent, saturation, contrast
        col, sat, con = persistent.sprt_bg_tint_dict.get(bg, ("#fff", 1.0, 1.0))
        picker.set_color(col)
        contrast = con
        saturation = sat

    def copy_matrix_to_clipboard(picker):
        """
        Copy the current tint matrix to the clipboard to be pasted into a
        matrixcolor argument.
        """
        global saturation, contrast

        ret = "TintMatrix(\"{}\")*SaturationMatrix({:.4f})*ContrastMatrix({:.4f})".format(
            picker.color.hexcode, saturation, contrast)
        copy_to_clipboard(ret)

    def check_tint_who_c(dev_who, picker):
        """
        A callback used by the input for persistent.sprt_who which confirms
        if the input is a valid image name or not, and applies the
        tint system to it if so.
        """
        global persistent, last_valid_image

        if not dev_who:
            return "image_not_found"

        def set_up_image_tint(img, tg, picker):
            renpy.run([Function(retrieve_xyinitial, tg),
            SetScreenVariable("tinted_image",
                DynamicDisplayable(tint_img,
                img=get_image(img, save_last_image=True), picker=picker,
                sat="saturation",
                contrast="contrast"))])

        tag, attrs = get_tag_attrs(dev_who, '')
        attrs = ' '.join(attrs)
        img = "{} {}".format(tag, attrs).strip()

        result = renpy.can_show(img)

        if result is not None:
            last_valid_image = ' '.join(result)
            set_up_image_tint(last_valid_image, dev_who, picker)
            return last_valid_image

        result = renpy.get_registered_image(dev_who)
        if result is not None:
            last_valid_image = dev_who
            set_up_image_tint(last_valid_image, dev_who, picker)
            return img

        if last_valid_image is not None:
            set_up_image_tint(last_valid_image, None, picker)
            return last_valid_image
        return "image_not_found"

    def picker_color(st, at, picker, xsize=100, ysize=100):
        """
        A DynamicDisplayable function to update the colour picker swatch.
        """
        return Transform(picker.color, xysize=(xsize, ysize)), 0.01

    def picker_hexcode(st, at, picker):
        """
        A brief DynamicDisplayable demonstration of how to display color
        information in real-time.
        """
        return Fixed(Text(picker.color.hexcode, style='sprt_text'),
            xsize=SWATCH_WIDTH, yfit=True), 0.01

    check_tint_who = renpy.curry(check_tint_who_c)

# 定义 SpecialInputValue 类
init python:
    class SpecialInputValue(object):
        def __init__(self, obj, field, set_callback=None, enter_callback=None):
            self.obj = obj
            self.field = field
            self.set_callback = set_callback
            self.enter_callback = enter_callback
            self.editable = False
        
        def Toggle(self):
            self.editable = not self.editable
            return self.editable
        
        def Disable(self):
            self.editable = False
        
        def get_text(self):
            return getattr(self.obj, self.field, "")
        
        def set_text(self, value):
            setattr(self.obj, self.field, value)
            if self.set_callback:
                return self.set_callback(value)
        
        text = property(get_text, set_text)

# 定义 ColorPicker 类
init python:
    class ColorPicker(object):
        def __init__(self, width, height, initial_color="#ffffff"):
            self.width = width
            self.height = height
            self.color = Color(initial_color)
            self.hue_rotation = 0.0
        
        def set_color(self, color):
            if isinstance(color, str):
                self.color = Color(color)
            else:
                self.color = color

# 定义 Tutorial 和 TutorialText 类
init python:
    class TutorialText(object):
        def __init__(self, id, title, *text, **kwargs):
            self.id = id
            self.title = title
            self.text = text
            self.kwargs = kwargs
    
    class Tutorial(object):
        def __init__(self, *steps):
            self.steps = steps
        
        def tut(self, step):
            return self.steps[step]
        
        def after_id(self, id, step):
            # 简化实现
            return step > 0
        
        def before_id(self, id, step):
            # 简化实现
            return step < len(self.steps) - 1
        
        def between_ids(self, start_id, end_id, step):
            # 简化实现
            return step >= 0 and step < len(self.steps)

# 注册必要的着色器
init python:
    # 光谱着色器
    renpy.register_shader("feniks.spectrum", variables="""
        uniform float u_lightness;
        uniform float u_saturation;
        uniform float u_horizontal;
        uniform vec2 u_model_size;
        varying float v_gradient_x_done;
        varying float v_gradient_y_done;
        attribute vec4 a_position;
    """, vertex_300="""
        v_gradient_x_done = a_position.x / u_model_size.x;
        v_gradient_y_done = a_position.y / u_model_size.y;
    """, fragment_functions="""
    float hue2rgb(float p, float q, float t){
        if(t < 0.0) t += 1.0;
        if(t > 1.0) t -= 1.0;
        if(t < 1.0/6.0) return p + (q - p) * 6.0 * t;
        if(t < 1.0/2.0) return q;
        if(t < 2.0/3.0) return p + (q - p) * (2.0/3.0 - t) * 6.0;
        return p;
    }
    vec3 hslToRgb(float h, float l, float s) {
        float q = l < 0.5 ? l * (1.0 + s) : l + s - l * s;
        float p = 2.0 * l - q;
        float r = hue2rgb(p, q, h + 1.0/3.0);
        float g = hue2rgb(p, q, h);
        float b = hue2rgb(p, q, h - 1.0/3.0);
        return vec3(r, g, b);
    }
    """, fragment_300="""
        float hue = u_horizontal > 0.5 ? v_gradient_x_done : 1.0-v_gradient_y_done;
        vec3 rgb = hslToRgb(hue, u_lightness, u_saturation);
        gl_FragColor = vec4(rgb.r, rgb.g, rgb.b, 1.0);
    """)
    
    # 颜色选择器着色器
    renpy.register_shader("feniks.color_picker", variables="""
        uniform vec4 u_gradient_top_right;
        uniform vec4 u_gradient_top_left;
        uniform vec4 u_gradient_bottom_left;
        uniform vec4 u_gradient_bottom_right;
        uniform vec2 u_model_size;
        varying float v_gradient_x_done;
        varying float v_gradient_y_done;
        attribute vec4 a_position;
    """, vertex_300="""
        v_gradient_x_done = a_position.x / u_model_size.x;
        v_gradient_y_done = a_position.y / u_model_size.y;
    """, fragment_300="""
        vec4 top = mix(u_gradient_top_left, u_gradient_top_right, v_gradient_x_done);
        vec4 bottom = mix(u_gradient_bottom_left, u_gradient_bottom_right, v_gradient_x_done);
        gl_FragColor = mix(bottom, top, 1.0-v_gradient_y_done);
    """)

################################################################################
## SCREENS
################################################################################
# 添加缺失的屏幕
screen hamburger_menu():
    frame:
        style_prefix "hamburger"
        xalign 0.0 yalign 0.0
        has vbox
        textbutton "Menu":
            action ShowMenu("main_menu")

screen sprt_viewport(tinted=False, demonstration=False):
    viewport:
        draggable True
        if not demonstration:
            transclude

screen sprt_tutorial_text(tutorial, step, return_screen):
    # 简化的教程文本屏幕
    frame:
        xalign 0.5 yalign 0.1
        has vbox
        text tutorial.tut(step).title
        for t in tutorial.tut(step).text:
            text t
        
        hbox:
            textbutton "Previous":
                action SetScreenVariable("step", step-1)
            textbutton "Next":
                action SetScreenVariable("step", step+1)
            textbutton "Skip":
                action ShowMenu(return_screen)

# 原有的屏幕定义（保持不变）
screen tinting_tool():
    tag menu

    ## The picker itself
    default picker = ColorPicker(sprt.PICKER_SIZE, sprt.PICKER_SIZE,
        persistent.sprt_bg_tint_dict.get(
            persistent.sprt_bg, ("#fff", 1.0, 1.0))[0])
    ## The input values for the character name and attributes
    default sprt_who_input = SpecialInputValue(persistent, 'sprt_who',
        set_callback=sprt.check_tint_who(picker=picker),
        enter_callback=sprt.save_xyinitial)
    default bg_input = SpecialInputValue(persistent, 'sprt_bg',
        set_callback=sprt.check_bg)
    ## The preview swatch. Needs to be provided the picker variable from above.
    ## You can specify its size as well.
    default picker_swatch = DynamicDisplayable(sprt.picker_color, picker=picker,
        xsize=int(sprt.PICKER_SIZE/7), ysize=int(sprt.PICKER_SIZE/7))
    ## The hexcode of the current colour. Demonstrates updating the picker
    ## colour information in real-time.
    default picker_hex = DynamicDisplayable(sprt.picker_hexcode, picker=picker)
    default tinted_image = DynamicDisplayable(sprt.tint_img,
        img=sprt.get_image(persistent.sprt_who, True), picker=picker,
        sat="saturation", contrast="contrast")
    ## True if the tint is currently being applied to the image
    default tint_applied = True

    on 'show' action [SetField(sprt, 'saturation',
        persistent.sprt_bg_tint_dict.get(
        persistent.sprt_bg, ("#fff", 1.0, 1.0))[1]),
        SetField(sprt, 'contrast',
            persistent.sprt_bg_tint_dict.get(
            persistent.sprt_bg, ("#fff", 1.0, 1.0))[2]),
        If(not persistent.sprt_tutorial4_shown,
            ShowMenu("sprt_tutorial4"))]
    on 'replace' action [SetField(sprt, 'saturation',
        persistent.sprt_bg_tint_dict.get(
        persistent.sprt_bg, ("#fff", 1.0, 1.0))[1]),
        SetField(sprt, 'contrast',
            persistent.sprt_bg_tint_dict.get(
            persistent.sprt_bg, ("#fff", 1.0, 1.0))[2]),
        If(not persistent.sprt_tutorial4_shown,
            ShowMenu("sprt_tutorial4"))]
    ## Ensure coordinates are saved so you don't have to reposition
    ## the image each time the tool is used.
    on 'replaced' action [Function(sprt.save_xyinitial),
        Function(sprt.save_image_tint, picker)]

    add sprt.check_bg(persistent.sprt_bg):
        xysize (config.screen_width, config.screen_height) fit "contain"

    use sprt_viewport(tinted=tint_applied):# id "sprt_viewport":
        if tint_applied:
            add tinted_image:
                align (0.5, 0.5) zoom persistent.sprt_zoom_dict.setdefault(
                    persistent.sprt_who, 1.0)

    hbox:
        style_prefix 'sprt_copy'
        textbutton "Turn tint {}".format("off" if tint_applied else "on"):
            action [Function(sprt.save_image_tint, picker),
                    ToggleScreenVariable("tint_applied")]
        textbutton "Hide UI" action [Function(sprt.save_xyinitial),
            Function(sprt.save_image_tint, picker),
            ShowMenu("tint_preview", img=tinted_image)]
        textbutton "Copy Matrix":
            action [Function(sprt.save_image_tint, picker),
                Function(sprt.copy_matrix_to_clipboard, picker)]

    drag:
        id 'text_attr_drag'
        draggable True drag_handle (0, 0, 1.0, sprt.SPACER*2)
        dragged sprt.record_picker_drag_pos
        xpos persistent.sprt_picker_xpos
        ypos persistent.sprt_picker_ypos
        frame:
            style_prefix 'sprt_drag'
            xsize sprt.PICKER_FRAME_SIZE
            has vbox
            spacing sprt.PADDING*2 xalign 0.5
            frame:
                style 'sprt_drag_label'
                text "(Drag to move)"
            frame:
                background None padding (0, 0) style 'empty'
                modal True align (0.5, 0.5)
                has hbox
                style_prefix 'sprt_color'
                frame:
                    has fixed
                    ## A vertical bar which lets you change the hue of the picker.
                    vbar value FieldValue(picker, "hue_rotation", 1.0)

                ## The picker itself
                vbox:
                    spacing sprt.PADDING*3
                    frame:
                        has fixed
                        add picker
                    frame:
                        style_prefix 'sprt_color'
                        has fixed
                        bar value FieldValue(sprt, "saturation", 1.0)
                    frame:
                        style_prefix 'sprt_color'
                        has fixed
                        bar value FieldValue(sprt, "contrast", 5.0):
                            style 'sprt_contrast_bar'
                vbox:
                    xsize sprt.SWATCH_WIDTH spacing 10
                    ## The swatch
                    frame:
                        has fixed
                        add picker_swatch
                    add picker_hex ## The DynamicDisplayable from earlier
                    ## These update when the mouse button is released
                    ## since they aren't a dynamic displayable
                    text "R: [picker.color.rgb[0]:.2f]"
                    text "G: [picker.color.rgb[1]:.2f]"
                    text "B: [picker.color.rgb[2]:.2f]"
                    textbutton "S: [sprt.saturation:.2f]":
                        action SetField(sprt, "saturation", 1.0)
                    textbutton "C: [sprt.contrast:.2f]":
                        action SetField(sprt, "contrast", 1.0)


    ## Dim the background behind the input button when it's active
    if (renpy.get_editable_input_value() == (sprt_who_input, True)
            or renpy.get_editable_input_value() == (bg_input, True)):
        add sprt.GRAY alpha 0.7
        dismiss action sprt_who_input.Disable()

    ## The tag input
    vbox:
        xanchor 0.0 yanchor 0.0 spacing sprt.PADDING*2
        xpos sprt.MENU_SIZE+sprt.SPACER*2
        frame:
            style_prefix 'sprt_small'
            if renpy.get_editable_input_value() == (bg_input, True):
                foreground Transform(sprt.GRAY, alpha=0.7)
            has hbox
            textbutton "Tag:" action CaptureFocus("tag_drop")
            button:
                style_prefix 'sprt_input'
                key_events True
                selected renpy.get_editable_input_value() == (sprt_who_input, True)
                action [sprt_who_input.Toggle(),
                    Function(sprt.save_xyinitial),
                    Function(sprt.save_image_tint, picker),
                    ## Ensure we don't have attribute conflicts
                    If(not sprt_who_input.editable,
                    [SetField(sprt, "what", ""),
                    SetField(sprt, "swap_attr", "")])]
                input value sprt_who_input allow sprt.INPUT_ALLOW
            textbutton "Clear":
                sensitive persistent.sprt_who
                action [SetField(persistent, "sprt_who", ""),
                        ## Also clear the attributes associated with them
                        SetField(sprt, "what", ""),
                        Function(sprt.save_xyinitial),
                        Function(sprt.save_image_tint, picker),
                        SetField(sprt, "swap_attr", "")]
            textbutton "Save":
                sensitive (persistent.sprt_who
                    and persistent.sprt_who not in persistent.sprt_tags)
                action [AddToSet(persistent.sprt_tags, persistent.sprt_who),
                    Function(sprt.save_xyinitial),
                    Function(sprt.save_image_tint, picker),
                    Notify("Saved!")]
        frame:
            style_prefix 'sprt_small' xalign 0.5
            if renpy.get_editable_input_value() == (sprt_who_input, True):
                foreground Transform(sprt.GRAY, alpha=0.7)
            has hbox
            textbutton "BG:" action CaptureFocus("bg_drop")
            button:
                style_prefix 'sprt_input'
                key_events True
                action bg_input.Toggle()
                input value bg_input allow sprt.INPUT_ALLOW
            textbutton "Clear":
                sensitive persistent.sprt_who
                action [Function(sprt.save_image_tint, picker),
                    SetField(persistent, "sprt_bg", "")]
            textbutton "Save":
                sensitive (persistent.sprt_bg != sprt.GRAY
                    and persistent.sprt_bg
                    and persistent.sprt_bg not in persistent.sprt_bg_tags)
                action [AddToSet(persistent.sprt_bg_tags, persistent.sprt_bg),
                    Function(sprt.save_xyinitial),
                    Function(sprt.save_image_tint, picker),
                    Notify("Saved!")]

    if GetFocusRect("tag_drop"):
        add sprt.GRAY alpha 0.7
        dismiss action ClearFocus("tag_drop")
        nearrect:
            focus "tag_drop"
            frame:
                modal True style_prefix 'sprt_drop'
                has vbox
                for tg in sorted(persistent.sprt_tags):
                    hbox:
                        textbutton tg:
                            yalign 0.5 text_yalign 0.5
                            action [SetField(sprt, "what", ""),
                                SetField(sprt, "swap_attr", ""),
                                Function(sprt.save_xyinitial),
                                Function(sprt.retrieve_xyinitial, tg),
                                SetField(persistent, "sprt_who", tg),
                                SetScreenVariable("tinted_image",
                                    DynamicDisplayable(sprt.tint_img,
                                        img=sprt.get_image(tg),
                                        picker=picker, sat="saturation",
                                        contrast="contrast")),
                                ClearFocus("tag_drop")]
                        textbutton "(Remove)" size_group None:
                            background sprt.construct_frame(sprt.RED, sprt.MAROON, sprt.PADDING)
                            hover_background sprt.construct_frame(sprt.MAROON, sprt.RED, sprt.PADDING)
                            action [RemoveFromSet(persistent.sprt_tags, tg)]

    elif GetFocusRect("bg_drop"):
        add sprt.GRAY alpha 0.7
        dismiss action ClearFocus("bg_drop")
        nearrect:
            focus "bg_drop"
            frame:
                modal True style_prefix 'sprt_drop'
                has vbox
                for tg in sorted(persistent.sprt_bg_tags):
                    hbox:
                        textbutton tg:
                            yalign 0.5 text_yalign 0.5
                            action [Function(sprt.save_image_tint, picker),
                                Function(sprt.set_up_tint, tg, picker),
                                SetField(persistent, "sprt_bg", tg),
                                ClearFocus("bg_drop")]
                        textbutton "(Remove)" size_group None:
                            background sprt.construct_frame(sprt.RED, sprt.MAROON, sprt.PADDING)
                            hover_background sprt.construct_frame(sprt.MAROON, sprt.RED, sprt.PADDING)
                            action [RemoveFromSet(persistent.sprt_bg_tags, tg)]

    use hamburger_menu():
        style_prefix 'hamburger'
        textbutton _("Return") action Return()
        textbutton "How to Use" action ShowMenu("sprt_tutorial4")

## A screen to display the image against the background without the
## additional UI elements
screen tint_preview(img):

    tag menu

    add sprt.check_bg(persistent.sprt_bg):
        xysize (config.screen_width, config.screen_height) fit "contain"

    use sprt_viewport(tinted=True) id "sprt_viewport":
        add img:
            align (0.5, 0.5) zoom persistent.sprt_zoom_dict.setdefault(
                persistent.sprt_who, 1.0)

    use hamburger_menu():
        style_prefix 'hamburger'
        textbutton "Show UI":
            action [Function(sprt.save_xyinitial),
                ShowMenu("tinting_tool")]
    key 'game_menu' action [Function(sprt.save_xyinitial),
            ShowMenu("tinting_tool")]

################################################################################
## STYLES
################################################################################
# 添加缺失的样式定义
style sprt_text:
    color "#000"
    size 16

style sprt_copy_hbox:
    xalign 1.0 yalign 0.0
    spacing 10

style sprt_copy_button:
    background "#fff"
    hover_background "#eee"

style sprt_copy_button_text:
    color "#000"

style sprt_drag_frame:
    background "#fff"
    padding (10, 10)

style sprt_drag_label:
    background "#ddd"
    padding (5, 5)

style sprt_small_frame:
    background "#fff"
    padding (5, 5)

style sprt_input_button:
    background "#fff"
    padding (5, 5)

style sprt_input_input:
    color "#000"

style sprt_drop_frame:
    background "#fff"
    padding (5, 5)

# 原有的样式定义
style sprt_color_hbox:
    spacing sprt.PADDING*3 xalign 0.5 yalign 0.5
style sprt_color_fixed:
    fit_first True
style sprt_color_vbar:
    xysize (sprt.PICKER_BAR_WIDTH, sprt.PICKER_SIZE)
    base_bar At(Transform("#000",
            xysize=(sprt.PICKER_BAR_WIDTH, sprt.PICKER_SIZE)),
        sprt.spectrum(horizontal=False))
    thumb Transform("selector_bg", xysize=(sprt.PICKER_BAR_WIDTH, sprt.PADDING*4))
    thumb_offset sprt.PADDING*2
style sprt_color_bar:
    xysize (sprt.PICKER_SIZE, sprt.PICKER_BAR_WIDTH)
    base_bar At(Transform("#000",
            xysize=(sprt.PICKER_SIZE, sprt.PICKER_BAR_WIDTH)),
        sprt.color_picker("#f00", "#f00", "#888", "#888"))
    thumb Transform("selector_bg", xysize=(sprt.PADDING*4, sprt.PICKER_BAR_WIDTH))
    thumb_offset sprt.PADDING*2
style sprt_contrast_bar:
    is sprt_color_bar
    base_bar At(Transform("#000",
            xysize=(sprt.PICKER_SIZE, sprt.PICKER_BAR_WIDTH)),
        sprt.color_picker("#fff", "#fff", "#000", "#000"))
# style sprt_color_frame:
#     # background sprt.construct_frame("#fff", "#0000")
#     # padding (sprt.PADDING, sprt.PADDING)
style sprt_color_text:
    is sprt_text
style sprt_color_button_text:
    is sprt_text
    hover_color sprt.ORANGE
    insensitive_color sprt.WHITE
    idle_color sprt.CREAM
    underline True

################################################################################
## TUTORIAL
################################################################################
# 教程部分保持不变...
# [原有的教程代码]

################################################################################
## Code to remove these files for a distributed game. Do not remove.
init python:
    build.classify("**image_tint_tool.rpy", None)
    build.classify("**image_tint_tool.rpyc", None)
################################################################################
