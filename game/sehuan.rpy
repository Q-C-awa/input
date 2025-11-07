# transform shader_tran_2:
#     shader "color_solid_2"
# transform shader_tran_3:
#     shader "color_solid_3"

default selected_color = (1.0, 0.0, 0.0)
default current_color_code = "#ff0000"

image white_bg = "white.jpg"

transform shader_tran_soild:
    shader "color_solid"
    # uniform "u_base_color" 

transform shader_tran_round:
    shader "color_round"

screen color_choice:
    tag menu 
    zorder 100
    
    add "white_bg" at shader_tran_soild:
        size (400,400)
        align(0.5,0.5)
    
    add "white_bg" at shader_tran_round:
        size (750,750)
        align(0.5,0.5)
    
    text current_color_code:
        align(0.5, 0.9)
        size 40
        color "#000000"
    
    mousearea:
        area (0, 0, 750, 750)
        hovered GetRingColor()
        unhovered None

init python:
    def GetRingColor():
        mouse_pos = renpy.get_mouse_pos()
        center_x = 1280 / 2
        center_y = 720 / 2
        mouse_x = mouse_pos[0] - center_x
        mouse_y = mouse_pos[1] - center_y
        
        dist = (mouse_x**2 + mouse_y**2)**0.5
        if 270 <= dist <= 337.5:
            angle = math.atan2(mouse_y, mouse_x)
            hue = (angle + math.pi) / (2 * math.pi)
            
            if hue < 1/6:
                r, g, b = 1.0, hue * 6, 0.0
            elif hue < 2/6:
                r, g, b = 1.0 - (hue - 1/6) * 6, 1.0, 0.0
            elif hue < 3/6:
                r, g, b = 0.0, 1.0, (hue - 2/6) * 6
            elif hue < 4/6:
                r, g, b = 0.0, 1.0 - (hue - 3/6) * 6, 1.0
            elif hue < 5/6:
                r, g, b = (hue - 4/6) * 6, 0.0, 1.0
            else:
                r, g, b = 1.0, 0.0, 1.0 - (hue - 5/6) * 6
            
            store.selected_color = (r, g, b)
            
            r_int = int(r * 255)
            g_int = int(g * 255)
            b_int = int(b * 255)
            store.current_color_code = "#{:02x}{:02x}{:02x}".format(r_int, g_int, b_int)

label sehuan:
    call screen color_choice
    return