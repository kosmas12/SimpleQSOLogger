from PySide2.QtWidgets import *
import sqlite3
from datetime import datetime
import pytz

UTC = pytz.utc
userCallsign = input("Enter your callsign: ")
mode = None
band = None

modes = ["DIGITALVOICE", "FT4", "FT8", "CW", "AM", "FM", "RTTY", "SSB"]
bands = ["80m", "40m", "20m", "10m", "5m", "2m", "1m", "70cm"]

class LoggerWindow(QWidget):
    def __init__(self, parent=None):
        super(LoggerWindow, self).__init__(parent) # Start LoggerWindow
        self.name = QLineEdit("Name")
        self.callsign = QLineEdit("Callsign")
        self.qth = QLineEdit("QTH")
        self.modesLabel = QLabel("<font color=gray size = 5>Modes</font>")
        self.btnDigital = QRadioButton("DIGITAL VOICE")
        self.btnFT4 = QRadioButton("FT4")
        self.btnFT8 = QRadioButton("FT8")
        self.btnCW = QRadioButton("CW")
        self.btnAM = QRadioButton("AM")
        self.btnFM = QRadioButton("FM")
        self.btnRTTY = QRadioButton("RTTY")
        self.btnSSB = QRadioButton("SSB")
        self.bandsLabel = QLabel("<font color=gray size = 5>Bands</font>")
        self.btn80m = QRadioButton("80m")
        self.btn40m = QRadioButton("40m")
        self.btn20m = QRadioButton("20m")
        self.btn10m = QRadioButton("10m")
        self.btn5m = QRadioButton("5m")
        self.btn2m = QRadioButton("2m")
        self.btn1m = QRadioButton("1m")
        self.btn70cm = QRadioButton("70cm")
        self.btnStime = QPushButton("Click to log start time")
        self.btnEtime = QPushButton("Click to log end time")
        self.btnSubmit = QPushButton("Log to database (" + userCallsign + ".db)")
        self.Layout = QVBoxLayout()
        self.setLayout(self.Layout) # Set the layout of LoggerWindow
        self.btnSubmit.clicked.connect(self.log) # Connect btnSubmit on self to the log function on self
        self.btnStime.clicked.connect(self.getStartTime)
        self.btnEtime.clicked.connect(self.getEndTime)
        self.addWidgets()
        self.groupModeButtons()
        self.groupBandButtons()
        
    def addWidgets(self):
        # Add everything to the window
        self.Layout.addWidget(self.name)
        self.Layout.addWidget(self.callsign)
        self.Layout.addWidget(self.qth)
        self.Layout.addWidget(self.modesLabel)
        self.Layout.addWidget(self.btnDigital)
        self.Layout.addWidget(self.btnFT4)
        self.Layout.addWidget(self.btnFT8)
        self.Layout.addWidget(self.btnCW)
        self.Layout.addWidget(self.btnAM)
        self.Layout.addWidget(self.btnFM)
        self.Layout.addWidget(self.btnRTTY)
        self.Layout.addWidget(self.btnSSB)
        self.Layout.addWidget(self.bandsLabel)
        self.Layout.addWidget(self.btn80m)
        self.Layout.addWidget(self.btn40m)
        self.Layout.addWidget(self.btn20m)
        self.Layout.addWidget(self.btn10m)
        self.Layout.addWidget(self.btn5m)
        self.Layout.addWidget(self.btn2m)
        self.Layout.addWidget(self.btn1m)
        self.Layout.addWidget(self.btn70cm)
        self.Layout.addWidget(self.btnStime)
        self.Layout.addWidget(self.btnEtime)
        self.Layout.addWidget(self.btnSubmit)
        
    def groupBandButtons(self):
        self.bandButtonGroup = QButtonGroup()
        self.bandButtonGroup.addButton(self.btn80m, 0)
        self.bandButtonGroup.addButton(self.btn40m, 1)
        self.bandButtonGroup.addButton(self.btn20m, 2)
        self.bandButtonGroup.addButton(self.btn10m, 3)
        self.bandButtonGroup.addButton(self.btn5m, 4)
        self.bandButtonGroup.addButton(self.btn2m, 5)
        self.bandButtonGroup.addButton(self.btn1m, 6)
        self.bandButtonGroup.addButton(self.btn70cm, 7)
        
        
    def groupModeButtons(self):
        self.modeButtonGroup = QButtonGroup()
        self.modeButtonGroup.addButton(self.btnDigital, 0)
        self.modeButtonGroup.addButton(self.btnFT4, 1)
        self.modeButtonGroup.addButton(self.btnFT8, 2)
        self.modeButtonGroup.addButton(self.btnCW, 3)
        self.modeButtonGroup.addButton(self.btnAM, 4)
        self.modeButtonGroup.addButton(self.btnFM, 5)
        self.modeButtonGroup.addButton(self.btnRTTY, 6)
        self.modeButtonGroup.addButton(self.btnSSB, 7)

    def getStartTime(self):
        self.Sdatetime = datetime.now(UTC)
        self.Sdatetime = self.Sdatetime.strftime("%B %d, %Y, %H:%M:%S")
        
    def getEndTime(self):
        self.Edatetime = datetime.now(UTC)
        self.Edatetime = self.Edatetime.strftime("%B %d, %Y, %H:%M:%S")

    def log(self):
        db = sqlite3.connect(userCallsign + ".db") # Connect with the database
        c = db.cursor() # Start DB cursor
        c.execute("CREATE TABLE IF NOT EXISTS contact (Name, Callsign, QTH, Mode, Band, Start_Time, End_Time)") # Make the data table
        selectedModeButtonID = self.modeButtonGroup.checkedId()
        mode = modes[selectedModeButtonID]
        selectedBandButtonID = self.bandButtonGroup.checkedId()
        band = bands[selectedBandButtonID]

        contact = [(self.name.text()),
                 (self.callsign.text()),
                 (self.qth.text()),
                 (mode),
                 (band),
                 (self.Sdatetime),
                 (self.Edatetime),]

        c.executemany("INSERT INTO contact (Name, Callsign, QTH, Mode, Band, Start_Time, End_Time) VALUES (?, ?, ?, ?, ?, ?, ?)", [contact]) # Write the data to the table
        db.commit() # Save to disk
        db.close()
        self.destroy(1, 1) # Delete LoggerWindow and all subwindows
        self.show()

app = QApplication([]) # Start the app

window = LoggerWindow() # Make the LoggerWindow
window.show() # Show LoggerWindow

app.exec_() # Run the app
