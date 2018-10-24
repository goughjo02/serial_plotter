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

def update():
    global curve, data
    point = serial_connector_queue.get()
    data.append(point)
    xdata = np.array(data, dtype='float64')
    curve.setData(xdata)
    p.setYRange(0, max(data[-100:]))
    p.setXRange(len(xdata)-100, len(xdata))
    app.processEvents()



timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
