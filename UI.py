#!/usr/bin/env python

import time
import sys
import multiprocessing
from pyduino import *
from multiprocessing import *
from ComposantUI import *
from BulleurUI import *
from PyQt5 import *
from matplot import * 



class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Réacteur à microalgues'
        self.left = 10
        self.top = 10
        self.width = 500
        self.height = 500
        self.temp = Value("d", 0.0)
        self.ph = Value("d", 0.0)
        self.ntu = Value("d", 0.0)
        self.runProcess = Value("b",True)
        self.i = 0
        self.connectArduino()
        self.initUI()
        self.initProcess()
        self.initTimer()
    
    def closeEvent(self, event):
        self.killProcess()

    def __del__(self):
       self.killProcess()
       

    def initTimer(self):
         # make QTimer
        self.qTimer = QTimer()
        # set interval to 1 s
        self.qTimer.setInterval(1000) # 1000 ms = 1 s
        # connect timeout signal to signal handler
        self.qTimer.timeout.connect(self.updateGui)
        # start timer
        self.qTimer.start()

    
    def initProcess(self):
        self.procGetValue = Process(target=self.procGetValue,args=[self.temp,self.ph,self.ntu])
        self.procGetValue.start()


    def killProcess(self):
        self.procGetValue.terminate()
        self.procGetValue.join()

    def connectArduino(self):
         
        print ('Establishing connection to Arduino...')
        
        # if your arduino was running on a serial port other than '/dev/ttyACM0/'
        # declare: a = Arduino(serial_port='/dev/ttyXXXX')
        self.a = Arduino()
        # sleep to ensure ample time for computer to make serial connection 
        time.sleep(3)
        print ('established!')
        # allow time to make connection
        time.sleep(1)





    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
       
        #INITIALISATION DES COMPOSANTS
       	self.bulleurUI = BulleurUI("Bulleur",46)
        self.ledUI = ComposantUI("Bandeau de Led",44)
        self.cableChauffantUI = ComposantUI("Câble chauffant",42)
       	
        self.bulleurUI.hide()
        self.ledUI.hide()
        self.cableChauffantUI.hide()

        self.tempLabel = QLabel("Température : " + str(self.temp.value) + "°C")
        self.phLabel = QLabel("Ph : " + str(self.ph.value) )
        self.ntuLabel = QLabel("Turbidité : " + str(self.ntu.value) + " NTU ")


        buttonBulleur = QPushButton('Bulleur', self)
        buttonBulleur.clicked.connect(self.afficheBulleur)
        buttonLed = QPushButton('Led', self)
        buttonLed.clicked.connect(self.afficheLed)
        buttonCable = QPushButton('Cable', self)
        buttonCable.clicked.connect(self.afficheCable)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(buttonBulleur)
        buttonLayout.addWidget(buttonLed)
        buttonLayout.addWidget(buttonCable)
        #AJOUT DES FONCTION ASSOCIÉ AUX BOUTONS
        self.bulleurUI.buttonDefault.clicked.connect(lambda: self.setDefault(self.bulleurUI))
        self.bulleurUI.buttonValidate.clicked.connect(lambda: self.setHour(self.bulleurUI))
        self.bulleurUI.validatePeriod.clicked.connect(lambda: self.setAltern(self.bulleurUI))
        self.ledUI.buttonDefault.clicked.connect(lambda: self.setDefault(self.ledUI))
        self.ledUI.buttonValidate.clicked.connect(lambda: self.setHour(self.ledUI))
        self.cableChauffantUI.buttonDefault.clicked.connect(lambda: self.setDefault(self.cableChauffantUI))
        self.cableChauffantUI.buttonValidate.clicked.connect(lambda: self.setHour(self.cableChauffantUI))



        self.graphTemp = MplCanvas(self)
        self.graphPh = MplCanvas(self)
        self.graphNtu = MplCanvas(self)


        graphLayout = QHBoxLayout()
        self.graphTemp.setLabel("Temps en seconde","Température en °C")
        self.graphPh.setLabel("Temps en seconde","Ph")
        self.graphNtu.setLabel("Temps en seconde","NTU")
        graphLayout.addWidget(self.graphTemp)
        graphLayout.addWidget(self.graphPh)
        graphLayout.addWidget(self.graphNtu)




        layout  = QVBoxLayout()

        layout.addWidget(self.tempLabel)
        layout.addWidget(self.phLabel)
        layout.addWidget(self.ntuLabel)
        layout.addLayout(buttonLayout)
        layout.addLayout(graphLayout)

        layout.addLayout(self.bulleurUI.layout)
        layout.addLayout(self.ledUI.layout)
        layout.addLayout(self.cableChauffantUI.layout)
        


        #AJOUT DU LAYOUT A LA FENETRE
        self.setLayout(layout)

        self.show()


    #-------------------------------------------------------------------#
    #TOUTES LES FONCTIONS SUIVANTES ENVOIE UNE REQUÊTE À LA CARTE ARDUINO

    #FONCTION QUI MET À 1 UN PIN DIGITAL
    @pyqtSlot()
    def afficheBulleur(self):
        self.bulleurUI.show()
        self.cableChauffantUI.hide()
        self.ledUI.hide()

    @pyqtSlot()
    def afficheLed(self):
        self.bulleurUI.hide()
        self.cableChauffantUI.hide()
        self.ledUI.show()

    @pyqtSlot()
    def afficheCable(self):
        self.bulleurUI.hide()
        self.cableChauffantUI.show()
        self.ledUI.hide()


    #FONCTION QUI ENVOIE DEUX REQUÊTE POUR METTRE L'HEURE D'ALLUMAGE ET 
    #DE COUPURE DES COMPOSANTS AUX HEURES PAR DÉFAUTS
    @pyqtSlot()
    def setDefault(self, composant):
        self.runProcess.value = False
        time.sleep(5)
        self.a.send_command('CS',composant.pin,composant.defaultHourStart.hour,composant.defaultHourStart.minute)
        time.sleep(1)
        self.a.send_command('CE',composant.pin,composant.defaultHourEnd.hour,composant.defaultHourEnd.minute)
        time.sleep(3)
        self.runProcess.value = True
    
    @pyqtSlot()
    def setHour(self, composant):
        self.runProcess.value = False
        time.sleep(5)
        self.a.send_command('CS',composant.pin,composant.getComboBoxStartHour(),composant.getComboBoxStartMinute())
        time.sleep(1)
        self.a.send_command('CE',composant.pin,composant.getComboBoxEndHour(),composant.getComboBoxEndMinute())
        time.sleep(3)
        self.runProcess.value = True
        

    @pyqtSlot()
    def setAltern(self, composant):
        self.runProcess.value = False
        time.sleep(5)
        self.a.send_command('BB',composant.pin,composant.getComboBoxOnTime(),composant.getComboBoxOffTime())
        time.sleep(1)
        self.runProcess.value = True
        time.sleep(3)


    @pyqtSlot()
    def getHour(self):
        self.runProcess.value = False
        time.sleep(5)
        self.a.get_Hour()
        time.sleep(2)
        self.runProcess.value = True



    @pyqtSlot()
    def procGetValue(self,temp,ph,ntu):

        while True:

            if self.runProcess.value == True:
                time.sleep(1)

                temp.value = float(self.a.read_command(52,'GT','D'))
                ph.value = float(self.a.read_command(9,'GP','A'))
                ntu.value = float(self.a.read_command(8,'GN','A'))
                
            else:
                time.sleep(2)
         
            
    @pyqtSlot()
    def updateGui(self):
        """
        Fonction qui met à jour les valeurs affichées sur l'IHM

        """
        self.tempLabel.setText("Température : " +str(self.temp.value) + "°C")
        self.phLabel.setText("Ph : " +str(self.ph.value))
        self.ntuLabel.setText("Turbidité : " +str(self.ntu.value) + "NTU")
        self.i+=1
        self.graphTemp.addValue(self.temp.value,self.i)
        self.graphPh.addValue(self.ph.value,self.i)
        self.graphNtu.addValue(self.ntu.value,self.i)
        
   #----------------------------------------------------------------------------#



if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = App()

    sys.exit(app.exec_())
    ex.killProcess()

