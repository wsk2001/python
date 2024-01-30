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
import AclMoudle.WatchPathEdit as WatchPathE
from datetime import datetime
import uuid


dbms = acl.AclDB()
wpe = WatchPathE.WatchPathEdit()

view_type = "flet_app"



def navi_change(e):
    if e.control.selected_index == 0:
        wpe.view_main(e.page, 'Home')
    elif e.control.selected_index == 1:
        wpe.view_main(e.page, '접근 경로 관리')
    elif e.control.selected_index == 2:
        wpe.view_main(e.page, "접근 경로 조회")
    elif e.control.selected_index == 3:
        wpe.view_main(e.page, "접근 제어 관리")
    elif e.control.selected_index == 4:
        wpe.view_main(e.page, "접근 제어 조회")
    elif e.control.selected_index == 5:
        e.page.window_destroy()


def set_navi(page):
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.EDIT_DOCUMENT, label="Home"),
            ft.NavigationDestination(icon=ft.icons.LIST_SHARP, label="접근 경로 관리"),
            ft.NavigationDestination(icon=ft.icons.EDIT_DOCUMENT, label="접근 경로 조회"),
            ft.NavigationDestination(icon=ft.icons.LIST_SHARP, label="접근 제어 관리"),
            ft.NavigationDestination(icon=ft.icons.EDIT_DOCUMENT, label="접근 제어 조회"),
            ft.NavigationDestination(icon=ft.icons.EXIT_TO_APP, label="Exit", ),
        ],
        on_change=navi_change,
    )


def set_appbar(page, pg_title=None):
    def change_theme(e):
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        theme_icon_button.selected = not theme_icon_button.selected
        page.update()

    # button to change theme_mode (from dark to light mode, or the reverse)
    theme_icon_button = ft.IconButton(
        icon=ft.icons.LIGHT_MODE,
        selected_icon=ft.icons.DARK_MODE,
        icon_color=ft.colors.WHITE,
        selected_icon_color=ft.colors.BLACK,
        selected=False,
        icon_size=35,
        tooltip="change theme",
        on_click=change_theme,
    )

    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.PALETTE),
        leading_width=40,
        title=ft.Text("ACL Manager") if pg_title is None else ft.Text(pg_title),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            theme_icon_button,
            ft.IconButton(ft.icons.EXIT_TO_APP, tooltip="Exit to App", on_click=lambda _: page.window_destroy()),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Home", icon=ft.icons.EDIT_DOCUMENT, on_click=lambda _: wpe.view_main(page, "Home")),
                    ft.VerticalDivider(),
                    ft.PopupMenuItem(text="Regist Watch Path", icon=ft.icons.EDIT_DOCUMENT, on_click=lambda _: wpe.view_main(page, "Regist Watch Path")),
                    ft.PopupMenuItem(text="List Watch Path", icon=ft.icons.VIEW_LIST_OUTLINED, on_click=lambda _: wpe.view_main(page, "List Watch Path")),
                    ft.VerticalDivider(),
                    ft.PopupMenuItem(text="Regist AC", icon=ft.icons.EDIT_DOCUMENT, on_click=lambda _: wpe.view_main(page, "Regist AC")),
                    ft.PopupMenuItem(text="List AC", icon=ft.icons.VIEW_LIST_OUTLINED, on_click=lambda _: wpe.view_main(page, "List AC")),
                    ft.VerticalDivider(),
                    ft.PopupMenuItem(text="Exit App", icon=ft.icons.EXIT_TO_APP, on_click=lambda _: page.window_destroy()),
                ]
            ),
        ],
    )



def main_page(page: ft.Page):
    curr_hour = datetime.now().time().hour
    if curr_hour < 7 or 18 < curr_hour:
        page.theme_mode = "light"
    else:
        page.theme_mode = "dark"

    # page.bgcolor = colors.BLUE_GREY_900
    page.title = "ACL Manager"
    page.scroll = "auto"
    page.window_maximized = True

    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    dbms.create_watch_path_table()
    dbms.create_access_control_table()

    set_appbar(page)
    set_navi(page)
    wpe.view_main(page, "Home")


def main(page: ft.Page):
    main_page(page)
    # LoginPage.Login(page, main_page, "Login 정보를 입력 하세요.")


# if __name__ == "__main__": 에서는 global 을 선언 하지 않는다.
# 이유는 ? if __name__ 문장이 있는곳은 함수 또는 Class 내부가 아니라 외부(즉 전역 영역) 이기 때문 이다.

if __name__ == "__main__":
    target = main
    view_type = ft.FLET_APP
    # view_type = ft.WEB_BROWSER

    ft.app(target=target, view=view_type, assets_dir='assets')

