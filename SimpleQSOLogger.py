from PySide2.QtWidgets import *
from PySide2.QtCore import Slot
import sqlite3
from datetime import datetime
import pytz

UTC = pytz.utc
userCallsign = input("Enter your callsign: ")
mode = None

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
        self.btnSubmit = QPushButton("Log to database (" + userCallsign + ".db)") # Φτιάξε κουμπί push
        self.Layout = QVBoxLayout() # Ξεκίνα το layout
        self.Layout.addWidget(self.name) # Βάλε όλα τα πλαίσια και κουμπιά που φτιάξαμε
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
        self.setLayout(self.Layout) # Όρισε το layout του LoggerWindow
        self.btnSubmit.clicked.connect(self.log) # Συνέδεσε το πατημένο κουμπί submit στο self με το function log στο self
        self.btnStime.clicked.connect(self.getStartTime)
        self.btnEtime.clicked.connect(self.getEndTime)

    def getStartTime(self):
        self.Sdatetime = datetime.now(UTC)
        self.Sdatetime = self.Sdatetime.strftime("%B %d, %Y, %H:%M:%S")
        
    def getEndTime(self):
        self.Edatetime = datetime.now(UTC)
        self.Edatetime = self.Edatetime.strftime("%B %d, %Y, %H:%M:%S")

    def log(self):
        db = sqlite3.connect(userCallsign + ".db") # Συνδέσου με τη βάση δεδομένων
        c = db.cursor() # Ξεκίνα το κέρσορα της βάσης δεδομένων
        c.execute("CREATE TABLE IF NOT EXISTS contact (name, callsign, mode, Start_time, End_time)") # Φτιάξε το "τραπέζι" δεδομένων contact άμα δεν υπάρχει, με δεδομένα name, callsign, mode
        if (self.btnDigital.isChecked()) :
            self.mode = "DIGITALVOICE"
        if (self.btnFT4.isChecked()): 
            self.mode = "FT4"
        if (self.btnFT8.isChecked()): 
            self.mode = "FT8"
        if (self.btnCW.isChecked()): 
            self.mode = "CW"
        if (self.btnAM.isChecked()): 
            self.mode = "AM"
        if (self.btnFM.isChecked()): 
            self.mode = "FM"
        if (self.btnRTTY.isChecked()): 
            self.mode = "RTTY"
        if (self.btnSSB.isChecked()): 
            self.mode = "SSB"

        contact = [(self.name.text()),
                 (self.callsign.text()),
                 (self.mode),
                 (self.Sdatetime),
                 (self.Edatetime),]

        c.executemany("INSERT INTO contact (name, callsign, mode, Start_time, End_time) VALUES (?, ?, ?, ?, ?)", [contact]) # Γράψε τα δεδομένα στο "τραπέζι"
        db.commit() # Αποθήκευσε στο δίσκο
        db.close() # Κλείσε τη σύνδεση με τη βάση δεδομένων
        self.destroy(1, 1) # Διέγραψε το LoggerWindow και όλα τα υποπαράθυρά του
        self.show() # Ξαναεμφανίσου

app = QApplication([]) # Ξεκινάμε την εφαρμογή

window = LoggerWindow() # Φτιάχνουμε το LoggerWindow
window.show() # Εμφάνισε το LoggerWindow

app.exec_() # Τρέξε την εφαρμογή
