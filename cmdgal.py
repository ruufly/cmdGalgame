from typing import *
import os, sys
import json
import time
import threading


class NoBindTypeError(Exception): ...


class UnknownStyleError(Exception): ...


def goto(x, y):
    os.system("setcursor %d %d" % (x, y))


def fontSize(n):
    os.system("fontsize %d" % n)


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
        goto(0, 0)
        time.sleep(timeout / 1000)

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

    def _bind_position(self, father: Window, x = 0, y = 0):
        for i in range(y, min(father.height, y + self.height)):
            goto(x, i)
            output(self.page[i - y][: min(self.width, father.width - x)])

    def _show_position(self, father: Window, speed: float, set: int, x = 0, y = 0):
        for i in range(y, min(father.height, y + self.height)):
            for j in range(x, min(father.width, x + self.width), set):
                goto(j, i)
                output(self.page[i - y][j - x : min(self.width - 1, j - x + set)])
                time.sleep(speed / 1000)

    def __get_side(self, father: Window, sidex, sidey):
        if sidex == "center":
            x = (father.width - self.width) // 2
        elif sidex == "right":
            x = father.width - self.width
        elif sidex == "left":
            x = 0
        if sidey == "middle":
            y = (father.height - self.height) // 2
        elif sidey == "bottom":
            y = father.height - self.height
        elif sidey == "top":
            y = 0
        return x, y

    def _bind_side(self, father: Window, sidex, sidey):
        self._bind_position(father, *self.__get_side(father, sidex, sidey))

    def _show_side(self, father: Window, sidex, sidey, speed: float, set: int):
        self._show_position(father, speed, set, *self.__get_side(father, sidex, sidey))

    def _bind(self, father: Window, type="position", *args, **kwargs):
        try:
            getattr(self, "_bind_%s" % type)(father, *args, **kwargs)
        except AttributeError:
            raise NoBindTypeError("No such binding type: %s" % type)

    def _show(
        self,
        father: Window,
        speed: float,
        set: int = 1,
        type="position",
        *args,
        **kwargs
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
        **kwargs
    ):
        self._show(father, speed, set, type, *args, **kwargs)


class Styles(object):
    def __init__(self):
        self.styles = {}


styles = Styles()


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

def InitialPage_Normal_Show(father: Window, widgets: list | tuple = [], waitTime: int = 1000):
    for i in widgets:
        i[0].show(father, *i[1], **i[2])
    father.wait(waitTime)


styles.styles["InitialPage::Normal"] = InitialPage_Normal
styles.styles["InitialPage::Normal::Show"] = InitialPage_Normal_Show


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
        styles.styles["%s::Show" % self.style](father, self.widgets, *args, **kwargs)



if __name__ == "__main__":
    setting = Settings(width=120, height=30, fontSize=20)
    galgame = Window(setting)
    input()
