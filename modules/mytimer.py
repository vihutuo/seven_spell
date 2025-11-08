import asyncio
import flet as ft

class Countdown(ft.Text):
    def __init__(self):
        super().__init__()
        self._initial_seconds = 0
        self._seconds = 0
        self.on_end = None
        self.running = False
        self.size = 20
        self._task = None
    def start(self,seconds,on_end):
        # cancel an existing task if still running
        self.running = False

        self._seconds = seconds
        self._initial_seconds = seconds
        self.on_end = on_end

        self.running = True
        # run the loop
        self._task = self.page.run_task(self.update_timer)

    def reset_timer(self):
        self._seconds = self._initial_seconds


    def did_mount(self):
        self.reset_timer()
    def will_unmount(self):
        self.running = False

    async def update_timer(self):
        while self._seconds>=0 and self.running:

            #mins, secs = divmod(self.seconds, 60)
            #self.value = "{:02d}:{:02d}".format(mins, secs)
            self.value = self._seconds
            self.update()
            await asyncio.sleep(1)
            self._seconds -= 1

        e = None
        self.running = False
        self.on_end(e)
