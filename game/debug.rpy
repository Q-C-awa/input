init -99 python:
    def show_code(func):
        import inspect
        print(inspect.getsource(func))
    # config.always_shown_screens.append("debug_screen")
    config.layers.append("debug_layer")
    config.top_layers.append("debug_layer")
    
# 这是一个主版本才有的注释
transform debug_mode_t():
    alpha 0.9

screen debug_screen():
    layer "debug_layer"
    add "debug/load.png" at debug_mode_t

