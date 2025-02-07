from typing import *
import os, sys
import json
import time
import msvcrt
import ctypes
import threading
import builtins
import copy
import unicodedata


class NoBindTypeError(Exception): ...


class UnknownStyleError(Exception): ...


lib = ctypes.WinDLL(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "window.dll")
)

nowCursor = True


def goto(x, y):
    lib.setcursor(x, y)
    # os.system("setcursor %d %d" % (x, y))


def fontSize(n):
    lib.setFontSizeMode(n)
    # os.system("fontsize %d" % n)


def showCursor(visible):
    global nowCursor
    nowCursor = visible
    lib.showcursor(visible)
    # os.system("showcursor %d" % (int(visible)))


def clear():
    os.system("cls")


def setWindow(width, height):
    os.system("mode con: cols=%d lines=%d" % (width, height))


def output(*string):
    # sys.stdout.write(*string,)
    print(*string, end="", flush=True)


def isFullWidth(char):
    return unicodedata.east_asian_width(char) in ("F", "W")


def _len(str: str):
    len = 0
    for i in str:
        len += 2 if isFullWidth(i) else 1
    return len


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

    def _show_position(self, father: Window, speed: float, x=0, y=0):
        for i in range(y, min(father.height, y + self.height)):
            goto(x, i)
            for j in range(x, min(father.width, x + self.width - 1)):
                try:
                    output(self.page[i - y][j - x])
                except IndexError:
                    pass
                # output(self.page[i - y][j - x : min(self.width - 1, j - x + 1)])
                time.sleep(speed / 1000)

    def __get_side(self, father: Window, sidex, sidey):
        if sidex == "center":
            x = (father.width - self.width) // 2
        elif sidex == "right":
            x = father.width - self.width  # - (1 if sidey == "bottom" else 0)
        elif sidex == "left":
            x = 0  # 1 if sidey == "bottom" else 0
        if sidey == "middle":
            y = (father.height - self.height) // 2
        elif sidey == "bottom":
            y = father.height - self.height
        elif sidey == "top":
            y = 0
        return x, y

    def _bind_side(self, father: Window, sidex, sidey):
        return self._bind_position(father, *self.__get_side(father, sidex, sidey))

    def _show_side(self, father: Window, sidex, sidey, speed: float):
        self._show_position(father, speed, *self.__get_side(father, sidex, sidey))

    def _bind(self, father: Window, type="position", *args, **kwargs):
        try:
            return getattr(self, "_bind_%s" % type)(father, *args, **kwargs)
        except AttributeError:
            raise NoBindTypeError("No such binding type: %s" % type)

    def _show(
        self,
        father: Window,
        speed: float,
        type="position",
        *args,
        **kwargs,
    ):
        try:
            getattr(self, "_show_%s" % type)(father, *args, **kwargs, speed=speed)
        except AttributeError:
            raise NoBindTypeError("No such showing type: %s" % type)


class Image(WidgetStatic):
    def __init__(self, image, **kwargs):
        super(Image, self).__init__(**kwargs)
        self.page = image.splitlines()
        self.width = 0
        for i in self.page:
            self.width = max(self.width, _len(i))
        self.height = len(self.page)

    def show(self, father: Window, type="position", *args, **kwargs):
        self._bind(father, type, *args, **kwargs)


class Label(WidgetStatic):
    def __init__(self, text, **kwargs):
        super(Label, self).__init__(**kwargs)
        self.page = text.splitlines()
        self.width = 0
        for i in self.page:
            self.width = max(self.width, _len(i))
        self.height = len(self.page)

    def show(
        self,
        father: Window,
        type="position",
        speed: float = 2.0,
        *args,
        **kwargs,
    ):
        self._show(father, speed, type, *args, **kwargs)


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


class BoxStyle(object):
    def __init__(
        self,
        corner: str,
        sideEdge: str,
        topEdge: str,
        splitEdge: str,
        cursor: str,
        leftDiagonal: str,
        rightDiagonal: str,
    ):
        self.corner = corner
        self.sideEdge = sideEdge
        self.topEdge = topEdge
        self.splitEdge = splitEdge
        self.cursor = cursor
        self.leftDiagonal = leftDiagonal
        self.rightDiagonal = rightDiagonal


class Styles(object):
    def __init__(self):
        self.styles = {}


styles = Styles()

styles.styles["Box::Normal"] = BoxStyle("+", "|", "=", "-", ">", "/", "\\")


def SelectWidget_Normal(
    choices: dict,
    minLength: int = 15,
    entering: str = "enter",
    show_cursor: bool = False,
    boxStyle: str = "Box::Normal",
):
    try:
        boxStyle = styles.styles[boxStyle]
    except KeyError:
        raise UnknownStyleError("No such box style: %s" % boxStyle)
    corner = boxStyle.corner
    sideEdge = boxStyle.sideEdge
    topEdge = boxStyle.topEdge
    cursor = boxStyle.cursor
    maxLength = -1
    for i in choices:
        if len(choices[i]) > maxLength:
            maxLength = len(choices[i])
    length = max(maxLength + 4, minLength)
    choiceDict = {}
    showing = corner + topEdge * (length - 2) + corner + "\n"
    cnt = 1
    for i in choices:
        showing += (
            sideEdge
            + " %s" % (choices[i])
            + " " * (length - _len(choices[i]) - 3)
            + sideEdge
            + "\n"
        )
        choiceDict[i] = (1, cnt)
        cnt += 1
    showing += corner + topEdge * (length - 2) + corner
    return showing, choiceDict, cursor, True, entering, show_cursor


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
        self.width = 0
        for i in self.page:
            self.width = max(self.width, _len(i))

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
        lstCursor = nowCursor
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
        showCursor(lstCursor)
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
    startRun = threading.Thread(target=runfunc)
    waitRun = threading.Thread(target=father.wait, args=(waitTime,))
    startRun.start()
    waitRun.start()
    while startRun.is_alive() or waitRun.is_alive():
        ...


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


def StoryPage_Normal(
    fatherSetting: Settings,
    section: str = " ",
    state: str = " ",
    person: str = " ",
    word: str = " ",
    boxStyle: str = "Box::Normal",
    boxMinLength: int = 40,
    nameMinLength: int = 18,
    messageboxHeight: int = 8,
    speed: float = 2.0,
):
    setting = fatherSetting.settings
    section_len = 0
    for i in section:
        section_len += 2 if isFullWidth(i) else 1
    state_len = 0
    for i in state:
        state_len += 2 if isFullWidth(i) else 1
    person_len = 0
    for i in person:
        person_len += 2 if isFullWidth(i) else 1
    topBox_length = min(
        max(max(section_len, state_len) + 8, boxMinLength), setting["width"]
    )
    try:
        boxStyle = styles.styles[boxStyle]
    except KeyError:
        raise UnknownStyleError("No such box style: %s" % boxStyle)
    topBox = (
        boxStyle.corner
        + boxStyle.topEdge * (topBox_length - 2)
        + boxStyle.corner
        + "\n"
        + boxStyle.sideEdge
        + " "
        + section
        + " " * (topBox_length - section_len - 3)
        + boxStyle.sideEdge
        + "\n"
        + boxStyle.sideEdge
        + "    "
        + state
        + " " * (topBox_length - state_len - 6)
        + boxStyle.sideEdge
        + "\n"
        + boxStyle.corner
        + boxStyle.topEdge * (topBox_length - 2)
        + boxStyle.corner
    )
    reMessagebox = boxStyle.topEdge * setting["width"]
    messagebox_length = max(nameMinLength, person_len + 2)
    messagebox = (
        "     "
        + boxStyle.corner
        + boxStyle.splitEdge * messagebox_length
        + boxStyle.corner
        + "\n"
        + "     "
        + boxStyle.sideEdge
        + " "
        + person
        + " " * (messagebox_length - person_len)
        + boxStyle.rightDiagonal
        + "\n"
        + boxStyle.topEdge * 5
        + boxStyle.corner
        + " " * (messagebox_length + 2)
        + boxStyle.corner
    )
    return (
        Image(topBox),
        (),
        {"type": "position", "x": 1, "y": 1},
        Image(reMessagebox),
        (),
        {"type": "position", "x": 0, "y": setting["height"] - messageboxHeight},
        Image(messagebox),
        (),
        {"type": "position", "x": 0, "y": setting["height"] - messageboxHeight - 2},
        Image(person),
        (),
        {"type": "position", "x": 7, "y": setting["height"] - messageboxHeight - 1},
        Label(word),
        (),
        {
            "type": "position",
            "speed": speed,
            "x": 7,
            "y": setting["height"] - messageboxHeight + 2,
        },
    )


def StoryPage_Normal_Show(father: Window, widgets: list | tuple = []):
    for i in widgets:
        i[0].show(father, *i[1], **i[2])
    while True:
        if msvcrt.kbhit():
            char = msvcrt.getch()
            if char == b"\r" or char == b"\n" or char == b" ":
                return True
            elif char == b"\x1b":
                return False
    # time.sleep(10)


styles.styles["StoryPage::Normal"] = StoryPage_Normal
styles.styles["StoryPage::Normal::Show"] = StoryPage_Normal_Show


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

    def show(self, father, isClear: bool = True, *args, **kwargs):
        if not "%s::Show" % self.style in styles.styles:
            raise UnknownStyleError("The style %s cannot be shown" % self.style)
        ret = styles.styles["%s::Show" % self.style](
            father, self.widgets, *args, **kwargs
        )
        if isClear:
            clear()
        return ret


class PluginUse(object):
    def __init__(self):
        self.goto = goto
        self.fontSize = fontSize
        self.showCursor = showCursor
        self.clear = clear
        self.Settings = Settings
        self.Window = Window
        self.WidgetStatic = WidgetStatic
        self.Image = Image
        self.Label = Label
        self.Styles = Styles
        self.Page = Page
        self.Variable = Variable
        self.Variables = Variables
        self.Select = Select


PluginUse = PluginUse()


class Plugin(object):
    def __init__(self, directory: str, /, *args, **kwargs):
        self.directory = directory
        with open(os.path.join(self.directory, "setup.json"), "r") as f:
            self.setup = json.load(f)
        self.name = self.setup["name"]
        self.version = self.setup["version"]
        self.author = self.setup["author"]
        self.description = self.setup["description"]
        self.import_ = self.setup["import"]
        print(
            "loading plugin... %s: %s by %s from %s"
            % (self.name, self.version, self.author, self.import_)
        )
        exec("import %s" % self.import_)
        exec(
            """if hasattr(%s, "styles"):
    for i in %s.styles:
        styles.styles[i] = %s.styles[i]"""
            % (self.import_, self.import_, self.import_)
        )
        exec("%s.api = [PluginUse, variables, styles.styles]" % self.import_)
        exec(
            """for i in dir(%s):
    if not hasattr(self, i):
        func = eval("%s." + str(i))
        if type(func) == type(lambda: ...):
            # self.funcS[i] = func
            # lastFunc = lambda *args, **kwargs: self.funcS[i](api=[PluginUse, variables, styles.styles], *args, **kwargs)
            setattr(self, i, func)
            # lastFunc()"""
            % (self.import_, self.import_)
        )

    def __repr__(self):
        return "<Plugin %s: %s at %s>" % (self.name, self.version, hex(id(self)))


if __name__ == "__main__":
    setting = Settings(width=120, height=30, fontSize=20)
    galgame = Window(setting)
