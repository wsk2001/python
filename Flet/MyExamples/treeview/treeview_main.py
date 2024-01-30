import time
from math import pi

import flet as ft
from flet import Column, Icon, Page, Text, icons

from controls.collapsible import Collapsible
from controls.menu_button import MenuButton

def my_def_func(event):
    page = event.control._page

    # Delete items added after the menu item.
    ctrl_count =  len(page.controls)
    if 1 < ctrl_count:
        loop = int(ctrl_count)
        for i in range(1, loop):
            page.remove_at(i)

    txt_number = ft.TextField(value=event.control.title, text_align=ft.TextAlign.CENTER, width=300)

    page.add(
        ft.Row(
            [
                txt_number,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    

def main(page: Page):

    page.scroll = "auto"
    page.add(
        Column(
            [
                Collapsible(
                    "Buttons",
                    icon=Icon(icons.SMART_BUTTON),
                    content=Column(
                        [
                            MenuButton("Basic buttons", item_click=my_def_func, page=page),
                            MenuButton("Floating action button", item_click=my_def_func, page=page),
                            MenuButton("Popup menu button", item_click=my_def_func, page=page),
                        ],
                        spacing=3,
                    ),
                ),
                Collapsible(
                    "Simple apps",
                    icon=Icon(icons.NEW_RELEASES),
                    content=Column(
                        [
                            MenuButton("Basic buttons", item_click=my_def_func, page=page),
                            MenuButton("Floating action button", item_click=my_def_func, page=page),
                            MenuButton("Popup menu button", item_click=my_def_func, page=page),
                        ],
                        spacing=3,
                    ),
                ),
                Collapsible(
                    "Forms",
                    icon=Icon(icons.DYNAMIC_FORM),
                    content=Column(
                        [
                            MenuButton("Basic buttons", item_click=my_def_func, page=page),
                            MenuButton("Floating action button", item_click=my_def_func, page=page),
                            MenuButton("Popup menu button", item_click=my_def_func, page=page),
                        ],
                        spacing=3,
                    ),
                ),
            ],
            spacing=3,
            width=230,
        )
    )

ft.app(target=main)
# flet.app(port=8550, target=main, view=flet.WEB_BROWSER)
