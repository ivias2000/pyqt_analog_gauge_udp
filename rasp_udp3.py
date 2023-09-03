
# This is part 12 of the PyQt5 learning series
# Start and Stop Qthreads
# Source code available: www.pyshine.com
from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5 import uic
import sys, time
import signal
import socket
import numpy as np
from numpy import pi,cos,sin,tan
import pyqtgraph as pg
import csv
import time
#from PySide2 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QBrush, QColor, QPalette
from PyQt5.QtWidgets import QApplication, qApp
from PyQt5.QtCore import Qt
from analoggaugewidget import AnalogGaugeWidget
global array_data


class THREADS_APP(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        #self.ui = uic.loadUi('adadxyz2.ui',self)
        
        #self.resize(950, 800)
        #icon = QtGui.QIcon()
        #icon.addPixmap(QtGui.QPixmap("PyShine.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #self.setWindowIcon(icon)
        self.ui = uic.loadUi('analoggaugewidget_demo3.ui',self)
        self.curve = self.graphicsView.plot(pen='y')
        a_data = np.zeros((100, 2))
        self.ui.widget.minValue=-45
        self.ui.widget.maxValue=45
        self.ui.widget.units = "phi"

        self.ui.widget_2.minValue=-30
        self.ui.widget_2.maxValue=60
        self.ui.widget_2.units = "psi"

        
        
        
        #MainWindow.setCentralWidget(self.centralwidget)

        self.thread={}
        
        global data

        #self.win = pg.plot(title="Real-time plot")
        #self.curve = self.graphicsView.plot(pen='y')
        

        

        self.start_ethenet()


    def start_ethenet(self):
        self.thread[1] = ThreadClass(parent=None,index=1)
        self.thread[1].start()
        self.thread[1].any_signal.connect(self.my_function)
        #self.thread[1].a_signal.connect(self.run_log_csv)
        #self.pushButton1.setEnabled(False)

        # self.thread[2] = LoggingThread()
        # self.thread[2].start()
        # self.thread[2].log_signal.connect(self.log_csv)
        # #self.thread[2].join()
        

        # self.thread[3] = ChronometerThread()
        # self.thread[3].start()
        # self.thread[3].time_signal.connect(self.timer_csv)
        #self.thread[2].join()
        

    # def timer_csv(self,timer):
         
    #     self.lcdNumber_timer_2.setProperty("value", float(timer))
    def run_log_csv(self,m):
        self.thread[2] = LoggingThread()
        self.thread[2].start()
        
        #self.thread[2].log_signal.connect(self.log_csv)
         
    def log_csv(self,x):
         with open(namafile, 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            #if (array_data[0][0]!=0):
            for i in range(0,np.shape(array_data)[0]):
                #print(array_data)
                info = {
                    header1: array_data[i][0],
                    header2: array_data[i][1],
                    header3: array_data[i][2],
                    header4: array_data[i][3],
                    header5: array_data[i][4],
                    header6: array_data[i][5],
                }
                csv_writer.writerow(info)

            

    def my_function(self,phi : str,psi,d,x,y,z,timer):
        #print(phi,psi,d,x,y,z)
        #print(timer)
        
        a_data=[float(phi),float(psi)]
        # print(a_data.shape())

        
        self.curve.setData(array_data)

        self.ui.widget.updateValue(float(phi),False)
        self.ui.widget_2.updateValue(float(psi),False)
        self.horizontalSlider.setValue(round(float(d)))
        a_d=round(float(d),2)
        #print(a_d)
        self.label_d.setText(str(a_d))
        self.ui.lcdNumber_X.setProperty("value", float(x))
        self.ui.lcdNumber_Y.setProperty("value", float(y))
        self.ui.lcdNumber_Z.setProperty("value", float(z))
        self.ui.lcdNumber.setProperty("value", float(timer))
         
        
        
        
# class ChronometerThread(QtCore.QThread):
#     time_signal = QtCore.pyqtSignal(int)

#     def run(self):
#         start_time = time.perf_counter()
#         while True:
#             end_time = time.perf_counter()
#             elapsed_time = (end_time - start_time) * 1000
#             self.time_signal.emit(round(elapsed_time))
#             #time.sleep(0.001)

class LoggingThread(QtCore.QThread):
    log_signal = QtCore.pyqtSignal(str)

    def run(self):
         with open(namafile, 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            #if (array_data[0][0]!=0):
            for i in range(0,np.shape(array_data)[0]):
                #print(array_data)
                info = {
                    header1: array_data[i][0],
                    header2: array_data[i][1],
                    header3: array_data[i][2],
                    header4: array_data[i][3],
                    header5: array_data[i][4],
                    header6: array_data[i][5],
                }
                csv_writer.writerow(info)              

           

class ThreadClass(QtCore.QThread):

    any_signal = QtCore.pyqtSignal(str,str,str,str,str,str,str)
    a_signal = QtCore.pyqtSignal(int)
    
    #array_data = np.zeros((5000, 2))

    #array_data=np.empty(shape=[500, 2])

    #print(array_data)
    #array_data=[]
    #array_data=array_data.reshape(1000,2)
    #array_data = np.array(array_data)
    
    def __init__(self, parent=None,index=0):
        super(ThreadClass, self).__init__(parent)
        self.index=index
        self.is_running = True
        self.array = []

    def run(self):
        print('Starting thread...',self.index)
        cnt=0
        UDP_IP = "127.0.0.1"  # Listen on all available network interfaces
        UDP_PORT = 5005

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        sock.bind((UDP_IP, UDP_PORT))
        #print('ok')
        data_asly_star=['0','0','0','0']
        data_not_proceed=''

        data=0
        data2=0
        data3=0
        l__0=0.006;
        l__1=0.1820;
        # l__1=0.1760;
        l__3=0.05;
        l__5=0.1150;
        l__2=0.07;
        l__7=0.0342;
        theta=42*(pi/180);
        alpha=50*(pi/180);
        data_baghi=''
        num=0
        global array_data
        array_data = np.empty((0, 2), float)
        phi_qably=-1000
        psi_qably=-1000
        d_qably=-1000
        x_qably=-1000
        y_qably=-1000
        z_qably=-1000
        data3_timer_qably=-1
        counter_for_emit=0
        while (True):
            data = sock.recv(50).decode()
            #print(data)
            data_ma=str(data_baghi)+str(data)
            #print(data_ma)
            # Decode the data
            n_hashtak = data_ma.find('#')
            data_baghi=str(data_ma[n_hashtak+1:])
            data_asly_star = data_ma[0:n_hashtak].split('*')
            #print(str(data_asly_star))
            if data_asly_star[0]=='':
                del data_asly_star[0]
            #print(data_asly_star)
            if len(data_asly_star) == 4:
                data_q1=int(data_asly_star[0])
                data2_q2=int(data_asly_star[1])
                data3_q3=int(data_asly_star[2])
                data3_timer=int(data_asly_star[3])
                #data_q1, data2_q2, data3_q3,data3_timer = map(float, str(data_asly_star))
                #print(f"x={x}, y={y}, z={z}")
                
            
            
            
             
                 #print(packet)     

            #tedad_moraba=data_asly.count('#')
            #data_asly_star=[data_asly_star[0], data_asly_star[1],data_asly_star[2],data_asly_star[3]]
            #data_asly_star=[]    
            #print(data_not_proceed,type(data_not_proceed))
            
            
            #data_asly_star=data_asly_q
            # while("" in data_asly_star):
            #     data_asly_star.remove("")
                       
            #data_q1=int(data_asly_star[0])
            #data2_q2=int(data_asly_star[1])
            #data3_q3=int(data_asly_star[2])
            #data3_timer=int(data_asly_star[3])
            #print(data_q1,data2_q2,data3_q3,data3_timer)
            phi=(data_q1)*(pi/180)
            psi=(data2_q2)*(pi/180)
            d=((-data3_q3))/1000
            x=(sin(theta) * cos(psi + alpha) * d + cos(theta) * cos(phi) * sin(psi + alpha) * d + sin(theta) * (l__1 + l__3 + l__5))
            y=(sin(phi) * sin(psi + alpha) * d)
            z=(cos(theta) * cos(psi + alpha) * d - cos(phi) * sin(theta) * sin(psi + alpha) * d + cos(theta) * (l__1 + l__3 + l__5))
            
            
            array_values = [phi, psi]
            array_values = np.array(array_values)
            self.array.append(array_values)

            array_values = np.array([phi, psi]).reshape(1, 2)  # create a new row to append
            # array_data = np.append(array_data, array_values, axis=0) 
            array_data = np.append(array_data, array_values, axis=0)
            #print(type(array_data))
            num=num+1
            if(num%50==0):
                 self.a_signal.emit(1)
                
            if(len(array_data)>500):
                #print(213)
                #array_data=np.append(array_values)
                
                #del array_data[0]
                #np.delete(array_data,0)
                #print(len(array_data))
                num=0
                
                #print(array_data) 
                #print(array_data)

            # array_values = np.array([phi, psi,d,x,y,z]).reshape(1, 6)  # create a new row to append
            # array_data = np.append(array_data, array_values, axis=0) 
            # if(num<50):
            #     #array_data=np.append(array_values)
            #     array_data = np.append(array_data, array_values, axis=0)
            #     num=num+1
            #     #print(array_data) 
            # else:
            #     self.a_signal.emit(1)
            #     array_data = np.empty((0, 6), float)
            #     #print(array_data)

            counter_for_emit=counter_for_emit+1
            if(phi_qably!=phi or psi_qably!=psi or d_qably!=d or x_qably!=x or y_qably!=y or z_qably!=z or data3_timer_qably!=data3_timer):
                #counter_for_emit=counter_for_emit+1
                #print(counter_for_emit)
                pass
            if(counter_for_emit>=100):
                self.any_signal.emit(str(phi),str(psi),str(d),str(x),str(y),str(z),str(data3_timer))
                counter_for_emit=0
            phi_qably=phi
            psi_qably=psi
            d_qably=d
            x_qably=x
            y_qably=y
            z_qably=z
            data3_timer_qably=data3_timer


    def stop(self):
        self.is_running = False
        print('Stopping thread...',self.index)
        self.terminate()

app = QtWidgets.QApplication(sys.argv)
#start_time = time.time()
namafile = 'data1D.csv'
header1 = "x_value"
header2 = "y_value"
header3 = "z_value"
header4 = "phi_value"
header5 = "psi_value"
header6 = "d_value"
header7 = "counter"
header8 = "Time"


fieldnames = [header1, header2, header3, header4, header5, header6,header7,header8]
with open(namafile, 'w') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                csv_writer.writeheader()
mainWindow = THREADS_APP()
#array=[1000]
mainWindow.show()
sys.exit(app.exec_())

