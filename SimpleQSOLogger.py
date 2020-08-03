from PySide2.QtWidgets import *
import sqlite3
from datetime import datetime
import pytz

UTC = pytz.utc
userCallsign = input("Enter your callsign: ")
mode = None

modes = ["DIGITALVOICE", "FT4", "FT8", "CW", "AM", "FM", "RTTY", "SSB"]

class LoggerWindow(QWidget):
    def __init__(self, parent=None):
        super(LoggerWindow, self).__init__(parent) # Start LoggerWindow
        self.name = QLineEdit("Name")
        self.callsign = QLineEdit("Callsign")
        self.btnDigital = QRadioButton("DIGITAL VOICE")
        self.btnFT4 = QRadioButton("FT4")
        self.btnFT8 = QRadioButton("FT8")
        self.btnCW = QRadioButton("CW")
        self.btnAM = QRadioButton("AM")
        self.btnFM = QRadioButton("FM")
        self.btnRTTY = QRadioButton("RTTY")
        self.btnSSB = QRadioButton("SSB")
        self.btnStime = QPushButton("Click to log start time")
        self.btnEtime = QPushButton("Click to log end time")
        self.btnSubmit = QPushButton("Log to database (" + userCallsign + ".db)")
        self.Layout = QVBoxLayout()
        self.setLayout(self.Layout) # Set the layout of LoggerWindow
        self.btnSubmit.clicked.connect(self.log) # Connect btnSubmit on self to the log function on self
        self.btnStime.clicked.connect(self.getStartTime)
        self.btnEtime.clicked.connect(self.getEndTime)
        self.addWidgets()
        self.groupButtons()
        
    def addWidgets(self):
        # Add everything to the window
        self.Layout.addWidget(self.name)
        self.Layout.addWidget(self.callsign)
        self.Layout.addWidget(self.btnDigital)
        self.Layout.addWidget(self.btnFT4)
        self.Layout.addWidget(self.btnFT8)
        self.Layout.addWidget(self.btnCW)
        self.Layout.addWidget(self.btnAM)
        self.Layout.addWidget(self.btnFM)
        self.Layout.addWidget(self.btnRTTY)
        self.Layout.addWidget(self.btnSSB)
        self.Layout.addWidget(self.btnStime)
        self.Layout.addWidget(self.btnEtime)
        self.Layout.addWidget(self.btnSubmit)
        
    def groupButtons(self):
        self.buttonGroup = QButtonGroup()
        self.buttonGroup.addButton(self.btnDigital, 0)
        self.buttonGroup.addButton(self.btnFT4, 1)
        self.buttonGroup.addButton(self.btnFT8, 2)
        self.buttonGroup.addButton(self.btnCW, 3)
        self.buttonGroup.addButton(self.btnAM, 4)
        self.buttonGroup.addButton(self.btnFM, 5)
        self.buttonGroup.addButton(self.btnRTTY, 6)
        self.buttonGroup.addButton(self.btnSSB, 7)

    def getStartTime(self):
        self.Sdatetime = datetime.now(UTC)
        self.Sdatetime = self.Sdatetime.strftime("%B %d, %Y, %H:%M:%S")
        
    def getEndTime(self):
        self.Edatetime = datetime.now(UTC)
        self.Edatetime = self.Edatetime.strftime("%B %d, %Y, %H:%M:%S")

    def log(self):
        db = sqlite3.connect(userCallsign + ".db") # Connect with the database
        c = db.cursor() # Start DB cursor
        c.execute("CREATE TABLE IF NOT EXISTS contact (name, callsign, mode, Start_time, End_time)") # Make the data table
        selectedButtonID = self.buttonGroup.checkedId()
        mode = modes[selectedButtonID]

        contact = [(self.name.text()),
                 (self.callsign.text()),
                 (mode),
                 (self.Sdatetime),
                 (self.Edatetime),]

        c.executemany("INSERT INTO contact (name, callsign, mode, Start_time, End_time) VALUES (?, ?, ?, ?, ?)", [contact]) # Write the data to the table
        db.commit() # Save to disk
        db.close()
        self.destroy(1, 1) # Delete LoggerWindow and all subwindows
        self.show()

app = QApplication([]) # Start the app

window = LoggerWindow() # Make the LoggerWindow
window.show() # Show LoggerWindow

app.exec_() # Run the app
