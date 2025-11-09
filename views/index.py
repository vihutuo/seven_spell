import flet as ft
from modules import mytimer
from modules import my_module
from modules import spell_server as server
import random
import threading
from modules import users_manager as um
from modules import log

def IndexView(page:ft.Page, params):
    def on_pubsub(msg):
        if msg == "users_changed":
            print("users_changed")
            user_count_txt.value = UM.get_user_count()
            page.update()

    page.pubsub.subscribe(on_pubsub)
    def update_score(s):
        nonlocal score
        score += s
        if score< 0:
            score = 0
        score_text.value = "Score : " + str(score)


    def page_on_connect(e):
        log.info("Session connect")
        UM.add_user(page.session_id,player_name)
        if not main_timer.running:
            log.info("On connect new round started")
            nonlocal is_game_active
            is_game_active = True
            new_round()


    def page_on_disconnect(e):
        print("Session disconnect")
        UM.remove_user(page.session_id)
        nonlocal  is_game_active
        is_game_active = False
    def show_status_message(msg):
        status_message_box.value = msg

    def get_high_score_table(json_data):
        # print("Drawinh HS table")
        data = json_data
        # print(data)
        tbl = ft.DataTable(columns=[
            ft.DataColumn(ft.Text("Rank")),
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Score"), numeric=True),
        ],
            heading_row_height=0,
            column_spacing=50,
            rows=[]
        )
        rank=1
        for item in data:

             #    if analytics.userid == item["id"]:
             #       c = ft.colors.SECONDARY_CONTAINER
             #   else:
             #      c = ft.colors.TRANSPARENT
                if item["player"] == player_name and  item["score"] == score:
                    c = ft.colors.SECONDARY_CONTAINER
                else:
                    c = ft.colors.TRANSPARENT

                tbl.rows.append( ft.DataRow(color=c,
                                           cells=[
                                               ft.DataCell(ft.Text(rank)),
                                               ft.DataCell(ft.Text(item["player"])),
                                               ft.DataCell(ft.Text(item["score"])),

                                           ]))
                rank+=1


        return tbl

    def start_main_timer(seconds,on_end):
        # helper function that starts main timer
        main_timer.start(seconds,on_end)
    def score_submit_event(e):

        top_row_buttons.disabled = True
        bottom_row_buttons.disabled = True
        third_row_buttons.disabled = True
        status_message_box.value = "Score submitted. Waiting for result"
        page.update()
        try:
            game_client.submit_score(player_name, score, main_word.lower())
        except Exception as e:
            log.error(e)

        start_main_timer(5,fetch_results)

    def fetch_results(e):
       try:
           all_scores=game_client.fetch_scores()
       except Exception as e:
           log.error(e)
       else:
           print(all_scores)
           scores_dialog.content  =get_high_score_table(all_scores)
           page.open(scores_dialog)
       secs  = game_client.get_time_remaining_for_next_round(game_state)
       start_main_timer(secs,new_round)

    def scores_display_screen():
        print("score display screen")
    def bottom_button_clicked(e):
        if e.control.text == " ":
            return
        x = e.control.data
        for btn in top_row_buttons.controls:
            if btn.text == " ":
                btn.text = x
                e.control.text = " "
                e.control.disabled = True
                break
        page.update()
    def top_button_clicked(e):
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

    def update_player_name(new_name):
            nonlocal player_name
            player_name = new_name
            txt_playername.spans[0].text = player_name
            UM.update_user(page.session_id, username=player_name)

            #page.update()

    def player_name_clicked(e):
        txt_name = ft.Ref[ft.TextField]()

        def close_dlg_ok(e):
            txt_name.current.value = txt_name.current.value.strip()
            if len(txt_name.current.value) == 0:
                return
            update_player_name(txt_name.current.value)
            dlg_modal.open = False
            page.update()


        def close_dlg_cancel(e):
            dlg_modal.open = False
            page.update()



        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Enter your name"),
            content=ft.TextField(ref=txt_name, hint_text="Enter your name", value=player_name, max_length=10),
            actions=[
                ft.TextButton("OK", on_click=close_dlg_ok),
                ft.TextButton("Cancel", on_click=close_dlg_cancel),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )
        page.open(dlg_modal)
        page.update()
    def hide_points():
            txt_points.opacity = 0
            txt_points.update()
            print("Hide points")

    def points_animation_end(e):

        if txt_points.opacity != 0:
            threading.Timer(1, hide_points).start()

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
            add_score = len(word)
            if len(word)==len(main_word):
                add_score=int(add_score*1.5)
            update_score(add_score)
            user_words_textbox.value+= word + " "
            txt_points.value = "+" + str(add_score)
            txt_points.opacity = 1
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
        update_score(-score)
        show_status_message("Make 3+ letter words")
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
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.Text("Online : "),
                ft.Container(
                    content=user_count_txt,
                    margin=ft.margin.only(right=20)  # ✅ Right margin
                )
            ],
        )
        return app_bar
    #game_variable
    score=0
    UM = um.UserManager(page)
    player_name = "Player" + str(random.randrange(1, 1000))
    UM.add_user(page.session_id, player_name)
    game_state ={}
    main_word = ""
    is_game_active = True

    game_client = server.GameClient("https://wordgameserver1.fly.dev/")
    user_count_txt = ft.Text(value="0", style=ft.TextThemeStyle.LABEL_LARGE)  #used in AppBar
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
    score_text=ft.Text("0",style=ft.TextStyle(size=20), )
    update_score(0)
    main_timer = mytimer.Countdown()

    txt_playername = ft.Text(style=ft.TextThemeStyle.LABEL_LARGE,
                             spans=[ft.TextSpan(player_name, on_click=player_name_clicked,
                                                style=ft.TextStyle(
                                                    decoration=ft.TextDecoration.UNDERLINE,
                                                    decoration_style=ft.TextDecorationStyle.DOTTED,
                                                    size=18,
                                                    color=ft.colors.SECONDARY
                                                )
                                                )
                                    ]
                             )
    icon_timer = ft.Icon(name=ft.icons.SCHEDULE, color=ft.colors.SECONDARY)
    line_1 = ft.Divider(height=1, color=ft.colors.SECONDARY_CONTAINER)
    vertical_line = ft.VerticalDivider(
        width=20,  # Line width
        color= ft.colors.AMBER,
        thickness=12  # Line thickness
    )
    txt_points = ft.Text("",
                         animate_opacity=600,
                         opacity=0,
                         on_animation_end=points_animation_end)

    score_row=ft.Row(controls=[txt_playername,  score_text,  ft.Row(controls=[icon_timer,main_timer], width = 80)],
                     alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    status_message_box=ft.Text()
    scores_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Scores"),
        content=ft.Text(""),
        actions_alignment=ft.MainAxisAlignment.END
    )
    content_width = 360
    user_words_row = ft.Row(controls=[user_words_textbox],  alignment=ft.alignment.top_left, wrap=True, width=content_width)
    #page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    all_content = ft.Container(
        content=ft.Column(
            controls=[score_row, line_1, ft.Row(controls=[top_row_buttons, txt_points]), bottom_row_buttons,
                      status_message_box,third_row_buttons,user_words_row],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        alignment=ft.alignment.center,
        width=content_width,  # Set a specific width
        padding=0,
        #border_radius=10,
        #border=ft.border.all(1, ft.colors.OUTLINE),
    )
    team_name = ft.Text(
        value="Created by :  Abhinash, Imkongsenup & Sir Vihutuo(Teacher), LSHSS. \nMake as many 3 letter or longer words.",
        size=15,
        opacity=0.60,
        color="#b2b2b2")
    page.views.append(ft.View(
        "/",[appbar,all_content,ft.Container(
        content=team_name,
        border=ft.border.only(
          top=ft.border.BorderSide(1, ft.colors.SECONDARY_CONTAINER)),
        margin=ft.margin.only(top=250))
             ],horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    )
    page.update()
    page.on_disconnect = page_on_disconnect
    page.on_connect = page_on_connect
    new_round()
