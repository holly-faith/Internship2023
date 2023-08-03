import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QDoubleSpinBox, QPushButton, QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QRadioButton
from pylablib.devices import Thorlabs
import time

print('Loading...')

#conn = {"port":"/dev/ttyUSB0","baudrate":115200,"rtscts":True}
#stage = Thorlabs.KinesisPiezoMotor(("serial",conn))

acc = 0.0
sr = 0.0
ss = 0.0
contmode = 'continuous' # may need to be cont=1 step=2
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Kinesis Piezomotor Control")

        
        self.Acceleration = QDoubleSpinBox()
        
        
        self.StepRate = QDoubleSpinBox()
         
        
        self.StepSize = QDoubleSpinBox()
        
        
        self.Resetbtn = QPushButton('Reset')
        
        
        self.StartStopbtn = QPushButton('Start')
        
        
        self.Continuousbtn = QRadioButton('Continuous')
        self.Continuousbtn.setChecked(True)
        
        
        self.SingleStepbtn = QRadioButton('Single Step')
        
        
        
        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()
        
        layout2.addWidget(QLabel('Set Acceleration:'))
        layout2.addWidget(self.Acceleration)
        self.Acceleration.textChanged.connect(self.SetAcceleration) # takes value from input (?)
        
        layout2.addWidget(QLabel('Set Step Rate:'))
        layout2.addWidget(self.StepRate)
        self.StepRate.textChanged.connect(self.SetStepRate)
        
        layout2.addWidget(QLabel('Set Step Size:'))
        layout2.addWidget(self.StepSize)
        self.StepSize.textChanged.connect(self.SetStepSize)
        
        layout1.addLayout(layout2)
        
        layout3.addWidget(QLabel('Set Mode:'))
        layout3.addWidget(self.Continuousbtn)
        self.Continuousbtn.setChecked(True)
        self.Continuousbtn.toggled.connect(self.SetMode)
        layout3.addWidget(self.SingleStepbtn)
        self.SingleStepbtn.toggled.connect(self.SetMode)
        
        layout3.addWidget(self.Resetbtn)
        self.Resetbtn.clicked.connect(self.Reset) # define - go all way to edge
        
        layout3.addWidget(self.StartStopbtn)
        self.StartStopbtn.setCheckable(True)
        
        
        
        self.StartStopbtn.clicked.connect(self.StartStop) # define - start motion, switch to stop button, when clicked, stops motion.
        
        
        
        layout1.addLayout(layout3)
        
        
        
        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)
         
 
    
    """
GET PARAMETERS FROM INPUTS
    """    
    def SetAcceleration(self):
        global acc # set global variable or can't be used outside of this function!!
        acc = self.Acceleration.value()
        # Pop up error if outside limits 1-100,000 []
        
    def SetStepRate(self):
        global sr
        sr = self.StepRate.value()
        # pop up error if outside limits 1-2,000 []
        
    def SetStepSize(self):
        global ss
        ss = self.StepSize.value()
        # pop up error if outside limits 1-1,000,000 []
        
    def SetMode(self):
        global contmode
        if self.Continuousbtn.isChecked():
            contmode = 'continuous'
        else:
            contmode = 'step' # might not be right (?)
        
    
    
    
    """
START/STOP BUTTON FUNCTIONS
    """   
     
    def StartStop(self):
        if self.StartStopbtn.isChecked():
            self.Start()
            
        else:
            self.Stop()
            
                  
    def Start(self):
        print('start')
        print('Acceleration: ' + str(acc))
        print('Step Rate: ' + str(sr))
        print('Step Size: ' + str(ss))
        print('Continuous: ' + str(contmode))
        self.StartStopbtn.setText('Stop')
        
        print('Connecting device...')
        stage.open()
        # may need to enable channel 1
        
        stage.setup_jog(mode=contmode, step_size_bk=ss, velocity=sr, acceleration=acc,channel=1) # mode=None as default (?)
        print('Device connected')
        print('Current parameters: ' + str(stage.get_jog_parameters()))
        print('Starting jog...')
        stage.jog(direction=='-',kind=='builtin') # may need to remove direction and kind (?)
        # when it reaches the end I assume it will automatically stop (?) may throw up error
        
        
        
            
        # change text to stop [DONE]
        # get imput parameters [DONE]
        # read off mode [DONE]
        # start movement acc to input parameters (MOVE BACKWARDS) [TEST]
        
        
    def Stop(self):
        print('stop')
        self.StartStopbtn.setText('Start')
        
        stage.stop() # may have to put channel 1
        
        # change text to start [DONE]
        # stop movement [TEST]
        
        
        
    """
    RESET BUTTON FUNCTION
    """
    
    def Reset(self):
        stage.setup_jog(mode='continuous', step_size_fw=500, velocity=2000, acceleration=100000,channel=1)
        while stage.get_position(channel=1) <500: # idk what number this would be, needs to be quite far positive to be able to move backwards 
            stage.jog(direction='+',kind=='builtin')
            
            # move stage all the way to before max positive value (if driven to end stops, can get jammed) [TEST]
        
        
        
        
            
app = QApplication(sys.argv)
window = MainWindow()
window.show()
print('Initialised')

app.exec()
stage.close()

        
        

