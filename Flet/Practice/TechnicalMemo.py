import flet as ft

category_list = [
    "all", "개발 종합", "개발 언어 C/C++", "개발 언어 Python", "개발 언어 Java", "개발 언어 JavaScript", "개발 언어 Go",
    "개발 언어 Dart", "개발 언어 PHP", "프레임워크", "경제", "사회", "문학", "개인 메모", "언어"
]


def navi_change(e):
    print("Selected destination:", e.control.selected_index)
    if e.control.selected_index == 0:
        edit_page(e.page)
    elif e.control.selected_index == 1:
        search_list(e.page)
    elif e.control.selected_index == 2:
        e.page.window_destroy()


rail = ft.NavigationRail(
    selected_index=0,
    label_type=ft.NavigationRailLabelType.ALL,
    min_width=100,
    min_extended_width=400,
    group_alignment=-0.9,
    destinations=[
        ft.NavigationRailDestination(
            icon=ft.icons.CREATE_SHARP, selected_icon=ft.icons.CREATE, label="편집"
        ),
        ft.NavigationRailDestination(
            icon=ft.icons.SAVED_SEARCH_SHARP, selected_icon=ft.icons.SAVED_SEARCH, label="검색"
        ),
        ft.NavigationRailDestination(
            icon=ft.icons.EXIT_TO_APP,
            selected_icon_content=ft.Icon(ft.icons.EXIT_TO_APP_SHARP),
            label_content=ft.Text("Exit"),
        ),
    ],
    on_change=navi_change,
)


def search_list(page):
    page.clean()
    title = ft.TextField(label="목록", width=1100)
    memo = ft.TextField(label="메모", multiline=True, width=1100)

    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                ft.Column([
                    ft.Row([title]),
                    ft.Row([memo]),
                ]),
            ],
            expand=True,
        )
    )
    page.update()


def new_memo(e):
    edit_page(e.page)


def save_memo(e):
    pass


def edit_page(page):
    page.clean()
    page.title = "기술 문서 작성"
    title = ft.TextField(label="제목", width=1100)
    # max_lines is not the maximum line that can be edited, but the maximum line displayed on the screen.
    # comment by wonsool.
    memo = ft.TextField(label="메모", multiline=True, max_lines=19, width=1100)
    btn_new = ft.ElevatedButton(text="새로 작성", icon=ft.icons.FIBER_NEW, on_click=new_memo)
    btn_save = ft.ElevatedButton(text="저장", icon=ft.icons.SAVE_ALT, on_click=save_memo)

    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                ft.Column([
                    ft.Row([btn_new, btn_save]),
                    ft.Divider(thickness=1, color="grey"),
                    ft.Row([title]),
                    ft.Row([memo]),
                ]),
            ],
            expand=True,
        )
    )
    page.update()

def main(page: ft.Page):
    # page.title = "기술 문서"
    # page.horizontal_alignment = "center"

    # page.padding = 60
    # page.scroll = True
    edit_page(page)


ft.app(target=main)