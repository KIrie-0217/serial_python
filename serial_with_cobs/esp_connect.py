from dataclasses import dataclass
import serial
from blessed import Terminal

class serialConnection(object):

    def __init__(self,port:str,bps:int):
        self.port = port
        self.bps =bps

        self.ser = serial.Serial(self.port,self.bps,timeout=4.0)

    @dataclass
    class Decoded:
        data: int =0
        flag: bool =0

    def read(self):
        values = []
        output = self.Decoded()
        while True:
            val = self.ser.read()
            if len(val) != 0:
                values.append(int(val.hex(),16))
                print( int(val.hex(),16) )
                if int(val.hex(),16) == 0:
                    decoded = self.cobs_decode(values)
                    output.data = int.from_bytes( bytearray(decoded[:4][::-1]) ,"big")
                    output.flag = int.from_bytes( bytearray(decoded[4]) , "big",signed=False)
                    print(output.data)
                    return output

    def write(self,value:str) -> None:
        self.ser.write(value)
        return None

    def close(self) -> None:
        self.ser.close()
        print("Connection closed")
        return None

    def cobs_decode(self,values:list):
        decoded = values.copy()
        print(values)
        print(decoded)
        count = 0
        while count < len(decoded) -1:
            count  += values[count]
            print(count)
            decoded[ count ] =0
            print(decoded)
        decoded = decoded[1:-1]
        print(decoded)
        return decoded


def main():

    serial_adaptor = serialConnection("/dev/ttyUSB0",115200)

    while True:
        try :
            serial_adaptor.read()
        except KeyboardInterrupt:
            serial_adaptor.close()
            break

    return None

if __name__ == '__main__':
    main()