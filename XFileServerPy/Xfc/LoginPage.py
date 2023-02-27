import flet
from flet import Page, TextField, Text, ElevatedButton, Column

count = 0

def Login(page: Page, func, title=None):
    def handle_login(e):
        if username.value == "test" and password.value == "test":
            page.window_left = 0
            page.window_top = 0
            return func(e.page)
        else:
            global count
            count += 1
            if 3 <= count:
                return page.window_destroy()

    if title is not None:
        page.title = title
    else:
        page.title = "Login"

    username = TextField(label="Login Name")
    password = TextField(label="Password", password=True)

    page.window_left = 400
    page.window_top = 200
    page.window_width = 600
    page.window_height = 250

    page.horizontal_alignment = "center"
    page.vertical_alignment = "spaceBetween"

    login = ElevatedButton(
        text="로그인",
        width=page.width,
        color="white",
        bgcolor="blue", # "purple",
        on_click=handle_login
    )

    col = Column(
        controls=[
            username,
            password,
            login
        ],
    )

    page.controls.append(col)

    page.update()


if __name__ == "__main__":
    target = Login
    view_type = flet.FLET_APP
    # view_type = ft.WEB_BROWSER

    flet.app(target=target, view=view_type, assets_dir='assets')
