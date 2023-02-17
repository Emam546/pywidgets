MOTION="motion"
RELEASE="release"
PRESS="press"
DOUBLE_PRESS="double_press"

MOUSE_1="left"
MOUSE_2=["scrollup","scrolldown"]#scrool mouse
MOUSE_3="right"
ENTER="<Return>"

BINDING={
    "<Button-1>":[PRESS,MOUSE_1],
    "<Button-2>":[PRESS,MOUSE_2],
    "<Button-3>":[PRESS,MOUSE_3],

    "<ButtonRelease-1>":[RELEASE,MOUSE_1],
    "<ButtonRelease-2>":[RELEASE,MOUSE_2],
    "<ButtonRelease-3>":[RELEASE,MOUSE_3],

    "<B1-Motion>":[MOTION,MOUSE_1],
    "<B2-Motion>":[MOTION,MOUSE_2],
    "<B3-Motion>":[MOTION,MOUSE_3],

    "<Double-Button-1>":[DOUBLE_PRESS,MOUSE_1],
    "<Double-Button-2>":[DOUBLE_PRESS,MOUSE_2],
    "<Double-Button-3>":[DOUBLE_PRESS,MOUSE_3],
}
