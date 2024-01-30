# -*- coding: utf-8 -*-

import flet as ft
from . import XfcDB as xdb
from . import XfcRaPolicy


def ra_policy_list_page(page: ft.Page):
    dbms = xdb.XfcDB()

    def select_ra_id(e):
        if 0 < len(e.control.content.value):
            ra_ip.value = e.control.content.value
            page.update()

    def edit_ra_policy(e):
        if 0 < len(ra_ip.value):
            ra_policy = XfcRaPolicy.XfcRaPolicy()
            ra_policy.ra_main(page, ra_ip.value)

    def delete_ra_policy(e):
        if 0 < len(ra_ip.value):
            dbms.delete_ra(ra_ip.value)
            ra_ip.value = e.control.content.value
            ra_policy_list_page(page)

    def close_dlg(e):
        dlg_modal.open = False
        page.update()

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please confirm"),
        content=ft.Text("Do you really want to delete selected policy?"),
        actions=[
            ft.TextButton("Yes", on_click=delete_ra_policy),
            ft.TextButton("No", on_click=close_dlg),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )

    def open_dlg_modal(e):
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    page.clean()

    page.appbar.title = ft.Text("List XFile Remote Agent Policy")

    ra_ip = ft.TextField(label="Remote Agent ID", disabled=True, color="cyan", width=360)
    btn_edit = ft.ElevatedButton(text="선택 항목 편집", icon=ft.icons.EDIT_DOCUMENT, on_click=edit_ra_policy)
    btn_del = ft.ElevatedButton(text="선택 항목 삭제", icon=ft.icons.DELETE, on_click=open_dlg_modal)

    page.add(ft.Row(controls=[ra_ip, btn_edit, btn_del]))

    header = [ft.DataColumn(ft.Text("RA ID")),
              ft.DataColumn(ft.Text("정책 유형")),
              ft.DataColumn(ft.Text("프로토콜")),
              ft.DataColumn(ft.Text("앤드 포인트")),
              ft.DataColumn(ft.Text("암호화 정책")),
              ft.DataColumn(ft.Text("설명", width=400))]

    df = dbms.list_ra_policy()
    value_list = df.values.tolist()
    row_list = []
    row_list.clear()

    first_row = True
    for v in value_list:
        row_list.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(v[0], color="cyan"), on_tap=select_ra_id),
                    ft.DataCell(ft.Text('RemoteAgent' if v[1] == 'C' else 'LocalAgent')),
                    ft.DataCell(ft.Text(v[2])),
                    ft.DataCell(ft.Text(v[3])),
                    ft.DataCell(ft.Text(v[4])),
                    ft.DataCell(ft.Text(v[8])),
                ],
            )
        )
        if first_row:
            ra_ip.value = v[0]
            first_row = False

    page.add(
        ft.DataTable(
            heading_row_color=ft.colors.BLACK12,
            columns=header,
            rows=row_list,
        ),
    )

    page.update()
