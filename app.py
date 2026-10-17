import rumps
import threading
import datetime
from main import next_prayers, prayer_times, get_coordinates

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
        self.timings = None  # cache prayer times

    @rumps.clicked("Set Location")
    def set_location(self, _):
        resp = rumps.Window("Enter your Location (city, country): ", dimensions=(200, 47), cancel=True).run()
        if resp._clicked == 0:
            return
        txt = resp._text
        self.city = txt.split(",")[0].strip()
        self.country = txt.split(",")[1].strip()
        threading.Thread(target=self._load_location, daemon=True).start()

    @rumps.clicked("Change Location")
    def change_location(self, _):
        resp = rumps.Window("Enter your Location (city, country): ", dimensions=(200, 47), cancel=True).run()
        if resp._clicked == 0:
            return
        txt = resp._text
        self.city = txt.split(",")[0].strip()
        self.country = txt.split(",")[1].strip()
        threading.Thread(target=self._load_location, daemon=True).start()

    def _load_location(self):
        # runs in background — safe to make network calls here
        self.lat, self.long = get_coordinates(self.city, self.country)
        self.timings = prayer_times(self.lat, self.long)  # fetch once, cache it
        self.icon = None
        self.display()
        self._refresh_title()

    def display(self):
        self.menu.clear()
        self.menu.add(rumps.MenuItem("Set Location", callback=self.set_location))
        self.menu.add(rumps.MenuItem("Change Location", callback=self.change_location))
        self.menu.add(rumps.separator)
        if self.timings:
            for prayer, time in self.timings.items():
                self.menu.add(rumps.MenuItem(title=f"{prayer}: {time[0]}", callback=lambda _: None))
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem("Quit", callback=rumps.quit_application))

    def _refresh_title(self):
        # uses cached timings — no network call
        if not self.timings:
            return
        next_prayer, next_time = next_prayers(self.lat, self.long)
        remaining = self.calculate_remaining_time(next_time)
        self.title = f"🕌 {self.city.title()} | {next_prayer}: {next_time} - {remaining}"

        if remaining == "0h 0m" and not self.notified:
            rumps.notification(title="Prayer", subtitle="",
                               message=f"Time to Pray: {next_prayer}")
            self.notified = True
        else:
            self.notified = False

    def calculate_remaining_time(self, next_time_str):
        times = datetime.datetime.strptime(next_time_str, "%H:%M").time()
        today = datetime.date.today()
        dt_prayer = datetime.datetime.combine(today, times)
        dt_now = datetime.datetime.now()
        elapsed = dt_prayer - dt_now
        hours = elapsed.seconds // 3600
        minutes = (elapsed.seconds % 3600) // 60
        return f"{hours}h {minutes}m"

    @rumps.timer(60)  # changed from 5 to 60
    def update(self, _):
        if self.lat and self.long:
            # refresh cached timings in background once per minute
            threading.Thread(target=self._refresh_timings, daemon=True).start()

    def _refresh_timings(self):
        self.timings = prayer_times(self.lat, self.long)
        self._refresh_title()

if __name__ == "__main__":
    app = PrayerMenuBar()
    app.run()
