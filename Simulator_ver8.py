import pandas as pd
import numpy as np
import datetime
import codecs
import MyModules #別ファイル
import random
import os.path
import sys
import main6 #別ファイル
import tkinter
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import decimal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


#plt.style.use('dark_background')
plt.style.use('dark_background_green.mplstyle')

main_win = tkinter.Tk()
main_win.title("電力コスト計算シミュレータ")
main_win.geometry("1100x580")
main_win.configure(bg='green')

main_frm = Frame(main_win,width=1050, height=550,bg = "green")
main_frm.grid(column=0, row=0, sticky=tkinter.NSEW, padx=5, pady=10)

ave = []
std = []
InputList = []

#ttkのスタイル
noteStyler = ttk.Style()




#ボタンで動く関数たち

def owari():
    sys.exit()

def reset():
    ave.clear()
    std.clear()
    InputList.clear()
    for j in answers:
        j.delete(0,tkinter.END)

def calculate():
    ax.clear()
    TermInput = int(flg1.get())
    if TermInput == 1:
        Term = "2week"
    elif TermInput == 2:
        Term = "2month"
    elif TermInput == 3:
        Term = "6month"
    elif TermInput == 4:
        Term = "1year"

    AlgoInput = int(flg2.get())
    if AlgoInput == 1:
        Algo = "decision"
    elif AlgoInput == 2:
        Algo = "neural"
    elif AlgoInput == 3:
        Algo = "timeseries"
    if bln_csv.get():
        Number_csv_M = str(int(list_csv.get())*2 -1)
        Number_csv_N =str(int(list_csv.get())*2)
        PurChasePol = pd.read_csv('Rule.csv',index_col='month')
        AitaiM = PurChasePol[Number_csv_M].values.tolist()
        AitaiN = PurChasePol[Number_csv_N].values.tolist()
        AitaiM = list(map(int,AitaiM))
        AitaiN = list(map(int,AitaiN))
    else:
        AitaiM = []
        for i in range(0,12):
            AitaiM.append(list_Items1[i].get())
        AitaiN = []
        for i in range(0,12):
            AitaiN.append(list_Items2[i].get())
    AverageCost,StandardCost = main6.main(Algo,Term,AitaiM,AitaiN)
    ave.append(AverageCost)
    std.append(StandardCost)
    names = np.array( ["Input%d"%i for i in range(len(ave))]) #ここも変える
    sc = plt.scatter(std,ave)
    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points", arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)
    ax.set_xlabel("annual erectricity cost standard[yen/kwh]")
    ax.set_ylabel("annual erectricity cost average[yen/kwh]")
    def update_annot(ind):
        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        text = "{}".format(" ".join([names[n] for n in ind["ind"]]))
        annot.set_text(text)

    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax and event.button is None: # 上下移動や虫眼鏡のドラッグ中は探さない
            cont, ind = sc.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()
    currentinput.insert(0,["Input" + str(len(ave)-1),Term,Algo,AitaiM,AitaiN])
    if len(InputList) > 10:
        for j in range(10):
            answers[j].insert(0,InputList[j])
    else:
        for j in range(len(InputList)):
            answers[j].insert(0,InputList[j])
    InputList.append(["Input" + str(len(ave)-1),Term,Algo,AitaiM,AitaiN])
    
    cnt = 1
    # hoverイベントを追加


    fig.canvas.mpl_connect("motion_notify_event", hover)
    fig.tight_layout()
    #ax.plot(x,y)
    canvas.draw()
    canvas.get_tk_widget().pack()
    OutputMonthlyCost()
    OutputDailyCost()
    OutputMonthlyInb()
    OutputDailyInb()
    #


#月次電力コストグラフ出力
def OutputMonthlyCost():
    ax_CostMonthly.clear()
    if bln_csv.get():
        Number_csv_M = str(int(list_csv.get())*2 -1)
        Number_csv_N =str(int(list_csv.get())*2)
        PurChasePol = pd.read_csv('Rule.csv',index_col='month')

        AitaiM = PurChasePol[Number_csv_M].values.tolist()
        AitaiN = PurChasePol[Number_csv_N].values.tolist()

        AitaiM = list(map(int,AitaiM))
        AitaiN = list(map(int,AitaiN))
    else:
        AitaiM = []
        for i in range(0,12):
            AitaiM.append(list_Items1[i].get())
        AitaiN = []
        for i in range(0,12):
            AitaiN.append(list_Items2[i].get())

    ax_CostMonthly.clear()
    Input_CostMonthly = int(CostMonthlyFlg.get())
    TermInput = int(flg1.get())
    if TermInput == 1:
        Term = "2week"
    elif TermInput == 2:
        Term = "2month"
    elif TermInput == 3:
        Term = "6month"
    elif TermInput == 4:
        Term = "1year"

    AlgoInput = int(flg2.get())
    if AlgoInput == 1:
        Algo = "decision"
    elif AlgoInput == 2:
        Algo = "neural"
    elif AlgoInput == 3:
        Algo = "timeseries"

    #Mの分データ取得
    FileName_MC_pre = Term + "_" + Algo + "_Tokyo_"
    FileName_MC_M = FileName_MC_pre + str(Input_CostMonthly) + "_" + str(AitaiM[Input_CostMonthly - 1])+"_M" + ".csv"
    FileDir_MC_M = str(Term) + "_" + str(Algo) + "_Tokyo_M/"
    FilePath_soutai_MC_M = '../scenarios/'+ FileDir_MC_M + FileName_MC_M
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_MC_M = os.path.normpath(os.path.join(base, FilePath_soutai_MC_M))

    data1 = pd.read_csv(FilePath_MC_M,header = None, encoding="shift-jis").values.tolist()

    #Nの分データ
    FileName_MC_N = FileName_MC_pre + str(Input_CostMonthly) + "_" + str(AitaiN[Input_CostMonthly - 1])+"_N" + ".csv"
    FileDir_MC_N = str(Term) + "_" + str(Algo) + "_Tokyo_N/"
    FilePath_soutai_MC_N = '../scenarios/'+ FileDir_MC_N + FileName_MC_N
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_MC_N = os.path.normpath(os.path.join(base, FilePath_soutai_MC_N))

    data2 = pd.read_csv(FilePath_MC_N,header = None, encoding="shift-jis").values.tolist()

    SceMC= []

    
    for i in range(4):
        CurrentSceMC = []
        days = int(len(data1[i])/25)
        NumDays = [k+1 for k in range(days)]
        #NumDays = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
        for j in range(days):
            day = []
            StartM = j * 25
            StartN = j * 23                        
            MC_N1 = data2[i][StartN:(StartN + 15)]
            day.extend(MC_N1)
            MC_M = data1[i][StartM:(StartM + 25)]
            day.extend(MC_M)
            MC_N2 = data2[i][(StartN + 15):(StartN + 23)]
            day.extend(MC_N2)
            CurrentSceMC.append((sum(day)/48))
        SceMC.append(CurrentSceMC)
    for i in range(4):
        ax_CostMonthly.plot(NumDays,SceMC[i])
        
    ax_CostMonthly.set_xlabel("Day")
    ax_CostMonthly.set_ylabel("erectricity cost[yen/kwh]")
    ax_CostMonthly.set_ylim(8, 16)
    canvas_CostMonthly.draw()
    canvas_CostMonthly.get_tk_widget().pack()

#1シナリオのみ
def OutputMonthlyCost_1():
    ax_CostMonthly.clear()
    if bln_csv.get():
        Number_csv_M = str(int(list_csv.get())*2 -1)
        Number_csv_N =str(int(list_csv.get())*2)
        PurChasePol = pd.read_csv('Rule.csv',index_col='month')

        AitaiM = PurChasePol[Number_csv_M].values.tolist()
        AitaiN = PurChasePol[Number_csv_N].values.tolist()

        AitaiM = list(map(int,AitaiM))
        AitaiN = list(map(int,AitaiN))
    else:
        AitaiM = []
        for i in range(0,12):
            AitaiM.append(list_Items1[i].get())
        AitaiN = []
        for i in range(0,12):
            AitaiN.append(list_Items2[i].get())

    ax_CostMonthly.clear()
    Input_CostMonthly = int(CostMonthlyFlg.get())
    TermInput = int(flg1.get())
    if TermInput == 1:
        Term = "2week"
    elif TermInput == 2:
        Term = "2month"
    elif TermInput == 3:
        Term = "6month"
    elif TermInput == 4:
        Term = "1year"

    AlgoInput = int(flg2.get())
    if AlgoInput == 1:
        Algo = "decision"
    elif AlgoInput == 2:
        Algo = "neural"
    elif AlgoInput == 3:
        Algo = "timeseries"

    #Mの分データ取得
    FileName_MC_pre = Term + "_" + Algo + "_Tokyo_"
    FileName_MC_M = FileName_MC_pre + str(Input_CostMonthly) + "_" + str(AitaiM[Input_CostMonthly - 1])+"_act_M" + ".csv"
    FileDir_MC_M = str(Term) + "_" + str(Algo) + "_Tokyo_act_M/"
    FilePath_soutai_MC_M = '../scenarios/'+ FileDir_MC_M + FileName_MC_M
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_MC_M = os.path.normpath(os.path.join(base, FilePath_soutai_MC_M))

    data1 = pd.read_csv(FilePath_MC_M,header = None, encoding="shift-jis").values.tolist()

    #Nの分データ
    FileName_MC_N = FileName_MC_pre + str(Input_CostMonthly) + "_" + str(AitaiN[Input_CostMonthly - 1])+"_act_N" + ".csv"
    FileDir_MC_N = str(Term) + "_" + str(Algo) + "_Tokyo_act_N/"
    FilePath_soutai_MC_N = '../scenarios/'+ FileDir_MC_N + FileName_MC_N
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_MC_N = os.path.normpath(os.path.join(base, FilePath_soutai_MC_N))

    data2 = pd.read_csv(FilePath_MC_N,header = None, encoding="shift-jis").values.tolist()

    SceMC= []

    
    days = int(len(data1[0])/25)
    NumDays = [k+1 for k in range(days)]
    #NumDays = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
    for j in range(days):
        day = []
        StartM = j * 25
        StartN = j * 23                        
        MC_N1 = data2[0][StartN:(StartN + 15)]
        day.extend(MC_N1)
        MC_M = data1[0][StartM:(StartM + 25)]
        day.extend(MC_M)
        MC_N2 = data2[0][(StartN + 15):(StartN + 23)]
        day.extend(MC_N2)
        SceMC.append((sum(day)/48))
 
    ax_CostMonthly.plot(NumDays,SceMC,marker='o')
    ax_CostMonthly.set_xlabel("Day")
    ax_CostMonthly.set_ylabel("erectricity cost[yen/kwh]")
    ax_CostMonthly.set_ylim(8, 16)
    canvas_CostMonthly.draw()
    canvas_CostMonthly.get_tk_widget().pack()


#日次電力コストグラフ出力
def OutputDailyCost():
    ax_CostDaily.clear()
    AitaiM = []
    if bln_csv.get():
        Number_csv_M = str(int(list_csv.get())*2 -1)
        Number_csv_N =str(int(list_csv.get())*2)
        PurChasePol = pd.read_csv('Rule.csv',index_col='month')
        AitaiM = PurChasePol[Number_csv_M].values.tolist()
        AitaiN = PurChasePol[Number_csv_N].values.tolist()

        AitaiM = list(map(int,AitaiM))
        AitaiN = list(map(int,AitaiN))
    else:
        AitaiM = []
        for i in range(0,12):
            AitaiM.append(list_Items1[i].get())
        AitaiN = []
        for i in range(0,12):
            AitaiN.append(list_Items2[i].get())

    Input_CostDaily = int(CostDailyFlg.get())
    TermInput = int(flg1.get())
    if TermInput == 1:
        Term = "2week"
    elif TermInput == 2:
        Term = "2month"
    elif TermInput == 3:
        Term = "6month"
    elif TermInput == 4:
        Term = "1year"

    AlgoInput = int(flg2.get())
    if AlgoInput == 1:
        Algo = "decision"
    elif AlgoInput == 2:
        Algo = "neural"
    elif AlgoInput == 3:
        Algo = "timeseries"

    #Mの分データ取得
    FileName_DC_pre = Term + "_" + Algo + "_Tokyo_"
    FileName_DC_M = FileName_DC_pre + str(Input_CostDaily) + "_" + str(AitaiM[Input_CostDaily - 1])+"_M" + ".csv"
    FileDir_DC_M = str(Term) + "_" + str(Algo) + "_Tokyo_M/"
    FilePath_soutai_DC_M = '../scenarios/'+ FileDir_DC_M + FileName_DC_M
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_DC_M = os.path.normpath(os.path.join(base, FilePath_soutai_DC_M))
    data1 = pd.read_csv(FilePath_DC_M,header = None, encoding="shift-jis").values.tolist()

    #Nの分データ
    FileName_DC_N = FileName_DC_pre + str(Input_CostDaily) + "_" + str(AitaiN[Input_CostDaily - 1])+"_N" + ".csv"
    FileDir_DC_N = str(Term) + "_" + str(Algo) + "_Tokyo_N/"
    FilePath_soutai_DC_N = '../scenarios/'+ FileDir_DC_N + FileName_DC_N
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_DC_N = os.path.normpath(os.path.join(base, FilePath_soutai_DC_N))
    data2 = pd.read_csv(FilePath_DC_N,header = None, encoding="shift-jis").values.tolist()

    SceDC= []

    
    for i in range(4):
        hours = 48
        Numhours = [i+1 for i in range(hours)]
        DateForC = 19
        #NumDays = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
        day = []
        StartM = DateForC * 25
        StartN = DateForC * 23              
        DC_N1 = data2[i][StartN:(StartN + 15)]
        day.extend(DC_N1)
        DC_M = data1[i][StartM:(StartM + 25)]
        day.extend(DC_M)
        DC_N2 = data2[i][(StartN + 15):(StartN + 23)]
        day.extend(DC_N2)
        SceDC.append(day)
    for i in range(4):
        ax_CostDaily.plot(Numhours,SceDC[i])
        
    ax_CostDaily.set_xlabel("timeslot")
    ax_CostDaily.set_ylabel("erectricity cost[yen/kwh]")
    ax_CostDaily.set_ylim(5, 20)
    canvas_CostDaily.draw()
    canvas_CostDaily.get_tk_widget().pack()


def OutputDailyCost_1():
    ax_CostDaily.clear()
    AitaiM = []
    if bln_csv.get():
        Number_csv_M = str(int(list_csv.get())*2 -1)
        Number_csv_N =str(int(list_csv.get())*2)
        PurChasePol = pd.read_csv('Rule.csv',index_col='month')
        AitaiM = PurChasePol[Number_csv_M].values.tolist()
        AitaiN = PurChasePol[Number_csv_N].values.tolist()

        AitaiM = list(map(int,AitaiM))
        AitaiN = list(map(int,AitaiN))
    else:
        AitaiM = []
        for i in range(0,12):
            AitaiM.append(list_Items1[i].get())
        AitaiN = []
        for i in range(0,12):
            AitaiN.append(list_Items2[i].get())

    Input_CostDaily = int(CostDailyFlg.get())
    TermInput = int(flg1.get())
    if TermInput == 1:
        Term = "2week"
    elif TermInput == 2:
        Term = "2month"
    elif TermInput == 3:
        Term = "6month"
    elif TermInput == 4:
        Term = "1year"

    AlgoInput = int(flg2.get())
    if AlgoInput == 1:
        Algo = "decision"
    elif AlgoInput == 2:
        Algo = "neural"
    elif AlgoInput == 3:
        Algo = "timeseries"

    #Mの分データ取得
    FileName_DC_pre = Term + "_" + Algo + "_Tokyo_"
    FileName_DC_M = FileName_DC_pre + str(Input_CostDaily) + "_" + str(AitaiM[Input_CostDaily - 1])+"_act_M" + ".csv"
    FileDir_DC_M = str(Term) + "_" + str(Algo) + "_Tokyo_act_M/"
    FilePath_soutai_DC_M = '../scenarios/'+ FileDir_DC_M + FileName_DC_M
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_DC_M = os.path.normpath(os.path.join(base, FilePath_soutai_DC_M))
    data1 = pd.read_csv(FilePath_DC_M,header = None, encoding="shift-jis").values.tolist()

    #Nの分データ
    FileName_DC_N = FileName_DC_pre + str(Input_CostDaily) + "_" + str(AitaiN[Input_CostDaily - 1])+"_act_N" + ".csv"
    FileDir_DC_N = str(Term) + "_" + str(Algo) + "_Tokyo_act_N/"
    FilePath_soutai_DC_N = '../scenarios/'+ FileDir_DC_N + FileName_DC_N
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_DC_N = os.path.normpath(os.path.join(base, FilePath_soutai_DC_N))
    data2 = pd.read_csv(FilePath_DC_N,header = None, encoding="shift-jis").values.tolist()

    SceDC= []

    
    hours = 48
    Numhours = [i+1 for i in range(hours)]
    DateForC = 19
    #NumDays = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
    StartM = DateForC * 25
    StartN = DateForC * 23                        
    DC_N1 = data2[0][StartN:(StartN + 15)]
    SceDC.extend(DC_N1)
    DC_M = data1[0][StartM:(StartM + 25)]
    SceDC.extend(DC_M)
    DC_N2 = data2[0][(StartN + 15):(StartN + 23)]
    SceDC.extend(DC_N2)
    ax_CostDaily.plot(Numhours,SceDC,marker='o')    
    ax_CostDaily.set_xlabel("timeslot")
    ax_CostDaily.set_ylabel("erectricity cost[yen/kwh]")
    ax_CostDaily.set_ylim(5, 20)
    canvas_CostDaily.draw()
    canvas_CostDaily.get_tk_widget().pack()


#月次インバランスグラフ出力
def OutputMonthlyInb():
    ax_InbMonthly.clear()
    AitaiM = []
    if bln_csv.get():
        Number_csv_M = str(int(list_csv.get())*2 -1)
        Number_csv_N =str(int(list_csv.get())*2)
        PurChasePol = pd.read_csv('Rule.csv',index_col='month')
        AitaiM = PurChasePol[Number_csv_M].values.tolist()
        AitaiN = PurChasePol[Number_csv_N].values.tolist()
        AitaiM = list(map(int,AitaiM))
        AitaiN = list(map(int,AitaiN))
    else:
        AitaiM = []
        for i in range(0,12):
            AitaiM.append(list_Items1[i].get())
        AitaiN = []
        for i in range(0,12):
            AitaiN.append(list_Items2[i].get())
    ax_InbMonthly.clear()
    Input_InbMonthly = int(InbMonthlyFlg.get())
    TermInput = int(flg1.get())
    if TermInput == 1:
        Term = "2week"
    elif TermInput == 2:
        Term = "2month"
    elif TermInput == 3:
        Term = "6month"
    elif TermInput == 4:
        Term = "1year"

    AlgoInput = int(flg2.get())
    if AlgoInput == 1:
        Algo = "decision"
    elif AlgoInput == 2:
        Algo = "neural"
    elif AlgoInput == 3:
        Algo = "timeseries"

    #Mの分データ取得
    FileName_MI_pre = "Inb_" + Term + "_" + Algo + "_Tokyo_"
    FileName_MI_M = FileName_MI_pre + str(Input_InbMonthly) + "_" + str(AitaiM[Input_InbMonthly - 1])+"_M" + ".csv"
    FileDir_MI_M = "inb_" + str(Term) + "_" + str(Algo) + "_Tokyo_M/"
    FilePath_soutai_MI_M = '../scenarios/'+ FileDir_MI_M + FileName_MI_M
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_MI_M = os.path.normpath(os.path.join(base, FilePath_soutai_MI_M))
    data1 = pd.read_csv(FilePath_MI_M,header = None, encoding="shift-jis").values.tolist()

    #Nの分データ
    FileName_MI_N = FileName_MI_pre + str(Input_InbMonthly) + "_" + str(AitaiN[Input_InbMonthly - 1])+"_N" + ".csv"
    FileDir_MI_N = "inb_" + str(Term) + "_" + str(Algo) + "_Tokyo_N/"
    FilePath_soutai_MI_N = '../scenarios/'+ FileDir_MI_N + FileName_MI_N
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_MI_N = os.path.normpath(os.path.join(base, FilePath_soutai_MI_N))
    data2 = pd.read_csv(FilePath_MI_N,header = None, encoding="shift-jis").values.tolist()

    SceMI= []

    
    for i in range(4):
        CurrentSceMI = []
        days = int(len(data1[i])/25)
        NumDays = [i+1 for i in range(days)]
        #NumDays = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
        for j in range(days):
            day = []
            StartM = j * 25
            StartN = j * 23                        
            MI_N1 = data2[i][StartN:(StartN + 15)]
            day.extend(MI_N1)
            MI_M = data1[i][StartM:(StartM + 25)]
            day.extend(MI_M)
            MI_N2 = data2[i][(StartN + 15):(StartN + 23)]
            day.extend(MI_N2)
            CurrentSceMI.append(sum(day))
        SceMI.append(CurrentSceMI)
    for i in range(4):
        ax_InbMonthly.plot(NumDays,SceMI[i])
        
    ax_InbMonthly.set_xlabel("Day")
    ax_InbMonthly.set_ylabel("Loss Anount[thousand yen]")
    ax_InbMonthly.set_ylim(0, 150000)
    canvas_InbMonthly.draw()
    canvas_InbMonthly.get_tk_widget().pack()

def OutputMonthlyInb_1():
    ax_InbMonthly.clear()
    AitaiM = []
    if bln_csv.get():
        Number_csv_M = str(int(list_csv.get())*2 -1)
        Number_csv_N =str(int(list_csv.get())*2)
        PurChasePol = pd.read_csv('Rule.csv',index_col='month')
        AitaiM = PurChasePol[Number_csv_M].values.tolist()
        AitaiN = PurChasePol[Number_csv_N].values.tolist()
        AitaiM = list(map(int,AitaiM))
        AitaiN = list(map(int,AitaiN))
    else:
        AitaiM = []
        for i in range(0,12):
            AitaiM.append(list_Items1[i].get())
        AitaiN = []
        for i in range(0,12):
            AitaiN.append(list_Items2[i].get())
    ax_InbMonthly.clear()
    Input_InbMonthly = int(InbMonthlyFlg.get())
    TermInput = int(flg1.get())
    if TermInput == 1:
        Term = "2week"
    elif TermInput == 2:
        Term = "2month"
    elif TermInput == 3:
        Term = "6month"
    elif TermInput == 4:
        Term = "1year"

    AlgoInput = int(flg2.get())
    if AlgoInput == 1:
        Algo = "decision"
    elif AlgoInput == 2:
        Algo = "neural"
    elif AlgoInput == 3:
        Algo = "timeseries"

    #Mの分データ取得
    FileName_MI_pre = "Inb_" + Term + "_" + Algo + "_Tokyo_"
    FileName_MI_M = FileName_MI_pre + str(Input_InbMonthly) + "_" + str(AitaiM[Input_InbMonthly - 1])+"_act_M" + ".csv"
    FileDir_MI_M = "inb_" + str(Term) + "_" + str(Algo) + "_Tokyo_act_M/"
    FilePath_soutai_MI_M = '../scenarios/'+ FileDir_MI_M + FileName_MI_M
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_MI_M = os.path.normpath(os.path.join(base, FilePath_soutai_MI_M))
    data1 = pd.read_csv(FilePath_MI_M,header = None, encoding="shift-jis").values.tolist()

    #Nの分データ
    FileName_MI_N = FileName_MI_pre + str(Input_InbMonthly) + "_" + str(AitaiN[Input_InbMonthly - 1])+"_act_N" + ".csv"
    FileDir_MI_N = "inb_" + str(Term) + "_" + str(Algo) + "_Tokyo_act_N/"
    FilePath_soutai_MI_N = '../scenarios/'+ FileDir_MI_N + FileName_MI_N
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_MI_N = os.path.normpath(os.path.join(base, FilePath_soutai_MI_N))
    data2 = pd.read_csv(FilePath_MI_N,header = None, encoding="shift-jis").values.tolist()

    SceMI= []

    days = int(len(data1[0])/25)
    NumDays = [i+1 for i in range(days)]
    #NumDays = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
    for j in range(days):
        day = []
        StartM = j * 25
        StartN = j * 23                        
        MI_N1 = data2[0][StartN:(StartN + 15)]
        day.extend(MI_N1)
        MI_M = data1[0][StartM:(StartM + 25)]
        day.extend(MI_M)
        MI_N2 = data2[0][(StartN + 15):(StartN + 23)]
        day.extend(MI_N2)
        SceMI.append(sum(day))
    ax_InbMonthly.plot(NumDays,SceMI,marker='o')
    ax_InbMonthly.set_xlabel("Day")
    ax_InbMonthly.set_ylabel("Loss Anount[thousand yen]")
    ax_InbMonthly.set_ylim(0, 150000)
    canvas_InbMonthly.draw()
    canvas_InbMonthly.get_tk_widget().pack()



#日次インバランスグラフ出力
def OutputDailyInb():
    ax_InbDaily.clear()
    AitaiM = []
    if bln_csv.get():
        Number_csv_M = str(int(list_csv.get())*2 -1)
        Number_csv_N =str(int(list_csv.get())*2)
        PurChasePol = pd.read_csv('Rule.csv',index_col='month')
        AitaiM = PurChasePol[Number_csv_M].values.tolist()
        AitaiN = PurChasePol[Number_csv_N].values.tolist()
        AitaiM = list(map(int,AitaiM))
        AitaiN = list(map(int,AitaiN))
    else:
        AitaiM = []
        for i in range(0,12):
            AitaiM.append(list_Items1[i].get())
        AitaiN = []
        for i in range(0,12):
            AitaiN.append(list_Items2[i].get())
    ax_InbDaily.clear()
    Input_InbDaily = int(InbDailyFlg.get())
    TermInput = int(flg1.get())
    if TermInput == 1:
        Term = "2week"
    elif TermInput == 2:
        Term = "2month"
    elif TermInput == 3:
        Term = "6month"
    elif TermInput == 4:
        Term = "1year"

    AlgoInput = int(flg2.get())
    if AlgoInput == 1:
        Algo = "decision"
    elif AlgoInput == 2:
        Algo = "neural"
    elif AlgoInput == 3:
        Algo = "timeseries"

    #Mの分データ取得
    FileName_DI_pre = "Inb_" + Term + "_" + Algo + "_Tokyo_"
    FileName_DI_M = FileName_DI_pre + str(Input_InbDaily) + "_" + str(AitaiM[Input_InbDaily - 1])+"_M" + ".csv"
    FileDir_DI_M = "inb_" + str(Term) + "_" + str(Algo) + "_Tokyo_M/"
    FilePath_soutai_DI_M = '../scenarios/'+ FileDir_DI_M + FileName_DI_M
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_DI_M = os.path.normpath(os.path.join(base, FilePath_soutai_DI_M))
    data1 = pd.read_csv(FilePath_DI_M,header = None, encoding="shift-jis").values.tolist()

    #Nの分データ
    FileName_DI_N = FileName_DI_pre + str(Input_InbDaily) + "_" + str(AitaiN[Input_InbDaily - 1])+"_N" + ".csv"
    FileDir_DI_N = "inb_" + str(Term) + "_" + str(Algo) + "_Tokyo_N/"
    FilePath_soutai_DI_N = '../scenarios/'+ FileDir_DI_N + FileName_DI_N
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_DI_N = os.path.normpath(os.path.join(base, FilePath_soutai_DI_N))
    data2 = pd.read_csv(FilePath_DI_N,header = None, encoding="shift-jis").values.tolist()

    SceDI= []

    
    for i in range(4):
        hours = 48
        Numhours = [i+1 for i in range(hours)]
        DateForC = 19
        day = []
        StartM = DateForC * 25
        StartN = DateForC * 23                        
        DI_N1 = data2[i][StartN:(StartN + 15)]
        day.extend(DI_N1)
        DI_M = data1[i][StartM:(StartM + 25)]
        day.extend(DI_M)
        DI_N2 = data2[i][(StartN + 15):(StartN + 23)]
        day.extend(DI_N2)
        SceDI.append(day)
    for i in range(4):
        ax_InbDaily.plot(Numhours,SceDI[i])
        
    ax_InbDaily.set_xlabel("Time")
    ax_InbDaily.set_ylabel("Loss Anount[thousand yen]")
    ax_InbDaily.set_ylim(0, 10000)
    canvas_InbDaily.draw()
    canvas_InbDaily.get_tk_widget().pack()

def OutputDailyInb_1():
    ax_InbDaily.clear()
    AitaiM = []
    if bln_csv.get():
        Number_csv_M = str(int(list_csv.get())*2 -1)
        Number_csv_N =str(int(list_csv.get())*2)
        PurChasePol = pd.read_csv('Rule.csv',index_col='month')
        AitaiM = PurChasePol[Number_csv_M].values.tolist()
        AitaiN = PurChasePol[Number_csv_N].values.tolist()
        AitaiM = list(map(int,AitaiM))
        AitaiN = list(map(int,AitaiN))
    else:
        AitaiM = []
        for i in range(0,12):
            AitaiM.append(list_Items1[i].get())
        AitaiN = []
        for i in range(0,12):
            AitaiN.append(list_Items2[i].get())
    ax_InbDaily.clear()
    Input_InbDaily = int(InbDailyFlg.get())
    TermInput = int(flg1.get())
    if TermInput == 1:
        Term = "2week"
    elif TermInput == 2:
        Term = "2month"
    elif TermInput == 3:
        Term = "6month"
    elif TermInput == 4:
        Term = "1year"

    AlgoInput = int(flg2.get())
    if AlgoInput == 1:
        Algo = "decision"
    elif AlgoInput == 2:
        Algo = "neural"
    elif AlgoInput == 3:
        Algo = "timeseries"

    #Mの分データ取得
    FileName_DI_pre = "Inb_" + Term + "_" + Algo + "_Tokyo_"
    FileName_DI_M = FileName_DI_pre + str(Input_InbDaily) + "_" + str(AitaiM[Input_InbDaily - 1])+"_act_M" + ".csv"
    FileDir_DI_M = "inb_" + str(Term) + "_" + str(Algo) + "_Tokyo_act_M/"
    FilePath_soutai_DI_M = '../scenarios/'+ FileDir_DI_M + FileName_DI_M
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_DI_M = os.path.normpath(os.path.join(base, FilePath_soutai_DI_M))
    data1 = pd.read_csv(FilePath_DI_M,header = None, encoding="shift-jis").values.tolist()

    #Nの分データ
    FileName_DI_N = FileName_DI_pre + str(Input_InbDaily) + "_" + str(AitaiN[Input_InbDaily - 1])+"_act_N" + ".csv"
    FileDir_DI_N = "inb_" + str(Term) + "_" + str(Algo) + "_Tokyo_act_N/"
    FilePath_soutai_DI_N = '../scenarios/'+ FileDir_DI_N + FileName_DI_N
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_DI_N = os.path.normpath(os.path.join(base, FilePath_soutai_DI_N))
    data2 = pd.read_csv(FilePath_DI_N,header = None, encoding="shift-jis").values.tolist()

    SceDI= []

    hours = 48
    Numhours = [i+1 for i in range(hours)]
    DateForC = 19
    StartM = DateForC * 25
    StartN = DateForC * 23                        
    DI_N1 = data2[0][StartN:(StartN + 15)]
    SceDI.extend(DI_N1)
    DI_M = data1[0][StartM:(StartM + 25)]
    SceDI.extend(DI_M)
    DI_N2 = data2[0][(StartN + 15):(StartN + 23)]
    SceDI.extend(DI_N2)
    print(SceDI)
    ax_InbDaily.plot(Numhours,SceDI,marker='o')    
    ax_InbDaily.set_xlabel("Time")
    ax_InbDaily.set_ylabel("Loss Anount[thousand yen]")
    ax_InbDaily.set_ylim(0, 10000)
    canvas_InbDaily.draw()
    canvas_InbDaily.get_tk_widget().pack()

                       
#入力のラベル

lf1 = LabelFrame(
    main_frm, 
    text='TrainingTerm',
    #padding=5,
    foreground='white',
    background = "green",
    width=200, height=50)
lf1.place(x = 30,y = 30)
lf1.propagate(False)

lf2 = LabelFrame(
    main_frm,
    text='Algorithm',bg = "green",foreground='white',
    #padding=5,
    width=200, height=50)
lf2.place(x = 30,y = 110)
lf2.propagate(False)

#グループA用変数
flg1 = StringVar()

#グループB用変数
flg2 = StringVar()

#ラジオ1（グループA）  
rb1 = ttk.Radiobutton(lf1,text='2weeks',value=1,variable=flg1)
rb1.grid(row=0,column=0)

#ラジオ2（グループA）
rb2 = ttk.Radiobutton(lf1,text='2months',value=2,variable=flg1)
rb2.grid(row=0,column=1)

#ラジオ3（グループA）
rb3 = ttk.Radiobutton(lf1,text='6months',value=3,variable=flg1)
rb3.grid(row=0,column=2)

#ラジオ4（グループA）
rb4 = ttk.Radiobutton(lf1,text='1year',value=4,variable=flg1)
rb4.grid(row=0,column=3)

#ラジオ4（グループB）
rb4 = ttk.Radiobutton(lf2,text='DecisionTree',value=1,variable=flg2)
rb4.grid(row=0,column=0)

#ラジオ5（グループB）
rb5 = ttk.Radiobutton(lf2,text='NeuralNetwork',value=2,variable=flg2)
rb5.grid(row=0,column=1)
rb5.state(['disabled'])


#ボタンのラベル


lf3 = LabelFrame(
    main_frm, 
    #padding=5,
    bg = "green",
    width=50, height=150)
run_btn = ttk.Button(lf3, text="実行", command=calculate)
owari_btn = ttk.Button(lf3, text="終了", command=owari)
reset_btn = ttk.Button(lf3, text="リセット", command=reset)
run_btn.grid(column=1, row=0)
owari_btn.grid(column=1, row=1)
reset_btn.grid(column=1, row=2)
lf3.place(x = 330,y = 30)
lf3.propagate(False)


#結果のグラフを描画するラベル


lf4 = LabelFrame(main_frm,text='結果',width=600,bg = "green",foreground='white', height=550)
lf4.place(x = 440, y = 30)
lf4.propagate(False)

#タブ作る

note = ttk.Notebook(lf4)

tab_a = tkinter.Frame(note,height=550,width=600,bg = "green")



#月間コスト用タブ
tab_b = tkinter.Frame(note,height=550,width=600,bg = "green")
tab_b_1 = LabelFrame(tab_b, height=500,width=600,bg = "green")
fig_CostMonthly = plt.figure(figsize=(5, 4))
canvas_CostMonthly = FigureCanvasTkAgg(fig_CostMonthly, master=tab_b_1)
ax_CostMonthly = fig_CostMonthly.add_subplot(111)
tab_b_1.grid(row=0,column=0)

tab_b_p = Frame(tab_b,bg = "green",width=500, height=50)
tab_b_p.grid(row=1,column=0)

tab_b_2 = LabelFrame(tab_b_p,text='月指定',bg = "green",foreground='white',width=500, height=50)
tab_b_2.grid(row=1,column=0)

tab_b_3 = LabelFrame(tab_b_p,text='シナリオ',bg = "green",foreground='white',width=500, height=50)
tab_b_3.grid(row=1,column=1)

CostMonthlyFlg = StringVar()

#ラジオ1（グループA）  
rb1_CostMonthly = ttk.Radiobutton(tab_b_2,text='2月',value=2,variable=CostMonthlyFlg,command=OutputMonthlyCost)
rb1_CostMonthly.grid(row=0,column=0)

#ラジオ2（グループA)
rb2_CostMonthly = ttk.Radiobutton(tab_b_2,text='5月',value=5,variable=CostMonthlyFlg,command=OutputMonthlyCost)
rb2_CostMonthly.grid(row=0,column=1)

#ラジオ3（グループA）
rb3_CostMonthly = ttk.Radiobutton(tab_b_2,text='8月',value=8,variable=CostMonthlyFlg,command=OutputMonthlyCost)
rb3_CostMonthly.grid(row=0,column=2)

#ラジオ4（グループA）
rb4_CostMonthly = ttk.Radiobutton(tab_b_2,text='11月',value=11,variable=CostMonthlyFlg,command=OutputMonthlyCost)
rb4_CostMonthly.grid(row=0,column=3)

CostMonthlyFlg.set(2)

rb_CostMonthly_switch = ttk.Button(tab_b_3,text='2019年',command=OutputMonthlyCost_1)
rb_CostMonthly_switch.grid(row=0,column=0)
rb_CostMonthly_switch_1 = ttk.Button(tab_b_3,text='仮想シナリオ',command=OutputMonthlyCost)
rb_CostMonthly_switch_1.grid(row=0,column=1)




#日次コスト用タブ
tab_c = tkinter.Frame(note,height=550,width=600,bg = "green")
tab_c_1 = LabelFrame(tab_c, height=500,width=600,bg = "green")
fig_CostDaily = plt.figure(figsize=(5, 4))
canvas_CostDaily = FigureCanvasTkAgg(fig_CostDaily, master=tab_c_1)
ax_CostDaily = fig_CostDaily.add_subplot(111)
tab_c_1.grid(row=0,column=0)

tab_c_p = Frame(tab_c,bg = "green",width=500, height=50)
tab_c_p.grid(row=1,column=0)


tab_c_2 = LabelFrame(tab_c_p, text='日指定',bg = "green",foreground='white',width=500, height=50)
tab_c_2.grid(row=1,column=0)

tab_c_3 = LabelFrame(tab_c_p,text='シナリオ',bg = "green",foreground='white',width=500, height=50)
tab_c_3.grid(row=1,column=1)


CostDailyFlg = StringVar()

#ラジオ1（グループA）  
rb1_CostDaily = ttk.Radiobutton(tab_c_2,text='2月20日',value=2,variable=CostDailyFlg,command=OutputDailyCost)
rb1_CostDaily.grid(row=0,column=0)

#ラジオ2（グループA）
rb2_CostDaily = ttk.Radiobutton(tab_c_2,text='5月20日',value=5,variable=CostDailyFlg,command=OutputDailyCost)
rb2_CostDaily.grid(row=0,column=1)

#ラジオ3（グループA）
rb3_CostDaily = ttk.Radiobutton(tab_c_2,text='8月20日',value=8,variable=CostDailyFlg,command=OutputDailyCost)
rb3_CostDaily.grid(row=0,column=2)

#ラジオ4（グループA）
rb4_CostDaily = ttk.Radiobutton(tab_c_2,text='11月20日',value=11,variable=CostDailyFlg,command=OutputDailyCost)
rb4_CostDaily.grid(row=0,column=3)

CostDailyFlg.set(2)



rb_CostDaily_switch = ttk.Button(tab_c_3,text='2019年',command=OutputDailyCost_1)
rb_CostDaily_switch.grid(row=0,column=0)
rb_CostDaily_switch_1 = ttk.Button(tab_c_3,text='仮想シナリオ',command=OutputDailyCost)
rb_CostDaily_switch_1.grid(row=0,column=1)


#月間インバランス用タブ
tab_d = tkinter.Frame(note,height=550,width=600,bg = "green")
tab_d_1 = LabelFrame(tab_d, height=500,width=600,bg = "green")
fig_InbMonthly = plt.figure(figsize=(6, 4))
canvas_InbMonthly = FigureCanvasTkAgg(fig_InbMonthly, master=tab_d_1)
ax_InbMonthly = fig_InbMonthly.add_subplot(111)
tab_d_1.grid(row=0,column=0)

tab_d_p = Frame(tab_d,bg = "green",width=500, height=50)
tab_d_p.grid(row=1,column=0)

tab_d_2 = LabelFrame(tab_d_p, text='月指定',bg = "green",foreground='white',width=500, height=50)
tab_d_2.grid(row=1,column=0)

tab_d_3 = LabelFrame(tab_d_p,text='シナリオ',bg = "green",foreground='white',width=500, height=50)
tab_d_3.grid(row=1,column=1)

InbMonthlyFlg = StringVar()

#ラジオ1（グループA）  
rb1_InbMonthly = ttk.Radiobutton(tab_d_2,text='2月',value=2,variable=InbMonthlyFlg,command=OutputMonthlyInb)
rb1_InbMonthly.grid(row=0,column=0)

#ラジオ2（グループA）
rb2_InbMonthly = ttk.Radiobutton(tab_d_2,text='5月',value=5,variable=InbMonthlyFlg,command=OutputMonthlyInb)
rb2_InbMonthly.grid(row=0,column=1)

#ラジオ3（グループA）
rb3_InbMonthly = ttk.Radiobutton(tab_d_2,text='8月',value=8,variable=InbMonthlyFlg,command=OutputMonthlyInb)
rb3_InbMonthly.grid(row=0,column=2)

#ラジオ4（グループA）
rb4_InbMonthly = ttk.Radiobutton(tab_d_2,text='11月',value=11,variable=InbMonthlyFlg,command=OutputMonthlyInb)
rb4_InbMonthly.grid(row=0,column=3)

InbMonthlyFlg.set(2)



rb_InbMonthly_switch = ttk.Button(tab_d_3,text='2019年',command=OutputMonthlyInb_1)
rb_InbMonthly_switch.grid(row=0,column=0)
rb_InbMonthly_switch_1 = ttk.Button(tab_d_3,text='仮想シナリオ',command=OutputMonthlyInb)
rb_InbMonthly_switch_1.grid(row=0,column=1)





#日次インバランス用タブ
tab_e = tkinter.Frame(note,height=550,bg = "green",width=600)
tab_e_1 = LabelFrame(tab_e, height=500,bg = "green",width=600)
fig_InbDaily = plt.figure(figsize=(5, 4))
canvas_InbDaily = FigureCanvasTkAgg(fig_InbDaily, master=tab_e_1)
ax_InbDaily = fig_InbDaily.add_subplot(111)
tab_e_1.grid(row=0,column=0)

tab_e_p = Frame(tab_e,bg = "green",width=500, height=50)
tab_e_p.grid(row=1,column=0)

tab_e_2 = LabelFrame(tab_e_p, text='日指定',bg = "green",foreground='white',width=500,height=50)
tab_e_2.grid(row=1,column=0)

tab_e_3 = LabelFrame(tab_e_p,text='シナリオ',bg = "green",foreground='white',width=500, height=50)
tab_e_3.grid(row=1,column=1)

InbDailyFlg = StringVar()

#ラジオ1（グループA）  
rb1_InbDaily = ttk.Radiobutton(tab_e_2,text='2月20日',value=2,variable=InbDailyFlg,command=OutputDailyInb)
rb1_InbDaily.grid(row=0,column=0)

#ラジオ2（グループA）
rb2_InbDaily = ttk.Radiobutton(tab_e_2,text='5月20日',value=5,variable=InbDailyFlg,command=OutputDailyInb)
rb2_InbDaily.grid(row=0,column=1)

#ラジオ3（グループA）
rb3_InbDaily = ttk.Radiobutton(tab_e_2,text='8月20日',value=8,variable=InbDailyFlg,command=OutputDailyInb)
rb3_InbDaily.grid(row=0,column=2)

#ラジオ4（グループA）
rb4_InbDaily = ttk.Radiobutton(tab_e_2,text='11月20日',value=11,variable=InbDailyFlg,command=OutputDailyInb)
rb4_InbDaily.grid(row=0,column=3)

InbDailyFlg.set(2)


rb_InbDaily_switch = ttk.Button(tab_e_3,text='2019年',command=OutputDailyInb_1)
rb_InbDaily_switch.grid(row=0,column=0)
rb_InbDaily_switch_1 = ttk.Button(tab_e_3,text='仮想シナリオ',command=OutputDailyInb)
rb_InbDaily_switch_1.grid(row=0,column=1)



note.add(tab_a, text="年間コスト")
note.add(tab_b, text="月間電力コスト")
note.add(tab_c, text="日次電力コスト")
note.add(tab_d, text="月間インバランス損失額")
note.add(tab_e, text="日次インバランス損失額")

note.pack()


#lbresult = Label(lf4,text = "hello",width=10, height=10)
#lbresult.grid(row = 0,column = 0)
fig = plt.figure(figsize=(5, 4),facecolor="green", edgecolor="green")
canvas = FigureCanvasTkAgg(fig, master=tab_a)
ax = fig.add_subplot(111,fc = "green")
"""
#ax.grid(which = 'major', linestyle = '-', color = 'white')
ax.xaxis.label.set_color("white")
ax.yaxis.label.set_color("white")
ax.spines['top'].set_color("white")
ax.spines['bottom'].set_color("white")
ax.spines['right'].set_color("white")
ax.spines['left'].set_color("white")
ax.tick_params(colors = "white")
ax.xaxis.grid(which = 'major', linestyle = '-', color = 'white')
ax.yaxis.grid(which = 'major', linestyle = '-', color = 'white')
"""


#入力をリストにするラベル


lf5 = LabelFrame(main_frm,text='入力リスト',bg = "green",foreground='white',width=200, height=300)
lf5.place(x = 30, y = 200)
lf5.propagate(1)
konkailabel = Label(lf5,text = "今回の入力",bg = "green",foreground='white')
koremadelabel = Label(lf5,text = "これまでの入力",bg = "green",foreground='white')
konkailabel.grid(column=0, row=0)
koremadelabel.grid(column=0, row=2)
currentinput = Entry(lf5, textvariable="",width=50,bg = "green",foreground='white')
currentinput.grid(column=0, row=1)
answers = []
for i in range(10):
    answer = Entry(lf5, textvariable="",width=50,bg = "green",foreground='white')
    answer.grid(column=0, row=i+3)
    answers.append(answer)


#相対入力用のウィンドウ

sub_win = Toplevel()
sub_win.title('相対取引購入比率')
frame0 = Frame(sub_win,bg = "green")
frame0.grid(row=0, column=0)
sub_win.configure(bg='green')


# チェックボタン作成
#bln_csv = tkinter.BooleanVar()
#chk = tkinter.Checkbutton(frame0, variable=bln_csv, text='csv',bg = "black",foreground='white',activebackground="white",activeforeground="black")
#bln_csv.set('False')
bln_csv = BooleanVar()

#ラジオ1（グループA）  
chk1 = ttk.Radiobutton(frame0,text='csv',value=True,variable=bln_csv)

#ラジオ2（グループA）
chk2 = ttk.Radiobutton(frame0,text='手動',value=False,variable=bln_csv)

chk1.grid(row=13, column = 0)
chk2.grid(row=13, column = 1)


ColumnNameLabelcsv = Label(frame0,text="番号",bg = "green",foreground='white')
ColumnNameLabelcsv.grid(row=14, column=0)
list_csv=ttk.Combobox(frame0,state='readonly',width=10)
list_csv['values'] = (1,2,3,4,5,6,7,8,9,10)
list_csv.grid(row=14, column=1)
noteStyler.configure("TCombobox",background="green",foreground='white')

ColumnList = ["日中","夜間"]
ColumnNameLabel1 = Label(frame0,text="日中",bg = "green",foreground='white')
ColumnNameLabel2 = Label(frame0,text="夜間",bg = "green",foreground='white')
ColumnNameLabel1.grid(row=0, column=1)
ColumnNameLabel2.grid(row=0, column=2)
MonthList = ["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"]
for i in range(0, len(MonthList)):
    label0 = Label(frame0,text=MonthList[i],bg = "green",foreground='white')
    label0.grid(row=i+1, column=0)
list_Items1 = [0] * 12
for i in range(0, 12):
    list_Items1[i] = ttk.Combobox(frame0,state='readonly',width=10)
    list_Items1[i]['values'] = (10,20,30,40,50,60,70,80,90,100)
    list_Items1[i].grid(row=i+1, column=1)
    list_Items1[i].current(4)
list_Items2 = [0] * 12
for i in range(0, 12):
    list_Items2[i] = ttk.Combobox(frame0,state='readonly',width=10)
    list_Items2[i]['values'] = (10,20,30,40,50,60,70,80,90,100)
    list_Items2[i].grid(row=i+1, column=2)
    list_Items2[i].current(4)
noteStyler.theme_use('winnative')
noteStyler.configure("TEntry",background="green",foreground='white')
noteStyler.configure("TButton",background="green",foreground='black')
noteStyler.configure("TRadiobutton",background="green",foreground='white')
noteStyler.configure("TNotebook",background="green",foreground='white')
noteStyler.configure("TCombobox", background="white",foreground='black')
noteStyler.configure("TNotebook.Tab",background='green',foreground='white')


if __name__ == "__main__":
    main_frm.mainloop()

