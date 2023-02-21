
import flet
import datetime
from flet import Page,TextField,Checkbox,Text,FloatingActionButton,icons,Column,Row,UserControl,IconButton,colors,theme,Divider

class Task(UserControl):
    def __init__(self,date, title,desc, task_delete):
        super().__init__()
        self.date = date
        self.title = title
        self.desc = desc
        self.task_delete = task_delete

    def delete_clicked(self, e):
        self.task_delete(self)

    def build(self):
        self.date = Text(value=self.date,expand=1,text_align="right")
        self.display_desc = TextField(value=self.desc,expand=True,visible=False,)
        self.display_task = Checkbox(value=False,label=self.title,)
        self.edit_title = TextField(expand=1,value=self.title)
        self.edit_desc = TextField(expand=1,multiline=True,min_lines=10,value=self.desc)
        self.view_title = Text(expand=1,value=self.title)
        self.view_desc = Text(expand=1,value=self.desc)
        

        self.display_view = Row(
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                
                self.display_task,
                self.display_desc,
                self.date,
                Row(
                    spacing=0,
                    controls=[
                        IconButton(
                            icon=icons.READ_MORE,
                            tooltip="View Diary",
                            on_click=self.show_desc,icon_color=colors.GREEN_ACCENT_400,
                        ),
                        IconButton(
                            icon=icons.CREATE_OUTLINED,
                            tooltip="Edit Diary",
                            on_click=self.edit_clicked,icon_color=colors.GREEN_600,
                        ),
                        IconButton(
                            icons.DELETE_OUTLINE,
                            tooltip="Delete Diary",
                            on_click=self.delete_clicked,icon_color=colors.RED,
                        ),
                    ],
                ),
            ],
        )

        self.item_view = Column(
                    visible=False,
                    controls=[
                        Row(controls=[self.view_title,]),
                        Row(controls=[self.view_desc,]),
                        Row(controls=[IconButton(icon=icons.CLOSE,
                        icon_color=colors.RED,tooltip="View Diary",on_click=self.close_clicked,)]),
                    ]
                )

        self.edit_view = Column(
                    visible=False,
                    controls=[
                        Row(controls=[self.edit_title,]),
                        Row(controls=[self.edit_desc,]),
                        Row(controls=[IconButton(icon=icons.DONE_OUTLINE_OUTLINED,
                        icon_color=colors.GREEN,tooltip="Update Diary",on_click=self.save_clicked,)]),
                    ]
                )
        return Column(controls=[self.display_view, self.edit_view,self.item_view])

    def show_desc(self,e):
        self.view_title.value  = self.display_task.label
        self.view_desc.value = self.display_desc.value
        self.item_view.visible = True
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def edit_clicked(self, e):
        self.edit_title.value  = self.display_task.label
        self.edit_desc.value = self.display_desc.value
        self.display_view.visible = False
        self.edit_view.visible = True
        self.item_view.visible = False
        self.update()

    def close_clicked(self,e):
        self.display_view.visible = True
        self.item_view.visible = False
        self.edit_view.visible = False
        self.update()

    def save_clicked(self, e):
        self.display_task.label = self.edit_title.value
        self.display_desc.value = self.edit_desc.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    

class DiaryApp(UserControl):
    def build(self):
        self.title = TextField(hint_text="Title...",icon=icons.TITLE,)
        self.desc = TextField(hint_text="Write your diary here...",multiline=True,border="outline", min_lines=18,max_lines=1000,)
        self.tasks = Column()


        return [Column(
                    width=500,
                    expand=True,
                    scroll=True,
                    controls=[
                        self.title,
                        self.desc,
                        FloatingActionButton(icon=icons.ADD,on_click=self.add_clicked),
                        
                    ],
                ),
                Row(
                    controls=[
                        Column(width=550,),
                        Column(
                            alignment="end",
                            expand=True,
                            scroll=True,
                            height=550,
                            controls=[
                                self.tasks
                            ],
                        )   
                    ]
                )  
           ]




    def add_clicked(self, e):
        self.datetime_object = datetime.date.today()
        task = Task(self.datetime_object,self.title.value,self.desc.value, self.task_delete)
        self.tasks.controls.append(task)
        self.title.value = ""
        self.desc.value = ""
        self.update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()



def main(page):
    page.title =  "Diary"
    page.theme = theme.Theme(color_scheme_seed="green",font_family="kanit")
    page.bgcolor = colors.LIGHT_GREEN_50
    page.horizontal_alignment="center"
    page.padding = 60
    page.scroll = True
    page.update()

    hr = Divider(height=10,thickness=3,color=colors.GREEN_ACCENT_700,)
    date_object = Text(datetime.date.today())
    time_object = Text(datetime.timezone.max)
    print(date_object)
    app = DiaryApp()
    page.add(Row(alignment="center",controls=[date_object,time_object]),hr,app)


flet.app(target=main)