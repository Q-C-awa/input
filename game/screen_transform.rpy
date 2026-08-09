image white = "bg/white.png"
image black = "bg/black.png"
image brown:
    "#332c2f"
    # "#ff0000"
    size(1920,1080)
image screen_switch:
    contains:
        "brown"
        yoffset -1080
        easein 0.5 yoffset 0
        pause 0.8
        easeout 0.5 yoffset -1080
    contains:
        "white" 
        yoffset -1080
        pause 0.25
        easein 0.5 yoffset 0
        pause 0.4
        easeout 0.5 yoffset -1080
image screen_switch_2:
    contains:
        "brown"
        yoffset 1080
        easein 1.0 yoffset -1080
        pause 0.8
    contains:
        "white" 
        yoffset 1080
        pause 0.25
        easein 1.0 yoffset -1080
screen ex_screen(menu):
    add "screen_switch_2"
    if menu:
        timer 0.5 action ShowMenu(menu)
    else:
        timer 0.5 action Return()
