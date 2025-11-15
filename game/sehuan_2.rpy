init python:
    import pygame
    import math
    
    # 注册圆环取色器着色器 - 修复版（左右颠倒）
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
        float outer_radius = 0.48;
        float inner_radius = 0.38;
        
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
    
    class Color_Round_Picker(renpy.Displayable):
        def __init__(self, width=400, height=400, xpos=0.5, ypos=0.5, **kwargs):
            super(Color_Round_Picker, self).__init__(**kwargs)
            self.width = width
            self.height = height
            self.xpos = xpos
            self.ypos = ypos

            self.center_x = width // 2
            self.center_y = height // 2
            self.outer_radius = min(width, height) // 2 - 10
            self.inner_radius = self.outer_radius - 40  # 环宽

            self.current_color = "#000000"
            self.color_code_string = "#000000"
            self.angle = 0.0  # 角度，0-2π
            self.dragging = False
            
        def get_color_from_angle(self, angle):
            """根据角度计算颜色 - 与shader一致的算法"""
            # 将角度转换为HSV色相 (0-1)
            hue = angle / (2 * math.pi)
            
            # 使用与shader一致的HSV到RGB转换
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
            
        def get_color_at_position(self, x, y):
            dx = x - self.center_x
            dy = y - self.center_y
            distance = math.sqrt(dx*dx + dy*dy)
            angle = math.atan2(dy, dx)
            if angle < 0:
                angle += 2 * math.pi
            if self.inner_radius <= distance <= self.outer_radius:
                return self.get_color_from_angle(angle), angle
            else:
                return None, None
                
        def get_color_code_string(self):
            return self.color_code_string
            
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
            color = self.get_color_from_angle(self.angle)
            self.current_color = color.hexcode
            self.color_code_string = self.current_color
            slider_radius = (self.inner_radius + self.outer_radius) // 2
            slider_x = actual_x + self.center_x + slider_radius * math.cos(self.angle)
            slider_y = actual_y + self.center_y + slider_radius * math.sin(self.angle)
            slider_size = 14
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
            angle_degrees = self.angle * 180 / math.pi
            position_text = "角度: {:.1f}°".format(angle_degrees)
            color_text = "颜色: {}".format(self.current_color)
            position_display = Text(
                position_text, 
                size=24, 
                color="#000000",
                outlines=[(1, "#FFFFFF", 0, 0)]
            )
            position_render = renpy.render(position_display, width, height, st, at)
            render.blit(position_render, (20, 20))
            
            color_display = Text(
                color_text, 
                size=24, 
                color="#000000",
                outlines=[(1, "#FFFFFF", 0, 0)]
            )
            color_render = renpy.render(color_display, width, height, st, at)
            render.blit(color_render, (20, 50))
            renpy.redraw(self, 0.001)
            return render
            
        def event(self, ev, x, y, st):
            screen_width, screen_height = renpy.get_physical_size()
            actual_x = int(self.xpos * (screen_width - self.width))
            actual_y = int(self.ypos * (screen_height - self.height))
            local_x = x - actual_x
            local_y = y - actual_y
            color, angle = self.get_color_at_position(local_x, local_y)
            if color is not None:
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    self.angle = angle
                    self.dragging = True
                    renpy.restart_interaction()
                elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                    self.dragging = False
                elif ev.type == pygame.MOUSEMOTION and self.dragging:
                    self.angle = angle
                    renpy.restart_interaction()
            return None
        def visit(self):
            return []

