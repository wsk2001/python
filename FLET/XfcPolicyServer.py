# -*- coding: utf-8 -*-

import json
import sys

import Xfc.XfcApiClass as XfcApiClass
import Xfc.XfcDB as xdb
import copy
from datetime import datetime

import flet as ft
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    icons,
    Theme
)

dbms = xdb.XfcDB()
api = XfcApiClass.XfcApi()


def load_json_file(page: ft.Page, filename):
    XfcApiClass.load_json_file(page, filename, api)


def input_page(page: ft.Page):
    page.clean()

    def button_save(e):
        if 0 < len(api.id.value):
            dbms.insert_api_policy(api)
            dlg = ft.AlertDialog(
                title=ft.Text(f"ID {api.id.value} Data 를 저장 하였습니다.")
            )
            page.dialog = dlg
            dlg.open = True
            page.update()
            api.clear()
            page.update()
        else:
            dlg = ft.AlertDialog(
                title=ft.Text("ID 가 입력되지 않았습니다.\n 저장 할 수 없습니다.")
            )
            page.dialog = dlg
            dlg.open = True
            page.update()

    def navi_change(e):
        _navi_change(page)

    selected_files = ft.Text()

    bsave = ft.ElevatedButton(text="저장 하기", icon=ft.icons.SAVE, on_click=button_save)
    bfilepick = ft.ElevatedButton(
                                  "Pick files",
                                  icon=ft.icons.FILE_OPEN,
                                  on_click=lambda _: pick_files_dialog.pick_files(
                                      allow_multiple=False,
                                      initial_directory=directory_path.value,
                                      allowed_extensions=['json']
                                  ),
                              )
    bopendir = ft.ElevatedButton(
                                  "Open director",
                                  icon=ft.icons.FOLDER_OPEN,
                                  on_click=lambda _: pick_files_dialog.get_directory_path(initial_directory='.'),
                              )

    page.title = "XFC Local Agent Policy"

    page.add(ft.Text("Edit XFC API Policy", size=30, color="pink600", italic=True))

    page.add(ft.Row(controls=[api.id, api.remark, api.createTime, api.updateTime]))

    page.add(ft.Row(controls=[api.platform, api.providerName, api.ipAddr, api.macAddr]))
    page.add(ft.Row(controls=[api.domainKeyId, api.domainAlgorithm, api.domainKeyLength]))
    page.add(api.modulus)
    page.add(api.publicExponent, api.privateExponent, api.domainCode)
    page.add(ft.Row(controls=[api.attributeKeyId, api.attributeIv, api.attributeAlgorithm, api.attributeKeyLength]))
    page.add(ft.Row(controls=[api.attributeChiperMode, api.attributePaddingMethod, api.attributeKeyMaterial]))
    page.add(ft.Row(controls=[api.contentsAlgorithm, api.contentsKeyLength, api.readChk, api.writeChk, api.excuteChk]))
    page.add(ft.Row(controls=[api.syncPeriod, api.logPeriod, api.excludeExts, api.decFileSize, api.encErrorCode, api.decErrorCode]))

    api.clear()

    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files is not None:
            for f in e.files:
                selected_files.value = f.path

            selected_files.update()

        load_json_file(page, selected_files.value)

    # Open directory dialog
    def get_directory_result(e: FilePickerResultEvent):
        directory_path.value = e.path if e.path else "Cancelled!"
        directory_path.update()

    get_directory_dialog = FilePicker(on_result=get_directory_result)
    directory_path = Text()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)

    page.overlay.extend([pick_files_dialog, get_directory_dialog])

    page.add(ft.Row(controls=[bsave, bopendir, bfilepick, selected_files]))

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.CREATE, label="Edit"),
            ft.NavigationDestination(icon=ft.icons.EXPLORE, label="Select"),
            ft.NavigationDestination(icon=ft.icons.EXIT_TO_APP, label="Exit",),
        ],
        on_change=navi_change,
    )

    page.theme_mode = "dark"

    page.update()


def select_page(page: ft.Page):
    page.clean()

    def navi_change(e):
        _navi_change(page)

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.CREATE, label="Edit"),
            ft.NavigationDestination(icon=ft.icons.EXPLORE, label="Select"),
            ft.NavigationDestination(icon=ft.icons.EXIT_TO_APP, label="Exit",),
        ],
        on_change=navi_change,
    )

    page.theme_mode = "dark"

    page.add(ft.Text("Select XFC API Policy", size=30, color="pink600", italic=True))

    header = []
    header.clear()
    header.append(ft.DataColumn(ft.Text("ID")))
    header.append(ft.DataColumn(ft.Text("p Address")))
    header.append(ft.DataColumn(ft.Text("Remark")))
    header.append(ft.DataColumn(ft.Text("Create Time")))
    header.append(ft.DataColumn(ft.Text("Update Time")))
    header.append(ft.DataColumn(ft.Text("Platform")))
    header.append(ft.DataColumn(ft.Text("Domain Key ID")))

    page.add(
        ft.DataTable(
            columns=header,
            show_checkbox_column=True,
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("API-192.168.60.190-01")),
                        ft.DataCell(ft.Text("192.168.60.190")),
                        ft.DataCell(ft.Text("XFC API Policy-001")),
                        ft.DataCell(ft.Text("2023-01-31 11:05:37")),
                        ft.DataCell(ft.Text("2023-01-31 11:05:37")),
                        ft.DataCell(ft.Text("Windows 10")),
                        ft.DataCell(ft.Text("69a072a3-2e51-4099-b0e6-53f8669906eb")),
                    ],
                    on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("API-192.168.60.211-02")),
                        ft.DataCell(ft.Text("192.168.60.211")),
                        ft.DataCell(ft.Text("XFC API Policy-002")),
                        ft.DataCell(ft.Text("2023-01-31 11:05:37")),
                        ft.DataCell(ft.Text("2023-01-31 11:05:37")),
                        ft.DataCell(ft.Text("Linux")),
                        ft.DataCell(ft.Text("69a072a3-2e51-4099-b0e6-53f8669906eb")),
                    ],
                    on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("API-192.168.60.190-03")),
                        ft.DataCell(ft.Text("192.168.60.190")),
                        ft.DataCell(ft.Text("XFC API Policy-003")),
                        ft.DataCell(ft.Text("2023-01-31 11:05:37")),
                        ft.DataCell(ft.Text("2023-01-31 11:05:37")),
                        ft.DataCell(ft.Text("Windows 10")),
                        ft.DataCell(ft.Text("69a072a3-2e51-4099-b0e6-53f8669906eb")),
                    ],
                    on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                ),
            ],
        ),
    )

    page.update()


def _navi_change(page: ft.Page):
    if page.navigation_bar.selected_index == 0:
        input_page(page)
        page.title = 'Edit'
    elif page.navigation_bar.selected_index == 1:
        select_page(page)
        page.title = 'Select'
    elif page.navigation_bar.selected_index == 2:
        page.title = 'Exit'
        sys.exit(-1)
    page.update()


def main(page: ft.Page):
    dbms.create_api_policy_table()

    input_page(page)


if __name__ == "__main__":
    ft.app(target=main)
    # ft.app(target=main, view=ft.WEB_BROWSER)

# get_directory_path() 는 보안을 이유로 view 가 WEB_BROWSER 인 경우는 동작 하지 않는다.
