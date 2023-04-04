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
import copy
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
        self.enc = ''  # yes/ no
        self.dec = ''  # yes/ no


class CAcl:
    def __init__(self):
        self.id = ''
        self.ra_id = ''
        self.path = ''
        self.exclude_exts = ''
        self.base_enc = ''  # yes/ no
        self.base_dec = ''  # yes/ no
        self.detail_acls = []  # CAclDetail
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
        self.id = ft.TextField(label="Remote Agent ID", disabled=True, width=700)
        self.btn_regenid = ft.ElevatedButton(text="생성", on_click=self.regenid, tooltip='ID 를 새로 생성 한다.')
        self.endpoint = ft.TextField(label="앤드 포인트", width=316)
        self.encpolicy = ft.TextField(label="암호화 정책", width=316)
        self.policyPollingPeriod = ft.TextField(label="정책 업데이트주기(분)", value="30", width=390)
        self.logSendPollingPeriod = ft.TextField(label="사용 이력전송주기(분)", value="30", width=390)
        self.targetPath = ft.TextField(label="대상경로", multiline=True, disabled=True, min_lines=3, max_lines=3, width=790)
        self.description = ft.TextField(label="설명", multiline=True, min_lines=3, max_lines=3, width=790)

        self.btn_get_endpoint = ft.ElevatedButton(text="선택", on_click=self.dlg_select_endpoint, tooltip='등록된 앤드 포인트를 선택한다.')
        self.btn_get_policy = ft.ElevatedButton(text="선택", on_click=self.dlg_select_policy, tooltip='등록된 API 정책을 선택한다.')

        self.info_acl = ft.Text("대상 경로 설정 및 경로에 대한 접근제어를 설정하시기 바랍니다.", width=700)
        self.have_detail = False

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

    def save_ra(self, e):
        pass

    def new_ra(self, e):
        self.clear()
        self.id.value = ''
        self.have_detail = False
        e.page.update()

    def regenid(self, e):
        if self.have_detail == False:
            self.id.value = str(uuid.uuid4())
            e.page.update()

    def dlg_select_endpoint(self, e):
        '''
        앤드포인트 선택
        '''
        def close_dlg(e):
            if hasattr(e.control, "text") and e.control.text == "Select":
                self.endpoint.value = ip.value

            dialog.open = False
            e.control.page.update()

        select_button = ft.ElevatedButton(text="Select", on_click=close_dlg, tooltip='앤드 포인트 선택')
        cancel_button = ft.ElevatedButton(text="Cancel", on_click=close_dlg, tooltip='취소 후 선택 창 닫기')

        def select_on_top(e):
            if 0 < len(e.control.content.value):
                ip.value = e.control.content.value
                e.control.content.page.update()

        header = [ft.DataColumn(ft.Text("앤드 포인트 IP", color="cyan")),
                  ft.DataColumn(ft.Text("설명")),
                  ft.DataColumn(ft.Text("플랫폼")),
                  ]

        row_list = []
        row_list.clear()

        dbms = xdb.XfcDB()

        df = dbms.select_api_list()
        value_list = df.values.tolist()

        for v in value_list:
            row_list.append(
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
                        rows=row_list,
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
        '''
        API 암호화 정책 선택
        '''
        enc_policy = ft.TextField(label="암호화 정책명", color="cyan")

        def close_dlg(e):
            if hasattr(e.control, "text") and e.control.text == "Select":
                self.encpolicy.value = enc_policy.value

            dialog.open = False
            e.control.page.update()

        select_button = ft.ElevatedButton(text="Select", on_click=close_dlg, tooltip='API 정책 선택')
        cancel_button = ft.ElevatedButton(text="Cancel", on_click=close_dlg, tooltip='취소 후 창 닫기')

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

    def dlg_set_target_path(self, e):
        '''
        타겟 경로 및 상세 권한 설정
        '''
        target_path = ft.TextField(label="경로명", color="cyan", width=740)
        path_list = []
        low_list = []

        path_list.clear()
        low_list.clear()

        if len(self.id.value) <= 0:
            self.id.value = str(uuid.uuid4())

        def tab_path(e):
            target_path.value = e.control.content.value
            update_detail_perm(target_path.value)
            e.control.page.update()

        def add_path(e):
            if len(target_path.value.strip()) == 0:
                msg_text.value = '경로명 을 입력 하여야 합니다.'
                e.control.page.update()
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

        add_btn = ft.ElevatedButton(text="추가", icon=ft.icons.ADD_CARD,
                                    on_click=add_path,
                                    tooltip='암/복호화 할 경로를 추가 합니다.')
        del_btn = ft.ElevatedButton(text="삭제", icon=ft.icons.DELETE_FOREVER_OUTLINED,
                                    on_click=del_path,
                                    tooltip='등록된 경로를 삭제 한다.\n' +\
                                    '주의 상세 경로 설정 정보도 같이 삭제됨')

        path_columns = [ft.DataColumn(ft.Text("경로명", width=400))]
        detail_columns = [
            ft.DataColumn(ft.Text("IP 주소")),
            ft.DataColumn(ft.Text("UID")),
            ft.DataColumn(ft.Text("GID")),
            ft.DataColumn(ft.Text("복호화")),
            ft.DataColumn(ft.Text("암호화")),
        ]

        dt_ip = ft.TextField(label="IP 주소", width=240)
        dt_uid = ft.TextField(label="UID", width=120)
        dt_gid = ft.TextField(label="GID", width=120)
        dt_dec = ft.Checkbox(label='복호화')
        dt_enc = ft.Checkbox(label='암호화')

        # detail permission list
        dpl = []
        dpl.clear()

        dpl_list = []
        dpl_list.clear()

        def tab_ip(e):
            dt_ip.value = e.control.content.value
            e.control.page.update()

        def update_detail_perm(tp=None):
            '''
            tp: target path, 외부에서 지정 한 경우, 지정 값과 list 의 첫번째 값 비교
            그렇지 않은 경우 target_path.value 와 list 의 첫번째 값 비교 하여 표시 목록을 만든다.
            '''
            dpl_list.clear()

            for l in dpl:
                app_flag = False
                if tp is None and l[0] == target_path.value:
                    app_flag = True
                elif tp is not None and l[0] == tp:
                    app_flag = True

                if app_flag:
                    dpl_list.append(ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(l[1], color="cyan"), on_tap=tab_ip),
                            ft.DataCell(ft.Text(l[2])),
                            ft.DataCell(ft.Text(l[3])),
                            ft.DataCell(ft.Text(l[4])),
                            ft.DataCell(ft.Text(l[5])),
                        ]))

        def save_target_path(e):
            self.have_detail = True
            first = True
            for path in path_list:
                if first:
                    self.targetPath.value = path
                    first = False
                else:
                    self.targetPath.value = self.targetPath.value + '\n' + path
            e.page.update()

        def close_target_path(e):
            e.page.dialog.open = False
            e.page.update()

        def reset_input(e):
            dt_ip.value = ''
            dt_uid.value = ''
            dt_gid.value = ''
            dt_enc.value = False
            dt_dec.value = False
            e.page.update()

        info = ft.Text('수정된 내용 전체를 저장 하려면 저장 버튼을 누르고, 수정된 내용을 무시 하려면 닫기 버튼을 누르세요. ', width=750)
        btn_save_target_path = ft.ElevatedButton(text="저장", icon=ft.icons.ADD_CARD, on_click=save_target_path)
        btn_close_target_path = ft.ElevatedButton(text="닫기", icon=ft.icons.DELETE, on_click=close_target_path)
        msg_title = ft.Text('Application Message: ')
        msg_text = ft.Text('')

        def append_detail_perm(e):
            '''
            입력된 상세 항목 list 에 추가
            '''
            if 0 < len(target_path.value.strip()):
                dpl.append([target_path.value, dt_ip.value, dt_uid.value, dt_gid.value,
                            'O' if dt_enc.value is True else '',
                            'O' if dt_dec.value is True else '',
                            ])
                update_detail_perm()
                e.control.page.update()

        def delete_detail_perm(e):
            tlist = copy.deepcopy(dpl)
            dpl.clear()
            for t in tlist:
                if t[0] == target_path.value and t[1] == dt_ip.value:
                    continue
                dpl.append([t[0], t[1], t[2], t[3], t[4], t[5]])

            update_detail_perm()
            e.control.page.update()

        add_detail_btn = ft.ElevatedButton(text="추가", icon=ft.icons.ADD_CARD, on_click=append_detail_perm)
        delete_detail_btn = ft.ElevatedButton(text="삭제", icon=ft.icons.DELETE, on_click=delete_detail_perm)
        reset_detail_btn = ft.ElevatedButton(text="입력 초기화", icon=ft.icons.REMOVE_CIRCLE, on_click=reset_input)

        dialog = AlertDialog(
            title=Text("Remote Agent 대상 경로 및 권한 설정", width=960),
            content=ft.Column(
                [
                    ft.Row([target_path, add_btn, del_btn, ]),
                    ft.Divider(),  # ======================================
                    ft.Row([
                        ft.Column([
                            ft.DataTable(
                                heading_row_color=ft.colors.BLACK12,
                                columns=path_columns,
                                rows=low_list,
                                width=420
                            ),
                        ], alignment=MainAxisAlignment.END),
                        # ft.VerticalDivider(),
                        ft.Column([
                            ft.TextField(label="대상 제외 확장자", color="green", width=480),
                            ft.Row([ft.Checkbox(label='복호화'), ft.Checkbox(label='암호화')]),
                            ft.Divider(),
                            ft.Row([dt_ip, dt_uid, dt_gid]),
                            ft.Row([dt_enc, dt_dec, add_detail_btn, delete_detail_btn, reset_detail_btn]),
                            ft.Divider(),
                            ft.DataTable(columns=detail_columns, rows=dpl_list, ),
                        ])
                    ]),
                    ft.Divider(),  # ======================================
                    ft.Row([info, btn_save_target_path, btn_close_target_path]),
                    ft.Divider(),  # ======================================
                    ft.Row([msg_title, msg_text]),
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
        btn_save = ft.ElevatedButton(text="저장 하기", icon=ft.icons.SAVE_ALT, on_click=self.save_ra, tooltip='설정된 RA 정보를 저장 한다.')
        btn_new = ft.ElevatedButton(text="새로 만들기", icon=ft.icons.FIBER_NEW_ROUNDED, on_click=self.new_ra, tooltip='RA 설정을 초기화 한다.')
        btn_acl = ft.ElevatedButton(text="설정", on_click=self.dlg_set_target_path, tooltip='Remote Agent 대상 경로 및 권한 설정')

        page.appbar.title = ft.Text("XFile RA Policy")
        page.add(ft.Row(controls=[self.id, self.btn_regenid]))
        page.add(ft.Row(controls=[btn_save, btn_new]))
        page.add(ft.Row(controls=[self.text_agent_type, self.agentType, self.text_protocol, self.protocol]))
        page.add(ft.Row(controls=[self.endpoint, self.btn_get_endpoint, self.encpolicy, self.btn_get_policy]))
        page.add(ft.Row(controls=[self.policyPollingPeriod, self.logSendPollingPeriod]))
        page.add(ft.Row(controls=[self.info_acl, btn_acl]))
        page.add(ft.Row(controls=[self.targetPath]))
        page.add(ft.Row(controls=[self.description]))

        page.update()
