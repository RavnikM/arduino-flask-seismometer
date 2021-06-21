import sqlite3
import serial

class arduino_nano_seizometer():
    def __init__(self,port, boudrate = 115200):
        self.serial = serial.Serial(port=port,
                            baudrate=boudrate,
                            bytesize=serial.EIGHTBITS,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            timeout=1)



    def __exit__(self, exc_type, exc_val, exc_tb):
        self.serial.close()

    def read_values(self):
        val_ascii = self.serial.read_until()
        val_utf = (val_ascii.decode('utf-8'))
        return val_utf.split('\t')

    def archive_values(self):
        self.conn = sqlite3.connect('sqlite3/seizmometer.db')
        self.cur = self.conn.cursor()
        while True:
            values_list = self.read_values()
            #print(values_list)
            if len(values_list) == 3:
                self.cur.execute('INSERT INTO seizmograph (ID,axis_x,axis_y,axis_z,timestamp) VALUES (NULL,?,?,?,datetime("Now"))',(values_list[0],values_list[1],values_list[2]))
                self.conn.commit()
