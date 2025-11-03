
import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon # icon
from PyQt5. QtGui import QFont, QFontDatabase
from PyQt5.QtCore import QTime, Qt, QTimer
from datetime import datetime, timedelta
from config import API_KEY


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.api_key = API_KEY
        self.zone = "America/Vancouver"
        self.formatted_time = None
        self.timezone_code = None
        self.last_update = None

        # The label
        self.time_zone = QLabel("Loading..", self)
        self.time_zone.setAlignment(Qt.AlignCenter)
        self.time_zone.setStyleSheet("""
            font-size: 50px;
            color: hsl(49, 98%, 49%);
            font-weight: bold;
            """)
        # fonts
        font_id = QFontDatabase.addApplicationFont("Good Times Rg.otf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        my_font = QFont(font_family, 50)
        self.time_zone.setFont(my_font)

        # Centering label as widget
        self.setCentralWidget(self.time_zone)
        # Window setup
        self.setWindowTitle("Time Zone")
        self.setWindowIcon(QIcon("clock_icon.svg"))
        self.setGeometry(1800, 100, 400, 150)
        self.setStyleSheet("background-color: black")

        # locally refresh every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_display)
        self.timer.start(1000)

        # refresh from API every 10 minutes
        self.api_timer = QTimer()
        self.api_timer.timeout.connect(self.get_time_from_api)
        self.api_timer.start(600000) # 10 minute refresh


        self.get_time_from_api()

    def get_time_from_api(self):
        # Some API shenanigans
        try:
            url = f"http://api.timezonedb.com/v2.1/get-time-zone?key={self.api_key}&format=json&by=zone&zone={self.zone}"
            response = requests.get(url,timeout=5)
            response.raise_for_status()
            data = response.json()

            self.formatted_time = datetime.strptime(data["formatted"], "%Y-%m-%d %H:%M:%S")
            self.timezone_code = data["abbreviation"]
            self.last_update = datetime.now()
        except Exception as e:
            print(f"Error fetching time: {e}")

    def update_display(self):
        if self.formatted_time and self.last_update:
            seconds_since_update = (datetime.now() - self.last_update).total_seconds()
            current_time = self.formatted_time + timedelta(seconds=seconds_since_update)
            now = current_time.strftime("%I:%M %p") # removed seconds (:%S)
            self.time_zone.setText(f"{self.timezone_code} {now}") #\n{self.zone}
            #print("Tick:", datetime.now())


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show() #showing the window.
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()