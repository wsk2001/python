# -*- coding: utf-8 -*-

import flet as ft


class XfcKeyMaterial:

    def __init__(self):
        self.key_id = ft.TextField(label="key_id", width=620, on_focus=self.focused)
        self.key_material = ft.TextField(label="key_material", width=620, on_focus=self.focused)
        self.key_iv = ft.TextField(label="key_iv", width=620, on_focus=self.focused)
        self.key_activeyn = ft.TextField(label="key_active", width=620)
        self.select_name = ""

    def clear(self):
        self.key_id.value = ""
        self.key_material.value = ""
        self.key_iv.value = ""
        self.key_activeyn.value = ""

    def view(self):
        print(self.key_id.value)
        print(self.key_material.value)
        print(self.key_iv.value)
        print(self.key_activeyn.value)

    def focused(self, e):
        self.select_name = e.control.label
