# -*- coding: utf-8 -*-

import flet as ft
from flet import (
    FilePicker,
    FilePickerResultEvent,
    Text,
    Icon
)

import Xfc.XfcApiClass as XfcApiClass
import Xfc.XfcLaClass as XfcLaClass
import Xfc.XfcSaClass as XfcSaClass

import Xfc.XfcDB as xdb

dbms = xdb.XfcDB()
api = XfcApiClass.XfcApi()
la_policy = XfcLaClass.XfcLaPolicy()
sa_policy = XfcSaClass.XfcSaPolicy()

view_type = "flet_app"


def load_json_file(page: ft.Page, filename):
    XfcApiClass.load_json_file(page, filename, api)


def navi_change(e):
    if e.control.selected_index == 0:
        api_policy_page(e.page)
    elif e.control.selected_index == 1:
        api_policy_list_page(e.page)
    elif e.control.selected_index == 2:
        la_policy_page(e.page)
    elif e.control.selected_index == 3:
        la_policy_list_page(e.page)
    elif e.control.selected_index == 4:
        sa_policy_page(e.page)
    elif e.control.selected_index == 5:
        sa_policy_list_page(e.page)
    elif e.control.selected_index == 6:
        e.page.window_destroy()


def set_navi(page):
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.EDIT_DOCUMENT, label="API Edit"),
            ft.NavigationDestination(icon=ft.icons.LIST_SHARP, label="API List"),
            ft.NavigationDestination(icon=ft.icons.EDIT_DOCUMENT, label="LA Edit"),
            ft.NavigationDestination(icon=ft.icons.LIST_SHARP, label="LA List"),
            ft.NavigationDestination(icon=ft.icons.EDIT_DOCUMENT, label="SA Edit"),
            ft.NavigationDestination(icon=ft.icons.LIST_SHARP, label="SA List"),
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
        title=ft.Text("XFC Policy Manager") if pg_title is None else ft.Text(pg_title),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            theme_icon_button,
            ft.IconButton(ft.icons.EXIT_TO_APP, tooltip="Exit to App", on_click=lambda _: page.window_destroy()),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="API 정책 관리", icon=ft.icons.EDIT_DOCUMENT, on_click=lambda _: api_policy_page(page)),
                    ft.PopupMenuItem(text="API 정책 조회", icon=ft.icons.FORMAT_LIST_BULLETED_SHARP, on_click=lambda _: api_policy_list_page(page)),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(text="LocalAgent 정책 관리", icon=ft.icons.EDIT_DOCUMENT, on_click=lambda _: la_policy_page(page)),
                    ft.PopupMenuItem(text="LocalAgent 정책 조회", icon=ft.icons.FORMAT_LIST_BULLETED_SHARP, on_click=lambda _: la_policy_list_page(page)),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(text="ScheduleAgent 정책 관리", icon=ft.icons.EDIT_DOCUMENT, on_click=lambda _: sa_policy_page(page)),
                    ft.PopupMenuItem(text="ScheduleAgent 정책 조회", icon=ft.icons.FORMAT_LIST_BULLETED_SHARP, on_click=lambda _: sa_policy_list_page(page)),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(text="App 종료", icon=ft.icons.EXIT_TO_APP, on_click=lambda _: page.window_destroy())
                ]
            ),
        ],
    )


def api_policy_page(page: ft.Page, selected_id=None):

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

    def new_click(e):
        api.clear()
        page.update()

    page.appbar.title = ft.Text("XFC API Policy")
    selected_files = ft.Text()

    btn_save = ft.ElevatedButton(text="저장 하기", icon=ft.icons.SAVE_ALT, on_click=button_save)
    btn_new = ft.ElevatedButton(text="새로 만들기", icon=ft.icons.FIBER_NEW_ROUNDED, on_click=new_click)

    file_pick = ft.ElevatedButton(
        "File 선택",
        icon=ft.icons.FILE_OPEN,
        on_click=lambda _: pick_files_dialog.pick_files(
            allow_multiple=False,
            initial_directory=directory_path.value,
            allowed_extensions=['json']
        ),
    )
    open_dir = ft.ElevatedButton(
        "Director 선택",
        icon=ft.icons.FOLDER_OPEN,
        on_click=lambda _: pick_files_dialog.get_directory_path(initial_directory='.'),
    )

    global view_type
    if view_type == ft.FLET_APP:
        page.add(ft.Row(controls=[btn_save, btn_new, ft.Text("json 파일 load ->", color="cyan"),
                                  open_dir, file_pick, selected_files]))
    else:
        page.add(ft.Row(controls=[btn_save, btn_new]))

    page.add(ft.Row(controls=[api.id, api.remark]))
    page.add(ft.Row(controls=[api.createTime, api.updateTime]))
    page.add(ft.Row(controls=[api.platform, api.providerName, api.ipAddr, api.macAddr]))
    page.add(ft.Row(controls=[api.domainKeyId, api.domainAlgorithm, api.domainKeyLength]))
    page.add(api.modulus)
    page.add(api.publicExponent, api.privateExponent, api.domainCode)
    page.add(ft.Row(controls=[api.attributeKeyId, api.attributeIv, api.attributeAlgorithm, api.attributeKeyLength]))
    page.add(ft.Row(controls=[api.attributeChiperMode, api.attributePaddingMethod, api.attributeKeyMaterial]))
    page.add(ft.Row(controls=[api.contentsAlgorithm, api.contentsKeyLength]))
    page.add(ft.Row(controls=[api.readChk, api.writeChk, api.excuteChk]))
    page.add(ft.Row(controls=[api.syncPeriod, api.logPeriod, api.excludeExts, api.decFileSize]))
    page.add(ft.Row(controls=[api.encErrorCode, api.decErrorCode]))

    api.clear()

    if selected_id is not None:
        dbms.get_api_policy(api, selected_id)

    get_directory_dialog = FilePicker(on_result=get_directory_result)
    directory_path = Text()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)

    page.overlay.extend([pick_files_dialog, get_directory_dialog])

    page.update()


def api_policy_list_page(page: ft.Page, key_id=None):
    page.clean()

    def selectOnTap(e):
        if 0 < len(e.control.content.value):
            tf_id.value = e.control.content.value
            page.update()

    def call_edit_page(e):
        api_policy_page(page, tf_id.value)

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

    page.appbar.title = ft.Text("List XFC API Policy")

    tf_id = ft.TextField(label="선택된 ID", color="cyan")
    btn_edit = ft.ElevatedButton(text="선택 항목 편집", icon=ft.icons.EDIT_DOCUMENT, on_click=call_edit_page)
    btn_del = ft.ElevatedButton(text="선택 항목 삭제", icon=ft.icons.DELETE, on_click=delete_data)
    tf_id_search = ft.TextField(label="검색할 ID", color="pink")
    btn_find = ft.ElevatedButton(text="검색", icon=ft.icons.SEARCH, on_click=search_data)

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


def la_policy_page(page: ft.Page, ip=None, policy=None):
    page.clean()

    def button_save(e):
        if 0 < len(la_policy.ip.value) and 0 < len(la_policy.policy.value):
            dbms.insert_la_policy(la_policy)
            dlg = ft.AlertDialog(
                title=ft.Text(f"ip:{la_policy.ip.value}, policy:{la_policy.policy.value} Data 를 저장 하였습니다.")
            )
            page.dialog = dlg
            dlg.open = True
            page.update()
            la_policy.clear()
            page.update()
        else:
            dlg = ft.AlertDialog(
                title=ft.Text("ip 또는 policy 가 입력되지 않았습니다.\n 저장 할 수 없습니다.")
            )
            page.dialog = dlg
            dlg.open = True
            page.update()

    def new_click(e):
        la_policy.clear()
        page.update()

    page.appbar.title = ft.Text("XFC Local Agent Policy")
    btn_save = ft.ElevatedButton(text="저장 하기", icon=ft.icons.SAVE_ALT, on_click=button_save)
    btn_new = ft.ElevatedButton(text="새로 만들기", icon=ft.icons.FIBER_NEW_OUTLINED, on_click=new_click)
    page.add(ft.Row(controls=[btn_save, btn_new]))

    page.add(ft.Row(controls=[la_policy.ip, la_policy.policy, la_policy.description]))
    page.add(la_policy.base_path)
    page.add(la_policy.dir)
    page.add(ft.Row(
        controls=[ft.Text("암/복호화 모드를 선택 하세요"), la_policy.mode, la_policy.time_limit, la_policy.check_file_closed]))
    page.add(ft.Row(controls=[la_policy.use_file_filter, la_policy.file_filter_type, la_policy.file_filter_exts]))
    page.add(ft.Row(controls=[la_policy.check_cycle, la_policy.thread_count]))
    page.add(ft.Row(controls=[la_policy.use_backup, la_policy.backup_path]))
    page.add(ft.Row(controls=[la_policy.temp_path, la_policy.dir_depth, la_policy.dir_format, la_policy.ymd_offset]))
    page.add(ft.Row(controls=[la_policy.use_trigger_file, la_policy.trigger_ext, la_policy.trigger_target]))

    if ip is not None:
        dbms.get_la_policy(la_policy, ip, policy)

    page.update()


def la_policy_list_page(page: ft.Page):
    def select_ip(e):
        if 0 < len(e.control.content.value):
            tf_ip.value = e.control.content.value
            page.update()

    def select_policy(e):
        if 0 < len(e.control.content.value):
            tf_policy.value = e.control.content.value
            page.update()

    def call_edit_page(e):
        la_policy_page(page, tf_ip.value, tf_policy.value)

    def delete_data(e):
        dbms.delete_la_policy(tf_ip.value, tf_policy.value)
        la_policy_list_page(page)

    def search_data(e):
        dbms.get_la_policy(tf_ip.value, tf_policy.value)
        la_policy_page(page)

    page.clean()

    page.appbar.title = ft.Text("List XFC Local Agent Policy")

    tf_ip = ft.TextField(label="ip", color="cyan")
    tf_policy = ft.TextField(label="policy", color="cyan")
    btn_edit = ft.ElevatedButton(text="선택 항목 편집", icon=ft.icons.EDIT_DOCUMENT, on_click=call_edit_page)
    btn_del = ft.ElevatedButton(text="선택 항목 삭제", icon=ft.icons.DELETE, on_click=delete_data)
    btn_find = ft.ElevatedButton(text="검색", icon=ft.icons.SEARCH, on_click=search_data)

    page.add(ft.Row(controls=[tf_ip, tf_policy, btn_edit, btn_del, btn_find]))

    header = [ft.DataColumn(ft.Text("ip", color="blue600")), ft.DataColumn(ft.Text("policy", color="blue600")),
              ft.DataColumn(ft.Text("description", width=380, color="cyan")),
              ft.DataColumn(ft.Text("base_path", width=380, color="cyan")), ft.DataColumn(ft.Text("dir", width=380, color="cyan")),
              ft.DataColumn(ft.Text("mode", color="cyan")), ft.DataColumn(ft.Text("temp_path", color="cyan"))]

    df = dbms.get_la_policy_list()
    value_list = df.values.tolist()
    low_list = []
    low_list.clear()

    first_row = True
    for v in value_list:
        low_list.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(v[0], color="cyan"), on_tap=select_ip),
                    ft.DataCell(ft.Text(v[1], color="cyan"), on_tap=select_policy), ft.DataCell(ft.Text(v[2])),
                    ft.DataCell(ft.Text(v[3])), ft.DataCell(ft.Text(v[4])),
                    ft.DataCell(ft.Text(v[5])), ft.DataCell(ft.Text(v[6])),
                ],
            )
        )
        if first_row:
            tf_ip.value = v[0]
            tf_policy.value = v[1]
            first_row = False

    page.add(
        ft.DataTable(
            heading_row_color=ft.colors.BLACK12,
            columns=header,
            rows=low_list,
        ),
    )

    page.update()


def sa_policy_page(page: ft.Page, ip=None, policy=None):
    def button_save(e):
        if 0 < len(sa_policy.ip.value) and 0 < len(sa_policy.policy.value):
            dbms.insert_sa_policy(sa_policy)
            dlg = ft.AlertDialog(
                title=ft.Text(f"ip:{sa_policy.ip.value}, policy:{sa_policy.policy.value} Data 를 저장 하였습니다.")
            )
            page.dialog = dlg
            dlg.open = True
            page.update()
            sa_policy.clear()
            page.update()
        else:
            dlg = ft.AlertDialog(
                title=ft.Text("ip 또는 policy 가 입력되지 않았습니다.\n 저장 할 수 없습니다.")
            )
            page.dialog = dlg
            dlg.open = True
            page.update()

    def new_click(e):
        sa_policy.clear()
        page.update()

    page.clean()

    page.appbar.title = ft.Text("XFC Schedule Agent Policy")

    btn_save = ft.ElevatedButton(text="저장 하기", icon=ft.icons.SAVE_ALT, on_click=button_save)
    btn_new = ft.ElevatedButton(text="새로 만들기", icon=ft.icons.FIBER_NEW_OUTLINED, on_click=new_click)
    page.add(ft.Row(controls=[btn_save,btn_new]))

    page.add(ft.Row(controls=[sa_policy.ip, sa_policy.policy, sa_policy.description]))
    page.add(sa_policy.file_path)
    page.add(ft.Row(controls=[ft.Text("암/복호화 모드를 선택 하세요"), sa_policy.mode, sa_policy.time_limit, sa_policy.repeat]))
    page.add(ft.Row(controls=[sa_policy.dir_depth, sa_policy.dir_format, sa_policy.ymd_offset]))
    page.add(ft.Row(controls=[sa_policy.use_weekday, sa_policy.weekdays, sa_policy.sun, sa_policy.mon, sa_policy.tue,
                              sa_policy.wed, sa_policy.thu, sa_policy.fri, sa_policy.sat]))
    page.add(ft.Row(controls=[sa_policy.day,sa_policy.hh,sa_policy.mm,sa_policy.ss]))
    page.add(ft.Row(controls=[sa_policy.use_file_filter, sa_policy.file_filter_type, sa_policy.file_filter_exts]))
    page.add(ft.Row(controls=[sa_policy.check_file_closed, sa_policy.thread_count, sa_policy.check_cycle]))
    page.add(ft.Row(controls=[sa_policy.use_backup, sa_policy.backup_path]))
    page.add(sa_policy.temp_path)

    if ip is not None:
        dbms.get_sa_policy(sa_policy, ip, policy)

    page.update()


def sa_policy_list_page(page: ft.Page):
    def select_ip(e):
        if 0 < len(e.control.content.value):
            tf_ip.value = e.control.content.value
            page.update()

    def select_policy(e):
        if 0 < len(e.control.content.value):
            tf_policy.value = e.control.content.value
            page.update()

    def call_edit_page(e):
        sa_policy_page(page, tf_ip.value, tf_policy.value)

    def delete_data(e):
        dbms.delete_sa_policy(tf_ip.value, tf_policy.value)
        sa_policy_list_page(page)

    def search_data(e):
        dbms.get_sa_policy(tf_ip.value, tf_policy.value)
        sa_policy_page(page)

    page.clean()

    page.appbar.title = ft.Text("List XFC Schedule Agent Policy")

    tf_ip = ft.TextField(label="ip", color="cyan")
    tf_policy = ft.TextField(label="policy", color="cyan")
    btn_edit = ft.ElevatedButton(text="선택 항목 편집", icon=ft.icons.EDIT_DOCUMENT, on_click=call_edit_page)
    btn_del = ft.ElevatedButton(text="선택 항목 삭제", icon=ft.icons.DELETE, on_click=delete_data)
    btn_find = ft.ElevatedButton(text="검색", icon=ft.icons.SEARCH, on_click=search_data)

    page.add(ft.Row(controls=[tf_ip, tf_policy, btn_edit, btn_del, btn_find]))

    # ip, policy, description, file_path, mode, repeat, day, hh, mm, ss
    header = [ft.DataColumn(ft.Text("ip", color="blue600")),
              ft.DataColumn(ft.Text("policy", color="blue600")),
              ft.DataColumn(ft.Text("description", width=380, color="cyan")),
              ft.DataColumn(ft.Text("file_path", width=380, color="cyan")),
              ft.DataColumn(ft.Text("mode", width=120, color="cyan")),
              ft.DataColumn(ft.Text("repeat", color="cyan")),
              ft.DataColumn(ft.Text("day", color="cyan")),
              ft.DataColumn(ft.Text("hh", color="cyan")),
              ft.DataColumn(ft.Text("mm", color="cyan")),
              ft.DataColumn(ft.Text("ss", color="cyan"))]

    df = dbms.get_sa_policy_list()
    value_list = df.values.tolist()
    low_list = []
    low_list.clear()

    first_row = True
    for v in value_list:
        low_list.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(v[0], color="cyan"), on_tap=select_ip),
                    ft.DataCell(ft.Text(v[1], color="cyan"), on_tap=select_policy),
                    ft.DataCell(ft.Text(v[2])),
                    ft.DataCell(ft.Text(v[3])),
                    ft.DataCell(ft.Text(v[4])),
                    ft.DataCell(ft.Text(v[5])),
                    ft.DataCell(ft.Text(v[6])),
                    ft.DataCell(ft.Text(v[7])),
                    ft.DataCell(ft.Text(v[8])),
                    ft.DataCell(ft.Text(v[9])),
                ],
            )
        )
        if first_row:
            tf_ip.value = v[0]
            tf_policy.value = v[1]
            first_row = False

    page.add(
        ft.DataTable(
            heading_row_color=ft.colors.BLACK12,
            columns=header,
            rows=low_list,
        ),
    )

    page.update()


def main(page: ft.Page):
    page.theme_mode = "dark"
    page.title = "XFC Manager"
    # page.scroll = "always"
    page.scroll = "auto"

    dbms.create_api_policy_table()
    dbms.create_la_policy_table()
    dbms.create_sa_policy_table()

    set_appbar(page)
    # set_navi(page)
    api_policy_page(page)


# if __name__ == "__main__": 에서는 global 을 선언 하지 않는다.
# 이유는 ? if __name__ 문장이 있는곳은 함수 또는 Class 내부가 아니라 외부(즉 전역 영역) 이기 때문 이다.

if __name__ == "__main__":
    target = main
    view_type = ft.FLET_APP
    # view_type = ft.WEB_BROWSER

    ft.app(target=target, view=view_type, assets_dir='assets')

# flet 종료 방법 : page.window_destroy(): WEB 에서는 정상 동작 하지 않음.
# get_directory_path() 는 보안을 이유로 view 가 WEB_BROWSER 인 경우는 정상 동작 하지 않는다.
