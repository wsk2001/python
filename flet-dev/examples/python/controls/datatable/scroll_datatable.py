import flet as ft

def main(page):
    table=ft.DataTable(
        border=ft.border.all(2, "red"),
        show_bottom_border=True,
        # DataColumn 유형의 컨트롤을 열에 추가해야 합니다.
        columns=[
                ft.DataColumn(ft.Text("HELLO 1")),
                ft.DataColumn(ft.Text("BYE 2")),
                ft.DataColumn(ft.Text("SAMPLE COLUMN 3")),
                ft.DataColumn(ft.Text("DUMMY COLUMN 4")),
                ft.DataColumn(ft.Text("HELLO COLUMNS 5")),
                ft.DataColumn(ft.Text("BYE COLUMNS 6")),
                ft.DataColumn(ft.Text("OKAY COLUMNS 7")),ft.DataColumn(ft.Text("I LOVE COLUMNS 8")),
                ft.DataColumn(ft.Text("COLUMNS FOR SCROLLING 9"), numeric=True),
            ],
        #DataRow 형식의 컨트롤을 행에 추가해야 합니다.
        #DataRow 
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("John 1")),
                    ft.DataCell(ft.Text("John 2")),
                    ft.DataCell(ft.Text("John 3")),
                    ft.DataCell(ft.Text("John 4")),
                    ft.DataCell(ft.Text("John 5")),
                    ft.DataCell(ft.Text("John 6")),
                    ft.DataCell(ft.Text("John 7")),
                    ft.DataCell(ft.Text("John 8")),
                    ft.DataCell(ft.Text("John 9")),
                    ])
            ]
        )
    cv = ft.Column([table],scroll=True)
    rv = ft.Row([cv],scroll=True,expand=1,vertical_alignment=ft.CrossAxisAlignment.START)
    page.add(rv)
    def button_clicked(e):
        b=ft.DataRow(
                cells=[  
                    ft.DataCell(ft.Text("John 1")),
                    ft.DataCell(ft.Text("John 2")),
                    ft.DataCell(ft.Text("John 3")),
                    ft.DataCell(ft.Text("John 4")),
                    ft.DataCell(ft.Text("John 5")),
                    ft.DataCell(ft.Text("John 6")),
                    ft.DataCell(ft.Text("John 7")),
                    ft.DataCell(ft.Text("John 8")),
                    ft.DataCell(ft.Text("John 9")),
                    ])

        table.rows.append(b)
        page.update()
        print("버튼을 클릭")
    add_row = ft.ElevatedButton(text="데이터 행 추가",on_click=button_clicked,data=0)
    page.add(add_row)

ft.app(target=main)