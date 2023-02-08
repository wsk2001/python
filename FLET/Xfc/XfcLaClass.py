# -*- coding: utf-8 -*-

import flet as ft
import json
from datetime import datetime


class XfcLaPolicy:
    def use_filter_checkbox_changed(self, e):
        if e.control.value:
            self.file_filter_type.visible = True
            self.file_filter_exts.visible = True

        else:
            self.file_filter_type.visible = False
            self.file_filter_exts.visible = False

        self.file_filter_type.update()
        self.file_filter_exts.update()

    def use_trigger_checkbox_changed(self, e):
        if e.control.value:
            self.trigger_ext.visible = True
            self.trigger_target.visible = True

        else:
            self.trigger_ext.visible = False
            self.trigger_target.visible = False

        self.trigger_ext.update()
        self.trigger_target.update()

    def use_backup_checkbox_changed(self, e):
        if e.control.value:
            self.backup_path.visible = True

        else:
            self.backup_path.visible = False

        self.backup_path.update()

    def __init__(self):
        hi = 60
        self.ip = ft.TextField(label="IP 주소", height=hi, color="white")
        self.policy = ft.TextField(label="정책 이름", height=hi, color="white")
        self.description = ft.TextField(label="설명", height=hi,  width=610, color="white")
        self.base_path = ft.TextField(label="파일 감시 기본 경로", height=hi, color="white")
        self.dir = ft.TextField(label="파일 감시 경로", height=hi)
        self.mode = ft.RadioGroup(content=ft.Row([
                                    ft.Radio(value="E", label="암호화", width=150),
                                    ft.Radio(value="D", label="복호화", width=150)]), value="E")

        self.time_limit = ft.TextField(label="최대 작업 시간", height=hi)
        self.check_file_closed = ft.Checkbox(label="파일 닫힘 검사", value=True, height=hi)
        self.use_file_filter = ft.Checkbox(label="파일 확장자 필터 사용", width=300, value=False, height=hi, on_change=self.use_filter_checkbox_changed)
        self.file_filter_type = ft.Dropdown(
            width=300,
            label="파일 필터 타입",
            options=[
                ft.dropdown.Option("I (필터 타입 포함)"),
                ft.dropdown.Option("E (필터 타입 제외)"),
            ],
            visible=False,
        )
        self.file_filter_exts = ft.TextField(label="파일 필터 확장자", width=610, height=hi, visible=False)
        self.check_cycle = ft.TextField(label="파일 변화(생성) 검사 주기(sec)", height=hi)
        self.thread_count = ft.TextField(label="작업 Thread 개 수", height=hi, visible=True)
        self.use_backup = ft.Checkbox(label="파일 암호화 전 백업", width=300, value=True, height=hi, on_change=self.use_backup_checkbox_changed)
        self.backup_path = ft.TextField(label="파일 백업 경로", width=915, height=hi)
        self.temp_path = ft.TextField(label="작업 임시 경로")
        self.dir_depth = ft.TextField(label="디렉토리 탐색 깊이", height=hi)
        self.dir_format = ft.TextField(label="디렉토리 포멧", height=hi)
        self.ymd_offset = ft.TextField(label="이전 일자 옵셋", height=hi)

        self.use_trigger_file = ft.Checkbox(label="트리거 확장자 사용 여부", value=False,  width=300, height=hi, on_change=self.use_trigger_checkbox_changed)
        self.trigger_ext = ft.TextField(label="트리거 파일 확장자", height=hi, visible=False)
        self.trigger_target = ft.TextField(label="트리거 목적 파일 확장자", height=hi, visible=False)

    def clear(self):
        self.ip.value = ""
        self.policy.value = ""
        self.description.value = ""
        self.base_path.value = ""
        self.dir.value = ""
        self.mode.value = "E"
        self.time_limit.value = ""
        self.check_file_closed.value = True
        self.use_file_filter.value = None
        self.file_filter_type.value = ""
        self.file_filter_exts.value = ""
        self.check_cycle.value = ""
        self.thread_count.value = ""
        self.use_backup.value = True
        self.backup_path.value = ""
        self.temp_path.value = ""
        self.dir_depth.value = ""
        self.dir_format.value = ""
        self.ymd_offset.value = ""
        self.use_trigger_file.value = False
        self.trigger_ext.value = ""
        self.trigger_target.value = ""

    def view(self):
        print(self.ip.value)
        print(self.policy.value)
        print(self.description.value)
        print(self.base_path.value)
        print(self.dir.value)
        print(self.mode.value)
        print(self.time_limit.value)
        print(self.check_file_closed.value)
        print(self.use_file_filter.value)
        print(self.file_filter_type.value)
        print(self.file_filter_exts.value)
        print(self.check_cycle.value)
        print(self.thread_count.value)
        print(self.use_backup.value)
        print(self.backup_path.value)
        print(self.temp_path.value)
        print(self.dir_depth.value)
        print(self.dir_format.value)
        print(self.ymd_offset.value)
        print(self.use_trigger_file.value)
        print(self.trigger_ext.value)
        print(self.trigger_target.value)

