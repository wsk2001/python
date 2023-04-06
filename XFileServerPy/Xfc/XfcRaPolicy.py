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
import threading
import sqlite3

import json
from datetime import datetime

from flet_core import MainAxisAlignment

# 동일 경로에 있는 파일 import
from . import XfcDB as xdb

import uuid


class CRaACL:
    def __init__(self):
        '''
        id 는 특별한 의미 없음.
        ra_id 와 path 조합이 unique 하면 됨.
        '''
        self.id = ''  # RA 정책 ACL 고유 ID (uuid.uuid())
        self.ra_id = ''  # RA 정책 ID (CRemoteAgent.id)
        self.path = ''  # RA 정책 적용 경로
        self.exclude_exts = ''  # RA 적용 제외 확장자
        self.comm_enc = ''  # RA 정책 적용 경로 공통으로 사용하는 암호화 가능 여부 지정
        self.comm_dec = ''  # RA 정책 적용 경로 공통으로 사용하는 복호화 가능 여부 지정
        self.ip = ''  # 지정 경로에 접근 할 수 있는 IP Address (local 에서 test 시 127.0.0.1 추가 해야 함)
        self.start_ip = ''  # 경로 지정 시작 주소
        self.end_ip = ''  # 경로 지정 마지막 주소
        self.uid = ''  # RA 접근 가능한 UID
        self.gid = ''  # RA 접근 가능한 GID
        self.enc = ''  # 암호화 가능 여부
        self.dec = ''  # 복호화 가능 여부

    def view(self):
        print('[CRaACL]')
        print('id          : ' + self.id)
        print('ra_id       : ' + self.ra_id)
        print('path        : ' + self.path)
        print('exclude_exts: ' + self.exclude_exts)
        print('comm_enc    : ' + self.comm_enc)
        print('comm_dec    : ' + self.comm_dec)
        print('ip          : ' + self.ip)
        print('start_ip    : ' + self.start_ip)
        print('end_ip      : ' + self.end_ip)
        print('uid         : ' + self.uid)
        print('gid         : ' + self.gid)
        print('enc         : ' + self.enc)
        print('dec         : ' + self.dec)


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

    def view(self):
        print('[CRemoteAgent]')
        print('id                  : ' + self.id)
        print('agent_type          : ' + self.agent_type)
        print('share_protocol      : ' + self.share_protocol)
        print('endpoint            : ' + self.endpoint)
        print('encpolicy           : ' + self.encpolicy)
        print('policyPollingPeriod : ' + str(self.policyPollingPeriod))
        print('logSendPollingPeriod: ' + str(self.logSendPollingPeriod))
        print('targetPath          : ' + self.targetPath)
        print('description         : ' + self.description)

class XfcRaPolicy:
    def __init__(self):
        self.data = CRemoteAgent()
        self.dbms = xdb.XfcDB()

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
        self.id = ft.TextField(label="Remote Agent 정책 ID", disabled=True, width=700)
        self.btn_regenid = ft.ElevatedButton(text="생성", on_click=self.regenid, tooltip='ID 를 새로 생성 한다.')
        self.endpoint = ft.TextField(label="앤드 포인트", disabled=True, width=316)
        self.encpolicy = ft.TextField(label="암호화 정책", disabled=True, width=316)
        self.policyPollingPeriod = ft.TextField(label="정책 업데이트주기(분)", value="30", width=390)
        self.logSendPollingPeriod = ft.TextField(label="사용 이력전송주기(분)", value="30", width=390)
        self.targetPath = ft.TextField(label="대상경로", multiline=True, disabled=True, min_lines=3, max_lines=3, width=790)
        self.description = ft.TextField(label="설명", multiline=True, min_lines=3, max_lines=3, width=790)

        self.btn_get_endpoint = ft.ElevatedButton(text="선택", on_click=self.dlg_select_endpoint,
                                                  tooltip='등록된 앤드 포인트를 선택한다.')
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
        flag = False

        dlg_title = ft.Text('')
        dlg_content = ft.Text('')

        def close_dlg(e):
            dlg_modal.open = False
            e.page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=dlg_title,
            content=dlg_content,
            actions=[
                ft.TextButton("확인", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            # on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

        if len(self.id.value.strip()) == 0:
            dlg_title.value = "ID 가 생성되지 않았습니다."
            dlg_content.value = "ID 생성 및 설정 완료 후 저장 하여 주시기 바랍니다."
            flag = True
        elif len(self.endpoint.value.strip()) == 0:
            dlg_title.value = "앤드 포인트 선택 오류"
            dlg_content.value = "앤드 포인트 선택 후 저장 하여 주시기 바랍니다."
            flag = True
        elif len(self.encpolicy.value.strip()) == 0:
            dlg_title.value = "암호화 정책 선택 오류"
            dlg_content.value = "암호화 정책 선택 후 저장 하여 주시기 바랍니다."
            flag = True
        elif len(self.targetPath.value.strip()) == 0:
            dlg_title.value = "대상 경로 설정 요청"
            dlg_content.value = "대상 경로 설정 완료 후 저장 하여 주시기 바랍니다."
            flag = True
        else:
            ra = CRemoteAgent()
            ra.id = self.id.value
            ra.agent_type = self.agentType.value
            ra.share_protocol = self.protocol.value
            ra.endpoint = self.endpoint.value
            ra.encpolicy = self.encpolicy.value
            ra.policyPollingPeriod = self.policyPollingPeriod.value
            ra.logSendPollingPeriod = self.logSendPollingPeriod.value
            ra.targetPath = self.targetPath.value
            ra.description = self.description.value
            print()
            ra.view()
            print()

            self.dbms.delete_ra(ra.id)
            self.dbms.save_ra(ra)

            dlg_title.value = "저장 완료"
            dlg_content.value = "데이터를 저장 하였습니다."
            flag = True
            self.clear()
            self.id.value = ''
            self.have_detail = False

        if flag is True:
            e.page.dialog = dlg_modal
            dlg_modal.open = True
            e.page.update()

    def new_ra(self, e):
        self.clear()
        self.id.value = ''
        self.have_detail = False
        e.page.update()

    def regenid(self, e):
        if (self.have_detail is False) and (0 == len(self.targetPath.value.strip())):
            self.id.value = str(uuid.uuid4())
            e.page.update()

    def dlg_select_endpoint(self, e):
        '''
        앤드포인트 선택
        '''

        def close_dlg(e):
            if hasattr(e.control, "text") and e.control.text == "선택":
                self.endpoint.value = ip.value

            dialog.open = False
            e.control.page.update()

        select_button = ft.ElevatedButton(text="선택", on_click=close_dlg, tooltip='앤드 포인트 선택')
        cancel_button = ft.ElevatedButton(text="취소", on_click=close_dlg, tooltip='취소 후 선택 창 닫기')

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

        df = self.dbms.select_api_list()
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
            modal=True,
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
            if hasattr(e.control, "text") and e.control.text == "선택":
                self.encpolicy.value = enc_policy.value

            dialog.open = False
            e.control.page.update()

        select_button = ft.ElevatedButton(text="선택", on_click=close_dlg, tooltip='API 정책 선택')
        cancel_button = ft.ElevatedButton(text="취소", on_click=close_dlg, tooltip='취소 후 창 닫기')

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

        df = self.dbms.select_enc_policy_list()
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
            modal=True,
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

    # #################################################################################################################
    # 타겟 경로 및 상세 권한 설정
    # #################################################################################################################
    def dlg_set_target_path(self, e):
        '''
        타겟 경로 및 상세 권한 설정
        '''
        target_path = ft.TextField(label="경로명", color="cyan", width=740)
        path_list = []  # path list
        path_widget_list = []  # path widget list
        msg_title = ft.Text('Application Message: ')
        msg_text = ft.Text('', color="red")

        path_list.clear()
        path_widget_list.clear()

        # detail permission list
        dpl = []
        dpl.clear()

        dpl_list = []
        dpl_list.clear()

        if len(self.id.value) <= 0:
            self.id.value = str(uuid.uuid4())

        # 5 초에 한번씩 msg 를 clear 한다.
        def msg_clear():
            if 0 < len(msg_text.value.strip()):
                msg_text.value = ''
                e.page.update()
            threading.Timer(5, msg_clear).start()

        msg_clear()

        def tab_path(e):
            '''
            target path 목록 선택시
            '''
            target_path.value = e.control.content.value
            update_detail_perm(target_path.value)
            e.control.page.update()

        def add_path(e):
            '''
            target path 추가, 중복 추가는 허용하지 않는다.
            '''
            if len(target_path.value.strip()) == 0:
                msg_text.value = '경로명을 입력한 후 추가할 수 있습니다.'
                e.control.page.update()
                return

            if target_path.value not in path_list:
                path_list.append(target_path.value)

                path_widget_list.clear()
                for v in path_list:
                    path_widget_list.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(v), on_tap=tab_path),
                            ],
                        )
                    )

                dt_exclude.value = ''
                dt_comm_dec.value = False
                dt_comm_enc.value = False

                reset_input(e)
                target_path.value = ''
                e.control.page.update()

        def del_path(e):
            '''
            선택된 target path 삭제
            '''
            if len(target_path.value.strip()) == 0:
                msg_text.value = '경로명을 입력한 후 삭제할 수 있습니다.'
                e.control.page.update()
                return

            if target_path.value in path_list:
                path_list.remove(target_path.value)

            path_widget_list.clear()
            for v in path_list:
                path_widget_list.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(v), on_tap=tab_path),
                        ],
                    )
                )
            target_path.value = ''
            e.control.page.update()

        btn_add_path = ft.ElevatedButton(text="추가", icon=ft.icons.ADD_CARD,
                                         on_click=add_path,
                                         tooltip='암/복호화 할 경로를 추가 합니다.')
        btn_del_path = ft.ElevatedButton(text="삭제", icon=ft.icons.DELETE_FOREVER_OUTLINED,
                                         on_click=del_path,
                                         tooltip='등록된 경로를 삭제 한다.\n' + \
                                                 '주의 상세 경로 설정 정보도 같이 삭제됨')

        path_columns = [ft.DataColumn(ft.Text("경로명", width=400))]
        detail_columns = [
            ft.DataColumn(ft.Text("IP 주소")),
            ft.DataColumn(ft.Text("UID")),
            ft.DataColumn(ft.Text("GID")),
            ft.DataColumn(ft.Text("복호화")),
            ft.DataColumn(ft.Text("암호화")),
        ]

        dt_exclude = ft.TextField(label="대상 제외 확장자", width=500)
        dt_comm_dec = ft.Checkbox(label='복호화')
        dt_comm_enc = ft.Checkbox(label='암호화')

        dt_ip = ft.TextField(label="IP 주소", width=320)
        dt_uid = ft.TextField(label="UID", width=80)
        dt_gid = ft.TextField(label="GID", width=80)
        dt_dec = ft.Checkbox(label='복호화')
        dt_enc = ft.Checkbox(label='암호화')

        def tab_ip(e):
            dt_ip.value = e.control.content.value
            for l in dpl:
                if l[4] == dt_ip.value:
                    dt_uid.value = l[5]
                    dt_gid.value = l[6]
                    dt_dec.value = True if l[7] == 'O' else False
                    dt_enc.value = True if l[8] == 'O' else False
                    break

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
                            ft.DataCell(ft.Text(l[4], color="cyan"), on_tap=tab_ip),
                            ft.DataCell(ft.Text(l[5])),
                            ft.DataCell(ft.Text(l[6])),
                            ft.DataCell(ft.Text(l[7])),
                            ft.DataCell(ft.Text(l[8])),
                        ]))

        def save_target_path(e):
            '''
            상세 설정 정보 저장
            '''
            self.have_detail = True
            first = True
            for path in path_list:
                if first:
                    self.targetPath.value = path
                    first = False
                else:
                    self.targetPath.value = self.targetPath.value + '\n' + path

            tmp_path = ''
            for d in dpl:
                acl = CRaACL()
                acl.id = str(uuid.uuid4())
                acl.ra_id = self.id.value
                acl.path = d[0]
                acl.exclude_exts = d[1]
                acl.comm_dec = d[2]
                acl.comm_enc = d[3]
                if ('~' in d[4]) or ('-' in d[4]):
                    if '~' in d[4]:
                        rip = str(d[4]).split('~')
                    elif '-' in d[4]:
                        rip = str(d[4]).split('-')

                    acl.start_ip = rip[0].strip()
                    acl.end_ip = rip[1].strip()
                else:
                    acl.ip = d[4]

                acl.uid = d[5]
                acl.gid = d[6]
                acl.dec = d[7]
                acl.enc = d[8]

                print()
                acl.view()
                print()

                if tmp_path != acl.path:
                    tmp_path = acl.path
                    self.dbms.delete_acl(acl.ra_id, tmp_path)
                self.dbms.save_acl(acl)

            msg_text.value = 'Data 를 정상 저장 하였습니다.'
            e.page.update()

        def close_target_path(e):
            e.page.dialog.open = False
            e.page.update()

        info = ft.Text('수정된 내용 전체를 저장 하려면 저장 버튼을 누르고, 수정된 내용을 무시 하려면 닫기 버튼을 누르세요. ', width=720)
        btn_save_target_path = ft.ElevatedButton(text="저장", icon=ft.icons.ADD_CARD, on_click=save_target_path)
        btn_close_target_path = ft.ElevatedButton(text="닫기", icon=ft.icons.DELETE, on_click=close_target_path)

        def reset_input(e):
            dt_ip.value = ''
            dt_uid.value = ''
            dt_gid.value = ''
            dt_enc.value = False
            dt_dec.value = False
            e.page.update()

        def append_detail_perm(e):
            '''
            입력된 상세 항목 list 에 추가
            '''
            if 0 < len(dt_ip.value.strip()) and 0 < len(target_path.value.strip()):
                dpl.append([target_path.value,
                            dt_exclude.value,
                            'O' if dt_comm_dec.value is True else '',
                            'O' if dt_comm_enc.value is True else '',
                            dt_ip.value, dt_uid.value, dt_gid.value,
                            'O' if dt_dec.value is True else '',
                            'O' if dt_enc.value is True else '',
                            ])
                update_detail_perm()
                e.control.page.update()
            else:
                msg_text.value = '경로명과 IP 주소를 입력한 후 추가할 수 있습니다.'
                e.control.page.update()

        def delete_detail_perm(e):
            '''
            선택된 경로를 삭제 한다.
            '''
            if 0 < len(dt_ip.value.strip()) and 0 < len(target_path.value.strip()):
                tlist = copy.deepcopy(dpl)
                dpl.clear()
                for t in tlist:
                    if t[0] == target_path.value and t[4] == dt_ip.value:
                        continue
                    dpl.append([t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8]])

                update_detail_perm()
                reset_input(e)
                e.control.page.update()
            else:
                msg_text.value = '경로명과 IP 주소를 선택한 후 삭제할 수 있습니다.'
                e.control.page.update()

        add_detail_btn = ft.ElevatedButton(text="추가", icon=ft.icons.ADD_CARD, on_click=append_detail_perm)
        delete_detail_btn = ft.ElevatedButton(text="삭제", icon=ft.icons.DELETE, on_click=delete_detail_perm)
        reset_detail_btn = ft.ElevatedButton(text="초기화", icon=ft.icons.RESTART_ALT, on_click=reset_input)

        dialog = AlertDialog(
            modal=True,
            title=Text("Remote Agent 대상 경로 및 권한 설정", width=940),
            content=ft.Column(
                [
                    ft.Row([target_path, btn_add_path, btn_del_path, ]),
                    ft.Divider(),  # ======================================
                    ft.Row([
                        ft.Column([
                            ft.DataTable(
                                heading_row_color=ft.colors.BLACK12,
                                columns=path_columns,
                                rows=path_widget_list,
                                width=420,
                                height=360  # 이것 빼면 중간에 나타남.
                            ),
                        ]),
                        ft.Column([
                            dt_exclude,
                            ft.Row([dt_comm_dec, dt_comm_enc]),
                            ft.Divider(),
                            ft.Row([dt_ip, dt_uid, dt_gid]),
                            ft.Row([dt_dec, dt_enc, add_detail_btn, delete_detail_btn, reset_detail_btn]),
                            ft.Divider(),
                            ft.DataTable(columns=detail_columns, rows=dpl_list, ),
                        ])
                    ]),
                    ft.Divider(),  # ======================================
                    ft.Row([info, btn_save_target_path, btn_close_target_path]),
                    ft.Divider(),  # ======================================
                    ft.Row([msg_title, msg_text]),
                ],
                tight=True
            ),
            # on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        e.page.dialog = dialog
        dialog.open = True
        e.page.update()

    def ra_main(self, page: ft.Page, ra_id=None):
        page.clean()
        btn_save = ft.ElevatedButton(text="저장 하기", icon=ft.icons.SAVE_ALT, on_click=self.save_ra,
                                     tooltip='설정된 RA 정보를 저장 한다.')
        btn_new = ft.ElevatedButton(text="새로 만들기", icon=ft.icons.FIBER_NEW_ROUNDED, on_click=self.new_ra,
                                    tooltip='RA 설정을 초기화 한다.')
        btn_acl = ft.ElevatedButton(text="설정", on_click=self.dlg_set_target_path, tooltip='Remote Agent 대상 경로 및 권한 설정')

        page.add(ft.Row(controls=[self.id, self.btn_regenid]))
        page.add(ft.Row(controls=[btn_save, btn_new]))
        page.add(ft.Row(controls=[self.text_agent_type, self.agentType, self.text_protocol, self.protocol]))
        page.add(ft.Row(controls=[self.endpoint, self.btn_get_endpoint, self.encpolicy, self.btn_get_policy]))
        page.add(ft.Row(controls=[self.policyPollingPeriod, self.logSendPollingPeriod]))
        page.add(ft.Row(controls=[self.info_acl, btn_acl]))
        page.add(ft.Row(controls=[self.targetPath]))
        page.add(ft.Row(controls=[self.description]))

        if ra_id is not None:
            df = self.dbms.list_ra_policy(ra_id)
            value_list = df.values.tolist()
            for v in value_list:
                self.id.value = v[0]
                self.agentType.value = v[1]
                self.protocol.value = v[2]
                self.endpoint.value = v[3]
                self.encpolicy.value = v[4]
                self.policyPollingPeriod.value = v[5]
                self.logSendPollingPeriod.value = v[6]
                self.targetPath.value = v[7]
                self.description.value = v[8]
                break

        page.update()
