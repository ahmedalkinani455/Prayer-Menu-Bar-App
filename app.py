import rumps
from main import next_prayers, prayer_times, get_coordinates
import datetime

class PrayerMenuBar(rumps.App):
    def __init__(self):
        super(PrayerMenuBar, self).__init__("Prayer Menu")
        self.icon = "icon.png"
        self.menu = ["Set Location", "Change Location"]
        self.notified = False
        self.city = None
        self.country = None
        self.lat = None
        self.long = None

    @rumps.clicked("Set Location")
    def set_location(self, _):
        resp = rumps.Window("Enter your Location (city, country): ", dimensions=(200, 47), cancel=True).run()

        if resp.clicked == 0:
            return
        txt = resp.text
        self.city = txt.split(",")[0].strip()
        self.country = txt.split(",")[1].strip()
        self.lat, self.long = get_coordinates(self.city, self.country)
        self.icon = None
        self.display()

    @rumps.clicked("Change Location")
    def change_location(self, _):
        resp = rumps.Window("Enter your Location (city, country): ", dimensions=(200, 47), cancel=True).run()
        if resp.clicked == 0:
            return
        txt = resp.text
        self.city = txt.split(",")[0].strip()
        self.country = txt.split(",")[1].strip()
        self.lat, self.long = get_coordinates(self.city, self.country)
        self.icon = None
        self.display()

    def display(self):
        self.menu.clear()

        self.menu.add(rumps.MenuItem("Set Location", callback=self.set_location))
        self.menu.add(rumps.MenuItem("Change Location", callback=self.change_location))
        self.menu.add(rumps.separator)

        times = prayer_times(self.lat, self.long)

        for prayer, time in times.items():
            self.menu.add(rumps.MenuItem(title=f"{prayer.upper()}: {time[0]}", callback=lambda _: None))
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem(title="Quit", callback=rumps.quit_application))

    def display_next(self):
        next_time = next_prayers(self.lat, self.long)
        prayer, time = next_time
        return f"{prayer.upper()}: {time}"

    def calculate_remaining_time(self):
        times = datetime.datetime.strptime(next_prayers(self.lat, self.long)[1], "%H:%M").time()
        time_now = datetime.datetime.now().time()

        today = datetime.date.today()

        dt_prayer = datetime.datetime.combine(today, times)
        dt_now = datetime.datetime.combine(today, time_now)

        elapsed = dt_prayer - dt_now

        hours = elapsed.seconds // 3600
        minutes = (elapsed.seconds % 3600) // 60

        return f"{round(hours)}h {round(minutes)}m"

    @rumps.timer(5)
    def update(self, _):
        if self.lat and self.long:
            self.display_next()
            self.calculate_remaining_time()
            self.title = f"🕌 {self.city.title()} | {self.display_next()} - {self.calculate_remaining_time()}"

            times = self.calculate_remaining_time()
            if times == "0h 0m" and not self.notified:
                self.title = f"🕌 {self.city.title()} | {self.display_next()} - {self.calculate_remaining_time()}"
                rumps.notification(title="Prayer", subtitle="",
                                   message=f"Time to Pray: {next_prayers(self.lat, self.long)[0]}")
                self.notified = True
            else:
                self.notified = False

if __name__ == "__main__":
    app = PrayerMenuBar()
    app.run()
