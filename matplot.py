
import matplotlib

matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure



class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=7, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        self.tempArray = []
        self.timeArray = []
      
       


    def addValue(self,value,valueTime):
        """
        Ajoute des valeurs au tableau
        """
        self.tempArray.append(value)
        self.timeArray.append(valueTime)
        if (len(self.timeArray) ==300):
            self.timeArray.pop(0)
            self.tempArray.pop(0)
        self.axes.clear()
        self.setLabel(self.xLabel,self.yLabel)

        self.axes.plot(self.timeArray,self.tempArray, color ='red')
        self.axes.figure.canvas.draw()

    def setLabel(self, xLabel,yLabel):
        """
        Set les noms des axis
        """
        self.xLabel = xLabel
        self.yLabel = yLabel
        self.axes.set_xlabel(xLabel)
        self.axes.set_ylabel(yLabel)
        self.axes.set_title(yLabel)   
