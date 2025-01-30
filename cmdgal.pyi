from typing import *
import os, sys
import json
import time
import threading

class NoBindTypeError(Exception): ...
class UnknownStyleError(Exception): ...

def goto(x: int, y: int) -> None: ...
def fontSize(n: int) -> None: ...
def clear() -> None: ...
def setWindow(width: int, height: int) -> None: ...
def output(*string: str) -> None: ...

class Settings(object):
    def __init__(self, width: int, height: int, fontSize: int, *args, **kwargs) -> Settings: ...
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
    def __init__(self, image: str, width: int, height: int, *args, **kwargs) -> Image: ...
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
    def __init__(self, text: str, width: int, height: int, *args, **kwargs) -> Label: ...
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
    def show(self, father: Window, /, *args, **kwargs) -> None: ...
