init python:
    import pygame
    
    class ColorSolidDisplayable(renpy.Displayable):
        def __init__(self, width, height, step=4, base_color="#ff0000", **kwargs):
            super(ColorSolidDisplayable, self).__init__(**kwargs)
            self.width = width
            self.height = height
            self.step = step
            self.base_color = base_color
            self.colors = self.precompute_colors()
        def precompute_colors(self):
            colors = {}
            step = self.step
            for x in range(0, self.width, step):
                for y in range(0, self.height, step):
                    u = x / float(self.width - 1) if self.width > 1 else 0
                    v = y / float(self.height - 1) if self.height > 1 else 0
                    saturation = u
                    brightness = 1.05 - v
                    r = ((1 - saturation) * brightness + saturation) * brightness
                    g = (1 - saturation) * brightness * brightness
                    b = (1 - saturation) * brightness * brightness
                    r = max(0.0, min(1.0, r))
                    g = max(0.0, min(1.0, g))
                    b = max(0.0, min(1.0, b))
                    colors[(x, y)] = (r, g, b)
            return colors   
        def render(self, width, height, st, at):
            render = renpy.Render(self.width, self.height)
            step = self.step
            for (x, y), color in self.colors.items():
                rect_width = min(step, self.width - x)
                rect_height = min(step, self.height - y)
                color_rect = Solid(
                    Color(rgb=color), 
                    xsize=rect_width, 
                    ysize=rect_height
                )
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
            brightness = 1.05 - v
            r = ((1 - saturation) * brightness + saturation) * brightness
            g = (1 - saturation) * brightness * brightness
            b = (1 - saturation) * brightness * brightness
            r = max(0.0, min(1.0, r))
            g = max(0.0, min(1.0, g))
            b = max(0.0, min(1.0, b))
            return (r, g, b)
    class MousePositionDisplay(renpy.Displayable):
        def __init__(self, target_rect=None, color_displayable=None, **kwargs):
            super(MousePositionDisplay, self).__init__(**kwargs)
            self.mouse_x = 0
            self.mouse_y = 0
            self.target_rect = target_rect 
            self.color_displayable = color_displayable
            self.is_in_target_area = False
            self.current_color = "#000000"
            # 添加颜色代码字符串存储
            self.color_code_string = "#000000"
        def render(self, width, height, st, at):
            render = renpy.Render(width, height)
            try:
                mouse_pos = pygame.mouse.get_pos()
                self.mouse_x, self.mouse_y = mouse_pos
                self.is_in_target_area = False
                if self.target_rect:
                    x, y, w, h = self.target_rect
                    self.is_in_target_area = (x <= self.mouse_x <= x + w and 
                                            y <= self.mouse_y <= y + h)
                if self.is_in_target_area and self.color_displayable:
                    local_x = (self.mouse_x - x) / 0.4
                    local_y = (self.mouse_y - y) / 0.4
                    local_x = max(0, min(self.color_displayable.width - 1, local_x))
                    local_y = max(0, min(self.color_displayable.height - 1, local_y))
                    color = self.color_displayable.get_color_at_position(local_x, local_y)
                    r_hex = int(color[0] * 255)
                    g_hex = int(color[1] * 255)
                    b_hex = int(color[2] * 255)
                    self.current_color = "#{:02x}{:02x}{:02x}".format(r_hex, g_hex, b_hex)
                    # 更新颜色代码字符串
                    self.color_code_string = self.current_color
                    position_text = "鼠标位置: ({}, {})(调试用)".format(self.mouse_x, self.mouse_y)
                    color_text = "颜色: {}".format(self.current_color)
                    position_display = Text(position_text, 
                                        size=24, 
                                        color="#FFFFFF",
                                        outlines=[(2, "#000000", 0, 0)])
                    position_render = renpy.render(position_display, width, height, st, at)
                    render.blit(position_render, (20, 20))
                    color_display = Text(color_text, 
                                    size=24, 
                                    color="#FFFFFF",
                                    outlines=[(2, "#000000", 0, 0)])
                    color_render = renpy.render(color_display, width, height, st, at)
                    render.blit(color_render, (20, 50))
                    border = Frame("gui/button/choice_idle_background.png", 5, 5)
                    border_render = renpy.render(border, w, h, st, at)
                    render.blit(border_render, (x, y))
                    print(position_text + " - 颜色: " + self.current_color + " - 在目标区内")
                else:
                    # 不在目标区域时重置颜色代码
                    self.color_code_string = "#000000"
                    text_display = Text("鼠标不在图像区域内", 
                                    size=24, 
                                    color="#888888",
                                    outlines=[(2, "#000000", 0, 0)])
                    text_render = renpy.render(text_display, width, height, st, at)
                    render.blit(text_render, (20, 20))
            except Exception as e:
                error_text = Text("错误: " + str(e), size=18, color="#FF0000")
                error_render = renpy.render(error_text, width, height, st, at)
                render.blit(error_render, (20, 20))
            renpy.redraw(self, 0.001)
            return render   
        def event(self, ev, x, y, st):
            if ev.type == pygame.MOUSEMOTION:
                self.mouse_x, self.mouse_y = ev.pos
            return None
        # 获取颜色代码字符串
        def get_color_code_string(self):
            return self.color_code_string

default color_solid_size_x = 1000
default color_solid_size_y = 1000
default color_solid_step = 6
default color_solid_size_zoom = 0.4

default image_width = color_solid_size_x * color_solid_size_zoom
default image_height = color_solid_size_y * color_solid_size_zoom
default image_x = (config.screen_width - image_width) / 2
default image_y = (config.screen_height - image_height) / 2

default color_displayable_instance = ColorSolidDisplayable(color_solid_size_x, color_solid_size_y, step = color_solid_step) # 颜色渲染分辨率以及精度
default mouse_display = MousePositionDisplay(
        target_rect=(image_x, image_y, image_width, image_height),
        color_displayable=color_displayable_instance
        )

default current_color_code = mouse_display.get_color_code_string()

image color_solid_displayable_medium_image:
    zoom color_solid_size_zoom
    color_displayable_instance

screen sehuan_screen:
    tag menu
    modal True
    add mouse_display
    add "color_solid_displayable_medium_image" at truecenter
    textbutton "返回" xalign 1.0 yalign 1.0 action Return()
    timer 0.001 repeat True action SetScreenVariable("current_color_code", mouse_display.get_color_code_string())
    hbox:
        spacing 20
        add Solid(current_color_code):
            size(50,50)
        button:
            text "当前颜色代码: [current_color_code]"
            text "确认设置"
            action SetVariable("current_color_code",gui.accent_color)

label sehuan:
    call screen sehuan_screen
