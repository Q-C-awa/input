init python:
    renpy.register_shader("color_solid", 
        variables="""
            uniform vec2 u_model_size;
            attribute vec2 a_tex_coord;
            varying vec2 v_tex_coord;
        """,
        vertex_100="""
            v_tex_coord = a_tex_coord;
        """,
        fragment_300="""
            precision highp float;
            vec2 uv = v_tex_coord;
            float saturation = uv.x; 
            float brightness = 1.0 - uv.y; 
            vec3 baseColor = vec3(1.0, 0.0, 0.0); 
            vec3 gray = vec3(brightness); 
            vec3 pureColor = baseColor;  
            vec3 mixedColor = mix(gray, pureColor, saturation);
            vec3 finalColor = mixedColor * brightness;
            gl_FragColor = vec4(finalColor, 1.0);
        """)
    renpy.register_shader("color_round", 
        variables="""
            uniform vec2 u_model_size;
            attribute vec2 a_tex_coord;
            varying vec2 v_tex_coord;
        """,
        vertex_100="""
            v_tex_coord = a_tex_coord;
        """,
        fragment_300="""
            precision highp float;  
            vec2 uv = v_tex_coord;
            vec2 center = vec2(0.5, 0.5);
            float dist = distance(uv, center);
            if(dist > 0.4 && dist < 0.5) {
                float angle = atan(uv.y - center.y, uv.x - center.x);
                float hue = (angle + 3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019) / (2.0 * 3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019);
                vec3 color = vec3(1.0);
                if(hue < 1.0/6.0) {
                    color = vec3(1.0, hue * 6.0, 0.0);
                } else if(hue < 2.0/6.0) {
                    color = vec3(1.0 - (hue - 1.0/6.0) * 6.0, 1.0, 0.0);
                } else if(hue < 3.0/6.0) {
                    color = vec3(0.0, 1.0, (hue - 2.0/6.0) * 6.0);
                } else if(hue < 4.0/6.0) {
                    color = vec3(0.0, 1.0 - (hue - 3.0/6.0) * 6.0, 1.0);
                } else if(hue < 5.0/6.0) {
                    color = vec3((hue - 4.0/6.0) * 6.0, 0.0, 1.0);
                } else {
                    color = vec3(1.0, 0.0, 1.0 - (hue - 5.0/6.0) * 6.0);
                }
                gl_FragColor = vec4(color, 1.0);
            } else {
                gl_FragColor = vec4(0.0, 0.0, 0.0, 0.0);
            }
        """)

# init python:
#     renpy.register_shader("color_solid_2", 
#         variables="""
#             uniform vec2 u_model_size;
#             attribute vec2 a_tex_coord;
#             varying vec2 v_tex_coord;
#         """,
#         vertex_100="""
#             v_tex_coord = a_tex_coord;
#         """,
#         fragment_300="""
#             precision highp float;
#             vec2 uv = v_tex_coord;
#             float saturation = uv.x; 
#             float brightness = 1.0 - uv.y;
#             vec3 baseColor = vec3(1.0, 0.0, 0.0);
#             vec3 gray = vec3(brightness); 
#             vec3 pureColor = baseColor * brightness; 
#             vec3 finalColor = mix(gray, pureColor, saturation);    
#             gl_FragColor = vec4(finalColor, 1.0);
#         """)

# init python:
#     renpy.register_shader("color_solid_3", 
#         variables="""
#             uniform vec2 u_model_size;
#             attribute vec2 a_tex_coord;
#             varying vec2 v_tex_coord;
#         """,
#         vertex_100="""
#             v_tex_coord = a_tex_coord;
#         """,
#         fragment_300="""
#             precision highp float;
            
#             vec2 uv = v_tex_coord;
#             float saturation = uv.x;
#             float brightness = 1.0 - uv.y;  
#             vec3 baseColor = vec3(1.0, 0.0, 0.0);
#             vec3 saturatedColor = mix(vec3(1.0), baseColor, saturation);
#             vec3 finalColor = saturatedColor * brightness;
#             gl_FragColor = vec4(finalColor, 1.0);
#         """)

    
