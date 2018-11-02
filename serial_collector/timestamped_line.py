from datetime import datetime
import json
import time


class TimestampedLine():

    def __init__(self, data: bytes):
        self.timestamp = time.time()
        self.data = int(data)

    def getSecond(self):
        result = int(round(self.timestamp * 1000))
        # last_two_digits = float(str(result)[-3:]) if '.' in str(result)[-2:] else int(str(result)[-2:])
        return result

    def getYData(self):
        return self.data
