import flet as ft
from modules import mytimer
from modules import spell_server as server
def IndexView(page:ft.Page, params):
    def timer_end(e):
        print("Timer end")
        #timer.restart_timer()
    def bottom_button_clicked(e):
        print("bottom button clicked")
        x = e.control.data
        for btn in top_row_buttons.controls:
            if btn.text == " ":
                btn.text = x
                e.control.text = " "
                e.control.disabled = True
                break
        page.update()
    def top_button_clicked(e):
        print("top button clicked")
        x=e.control.text
        for btn in bottom_row_buttons.controls:
            if btn.data == x and btn.text == " ":
                btn.text = x
                btn.disabled = False
                e.control.text=" "
                break
        page.update()
    def clear_top_buttons(e):
          for top_btn in top_row_buttons.controls:
              x = top_btn.text
              print(x)
              if x !=" ":
                  for bottom_btn in bottom_row_buttons.controls:
                      if bottom_btn.text == " " and bottom_btn.data== x:
                          print("found")
                          bottom_btn.text=x
                          bottom_btn.disabled=False
                          top_btn.text =" "
                          break
          page.update()


    def new_round(word):
        top_row_buttons.controls.clear()
        bottom_row_buttons.controls.clear()
        for x in word:
            bt1 = ft.OutlinedButton(" ",on_click=top_button_clicked)

            bt2 = ft.FilledButton(x, on_click=bottom_button_clicked, data=x)
            top_row_buttons.controls.append(bt1)
            bottom_row_buttons.controls.append(bt2)

    def CreateAppBar():
        app_bar = ft.AppBar(
            leading=ft.Image("images/csc_logo_100.png"),
            leading_width=40,
            title=ft.Text(" sample Flet Template"),
            #center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT
        )
        return app_bar
    appbar = CreateAppBar()
    game_client = server.GameClient("https://wordgameserver-production-e5c6.up.railway.app/")
    game_state = game_client.get_game_state()
    timer = mytimer.Countdown(game_state["time_remaining"], timer_end)
    print(game_state)
    #word = game_state["current_word"].upper()
    word = "LOOP"
    print(word)
    top_row_buttons = ft.Row(spacing=10,
        alignment=ft.MainAxisAlignment.CENTER)
    bottom_row_buttons = ft.Row(spacing=10,
        alignment=ft.MainAxisAlignment.CENTER)

    third_row_buttons = ft.Row(spacing=200,
        alignment=ft.MainAxisAlignment.CENTER)
    submit_button = ft.OutlinedButton("Submit")
    clear_button = ft.OutlinedButton("Clear" ,on_click=clear_top_buttons)

    third_row_buttons.controls.append(submit_button)
    third_row_buttons.controls.append(clear_button)
    new_round(word)
    page.views.append(ft.View(
        "/",
        [appbar, timer, top_row_buttons, bottom_row_buttons,third_row_buttons],


    )
    )
    page.update()
