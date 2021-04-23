
from PyQt5.QtWidgets import QApplication,QLabel,QTextEdit,QComboBox, QWidget,QVBoxLayout ,QHBoxLayout, QPushButton, QLCDNumber, QSlider
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pyduino import *

class Hour():
    def __init__(self, hour, minute):
        self.hour = hour
        self.minute = minute

class HourCombo:

    def __init__(self, label):
        super().__init__()
        self.hours = QComboBox()
        self.minutes = QComboBox()
        self.label = QLabel(label)
        self.layout = QVBoxLayout()
        self.HLayout = QHBoxLayout()
        for i in range(0,24):
            self.hours.addItem(str(i))
        for i in range(0,60):
            self.minutes.addItem(str(i))
        #Gestion Style du layout
       
       
        
        #Gestion des layouts
        self.layout.addWidget(self.label)
        self.HLayout.addWidget(self.hours)
        self.HLayout.addWidget(self.minutes)
        self.layout.addLayout(self.HLayout)


class ComposantUI:

    def __init__(self,name,pin):
        self.visible = True
        self.defaultHourStart = Hour(6,0)
        self.defaultHourEnd = Hour(22,0)
        self.pin = pin

        self.startHour = HourCombo("Heure d'allumage")
        self.endHour = HourCombo("Heure de coupure")
        
        
        self.buttonValidate = QPushButton("Valider")
        self.buttonDefault = QPushButton("Default")
       

        self.label = QLabel(name)
        self.layout= QHBoxLayout()
        hoursLayout = QVBoxLayout()

        buttonLayout = QVBoxLayout()
        hoursLayout.addLayout(self.startHour.layout)
        hoursLayout.addLayout(self.endHour.layout)
        buttonLayout.addWidget(self.buttonValidate)
        buttonLayout.addWidget(self.buttonDefault)

        self.layout.addWidget(self.label)
        self.layout.addLayout(hoursLayout)
        self.layout.addLayout(buttonLayout)

    

    def blockButton(self):
        self.buttonDefault.setEnabled(False)
        self.buttonValidate.setEnabled(False)


    def unblockButton(self):
        self.buttonDefault.setEnabled(True)
        self.buttonValidate.setEnabled(True)

    def getComboBoxStartHour(self):
        return self.startHour.hours.currentIndex()

    def getComboBoxStartMinute(self):
        return self.startHour.minutes.currentIndex()

    def getComboBoxEndHour(self):
        return self.endHour.hours.currentIndex()

    def getComboBoxEndMinute(self):
        return self.endHour.minutes.currentIndex()

    def hide(self):
        
        self.label.hide()
        self.buttonDefault.hide()
        self.buttonValidate.hide()
        self.startHour.hours.hide()
        self.startHour.minutes.hide()
        self.endHour.hours.hide()
        self.endHour.minutes.hide()
        self.endHour.label.hide()
        self.startHour.label.hide()
        self.visible = False
    def show(self):
        
        self.label.show() 
        self.buttonDefault.show()
        self.buttonValidate.show()
        self.startHour.hours.show()
        self.startHour.minutes.show()
        self.endHour.hours.show()
        self.endHour.minutes.show()
        self.endHour.label.show()
        self.startHour.label.show()
        self.visible = True





        
