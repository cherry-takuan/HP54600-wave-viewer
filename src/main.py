import sys
import serial_ctrl

def HPGL2SVG(source):
    #プロット範囲オフセット
    x_offset = 0
    y_offset = 0
    #プロット範囲
    x_size = 0
    y_size=0
    #現在のペン
    SP = None
    #ペンの選択
    SP_TABLE = [
        """<g fill="#fff" stroke="#FFF" stroke-width="1">""",#背景色
        """<g fill="#fff" stroke="#F00" stroke-width="1">""",#R
        """<g fill="#fff" stroke="#0F0" stroke-width="1">""",#G
        """<g fill="#fff" stroke="#00F" stroke-width="1">""",#B
    ]
    # ペンの状態
    # PU:ペンが上がっている状態
    # PD:ペンが下がっている状態
    pen_cond = "PU"
    
    # テキスト処理中フラグ
    LB = False

    # 現在のペンの座標
    pen_x = 0
    pen_y = 0

    # SVGのデータを保持
    svg_data = ""
    # ";" で分割
    data_list = source.split(";")
    #一行ずつ処理
    for line in data_list:
        #print(line)
        line = line.upper()
        if len(line) < 2:
            continue
        op = line[0:2]
        param = ""
        if len(line) >= 3:
            param = line[2:]
        #print(op,":",param)
        if LB == True:
            svg_data += ";"
            for data in param:
                if ord(data) == 0x03:
                    svg_data += '</div></foreignObject>'
                    LB = False
                    break
                else:
                    svg_data += data
        elif op == "DF":
            pass
        elif op == "SC":
            #スクリーン切り替え時初期化
            #print("</g>",file=sys.stderr)
            if SP != None:
                #print("</g>",file=sys.stderr)
                svg_data += "</g>" + "\n"
            SP = None
            ###########################
            param = param.split(",")
            print("x:",int(param[0]),int(param[1]),file=sys.stderr)
            print("y:",int(param[2]),int(param[3]),file=sys.stderr)
            x_offset = int(param[0])
            y_offset = int(param[2])

            x_size = int(param[1])
            y_size = int(param[3])
        elif op == "SP":
            if SP != None:
                #print("</g>",file=sys.stderr)
                svg_data += "</g>" + "\n"
            SP = int(param)
            #print(SP_TABLE[SP],file=sys.stderr)
            svg_data += SP_TABLE[SP] + "\n"
        elif op == "PU":
            param = param.split(",")
            if len(param)==2:
                pen_x = int(param[0])
                pen_y = int(param[1])
            elif len(param)>2:
                print("Err:to many param:",op,param,file=sys.stderr)
            if pen_cond != "PU":
                svg_data += '" stroke-width="1"/>\n'
            pen_cond = "PU"
        elif op == "PD":
            pen_cond = "PD"
            param = param.split(",")
            if len(param)==2:
                pen_x = int(param[0])
                pen_y = int(param[1])
            elif len(param)>2:
                print("Err:to many param:",op,param,file=sys.stderr)
            #svg_data += '<path d="M'+str(pen_x)+','+str(y_size-pen_y)
            svg_data += '<path d="M'+str(pen_y)+','+str(pen_x)

        elif op == "PA":
            param = param.split(",")
            if pen_cond == "PD":
                #print('<path d="M'+str(pen_x)+','+str(pen_y)+' L'+str(param[0])+','+str(param[1])+'" />',file=sys.stderr)
                #svg_data += '<path d="M'+str(pen_x)+','+str(y_size-pen_y)+' L'+str(int(param[0]))+','+str(y_size-int(param[1]))+'" stroke-width="1.5"/>\n'
                #svg_data += ' L'+str(int(param[0]))+','+str(y_size-int(param[1]))
                svg_data += ' L'+str(int(param[1]))+','+str(int(param[0]))
            if len(param)>0:
                pen_x = int(param[-2])
                pen_y = int(param[-1])
            pass
        elif op == "DR":
            pass
        elif op == "SR":
            pass
        elif op == "LB":
            #svg_data += '<text x="'+str(pen_y)+'" y="'+str(pen_x)+'">'
            svg_data += '<foreignObject x="'+str(pen_y)+'" y="'+str(pen_x)+'" width="'+str(y_size)+'" height="'+str(x_size)+'"><div xmlns="http://www.w3.org/1999/xhtml" style="white-space: pre; font-family: Arial; font-size: 7px; background-color: #e0e0ff; padding: 5px;">'
            svg_data += ";"
            for data in param:
                if ord(data) == 0x03:
                    svg_data += '</div></foreignObject>'
                    LB = False
                    break
                else:
                    svg_data += data
        else:
            print("Err:unknown oprator :",op,file=sys.stderr)
            print("              param :",param,file=sys.stderr)
            exit(1)

    #print('<svg widht="',str(x_size),'" height="',str(y_size),'" xmlns="http://www.w3.org/2000/svg">')
    #print('<svg widht="',str(y_size),'" height="',str(x_size),'" xmlns="http://www.w3.org/2000/svg">')
    #print(svg_data)
    #print('</g></svg>')
    svg_result = '<svg widht="'+str(y_size)+'" height="'+str(x_size)+'" xmlns="http://www.w3.org/2000/svg">'
    svg_result += svg_data
    svg_result += '</g></svg>'
    return svg_result


# メイン
if __name__ == "__main__":
    ser = serial_ctrl.select_port(baudrate=19200)
    #source=sys.stdin.read()
    source = ""
    print("Receive...",file=sys.stderr)
    ser.reset_input_buffer()
    while True:
        data = ser.read(1)
        if not data:
            print("time out",file=sys.stderr)
            break
        if int.from_bytes(data, byteorder='little') == 0x03:
            #print("0x03",file=sys.stderr)
            source += chr(0x03)
            source += ";"
        else:
            source += data.decode('UTF-8')
        #print(data.strip().decode('UTF-8'),file=sys.stderr)

    print("Done",file=sys.stderr)
    print(HPGL2SVG(source))