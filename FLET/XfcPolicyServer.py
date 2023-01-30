# -*- coding: utf-8 -*-

import json
import Xfc.XfcApiClass as XfcApiClass
import Xfc.XfcDB as xdb
import copy

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

api = XfcApiClass.XfcApi()

ta_id = api.id
ta_remark = api.remark
ta_createTime = api.createTime
ta_updateTime = api.updateTime

tb1 = api.platform
tb2 = api.providerName
tb3 = api.process
tb4 = api.ipAddr
tb5 = api.macAddr
tb6 = api.modifiedDate
tb7 = api.domainKeyId
tb8 = api.domainAlgorithm
tb9 = api.domainKeyLength
tb10 = api.modulus
tb11 = api.publicExponent
tb12 = api.privateExponent
tb13 = api.domainCode
tb14 = api.attributeKeyId
tb15 = api.attributeIv
tb16 = api.attributeAlgorithm
tb17 = api.attributeKeyLength
tb18 = api.attributeChiperMode
tb19 = api.attributePaddingMethod
tb20 = api.attributeKeyMaterial
tb21 = api.contentsAlgorithm
tb22 = api.contentsKeyLength
tb23 = api.readChk
tb24 = api.writeChk
tb25 = api.excuteChk
tb26 = api.syncPeriod
tb27 = api.logPeriod
tb28 = api.excludeExts
tb29 = api.decFileSize
tb30 = api.encErrorCode
tb31 = api.decErrorCode


def load_json_file(page: ft.Page, filename):
    with open(filename) as json_file:
        json_data = json.load(json_file)
        tb1.value = json_data["platform"]
        tb2.value = json_data["providerName"]
        tb3.value = json_data["process"]
        tb4.value = json_data["ipAddr"]
        tb5.value = json_data["macAddr"]
        tb6.value = json_data["modifiedDate"]
        tb7.value = json_data["domainKeyId"]
        tb8.value = json_data["domainAlgorithm"]
        tb9.value = json_data["domainKeyLength"]
        tb10.value = json_data["modulus"]
        tb11.value = json_data["publicExponent"]
        tb12.value = json_data["privateExponent"]
        tb13.value = json_data["domainCode"]
        tb14.value = json_data["attributeKeyId"]
        tb15.value = json_data["attributeIv"]
        tb16.value = json_data["attributeAlgorithm"]
        tb17.value = json_data["attributeKeyLength"]
        tb18.value = json_data["attributeChiperMode"]
        tb19.value = json_data["attributePaddingMethod"]
        tb20.value = json_data["attributeKeyMaterial"]
        tb21.value = json_data["contentsAlgorithm"]
        tb22.value = json_data["contentsKeyLength"]
        tb23.value = json_data["readChk"]
        tb24.value = json_data["writeChk"]
        tb25.value = json_data["excuteChk"]
        tb26.value = json_data["syncPeriod"]
        tb27.value = json_data["logPeriod"]
        tb28.value = json_data["excludeExts"]
        tb29.value = json_data["decFileSize"]
        tb30.value = json_data["encErrorCode"]
        tb31.value = json_data["decErrorCode"]

        ta_id.value = "API-" + json_data["ipAddr"]
        ta_remark.value = "API-" + json_data["ipAddr"]

        page.update()

        api.view()


def init_page(page: ft.Page):
    page.title = "XFC Local Agent Policy"

    page.add(ft.Text("XFC API Policy Manager", size=30, color="pink600", italic=True))

    page.add(ft.Row(controls=[api.id, api.remark, api.createTime, api.updateTime]))

    page.add(ft.Row(controls=[api.platform, api.providerName, api.ipAddr, api.macAddr]))
    page.add(ft.Row(controls=[tb7, tb8, tb9]))
    page.add(tb10)
    page.add(tb11, tb12, tb13)
    page.add(ft.Row(controls=[tb14, tb15, tb16, tb17]))
    page.add(ft.Row(controls=[tb18, tb19, tb20]))
    page.add(ft.Row(controls=[tb21, tb22, tb23, tb24, tb25]))
    page.add(ft.Row(controls=[tb26, tb27, tb28, tb29, tb30, tb31]))

    api.clear()

    page.theme_mode = "dark"
    page.update()


def main(page: ft.Page):
    def button_clicked(e):
        t.value = f"Textboxes values are:  '{tb1.value}', '{tb2.value}', '{tb3.value}', '{tb4.value}', '{tb5.value}'."
        page.update()

    def navi_change(e):
        if page.navigation_bar.selected_index == 0:
            page.title = 'Explore'
        elif page.navigation_bar.selected_index == 1:
            page.title = 'Commute'
        elif page.navigation_bar.selected_index == 2:
            page.title = 'Bookmark'
        page.update()

    dbms = xdb.XfcDB()
    dbms.create_api_policy_table()

    t = ft.Text()
    selected_files = ft.Text()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.EXPLORE, label="Explore"),
            ft.NavigationDestination(icon=ft.icons.COMMUTE, label="Commute"),
            ft.NavigationDestination(
                icon=ft.icons.BOOKMARK_BORDER,
                selected_icon=ft.icons.BOOKMARK,
                label="Bookmark",
            ),
        ],
        on_change=navi_change,
    )


    bsave = ft.ElevatedButton(text="저장 하기", icon=ft.icons.SAVE, on_click=button_clicked)
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
    init_page(page)

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

    page.auto_scroll = True


if __name__ == "__main__":
    ft.app(target=main)
    # ft.app(target=main, view=ft.WEB_BROWSER)

# get_directory_path() 는 보안을 이유로 view 가 WEB_BROWSER 인 경우는 동작 하지 않는다.
