# -*- coding: utf-8 -*-

import flet as ft
from flet import (
    FilePicker,
    FilePickerResultEvent,
    Text,
    AlertDialog,
    colors,
    Icon
)

import AclMoudle.AclDB as acl

class WatchPathEdit:
    def __init__(self):
        self.database_name = './dbms/xdb_acl.db3'

    def view_main(self, page: ft.Page, txt: str):
        txt_number = ft.TextField(value=txt, text_align=ft.TextAlign.CENTER, width=300)
        # navibar, appbar 등은 clean 되지 않는다.
        page.clean()
        page.add(
            ft.Row(
                [
                    txt_number,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )


