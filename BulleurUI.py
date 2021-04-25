from ComposantUI import *


class BulleurUI(ComposantUI):
    def __init__(self,name,pin):
        
        ComposantUI.__init__(self,name,pin)

        self.onLabel= QLabel("période allumé (min)")
        self.offLabel= QLabel("période éteint (min)")
        self.onTimeCombo = QComboBox()
        self.offTimeCombo = QComboBox()
        self.validatePeriod = QPushButton("Valider")
        for i in range(0,60):
            self.onTimeCombo.addItem(str(i))
            self.offTimeCombo.addItem(str(i))
        pVLayout = QVBoxLayout()
        onLayout = QHBoxLayout()
        offLayout = QHBoxLayout()
        onLayout.addWidget(self.onLabel,stretch=1)
        onLayout.addWidget(self.onTimeCombo,stretch=1)
        offLayout.addWidget(self.offLabel,stretch=1)
        offLayout.addWidget(self.offTimeCombo,stretch=1)
        pVLayout.addLayout(onLayout)
        pVLayout.addLayout(offLayout)
        pVLayout.addWidget(self.validatePeriod)
        self.layout.addLayout(pVLayout)
        self.hide()

    def blockButton(self):
        """
        Bloque l'utilisation des boutons du composant
        """

        ComposantUI.blockButton(self)
        self.validatePeriod.setEnabled(False)

    def unblockButton(self):
        """
        Débloque l'utilisation des boutons
        """
        ComposantUI.unblockButton(self)
        self.validatePeriod.setEnabled(True)

    def hide(self):
        """
        Cache tous les widgets
        """
        
        self.onLabel.hide()
        self.offLabel.hide()
        self.offTimeCombo.hide()
        self.onTimeCombo.hide()
        self.validatePeriod.hide()
        ComposantUI.hide(self)

    def show(self): 
        """
        Affiche tous les widgets
        """
        self.onLabel.show()
        self.offLabel.show()
        self.offTimeCombo.show()
        self.onTimeCombo.show()
        self.validatePeriod.show()
        ComposantUI.show(self)

    def getComboBoxOnTime(self):
        return self.onTimeCombo.currentIndex()
    
    def getComboBoxOffTime(self):
        return self.offTimeCombo.currentIndex()


