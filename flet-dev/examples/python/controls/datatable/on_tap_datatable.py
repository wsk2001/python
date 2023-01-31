import flet as ft

def main(page: ft.Page):
    # this is the function that controls the value of the cell 
    # returns value on tap
    def updateOnTap(e):
      print(e.control.content.value)
      e.control.content.value = "Hello John"
      page.update()

    page.add(
        ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("First name")),
                ft.DataColumn(ft.Text("Last name")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("John"), show_edit_icon=True, on_tap=updateOnTap),
                        ft.DataCell(ft.Text("Smith")),
                    ],
                ),
            ],
        ),
    )

ft.app(target=main, view=ft.WEB_BROWSER)
