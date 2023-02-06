# -*- coding: utf-8 -*-

import flet as ft
from flet import (
    FilePicker,
    FilePickerResultEvent,
    Text
)

import Xfc.XfcApiClass as XfcApiClass
import Xfc.XfcLaClass as XfcLaClass
import Xfc.XfcSaClass as XfcSaClass

import Xfc.XfcDB as xdb

dbms = xdb.XfcDB()
api = XfcApiClass.XfcApi()
la_policy = XfcLaClass.XfcLaPolicy()
sa_policy = XfcSaClass.XfcSaPolicy()

selected_id = None
xfc_page = None


def load_json_file(page: ft.Page, filename):
    XfcApiClass.load_json_file(page, filename, api)


def navi_change(e):
    _navi_change(xfc_page)


def _navi_change(page: ft.Page):
    if page.navigation_bar.selected_index == 0:
        api_policy_page(page)
    elif page.navigation_bar.selected_index == 1:
        api_policy_list_page(page)
    elif page.navigation_bar.selected_index == 2:
        la_policy_page(page)
    elif page.navigation_bar.selected_index == 3:
        la_policy_list_page(page)
    elif page.navigation_bar.selected_index == 4:
        sa_policy_page(page)
    elif page.navigation_bar.selected_index == 5:
        sa_policy_list_page(page)
    elif page.navigation_bar.selected_index == 6:
        page.window_destroy()
    page.update()


def set_navi():
    xfc_page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.EDIT, label="API Edit"),
            ft.NavigationDestination(icon=ft.icons.LIST_OUTLINED, label="API List"),
            ft.NavigationDestination(icon=ft.icons.EDIT_LOCATION, label="LA Edit"),
            ft.NavigationDestination(icon=ft.icons.LIST_ALT_SHARP, label="LA List"),
            ft.NavigationDestination(icon=ft.icons.EDIT_NOTE, label="SA Edit"),
            ft.NavigationDestination(icon=ft.icons.LIST_SHARP, label="SA List"),
            ft.NavigationDestination(icon=ft.icons.EXIT_TO_APP, label="Exit", ),
        ],
        on_change=navi_change,
    )


def api_policy_page(page: ft.Page):
    global selected_id

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
    # page.auto_scroll = True

    page.title = "XFC API Policy Manager"

    page.add(ft.Text("Edit XFC API Policy", size=30, color="pink600", italic=True))

    page.add(ft.Row(controls=[api.id, api.remark, api.createTime, api.updateTime]))

    page.add(ft.Row(controls=[api.platform, api.providerName, api.ipAddr, api.macAddr]))
    page.add(ft.Row(controls=[api.domainKeyId, api.domainAlgorithm, api.domainKeyLength]))
    page.add(api.modulus)
    page.add(api.publicExponent, api.privateExponent, api.domainCode)
    page.add(ft.Row(controls=[api.attributeKeyId, api.attributeIv, api.attributeAlgorithm, api.attributeKeyLength]))
    page.add(ft.Row(controls=[api.attributeChiperMode, api.attributePaddingMethod, api.attributeKeyMaterial]))
    page.add(ft.Row(controls=[api.contentsAlgorithm, api.contentsKeyLength, api.readChk, api.writeChk, api.excuteChk]))
    page.add(ft.Row(
        controls=[api.syncPeriod, api.logPeriod, api.excludeExts, api.decFileSize, api.encErrorCode, api.decErrorCode]))

    api.clear()

    if selected_id != None:
        dbms.get_api_policy(api, selected_id)
        selected_id = None

    get_directory_dialog = FilePicker(on_result=get_directory_result)
    directory_path = Text()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)

    page.overlay.extend([pick_files_dialog, get_directory_dialog])

    page.add(ft.Row(controls=[bsave, bopendir, bfilepick, selected_files]))

    set_navi()

    page.theme_mode = "dark"
    page.window_maximized = True
    page.update()


def api_policy_list_page(page: ft.Page, key_id=None):
    global selected_id

    page.clean()

    def selectOnTap(e):
        if 0 < len(e.control.content.value):
            tf_id.value = e.control.content.value
            page.update()

    def call_edit_page(e):
        global selected_id
        selected_id = tf_id.value
        api_policy_page(page)

    def delete_data(e):
        if 0 < len(tf_id.value):
            dbms.delete_api_policy(tf_id.value)
            dlg = ft.AlertDialog(
                title=ft.Text(f"ID {tf_id.value} Data 를 삭제 하였습니다.")
            )
            page.dialog = dlg
            dlg.open = True
            page.update()
            api_policy_list_page(page)

    def search_data(e):
        if 0 < len(tf_id_search.value):
            api_policy_list_page(page, tf_id_search.value)
        else:
            dlg = ft.AlertDialog(
                title=ft.Text(f"검색할 ID 의 일부를 입력 하세요.")
            )
            page.dialog = dlg
            dlg.open = True
            page.update()

    set_navi()

    page.theme_mode = "dark"

    page.add(ft.Text("List XFC API Policy", size=30, color="pink600", italic=True))
    tf_id = ft.TextField(label="선택된 ID", color="cyan")
    btn_edit = ft.ElevatedButton(text="선택 항목 편집", icon=ft.icons.EDIT_ROAD, on_click=call_edit_page)
    btn_del = ft.ElevatedButton(text="선택 항목 삭제", icon=ft.icons.DELETE, on_click=delete_data)
    tf_id_search = ft.TextField(label="검색할 ID", color="pink")
    btn_find = ft.ElevatedButton(text="검색", icon=ft.icons.FIND_IN_PAGE_OUTLINED, on_click=search_data)

    page.add(ft.Row(controls=[tf_id, btn_edit, btn_del, tf_id_search, btn_find]))

    header = [ft.DataColumn(ft.Text("ID", color="pink600")), ft.DataColumn(ft.Text("ip Address", color="cyan")),
              ft.DataColumn(ft.Text("Remark", width=480, color="cyan")),
              ft.DataColumn(ft.Text("Create Time", color="cyan")), ft.DataColumn(ft.Text("Update Time", color="cyan")),
              ft.DataColumn(ft.Text("Platform", color="cyan")), ft.DataColumn(ft.Text("Domain Key ID", color="cyan"))]

    if key_id is None:
        df = dbms.get_api_policy_list()
    else:
        df = dbms.get_api_policy_list(key_id)

    value_list = df.values.tolist()
    low_list = []
    low_list.clear()

    first_row = True
    for v in value_list:
        low_list.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(v[0], color="cyan"), on_tap=selectOnTap),
                    ft.DataCell(ft.Text(v[1])), ft.DataCell(ft.Text(v[2])),
                    ft.DataCell(ft.Text(v[3])), ft.DataCell(ft.Text(v[4])),
                    ft.DataCell(ft.Text(v[5])), ft.DataCell(ft.Text(v[6])),
                ],
            )
        )
        if first_row:
            tf_id.value = v[0]
            first_row = False

    page.add(
        ft.DataTable(
            heading_row_color=ft.colors.BLACK12,
            columns=header,
            rows=low_list,
        ),
    )

    page.update()


def la_policy_page(page: ft.Page):
    page.clean()

    def button_save(e):
        pass

    set_navi()

    page.theme_mode = "dark"

    title = ft.Text("Edit XFC Local Agent Policy", size=30, color="blue600", italic=True)
    btn_save = ft.ElevatedButton(text="저장 하기", icon=ft.icons.SAVE, on_click=button_save)
    page.add(title)
    page.add(btn_save)

    page.add(ft.Row(controls=[la_policy.ip, la_policy.policy, la_policy.description]))
    page.add(ft.Row(controls=[la_policy.ip, la_policy.policy, la_policy.description]))
    page.add(la_policy.base_path)
    page.add(la_policy.dir)
    page.add(ft.Row(controls=[ft.Text("암/복호화 모드를 선택 하세요"), la_policy.mode, la_policy.time_limit, la_policy.check_file_closed]))
    page.add(ft.Row(controls=[la_policy.use_file_filter, la_policy.file_filter_type, la_policy.file_filter_exts]))
    page.add(ft.Row(controls=[la_policy.check_cycle, la_policy.thread_count]))
    page.add(ft.Row(controls=[la_policy.use_backup, la_policy.backup_path]))
    page.add(ft.Row(controls=[la_policy.temp_path, la_policy.dir_depth, la_policy.dir_format, la_policy.ymd_offset]))
    page.add(ft.Row(controls=[la_policy.use_trigger_file, la_policy.trigger_ext, la_policy.trigger_target]))

    page.update()


def la_policy_list_page(page: ft.Page):
    page.clean()
    set_navi()

    page.theme_mode = "dark"

    page.add(ft.Text("List XFC Local Agent Policy", size=30, color="blue600", italic=True))
    page.update()


def sa_policy_page(page: ft.Page):
    page.clean()
    set_navi()

    page.theme_mode = "dark"

    page.add(ft.Text("Edit XFC Schedule Agent Policy", size=30, color="yellow600", italic=True))
    page.update()


def sa_policy_list_page(page: ft.Page):
    page.clean()
    set_navi()

    page.theme_mode = "dark"

    page.add(ft.Text("List XFC Schedule Agent Policy", size=30, color="yellow600", italic=True))
    page.update()


def main(page: ft.Page):
    global xfc_page
    dbms.create_api_policy_table()
    dbms.create_la_policy_table()
    dbms.create_sa_policy_table()

    xfc_page = page
    api_policy_page(page)


if __name__ == "__main__":
    ft.app(target=main)
    # ft.app(target=main, view=ft.WEB_BROWSER)

# flet 종료 방법 : page.window_destroy(): WEB 에서는 정상 동작 하지 않음.
# get_directory_path() 는 보안을 이유로 view 가 WEB_BROWSER 인 경우는 정상 동작 하지 않는다.
