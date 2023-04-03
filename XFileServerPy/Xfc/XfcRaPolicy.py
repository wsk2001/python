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
import json
from datetime import datetime

# 동일 경로에 있는 파일 import
from flet_core import MainAxisAlignment

from . import XfcDB as xdb
import uuid

class CAclDetail:
    def __init__(self):
        self.id = ''
        self.ra_acls_id = ''
        self.ip = ''
        self.start_ip = ''
        self.end_ip = ''
        self.uid = ''
        self.gid = ''
        self.enc = '' # yes/ no
        self.dec = '' # yes/ no

class CAcl:
    def __init__(self):
        self.id = ''
        self.ra_id = ''
        self.path = ''
        self.exclude_exts = ''
        self.base_enc = '' # yes/ no
        self.base_dec = '' # yes/ no
        self.detail_acls = [] # CAclDetail
        self.detail_acls.clear()

class CRemoteAgent:
    def __init__(self):
        self.id = ''
        self.agent_type = 'C'
        self.share_protocol = 'NFS'
        self.endpoint = ''
        self.encpolicy = ''
        self.policyPollingPeriod = 30
        self.logSendPollingPeriod = 30
        self.targetPath = ''
        self.description = ''
        self.acls = []
        self.acls.clear()

class XfcRaPolicy:
    def __init__(self):
        self.data = CRemoteAgent()
        self.text_agent_type = ft.Text('에이전트 타입', width=100)
        self.agentType = ft.Dropdown(
            width=280,
            options=[
                ft.dropdown.Option("L", "Local Agent"),
                ft.dropdown.Option("C", "Remote Agent"),
            ],
            value=self.data.agent_type
        )

        self.text_protocol = ft.Text('파일 공유 프로토콜', width=130)
        self.protocol = ft.Dropdown(
            width=250,
            options=[
                ft.dropdown.Option("NFS"),
                ft.dropdown.Option("CIFS"),
            ],
            value="NFS"
        )
        self.endpoint = ft.TextField(label="앤드 포인트", width=316)
        self.encpolicy = ft.TextField(label="암호화 정책", width=316)
        self.policyPollingPeriod = ft.TextField(label="정책 업데이트주기(분)", value="30", width=390)
        self.logSendPollingPeriod = ft.TextField(label="사용 이력전송주기(분)", value="30", width=390)
        self.targetPath = ft.TextField(label="대상경로", multiline=True,  min_lines=3, max_lines=3, width=790)
        self.description = ft.TextField(label="설명", multiline=True, min_lines=3, max_lines=3, width=790)

        self.btn_get_endpoint = ft.ElevatedButton(text="선택", on_click=self.dlg_select_endpoint)
        self.btn_get_policy = ft.ElevatedButton(text="선택", on_click=self.dlg_select_policy)

        self.info_acl = ft.Text("대상 경로 설정 및 경로에 대한 접근제어를 설정하시기 바랍니다.", width=700)


    def clear(self):
        self.agentType.value = "C"
        self.protocol.value = "NFS"
        self.endpoint.value = ""
        self.encpolicy.value = ""
        self.policyPollingPeriod.value = "30"
        self.logSendPollingPeriod.value = "30"
        self.targetPath.value = ""
        self.description.value = ""

    def view(self):
        print(self.agentType.value)
        print(self.protocol.value)
        print(self.endpoint.value)
        print(self.encpolicy.value)
        print(self.policyPollingPeriod.value)
        print(self.logSendPollingPeriod.value)
        print(self.targetPath.value)
        print(self.description.value)

    def button_save(self, e):
        pass

    def new_click(self, e):
        pass

    def dlg_select_endpoint(self, e):
        def close_dlg(e):
            if hasattr(e.control, "text") and e.control.text == "Select":
                self.endpoint.value = ip.value

            dialog.open = False
            e.control.page.update()

        select_button = ft.ElevatedButton(text="Select", on_click=close_dlg)
        cancel_button = ft.ElevatedButton(text="Cancel", on_click=close_dlg)

        def select_on_top(e):
            if 0 < len(e.control.content.value):
                ip.value = e.control.content.value
                e.control.content.page.update()

        header = [ft.DataColumn(ft.Text("앤드 포인트 IP", color="cyan")),
                  ft.DataColumn(ft.Text("설명")),
                  ft.DataColumn(ft.Text("플랫폼")),
                  ]

        low_list = []
        low_list.clear()

        dbms = xdb.XfcDB()

        df = dbms.select_api_list()
        value_list = df.values.tolist()

        for v in value_list:
            low_list.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(v[0], color="cyan"), on_tap=select_on_top),
                        ft.DataCell(ft.Text(v[1])),
                        ft.DataCell(ft.Text(v[2])),
                    ],
                )
            )

        ip = ft.TextField(label="앤드 포인트 아이피", color="cyan")

        dialog = AlertDialog(
            title=Text("Remote Agent 앤드 포인트 선택"),
            content=ft.Column(
                [
                    ft.Row([ip, select_button, cancel_button, ]),
                    ft.DataTable(
                        heading_row_color=ft.colors.BLACK12,
                        columns=header,
                        rows=low_list,
                    )
                ],
                tight=True,
            ),
            # on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        e.page.dialog = dialog
        dialog.open = True
        e.page.update()

    def dlg_select_policy(self, e):
        enc_policy = ft.TextField(label="암호화 정책명", color="cyan")

        def close_dlg(e):
            if hasattr(e.control, "text") and e.control.text == "Select":
                self.encpolicy.value = enc_policy.value

            dialog.open = False
            e.control.page.update()

        select_button = ft.ElevatedButton(text="Select", on_click=close_dlg)
        cancel_button = ft.ElevatedButton(text="Cancel", on_click=close_dlg)

        def select_on_top(e):
            if 0 < len(e.control.content.value):
                enc_policy.value = e.control.content.value
                e.control.content.page.update()

        header = [ft.DataColumn(ft.Text("암호화 정책명", color="cyan")),
                  ft.DataColumn(ft.Text("알고리즘")),
                  ft.DataColumn(ft.Text("키 길이")),
                  ft.DataColumn(ft.Text("설명")),
                  ]

        low_list = []
        low_list.clear()

        dbms = xdb.XfcDB()

        df = dbms.select_enc_policy_list()
        value_list = df.values.tolist()

        for v in value_list:
            low_list.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(v[1], color="cyan"), on_tap=select_on_top),
                        ft.DataCell(ft.Text(v[2])),
                        ft.DataCell(ft.Text(v[3])),
                        ft.DataCell(ft.Text(v[4])),
                    ],
                )
            )

        dialog = AlertDialog(
            title=Text("Remote Agent 앤드 포인트 선택"),
            content=ft.Column(
                [
                    ft.Row([enc_policy, select_button, cancel_button, ]),
                    ft.DataTable(
                        heading_row_color=ft.colors.BLACK12,
                        columns=header,
                        rows=low_list,
                    )
                ],
                tight=True,
            ),
            # on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        e.page.dialog = dialog
        dialog.open = True
        e.page.update()

    def dlg_select_target_path(self, e):
        target_path = ft.TextField(label="경로명", color="cyan", width=740)
        path_list = []
        low_list = []

        path_list.clear()
        low_list.clear()

        def tab_path(e):
            target_path.value = e.control.content.value
            e.control.page.update()

        def add_path(e):
            if len(target_path.value.strip()) == 0:
                return

            if target_path.value not in path_list:
                path_list.append(target_path.value)

                low_list.clear()
                for v in path_list:
                    low_list.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(v), on_tap=tab_path),
                            ],
                        )
                    )

            target_path.value = ''
            e.control.page.update()

        def del_path(e):
            if len(target_path.value.strip()) == 0:
                return

            if target_path.value in path_list:
                path_list.remove(target_path.value)

            low_list.clear()
            for v in path_list:
                low_list.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(v), on_tap=tab_path),
                        ],
                    )
                )
            target_path.value = ''
            e.control.page.update()

        add_btn = ft.ElevatedButton(text="추가", icon=ft.icons.ADD_CARD, on_click=add_path)
        del_btn = ft.ElevatedButton(text="삭제", icon=ft.icons.DELETE_FOREVER_OUTLINED, on_click=del_path)

        path_columns = [ft.DataColumn(ft.Text("경로명", width=400)) ]
        detail_columns = [
            ft.DataColumn(ft.Text("IP 주소")),
            ft.DataColumn(ft.Text("UID")),
            ft.DataColumn(ft.Text("GID")),
            ft.DataColumn(ft.Text("복호화")),
            ft.DataColumn(ft.Text("암호화")),
        ]

        dialog = AlertDialog(
            title=Text("Remote Agent 대상 경로 설정"),
            content=ft.Column(
                [
                    ft.Row([target_path, add_btn, del_btn, ]),
                    ft.Row([
                        ft.DataTable(
                            heading_row_color=ft.colors.BLACK12,
                            columns=path_columns,
                            rows=low_list,
                        ),
                        ft.Column([
                            ft.TextField(label="대상 제외 확장자", color="cyan", width=480),
                            ft.Row([ft.Checkbox(label='복호화'), ft.Checkbox(label='암호화')]),
                            ft.DataTable(
                                columns=detail_columns,
                                rows=[
                                    ft.DataRow(
                                        cells=[
                                            ft.DataCell(ft.Text('127.0.0.1', color="cyan")),
                                            ft.DataCell(ft.Text('1000')),
                                            ft.DataCell(ft.Text('')),
                                            ft.DataCell(ft.Text('O')),
                                            ft.DataCell(ft.Text('O')),
                                        ],
                                    )
                                ]
                            ),
                        ])
                    ])
                ],
                tight=True,
            ),
            # on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        e.page.dialog = dialog
        dialog.open = True
        e.page.update()


    def ra_main(self, page: ft.Page, selected_id=None):
        page.clean()
        btn_save = ft.ElevatedButton(text="저장 하기", icon=ft.icons.SAVE_ALT, on_click=self.button_save)
        btn_new = ft.ElevatedButton(text="새로 만들기", icon=ft.icons.FIBER_NEW_ROUNDED, on_click=self.new_click)

        btn_acl = ft.ElevatedButton(text="설정", on_click=self.dlg_select_target_path)

        page.appbar.title = ft.Text("XFile RA Policy")
        page.add(ft.Row(controls=[btn_save, btn_new]))
        page.add(ft.Row(controls=[self.text_agent_type, self.agentType, self.text_protocol, self.protocol]))
        page.add(ft.Row(controls=[self.endpoint, self.btn_get_endpoint, self.encpolicy, self.btn_get_policy]))
        page.add(ft.Row(controls=[self.policyPollingPeriod, self.logSendPollingPeriod]))
        page.add(ft.Row(controls=[self.info_acl, btn_acl]))
        page.add(ft.Row(controls=[self.targetPath]))
        page.add(ft.Row(controls=[self.description]))

        page.update()
