from typing import *

class NoBindTypeError(Exception): ...
class UnknownStyleError(Exception): ...

def goto(x: int, y: int) -> None: ...
def fontSize(n: int) -> None: ...
def showCursor(visible: bool) -> None: ...
def clear() -> None: ...
def setWindow(width: int, height: int) -> None: ...
def output(*string: str) -> None: ...

class Settings(object):
    def __init__(
        self, width: int, height: int, fontSize: int, *args, **kwargs
    ) -> Settings: ...
    def export() -> None: ...
    def import_() -> None: ...

class Window(object):
    def __init__(self, settings: Settings) -> Window: ...
    def refresh(self) -> None: ...
    def wait(self, timeout: int) -> None: ...

class WidgetStatic(object):
    def __init__(
        self, width: int, *, height: int, page: str | list
    ) -> WidgetStatic: ...

class Image(WidgetStatic):
    def __init__(
        self, image: str, width: int, height: int, *args, **kwargs
    ) -> Image: ...
    @overload
    def show(
        self, father: Window, type: str = "position", /, x: int = 0, y: int = 0
    ) -> None: ...
    @overload
    def show(
        self,
        father: Window,
        type: str = "side",
        /,
        sidex: str = "right" | "left" | "center",
        sidey: str = "top" | "bottom" | "middle",
    ) -> None: ...

class Label(WidgetStatic):
    def __init__(
        self, text: str, width: int, height: int, *args, **kwargs
    ) -> Label: ...
    @overload
    def show(
        self,
        father: Window,
        type: str = "position",
        /,
        speed: float = 2.0,
        set: int = 1,
        x: int = 0,
        y: int = 0,
    ) -> None: ...
    @overload
    def show(
        self,
        father: Window,
        type: str = "side",
        /,
        speed: float = 2.0,
        set: int = 1,
        sidex: str = "right" | "left" | "center",
        sidey: str = "top" | "bottom" | "middle",
    ) -> None: ...

class Styles(object):
    def __init__(self) -> Styles: ...

class Page(object):
    @overload
    def __init__(
        self,
        style: str = "InitialPage::Normal",
        /,
        mainImage: str = "",
        noticeText: str = "",
        isFlow: bool = True,
        speed: float = 2.0,
        set: int = 1,
    ) -> Page: ...
    @overload
    def __init__(
        self,
        style: str = "StartPage::Normal",
        /,
        title_page: str = "",
        start_cg: str = "",
        message: str = "",
        choiceDict: dict = {},
        title_setup: dict = {"type": "position", "x": 6, "y": 3},
        choice_setup: dict = {"type": "side", "sidex": "right", "sidey": "middle"},
    ) -> Page: ...
    def show(self, father: Window, /, *args, **kwargs) -> Any: ...

class Variable(object):
    def __init__(self, name: str) -> Variable: ...
    def set(self, value: Any) -> None: ...
    def get(self) -> Any: ...
    def delete(self) -> None: ...

class Variables(object):
    def __init__(self) -> Variables: ...
    def set(self, name: str, value: Any) -> Variable: ...
    def get(self, name: str) -> Any: ...
    def delete(self, name: str) -> None: ...

variables = Variables()

class Select(object):
    @overload
    def __init__(
        self,
        choices: dict,
        style: str = "SelectWidget::Normal",
        /,
        minLength: int = 15,
        entering: str = "enter",
        show_cursor: bool = False,
    ) -> Select: ...
    def refresh(self) -> None: ...
    @overload
    def run(
        self, father: Window, /, type: str = "position", x: int = 0, y: int = 0
    ) -> Any: ...
    @overload
    def run(
        self,
        father: Window,
        /,
        type: str = "side",
        sidex: str = "right" | "left" | "center",
        sidey: str = "top" | "bottom" | "middle",
    ) -> Any: ...
