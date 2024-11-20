import flet as ft
from flet_core import OutlinedButton

from modules import mytimer
from modules import spell_server as server

def IndexView(page:ft.Page, params):
    def timer_end(e):
        print("Timer end")
        timer.restart_timer()
    def CreateAppBar():
        app_bar = ft.AppBar(
            leading=ft.Image("images/csc_logo_100.png"),
            leading_width=40,
            title=ft.Text(" sample Flet Template"),
            #center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(ft.icons.RESTART_ALT, on_click=restart_clicked),
                ft.IconButton(ft.icons.FILTER_3),

            ],
        )
        return app_bar

    def restart_clicked(e):
         dlg = ft.AlertDialog(title=ft.Text("You clicked restart"))
         page.open(dlg)
    def btn_question1_clicked(e):
        page.go("/question/1")

    def btn_question2_clicked(e):
        page.go("/question/2")

    def btn_simple_clicked(e):
        page.go("/simple_view")

    txt = ft.Text("Welcome to the Flet Template", font_family="playwrite")
    col_right = ft.Row(controls=[txt], alignment=ft.MainAxisAlignment.END)
    btn_question1 = ft.ElevatedButton("Question1", on_click=btn_question1_clicked)
    btn_question2 = ft.ElevatedButton("Question2", on_click=btn_question2_clicked)
    btn_simple = ft.ElevatedButton("Simple View", on_click=btn_simple_clicked)

    appbar = CreateAppBar()
    timer = mytimer.Countdown(10, timer_end)
    game_client = server.GameClient("https://wordgameserver-production-e5c6.up.railway.app/")
    game_state = game_client.get_game_state()
    word = game_state["current_word"]
    #word = "bright"
    print(word)
    top_row_buttons = ft.Row()

    lst_top_buttons = []
    for i in range(len(word)):
        bt = ft.OutlinedButton(" ")
        lst_top_buttons.append(bt)
        top_row_buttons.controls.append(bt)

    bottom_row_buttons = ft.Row()

    lst_bottom_buttons = []
    for x in word:
        bt = ft.FilledButton(x)
        lst_bottom_buttons.append(bt)
        bottom_row_buttons.controls.append(bt)

    page.views.append(ft.View(
        "/",
        [appbar, col_right, btn_question1,
         btn_question2, btn_simple, timer, top_row_buttons, bottom_row_buttons],

    )
    )
    page.update()
