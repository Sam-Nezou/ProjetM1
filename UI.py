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
        """
        Initialise l'objet App
        """
        super().__init__()
        self.title = 'Réacteur à microalgues'
        self.left = 10
        self.top = 10
        self.width = 1000
        self.height = 600
        self.temp = Value("d", 0.0)
        self.ph = Value("d", 0.0)
        self.ntu = Value("d", 0.0)
        self.runProcess = Value("b",True)
        self.i = 0
        #self.connectArduino()
        self.initUI()
        self.initProcess()
        self.initTimer()
    

    def initTimer(self):
        """
        Initialise le QTimer
        """
         # make QTimer
        self.qTimer = QTimer()
        # set interval to 1 s
        self.qTimer.setInterval(1000) # 1000 ms = 1 s
        # connect timeout signal to signal handler
        self.qTimer.timeout.connect(self.updateGui)
        # start timer
        self.qTimer.start()

    
    def initProcess(self):
        """
        Fonction qui initialise le process
        """
        self.procGetValue = Process(target=self.procGetValue,args=[self.temp,self.ph,self.ntu])
        self.procGetValue.start()


    def killProcess(self):
        """
        Fonction qui supprime les process
        """
        self.procGetValue.terminate()
        self.procGetValue.join()

    def connectArduino(self):
        """
        Fonction de connexion à la carte 
        """
         
        print ('Establishing connection to Arduino...')
        
        # if your arduino was running on a serial port other than '/dev/ttyACM0/'
        # declare: a = Arduino(serial_port='/dev/ttyXXXX')
        self.a = Arduino()
        if self.a.error == 2:
            sys.exit(0)
        # sleep to ensure ample time for computer to make serial connection 
        time.sleep(5)
        print ('established!')
        # allow time to make connection
        time.sleep(1)


    def initButton(self):
        """
        Initialie les boutons des différents composants
        """
        
        #AJOUT DES FONCTION ASSOCIÉ AUX BOUTONS
        self.bulleurUI.buttonDefault.clicked.connect(lambda: self.setDefault(self.bulleurUI))
        self.bulleurUI.buttonValidate.clicked.connect(lambda: self.setHour(self.bulleurUI))
        self.bulleurUI.validatePeriod.clicked.connect(lambda: self.setAltern(self.bulleurUI))
        self.ledUI.buttonDefault.clicked.connect(lambda: self.setDefault(self.ledUI))
        self.ledUI.buttonValidate.clicked.connect(lambda: self.setHour(self.ledUI))
        self.cableChauffantUI.buttonDefault.clicked.connect(lambda: self.setDefault(self.cableChauffantUI))
        self.cableChauffantUI.buttonValidate.clicked.connect(lambda: self.setHour(self.cableChauffantUI))

    def graphLayout(self, graph, label):
        """
        Retourne un layout horizontale contenant un graphique et la valeur lié a celui ci
        """
        layout = QVBoxLayout()
        layout.addWidget(graph)
        layout.addWidget(label)

        return layout



    def initGraph(self):
        """
        Initialise la partie des graphiques sur l'interface
        Return : QHBoxLayout
        """
        self.tempLabel = QLabel("Température : " + str(self.temp.value) + "°C")
        self.phLabel = QLabel("Ph : " + str(self.ph.value) )
        self.ntuLabel = QLabel("Turbidité : " + str(self.ntu.value) + " NTU ")



        self.graphTemp = MplCanvas(self)
        self.graphPh = MplCanvas(self)
        self.graphNtu = MplCanvas(self)

        self.graphTemp.setLabel("Temps en seconde","Température en °C")
        self.graphPh.setLabel("Temps en seconde","Ph")
        self.graphNtu.setLabel("Temps en seconde","NTU")

        graphLayout = QHBoxLayout()

        graphLayout.addLayout(self.graphLayout(self.graphTemp,self.tempLabel))
        graphLayout.addLayout(self.graphLayout(self.graphPh,self.phLabel))
        graphLayout.addLayout(self.graphLayout(self.graphNtu,self.ntuLabel))

        return graphLayout


    def initUI(self):
        """
        Initialise l'interface de l'IHM
        """
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
       
        #INITIALISATION DES COMPOSANTS
       	self.bulleurUI = BulleurUI("Bulleur",46)
        self.ledUI = ComposantUI("Bandeau de Led",44)
        self.cableChauffantUI = ComposantUI("Câble chauffant",42)
       	
        #Cache l'interface des comosants
        self.bulleurUI.hide()
        self.ledUI.hide()
        self.cableChauffantUI.hide()



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
       
        self.initButton()

        graphLayout = self.initGraph()
        layout  = QVBoxLayout()

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
        """
        Affiche sur l'inerface la parti du bulleur
        """

        self.bulleurUI.show()
        self.cableChauffantUI.hide()
        self.ledUI.hide()

    @pyqtSlot()
    def afficheLed(self):
        """
        Affiche sur l'inerface la parti de la LED
        """

        self.bulleurUI.hide()
        self.cableChauffantUI.hide()
        self.ledUI.show()

    @pyqtSlot()
    def afficheCable(self):
        """
        Affiche sur l'inerface la parti du cable chauffant
        """
        self.bulleurUI.hide()
        self.cableChauffantUI.show()
        self.ledUI.hide()



    @pyqtSlot()
    def setDefault(self, composant):
        """
        Cette fonction envoie une requête à la carte avec les valeurs des heure d'allumage et de coupure par défaut du composant 

        """
        self.blockButton()
        self.runProcess.value = False
        time.sleep(5)
        self.a.send_command('CS',composant.pin,composant.defaultHourStart.hour,composant.defaultHourStart.minute)
        time.sleep(1)
        self.a.send_command('CE',composant.pin,composant.defaultHourEnd.hour,composant.defaultHourEnd.minute)
        time.sleep(3)
        self.runProcess.value = True
        self.unblockButton()
    
    @pyqtSlot()
    def setHour(self, composant):
        """
        Cette fonction envoie une requête à la carte avec les valeurs des heure d'allumage et de coupure  

        """
        self.blockButton()
        self.runProcess.value = False
        time.sleep(5)
        self.a.send_command('CS',composant.pin,composant.getComboBoxStartHour(),composant.getComboBoxStartMinute())
        time.sleep(1)
        self.a.send_command('CE',composant.pin,composant.getComboBoxEndHour(),composant.getComboBoxEndMinute())
        time.sleep(3)
        self.runProcess.value = True
        self.unblockButton()
        

    @pyqtSlot()
    def setAltern(self, composant):
        """
        Fonction qui envoie les valeurs pour l'aternance du bulleur
        """
        self.blockButton()
        self.runProcess.value = False
        time.sleep(5)
        self.a.send_command('BB',composant.pin,composant.getComboBoxOnTime(),composant.getComboBoxOffTime())
        time.sleep(1)
        self.runProcess.value = True
        self.unblockButton()

    @pyqtSlot()
    def procGetValue(self,temp,ph,ntu):
        """
        Process qui permet de récupérer les valeurs de la température, du ph et de la turbidité
        """

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
        
    def blockButton(self):
        """
        Bloque l'utilisation des boutons
        """
        self.bulleurUI.blockButton()
        self.cableChauffantUI.blockButton()
        self.ledUI.blockButton()
   
    def unblockButton(self):
        """
        Débloque les bouttons
        """
        self.bulleurUI.unblockButton()
        self.cableChauffantUI.unblockButton()
        self.ledUI.unblockButton()
   #----------------------------------------------------------------------------#



if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = App()

    sys.exit(app.exec_())
    ex.killProcess()

