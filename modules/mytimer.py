import asyncio
import flet as ft

class Countdown(ft.Text):
    def __init__(self, seconds, on_end):
        super().__init__()
        self.initial_seconds = seconds
        self.seconds = seconds
        self.on_end = on_end
        self.running = False
        self.size = 20
    def start(self):
        self.running = True
        self.seconds = self.initial_seconds
        self.page.run_task(self.update_timer)
    def reset_timer(self):
        self.seconds = self.initial_seconds


    def did_mount(self):
        self.reset_timer()
    def will_unmount(self):
        self.running = False

    async def update_timer(self):
        while self.seconds>=0 and self.running:

            #mins, secs = divmod(self.seconds, 60)
            #self.value = "{:02d}:{:02d}".format(mins, secs)
            self.value = self.seconds
            self.update()
            await asyncio.sleep(1)
            self.seconds -= 1

        e = None
        self.on_end(e)
