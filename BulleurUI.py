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

    def hide(self):
    
        self.onLabel.hide()
        self.offLabel.hide()
        self.offTimeCombo.hide()
        self.onTimeCombo.hide()
        self.validatePeriod.hide()
        ComposantUI.hide(self)

    def show(self): 
    
        self.onLabel.show()
        self.offLabel.show()
        self.offTimeCombo.show()
        self.onTimeCombo.show()
        self.validatePeriod.show()
        ComposantUI.show(self)

    def getComboBoxOnTime(self):
        print(self.onTimeCombo.currentIndex())

        return self.onTimeCombo.currentIndex()
    
    def getComboBoxOffTime(self):
        print(self.offTimeCombo.currentIndex())

        return self.offTimeCombo.currentIndex()


