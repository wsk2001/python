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


class XfcRaPolicy:
    def __init__(self):
        self.text_agent_type = ft.Text('에이전트 타입', width=100)
        self.agentType = ft.Dropdown(
            width=280,
            options=[
                ft.dropdown.Option("L", "Local Agent"),
                ft.dropdown.Option("C", "Remote Agent"),
            ],
            value="C"
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
                  ft.DataColumn(ft.Text("설명", width=240))]

        low_list = []
        low_list.clear()

        low_list.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("192.168.60.190", color="cyan"), on_tap=select_on_top),
                    ft.DataCell(ft.Text("desktop")),
                ],
            )
        )

        low_list.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("192.168.60.211", color="cyan"), on_tap=select_on_top),
                    ft.DataCell(ft.Text("notebook")),
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
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
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

        low_list.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("AES-128", color="cyan"), on_tap=select_on_top),
                    ft.DataCell(ft.Text("ASE")),
                    ft.DataCell(ft.Text("128")),
                    ft.DataCell(ft.Text("AES-128")),
                ],
            )
        )

        low_list.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("AES-256", color="cyan"), on_tap=select_on_top),
                    ft.DataCell(ft.Text("ASE")),
                    ft.DataCell(ft.Text("256")),
                    ft.DataCell(ft.Text("AES-256")),
                ],
            )
        )

        low_list.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("ARIA-256", color="cyan"), on_tap=select_on_top),
                    ft.DataCell(ft.Text("ARIA")),
                    ft.DataCell(ft.Text("256")),
                    ft.DataCell(ft.Text("ARIA-256")),
                ],
            )
        )

        low_list.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("RA", color="cyan"), on_tap=select_on_top),
                    ft.DataCell(ft.Text("AES")),
                    ft.DataCell(ft.Text("256")),
                    ft.DataCell(ft.Text("AES-256")),
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
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        e.page.dialog = dialog
        dialog.open = True
        e.page.update()

    def ra_main(self, page: ft.Page, selected_id=None):
        page.clean()
        btn_save = ft.ElevatedButton(text="저장 하기", icon=ft.icons.SAVE_ALT, on_click=self.button_save)
        btn_new = ft.ElevatedButton(text="새로 만들기", icon=ft.icons.FIBER_NEW_ROUNDED, on_click=self.new_click)

        btn_acl = ft.ElevatedButton(text="설정", on_click=self.new_click)

        page.appbar.title = ft.Text("XFile RA Policy")
        page.add(ft.Row(controls=[btn_save, btn_new]))
        page.add(ft.Row(controls=[self.text_agent_type, self.agentType, self.text_protocol, self.protocol]))
        page.add(ft.Row(controls=[self.endpoint, self.btn_get_endpoint, self.encpolicy, self.btn_get_policy]))
        page.add(ft.Row(controls=[self.policyPollingPeriod, self.logSendPollingPeriod]))
        page.add(ft.Row(controls=[self.info_acl, btn_acl]))
        page.add(ft.Row(controls=[self.targetPath]))
        page.add(ft.Row(controls=[self.description]))

        page.update()
