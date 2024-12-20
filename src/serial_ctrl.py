import sys
#sys.path.append("/home/cherry/.local/lib/python2.7/site-packages")
import serial
from serial.tools import list_ports
from time import sleep


def select_port(baudrate=19200):
    ser = serial.Serial()
    ser.baudrate = baudrate    
    ser.timeout = 10       # タイムアウトの時間
    ports = list_ports.comports()    # ポートデータを取得
    devices = [info.device for info in ports]
    if len(devices) == 0:
        # シリアル通信できるデバイスが見つからなかった場合
        print("Error: Port not found",file=sys.stderr)
        return None
    else:
        # 複数ポートの場合、選択
        for i in range(len(devices)):
            print(f"input {i:d} open {devices[i]}",file=sys.stderr)
        # 標準出力がファイル出力に吸われるのでポートの選択は決め打ち
        #num = int(input("Please enter the port number:"))
        num = 0
        ser.port = devices[num]
    
    # 開いてみる
    try:
        ser.open()
        return ser
    except:
        print("Error：The port could not be opened.",file=sys.stderr)
        return None