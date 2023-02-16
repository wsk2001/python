import flet as ft


def navi_change(e):
    print("Selected destination:", e.control.selected_index)
    if e.control.selected_index == 3:
        e.page.window_destroy()


rail = ft.NavigationRail(
    selected_index=0,
    label_type=ft.NavigationRailLabelType.ALL,
    # extended=True,
    min_width=100,
    min_extended_width=400,
    # leading=ft.FloatingActionButton(icon=ft.icons.CREATE, text="Add"),
    group_alignment=-0.9,
    destinations=[
        ft.NavigationRailDestination(
            icon=ft.icons.CREATE_SHARP, selected_icon=ft.icons.CREATE, label="Api"
        ),
        ft.NavigationRailDestination(
            icon=ft.icons.FAVORITE_BORDER, selected_icon=ft.icons.FAVORITE, label="Local Agent"
        ),
        ft.NavigationRailDestination(
            icon_content=ft.Icon(ft.icons.BOOKMARK_BORDER),
            selected_icon_content=ft.Icon(ft.icons.BOOKMARK),
            label="Schedule Agent",
        ),
        ft.NavigationRailDestination(
            icon=ft.icons.EXIT_TO_APP,
            selected_icon_content=ft.Icon(ft.icons.EXIT_TO_APP_SHARP),
            label_content=ft.Text("Exit"),
        ),
    ],
    on_change=navi_change,
)


def main(page: ft.Page):
    # page.expand = True
    # page.scroll = "auto"

    id = ft.TextField(label="ID", color="red")
    remark = ft.TextField(label="Remark", width=920, color="red")
    createTime = ft.TextField(label="Create Time", color="red")
    updateTime = ft.TextField(label="Update Time", color="red")

    platform = ft.TextField(label="platform")
    providerName = ft.TextField(label="provider Name")
    process = ft.TextField(label="process")
    ipAddr = ft.TextField(label="ip Address")
    macAddr = ft.TextField(label="MAC Address")
    modifiedDate = ft.TextField(label="수정 일자")
    domainKeyId = ft.TextField(label="도메인 Key Id", width=610)
    domainAlgorithm = ft.TextField(label="도메인 암호화 Algorithm")
    domainKeyLength = ft.TextField(label="도메인 키 길이")
    modulus = ft.TextField(label="modulus", width=1230)
    publicExponent = ft.TextField(label="publicExponent", width=1230)
    privateExponent = ft.TextField(label="privateExponent", width=1230)
    domainCode = ft.TextField(label="도메인 코드", width=1230)
    attributeKeyId = ft.TextField(label="attributeKeyId")
    attributeIv = ft.TextField(label="attributeIv")
    attributeAlgorithm = ft.TextField(label="attributeAlgorithm")
    attributeKeyLength = ft.TextField(label="attributeKeyLength")
    attributeChiperMode = ft.TextField(label="attributeChiperMode")
    attributePaddingMethod = ft.TextField(label="attributePaddingMethod")
    attributeKeyMaterial = ft.TextField(label="attributeKeyMaterial", width=610)
    contentsAlgorithm = ft.TextField(label="contentsAlgorithm")
    contentsKeyLength = ft.TextField(label="contentsKeyLength")
    memo = ft.TextField(label="Memo", multiline=True, width=1230, height=180)

    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                ft.Column([
                    ft.Row([id, remark]),
                    ft.Row([createTime, updateTime]),
                    ft.Row([platform, providerName, ipAddr, macAddr]),
                    ft.Row([domainKeyId, domainAlgorithm, domainKeyLength]),
                    ft.Row([modulus]),
                    ft.Row([publicExponent]),
                    ft.Row([privateExponent]),
                    ft.Row([domainCode]),
                    ft.Row([attributeKeyId, attributeIv, attributeAlgorithm, attributeKeyLength]),
                    ft.Row([attributeChiperMode, attributePaddingMethod, attributeKeyMaterial]),
                    ft.Row([contentsAlgorithm, contentsKeyLength]),
                    ft.Row([memo]),
                ]),
            ],
            expand=True,
        )
    )


ft.app(target=main)