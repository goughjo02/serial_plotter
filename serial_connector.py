from serial import Serial, SerialException
from multiprocessing import Process, Queue
from time import sleep

import config


class SerialConnector(Process):
    """A thread class which reads the lines
    from a serial port, timestamps them and
    puts them on a queue
    """

    def __init__(self, q: Queue):
        Process.__init__(self)
        self.ser = Serial()
        self.q = q

    def run(self):
        self.try_make_serial()
        # NB: Serial is not open if it was instantiated without ports
        while(True):
            if not self.ser.is_open:
                print("serial connection not found")
                sleep(5)
                self.try_make_serial()
            else:
                try:
                    line = self.ser.readline()
                    self.q.put(int(line))
                    # y = x.decode()
                    # z = int(y)
                    # print(line)
                except SerialException:
                    print("serial connection disconnected")
                    self.ser = Serial()

    def try_make_serial(self):
        """ Tries to create a serial connection
        using the config. If it is unable to do
        this, it just exits.
        """
        try:
            self.ser = Serial(config.serial_port, config.baud_rate)
            self.ser.reset_input_buffer()
        except SerialException:
            self.ser = Serial()
