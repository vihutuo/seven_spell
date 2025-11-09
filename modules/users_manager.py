from dataclasses import dataclass
import flet as ft


class UserNotFound(Exception):
    pass

@dataclass
class User:
    userid: str
    username: str
    score: int = 0


users: dict[str, User] = {}

class UserManager:
    def __init__(self, page: ft.Page):
        self._page = page   # reference to this session's page

    # ---------------------------------------------------------
    def add_user(self, userid, username):
        users[userid] = User(userid=userid, username=username)
        self._page.pubsub.send_all("users_changed")

    # ---------------------------------------------------------
    def remove_user(self, userid):
        users.pop(userid, None)
        self._page.pubsub.send_all("users_changed")

    # ---------------------------------------------------------
    def update_user(self, userid, **changes):
        u = users.get(userid)
        if not u:
            return
        for k, v in changes.items():
            if hasattr(u, k):
                setattr(u, k, v)
        self._page.pubsub.send_all("users_changed")

    # ---------------------------------------------------------
    def get_user(self, userid):
        return users.get(userid)

    # ---------------------------------------------------------
    def get_user_count(self):
        return len(users)

    # ---------------------------------------------------------
    def all_users(self):
        return list(users.values())