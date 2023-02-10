# -*- coding: utf-8 -*-

import flet as ft
import json
from datetime import datetime


class XfcSaPolicy:
    num_list = [
        "00", "01", "02", "03", "04", "05", "06", "07", "08", "09",
        "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
        "20", "21", "22", "23", "24", "25", "26", "27", "28", "29",
        "30", "31", "32", "33", "34", "35", "36", "37", "38", "39",
        "40", "41", "42", "43", "44", "45", "46", "47", "48", "49",
        "50", "51", "52", "53", "54", "55", "56", "57", "58", "59",
    ]

    def use_weekday_checkbox_changed(self, e):
        if self.use_weekday.value:
            self.sun.visible = True
            self.mon.visible = True
            self.tue.visible = True
            self.wed.visible = True
            self.thu.visible = True
            self.fri.visible = True
            self.sat.visible = True

        else:
            self.sun.visible = False
            self.mon.visible = False
            self.tue.visible = False
            self.wed.visible = False
            self.thu.visible = False
            self.fri.visible = False
            self.sat.visible = False

        self.sun.update()
        self.mon.update()
        self.tue.update()
        self.wed.update()
        self.thu.update()
        self.fri.update()
        self.sat.update()

    def use_filter_checkbox_changed(self, e):
        if e.control.value:
            self.file_filter_type.visible = True
            self.file_filter_exts.visible = True

        else:
            self.file_filter_type.visible = False
            self.file_filter_exts.visible = False

        self.file_filter_type.update()
        self.file_filter_exts.update()

    def use_backup_checkbox_changed(self, e):
        if e.control.value:
            self.backup_path.visible = True

        else:
            self.backup_path.visible = False

        self.backup_path.update()

    def __init__(self):
        self.ip = ft.TextField(label="IP 주소")
        self.policy = ft.TextField(label="정책 이름")
        self.description = ft.TextField(label="설명", width=610)

        self.file_path = ft.TextField(label="파일 암/복호화 대상 경로", width=1230)

        self.mode = ft.RadioGroup(content=ft.Row([
            ft.Radio(value="E", label="암호화", width=150),
            ft.Radio(value="D", label="복호화", width=150)]), value="E")
        self.time_limit = ft.TextField(label="최대 작업 시간")

        self.repeat = ft.Checkbox(label="주기별 반복 작업", value=True)

        self.dir_depth = ft.TextField(label="디렉토리 탐색 깊이")
        self.dir_format = ft.TextField(label="디렉토리 포멧")
        self.ymd_offset = ft.TextField(label="날짜 포멧의 일자 옵셋")

        self.use_weekday = ft.Checkbox(label="요일 구분 사용", width=300,
                                       on_change=self.use_weekday_checkbox_changed)
        self.weekdays = ft.TextField(label="작업 요일 선택", visible=False)
        self.sun = ft.Checkbox(label="일요일", width=100, visible=False)
        self.mon = ft.Checkbox(label="월요일", width=100, visible=False)
        self.tue = ft.Checkbox(label="화요일", width=100, visible=False)
        self.wed = ft.Checkbox(label="수요일", width=100, visible=False)
        self.thu = ft.Checkbox(label="목요일", width=100, visible=False)
        self.fri = ft.Checkbox(label="금요일", width=100, visible=False)
        self.sat = ft.Checkbox(label="토요일", width=100, visible=False)

        lst_days = []
        lst_days.clear()
        for i in range(0, 32):
            lst_days.append(ft.dropdown.Option(self.num_list[i]))

        lst_hhs = []
        lst_hhs.clear()
        for i in range(0, 24):
            lst_hhs.append(ft.dropdown.Option(self.num_list[i]))

        lst_mms = []
        lst_mms.clear()
        for i in range(0, 60):
            lst_mms.append(ft.dropdown.Option(self.num_list[i]))

        self.day = ft.Dropdown(
            width=300,
            label="일자",
            options=lst_days,
        )
        self.hh = ft.Dropdown(
            width=300,
            label="시간",
            options=lst_hhs,
        )
        self.mm = ft.Dropdown(
            width=300,
            label="분",
            options=lst_mms,
        )
        self.ss = ft.Dropdown(
            width=300,
            label="초",
            options=lst_mms,
        )

        self.use_file_filter = ft.Checkbox(label="파일 확장자 필터 사용", width=300, value=False,
                                           on_change=self.use_filter_checkbox_changed)
        self.file_filter_type = ft.Dropdown(
            width=300,
            label="파일 필터 타입",
            options=[
                ft.dropdown.Option("I (필터 타입 포함)"),
                ft.dropdown.Option("E (필터 타입 제외)"),
            ],
            visible=False,
        )
        self.file_filter_exts = ft.TextField(label="파일 필터 확장자", width=610, visible=False)

        self.check_file_closed = ft.Checkbox(label="파일 닫힘 검사", value=True, width=300)
        self.thread_count = ft.TextField(label="작업 Thread 개 수")

        self.use_backup = ft.Checkbox(label="파일 암호화 전 백업", width=300, value=True,
                                      on_change=self.use_backup_checkbox_changed)
        self.backup_path = ft.TextField(label="파일 백업 경로", width=920)

        self.temp_path = ft.TextField(label="작업 임시 경로", width=1230)
        self.check_cycle = ft.TextField(label="작업 시간 도달 검사 주기(sec)")

    def clear(self):
        self.ip.value = ""
        self.policy.value = ""
        self.description.value = ""
        self.file_path.value = ""
        self.mode.value = ""
        self.time_limit.value = ""
        self.repeat.value = True
        self.dir_format.value = ""
        self.ymd_offset.value = ""
        self.dir_depth.value = ""
        self.use_weekday.value = False
        self.weekdays.value = ""
        self.day.value = "00"
        self.hh.value = "00"
        self.mm.value = "00"
        self.ss.value = "00"
        self.use_file_filter.value = False
        self.file_filter_type.value = ""
        self.file_filter_exts.value = ""
        self.check_file_closed.value = True
        self.thread_count.value = ""
        self.use_backup.value = True
        self.backup_path.value = ""
        self.temp_path.value = ""
        self.check_cycle.value = ""

        self.mon.visible = False
        self.tue.visible = False
        self.wed.visible = False
        self.thu.visible = False
        self.fri.visible = False
        self.sat.visible = False
        self.sun.visible = False

    def view(self):
        print(self.ip.value)
        print(self.policy.value)
        print(self.description.value)
        print(self.file_path.value)
        print(self.mode.value)
        print(self.time_limit.value)
        print(self.repeat.value)
        print(self.dir_format.value)
        print(self.ymd_offset.value)
        print(self.dir_depth.value)
        print(self.use_weekday.value)
        print(self.weekdays.value)
        print(self.day.value)
        print(self.hh.value)
        print(self.mm.value)
        print(self.ss.value)
        print(self.use_file_filter.value)
        print(self.file_filter_type.value)
        print(self.file_filter_exts.value)
        print(self.check_file_closed.value)
        print(self.thread_count.value)
        print(self.use_backup.value)
        print(self.backup_path.value)
        print(self.temp_path.value)
        print(self.check_cycle.value)
