"""main script."""
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from multiprocessing import Queue

from serial_collector.serial_connector import SerialConnector


import numpy as np
from pyqtgraph.ptime import time
from datetime import datetime

serial_connector_queue = Queue(2000)
my_serial_connector = SerialConnector(serial_connector_queue)
my_serial_connector.start()

app = QtGui.QApplication([])
p = pg.plot()
p.setWindowTitle('live plot from serial')
curve = p.plot()

data = []
times = np.array([], dtype='float64')
y_data = np.array([], dtype='float64')

def update():
    global curve, data, times, y_data
    point = serial_connector_queue.get()
    times = np.append(times, point.getSecond())
    y_data = np.append(y_data, point.getYData())
    times = times[-60:]
    y_data = y_data[-60:]
    # times.append(point.getSecond())
    # y_data.append(point.getYData())
    # print(times)
    # print(y_data)
    # print("        ")
    # y_data = np.array(ydata, dtype='float64')
    # x_data = np.array(times, dtype='float64')
    curve.setData(times, y_data, pen='r')
    p.setYRange(0, max(y_data))
    p.setXRange(min(times), max(times))
    app.processEvents()



timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
