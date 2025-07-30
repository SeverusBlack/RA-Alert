# This script uses multiprocessing to analize three set of data in paralell.
# however, the process are not interaction with each other.

import tkinter as tk
from tkinter import *
from PIL import ImageTk
import pyautogui as pg
import pytesseract
from pynput.mouse import Listener
import time
import threading
import multiprocessing
from twilio.rest import Client
import pyperclip as pc
import pandas as pd
import re


def StartANewThread(status, xs, ys, StrokeUL, StrokeLL, LoadUL, LoadLL, DefUL, DefLL, ErrorCountLimit, starttime=[],
                    printed=[]):
    printed = 0

    global I_List_Stroke, T_List_Stroke, callstatus
    I_List_Stroke = []
    T_List_Stroke = []

    global I_List_Load, T_List_Load
    I_List_Load = []
    T_List_Load = []

    global I_List_Def, T_List_Def
    I_List_Def = []
    T_List_Def = []

    global ErrorTypeS, ErrorLogTimeS
    ErrorTypeS = []
    ErrorLogTimeS = []
    ErrorCount = 0
    ErrorTime = []

    global csv_List_Time, csv_List_Stroke, csv_List_Load, csv_List_Def
    csv_List_Time = []
    csv_List_Stroke = []
    csv_List_Load = []
    csv_List_Def = []
    csvsaved = 0

    count = 0

    def CallThread(callstatus):
        ActuatroStopURL = #insert twolio url for specific call or text prompt
        ROLLSStopURL = #insert twolio url for specific call or text prompt
        ErrorURL = #insert twolio url for specific call or text prompt
        account_sid = #insert twolio account info
        auth_token =  #insert twolio account info
        client = Client(account_sid, auth_token)
        while True:
            if callstatus == "Actuator Stop":
                call = client.calls.create(

                    url=ActuatroStopURL,
                    to= #alert phone number,
                    from_=#twolio phone number

                )
                print(call.sid)
                callstatus = "None"
            elif callstatus == "ROLLS Stop":
                call = client.calls.create(

                    url=ROLLSStopURL,
                    to= #alert phone number,
                    from_=#twolio phone number

                )
                print(call.sid)
                callstatus = "None"
            elif callstatus == "Too Much Error":
                call = client.calls.create(

                    url=ErrorURL,
                    to= #alert phone number,
                    from_=#twolio phone number

                )
                print(call.sid)
                callstatus = "None"
            else:
                pass

    def savecsv(time_List, stroke_List, load_List, def_List, filename):
        df_log = pd.DataFrame()
        df_log['Time'] = time_List
        df_log['Stroke [mm]'] = stroke_List
        df_log['Load [kN]'] = load_List
        df_log['Def [mm]'] = def_List
        df_log.to_csv('LogFile/LogFile' + str(filename) + '.csv')
        print('csv log saved')
        del df_log

    while True:

        if status == "Go":

            if len(ErrorTime) > 1:
                ErrorTime_Temp = []
                for t in ErrorTime:
                    if t + 60 < time.time():
                        pass
                    else:
                        ErrorTime_Temp.append(t)
                ErrorTime = ErrorTime_Temp
                ErrorCount = len(ErrorTime)

            if len(I_List_Stroke) == 101:
                I_List_Stroke = I_List_Stroke[1:]
                T_List_Stroke = T_List_Stroke[1:]

            if len(I_List_Load) == 101:
                I_List_Load = I_List_Load[1:]
                T_List_Load = T_List_Load[1:]

            if len(I_List_Def) == 101:
                I_List_Def = I_List_Def[1:]
                T_List_Def = T_List_Def[1:]

            if len(csv_List_Stroke) == 2000:
                savecsv(csv_List_Time, csv_List_Stroke, csv_List_Load, csv_List_Def, csvsaved)
                csv_List_Time = []
                csv_List_Stroke = []
                csv_List_Load = []
                csv_List_Def = []
                csvsaved = csvsaved + 1

            if len(I_List_Def) == 0:
                pg.click(xs, ys)
            else:
                pass
            pg.hotkey('ctrl', 'c')
            pg.press('enter')
            text = pc.paste()
            pg.press('enter')

            St = time.time()

            SLine = text.splitlines()[2]
            LLine = text.splitlines()[1]
            DLine = text.splitlines()[6]

            S = SLine[0:6]
            L = LLine[0:6]
            D = DLine[0:6]

            try:
                float(S)
            except ValueError:
                S = ""
                ErrorTypeS.append("float error Stroke")
                ErrorLogTimeS.append(time.asctime())
                print("stroke float error")
                # print("float error Stroke")

            try:
                float(L)
            except ValueError:
                L = ""
                ErrorTypeS.append("float error Load")
                ErrorLogTimeS.append(time.asctime())
                print("Load float error")

            try:
                float(D)
            except ValueError:
                D = ""
                ErrorTypeS.append("float error Def")
                ErrorLogTimeS.append(time.asctime())
                print("Def float error")

            while True:
                if len(S) < 1 or len(L) < 1 or len(D) < 1:

                    if len(I_List_Def) == 0:
                        pg.click(xs, ys)
                    else:
                        pass
                    pg.hotkey('ctrl', 'c')
                    pg.press('enter')
                    text = pc.paste()
                    pg.press('enter')

                    St = time.time()

                    SLine = text.splitlines()[2]
                    LLine = text.splitlines()[1]
                    DLine = text.splitlines()[6]

                    S = SLine[0:6]
                    L = LLine[0:6]
                    D = DLine[0:6]

                    try:
                        float(S)
                    except ValueError:
                        S = ""
                        ErrorTypeS.append("float error Stroke")
                        ErrorLogTimeS.append(time.asctime())
                        # print("float error Stroke")

                    try:
                        float(L)
                    except ValueError:
                        L = ""
                        ErrorTypeS.append("float error Load")
                        ErrorLogTimeS.append(time.asctime())
                        # print("float error Stroke")

                    try:
                        float(D)
                    except ValueError:
                        D = ""
                        ErrorTypeS.append("float error Def")
                        ErrorLogTimeS.append(time.asctime())
                        # print("float error Stroke")

                    ErrorCount = ErrorCount + 1
                    ErrorTime.append(time.time())
                    if ErrorCount == ErrorCountLimit + 1:
                        break
                    elif ErrorCount > ErrorCountLimit:
                        ErrorTypeS.append("Too much error")
                        ErrorLogTimeS.append(time.asctime())
                        # print("Error Count:", " ", ErrorCount)
                        status = "Stop"
                        callstatus = "Too Much Error"
                        print("Too Much Error")
                        print(ErrorTypeS)
                        print("Stroke: ", I_List_Stroke)
                        CallThread(callstatus)
                        # break

                else:
                    break

            if ErrorCount <= ErrorCountLimit:

                #print("Stroke: ", S, "mm")
                #print("Load: ", L, "kN")
                #print("Def: ", D, "mm")

                T_List_Stroke.append(St)

                S = float(S)
                L = float(L)
                D = float(D)

                I_List_Stroke.append(S)
                I_List_Load.append(L)
                I_List_Def.append(D)

                csv_List_Time.append(time.asctime())
                csv_List_Stroke.append(S)
                csv_List_Load.append(L)
                csv_List_Def.append(D)

                if S > StrokeUL or S < StrokeLL:
                    ErrorTypeS.append("Stroke outside boundary")
                    ErrorLogTimeS.append(time.asctime())
                    # print("Stroke outside boundary")
                    ErrorCount = ErrorCount + 1
                    ErrorTime.append(time.time())
                else:
                    pass

                if L > LoadUL or L < LoadLL:
                    ErrorTypeS.append("Load outside boundary")
                    ErrorLogTimeS.append(time.asctime())
                    # print("Stroke outside boundary")
                    ErrorCount = ErrorCount + 1
                    ErrorTime.append(time.time())
                else:
                    pass

                if D > DefUL or D < DefLL:
                    ErrorTypeS.append("Def outside boundary")
                    ErrorLogTimeS.append(time.asctime())
                    # print("Stroke outside boundary")
                    ErrorCount = ErrorCount + 1
                    ErrorTime.append(time.time())
                else:
                    pass

                Llenth = len(I_List_Stroke)
                # print("Stroke Llenth :", Llenth)

                if Llenth > 30:

                    P_same_Stroke = 0
                    for i in range(Llenth - 30, Llenth):
                        if S + 0.2 > I_List_Stroke[i] > S - 0.2:
                            P_same_Stroke = P_same_Stroke + 1
                            # print("P_same_Stroke", P_same_Stroke)
                        else:
                            pass
                    if P_same_Stroke >= 25:  # 25:
                        ErrorTypeS.append("Actuator Stopped: Stroke Confirmed")
                        ErrorLogTimeS.append(time.asctime())
                        # print("Actuator Stopped: Stroke Confirmed")
                        status = "Stop"
                        callstatus = "Actuator Stop"
                        print("Acuator Stop Stroke Confirmed")
                        print("Stroke: ", I_List_Stroke)
                        savecsv(csv_List_Time, csv_List_Stroke, csv_List_Load, csv_List_Def, callstatus)
                        CallThread(callstatus)
                    else:
                        pass
                if Llenth > 30:
                    P_same_Load = 0
                    for i in range(Llenth - 30, Llenth):
                        if L + 0.5 > I_List_Load[i] > L - 0.5:
                            P_same_Load = P_same_Load + 1
                            # print("P_same_Stroke", P_same_Stroke)
                        else:
                            pass
                    if P_same_Load >= 25:  # 25:
                        ErrorTypeS.append("Actuator Stopped: Load Confirmed")
                        ErrorLogTimeS.append(time.asctime())
                        # print("Actuator Stopped: Stroke Confirmed")
                        status = "Stop"
                        callstatus = "Actuator Stop"
                        print("Acuator Stop Load Confirmed")
                        print("Load: ", I_List_Load)
                        savecsv(csv_List_Time, csv_List_Stroke, csv_List_Load, csv_List_Def, callstatus)
                        CallThread(callstatus)
                    else:
                        pass
                if Llenth > 30:
                    P_same_Def = 0
                    for i in range(Llenth - 30, Llenth):
                        if D + 0.05 > I_List_Def[i] > D - 0.05:
                            P_same_Def = P_same_Def + 1
                            # print("P_same_Stroke", P_same_Stroke)
                        else:
                            pass
                    if P_same_Def == -1:  # >=25:
                        ErrorTypeS.append("ROLLS Stopped")
                        ErrorLogTimeS.append(time.asctime())
                        print("ROLLS Stopped")
                        status = "Stop"
                        callstatus = "ROLLS Stop"
                        print("ROLLS Stopped")
                        print("Def: ", I_List_Def)
                        savecsv(csv_List_Time, csv_List_Stroke, csv_List_Load, csv_List_Def, callstatus)
                        CallThread(callstatus)
                    else:
                        pass

            if ErrorCount > ErrorCountLimit:
                ErrorTypeS.append("Too much error")
                ErrorLogTimeS.append(time.asctime())
                # print("Error count exceeded limit")
                status = "Stop"
                callstatus = "Too Much Error"
                print("Too Much Error")
                print(ErrorTypeS)
                print("Stroke: ", I_List_Stroke)
                print("Load: ", I_List_Load)
                print("Def: ", I_List_Def)
                savecsv(csv_List_Time, csv_List_Stroke, csv_List_Load, csv_List_Def, callstatus)
                CallThread(callstatus)

            count = count + 1

            try:
                starttime
            except NameError:
                starttime = []

            if count == 1:
                print("starttime", time.time())
                starttime = time.time()
            elif count == 10:
                print(count, "S data aquried takes", time.time() - starttime, " sec")
            elif count == 20:
                print(count, "S data aquried takes", time.time() - starttime, " sec")
            elif count == 30:
                print(count, "S data aquried takes", time.time() - starttime, " sec")
            # return callstatus, status
            print('Data Collected:', count)
            time.sleep(0.2)

        elif status == "Stop":
            if printed == 0:
                for e, t in zip(ErrorTypeS, ErrorLogTimeS):
                    print(e, t)
                printed = 1
            else:
                pass
        elif status == "Resume":

            I_List_Stroke = []
            I_List_Load = []
            I_List_Def = []
            T_List_Stroke = []

            print("Program Resumed")

            status = "Go"

            ErrorCount = 0
            ErrorTime = []
            ErrorLogTimeS = []
            ErrorTypeS = []
            # return callstatus, status


def StartA():
    global ErrorCountLimit
    ErrorCountLimit = 150
    global status
    status = "Go"

    program = multiprocessing.Process(target=StartANewThread, args=(status, xs, ys, StrokeUL, StrokeLL, LoadUL,
                                                                    LoadLL, DefUL, DefLL, ErrorCountLimit))
    program.daemon = True
    print("program started")
    program.start()

    program.join()


if __name__ == "__main__":
    root = Tk()

    root.title("RA Alert")
    root.geometry("600x270")

    f_Stroke = tk.Frame(root, height=200, width=200)
    f_SF = tk.Frame(root, height=50, width=600)

    f_Stroke.grid(row=0, column=0)
    f_SF.grid(row=1, column=0, columnspan=3)

    f_Stroke.grid_propagate(0)
    f_SF.grid_propagate(0)

    ErrorCountLimit = 200


    def StrokeArea():
        StrokeA = Toplevel()
        StrokeA.geometry("270x200")
        l = Label(StrokeA, text="Please click on the start and end point")
        imagedis = Label(StrokeA)
        imagedis.grid(row=1, column=0, columnspan=3)
        global xs
        global ys
        global hs
        global ws
        xs = 0
        ys = 0
        hs = 0
        ws = 0

        def confirm(xs, ys):
            global r_Stroke
            r_Stroke = [xs, ys]

            global StrokeUL
            StrokeUL = float(EStrokeUL.get())

            global StrokeLL
            StrokeLL = float(EStrokeLL.get())

            global LoadUL
            LoadUL = float(ELoadUL.get())

            global LoadLL
            LoadLL = float(ELoadLL.get())

            global DefUL
            DefUL = float(EDefUL.get())

            global DefLL
            DefLL = float(EDefLL.get())

            return r_Stroke

        def start():

            spointx = []
            spointy = []

            def on_click(x, y, button, pressed):
                if pressed:
                    spointx.append(x)
                    spointy.append(y)
                if len(spointx) == 1:
                    listener.stop()

            with Listener(on_click=on_click) as listener:
                listener.join()

            if len(spointx) == 1:
                global xs
                global ys
                global hs
                global ws
                xs = spointx[0]
                ys = spointy[0]

                print(xs, ys)
                print(spointx, spointy)

                pg.moveTo(xs, ys)

                pg.hotkey("ctrl", "c")
                time.sleep(0.01)

                text = pc.paste()

                print(text)

        def redo():
            pass

        b1 = Button(StrokeA, text="Confirm", command=lambda: confirm(xs, ys))
        b2 = Button(StrokeA, text="Start", command=start)
        b3 = Button(StrokeA, text="Redo", command=redo)

        LStrokeUL = Label(StrokeA, text="Stroke Upper Limit")
        LStrokeLL = Label(StrokeA, text="Stroke Lower Limit")
        LLoadUL = Label(StrokeA, text="Load Upper Limit")
        LLoadLL = Label(StrokeA, text="Load Lower Limit")
        LDefUL = Label(StrokeA, text="Def Upper Limit")
        LDefLL = Label(StrokeA, text="Def Lower Limit")

        global EStrokeUL
        global EStrokeLL
        global ELoadUL
        global ELoadLL
        global EDefUL
        global EDefLL

        EStrokeUL = Entry(StrokeA)
        EStrokeUL.insert(0, "0")
        EStrokeLL = Entry(StrokeA)
        EStrokeLL.insert(0, "-50")




        ELoadUL = Entry(StrokeA)
        ELoadUL.insert(0, "0")
        ELoadLL = Entry(StrokeA)
        ELoadLL.insert(0, "-250")

        EDefUL = Entry(StrokeA)
        EDefUL.insert(0, "0")
        EDefLL = Entry(StrokeA)
        EDefLL.insert(0, "-100")

        l.grid(row=0, column=0, columnspan=3)

        LStrokeUL.grid(row=2, column=0)
        EStrokeUL.grid(row=2, column=1, columnspan=2)

        LStrokeLL.grid(row=3, column=0)
        EStrokeLL.grid(row=3, column=1, columnspan=2)

        LLoadUL.grid(row=4, column=0)
        ELoadUL.grid(row=4, column=1, columnspan=2)

        LLoadLL.grid(row=5, column=0)
        ELoadLL.grid(row=5, column=1, columnspan=2)

        LDefUL.grid(row=6, column=0)
        EDefUL.grid(row=6, column=1, columnspan=2)

        LDefLL.grid(row=7, column=0)
        EDefLL.grid(row=7, column=1, columnspan=2)

        b1.grid(row=8, column=0)
        b2.grid(row=8, column=1)
        b3.grid(row=8, column=2)








    def StopA():
        global status
        status = "Stop"


    def ResumeA():
        global status
        status = "Resume"


    def ExitA():
        sys.exit()


    b_Stroke = Button(f_Stroke, text="Set Up", command=StrokeArea)
    b_Start = Button(f_SF, text="Start", command=StartA)
    b_Stop = Button(f_SF, text="Stop", command=StopA)
    b_Resume = Button(f_SF, text="Resume", command=ResumeA)
    b_Exit = Button(f_SF, text="Exit", command=ExitA)

    l_Stroke = Label(f_Stroke, text="Set Up").grid(row=0, column=0)

    b_Stroke.grid(row=2, column=1)
    b_Start.grid(row=0, column=0, padx=50)
    b_Stop.grid(row=0, column=1, padx=50)
    b_Resume.grid(row=0, column=2, padx=50)
    b_Exit.grid(row=0, column=3, padx=50)

    root.mainloop()
