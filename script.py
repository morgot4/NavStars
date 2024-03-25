from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import random
import numpy as np
from math import pi, sin, cos

def get_ulian(date):
    a=(14-int(date[1]))/12
    y=int(date[0])+4800-a
    m=int(date[1])+12*a-3
    JDN=int(date[2])+(153*m+2)/5+365*y+y/4-y/100+y/400-32045
    JD=JDN+(int(date[3])-12)/24+int(date[4])/1440+float(date[5])/86400
    return JD

def draw(names):
    ax = plt.figure().add_subplot(projection='3d')
    for name in names:
        data = SystemsEqualsParams[name[1]][1][name]; color = SystemsEqualsParams[name[1]][0]; X = []; Y = []; Z = []; T = []
        print(data)
        for event in data:
            X_0 = list(map(float,event[1:4]))
            
            t = timeList[0] - timeList[event[0]-1]  # Matrix
            print(t)
            a = - 2*pi *t
            matrix_rotation = [ [cos(a), sin(a), 0],
                                [-sin(a), cos(a), 0],
                                [0, 0, 1]]
            X_t = np.matmul(X_0,matrix_rotation)
            X.append(list(X_t)[0])
            Y.append(list(X_t)[1])
            Z.append(list(X_t)[2])
            T.append(timeList[event[0]-1])
        figure = plt.figure(figsize=(7,3))
        plt.subplot(1,3,1)
        plt.plot(T, X, color = color); plt.grid()
        plt.title(f"X(T) {name}")
        plt.subplot(1,3,2)
        plt.plot(T, Y,color = color); plt.grid()
        plt.title(f"Y(T) {name}")
        plt.subplot(1,3,3)
        plt.plot(T, Z,color = color); plt.grid()
        plt.title(f"Z(T) {name}")
        figure2 = plt.figure(figsize=(7,3))
        plt.subplot(1,3,1)
        plt.plot(X, Z,color = color); plt.grid()
        plt.title(f"X(Z) {name}")
        plt.subplot(1,3,2)
        plt.plot(X, Y,color = color); plt.grid()
        plt.title(f"X(Y) {name}")
        plt.subplot(1,3,3)
        plt.plot(Y, Z,color=color); plt.grid()
        plt.title(f"Y(Z) {name}")
        ax.plot3D(X, Y, Z, label=name, color=color)
    
    ax.legend()
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = 6371 * np.outer(np.cos(u), np.sin(v))
    y = 6371 * np.outer(np.sin(u), np.sin(v))
    z = 6371 * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z)
    ax.set_aspect('equal')
    plt.show()
    figure2.show()
    figure.show()
    

    

            
def render():
    global Glonass,Galileo,Gps,Qzss,Beidou,tk_elements,timeList, systems, selected, filenames, checkvar, start_date, finish_date,SystemsEqualsParams, SatellitesForDraw, SystemForDraw, W, SystemsNames, NormalDate
    
    with open(filenames[selected.get()],'r',encoding='utf-8') as f:
        SatellitesForDraw = []
        SystemForDraw = []
        W = []
        Glonass = {}
        Galileo = {}
        Gps = {}
        Beidou = {}
        Qzss = {}
        NormalDate = []
        timeList = []
        systems = []
        indexTime = 0
        SystemsEqualsParams = {'R':['green',Glonass,'Глонасс'],
               'E':['red', Galileo, 'Галилео'],
               'C': ['blue', Beidou, 'Beidou'],
                'G': ['yellow', Gps, 'Gps'],
                'J': ['orange', Qzss, 'Qzss']}
        
        SystemsNames = {'Глонасс': Glonass,
                       'Галилео': Galileo,
                       'Beidou': Beidou,
                       'Qzss': Qzss,
                       'Gps': Gps,}
        for i in range(2):
            line = f.readline()
        line = f.readline()
        n = line[3:6]
        line = line[6:]
        names = []
        current_name = ''
        checkvar = []
        for i in range(7):  # read all satelites
            for index, letter in enumerate(line):
                if line[:1] == '++':
                    break
                if letter == '\n':
                    names.append(current_name)
                    current_name = ''
                    break
                if letter not in '+ ':
                    if letter in 'CJERG':
                        if line[index-1] == ' ':
                            current_name += letter
                        else:
                            names.append(current_name)
                            current_name = ''
                            current_name += letter
                    else:
                        current_name += letter
                else:
                    if current_name != '':
                        names.append(current_name)
                        break
            line = f.readline()
        while True:
            if line[0] == '*':
                break
            line = f.readline()

        date = line.split()
        
        date = date[1:]
        NormalDate.append((int(date[3]),int(date[4]),float(date[5]),int(date[2]),int(date[1]),))
        start_date = [int(date[2]), int(date[1]), int(date[0])]
        time = get_ulian(date)
        timeList.append(time)
        
        indexTime+=1
        while True:
            
            line = f.readline()
            if line[0:3] == 'EOF':
                break
            elif line[0] == '*':
                date = line.split()
                date = date[1:]
                finish_date = [int(date[2]), int(date[1]), int(date[0])]
                NormalDate.append((int(date[3]),int(date[4]),float(date[5]),int(date[2]),int(date[1]),))
                time = get_ulian(date)
                timeList.append(time)
                indexTime+=1
            else:    
                info = line.split()
                if info[0][1] == 'E':
                    if 'Галилео' not in systems:
                        systems.append('Галилео')
                        checkvar.append(BooleanVar())
                    name = info[0]
                    info = info[1:4]
                    info.insert(0,indexTime)
                    if name not in Galileo.keys():
                        Galileo[name] = [info]
                    else:
                        Galileo[name].append(info)
                elif info[0][1] == 'R':
                    if 'Глонасс' not in systems:
                        systems.append('Глонасс')
                        checkvar.append(BooleanVar())
                    name = info[0]
                    info = info[1:4]
                    info.insert(0,indexTime)
                    if name not in Glonass.keys():
                        Glonass[name] = [info]
                    else:
                        Glonass[name].append(info)
                elif info[0][1] == 'G':
                    if 'Gps' not in systems:
                        systems.append('Gps')
                        checkvar.append(BooleanVar())
                    name = info[0] 
                    info = info[1:4]
                    info.insert(0,indexTime)
                    if name not in Gps.keys():
                        Gps[name] = [info]
                    else:
                        Gps[name].append(info)
                elif info[0][1] == 'C':
                    if 'Beidou' not in systems:
                        systems.append('Beidou')
                        checkvar.append(BooleanVar())
                    name = info[0]
                    info = info[1:4]
                    info.insert(0,indexTime)
                    if name not in Beidou.keys():
                        Beidou[name] = [info]
                    else:
                        Beidou[name].append(info)
                elif info[0][1] == 'J':
                    if 'Qzss' not in systems:
                        systems.append('Qzss')
                        checkvar.append(BooleanVar())
                    name = info[0]
                    info = info[1:4]
                    info.insert(0,indexTime)
                    if name not in Qzss.keys():
                        Qzss[name] = [info]
                    else:
                        Qzss[name].append(info)
        
            
        tk_elements = [Label(root, text='Choose the system', font=('Consolas', 20))]
        for i in range(len(systems)):
            tk_elements.append(Checkbutton(root, text=systems[i], variable=checkvar[i], onvalue=1, offvalue=0))
        tk_elements.append(Button(root, text="Next", command=choose_satelities))
        for i in range(len(tk_elements)):
            tk_elements[i].grid(column=0, row=i)

       
def choose_satelities():
    global tk_elements_2, buttons, all_satellites, proverka
    systems_for_draw = []
    all_satellites = []
    proverka = []
    buttons = []
    for i in tk_elements:
        i.destroy()
    tk_elements_2 = [Label(root, text='Choose the satellite', font=('Consolas', 20))]
    
    for i in range(len(checkvar)):
        if checkvar[i].get():
            systems_for_draw.append(systems[i])
    for i in range(len(systems_for_draw)):
        tk_elements_2.append(Label(root, text=systems_for_draw[i]))
        buttons.append(BooleanVar())
        tk_elements_2.append(Checkbutton(root, text='Choose all', variable=buttons[i], onvalue=1, offvalue=0, command=choose_all)) # [bv, bv, bv]
        satellites= list(map(str, SystemsNames[systems_for_draw[i]].keys()))
        all_satellites.append(satellites)
        proverka.append([])
        for j in range(len(satellites)):
            proverka[i].append(BooleanVar()) 
            tk_elements_2.append(Checkbutton(root, text=satellites[j], variable=proverka[i][j], onvalue=1,
                                             offvalue=0))
    tk_elements_2.append(Button(root, text="Next", command=choose_time))
    a = 1
    m = 1
    tk_elements_2[0].grid(column=0, row=0)
    for i in range(len(all_satellites)):
        b = 1
        for j in range(a, len(all_satellites[i]) + a + 2):
            tk_elements_2[j].grid(column=i, row=b)
            a += 1
            b += 1
        m = max(m, b)
    
    tk_elements_2[-1].grid(column=len(all_satellites)- 1, row=m+1)

def choose_all():
    a = 1
    for i in range(len(buttons)):
        if buttons[i].get():
            a += 2
            for j in range(a, len(all_satellites[i]) + a):
                tk_elements_2[j].select()
                a += 1
        else:
            a += len(all_satellites[i]) + 2

root = Tk()          
selected = IntVar()
labels = [Label(root, text='Choose the file', font=('Consolas', 20))]
filenames = []
for filename in os.scandir('navdata'):
    if filename.is_file():
        filenames.append(filename.path)
for i in range(len(filenames)):
    labels.append(Radiobutton(root, text=filenames[i][8:], value=i, variable=selected))
labels.append(Button(root, text="Next", command=render))
for i in range(len(labels)):
    labels[i].grid(column=i, row=0)


def pre_draw():
    global SatellitesForDraw, root, SystemForDraw  # Список выбранных спутников
   
    for i in range(len(all_satellites)):   # [[], []]
        for s in range(len(all_satellites[i])):
            if proverka[i][s].get():
                SatellitesForDraw.append(all_satellites[i][s])
    draw(SatellitesForDraw)

    root.destroy()
def choose_time():
    global tk_elements_3, f_var, s_var,NormalDate, cmb_f, cmb_s
    for widget in tk_elements_2:
        widget.destroy()
    for i in range(len(NormalDate)):
        NormalDate[i] = f"{NormalDate[i][0]}:{NormalDate[i][1]}:{str(NormalDate[i][2])[:len(str(NormalDate[i][2]))-2]} {NormalDate[i][3]}.{NormalDate[i][4]}"
    s_var = StringVar(value=NormalDate[0])
    tk_elements_3 = [Label(root, text="Choose th time"),Label(root, text=f"since {NormalDate[0]}.{start_date[2]} "),Label(root, text=f"to {NormalDate[-1]}.{finish_date[2]} ")]
    cmb_s = ttk.Combobox(textvariable=s_var, values=NormalDate, state="readonly")
    f_var = StringVar(value=NormalDate[0])
    cmb_f = ttk.Combobox(textvariable=f_var, values=NormalDate, state="readonly")
    cmb_f.bind("<<ComboboxSelected>>", select);cmb_s.bind("<<ComboboxSelected>>", select)
    tk_elements_3.append(cmb_s);tk_elements_3.append(cmb_f)
    tk_elements_3[0].grid(column=0, row=0);tk_elements_3[1].grid(column=0, row=1);tk_elements_3[2].grid(column=1, row=1);tk_elements_3[3].grid(column=0, row=2);tk_elements_3[4].grid(column=1, row=2)


def select(obj):
    global error_text,W,cmb_s,cmb_f, NormalDate,finish, start
    a = 0
    i = 0
    for w in W:
        w.destroy()
        W.remove(w)
    if NormalDate.index(cmb_f.get()) > NormalDate.index(cmb_s.get()):
        error_text = "Ok"
        a = 1
    else:
        error_text = "Check the correct of your choose"
        a = 0
    W.append(Label(root, text=error_text))
    if a:
        W.append(Button(root, text="Next", command=pre_draw))
        start = NormalDate.index(cmb_s.get())
        finish = NormalDate.index(cmb_f.get())
    for w in W:
        w.grid(column=i, row=3)
        i += 1

root.mainloop()