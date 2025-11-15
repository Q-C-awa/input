init python:
    import pygame
    import math
    
    # 注册圆环取色器着色器
    renpy.register_shader("color_round_picker", variables="""
        uniform vec2 u_model_size;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
    """, vertex_100="""
        v_tex_coord = a_tex_coord;
    """, fragment_300="""
        precision highp float;
        vec2 uv = v_tex_coord;
        vec2 center = vec2(0.5, 0.5);
        float dist = distance(uv, center);
        float outer_radius = 0.4;
        float inner_radius = 0.1;
        
        if(dist >= inner_radius && dist <= outer_radius) {
            float angle = atan(center.y - uv.y , center.x - uv.x); 
            float hue = (angle + 3.141592653589793) / (2.0 * 3.141592653589793);
            float h = hue * 6.0;
            int i = int(floor(h));
            float f = h - float(i);
            float p = 0.0;
            float q = 1.0 - f;
            float t = f;
            
            if (i == 0) {
                gl_FragColor = vec4(1.0, t, p, 1.0);
            } else if (i == 1) {
                gl_FragColor = vec4(q, 1.0, p, 1.0);
            } else if (i == 2) {
                gl_FragColor = vec4(p, 1.0, t, 1.0);
            } else if (i == 3) {
                gl_FragColor = vec4(p, q, 1.0, 1.0);
            } else if (i == 4) {
                gl_FragColor = vec4(t, p, 1.0, 1.0);
            } else {
                gl_FragColor = vec4(1.0, p, q, 1.0);
            }
        } else {
            gl_FragColor = vec4(0.0, 0.0, 0.0, 0.0);
        }
    """)
    
    class ColorPicker(renpy.Displayable):
        def __init__(self, width=800, height=800, xpos=0.5, ypos=0.5, color_picker_zoom=1.0, step=6,**kwargs):
            super(ColorPicker, self).__init__(**kwargs)
            self.color_picker_zoom = color_picker_zoom
            self.width = int(width * color_picker_zoom)
            self.height = int(height * color_picker_zoom)
            self.xpos = xpos
            self.ypos = ypos
            self.center_x = self.width // 2
            self.center_y = self.height // 2
            base_radius = min(width, height) // 2
            self.outer_radius = int(base_radius * 0.98 * color_picker_zoom) 
            self.inner_radius = int(base_radius * 0.74 * color_picker_zoom)
            self.slider_radius = (self.inner_radius + self.outer_radius) // 2
            self.rect_width = int(420 * color_picker_zoom)
            self.rect_height = int(420 * color_picker_zoom)
            self.rect_step = step
            self.rect_x = (self.width - self.rect_width) // 2
            self.rect_y = (self.height - self.rect_height) // 2
            self.angle = 0.0 
            self.slider_rel_x = 0.5 
            self.slider_rel_y = 0.5
            self.dragging_ring = False
            self.dragging_rect = False
            self.base_color = "#ff0000" 
            self.final_color = "#ff0000" 
            
        def get_hue_color(self, angle):
            hue = angle / (2 * math.pi)
            h = hue * 6.0
            i = int(math.floor(h))
            f = h - i
            p = 0.0
            q = 1.0 - f
            t = f
            if i == 0:
                r, g, b = 1.0, t, p
            elif i == 1:
                r, g, b = q, 1.0, p
            elif i == 2:
                r, g, b = p, 1.0, t
            elif i == 3:
                r, g, b = p, q, 1.0
            elif i == 4:
                r, g, b = t, p, 1.0
            else:
                r, g, b = 1.0, p, q
            return Color(rgb=(r, g, b))
            
        def get_rect_color(self, x, y):
            u = max(0.0, min(1.0, x / float(self.rect_width - 1) if self.rect_width > 1 else 0))
            v = max(0.0, min(1.0, y / float(self.rect_height - 1) if self.rect_height > 1 else 0))
            saturation = u
            brightness = 1.02 - v
            base_r, base_g, base_b = Color(self.base_color).rgb
            gray = Color(rgb=(brightness, brightness, brightness))
            pure_color = Color(rgb=(
                base_r * brightness,
                base_g * brightness, 
                base_b * brightness
            ))
            return gray.interpolate(pure_color, saturation)
            
        def precompute_rect_colors(self):
            colors = {}
            base_r, base_g, base_b = Color(self.base_color).rgb
            for x in range(0, self.rect_width, self.rect_step):
                for y in range(0, self.rect_height, self.rect_step):
                    u = x / float(self.rect_width - 1) if self.rect_width > 1 else 0
                    v = y / float(self.rect_height - 1) if self.rect_height > 1 else 0
                    saturation = u
                    brightness = 1.0 - v
                    gray = Color(rgb=(brightness, brightness, brightness))
                    pure_color = Color(rgb=(
                        base_r * brightness,
                        base_g * brightness, 
                        base_b * brightness
                    ))
                    colors[(x, y)] = gray.interpolate(pure_color, saturation)
            return colors
            
        def render(self, width, height, st, at):
            screen_width, screen_height = renpy.get_physical_size()
            actual_x = int(self.xpos * (screen_width - self.width))
            actual_y = int(self.ypos * (screen_height - self.height))
            render = renpy.Render(width, height)
            shader_display = Transform(Solid("#ffffff"), 
                                    shader="color_round_picker", 
                                    mesh=True,
                                    xsize=self.width, 
                                    ysize=self.height)
            shader_render = renpy.render(shader_display, width, height, st, at)
            render.blit(shader_render, (actual_x, actual_y))
            self.base_color = self.get_hue_color(self.angle).hexcode
            rect_colors = self.precompute_rect_colors()
            for (x, y), color in rect_colors.items():
                rect_width = min(self.rect_step, self.rect_width - x)
                rect_height = min(self.rect_step, self.rect_height - y)
                color_rect = Solid(color, xsize=rect_width, ysize=rect_height)
                color_render = renpy.render(color_rect, width, height, st, at)
                render.blit(color_render, (actual_x + self.rect_x + x, actual_y + self.rect_y + y))
            rect_slider_x = actual_x + self.rect_x + (self.slider_rel_x * self.rect_width)
            rect_slider_y = actual_y + self.rect_y + (self.slider_rel_y * self.rect_height)
            self.final_color = self.get_rect_color(
                self.slider_rel_x * self.rect_width,
                self.slider_rel_y * self.rect_height
            ).hexcode
            ring_slider_x = actual_x + self.center_x + self.slider_radius * math.cos(self.angle)
            ring_slider_y = actual_y + self.center_y + self.slider_radius * math.sin(self.angle)
            slider_size = int(min(self.width, self.height) * 0.15 * self.color_picker_zoom)  # 滑块大小
            slider_pos_x = ring_slider_x - slider_size // 2
            slider_pos_y = ring_slider_y - slider_size // 2
            slider_border = Solid("#000000", xsize=slider_size, ysize=slider_size)
            slider_border_render = renpy.render(slider_border, width, height, st, at)
            render.blit(slider_border_render, (slider_pos_x, slider_pos_y))
            inner_size = slider_size - 4
            inner_pos_x = slider_pos_x + 2
            inner_pos_y = slider_pos_y + 2
            slider_inner = Solid("#FFFFFF", xsize=inner_size, ysize=inner_size)
            slider_inner_render = renpy.render(slider_inner, width, height, st, at)
            render.blit(slider_inner_render, (inner_pos_x, inner_pos_y))
            rect_slider_size = int(min(self.width, self.height) * 0.05 * self.color_picker_zoom) 
            rect_slider_pos_x = rect_slider_x - rect_slider_size // 2
            rect_slider_pos_y = rect_slider_y - rect_slider_size // 2
            rect_slider_border = Solid("#000000", xsize=rect_slider_size, ysize=rect_slider_size)
            rect_slider_border_render = renpy.render(rect_slider_border, width, height, st, at)
            render.blit(rect_slider_border_render, (rect_slider_pos_x, rect_slider_pos_y))
            rect_inner_size = rect_slider_size - 4
            rect_inner_pos_x = rect_slider_pos_x + 2
            rect_inner_pos_y = rect_slider_pos_y + 2
            rect_slider_inner = Solid("#FFFFFF", xsize=rect_inner_size, ysize=rect_inner_size)
            rect_slider_inner_render = renpy.render(rect_slider_inner, width, height, st, at)
            render.blit(rect_slider_inner_render, (rect_inner_pos_x, rect_inner_pos_y))
            angle_degrees = self.angle * 180 / math.pi
            position_text = "圆环角度: {:.1f}°".format(angle_degrees)
            base_color_text = "基础颜色: {}".format(self.base_color)
            final_color_text = "最终颜色: {}".format(self.final_color)
            position_display = Text(
                position_text, 
                size=20, 
                color="#000000",
                outlines=[(1, "#FFFFFF", 0, 0)]
            )
            position_render = renpy.render(position_display, width, height, st, at)
            render.blit(position_render, (20, 20))
            
            base_color_display = Text(
                base_color_text, 
                size=20, 
                color="#000000",
                outlines=[(1, "#FFFFFF", 0, 0)]
            )
            base_color_render = renpy.render(base_color_display, width, height, st, at)
            render.blit(base_color_render, (20, 50))
            
            final_color_display = Text(
                final_color_text, 
                size=20, 
                color="#000000",
                outlines=[(1, "#FFFFFF", 0, 0)]
            )
            final_color_render = renpy.render(final_color_display, width, height, st, at)
            render.blit(final_color_render, (20, 80))
            renpy.redraw(self, 0.01)
            return render
            
        def event(self, ev, x, y, st):
            screen_width, screen_height = renpy.get_physical_size()
            actual_x = int(self.xpos * (screen_width - self.width))
            actual_y = int(self.ypos * (screen_height - self.height))
            local_x = x - actual_x
            local_y = y - actual_y
            dx = local_x - self.center_x
            dy = local_y - self.center_y
            distance = math.sqrt(dx*dx + dy*dy)
            angle = math.atan2(dy, dx)
            if angle < 0:
                angle += 2 * math.pi
            if self.inner_radius <= distance <= self.outer_radius:
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    self.angle = angle
                    self.dragging_ring = True
                    renpy.restart_interaction()
                elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                    self.dragging_ring = False
                elif ev.type == pygame.MOUSEMOTION and self.dragging_ring:
                    self.angle = angle
                    renpy.restart_interaction()
            rect_actual_x = actual_x + self.rect_x
            rect_actual_y = actual_y + self.rect_y
            if (rect_actual_x <= x <= rect_actual_x + self.rect_width and 
                rect_actual_y <= y <= rect_actual_y + self.rect_height):
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    rel_x = (x - rect_actual_x) / self.rect_width
                    rel_y = (y - rect_actual_y) / self.rect_height
                    self.slider_rel_x = max(0.0, min(1.0, rel_x))
                    self.slider_rel_y = max(0.0, min(1.0, rel_y))
                    self.dragging_rect = True
                elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                    self.dragging_rect = False
                elif ev.type == pygame.MOUSEMOTION and self.dragging_rect:
                    rel_x = (x - rect_actual_x) / self.rect_width
                    rel_y = (y - rect_actual_y) / self.rect_height
                    self.slider_rel_x = max(0.0, min(1.0, rel_x))
                    self.slider_rel_y = max(0.0, min(1.0, rel_y))
                    renpy.restart_interaction()
            return None
            
        def visit(self):
            return []
            
        def get_final_color(self):
            return self.final_color

default color_picker_width = 800 # 数越大 内存越爆炸
default color_picker_height = 800
default color_picker_zoom = 0.5
default color_picker_step = 5 # 数越小cpu越爆炸

screen color_picker_screen:
    tag menu
    modal True
    default color_picker = ColorPicker(
        width=color_picker_width,
        height=color_picker_height,
        xpos=0.5,
        ypos=0.5,
        color_picker_zoom=color_picker_zoom,
        step=color_picker_step
    )
    add color_picker

    textbutton "返回" xalign 1.0 yalign 1.0 action Return()
    
    hbox:
        align (0.5, 0.1)
        spacing 20
        add Solid(color_picker.get_final_color()):
            size(50, 50)
        vbox:
            spacing 5
            text "最终颜色: [color_picker.get_final_color()]":
                color "#000000"
                size 25
            textbutton "确认选择此颜色" action [SetVariable("gui.accent_color", color_picker.get_final_color())]
        text "{b}颜色预览{/b}":
            size 50
            color gui.accent_color

label sehuan:
    call screen color_picker_screen
