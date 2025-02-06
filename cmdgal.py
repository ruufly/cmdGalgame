from typing import *
import os, sys
import json
import time
import msvcrt
import ctypes
import threading
import builtins


class NoBindTypeError(Exception): ...


class UnknownStyleError(Exception): ...


lib = ctypes.WinDLL(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "window.dll")
)


def goto(x, y):
    lib.setcursor(x, y)
    # os.system("setcursor %d %d" % (x, y))


def fontSize(n):
    lib.setFontSizeMode(n)
    # os.system("fontsize %d" % n)


def showCursor(visible):
    lib.showcursor(visible)
    # os.system("showcursor %d" % (int(visible)))


def clear():
    os.system("cls")


def setWindow(width, height):
    os.system("mode con: cols=%d lines=%d" % (width, height))


def output(*string):
    # sys.stdout.write(*string,)
    print(*string, end="", flush=True)


class Settings(object):
    def __init__(self, **kwargs):
        self.settings = kwargs

    def export(self):
        with open("settings.json", "w") as f:
            json.dump(self.settings, f, indent=4)

    def import_(self):
        with open("settings.json", "r") as f:
            self.settings = json.load(f)


class Window(object):
    def __init__(self, settings: Settings):
        self.settings = settings
        self.refresh()

    def refresh(self):
        settings = self.settings.settings
        setWindow(settings["width"], settings["height"])
        fontSize(settings["fontSize"])
        self.width = settings["width"]
        self.height = settings["height"]

    def wait(self, timeout):
        time.sleep(timeout / 1000)
        goto(0, 0)
        clear()

    # def maintain(self):
    #     def going(self):
    #         while True:
    #             self.readSettings(self.settings)
    #             time.sleep(1)
    #     threading.Thread(target=going, args=(self,)).start()


class WidgetStatic(object):
    def __init__(self, **kwargs):
        self.width = 20
        self.height = 3
        self.page = [""]
        self.__dict__.update(kwargs)
        if type(self.page) == str:
            self.page = self.page.splitlines()

    def _bind_position(self, father: Window, x=0, y=0):
        for i in range(y, min(father.height, y + self.height)):
            goto(x, i)
            output(self.page[i - y][: min(self.width, father.width - x)])
        return x, y

    def _show_position(self, father: Window, speed: float, set: int, x=0, y=0):
        for i in range(y, min(father.height, y + self.height)):
            for j in range(x, min(father.width, x + self.width), set):
                goto(j, i)
                output(self.page[i - y][j - x : min(self.width - 1, j - x + set)])
                time.sleep(speed / 1000)

    def __get_side(self, father: Window, sidex, sidey):
        if sidex == "center":
            x = (father.width - self.width) // 2
        elif sidex == "right":
            x = father.width - self.width - (1 if sidey == "bottom" else 0)
        elif sidex == "left":
            x = (1 if sidey == "bottom" else 0)
        if sidey == "middle":
            y = (father.height - self.height) // 2
        elif sidey == "bottom":
            y = father.height - self.height
        elif sidey == "top":
            y = 0
        return x, y

    def _bind_side(self, father: Window, sidex, sidey):
        return self._bind_position(father, *self.__get_side(father, sidex, sidey))

    def _show_side(self, father: Window, sidex, sidey, speed: float, set: int):
        self._show_position(father, speed, set, *self.__get_side(father, sidex, sidey))

    def _bind(self, father: Window, type="position", *args, **kwargs):
        try:
            return getattr(self, "_bind_%s" % type)(father, *args, **kwargs)
        except AttributeError:
            raise NoBindTypeError("No such binding type: %s" % type)

    def _show(
        self,
        father: Window,
        speed: float,
        set: int = 1,
        type="position",
        *args,
        **kwargs,
    ):
        try:
            getattr(self, "_show_%s" % type)(
                father, *args, **kwargs, speed=speed, set=set
            )
        except AttributeError:
            raise NoBindTypeError("No such showing type: %s" % type)


class Image(WidgetStatic):
    def __init__(self, image, **kwargs):
        super(Image, self).__init__(**kwargs)
        self.page = image.splitlines()
        self.width = len(self.page[0])
        self.height = len(self.page)

    def show(self, father: Window, type="position", *args, **kwargs):
        self._bind(father, type, *args, **kwargs)


class Label(WidgetStatic):
    def __init__(self, text, **kwargs):
        super(Label, self).__init__(**kwargs)
        self.page = text.splitlines()
        self.width = len(self.page[0])
        self.height = len(self.page)

    def show(
        self,
        father: Window,
        type="position",
        speed: float = 2.0,
        set: int = 1,
        *args,
        **kwargs,
    ):
        self._show(father, speed, set, type, *args, **kwargs)


class Variables(object):
    def __init__(self):
        self.pool = {}

    def set(self, name, value):
        self.pool[name] = value
        return Variable(name)

    def get(self, name):
        return self.pool[name]

    def delete(self, name):
        del self.pool[name]


variables = Variables()


class Variable(object):
    def __init__(self, name):
        self.name = name

    def get(self):
        return variables.get(self.name)

    def set(self, value):
        variables.set(self.name, value)

    def delete(self):
        variables.delete(self.name)

    def __delete__(self):
        self.delete()

    def __set__(self, value):
        self.set(value)

    def __repr__(self):
        return self.get()

    def __str__(self):
        return str(self.get())

    def __int__(self):
        return int(self.get())

    def __float__(self):
        return float(self.get())

    def __bool__(self):
        return bool(self.get())


class Styles(object):
    def __init__(self):
        self.styles = {}


styles = Styles()


def SelectWidget_Normal(
    choices: dict,
    minLength: int = 15,
    entering: str = "enter",
    show_cursor: bool = False,
):
    maxLength = -1
    for i in choices:
        if len(choices[i]) > maxLength:
            maxLength = len(choices[i])
    length = max(maxLength + 4, minLength)
    choiceDict = {}
    showing = "*" * length + "\n"
    cnt = 1
    for i in choices:
        showing += "* %s" % (choices[i]) + " " * (length - len(choices[i]) - 3) + "*\n"
        choiceDict[i] = (1, cnt)
        cnt += 1
    showing += "*" * length
    return showing, choiceDict, ">", True, entering, show_cursor


styles.styles["SelectWidget::Normal"] = SelectWidget_Normal


class Select(WidgetStatic):
    def __init__(self, choices: dict, style: str, /, *args, **kwargs):
        self.choices = choices
        self.choiceList = []
        for i in self.choices:
            self.choiceList.append(i)
        self.running = False
        self.now_at, self.now_pos, self.ending = (
            self.choiceList[0],
            0,
            len(self.choiceList) - 1,
        )
        self.x, self.y = 0, 0
        if not style in styles.styles:
            raise UnknownStyleError("No such style: %s" % style)
        self.style = style
        self.choices = choices
        self.__refresh(style, *args, **kwargs)
        self.__args = args
        self.__kwargs = kwargs

    def __refresh(self, style: str, *args, **kwargs):
        self.style = style
        (
            self.showing,
            self.choiceDict,
            self.cursor,
            self.move,
            self.okay,
            self.show_cursor,
        ) = styles.styles[style](
            choices=self.choices, *args, **kwargs
        )  # self.move: move by "W&S/Up&Down" if True else by "A&D/Left&Right"
        self.page = self.showing.splitlines()
        self.height = len(self.page)
        self.width = len(self.page[0])

    def refresh(self):
        self.__refresh(self.style, *self.__args, **self.__kwargs)

    def __changeKey(self, key):
        # print(key)
        if not self.running:
            raise Exception("I have no idea why this line was run.")
        if key == self.okay:
            return
        if self.move:
            if key in [b"w", b"W", b"H"]:
                if self.now_pos != 0:
                    self.now_pos -= 1
            elif key in [b"s", b"S", b"P"]:
                if self.now_pos != self.ending:
                    self.now_pos += 1
        else:
            if key in [b"a", b"A", b"K"]:
                if self.now_pos != 0:
                    self.now_pos -= 1
            elif key in [b"d", b"D", "M"]:
                if self.now_pos != self.ending:
                    self.now_pos += 1
        # print(self.nowKey)
        self.now_at = self.choiceList[self.now_pos]
        self.flush()

    def flush(self):
        # print(self.choiceDict)
        if not self.running:
            return
        self.cursor_at = (
            self.x + self.choiceDict[self.now_at][0],
            self.y + self.choiceDict[self.now_at][1],
        )
        if self.cursor_lst[0] != None:
            goto(*self.cursor_lst)
            print(" ")
        goto(*self.cursor_at)
        print(self.cursor)
        goto(*self.cursor_at)
        self.cursor_lst = self.cursor_at

    def run(self, father: Window, /, type: str = "position", *args, **kwargs):
        self.running = True
        showCursor(self.show_cursor)
        self.x, self.y = self._bind(father, type, *args, **kwargs)
        self.cursor_lst = (None, None)
        self.now_at = self.choiceList[0]
        self.now_pos = 0
        self.ending = len(self.choiceList) - 1
        self.flush()
        while True:
            if msvcrt.kbhit():
                char = msvcrt.getch()
                if self.okay == "enter":
                    if char == b"\r" or char == b"\n":
                        break
                else:
                    if char == self.okay:
                        break
                self.__changeKey(char)
        self.running = False
        sys.stdin.flush()
        showCursor(True)
        return self.now_at


def InitialPage_Normal(
    mainImage: str = "", noticeText: str = "", isFlow: bool = True, *args
):
    if isFlow:
        return (
            Image(mainImage),
            (),
            {"type": "side", "sidex": "center", "sidey": "middle"},
            Label(noticeText),
            (*args,),
            {"type": "side", "sidex": "left", "sidey": "bottom"},
        )
    else:
        return (
            Image(mainImage),
            (),
            {"type": "side", "sidex": "center", "sidey": "middle"},
            Image(noticeText),
            (),
            {"type": "side", "sidex": "left", "sidey": "bottom"},
        )


def InitialPage_Normal_Show(
    father: Window,
    widgets: list | tuple = [],
    waitTime: int = 1000,
    runfunc: Any = lambda: ...,
):
    for i in widgets:
        i[0].show(father, *i[1], **i[2])
    runfunc()
    father.wait(waitTime)


styles.styles["InitialPage::Normal"] = InitialPage_Normal
styles.styles["InitialPage::Normal::Show"] = InitialPage_Normal_Show


def StartPage_Normal(
    title_page: str = "",
    start_cg: str = "",
    message: str = "",
    choiceDict: dict = {},
    title_setup: dict = {"type": "position", "x": 6, "y": 3},
    choice_setup: dict = {"type": "side", "sidex": "right", "sidey": "middle"},
):
    return (
        Image(start_cg),
        (),
        {"type": "position", "x": 0, "y": 0},
        Image(title_page),
        (),
        title_setup,
        Image(message),
        (),
        {"type": "side", "sidex": "right", "sidey": "bottom"},
        Select(choiceDict, "SelectWidget::Normal"),
        (),
        choice_setup,
    )


def StartPage_Normal_Show(father: Window, widgets: list | tuple = []):
    for i in widgets[:-1]:
        i[0].show(father, *i[1], **i[2])
    ri = widgets[-1]
    return ri[0].run(father, *ri[1], **ri[2])


styles.styles["StartPage::Normal"] = StartPage_Normal
styles.styles["StartPage::Normal::Show"] = StartPage_Normal_Show


class Page(object):
    def __init__(self, style, *args, **kwargs):
        if not style in styles.styles:
            raise UnknownStyleError("No such style: %s" % style)
        self.style = style
        paraList = styles.styles[style](*args, **kwargs)
        self.init(*paraList)

    def init(self, *args):
        self.widgets = []
        if len(args) % 3:
            raise ValueError("Args must be in pairs: widget, arguments")
        for i in range(0, len(args), 3):
            self.widgets.append((args[i], args[i + 1], args[i + 2]))

    def show(self, father, *args, **kwargs):
        if not "%s::Show" % self.style in styles.styles:
            raise UnknownStyleError("The style %s cannot be shown" % self.style)
        return styles.styles["%s::Show" % self.style](
            father, self.widgets, *args, **kwargs
        )


class Plugin(object):
    def __init__(self, directory: str, *args, **kwargs):
        self.directory = directory
        with open(os.path.join(self.directory, "setup.json"), "r") as f:
            self.setup = json.load(f)
        self.name = self.setup["name"]
        self.version = self.setup["version"]
        self.author = self.setup["author"]
        self.description = self.setup["description"]
        self.import_ = self.setup["import"]
        exec("import %s" % self.import_)
        exec(
            """for i in %s.styles:
    styles.styles[i] = %s.styles[i]"""
            % (self.import_, self.import_)
        )
        exec(
            """for i in dir(%s):
    if not hasattr(self, i):
        setattr(self,i,eval("%s."+i))"""
            % (self.import_, self.import_)
        )

    def __repr__(self):
        return "<Plugin %s: %s at %s>" % (self.name, self.version, hex(id(self)))


if __name__ == "__main__":
    setting = Settings(width=120, height=30, fontSize=20)
    galgame = Window(setting)
