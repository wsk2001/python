# -*- coding: utf-8 -*-

import flet as ft

def main(page: ft.Page):
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                txt_number,
                ft.IconButton(ft.icons.ADD, on_click=plus_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

# ft.app(target=main)
ft.app(target=main, view=ft.WEB_BROWSER)


# 이제 앱을 웹 앱으로 실행하려면 마지막 줄을 다음으로 바꾸십시오.
# ft.app(target=main) -> ft.app(target=main, view=ft.WEB_BROWSER)
# 다시 실행하면 이제 즉시 웹 앱을 얻을 수 있습니다.

# pip install flet
# python counter.py
