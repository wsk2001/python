# -*- coding: utf-8 -*-

import flet as ft

def main(page: ft.Page):
    ext_rows = [
                ft.DataRow(
                    [ft.DataCell(ft.Text("A")), ft.DataCell(ft.Text("1"))],
                    selected=True,
                    on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                ),
                ft.DataRow([ft.DataCell(ft.Text("Z")), ft.DataCell(ft.Text("2"))]),
            ]
    print(type(ext_rows))
	
    page.add(
        ft.DataTable(
            width=700,
            bgcolor="yellow",
            border=ft.border.all(2, "red"),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(3, "blue"),
            horizontal_lines=ft.border.BorderSide(1, "green"),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=ft.colors.BLACK12,
            heading_row_height=100,
            data_row_color={"hovered": "0x30FF0000"},
            show_checkbox_column=True,
            divider_thickness=0,
            column_spacing=200,
            columns=[
                ft.DataColumn(
                    ft.Text("Column 1"),
                    on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                ft.DataColumn(
                    ft.Text("Column 2"),
                    tooltip="This is a second column",
                    numeric=True,
                    on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
            ],
            rows=ext_rows,
        ),
    )

    page.add(
        ft.OutlinedButton(text="Outlined button"),
        ft.OutlinedButton("Disabled button", disabled=True),
    )

    page.add(
        ft.ElevatedButton(text="Elevated button"),
        ft.ElevatedButton("Disabled button", disabled=True),
    )

    def button_clicked(e):
        t.value = (
            f"Switch values are:  {c1.value}, {c2.value}, {c3.value}, {c4.value}."
        )
        page.update()

    t = ft.Text()
    c1 = ft.Switch(label="Unchecked switch", value=False)
    c2 = ft.Switch(label="Checked switch", value=True)
    c3 = ft.Switch(label="Disabled switch", disabled=True)
    c4 = ft.Switch(
        label="Switch with rendered label_position='left'", label_position=ft.LabelPosition.LEFT
    )
    b = ft.ElevatedButton(text="Submit", on_click=button_clicked)
    page.add(c1, c2, c3, c4, b, t)


    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_files.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text()

    page.overlay.append(pick_files_dialog)

    page.add(
        ft.Row(
            [
                ft.ElevatedButton(
                    "Pick files",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=True
                    ),
                ),
                selected_files,
            ]
        )
    )

#ft.app(target=main)
ft.app(target=main, view=ft.WEB_BROWSER)

# ext_rows 의 내용(list) 를 직접 내부의 rows 에 대입 하여도 된다.
