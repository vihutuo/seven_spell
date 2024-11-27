import flet as ft
from modules import mytimer
from modules import my_module
from modules import spell_server as server
def IndexView(page:ft.Page, params):
    def page_on_connect(e):
         print("Session connect")

    def page_on_disconnect(e):
        print("Session disconnect")
        nonlocal  is_game_active
        is_game_active = False
    def show_status_message(msg):
        status_message_box.value = msg
    def start_main_timer(seconds,on_end):
        # helper function that starts main timer
        main_timer.initial_seconds = seconds
        main_timer.on_end = on_end
        main_timer.start()
    def score_submit_event(e):
        game_client.submit_score(player_name,score,main_word.lower())
        top_row_buttons.disabled = True
        bottom_row_buttons.disabled = True
        third_row_buttons.disabled = True
        status_message_box.value="Score submitted. Waiting for result"
        start_main_timer(5,fetch_results)
        page.update()


    def fetch_results(e):
       all_scores=game_client.fetch_scores()
       scores_dialog.content.value =all_scores
       page.open(scores_dialog)
       secs  = game_client.get_time_remaining_for_next_round(game_state)
       start_main_timer(secs,new_round)
    def score_submit_screen():
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Scores"),
            content=ft.Text("Do you really want to delete all those files?"),

            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: page.add(
                ft.Text("Modal dialog dismissed"),
            ),
        )
        page.open(dlg_modal)
    def scores_display_screen():
        print("score display screen")
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
              top_btn.text= " "
          for bottom_btn in bottom_row_buttons.controls:
              bottom_btn.text= bottom_btn.data
              bottom_btn.disabled = False
          page.update()
    def calculate_score(word):
        nonlocal score
        score+=len(word)
        score_text.value = str(score)
        page.update()

    def submit_click(e):
        word = ""
        for top_btn in top_row_buttons.controls:
            if top_btn.text != " ":
                word+=top_btn.text
            else:
                break
        print(word)
        is_valid = True
        if len(word)<3:
            is_valid=False
            print("len less than 3")
        if word in user_words:
            is_valid=False
            print("is in userword")
        if is_valid and word not in all_words:
            is_valid=False
            print("not in all word")
        if is_valid:
            user_words.append(word)
            calculate_score(word)
            user_words_textbox.value+= word + " "
            page.update()
        else:
            print("invalid")
    def load_game_state():
        nonlocal game_state
        nonlocal main_word
        game_state = game_client.get_game_state()
        main_word = game_state["current_word"].upper()
    def new_round(event=None):
        if not  is_game_active:
            print("Game not active")
            return
        scores_dialog.open = False
        nonlocal  score

        load_game_state()
        if game_state["time_remaining"] <= 3:
            status_message_box.value = "Waiting to start next round "
            start_main_timer(game_state["next_round_starts_in"], new_round)
            page.update()
            return

        top_row_buttons.controls.clear()
        bottom_row_buttons.controls.clear()
        for x in main_word:
            bt1 = ft.OutlinedButton(" ",on_click=top_button_clicked,
                                    width=40,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=7),
                                        padding=4)
                                    )
            bt2 = ft.FilledButton(x, on_click=bottom_button_clicked, data=x,
                                  width=40,
                                  style=ft.ButtonStyle(
                                      shape=ft.RoundedRectangleBorder(radius=20),
                                      padding=4)
            )

            top_row_buttons.controls.append(bt1)
            bottom_row_buttons.controls.append(bt2)
        start_main_timer(game_state["time_remaining"], score_submit_event)
        score=0
        score_text.value=score
        show_status_message("")
        user_words_textbox.value=""
        top_row_buttons.disabled = False
        bottom_row_buttons.disabled = False
        third_row_buttons.disabled = False
        page.update()

    def CreateAppBar():
        app_bar = ft.AppBar(
            leading=ft.Image("images/csc_logo_100.png"),
            leading_width=40,
            title=ft.Text("Seven Spell"),
            #center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT
        )
        return app_bar
    #game_variable
    score=0
    player_name="John"
    game_state ={}
    main_word = ""
    is_game_active = True

    game_client = server.GameClient("https://wordgameserver-production.up.railway.app/")

    appbar = CreateAppBar()

    top_row_buttons = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
    bottom_row_buttons = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
    third_row_buttons = ft.Row(spacing=100,
        alignment=ft.MainAxisAlignment.CENTER)
    submit_button = ft.OutlinedButton("Submit" ,on_click=submit_click)
    clear_button = ft.OutlinedButton("Clear" ,on_click=clear_top_buttons)

    third_row_buttons.controls.append(submit_button)
    third_row_buttons.controls.append(clear_button)
    user_words_textbox=ft.Text("")

    all_words=my_module.GetAllWords("data/3_letter_plus_words.txt")
    user_words=[]
    score_text=ft.Text("0",style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD))
    main_timer = mytimer.Countdown(0, score_submit_event)

    score_row=ft.Row(controls=[ft.Text("SCORE",style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD)),score_text, main_timer],
                     alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    status_message_box=ft.Text()
    scores_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Scores"),
        content=ft.Text(""),
        actions_alignment=ft.MainAxisAlignment.END
    )
    page.views.append(ft.View(
        "/",
        [appbar,score_row,  top_row_buttons, bottom_row_buttons,
         third_row_buttons,status_message_box,user_words_textbox],



    )
    )
    page.update()
    page.on_disconnect = page_on_disconnect
    page.on_connect = page_on_connect
    new_round()
