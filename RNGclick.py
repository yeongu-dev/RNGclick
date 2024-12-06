from tkinter import Tk, Label, Menu, IntVar
from tkinter.font import Font
from random import SystemRandom
import sys, os

FONTSIZE_INCR = 15
menu_isvisible = True
color_mode = False
rng_istimed = False
rng_limit = (1, 100)

def main():
    root = Tk()
    root.title('RNGclick')
    root.wm_iconbitmap(resource_path('logo.ico'))

    fontStyle = Font(family='Consolas', size=80)
    label = Label(root, text="0", font=fontStyle, bg='black')
    label.pack(expand='True', fill="both")

    emptyMenu = Menu(root)
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Switch Color Order", command=color_switch)
    filemenu.add_separator()
    radio_var = IntVar()
    filemenu.add_radiobutton(label="RNG from 0-99", variable=radio_var, value = 1, command=lambda: rng_limit_switch((0,99)))
    filemenu.add_radiobutton(label="RNG from 1-100", variable=radio_var, value = 0, command=lambda: rng_limit_switch((1,100)))
    filemenu.add_separator()
    filemenu.add_command(label="Increase Font Size", command=lambda: fontStyle.config(size = fontStyle['size'] + FONTSIZE_INCR))
    filemenu.add_command(label="Decrease Font Size", command=lambda: fontStyle.config(size = fontStyle['size'] - FONTSIZE_INCR))
    filemenu.add_separator()
    filemenu.add_radiobutton(label="Timed Mode Toggle", command=timed_switch)
    menubar.add_cascade(label="Options", menu=filemenu)
    root.config(menu=menubar)

    root.configure(background='black')
    root.bind('<Button-1>', lambda event, r=root, l=label: gen_rand(r, l))
    root.bind('<Button-3>', lambda event, l=label: clear_rand(l))
    root.bind('<Double-Button-3>', lambda event, r=root, e=emptyMenu, m=menubar: menu_switch(r, e, m))

    root.geometry("220x160+100+100")
    root.wm_attributes("-topmost", 1)
    gen_rand(root, label)
    root.mainloop()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def gen_rand(root, label):
    global rng_istimed, color_mode, rng_limit
    COLORS = ('#920000','#db6d00','#ffff6d','#24ff24','#24ff24','#ffff6d','#db6d00','#920000')

    label['text'] = SystemRandom().randint(rng_limit[0], rng_limit[1])
    label.config(fg=COLORS[(label['text'] + 100*int(color_mode) - rng_limit[0]) // 25])
    if rng_istimed:
        root.after(3000, lambda: gen_rand(root, label))

def clear_rand(label):
	label['text'] = ""

def color_switch():
    global color_mode
    color_mode = not(color_mode)

def timed_switch():
    global rng_istimed
    rng_istimed = not(rng_istimed)

def rng_limit_switch(new_limit):
    global rng_limit
    rng_limit = new_limit

def menu_switch(root, emptyMenu, menubar):
    global menu_isvisible
    if menu_isvisible:
        root.config(menu=emptyMenu)
        menu_isvisible = not menu_isvisible
        winx = root.winfo_rootx() - 1
        winy = root.winfo_rooty() + 19
        winw = root.winfo_width()
        winh = root.winfo_height() - 38
        root.geometry(f'{winw}x{winh}')
        root.geometry(f'+{winx}+{winy}')
        root.overrideredirect(1)
    else:
        root.config(menu=menubar)
        menu_isvisible = not menu_isvisible
        winx = root.winfo_rootx() - 7
        winy = root.winfo_rooty() - 50
        winw = root.winfo_width()
        winh = root.winfo_height() - 2
        root.geometry(f'{winw}x{winh}')
        root.geometry(f'+{winx}+{winy}')
        root.overrideredirect(0)

if __name__ == '__main__':
    main()
