init python:
    import pygame
    import math
    
    class ColorPickerDisplayable(renpy.Displayable):
        def __init__(self, width=400, height=400, step=6, base_color="#00ff73", **kwargs):
            super(ColorPickerDisplayable, self).__init__(**kwargs)
            self.width = width
            self.height = height
            self.step = step
            self.base_color = Color(base_color)
            self.colors = self.precompute_colors()
            
        def precompute_colors(self):
            colors = {}
            step = self.step
            base_r, base_g, base_b = self.base_color.rgb
            for x in range(0, self.width, step):
                for y in range(0, self.height, step):
                    u = x / float(self.width - 1) if self.width > 1 else 0
                    v = y / float(self.height - 1) if self.height > 1 else 0
                    saturation = u
                    brightness = 1.0 - v
                    gray = Color(rgb=(brightness, brightness, brightness))
                    pure_color = Color(rgb=(
                        base_r * brightness,
                        base_g * brightness, 
                        base_b * brightness
                    ))
                    final_color = gray.interpolate(pure_color, saturation)
                    
                    colors[(x, y)] = final_color
            return colors
                    
        def render(self, width, height, st, at):
            render = renpy.Render(self.width, self.height)
            step = self.step
            for (x, y), color in self.colors.items():
                rect_width = min(step, self.width - x)
                rect_height = min(step, self.height - y)
                color_rect = Solid(color, xsize=rect_width, ysize=rect_height)
                render.place(color_rect, x=x, y=y)
            return render
            
        def event(self, ev, x, y, st):
            return None
            
        def visit(self):
            return []
            
        def get_color_at_position(self, x, y):
            u = x / float(self.width - 1) if self.width > 1 else 0
            v = y / float(self.height - 1) if self.height > 1 else 0
            u = max(0.0, min(1.0, u))
            v = max(0.0, min(1.0, v))
            saturation = u
            brightness = 1.0 - v
            base_r, base_g, base_b = self.base_color.rgb
            gray = Color(rgb=(brightness, brightness, brightness))
            pure_color = Color(rgb=(
                base_r * brightness,
                base_g * brightness, 
                base_b * brightness
            ))
            final_color = gray.interpolate(pure_color, saturation)
            return final_color

    class ColorPickerSliderDisplayable(renpy.Displayable):
        def __init__(self, color_picker, target_rect=None, **kwargs):
            super(ColorPickerSliderDisplayable, self).__init__(**kwargs)
            self.color_picker = color_picker
            self.target_rect = target_rect
            self.current_color = "#000000"
            self.color_code_string = "#000000"
            self.slider_rel_x = 0.5
            self.slider_rel_y = 0.5
            self.dragging = False
        def render(self, width, height, st, at):
            render = renpy.Render(width, height)
            try:
                if self.target_rect:
                    rect_x, rect_y, rect_w, rect_h = self.target_rect
                    color_render = renpy.render(self.color_picker, width, height, st, at)
                    render.blit(color_render, (rect_x, rect_y))
                    slider_x = rect_x + (self.slider_rel_x * rect_w)
                    slider_y = rect_y + (self.slider_rel_y * rect_h)
                    picker_x = self.slider_rel_x * self.color_picker.width
                    picker_y = self.slider_rel_y * self.color_picker.height
                    color = self.color_picker.get_color_at_position(picker_x, picker_y)
                    self.current_color = color.hexcode
                    self.color_code_string = self.current_color
                    slider_size = 15
                    slider_pos_x = slider_x - slider_size // 2
                    slider_pos_y = slider_y - slider_size // 2
                    slider_border = Solid("#000000", xsize=slider_size, ysize=slider_size)
                    slider_border_render = renpy.render(slider_border, width, height, st, at)
                    render.blit(slider_border_render, (slider_pos_x, slider_pos_y))
                    inner_size = slider_size - 4
                    inner_pos_x = slider_pos_x + 2
                    inner_pos_y = slider_pos_y + 2
                    slider_inner = Solid("#FFFFFF", xsize=inner_size, ysize=inner_size)
                    slider_inner_render = renpy.render(slider_inner, width, height, st, at)
                    render.blit(slider_inner_render, (inner_pos_x, inner_pos_y))
                    position_text = "滑块位置: ({:.1f}%, {:.1f}%)".format(
                        self.slider_rel_x * 100, self.slider_rel_y * 100
                    )
                    color_text = "颜色: {}".format(self.current_color)
                    
                    position_display = Text(
                        position_text, 
                        size=24, 
                        color="#FFFFFF",
                        outlines=[(2, "#000000", 0, 0)]
                    )
                    position_render = renpy.render(position_display, width, height, st, at)
                    render.blit(position_render, (20, 20))
                    
                    color_display = Text(
                        color_text, 
                        size=24, 
                        color="#FFFFFF",
                        outlines=[(2, "#000000", 0, 0)]
                    )
                    color_render = renpy.render(color_display, width, height, st, at)
                    render.blit(color_render, (20, 50))
            except Exception as e:
                error_text = Text("错误: " + str(e), size=18, color="#FF0000")
                error_render = renpy.render(error_text, width, height, st, at)
                render.blit(error_render, (20, 20))
            renpy.redraw(self, 0.001)
            return render
        def event(self, ev, x, y, st):
            if not self.target_rect:
                return None
            rect_x, rect_y, rect_w, rect_h = self.target_rect
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if (rect_x <= ev.pos[0] <= rect_x + rect_w and 
                    rect_y <= ev.pos[1] <= rect_y + rect_h):
                    self.slider_rel_x = (ev.pos[0] - rect_x) / rect_w
                    self.slider_rel_y = (ev.pos[1] - rect_y) / rect_h
                    self.slider_rel_x = max(0.0, min(1.0, self.slider_rel_x))
                    self.slider_rel_y = max(0.0, min(1.0, self.slider_rel_y))
                    self.dragging = True
            elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                self.dragging = False
            elif ev.type == pygame.MOUSEMOTION and self.dragging:
                if (rect_x <= ev.pos[0] <= rect_x + rect_w and 
                    rect_y <= ev.pos[1] <= rect_y + rect_h):
                    self.slider_rel_x = (ev.pos[0] - rect_x) / rect_w
                    self.slider_rel_y = (ev.pos[1] - rect_y) / rect_h
                    self.slider_rel_x = max(0.0, min(1.0, self.slider_rel_x))
                    self.slider_rel_y = max(0.0, min(1.0, self.slider_rel_y))
            return None

        def get_color_code_string(self):
            return self.color_code_string

# 默认设置
default color_picker_width = 400
default color_picker_height = 400
default color_picker_step = 6
default base_color = "#00ff2a"

# 计算位置
default picker_width = color_picker_width
default picker_height = color_picker_height
default picker_x = (config.screen_width - picker_width) / 2
default picker_y = (config.screen_height - picker_height) / 2

# 创建颜色选择器实例
default color_picker_instance = ColorPickerDisplayable(
    width=color_picker_width,
    height=color_picker_height,
    step=color_picker_step,
    base_color=base_color
)

# 创建滑块显示实例
default color_slider_display = ColorPickerSliderDisplayable(
    color_picker=color_picker_instance,
    target_rect=(picker_x, picker_y, picker_width, picker_height)
)

default current_color_code = color_slider_display.get_color_code_string()
default color_test = "#ffffff"

# 选择颜色界面
screen color_picker_screen:
    tag menu
    modal True
    add "color_picker_image" at truecenter
    add color_slider_display
    textbutton "返回" xalign 1.0 yalign 1.0 action Return()
    timer 0.01 action [Hide("color_picker_screen"), Show("color_picker_screen")]
    hbox:
        align (0.5, 0.1)
        spacing 20
        add Solid(color_slider_display.get_color_code_string()):
            size(50, 50)
        vbox:
            spacing 5
            text "当前颜色: [color_slider_display.get_color_code_string()]":
                color "#000000"
                size 25
            textbutton "确认选择此颜色" action SetVariable("gui.accent_color", color_slider_display.get_color_code_string())
        text "{b}这个文本是颜色测试{/b}":
            size 50
            color gui.accent_color

# 颜色选择器图像
image color_picker_image:
    color_picker_instance

label sehuan:
    call screen color_picker_screen
    return
