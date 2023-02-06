# -*- coding: utf-8 -*-

import flet as ft
import json
from datetime import datetime


class XfcSaPolicy:
    def __init__(self):
        hi = 60

        self.ip = ft.TextField(label="IP 주소", height=hi, color="red")
        self.policy = ft.TextField(label="정책 이름", height=hi, color="red")
        self.description = ft.TextField(label="설명", height=hi,  width=610, color="red")

        self.file_path = ft.TextField(label="파일 암/복호화 대상 경로", height=hi, color="red")
        self.mode = ft.TextField(label="암(E)/복(D)호화 모드", height=hi)
        self.time_limit = ft.TextField(label="최대 작업 시간(msec)", height=hi)
        self.repeat = ft.TextField(label="주기별 반복 작업 여부", height=hi)
        self.dir_format = ft.TextField(label="디렉토리 포멧", height=hi)
        self.ymd_offset = ft.TextField(label="이전 일자 옵셋", height=hi)
        self.dir_depth = ft.TextField(label="디렉토리 탐색 깊이", height=hi)
        self.use_weekday = ft.TextField(label="요일 구분 사용", width=610, height=hi)
        self.weekdays = ft.TextField(label="작업 요일 선택", height=hi)
        self.day = ft.TextField(label="일자", height=hi)
        self.hh = ft.TextField(label="시간")
        self.mm = ft.TextField(label="분", height=hi)
        self.ss = ft.TextField(label="초")
        self.use_file_filter = ft.TextField(label="파일 확장자 필터 사용", height=hi)
        self.file_filter_type = ft.TextField(label="파일 필터 타입(I/E)", height=hi)
        self.file_filter_exts = ft.TextField(label="파일 필터 확장자", width=610, height=hi)
        self.check_file_closed = ft.TextField(label="파일 닫힘 검사", height=hi)
        self.thread_count = ft.TextField(label="작업 Thread 개 수", height=hi)
        self.use_backup = ft.TextField(label="파일 암호화 전 백업 여부(Y/N)")
        self.backup_path = ft.TextField(label="파일 백업 경로", height=hi)
        self.temp_path = ft.TextField(label="작업 임시 경로")
        self.check_cycle = ft.TextField(label="작업 시간 도달 검시주기(sec)", height=hi)


    def clear(self):
        self.ip.value = ""
        self.policy.value = ""
        self.description.value = ""
        self.file_path.value = ""
        self.mode.value = ""
        self.time_limit.value = ""
        self.repeat.value = ""
        self.dir_format.value = ""
        self.ymd_offset.value = ""
        self.dir_depth.value = ""
        self.use_weekday.value = ""
        self.weekdays.value = ""
        self.day.value = ""
        self.hh.value = ""
        self.mm.value = ""
        self.ss.value = ""
        self.use_file_filter.value = ""
        self.file_filter_type.value = ""
        self.file_filter_exts.value = ""
        self.check_file_closed.value = ""
        self.thread_count.value = ""
        self.use_backup.value = ""
        self.backup_path.value = ""
        self.temp_path.value = ""
        self.check_cycle.value = ""

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

