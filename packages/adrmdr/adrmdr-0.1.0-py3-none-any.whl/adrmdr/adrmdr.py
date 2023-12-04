#!/usr/bin/env python
# coding: utf-8

# 第一部分：程序说明###################################################################################
# coding=utf-8
# 药械不良事件工作平台
# 开发人：蔡权周
import tkinter as Tk #line:11
import os #line:12
import traceback #line:13
import ast #line:14
import re #line:15
import xlrd #line:16
import xlwt #line:17
import openpyxl #line:18
import pandas as pd #line:19
import numpy as np #line:20
import math #line:21
import scipy .stats as st #line:22
from tkinter import ttk ,Menu ,Frame ,Canvas ,StringVar ,LEFT ,RIGHT ,TOP ,BOTTOM ,BOTH ,Y ,X ,YES ,NO ,DISABLED ,END ,Button ,LabelFrame ,GROOVE ,Toplevel ,Label ,Entry ,Scrollbar ,Text ,filedialog ,dialog ,PhotoImage #line:23
import tkinter .font as tkFont #line:24
from tkinter .messagebox import showinfo #line:25
from tkinter .scrolledtext import ScrolledText #line:26
import matplotlib as plt #line:27
from matplotlib .backends .backend_tkagg import FigureCanvasTkAgg #line:28
from matplotlib .figure import Figure #line:29
from matplotlib .backends .backend_tkagg import NavigationToolbar2Tk #line:30
import collections #line:31
from collections import Counter #line:32
import datetime #line:33
from datetime import datetime ,timedelta #line:34
import xlsxwriter #line:35
import time #line:36
import threading #line:37
import warnings #line:38
from matplotlib .ticker import PercentFormatter #line:39
import sqlite3 #line:40
from sqlalchemy import create_engine #line:41
from sqlalchemy import text as sqltext #line:42
import webbrowser #line:44
global ori #line:47
ori =0 #line:48
global auto_guize #line:49
global biaozhun #line:52
global dishi #line:53
biaozhun =""#line:54
dishi =""#line:55
global ini #line:59
ini ={}#line:60
ini ["四个品种"]=1 #line:61
import random #line:64
import requests #line:65
global version_now #line:66
global usergroup #line:67
global setting_cfg #line:68
global csdir #line:69
global peizhidir #line:70
version_now ="0.1.0"#line:71
usergroup ="用户组=0"#line:72
setting_cfg =""#line:73
csdir =str (os .path .abspath (__file__ )).replace (str (__file__ ),"")#line:74
if csdir =="":#line:75
    csdir =str (os .path .dirname (__file__ ))#line:76
    csdir =csdir +csdir .split ("adrmdr")[0 ][-1 ]#line:77
title_all ="药械妆不良反应报表统计分析工作站 V"+version_now #line:80
title_all2 ="药械妆不良反应报表统计分析工作站 V"+version_now #line:81
def extract_zip_file (O000O0OO0O0OO00O0 ,O00O0000O000OO00O ):#line:88
    import zipfile #line:90
    if O00O0000O000OO00O =="":#line:91
        return 0 #line:92
    with zipfile .ZipFile (O000O0OO0O0OO00O0 ,'r')as O0O00OOOO00OO0O0O :#line:93
        for OO00OOOO0OO000O00 in O0O00OOOO00OO0O0O .infolist ():#line:94
            OO00OOOO0OO000O00 .filename =OO00OOOO0OO000O00 .filename .encode ('cp437').decode ('gbk')#line:96
            O0O00OOOO00OO0O0O .extract (OO00OOOO0OO000O00 ,O00O0000O000OO00O )#line:97
def get_directory_path (O00O00O000OO0000O ):#line:103
    global csdir #line:105
    if not (os .path .isfile (os .path .join (O00O00O000OO0000O ,'0（范例）比例失衡关键字库.xls'))):#line:107
        extract_zip_file (csdir +"def.py",O00O00O000OO0000O )#line:112
    if O00O00O000OO0000O =="":#line:114
        quit ()#line:115
    return O00O00O000OO0000O #line:116
def convert_and_compare_dates (OOO0000OO0OO0OOO0 ):#line:120
    import datetime #line:121
    OO000O00O0OOO0OOO =datetime .datetime .now ()#line:122
    try :#line:124
       OOO000OOO0O0O0O00 =datetime .datetime .strptime (str (int (int (OOO0000OO0OO0OOO0 )/4 )),"%Y%m%d")#line:125
    except :#line:126
        print ("fail")#line:127
        return "已过期"#line:128
    if OOO000OOO0O0O0O00 >OO000O00O0OOO0OOO :#line:130
        return "未过期"#line:132
    else :#line:133
        return "已过期"#line:134
def read_setting_cfg ():#line:136
    global csdir #line:137
    if os .path .exists (csdir +'setting.cfg'):#line:139
        text .insert (END ,"已完成初始化\n")#line:140
        with open (csdir +'setting.cfg','r')as O00O0O000OOO0O0O0 :#line:141
            OOOOOOO000O000OO0 =eval (O00O0O000OOO0O0O0 .read ())#line:142
    else :#line:143
        O0OO0OOO00O000O0O =csdir +'setting.cfg'#line:145
        with open (O0OO0OOO00O000O0O ,'w')as O00O0O000OOO0O0O0 :#line:146
            O00O0O000OOO0O0O0 .write ('{"settingdir": 0, "sidori": 0, "sidfinal": "11111180000808"}')#line:147
        text .insert (END ,"未初始化，正在初始化...\n")#line:148
        OOOOOOO000O000OO0 =read_setting_cfg ()#line:149
    return OOOOOOO000O000OO0 #line:150
def open_setting_cfg ():#line:153
    global csdir #line:154
    with open (csdir +"setting.cfg","r")as OOOO00OO00OOO0O00 :#line:156
        OOOO0OO000000OO0O =eval (OOOO00OO00OOO0O00 .read ())#line:158
    return OOOO0OO000000OO0O #line:159
def update_setting_cfg (O0OOOO0O0O0O0OO0O ,O0O000000O00OOO00 ):#line:161
    global csdir #line:162
    with open (csdir +"setting.cfg","r")as OO0O000O0OOO0OO0O :#line:164
        O00O00O0OOOOOO00O =eval (OO0O000O0OOO0OO0O .read ())#line:166
    if O00O00O0OOOOOO00O [O0OOOO0O0O0O0OO0O ]==0 or O00O00O0OOOOOO00O [O0OOOO0O0O0O0OO0O ]=="11111180000808":#line:168
        O00O00O0OOOOOO00O [O0OOOO0O0O0O0OO0O ]=O0O000000O00OOO00 #line:169
        with open (csdir +"setting.cfg","w")as OO0O000O0OOO0OO0O :#line:171
            OO0O000O0OOO0OO0O .write (str (O00O00O0OOOOOO00O ))#line:172
def generate_random_file ():#line:175
    O00O0OOO0000000OO =random .randint (200000 ,299999 )#line:177
    update_setting_cfg ("sidori",O00O0OOO0000000OO )#line:179
def display_random_number ():#line:181
    global csdir #line:182
    OO0OO00OO00000O00 =Toplevel ()#line:183
    OO0OO00OO00000O00 .title ("ID")#line:184
    OOO00OOOOOO000O0O =OO0OO00OO00000O00 .winfo_screenwidth ()#line:186
    O0OOO0O00O0OO0OOO =OO0OO00OO00000O00 .winfo_screenheight ()#line:187
    OOOO00O0O000000OO =80 #line:189
    OO00O00OO0O00OO00 =70 #line:190
    O000OOOO00000O000 =(OOO00OOOOOO000O0O -OOOO00O0O000000OO )/2 #line:192
    OO0O00O00OO0OO000 =(O0OOO0O00O0OO0OOO -OO00O00OO0O00OO00 )/2 #line:193
    OO0OO00OO00000O00 .geometry ("%dx%d+%d+%d"%(OOOO00O0O000000OO ,OO00O00OO0O00OO00 ,O000OOOO00000O000 ,OO0O00O00OO0OO000 ))#line:194
    with open (csdir +"setting.cfg","r")as O000O0O000000O0OO :#line:197
        O000O0OO000OO0OOO =eval (O000O0O000000O0OO .read ())#line:199
    O0O000O000O0O0OO0 =int (O000O0OO000OO0OOO ["sidori"])#line:200
    O00OO0O00O0OOO000 =O0O000O000O0O0OO0 *2 +183576 #line:201
    print (O00OO0O00O0OOO000 )#line:203
    OO0OOOOOO0OOOOOO0 =ttk .Label (OO0OO00OO00000O00 ,text =f"机器码: {O0O000O000O0O0OO0}")#line:205
    OO0000O0OOO00O00O =ttk .Entry (OO0OO00OO00000O00 )#line:206
    OO0OOOOOO0OOOOOO0 .pack ()#line:209
    OO0000O0OOO00O00O .pack ()#line:210
    ttk .Button (OO0OO00OO00000O00 ,text ="验证",command =lambda :check_input (OO0000O0OOO00O00O .get (),O00OO0O00O0OOO000 )).pack ()#line:214
def check_input (OO0O0OO00O00OOOOO ,O0OOO0000OO00OOOO ):#line:216
    try :#line:220
        O0O00O0O00O0OO000 =int (str (OO0O0OO00O00OOOOO )[0 :6 ])#line:221
        O0O0O00O0O0O00O00 =convert_and_compare_dates (str (OO0O0OO00O00OOOOO )[6 :14 ])#line:222
    except :#line:223
        showinfo (title ="提示",message ="不匹配，注册失败。")#line:224
        return 0 #line:225
    if O0O00O0O00O0OO000 ==O0OOO0000OO00OOOO and O0O0O00O0O0O00O00 =="未过期":#line:227
        update_setting_cfg ("sidfinal",OO0O0OO00O00OOOOO )#line:228
        showinfo (title ="提示",message ="注册成功,请重新启动程序。")#line:229
        quit ()#line:230
    else :#line:231
        showinfo (title ="提示",message ="不匹配，注册失败。")#line:232
def update_software (OOOOO0OO00OOOO00O ):#line:237
    global version_now #line:239
    text .insert (END ,"当前版本为："+version_now +",正在检查更新...(您可以同时执行分析任务)")#line:240
    try :#line:241
        OO00O0O000OO000OO =requests .get (f"https://pypi.org/pypi/{OOOOO0OO00OOOO00O}/json",timeout =2 ).json ()["info"]["version"]#line:242
    except :#line:243
        return "...更新失败。"#line:244
    if OO00O0O000OO000OO >version_now :#line:245
        text .insert (END ,"\n最新版本为："+OO00O0O000OO000OO +",正在尝试自动更新....")#line:246
        pip .main (['install',OOOOO0OO00OOOO00O ,'--upgrade'])#line:248
        text .insert (END ,"\n您可以开展工作。")#line:249
        return "...更新成功。"#line:250
def TOOLS_ror_mode1 (O0OO00OOOOOOOO00O ,OOO0OOO00OO00O0O0 ):#line:267
	OOO0OOOO00OOO00O0 =[]#line:268
	for OOOO0000O0OO0OOO0 in ("事件发生年份","性别","年龄段","报告类型-严重程度","停药减药后反应是否减轻或消失","再次使用可疑药是否出现同样反应","对原患疾病影响","不良反应结果","关联性评价"):#line:269
		O0OO00OOOOOOOO00O [OOOO0000O0OO0OOO0 ]=O0OO00OOOOOOOO00O [OOOO0000O0OO0OOO0 ].astype (str )#line:270
		O0OO00OOOOOOOO00O [OOOO0000O0OO0OOO0 ]=O0OO00OOOOOOOO00O [OOOO0000O0OO0OOO0 ].fillna ("不详")#line:271
		O00OOO000OO0O000O =0 #line:273
		for O0OOO0O00OOO00OO0 in O0OO00OOOOOOOO00O [OOO0OOO00OO00O0O0 ].drop_duplicates ():#line:274
			O00OOO000OO0O000O =O00OOO000OO0O000O +1 #line:275
			O0O0000O00OO00OOO =O0OO00OOOOOOOO00O [(O0OO00OOOOOOOO00O [OOO0OOO00OO00O0O0 ]==O0OOO0O00OOO00OO0 )].copy ()#line:276
			OOOOO00OO00OO0OOO =str (O0OOO0O00OOO00OO0 )+"计数"#line:278
			O00OO000OO0OO0000 =str (O0OOO0O00OOO00OO0 )+"构成比(%)"#line:279
			O0OO0OOO0O00OO00O =O0O0000O00OO00OOO .groupby (OOOO0000O0OO0OOO0 ).agg (计数 =("报告编码","nunique")).sort_values (by =OOOO0000O0OO0OOO0 ,ascending =[True ],na_position ="last").reset_index ()#line:280
			O0OO0OOO0O00OO00O [O00OO000OO0OO0000 ]=round (100 *O0OO0OOO0O00OO00O ["计数"]/O0OO0OOO0O00OO00O ["计数"].sum (),2 )#line:281
			O0OO0OOO0O00OO00O =O0OO0OOO0O00OO00O .rename (columns ={OOOO0000O0OO0OOO0 :"项目"})#line:282
			O0OO0OOO0O00OO00O =O0OO0OOO0O00OO00O .rename (columns ={"计数":OOOOO00OO00OO0OOO })#line:283
			if O00OOO000OO0O000O >1 :#line:284
				OO0O00000OOO000O0 =pd .merge (OO0O00000OOO000O0 ,O0OO0OOO0O00OO00O ,on =["项目"],how ="outer")#line:285
			else :#line:286
				OO0O00000OOO000O0 =O0OO0OOO0O00OO00O .copy ()#line:287
		OO0O00000OOO000O0 ["类别"]=OOOO0000O0OO0OOO0 #line:289
		OOO0OOOO00OOO00O0 .append (OO0O00000OOO000O0 .copy ().reset_index (drop =True ))#line:290
	OO00O0O000O000O0O =pd .concat (OOO0OOOO00OOO00O0 ,ignore_index =True ).fillna (0 )#line:293
	OO00O0O000O000O0O ["报表类型"]="KETI"#line:294
	TABLE_tree_Level_2 (OO00O0O000O000O0O ,1 ,OO00O0O000O000O0O )#line:295
def TOOLS_ror_mode2 (O00000O0O0O0O0000 ,OOO00OO0OO0O000OO ):#line:297
	OO0O0OO0000000OOO =Countall (O00000O0O0O0O0000 ).df_ror (["产品类别",OOO00OO0OO0O000OO ]).reset_index ()#line:298
	OO0O0OO0000000OOO ["四分表"]=OO0O0OO0000000OOO ["四分表"].str .replace ("(","")#line:299
	OO0O0OO0000000OOO ["四分表"]=OO0O0OO0000000OOO ["四分表"].str .replace (")","")#line:300
	OO0O0OO0000000OOO ["ROR信号（0-否，1-是）"]=0 #line:301
	OO0O0OO0000000OOO ["PRR信号（0-否，1-是）"]=0 #line:302
	OO0O0OO0000000OOO ["分母核验"]=0 #line:303
	for O000OOOO0O0OO00OO ,OOO00O0OOOOO00000 in OO0O0OO0000000OOO .iterrows ():#line:304
		O000OO0OO0OO0OOO0 =tuple (OOO00O0OOOOO00000 ["四分表"].split (","))#line:305
		OO0O0OO0000000OOO .loc [O000OOOO0O0OO00OO ,"a"]=int (O000OO0OO0OO0OOO0 [0 ])#line:306
		OO0O0OO0000000OOO .loc [O000OOOO0O0OO00OO ,"b"]=int (O000OO0OO0OO0OOO0 [1 ])#line:307
		OO0O0OO0000000OOO .loc [O000OOOO0O0OO00OO ,"c"]=int (O000OO0OO0OO0OOO0 [2 ])#line:308
		OO0O0OO0000000OOO .loc [O000OOOO0O0OO00OO ,"d"]=int (O000OO0OO0OO0OOO0 [3 ])#line:309
		if int (O000OO0OO0OO0OOO0 [1 ])*int (O000OO0OO0OO0OOO0 [2 ])*int (O000OO0OO0OO0OOO0 [3 ])*int (O000OO0OO0OO0OOO0 [0 ])==0 :#line:310
			OO0O0OO0000000OOO .loc [O000OOOO0O0OO00OO ,"分母核验"]=1 #line:311
		if OOO00O0OOOOO00000 ['ROR值的95%CI下限']>1 and OOO00O0OOOOO00000 ['出现频次']>=3 :#line:312
			OO0O0OO0000000OOO .loc [O000OOOO0O0OO00OO ,"ROR信号（0-否，1-是）"]=1 #line:313
		if OOO00O0OOOOO00000 ['PRR值的95%CI下限']>1 and OOO00O0OOOOO00000 ['出现频次']>=3 :#line:314
			OO0O0OO0000000OOO .loc [O000OOOO0O0OO00OO ,"PRR信号（0-否，1-是）"]=1 #line:315
		OO0O0OO0000000OOO .loc [O000OOOO0O0OO00OO ,"事件分类"]=str (TOOLS_get_list (OO0O0OO0000000OOO .loc [O000OOOO0O0OO00OO ,"特定关键字"])[0 ])#line:316
	OO0O0OO0000000OOO =pd .pivot_table (OO0O0OO0000000OOO ,values =["出现频次",'ROR值',"ROR值的95%CI下限","ROR信号（0-否，1-是）",'PRR值',"PRR值的95%CI下限","PRR信号（0-否，1-是）","a","b","c","d","分母核验","风险评分"],index ='事件分类',columns =OOO00OO0OO0O000OO ,aggfunc ='sum').reset_index ().fillna (0 )#line:318
	try :#line:321
		O00OOOO0OOO0000OO =peizhidir +"0（范例）比例失衡关键字库.xls"#line:322
		if "报告类型-新的"in O00000O0O0O0O0000 .columns :#line:323
			O00O0OO0O0O0O000O ="药品"#line:324
		else :#line:325
			O00O0OO0O0O0O000O ="器械"#line:326
		O00000OO0O0000000 =pd .read_excel (O00OOOO0OOO0000OO ,header =0 ,sheet_name =O00O0OO0O0O0O000O ).reset_index (drop =True )#line:327
	except :#line:328
		pass #line:329
	for O000OOOO0O0OO00OO ,OOO00O0OOOOO00000 in O00000OO0O0000000 .iterrows ():#line:331
		OO0O0OO0000000OOO .loc [OO0O0OO0000000OOO ["事件分类"].str .contains (OOO00O0OOOOO00000 ["值"],na =False ),"器官系统损害"]=TOOLS_get_list (OOO00O0OOOOO00000 ["值"])[0 ]#line:332
	try :#line:335
		OOOOOOOOO0O0OO000 =peizhidir +""+"0（范例）标准术语"+".xlsx"#line:336
		try :#line:337
			O0OO0O00O00OO00O0 =pd .read_excel (OOOOOOOOO0O0OO000 ,sheet_name ="onept",header =0 ,index_col =0 ).reset_index ()#line:338
		except :#line:339
			showinfo (title ="错误信息",message ="标准术语集无法加载。")#line:340
		try :#line:342
			O0OOOO0O0O000OOOO =pd .read_excel (OOOOOOOOO0O0OO000 ,sheet_name ="my",header =0 ,index_col =0 ).reset_index ()#line:343
		except :#line:344
			showinfo (title ="错误信息",message ="自定义术语集无法加载。")#line:345
		O0OO0O00O00OO00O0 =pd .concat ([O0OOOO0O0O000OOOO ,O0OO0O00O00OO00O0 ],ignore_index =True ).drop_duplicates ("code")#line:347
		O0OO0O00O00OO00O0 ["code"]=O0OO0O00O00OO00O0 ["code"].astype (str )#line:348
		OO0O0OO0000000OOO ["事件分类"]=OO0O0OO0000000OOO ["事件分类"].astype (str )#line:349
		O0OO0O00O00OO00O0 ["事件分类"]=O0OO0O00O00OO00O0 ["PT"]#line:350
		O000O0O0O0O0OO000 =pd .merge (OO0O0OO0000000OOO ,O0OO0O00O00OO00O0 ,on =["事件分类"],how ="left")#line:351
		for O000OOOO0O0OO00OO ,OOO00O0OOOOO00000 in O000O0O0O0O0OO000 .iterrows ():#line:352
			OO0O0OO0000000OOO .loc [OO0O0OO0000000OOO ["事件分类"]==OOO00O0OOOOO00000 ["事件分类"],"Chinese"]=OOO00O0OOOOO00000 ["Chinese"]#line:353
			OO0O0OO0000000OOO .loc [OO0O0OO0000000OOO ["事件分类"]==OOO00O0OOOOO00000 ["事件分类"],"PT"]=OOO00O0OOOOO00000 ["PT"]#line:354
			OO0O0OO0000000OOO .loc [OO0O0OO0000000OOO ["事件分类"]==OOO00O0OOOOO00000 ["事件分类"],"HLT"]=OOO00O0OOOOO00000 ["HLT"]#line:355
			OO0O0OO0000000OOO .loc [OO0O0OO0000000OOO ["事件分类"]==OOO00O0OOOOO00000 ["事件分类"],"HLGT"]=OOO00O0OOOOO00000 ["HLGT"]#line:356
			OO0O0OO0000000OOO .loc [OO0O0OO0000000OOO ["事件分类"]==OOO00O0OOOOO00000 ["事件分类"],"SOC"]=OOO00O0OOOOO00000 ["SOC"]#line:357
	except :#line:358
		pass #line:359
	OO0O0OO0000000OOO ["报表类型"]="KETI"#line:362
	TABLE_tree_Level_2 (OO0O0OO0000000OOO ,1 ,OO0O0OO0000000OOO )#line:363
def TOOLS_ror_mode3 (O0O00OOOO0O0OOOO0 ,OOOO000OO000OOO0O ):#line:365
	O0O00OOOO0O0OOOO0 ["css"]=0 #line:366
	TOOLS_ror_mode2 (O0O00OOOO0O0OOOO0 ,OOOO000OO000OOO0O )#line:367
def TOOLS_ror_mode4 (O00000O0O0OOOOOO0 ,OOOO0O0OOO0OO0OO0 ):#line:369
	OOO0000OOO0OO000O =[]#line:370
	for O0O0OOO000O0OO000 ,O0OO0000OO000O0OO in data .drop_duplicates (OOOO0O0OOO0OO0OO0 ).iterrows ():#line:371
		OOOOO0OOO0O0O0OO0 =data [(O00000O0O0OOOOOO0 [OOOO0O0OOO0OO0OO0 ]==O0OO0000OO000O0OO [OOOO0O0OOO0OO0OO0 ])]#line:372
		O00OO0OOO000000O0 =Countall (OOOOO0OOO0O0O0OO0 ).df_psur ()#line:373
		O00OO0OOO000000O0 [OOOO0O0OOO0OO0OO0 ]=O0OO0000OO000O0OO [OOOO0O0OOO0OO0OO0 ]#line:374
		if len (O00OO0OOO000000O0 )>0 :#line:375
			OOO0000OOO0OO000O .append (O00OO0OOO000000O0 )#line:376
	O0000O0OO00O000O0 =pd .concat (OOO0000OOO0OO000O ,ignore_index =True ).sort_values (by ="关键字标记",ascending =[False ],na_position ="last").reset_index ()#line:378
	O0000O0OO00O000O0 ["报表类型"]="KETI"#line:379
	TABLE_tree_Level_2 (O0000O0OO00O000O0 ,1 ,O0000O0OO00O000O0 )#line:380
def STAT_pinzhong (OO0O00OOO00OOO0O0 ,OO000OO0OO000O0OO ,OOO0O0O00000O0OO0 ):#line:382
	OOO0O000O0000OOOO =[OO000OO0OO000O0OO ]#line:384
	if OOO0O0O00000O0OO0 ==-1 :#line:385
		O000O0OO00OO00O00 =OO0O00OOO00OOO0O0 .drop_duplicates ("报告编码").copy ()#line:386
		O0O0O0000O0O0O0O0 =O000O0OO00OO00O00 .groupby ([OO000OO0OO000O0OO ]).agg (计数 =("报告编码","nunique")).sort_values (by =OO000OO0OO000O0OO ,ascending =[True ],na_position ="last").reset_index ()#line:387
		O0O0O0000O0O0O0O0 ["构成比(%)"]=round (100 *O0O0O0000O0O0O0O0 ["计数"]/O0O0O0000O0O0O0O0 ["计数"].sum (),2 )#line:388
		O0O0O0000O0O0O0O0 [OO000OO0OO000O0OO ]=O0O0O0000O0O0O0O0 [OO000OO0OO000O0OO ].astype (str )#line:389
		O0O0O0000O0O0O0O0 ["报表类型"]="dfx_deepview"+"_"+str (OOO0O000O0000OOOO )#line:390
		TABLE_tree_Level_2 (O0O0O0000O0O0O0O0 ,1 ,O000O0OO00OO00O00 )#line:391
	if OOO0O0O00000O0OO0 ==1 :#line:393
		O000O0OO00OO00O00 =OO0O00OOO00OOO0O0 .copy ()#line:394
		O0O0O0000O0O0O0O0 =O000O0OO00OO00O00 .groupby ([OO000OO0OO000O0OO ]).agg (计数 =("报告编码","nunique")).sort_values (by ="计数",ascending =[False ],na_position ="last").reset_index ()#line:395
		O0O0O0000O0O0O0O0 ["构成比(%)"]=round (100 *O0O0O0000O0O0O0O0 ["计数"]/O0O0O0000O0O0O0O0 ["计数"].sum (),2 )#line:396
		O0O0O0000O0O0O0O0 ["报表类型"]="dfx_deepview"+"_"+str (OOO0O000O0000OOOO )#line:397
		TABLE_tree_Level_2 (O0O0O0000O0O0O0O0 ,1 ,O000O0OO00OO00O00 )#line:398
	if OOO0O0O00000O0OO0 ==4 :#line:400
		O000O0OO00OO00O00 =OO0O00OOO00OOO0O0 .copy ()#line:401
		O000O0OO00OO00O00 .loc [O000O0OO00OO00O00 ["不良反应结果"].str .contains ("好转",na =False ),"不良反应结果2"]="好转"#line:402
		O000O0OO00OO00O00 .loc [O000O0OO00OO00O00 ["不良反应结果"].str .contains ("痊愈",na =False ),"不良反应结果2"]="痊愈"#line:403
		O000O0OO00OO00O00 .loc [O000O0OO00OO00O00 ["不良反应结果"].str .contains ("无进展",na =False ),"不良反应结果2"]="无进展"#line:404
		O000O0OO00OO00O00 .loc [O000O0OO00OO00O00 ["不良反应结果"].str .contains ("死亡",na =False ),"不良反应结果2"]="死亡"#line:405
		O000O0OO00OO00O00 .loc [O000O0OO00OO00O00 ["不良反应结果"].str .contains ("不详",na =False ),"不良反应结果2"]="不详"#line:406
		O000O0OO00OO00O00 .loc [O000O0OO00OO00O00 ["不良反应结果"].str .contains ("未好转",na =False ),"不良反应结果2"]="未好转"#line:407
		O0O0O0000O0O0O0O0 =O000O0OO00OO00O00 .groupby (["不良反应结果2"]).agg (计数 =("报告编码","nunique")).sort_values (by ="计数",ascending =[False ],na_position ="last").reset_index ()#line:408
		O0O0O0000O0O0O0O0 ["构成比(%)"]=round (100 *O0O0O0000O0O0O0O0 ["计数"]/O0O0O0000O0O0O0O0 ["计数"].sum (),2 )#line:409
		O0O0O0000O0O0O0O0 ["报表类型"]="dfx_deepview"+"_"+str (["不良反应结果2"])#line:410
		TABLE_tree_Level_2 (O0O0O0000O0O0O0O0 ,1 ,O000O0OO00OO00O00 )#line:411
	if OOO0O0O00000O0OO0 ==5 :#line:413
		O000O0OO00OO00O00 =OO0O00OOO00OOO0O0 .copy ()#line:414
		O000O0OO00OO00O00 ["关联性评价汇总"]="("+O000O0OO00OO00O00 ["评价状态"].astype (str )+"("+O000O0OO00OO00O00 ["县评价"].astype (str )+"("+O000O0OO00OO00O00 ["市评价"].astype (str )+"("+O000O0OO00OO00O00 ["省评价"].astype (str )+"("+O000O0OO00OO00O00 ["国家评价"].astype (str )+")"#line:416
		O000O0OO00OO00O00 ["关联性评价汇总"]=O000O0OO00OO00O00 ["关联性评价汇总"].str .replace ("(nan","",regex =False )#line:417
		O000O0OO00OO00O00 ["关联性评价汇总"]=O000O0OO00OO00O00 ["关联性评价汇总"].str .replace ("nan)","",regex =False )#line:418
		O000O0OO00OO00O00 ["关联性评价汇总"]=O000O0OO00OO00O00 ["关联性评价汇总"].str .replace ("nan","",regex =False )#line:419
		O000O0OO00OO00O00 ['最终的关联性评价']=O000O0OO00OO00O00 ["关联性评价汇总"].str .extract ('.*\((.*)\).*',expand =False )#line:420
		O0O0O0000O0O0O0O0 =O000O0OO00OO00O00 .groupby ('最终的关联性评价').agg (计数 =("报告编码","nunique")).sort_values (by ="计数",ascending =[False ],na_position ="last").reset_index ()#line:421
		O0O0O0000O0O0O0O0 ["构成比(%)"]=round (100 *O0O0O0000O0O0O0O0 ["计数"]/O0O0O0000O0O0O0O0 ["计数"].sum (),2 )#line:422
		O0O0O0000O0O0O0O0 ["报表类型"]="dfx_deepview"+"_"+str (['最终的关联性评价'])#line:423
		TABLE_tree_Level_2 (O0O0O0000O0O0O0O0 ,1 ,O000O0OO00OO00O00 )#line:424
	if OOO0O0O00000O0OO0 ==0 :#line:426
		OO0O00OOO00OOO0O0 [OO000OO0OO000O0OO ]=OO0O00OOO00OOO0O0 [OO000OO0OO000O0OO ].fillna ("未填写")#line:427
		OO0O00OOO00OOO0O0 [OO000OO0OO000O0OO ]=OO0O00OOO00OOO0O0 [OO000OO0OO000O0OO ].str .replace ("*","",regex =False )#line:428
		OOO00OOO00OO0OO0O ="use("+str (OO000OO0OO000O0OO )+").file"#line:429
		OOO0OO00000OO0OO0 =str (Counter (TOOLS_get_list0 (OOO00OOO00OO0OO0O ,OO0O00OOO00OOO0O0 ,1000 ))).replace ("Counter({","{")#line:430
		OOO0OO00000OO0OO0 =OOO0OO00000OO0OO0 .replace ("})","}")#line:431
		OOO0OO00000OO0OO0 =ast .literal_eval (OOO0OO00000OO0OO0 )#line:432
		O0O0O0000O0O0O0O0 =pd .DataFrame .from_dict (OOO0OO00000OO0OO0 ,orient ="index",columns =["计数"]).reset_index ()#line:433
		O0O0O0000O0O0O0O0 ["构成比(%)"]=round (100 *O0O0O0000O0O0O0O0 ["计数"]/O0O0O0000O0O0O0O0 ["计数"].sum (),2 )#line:435
		O0O0O0000O0O0O0O0 ["报表类型"]="dfx_deepvie2"+"_"+str (OOO0O000O0000OOOO )#line:436
		TABLE_tree_Level_2 (O0O0O0000O0O0O0O0 ,1 ,OO0O00OOO00OOO0O0 )#line:437
		return O0O0O0000O0O0O0O0 #line:438
	if OOO0O0O00000O0OO0 ==2 or OOO0O0O00000O0OO0 ==3 :#line:442
		OO0O00OOO00OOO0O0 [OO000OO0OO000O0OO ]=OO0O00OOO00OOO0O0 [OO000OO0OO000O0OO ].astype (str )#line:443
		OO0O00OOO00OOO0O0 [OO000OO0OO000O0OO ]=OO0O00OOO00OOO0O0 [OO000OO0OO000O0OO ].fillna ("未填写")#line:444
		OOO00OOO00OO0OO0O ="use("+str (OO000OO0OO000O0OO )+").file"#line:446
		OOO0OO00000OO0OO0 =str (Counter (TOOLS_get_list0 (OOO00OOO00OO0OO0O ,OO0O00OOO00OOO0O0 ,1000 ))).replace ("Counter({","{")#line:447
		OOO0OO00000OO0OO0 =OOO0OO00000OO0OO0 .replace ("})","}")#line:448
		OOO0OO00000OO0OO0 =ast .literal_eval (OOO0OO00000OO0OO0 )#line:449
		O0O0O0000O0O0O0O0 =pd .DataFrame .from_dict (OOO0OO00000OO0OO0 ,orient ="index",columns =["计数"]).reset_index ()#line:450
		print ("正在统计，请稍后...")#line:451
		OOO0O0OOO0000000O =peizhidir +""+"0（范例）标准术语"+".xlsx"#line:452
		try :#line:453
			O0OO0000O0O0OOOOO =pd .read_excel (OOO0O0OOO0000000O ,sheet_name ="simple",header =0 ,index_col =0 ).reset_index ()#line:454
		except :#line:455
			showinfo (title ="错误信息",message ="标准术语集无法加载。")#line:456
			return 0 #line:457
		try :#line:458
			O00O000O0O0O0OO0O =pd .read_excel (OOO0O0OOO0000000O ,sheet_name ="my",header =0 ,index_col =0 ).reset_index ()#line:459
		except :#line:460
			showinfo (title ="错误信息",message ="自定义术语集无法加载。")#line:461
			return 0 #line:462
		O0OO0000O0O0OOOOO =pd .concat ([O00O000O0O0O0OO0O ,O0OO0000O0O0OOOOO ],ignore_index =True ).drop_duplicates ("code")#line:463
		O0OO0000O0O0OOOOO ["code"]=O0OO0000O0O0OOOOO ["code"].astype (str )#line:464
		O0O0O0000O0O0O0O0 ["index"]=O0O0O0000O0O0O0O0 ["index"].astype (str )#line:465
		O0O0O0000O0O0O0O0 =O0O0O0000O0O0O0O0 .rename (columns ={"index":"code"})#line:467
		O0O0O0000O0O0O0O0 =pd .merge (O0O0O0000O0O0O0O0 ,O0OO0000O0O0OOOOO ,on =["code"],how ="left")#line:468
		O0O0O0000O0O0O0O0 ["code构成比(%)"]=round (100 *O0O0O0000O0O0O0O0 ["计数"]/O0O0O0000O0O0O0O0 ["计数"].sum (),2 )#line:469
		OO000O00O00O00OO0 =O0O0O0000O0O0O0O0 .groupby ("SOC").agg (SOC计数 =("计数","sum")).sort_values (by ="SOC计数",ascending =[False ],na_position ="last").reset_index ()#line:470
		OO000O00O00O00OO0 ["soc构成比(%)"]=round (100 *OO000O00O00O00OO0 ["SOC计数"]/OO000O00O00O00OO0 ["SOC计数"].sum (),2 )#line:471
		OO000O00O00O00OO0 ["SOC计数"]=OO000O00O00O00OO0 ["SOC计数"].astype (int )#line:472
		O0O0O0000O0O0O0O0 =pd .merge (O0O0O0000O0O0O0O0 ,OO000O00O00O00OO0 ,on =["SOC"],how ="left")#line:473
		if OOO0O0O00000O0OO0 ==3 :#line:475
			OO000O00O00O00OO0 ["具体名称"]=""#line:476
			for OO000O0OO0OOO000O ,OOO0O0OO0OOOOOO00 in OO000O00O00O00OO0 .iterrows ():#line:477
				O000O000OOO0O00OO =""#line:478
				OO0O00000O000OOO0 =O0O0O0000O0O0O0O0 .loc [O0O0O0000O0O0O0O0 ["SOC"].str .contains (OOO0O0OO0OOOOOO00 ["SOC"],na =False )].copy ()#line:479
				for OO0O00OO000O0O000 ,OO0O0OOO0O000O0O0 in OO0O00000O000OOO0 .iterrows ():#line:480
					O000O000OOO0O00OO =O000O000OOO0O00OO +str (OO0O0OOO0O000O0O0 ["PT"])+"("+str (OO0O0OOO0O000O0O0 ["计数"])+")、"#line:481
				OO000O00O00O00OO0 .loc [OO000O0OO0OOO000O ,"具体名称"]=O000O000OOO0O00OO #line:482
			OO000O00O00O00OO0 ["报表类型"]="dfx_deepvie2"+"_"+str (["SOC"])#line:483
			TABLE_tree_Level_2 (OO000O00O00O00OO0 ,1 ,O0O0O0000O0O0O0O0 )#line:484
		if OOO0O0O00000O0OO0 ==2 :#line:486
			O0O0O0000O0O0O0O0 ["报表类型"]="dfx_deepvie2"+"_"+str (OOO0O000O0000OOOO )#line:487
			TABLE_tree_Level_2 (O0O0O0000O0O0O0O0 ,1 ,OO0O00OOO00OOO0O0 )#line:488
	pass #line:491
def DRAW_pre (O0OO00OO0000OOO00 ):#line:493
	""#line:494
	O000000OOO0O0O0OO =list (O0OO00OO0000OOO00 ["报表类型"])[0 ].replace ("1","")#line:502
	if "dfx_org监测机构"in O000000OOO0O0O0OO :#line:504
		O0OO00OO0000OOO00 =O0OO00OO0000OOO00 [:-1 ]#line:505
		DRAW_make_one (O0OO00OO0000OOO00 ,"报告图","监测机构","报告数量","超级托帕斯图(严重伤害数)")#line:506
	elif "dfx_org市级监测机构"in O000000OOO0O0O0OO :#line:507
		O0OO00OO0000OOO00 =O0OO00OO0000OOO00 [:-1 ]#line:508
		DRAW_make_one (O0OO00OO0000OOO00 ,"报告图","市级监测机构","报告数量","超级托帕斯图(严重伤害数)")#line:509
	elif "dfx_user"in O000000OOO0O0O0OO :#line:510
		O0OO00OO0000OOO00 =O0OO00OO0000OOO00 [:-1 ]#line:511
		DRAW_make_one (O0OO00OO0000OOO00 ,"报告单位图","单位名称","报告数量","超级托帕斯图(严重伤害数)")#line:512
	elif "dfx_deepview"in O000000OOO0O0O0OO :#line:515
		DRAW_make_one (O0OO00OO0000OOO00 ,"柱状图",O0OO00OO0000OOO00 .columns [0 ],"计数","柱状图")#line:516
	elif "dfx_chiyouren"in O000000OOO0O0O0OO :#line:518
		O0OO00OO0000OOO00 =O0OO00OO0000OOO00 [:-1 ]#line:519
		DRAW_make_one (O0OO00OO0000OOO00 ,"涉及持有人图","上市许可持有人名称","总报告数","超级托帕斯图(总待评价数量)")#line:520
	elif "dfx_zhenghao"in O000000OOO0O0O0OO :#line:522
		O0OO00OO0000OOO00 ["产品"]=O0OO00OO0000OOO00 ["产品名称"]+"("+O0OO00OO0000OOO00 ["注册证编号/曾用注册证编号"]+")"#line:523
		DRAW_make_one (O0OO00OO0000OOO00 ,"涉及产品图","产品","证号计数","超级托帕斯图(严重伤害数)")#line:524
	elif "dfx_pihao"in O000000OOO0O0O0OO :#line:526
		if len (O0OO00OO0000OOO00 ["注册证编号/曾用注册证编号"].drop_duplicates ())>1 :#line:527
			O0OO00OO0000OOO00 ["产品"]=O0OO00OO0000OOO00 ["产品名称"]+"("+O0OO00OO0000OOO00 ["注册证编号/曾用注册证编号"]+"--"+O0OO00OO0000OOO00 ["产品批号"]+")"#line:528
			DRAW_make_one (O0OO00OO0000OOO00 ,"涉及批号图","产品","批号计数","超级托帕斯图(严重伤害数)")#line:529
		else :#line:530
			DRAW_make_one (O0OO00OO0000OOO00 ,"涉及批号图","产品批号","批号计数","超级托帕斯图(严重伤害数)")#line:531
	elif "dfx_xinghao"in O000000OOO0O0O0OO :#line:533
		if len (O0OO00OO0000OOO00 ["注册证编号/曾用注册证编号"].drop_duplicates ())>1 :#line:534
			O0OO00OO0000OOO00 ["产品"]=O0OO00OO0000OOO00 ["产品名称"]+"("+O0OO00OO0000OOO00 ["注册证编号/曾用注册证编号"]+"--"+O0OO00OO0000OOO00 ["型号"]+")"#line:535
			DRAW_make_one (O0OO00OO0000OOO00 ,"涉及型号图","产品","型号计数","超级托帕斯图(严重伤害数)")#line:536
		else :#line:537
			DRAW_make_one (O0OO00OO0000OOO00 ,"涉及型号图","型号","型号计数","超级托帕斯图(严重伤害数)")#line:538
	elif "dfx_guige"in O000000OOO0O0O0OO :#line:540
		if len (O0OO00OO0000OOO00 ["注册证编号/曾用注册证编号"].drop_duplicates ())>1 :#line:541
			O0OO00OO0000OOO00 ["产品"]=O0OO00OO0000OOO00 ["产品名称"]+"("+O0OO00OO0000OOO00 ["注册证编号/曾用注册证编号"]+"--"+O0OO00OO0000OOO00 ["规格"]+")"#line:542
			DRAW_make_one (O0OO00OO0000OOO00 ,"涉及规格图","产品","规格计数","超级托帕斯图(严重伤害数)")#line:543
		else :#line:544
			DRAW_make_one (O0OO00OO0000OOO00 ,"涉及规格图","规格","规格计数","超级托帕斯图(严重伤害数)")#line:545
	elif "PSUR"in O000000OOO0O0O0OO :#line:547
		DRAW_make_mutibar (O0OO00OO0000OOO00 ,"总数量","严重","事件分类","总数量","严重","表现分类统计图")#line:548
	elif "keyword_findrisk"in O000000OOO0O0O0OO :#line:550
		O00O0OOO0000OOO00 =O0OO00OO0000OOO00 .columns .to_list ()#line:552
		OOO0OO00O0OO0O00O =O00O0OOO0000OOO00 [O00O0OOO0000OOO00 .index ("关键字")+1 ]#line:553
		OOOO0O000OO0O0OO0 =pd .pivot_table (O0OO00OO0000OOO00 ,index =OOO0OO00O0OO0O00O ,columns ="关键字",values =["计数"],aggfunc ={"计数":"sum"},fill_value ="0",margins =True ,dropna =False ,)#line:564
		OOOO0O000OO0O0OO0 .columns =OOOO0O000OO0O0OO0 .columns .droplevel (0 )#line:565
		OOOO0O000OO0O0OO0 =OOOO0O000OO0O0OO0 [:-1 ].reset_index ()#line:566
		OOOO0O000OO0O0OO0 =pd .merge (OOOO0O000OO0O0OO0 ,O0OO00OO0000OOO00 [[OOO0OO00O0OO0O00O ,"该元素总数量"]].drop_duplicates (OOO0OO00O0OO0O00O ),on =[OOO0OO00O0OO0O00O ],how ="left")#line:568
		del OOOO0O000OO0O0OO0 ["All"]#line:570
		DRAW_make_risk_plot (OOOO0O000OO0O0OO0 ,OOO0OO00O0OO0O00O ,[O0000OOOO0OO0O0O0 for O0000OOOO0OO0O0O0 in OOOO0O000OO0O0OO0 .columns if O0000OOOO0OO0O0O0 !=OOO0OO00O0OO0O00O ],"关键字趋势图",100 )#line:575
def DRAW_make_risk_plot (OOO00OO00OO0O0000 ,O0OOO00000O0OOOO0 ,OO0O000000O0O0OOO ,O0OO00000O00O0O00 ,OOOO0OOO0O0O0OO00 ,*OOO0OO0OO0OOOO00O ):#line:580
    ""#line:581
    OO0O0OOO0OO00OOO0 =Toplevel ()#line:584
    OO0O0OOO0OO00OOO0 .title (O0OO00000O00O0O00 )#line:585
    O000OO0O00O000OO0 =ttk .Frame (OO0O0OOO0OO00OOO0 ,height =20 )#line:586
    O000OO0O00O000OO0 .pack (side =TOP )#line:587
    OOOO0OOOOO00000OO =Figure (figsize =(12 ,6 ),dpi =100 )#line:589
    OOO0000O0OOOO0000 =FigureCanvasTkAgg (OOOO0OOOOO00000OO ,master =OO0O0OOO0OO00OOO0 )#line:590
    OOO0000O0OOOO0000 .draw ()#line:591
    OOO0000O0OOOO0000 .get_tk_widget ().pack (expand =1 )#line:592
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:594
    plt .rcParams ['axes.unicode_minus']=False #line:595
    O00OO00O0000OO0OO =NavigationToolbar2Tk (OOO0000O0OOOO0000 ,OO0O0OOO0OO00OOO0 )#line:597
    O00OO00O0000OO0OO .update ()#line:598
    OOO0000O0OOOO0000 .get_tk_widget ().pack ()#line:599
    O000O0OO0000O00OO =OOOO0OOOOO00000OO .add_subplot (111 )#line:601
    O000O0OO0000O00OO .set_title (O0OO00000O00O0O00 )#line:603
    OOOO0O0O0O00O0O0O =OOO00OO00OO0O0000 [O0OOO00000O0OOOO0 ]#line:604
    if OOOO0OOO0O0O0OO00 !=999 :#line:607
        O000O0OO0000O00OO .set_xticklabels (OOOO0O0O0O00O0O0O ,rotation =-90 ,fontsize =8 )#line:608
    O00OOOO0O000O0O00 =range (0 ,len (OOOO0O0O0O00O0O0O ),1 )#line:611
    try :#line:616
        O000O0OO0000O00OO .bar (OOOO0O0O0O00O0O0O ,OOO00OO00OO0O0000 ["报告总数"],color ='skyblue',label ="报告总数")#line:617
        O000O0OO0000O00OO .bar (OOOO0O0O0O00O0O0O ,height =OOO00OO00OO0O0000 ["严重伤害数"],color ="orangered",label ="严重伤害数")#line:618
    except :#line:619
        pass #line:620
    for O00OOO0OO00O0000O in OO0O000000O0O0OOO :#line:623
        OO00OOOOOOOO000O0 =OOO00OO00OO0O0000 [O00OOO0OO00O0000O ].astype (float )#line:624
        if O00OOO0OO00O0000O =="关注区域":#line:626
            O000O0OO0000O00OO .plot (list (OOOO0O0O0O00O0O0O ),list (OO00OOOOOOOO000O0 ),label =str (O00OOO0OO00O0000O ),color ="red")#line:627
        else :#line:628
            O000O0OO0000O00OO .plot (list (OOOO0O0O0O00O0O0O ),list (OO00OOOOOOOO000O0 ),label =str (O00OOO0OO00O0000O ))#line:629
        if OOOO0OOO0O0O0OO00 ==100 :#line:632
            for OO00O0000OOOO0OO0 ,O0OO0OO00O0OOOOOO in zip (OOOO0O0O0O00O0O0O ,OO00OOOOOOOO000O0 ):#line:633
                if O0OO0OO00O0OOOOOO ==max (OO00OOOOOOOO000O0 )and O0OO0OO00O0OOOOOO >=3 :#line:634
                     O000O0OO0000O00OO .text (OO00O0000OOOO0OO0 ,O0OO0OO00O0OOOOOO ,(str (O00OOO0OO00O0000O )+":"+str (int (O0OO0OO00O0OOOOOO ))),color ='black',size =8 )#line:635
    try :#line:645
        if OOO0OO0OO0OOOO00O [0 ]:#line:646
            OOOO0OO0O0000OO0O =OOO0OO0OO0OOOO00O [0 ]#line:647
    except :#line:648
        OOOO0OO0O0000OO0O ="ucl"#line:649
    if len (OO0O000000O0O0OOO )==1 :#line:651
        if OOOO0OO0O0000OO0O =="更多控制线分位数":#line:653
            OOO0OO0O00OO0OO00 =OOO00OO00OO0O0000 [OO0O000000O0O0OOO ].astype (float ).values #line:654
            OOO0O0000OO000OO0 =np .where (OOO0OO0O00OO0OO00 >0 ,1 ,0 )#line:655
            O0000OO0O00O00000 =np .nonzero (OOO0O0000OO000OO0 )#line:656
            OOO0OO0O00OO0OO00 =OOO0OO0O00OO0OO00 [O0000OO0O00O00000 ]#line:657
            O0OOOOOOO000OO0OO =np .median (OOO0OO0O00OO0OO00 )#line:658
            OOOOO00OOO0O0O0OO =np .percentile (OOO0OO0O00OO0OO00 ,25 )#line:659
            O0O0OOO0OO0OO0OOO =np .percentile (OOO0OO0O00OO0OO00 ,75 )#line:660
            O0O00O00000OO0000 =O0O0OOO0OO0OO0OOO -OOOOO00OOO0O0O0OO #line:661
            O0000OO00OOOO0OO0 =O0O0OOO0OO0OO0OOO +1.5 *O0O00O00000OO0000 #line:662
            O0OO0OO0OOOO00OOO =OOOOO00OOO0O0O0OO -1.5 *O0O00O00000OO0000 #line:663
            O000O0OO0000O00OO .axhline (O0OO0OO0OOOO00OOO ,color ='c',linestyle ='--',label ='异常下限')#line:666
            O000O0OO0000O00OO .axhline (OOOOO00OOO0O0O0OO ,color ='r',linestyle ='--',label ='第25百分位数')#line:668
            O000O0OO0000O00OO .axhline (O0OOOOOOO000OO0OO ,color ='g',linestyle ='--',label ='中位数')#line:669
            O000O0OO0000O00OO .axhline (O0O0OOO0OO0OO0OOO ,color ='r',linestyle ='--',label ='第75百分位数')#line:670
            O000O0OO0000O00OO .axhline (O0000OO00OOOO0OO0 ,color ='c',linestyle ='--',label ='异常上限')#line:672
            O00O000O0O0O00000 =ttk .Label (OO0O0OOO0OO00OOO0 ,text ="中位数="+str (O0OOOOOOO000OO0OO )+"; 第25百分位数="+str (OOOOO00OOO0O0O0OO )+"; 第75百分位数="+str (O0O0OOO0OO0OO0OOO )+"; 异常上限(第75百分位数+1.5IQR)="+str (O0000OO00OOOO0OO0 )+"; IQR="+str (O0O00O00000OO0000 ))#line:673
            O00O000O0O0O00000 .pack ()#line:674
        elif OOOO0OO0O0000OO0O =="更多控制线STD":#line:676
            OOO0OO0O00OO0OO00 =OOO00OO00OO0O0000 [OO0O000000O0O0OOO ].astype (float ).values #line:677
            OOO0O0000OO000OO0 =np .where (OOO0OO0O00OO0OO00 >0 ,1 ,0 )#line:678
            O0000OO0O00O00000 =np .nonzero (OOO0O0000OO000OO0 )#line:679
            OOO0OO0O00OO0OO00 =OOO0OO0O00OO0OO00 [O0000OO0O00O00000 ]#line:680
            O0O0OOO000O0000O0 =OOO0OO0O00OO0OO00 .mean ()#line:682
            O0O0O0O00O00O0000 =OOO0OO0O00OO0OO00 .std (ddof =1 )#line:683
            O0OOO00OO0000O0O0 =O0O0OOO000O0000O0 +3 *O0O0O0O00O00O0000 #line:684
            OOO0O000O0000OO0O =O0O0O0O00O00O0000 -3 *O0O0O0O00O00O0000 #line:685
            if len (OOO0OO0O00OO0OO00 )<30 :#line:687
                OOOOOOO0O0000OO0O =st .t .interval (0.95 ,df =len (OOO0OO0O00OO0OO00 )-1 ,loc =np .mean (OOO0OO0O00OO0OO00 ),scale =st .sem (OOO0OO0O00OO0OO00 ))#line:688
            else :#line:689
                OOOOOOO0O0000OO0O =st .norm .interval (0.95 ,loc =np .mean (OOO0OO0O00OO0OO00 ),scale =st .sem (OOO0OO0O00OO0OO00 ))#line:690
            OOOOOOO0O0000OO0O =OOOOOOO0O0000OO0O [1 ]#line:691
            O000O0OO0000O00OO .axhline (O0OOO00OO0000O0O0 ,color ='r',linestyle ='--',label ='UCL')#line:692
            O000O0OO0000O00OO .axhline (O0O0OOO000O0000O0 +2 *O0O0O0O00O00O0000 ,color ='m',linestyle ='--',label ='μ+2σ')#line:693
            O000O0OO0000O00OO .axhline (O0O0OOO000O0000O0 +O0O0O0O00O00O0000 ,color ='m',linestyle ='--',label ='μ+σ')#line:694
            O000O0OO0000O00OO .axhline (O0O0OOO000O0000O0 ,color ='g',linestyle ='--',label ='CL')#line:695
            O000O0OO0000O00OO .axhline (O0O0OOO000O0000O0 -O0O0O0O00O00O0000 ,color ='m',linestyle ='--',label ='μ-σ')#line:696
            O000O0OO0000O00OO .axhline (O0O0OOO000O0000O0 -2 *O0O0O0O00O00O0000 ,color ='m',linestyle ='--',label ='μ-2σ')#line:697
            O000O0OO0000O00OO .axhline (OOO0O000O0000OO0O ,color ='r',linestyle ='--',label ='LCL')#line:698
            O000O0OO0000O00OO .axhline (OOOOOOO0O0000OO0O ,color ='g',linestyle ='-',label ='95CI')#line:699
            OO0O0OO00O0OO00OO =ttk .Label (OO0O0OOO0OO00OOO0 ,text ="mean="+str (O0O0OOO000O0000O0 )+"; std="+str (O0O0O0O00O00O0000 )+"; 99.73%:UCL(μ+3σ)="+str (O0OOO00OO0000O0O0 )+"; LCL(μ-3σ)="+str (OOO0O000O0000OO0O )+"; 95%CI="+str (OOOOOOO0O0000OO0O ))#line:700
            OO0O0OO00O0OO00OO .pack ()#line:701
            O00O000O0O0O00000 =ttk .Label (OO0O0OOO0OO00OOO0 ,text ="68.26%:μ+σ="+str (O0O0OOO000O0000O0 +O0O0O0O00O00O0000 )+"; 95.45%:μ+2σ="+str (O0O0OOO000O0000O0 +2 *O0O0O0O00O00O0000 ))#line:703
            O00O000O0O0O00000 .pack ()#line:704
        else :#line:706
            OOO0OO0O00OO0OO00 =OOO00OO00OO0O0000 [OO0O000000O0O0OOO ].astype (float ).values #line:707
            OOO0O0000OO000OO0 =np .where (OOO0OO0O00OO0OO00 >0 ,1 ,0 )#line:708
            O0000OO0O00O00000 =np .nonzero (OOO0O0000OO000OO0 )#line:709
            OOO0OO0O00OO0OO00 =OOO0OO0O00OO0OO00 [O0000OO0O00O00000 ]#line:710
            O0O0OOO000O0000O0 =OOO0OO0O00OO0OO00 .mean ()#line:711
            O0O0O0O00O00O0000 =OOO0OO0O00OO0OO00 .std (ddof =1 )#line:712
            O0OOO00OO0000O0O0 =O0O0OOO000O0000O0 +3 *O0O0O0O00O00O0000 #line:713
            OOO0O000O0000OO0O =O0O0O0O00O00O0000 -3 *O0O0O0O00O00O0000 #line:714
            O000O0OO0000O00OO .axhline (O0OOO00OO0000O0O0 ,color ='r',linestyle ='--',label ='UCL')#line:715
            O000O0OO0000O00OO .axhline (O0O0OOO000O0000O0 ,color ='g',linestyle ='--',label ='CL')#line:716
            O000O0OO0000O00OO .axhline (OOO0O000O0000OO0O ,color ='r',linestyle ='--',label ='LCL')#line:717
            OO0O0OO00O0OO00OO =ttk .Label (OO0O0OOO0OO00OOO0 ,text ="mean="+str (O0O0OOO000O0000O0 )+"; std="+str (O0O0O0O00O00O0000 )+"; UCL(μ+3σ)="+str (O0OOO00OO0000O0O0 )+"; LCL(μ-3σ)="+str (OOO0O000O0000OO0O ))#line:718
            OO0O0OO00O0OO00OO .pack ()#line:719
    O000O0OO0000O00OO .set_title ("控制图")#line:722
    O000O0OO0000O00OO .set_xlabel ("项")#line:723
    OOOO0OOOOO00000OO .tight_layout (pad =0.4 ,w_pad =3.0 ,h_pad =3.0 )#line:724
    O00000OOO000OOOOO =O000O0OO0000O00OO .get_position ()#line:725
    O000O0OO0000O00OO .set_position ([O00000OOO000OOOOO .x0 ,O00000OOO000OOOOO .y0 ,O00000OOO000OOOOO .width *0.7 ,O00000OOO000OOOOO .height ])#line:726
    O000O0OO0000O00OO .legend (loc =2 ,bbox_to_anchor =(1.05 ,1.0 ),fontsize =10 ,borderaxespad =0.0 )#line:727
    OO00O00O0OO00OOO0 =StringVar ()#line:730
    O0OO0OOO0O0O000OO =ttk .Combobox (O000OO0O00O000OO0 ,width =15 ,textvariable =OO00O00O0OO00OOO0 ,state ='readonly')#line:731
    O0OO0OOO0O0O000OO ['values']=OO0O000000O0O0OOO #line:732
    O0OO0OOO0O0O000OO .pack (side =LEFT )#line:733
    O0OO0OOO0O0O000OO .current (0 )#line:734
    O0OOO00O0O0O00O0O =Button (O000OO0O00O000OO0 ,text ="控制图（单项-UCL(μ+3σ)）",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_make_risk_plot (OOO00OO00OO0O0000 ,O0OOO00000O0OOOO0 ,[O0000000O0O0000OO for O0000000O0O0000OO in OO0O000000O0O0OOO if OO00O00O0OO00OOO0 .get ()in O0000000O0O0000OO ],O0OO00000O00O0O00 ,OOOO0OOO0O0O0OO00 ))#line:744
    O0OOO00O0O0O00O0O .pack (side =LEFT ,anchor ="ne")#line:745
    O0O0000OO0OOOO000 =Button (O000OO0O00O000OO0 ,text ="控制图（单项-UCL(标准差法)）",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_make_risk_plot (OOO00OO00OO0O0000 ,O0OOO00000O0OOOO0 ,[O0OOO0OO00OOO0000 for O0OOO0OO00OOO0000 in OO0O000000O0O0OOO if OO00O00O0OO00OOO0 .get ()in O0OOO0OO00OOO0000 ],O0OO00000O00O0O00 ,OOOO0OOO0O0O0OO00 ,"更多控制线STD"))#line:753
    O0O0000OO0OOOO000 .pack (side =LEFT ,anchor ="ne")#line:754
    O0O0000OO0OOOO000 =Button (O000OO0O00O000OO0 ,text ="控制图（单项-分位数）",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_make_risk_plot (OOO00OO00OO0O0000 ,O0OOO00000O0OOOO0 ,[O00O0OO0000000OOO for O00O0OO0000000OOO in OO0O000000O0O0OOO if OO00O00O0OO00OOO0 .get ()in O00O0OO0000000OOO ],O0OO00000O00O0O00 ,OOOO0OOO0O0O0OO00 ,"更多控制线分位数"))#line:762
    O0O0000OO0OOOO000 .pack (side =LEFT ,anchor ="ne")#line:763
    O000OOO00O0000000 =Button (O000OO0O00O000OO0 ,text ="去除标记",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_make_risk_plot (OOO00OO00OO0O0000 ,O0OOO00000O0OOOO0 ,OO0O000000O0O0OOO ,O0OO00000O00O0O00 ,0 ))#line:772
    O000OOO00O0000000 .pack (side =LEFT ,anchor ="ne")#line:774
    OOO0000O0OOOO0000 .draw ()#line:775
def DRAW_make_one (OO0O0O00000O000O0 ,O00000OO0OO0O0O00 ,O0OO0000OO00O0000 ,OO0OO0OO0O0OOO00O ,OO000OO000OO0OOO0 ):#line:779
    ""#line:780
    warnings .filterwarnings ("ignore")#line:781
    OO00OOO0OOO0OO0OO =Toplevel ()#line:782
    OO00OOO0OOO0OO0OO .title (O00000OO0OO0O0O00 )#line:783
    O0OOO0OO0O00O0OO0 =ttk .Frame (OO00OOO0OOO0OO0OO ,height =20 )#line:784
    O0OOO0OO0O00O0OO0 .pack (side =TOP )#line:785
    O0OO0O0OOOOOOO000 =Figure (figsize =(12 ,6 ),dpi =100 )#line:787
    O0000O0O0OO00O00O =FigureCanvasTkAgg (O0OO0O0OOOOOOO000 ,master =OO00OOO0OOO0OO0OO )#line:788
    O0000O0O0OO00O00O .draw ()#line:789
    O0000O0O0OO00O00O .get_tk_widget ().pack (expand =1 )#line:790
    O000000OOOOOO000O =O0OO0O0OOOOOOO000 .add_subplot (111 )#line:791
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:793
    plt .rcParams ['axes.unicode_minus']=False #line:794
    OOOOOO000OO00OOOO =NavigationToolbar2Tk (O0000O0O0OO00O00O ,OO00OOO0OOO0OO0OO )#line:796
    OOOOOO000OO00OOOO .update ()#line:797
    O0000O0O0OO00O00O .get_tk_widget ().pack ()#line:799
    try :#line:802
        OO0OOOO00OO000O00 =OO0O0O00000O000O0 .columns #line:803
        OO0O0O00000O000O0 =OO0O0O00000O000O0 .sort_values (by =OO0OO0OO0O0OOO00O ,ascending =[False ],na_position ="last")#line:804
    except :#line:805
        OOOO0OOO00O00OO00 =eval (OO0O0O00000O000O0 )#line:806
        OOOO0OOO00O00OO00 =pd .DataFrame .from_dict (OOOO0OOO00O00OO00 ,orient =O0OO0000OO00O0000 ,columns =[OO0OO0OO0O0OOO00O ]).reset_index ()#line:809
        OO0O0O00000O000O0 =OOOO0OOO00O00OO00 .sort_values (by =OO0OO0OO0O0OOO00O ,ascending =[False ],na_position ="last")#line:810
    if ("日期"in O00000OO0OO0O0O00 or "时间"in O00000OO0OO0O0O00 or "季度"in O00000OO0OO0O0O00 )and "饼图"not in OO000OO000OO0OOO0 :#line:814
        OO0O0O00000O000O0 [O0OO0000OO00O0000 ]=pd .to_datetime (OO0O0O00000O000O0 [O0OO0000OO00O0000 ],format ="%Y/%m/%d").dt .date #line:815
        OO0O0O00000O000O0 =OO0O0O00000O000O0 .sort_values (by =O0OO0000OO00O0000 ,ascending =[True ],na_position ="last")#line:816
    elif "批号"in O00000OO0OO0O0O00 :#line:817
        OO0O0O00000O000O0 [O0OO0000OO00O0000 ]=OO0O0O00000O000O0 [O0OO0000OO00O0000 ].astype (str )#line:818
        OO0O0O00000O000O0 =OO0O0O00000O000O0 .sort_values (by =O0OO0000OO00O0000 ,ascending =[True ],na_position ="last")#line:819
        O000000OOOOOO000O .set_xticklabels (OO0O0O00000O000O0 [O0OO0000OO00O0000 ],rotation =-90 ,fontsize =8 )#line:820
    else :#line:821
        OO0O0O00000O000O0 [O0OO0000OO00O0000 ]=OO0O0O00000O000O0 [O0OO0000OO00O0000 ].astype (str )#line:822
        O000000OOOOOO000O .set_xticklabels (OO0O0O00000O000O0 [O0OO0000OO00O0000 ],rotation =-90 ,fontsize =8 )#line:823
    O00OOOO0O0OO00000 =OO0O0O00000O000O0 [OO0OO0OO0O0OOO00O ]#line:825
    OOOO0OO000O00OO0O =range (0 ,len (O00OOOO0O0OO00000 ),1 )#line:826
    O000000OOOOOO000O .set_title (O00000OO0OO0O0O00 )#line:828
    if OO000OO000OO0OOO0 =="柱状图":#line:832
        O000000OOOOOO000O .bar (x =OO0O0O00000O000O0 [O0OO0000OO00O0000 ],height =O00OOOO0O0OO00000 ,width =0.2 ,color ="#87CEFA")#line:833
    elif OO000OO000OO0OOO0 =="饼图":#line:834
        O000000OOOOOO000O .pie (x =O00OOOO0O0OO00000 ,labels =OO0O0O00000O000O0 [O0OO0000OO00O0000 ],autopct ="%0.2f%%")#line:835
    elif OO000OO000OO0OOO0 =="折线图":#line:836
        O000000OOOOOO000O .plot (OO0O0O00000O000O0 [O0OO0000OO00O0000 ],O00OOOO0O0OO00000 ,lw =0.5 ,ls ='-',c ="r",alpha =0.5 )#line:837
    elif "托帕斯图"in str (OO000OO000OO0OOO0 ):#line:839
        O0O00O0OO0OO000O0 =OO0O0O00000O000O0 [OO0OO0OO0O0OOO00O ].fillna (0 )#line:840
        O0OOO00000O000OOO =O0O00O0OO0OO000O0 .cumsum ()/O0O00O0OO0OO000O0 .sum ()*100 #line:844
        OO000000OO0O0O0OO =O0OOO00000O000OOO [O0OOO00000O000OOO >0.8 ].index [0 ]#line:846
        O0OOO0OO00OO00OO0 =O0O00O0OO0OO000O0 .index .tolist ().index (OO000000OO0O0O0OO )#line:847
        O000000OOOOOO000O .bar (x =OO0O0O00000O000O0 [O0OO0000OO00O0000 ],height =O0O00O0OO0OO000O0 ,color ="C0",label =OO0OO0OO0O0OOO00O )#line:851
        OO00OO0OO0OO0OOO0 =O000000OOOOOO000O .twinx ()#line:852
        OO00OO0OO0OO0OOO0 .plot (OO0O0O00000O000O0 [O0OO0000OO00O0000 ],O0OOO00000O000OOO ,color ="C1",alpha =0.6 ,label ="累计比例")#line:853
        OO00OO0OO0OO0OOO0 .yaxis .set_major_formatter (PercentFormatter ())#line:854
        O000000OOOOOO000O .tick_params (axis ="y",colors ="C0")#line:859
        OO00OO0OO0OO0OOO0 .tick_params (axis ="y",colors ="C1")#line:860
        if "超级托帕斯图"in str (OO000OO000OO0OOO0 ):#line:863
            O00000O0OO0O000OO =re .compile (r'[(](.*?)[)]',re .S )#line:864
            O000OOO0O00O0OO0O =re .findall (O00000O0OO0O000OO ,OO000OO000OO0OOO0 )[0 ]#line:865
            O000000OOOOOO000O .bar (x =OO0O0O00000O000O0 [O0OO0000OO00O0000 ],height =OO0O0O00000O000O0 [O000OOO0O00O0OO0O ],color ="orangered",label =O000OOO0O00O0OO0O )#line:866
    O0OO0O0OOOOOOO000 .tight_layout (pad =0.4 ,w_pad =3.0 ,h_pad =3.0 )#line:868
    O0O00O00O0O0O0000 =O000000OOOOOO000O .get_position ()#line:869
    O000000OOOOOO000O .set_position ([O0O00O00O0O0O0000 .x0 ,O0O00O00O0O0O0000 .y0 ,O0O00O00O0O0O0000 .width *0.7 ,O0O00O00O0O0O0000 .height ])#line:870
    O000000OOOOOO000O .legend (loc =2 ,bbox_to_anchor =(1.05 ,1.0 ),fontsize =10 ,borderaxespad =0.0 )#line:871
    O0000O0O0OO00O00O .draw ()#line:874
    if len (O00OOOO0O0OO00000 )<=20 and OO000OO000OO0OOO0 !="饼图":#line:877
        for OO0OOOOO00O000000 ,OOO0O00O000OO0OO0 in zip (OOOO0OO000O00OO0O ,O00OOOO0O0OO00000 ):#line:878
            OOOO00OO00OO0O00O =str (OOO0O00O000OO0OO0 )#line:879
            OO0O0OO0O000O0OOO =(OO0OOOOO00O000000 ,OOO0O00O000OO0OO0 +0.3 )#line:880
            O000000OOOOOO000O .annotate (OOOO00OO00OO0O00O ,xy =OO0O0OO0O000O0OOO ,fontsize =8 ,color ="black",ha ="center",va ="baseline")#line:881
    OOO0OO0O0OOOOO00O =Button (O0OOO0OO0O00O0OO0 ,relief =GROOVE ,activebackground ="green",text ="保存原始数据",command =lambda :TOOLS_save_dict (OO0O0O00000O000O0 ),)#line:891
    OOO0OO0O0OOOOO00O .pack (side =RIGHT )#line:892
    O00OO0O0O0O0000O0 =Button (O0OOO0OO0O00O0OO0 ,relief =GROOVE ,text ="查看原始数据",command =lambda :TOOLS_view_dict (OO0O0O00000O000O0 ,0 ))#line:896
    O00OO0O0O0O0000O0 .pack (side =RIGHT )#line:897
    O0O000OO00OO00O00 =Button (O0OOO0OO0O00O0OO0 ,relief =GROOVE ,text ="饼图",command =lambda :DRAW_make_one (OO0O0O00000O000O0 ,O00000OO0OO0O0O00 ,O0OO0000OO00O0000 ,OO0OO0OO0O0OOO00O ,"饼图"),)#line:905
    O0O000OO00OO00O00 .pack (side =LEFT )#line:906
    O0O000OO00OO00O00 =Button (O0OOO0OO0O00O0OO0 ,relief =GROOVE ,text ="柱状图",command =lambda :DRAW_make_one (OO0O0O00000O000O0 ,O00000OO0OO0O0O00 ,O0OO0000OO00O0000 ,OO0OO0OO0O0OOO00O ,"柱状图"),)#line:913
    O0O000OO00OO00O00 .pack (side =LEFT )#line:914
    O0O000OO00OO00O00 =Button (O0OOO0OO0O00O0OO0 ,relief =GROOVE ,text ="折线图",command =lambda :DRAW_make_one (OO0O0O00000O000O0 ,O00000OO0OO0O0O00 ,O0OO0000OO00O0000 ,OO0OO0OO0O0OOO00O ,"折线图"),)#line:920
    O0O000OO00OO00O00 .pack (side =LEFT )#line:921
    O0O000OO00OO00O00 =Button (O0OOO0OO0O00O0OO0 ,relief =GROOVE ,text ="托帕斯图",command =lambda :DRAW_make_one (OO0O0O00000O000O0 ,O00000OO0OO0O0O00 ,O0OO0000OO00O0000 ,OO0OO0OO0O0OOO00O ,"托帕斯图"),)#line:928
    O0O000OO00OO00O00 .pack (side =LEFT )#line:929
def DRAW_make_mutibar (O00OO0O00000OOOOO ,O0000OO00O0OO0OOO ,O0OOO0OOOOOOOO000 ,OO00OOOO0O00O000O ,O000O0OO00O0O000O ,O00OOOO00OOOOOOO0 ,OO00OO0OO0OOO000O ):#line:930
    ""#line:931
    OOO0OOOO0O0OO00OO =Toplevel ()#line:932
    OOO0OOOO0O0OO00OO .title (OO00OO0OO0OOO000O )#line:933
    O0O0OOO0O0O00O0OO =ttk .Frame (OOO0OOOO0O0OO00OO ,height =20 )#line:934
    O0O0OOO0O0O00O0OO .pack (side =TOP )#line:935
    O0O0O0O000O00000O =0.2 #line:937
    O0OO00O00O00O0OO0 =Figure (figsize =(12 ,6 ),dpi =100 )#line:938
    OOO0OOO00OO0O000O =FigureCanvasTkAgg (O0OO00O00O00O0OO0 ,master =OOO0OOOO0O0OO00OO )#line:939
    OOO0OOO00OO0O000O .draw ()#line:940
    OOO0OOO00OO0O000O .get_tk_widget ().pack (expand =1 )#line:941
    O0O0OO0O00OO00O00 =O0OO00O00O00O0OO0 .add_subplot (111 )#line:942
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:944
    plt .rcParams ['axes.unicode_minus']=False #line:945
    O0O00O0O0OOO00OO0 =NavigationToolbar2Tk (OOO0OOO00OO0O000O ,OOO0OOOO0O0OO00OO )#line:947
    O0O00O0O0OOO00OO0 .update ()#line:948
    OOO0OOO00OO0O000O .get_tk_widget ().pack ()#line:950
    O0000OO00O0OO0OOO =O00OO0O00000OOOOO [O0000OO00O0OO0OOO ]#line:951
    O0OOO0OOOOOOOO000 =O00OO0O00000OOOOO [O0OOO0OOOOOOOO000 ]#line:952
    OO00OOOO0O00O000O =O00OO0O00000OOOOO [OO00OOOO0O00O000O ]#line:953
    OOOOOO00O0O0OO0OO =range (0 ,len (O0000OO00O0OO0OOO ),1 )#line:955
    O0O0OO0O00OO00O00 .set_xticklabels (OO00OOOO0O00O000O ,rotation =-90 ,fontsize =8 )#line:956
    O0O0OO0O00OO00O00 .bar (OOOOOO00O0O0OO0OO ,O0000OO00O0OO0OOO ,align ="center",tick_label =OO00OOOO0O00O000O ,label =O000O0OO00O0O000O )#line:959
    O0O0OO0O00OO00O00 .bar (OOOOOO00O0O0OO0OO ,O0OOO0OOOOOOOO000 ,align ="center",label =O00OOOO00OOOOOOO0 )#line:962
    O0O0OO0O00OO00O00 .set_title (OO00OO0OO0OOO000O )#line:963
    O0O0OO0O00OO00O00 .set_xlabel ("项")#line:964
    O0O0OO0O00OO00O00 .set_ylabel ("数量")#line:965
    O0OO00O00O00O0OO0 .tight_layout (pad =0.4 ,w_pad =3.0 ,h_pad =3.0 )#line:967
    OO0O000OO00000000 =O0O0OO0O00OO00O00 .get_position ()#line:968
    O0O0OO0O00OO00O00 .set_position ([OO0O000OO00000000 .x0 ,OO0O000OO00000000 .y0 ,OO0O000OO00000000 .width *0.7 ,OO0O000OO00000000 .height ])#line:969
    O0O0OO0O00OO00O00 .legend (loc =2 ,bbox_to_anchor =(1.05 ,1.0 ),fontsize =10 ,borderaxespad =0.0 )#line:970
    OOO0OOO00OO0O000O .draw ()#line:972
    OOOOO00OOOO0O000O =Button (O0O0OOO0O0O00O0OO ,relief =GROOVE ,activebackground ="green",text ="保存原始数据",command =lambda :TOOLS_save_dict (O00OO0O00000OOOOO ),)#line:979
    OOOOO00OOOO0O000O .pack (side =RIGHT )#line:980
def CLEAN_hzp (OOOOO00O000OO00O0 ):#line:985
    ""#line:986
    if "报告编码"not in OOOOO00O000OO00O0 .columns :#line:987
            OOOOO00O000OO00O0 ["特殊化妆品注册证书编号/普通化妆品备案编号"]=OOOOO00O000OO00O0 ["特殊化妆品注册证书编号/普通化妆品备案编号"].fillna ("-未填写-")#line:988
            OOOOO00O000OO00O0 ["省级评价结果"]=OOOOO00O000OO00O0 ["省级评价结果"].fillna ("-未填写-")#line:989
            OOOOO00O000OO00O0 ["生产企业"]=OOOOO00O000OO00O0 ["生产企业"].fillna ("-未填写-")#line:990
            OOOOO00O000OO00O0 ["提交人"]="不适用"#line:991
            OOOOO00O000OO00O0 ["医疗机构类别"]="不适用"#line:992
            OOOOO00O000OO00O0 ["经营企业或使用单位"]="不适用"#line:993
            OOOOO00O000OO00O0 ["报告状态"]="报告单位评价"#line:994
            OOOOO00O000OO00O0 ["所属地区"]="不适用"#line:995
            OOOOO00O000OO00O0 ["医院名称"]="不适用"#line:996
            OOOOO00O000OO00O0 ["报告地区名称"]="不适用"#line:997
            OOOOO00O000OO00O0 ["提交人"]="不适用"#line:998
            OOOOO00O000OO00O0 ["型号"]=OOOOO00O000OO00O0 ["化妆品分类"]#line:999
            OOOOO00O000OO00O0 ["关联性评价"]=OOOOO00O000OO00O0 ["上报单位评价结果"]#line:1000
            OOOOO00O000OO00O0 ["规格"]="不适用"#line:1001
            OOOOO00O000OO00O0 ["器械故障表现"]=OOOOO00O000OO00O0 ["初步判断"]#line:1002
            OOOOO00O000OO00O0 ["伤害表现"]=OOOOO00O000OO00O0 ["自觉症状"]+OOOOO00O000OO00O0 ["皮损部位"]+OOOOO00O000OO00O0 ["皮损形态"]#line:1003
            OOOOO00O000OO00O0 ["事件原因分析"]="不适用"#line:1004
            OOOOO00O000OO00O0 ["事件原因分析描述"]="不适用"#line:1005
            OOOOO00O000OO00O0 ["调查情况"]="不适用"#line:1006
            OOOOO00O000OO00O0 ["具体控制措施"]="不适用"#line:1007
            OOOOO00O000OO00O0 ["未采取控制措施原因"]="不适用"#line:1008
            OOOOO00O000OO00O0 ["报告地区名称"]="不适用"#line:1009
            OOOOO00O000OO00O0 ["上报单位所属地区"]="不适用"#line:1010
            OOOOO00O000OO00O0 ["持有人报告状态"]="不适用"#line:1011
            OOOOO00O000OO00O0 ["年龄类型"]="岁"#line:1012
            OOOOO00O000OO00O0 ["经营企业使用单位报告状态"]="不适用"#line:1013
            OOOOO00O000OO00O0 ["产品归属"]="化妆品"#line:1014
            OOOOO00O000OO00O0 ["管理类别"]="不适用"#line:1015
            OOOOO00O000OO00O0 ["超时标记"]="不适用"#line:1016
            OOOOO00O000OO00O0 =OOOOO00O000OO00O0 .rename (columns ={"报告表编号":"报告编码","报告类型":"伤害","报告地区":"监测机构","报告单位名称":"单位名称","患者/消费者姓名":"姓名","不良反应发生日期":"事件发生日期","过程描述补充说明":"使用过程","化妆品名称":"产品名称","化妆品分类":"产品类别","生产企业":"上市许可持有人名称","生产批号":"产品批号","特殊化妆品注册证书编号/普通化妆品备案编号":"注册证编号/曾用注册证编号",})#line:1035
            OOOOO00O000OO00O0 ["时隔"]=pd .to_datetime (OOOOO00O000OO00O0 ["事件发生日期"])-pd .to_datetime (OOOOO00O000OO00O0 ["开始使用日期"])#line:1036
            OOOOO00O000OO00O0 ["时隔"]=OOOOO00O000OO00O0 ["时隔"].astype (str )#line:1037
            OOOOO00O000OO00O0 .loc [(OOOOO00O000OO00O0 ["省级评价结果"]!="-未填写-"),"有效报告"]=1 #line:1038
            OOOOO00O000OO00O0 ["伤害"]=OOOOO00O000OO00O0 ["伤害"].str .replace ("严重","严重伤害",regex =False )#line:1039
            try :#line:1040
	            OOOOO00O000OO00O0 =TOOL_guizheng (OOOOO00O000OO00O0 ,4 ,True )#line:1041
            except :#line:1042
                pass #line:1043
            return OOOOO00O000OO00O0 #line:1044
def CLEAN_yp (OOO00O00O0OO00O00 ):#line:1049
    ""#line:1050
    if "报告编码"not in OOO00O00O0OO00O00 .columns :#line:1051
        if "反馈码"in OOO00O00O0OO00O00 .columns and "报告表编码"not in OOO00O00O0OO00O00 .columns :#line:1053
            OOO00O00O0OO00O00 ["提交人"]="不适用"#line:1055
            OOO00O00O0OO00O00 ["经营企业或使用单位"]="不适用"#line:1056
            OOO00O00O0OO00O00 ["报告状态"]="报告单位评价"#line:1057
            OOO00O00O0OO00O00 ["所属地区"]="不适用"#line:1058
            OOO00O00O0OO00O00 ["产品类别"]="无源"#line:1059
            OOO00O00O0OO00O00 ["医院名称"]="不适用"#line:1060
            OOO00O00O0OO00O00 ["报告地区名称"]="不适用"#line:1061
            OOO00O00O0OO00O00 ["提交人"]="不适用"#line:1062
            OOO00O00O0OO00O00 =OOO00O00O0OO00O00 .rename (columns ={"反馈码":"报告表编码","序号":"药品序号","新的":"报告类型-新的","报告类型":"报告类型-严重程度","用药-日数":"用法-日","用药-次数":"用法-次",})#line:1075
        if "唯一标识"not in OOO00O00O0OO00O00 .columns :#line:1080
            OOO00O00O0OO00O00 ["报告编码"]=OOO00O00O0OO00O00 ["报告表编码"].astype (str )+OOO00O00O0OO00O00 ["患者姓名"].astype (str )#line:1081
        if "唯一标识"in OOO00O00O0OO00O00 .columns :#line:1082
            OOO00O00O0OO00O00 ["唯一标识"]=OOO00O00O0OO00O00 ["唯一标识"].astype (str )#line:1083
            OOO00O00O0OO00O00 =OOO00O00O0OO00O00 .rename (columns ={"唯一标识":"报告编码"})#line:1084
        if "医疗机构类别"not in OOO00O00O0OO00O00 .columns :#line:1085
            OOO00O00O0OO00O00 ["医疗机构类别"]="医疗机构"#line:1086
            OOO00O00O0OO00O00 ["经营企业使用单位报告状态"]="已提交"#line:1087
        try :#line:1088
            OOO00O00O0OO00O00 ["年龄和单位"]=OOO00O00O0OO00O00 ["年龄"].astype (str )+OOO00O00O0OO00O00 ["年龄单位"]#line:1089
        except :#line:1090
            OOO00O00O0OO00O00 ["年龄和单位"]=OOO00O00O0OO00O00 ["年龄"].astype (str )+OOO00O00O0OO00O00 ["年龄类型"]#line:1091
        OOO00O00O0OO00O00 .loc [(OOO00O00O0OO00O00 ["报告类型-新的"]=="新的"),"管理类别"]="Ⅲ类"#line:1092
        OOO00O00O0OO00O00 .loc [(OOO00O00O0OO00O00 ["报告类型-严重程度"]=="严重"),"管理类别"]="Ⅲ类"#line:1093
        text .insert (END ,"剔除已删除报告和重复报告...")#line:1094
        if "删除标识"in OOO00O00O0OO00O00 .columns :#line:1095
            OOO00O00O0OO00O00 =OOO00O00O0OO00O00 [(OOO00O00O0OO00O00 ["删除标识"]!="删除")]#line:1096
        if "重复报告"in OOO00O00O0OO00O00 .columns :#line:1097
            OOO00O00O0OO00O00 =OOO00O00O0OO00O00 [(OOO00O00O0OO00O00 ["重复报告"]!="重复报告")]#line:1098
        OOO00O00O0OO00O00 ["报告类型-新的"]=OOO00O00O0OO00O00 ["报告类型-新的"].fillna (" ")#line:1101
        OOO00O00O0OO00O00 .loc [(OOO00O00O0OO00O00 ["报告类型-严重程度"]=="严重"),"伤害"]="严重伤害"#line:1102
        OOO00O00O0OO00O00 ["伤害"]=OOO00O00O0OO00O00 ["伤害"].fillna ("所有一般")#line:1103
        OOO00O00O0OO00O00 ["伤害PSUR"]=OOO00O00O0OO00O00 ["报告类型-新的"].astype (str )+OOO00O00O0OO00O00 ["报告类型-严重程度"].astype (str )#line:1104
        OOO00O00O0OO00O00 ["用量用量单位"]=OOO00O00O0OO00O00 ["用量"].astype (str )+OOO00O00O0OO00O00 ["用量单位"].astype (str )#line:1105
        OOO00O00O0OO00O00 ["规格"]="不适用"#line:1107
        OOO00O00O0OO00O00 ["事件原因分析"]="不适用"#line:1108
        OOO00O00O0OO00O00 ["事件原因分析描述"]="不适用"#line:1109
        OOO00O00O0OO00O00 ["初步处置情况"]="不适用"#line:1110
        OOO00O00O0OO00O00 ["伤害表现"]=OOO00O00O0OO00O00 ["不良反应名称"]#line:1111
        OOO00O00O0OO00O00 ["产品类别"]="无源"#line:1112
        OOO00O00O0OO00O00 ["调查情况"]="不适用"#line:1113
        OOO00O00O0OO00O00 ["具体控制措施"]="不适用"#line:1114
        OOO00O00O0OO00O00 ["上报单位所属地区"]=OOO00O00O0OO00O00 ["报告地区名称"]#line:1115
        OOO00O00O0OO00O00 ["注册证编号/曾用注册证编号"]=OOO00O00O0OO00O00 ["批准文号"]#line:1118
        OOO00O00O0OO00O00 ["器械故障表现"]=OOO00O00O0OO00O00 ["不良反应名称"]#line:1119
        OOO00O00O0OO00O00 ["型号"]=OOO00O00O0OO00O00 ["剂型"]#line:1120
        OOO00O00O0OO00O00 ["未采取控制措施原因"]="不适用"#line:1123
        OOO00O00O0OO00O00 ["报告单位评价"]=OOO00O00O0OO00O00 ["报告类型-新的"].astype (str )+OOO00O00O0OO00O00 ["报告类型-严重程度"].astype (str )#line:1124
        OOO00O00O0OO00O00 .loc [(OOO00O00O0OO00O00 ["报告类型-新的"]=="新的"),"持有人报告状态"]="待评价"#line:1125
        OOO00O00O0OO00O00 ["用法temp日"]="日"#line:1126
        OOO00O00O0OO00O00 ["用法temp次"]="次"#line:1127
        OOO00O00O0OO00O00 ["用药频率"]=(OOO00O00O0OO00O00 ["用法-日"].astype (str )+OOO00O00O0OO00O00 ["用法temp日"]+OOO00O00O0OO00O00 ["用法-次"].astype (str )+OOO00O00O0OO00O00 ["用法temp次"])#line:1133
        try :#line:1134
            OOO00O00O0OO00O00 ["相关疾病信息[疾病名称]-术语"]=OOO00O00O0OO00O00 ["原患疾病"]#line:1135
            OOO00O00O0OO00O00 ["治疗适应症-术语"]=OOO00O00O0OO00O00 ["用药原因"]#line:1136
        except :#line:1137
            pass #line:1138
        try :#line:1140
            OOO00O00O0OO00O00 =OOO00O00O0OO00O00 .rename (columns ={"提交日期":"报告日期"})#line:1141
            OOO00O00O0OO00O00 =OOO00O00O0OO00O00 .rename (columns ={"提交人":"报告人"})#line:1142
            OOO00O00O0OO00O00 =OOO00O00O0OO00O00 .rename (columns ={"报告状态":"持有人报告状态"})#line:1143
            OOO00O00O0OO00O00 =OOO00O00O0OO00O00 .rename (columns ={"所属地区":"使用单位、经营企业所属监测机构"})#line:1144
            OOO00O00O0OO00O00 =OOO00O00O0OO00O00 .rename (columns ={"医院名称":"单位名称"})#line:1145
            OOO00O00O0OO00O00 =OOO00O00O0OO00O00 .rename (columns ={"通用名称":"产品名称"})#line:1147
            OOO00O00O0OO00O00 =OOO00O00O0OO00O00 .rename (columns ={"生产厂家":"上市许可持有人名称"})#line:1148
            OOO00O00O0OO00O00 =OOO00O00O0OO00O00 .rename (columns ={"不良反应发生时间":"事件发生日期"})#line:1149
            OOO00O00O0OO00O00 =OOO00O00O0OO00O00 .rename (columns ={"不良反应过程描述":"使用过程"})#line:1151
            OOO00O00O0OO00O00 =OOO00O00O0OO00O00 .rename (columns ={"生产批号":"产品批号"})#line:1152
            OOO00O00O0OO00O00 =OOO00O00O0OO00O00 .rename (columns ={"报告地区名称":"使用单位、经营企业所属监测机构"})#line:1153
            OOO00O00O0OO00O00 =OOO00O00O0OO00O00 .rename (columns ={"报告人评价":"关联性评价"})#line:1155
            OOO00O00O0OO00O00 =OOO00O00O0OO00O00 .rename (columns ={"年龄单位":"年龄类型"})#line:1156
        except :#line:1157
            text .insert (END ,"数据规整失败。")#line:1158
            return 0 #line:1159
        OOO00O00O0OO00O00 ['报告日期']=OOO00O00O0OO00O00 ['报告日期'].str .strip ()#line:1162
        OOO00O00O0OO00O00 ['事件发生日期']=OOO00O00O0OO00O00 ['事件发生日期'].str .strip ()#line:1163
        OOO00O00O0OO00O00 ['用药开始时间']=OOO00O00O0OO00O00 ['用药开始时间'].str .strip ()#line:1164
        return OOO00O00O0OO00O00 #line:1166
    if "报告编码"in OOO00O00O0OO00O00 .columns :#line:1167
        return OOO00O00O0OO00O00 #line:1168
def CLEAN_qx (OO0O0O000O0O0OO00 ):#line:1170
		""#line:1171
		if "使用单位、经营企业所属监测机构"not in OO0O0O000O0O0OO00 .columns and "监测机构"not in OO0O0O000O0O0OO00 .columns :#line:1173
			OO0O0O000O0O0OO00 ["使用单位、经营企业所属监测机构"]="本地"#line:1174
		if "上市许可持有人名称"not in OO0O0O000O0O0OO00 .columns :#line:1175
			OO0O0O000O0O0OO00 ["上市许可持有人名称"]=OO0O0O000O0O0OO00 ["单位名称"]#line:1176
		if "注册证编号/曾用注册证编号"not in OO0O0O000O0O0OO00 .columns :#line:1177
			OO0O0O000O0O0OO00 ["注册证编号/曾用注册证编号"]=OO0O0O000O0O0OO00 ["注册证编号"]#line:1178
		if "事件原因分析描述"not in OO0O0O000O0O0OO00 .columns :#line:1179
			OO0O0O000O0O0OO00 ["事件原因分析描述"]="  "#line:1180
		if "初步处置情况"not in OO0O0O000O0O0OO00 .columns :#line:1181
			OO0O0O000O0O0OO00 ["初步处置情况"]="  "#line:1182
		text .insert (END ,"\n正在执行格式规整和增加有关时间、年龄、性别等统计列...")#line:1185
		OO0O0O000O0O0OO00 =OO0O0O000O0O0OO00 .rename (columns ={"使用单位、经营企业所属监测机构":"监测机构"})#line:1186
		OO0O0O000O0O0OO00 ["报告编码"]=OO0O0O000O0O0OO00 ["报告编码"].astype ("str")#line:1187
		OO0O0O000O0O0OO00 ["产品批号"]=OO0O0O000O0O0OO00 ["产品批号"].astype ("str")#line:1188
		OO0O0O000O0O0OO00 ["型号"]=OO0O0O000O0O0OO00 ["型号"].astype ("str")#line:1189
		OO0O0O000O0O0OO00 ["规格"]=OO0O0O000O0O0OO00 ["规格"].astype ("str")#line:1190
		OO0O0O000O0O0OO00 ["注册证编号/曾用注册证编号"]=OO0O0O000O0O0OO00 ["注册证编号/曾用注册证编号"].str .replace ("(","（",regex =False )#line:1191
		OO0O0O000O0O0OO00 ["注册证编号/曾用注册证编号"]=OO0O0O000O0O0OO00 ["注册证编号/曾用注册证编号"].str .replace (")","）",regex =False )#line:1192
		OO0O0O000O0O0OO00 ["注册证编号/曾用注册证编号"]=OO0O0O000O0O0OO00 ["注册证编号/曾用注册证编号"].str .replace ("*","※",regex =False )#line:1193
		OO0O0O000O0O0OO00 ["注册证编号/曾用注册证编号"]=OO0O0O000O0O0OO00 ["注册证编号/曾用注册证编号"].fillna ("-未填写-")#line:1194
		OO0O0O000O0O0OO00 ["产品名称"]=OO0O0O000O0O0OO00 ["产品名称"].str .replace ("*","※",regex =False )#line:1195
		OO0O0O000O0O0OO00 ["产品批号"]=OO0O0O000O0O0OO00 ["产品批号"].str .replace ("(","（",regex =False )#line:1196
		OO0O0O000O0O0OO00 ["产品批号"]=OO0O0O000O0O0OO00 ["产品批号"].str .replace (")","）",regex =False )#line:1197
		OO0O0O000O0O0OO00 ["产品批号"]=OO0O0O000O0O0OO00 ["产品批号"].str .replace ("*","※",regex =False )#line:1198
		OO0O0O000O0O0OO00 ["上市许可持有人名称"]=OO0O0O000O0O0OO00 ["上市许可持有人名称"].fillna ("-未填写-")#line:1202
		OO0O0O000O0O0OO00 ["产品类别"]=OO0O0O000O0O0OO00 ["产品类别"].fillna ("-未填写-")#line:1203
		OO0O0O000O0O0OO00 ["产品名称"]=OO0O0O000O0O0OO00 ["产品名称"].fillna ("-未填写-")#line:1204
		OO0O0O000O0O0OO00 ["注册证编号/曾用注册证编号"]=OO0O0O000O0O0OO00 ["注册证编号/曾用注册证编号"].fillna ("-未填写-")#line:1205
		OO0O0O000O0O0OO00 ["产品批号"]=OO0O0O000O0O0OO00 ["产品批号"].fillna ("-未填写-")#line:1206
		OO0O0O000O0O0OO00 ["型号"]=OO0O0O000O0O0OO00 ["型号"].fillna ("-未填写-")#line:1207
		OO0O0O000O0O0OO00 ["规格"]=OO0O0O000O0O0OO00 ["规格"].fillna ("-未填写-")#line:1208
		OO0O0O000O0O0OO00 ["伤害与评价"]=OO0O0O000O0O0OO00 ["伤害"]+OO0O0O000O0O0OO00 ["持有人报告状态"]#line:1211
		OO0O0O000O0O0OO00 ["注册证备份"]=OO0O0O000O0O0OO00 ["注册证编号/曾用注册证编号"]#line:1212
		OO0O0O000O0O0OO00 ['报告日期']=pd .to_datetime (OO0O0O000O0O0OO00 ['报告日期'],format ='%Y-%m-%d',errors ='coerce')#line:1215
		OO0O0O000O0O0OO00 ['事件发生日期']=pd .to_datetime (OO0O0O000O0O0OO00 ['事件发生日期'],format ='%Y-%m-%d',errors ='coerce')#line:1216
		OO0O0O000O0O0OO00 ["报告月份"]=OO0O0O000O0O0OO00 ["报告日期"].dt .to_period ("M").astype (str )#line:1218
		OO0O0O000O0O0OO00 ["报告季度"]=OO0O0O000O0O0OO00 ["报告日期"].dt .to_period ("Q").astype (str )#line:1219
		OO0O0O000O0O0OO00 ["报告年份"]=OO0O0O000O0O0OO00 ["报告日期"].dt .to_period ("Y").astype (str )#line:1220
		OO0O0O000O0O0OO00 ["事件发生月份"]=OO0O0O000O0O0OO00 ["事件发生日期"].dt .to_period ("M").astype (str )#line:1221
		OO0O0O000O0O0OO00 ["事件发生季度"]=OO0O0O000O0O0OO00 ["事件发生日期"].dt .to_period ("Q").astype (str )#line:1222
		OO0O0O000O0O0OO00 ["事件发生年份"]=OO0O0O000O0O0OO00 ["事件发生日期"].dt .to_period ("Y").astype (str )#line:1223
		if ini ["模式"]=="器械":#line:1227
			OO0O0O000O0O0OO00 ['发现或获知日期']=pd .to_datetime (OO0O0O000O0O0OO00 ['发现或获知日期'],format ='%Y-%m-%d',errors ='coerce')#line:1228
			OO0O0O000O0O0OO00 ["时隔"]=pd .to_datetime (OO0O0O000O0O0OO00 ["发现或获知日期"])-pd .to_datetime (OO0O0O000O0O0OO00 ["事件发生日期"])#line:1229
			OO0O0O000O0O0OO00 ["时隔"]=OO0O0O000O0O0OO00 ["时隔"].astype (str )#line:1230
			OO0O0O000O0O0OO00 ["报告时限"]=pd .to_datetime (OO0O0O000O0O0OO00 ["报告日期"])-pd .to_datetime (OO0O0O000O0O0OO00 ["发现或获知日期"])#line:1231
			OO0O0O000O0O0OO00 ["报告时限"]=OO0O0O000O0O0OO00 ["报告时限"].dt .days #line:1232
			OO0O0O000O0O0OO00 .loc [(OO0O0O000O0O0OO00 ["报告时限"]>20 )&(OO0O0O000O0O0OO00 ["伤害"]=="严重伤害"),"超时标记"]=1 #line:1233
			OO0O0O000O0O0OO00 .loc [(OO0O0O000O0O0OO00 ["报告时限"]>30 )&(OO0O0O000O0O0OO00 ["伤害"]=="其他"),"超时标记"]=1 #line:1234
			OO0O0O000O0O0OO00 .loc [(OO0O0O000O0O0OO00 ["报告时限"]>7 )&(OO0O0O000O0O0OO00 ["伤害"]=="死亡"),"超时标记"]=1 #line:1235
			OO0O0O000O0O0OO00 .loc [(OO0O0O000O0O0OO00 ["经营企业使用单位报告状态"]=="审核通过"),"有效报告"]=1 #line:1237
		if ini ["模式"]=="药品":#line:1240
			OO0O0O000O0O0OO00 ['用药开始时间']=pd .to_datetime (OO0O0O000O0O0OO00 ['用药开始时间'],format ='%Y-%m-%d',errors ='coerce')#line:1241
			OO0O0O000O0O0OO00 ["时隔"]=pd .to_datetime (OO0O0O000O0O0OO00 ["事件发生日期"])-pd .to_datetime (OO0O0O000O0O0OO00 ["用药开始时间"])#line:1242
			OO0O0O000O0O0OO00 ["时隔"]=OO0O0O000O0O0OO00 ["时隔"].astype (str )#line:1243
			OO0O0O000O0O0OO00 ["报告时限"]=pd .to_datetime (OO0O0O000O0O0OO00 ["报告日期"])-pd .to_datetime (OO0O0O000O0O0OO00 ["事件发生日期"])#line:1244
			OO0O0O000O0O0OO00 ["报告时限"]=OO0O0O000O0O0OO00 ["报告时限"].dt .days #line:1245
			OO0O0O000O0O0OO00 .loc [(OO0O0O000O0O0OO00 ["报告时限"]>15 )&(OO0O0O000O0O0OO00 ["报告类型-严重程度"]=="严重"),"超时标记"]=1 #line:1246
			OO0O0O000O0O0OO00 .loc [(OO0O0O000O0O0OO00 ["报告时限"]>30 )&(OO0O0O000O0O0OO00 ["报告类型-严重程度"]=="一般"),"超时标记"]=1 #line:1247
			OO0O0O000O0O0OO00 .loc [(OO0O0O000O0O0OO00 ["报告时限"]>15 )&(OO0O0O000O0O0OO00 ["报告类型-新的"]=="新的"),"超时标记"]=1 #line:1248
			OO0O0O000O0O0OO00 .loc [(OO0O0O000O0O0OO00 ["报告时限"]>1 )&(OO0O0O000O0O0OO00 ["报告类型-严重程度"]=="死亡"),"超时标记"]=1 #line:1249
			OO0O0O000O0O0OO00 .loc [(OO0O0O000O0O0OO00 ["评价状态"]!="未评价"),"有效报告"]=1 #line:1251
		OO0O0O000O0O0OO00 .loc [((OO0O0O000O0O0OO00 ["年龄"]=="未填写")|OO0O0O000O0O0OO00 ["年龄"].isnull ()),"年龄"]=-1 #line:1253
		OO0O0O000O0O0OO00 ["年龄"]=OO0O0O000O0O0OO00 ["年龄"].astype (float )#line:1254
		OO0O0O000O0O0OO00 ["年龄"]=OO0O0O000O0O0OO00 ["年龄"].fillna (-1 )#line:1255
		OO0O0O000O0O0OO00 ["性别"]=OO0O0O000O0O0OO00 ["性别"].fillna ("未填写")#line:1256
		OO0O0O000O0O0OO00 ["年龄段"]="未填写"#line:1257
		try :#line:1258
			OO0O0O000O0O0OO00 .loc [(OO0O0O000O0O0OO00 ["年龄类型"]=="月"),"年龄"]=OO0O0O000O0O0OO00 ["年龄"].values /12 #line:1259
			OO0O0O000O0O0OO00 .loc [(OO0O0O000O0O0OO00 ["年龄类型"]=="月"),"年龄类型"]="岁"#line:1260
		except :#line:1261
			pass #line:1262
		try :#line:1263
			OO0O0O000O0O0OO00 .loc [(OO0O0O000O0O0OO00 ["年龄类型"]=="天"),"年龄"]=OO0O0O000O0O0OO00 ["年龄"].values /365 #line:1264
			OO0O0O000O0O0OO00 .loc [(OO0O0O000O0O0OO00 ["年龄类型"]=="天"),"年龄类型"]="岁"#line:1265
		except :#line:1266
			pass #line:1267
		OO0O0O000O0O0OO00 .loc [(OO0O0O000O0O0OO00 ["年龄"].values <=4 ),"年龄段"]="0-婴幼儿（0-4）"#line:1268
		OO0O0O000O0O0OO00 .loc [(OO0O0O000O0O0OO00 ["年龄"].values >=5 ),"年龄段"]="1-少儿（5-14）"#line:1269
		OO0O0O000O0O0OO00 .loc [(OO0O0O000O0O0OO00 ["年龄"].values >=15 ),"年龄段"]="2-青壮年（15-44）"#line:1270
		OO0O0O000O0O0OO00 .loc [(OO0O0O000O0O0OO00 ["年龄"].values >=45 ),"年龄段"]="3-中年期（45-64）"#line:1271
		OO0O0O000O0O0OO00 .loc [(OO0O0O000O0O0OO00 ["年龄"].values >=65 ),"年龄段"]="4-老年期（≥65）"#line:1272
		OO0O0O000O0O0OO00 .loc [(OO0O0O000O0O0OO00 ["年龄"].values ==-1 ),"年龄段"]="未填写"#line:1273
		OO0O0O000O0O0OO00 ["规整后品类"]="N"#line:1277
		OO0O0O000O0O0OO00 =TOOL_guizheng (OO0O0O000O0O0OO00 ,2 ,True )#line:1278
		if ini ['模式']in ["器械"]:#line:1281
			OO0O0O000O0O0OO00 =TOOL_guizheng (OO0O0O000O0O0OO00 ,3 ,True )#line:1282
		OO0O0O000O0O0OO00 =TOOL_guizheng (OO0O0O000O0O0OO00 ,"课题",True )#line:1286
		try :#line:1288
			OO0O0O000O0O0OO00 ["注册证编号/曾用注册证编号"]=OO0O0O000O0O0OO00 ["注册证编号/曾用注册证编号"].fillna ("未填写")#line:1289
		except :#line:1290
			pass #line:1291
		OO0O0O000O0O0OO00 ["数据清洗完成标记"]="是"#line:1293
		OO0O0O000OOOO000O =OO0O0O000O0O0OO00 .loc [:]#line:1294
		return OO0O0O000O0O0OO00 #line:1295
def TOOLS_fileopen ():#line:1301
    ""#line:1302
    warnings .filterwarnings ('ignore')#line:1303
    OO0OOO00O0OO0OOOO =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:1304
    O00OO0OO0OOOO0000 =Useful_tools_openfiles (OO0OOO00O0OO0OOOO ,0 )#line:1305
    try :#line:1306
        O00OO0OO0OOOO0000 =O00OO0OO0OOOO0000 .loc [:,~O00OO0OO0OOOO0000 .columns .str .contains ("^Unnamed")]#line:1307
    except :#line:1308
        pass #line:1309
    ini ["模式"]="其他"#line:1311
    O0O0O0O00OO000OOO =O00OO0OO0OOOO0000 #line:1312
    TABLE_tree_Level_2 (O0O0O0O00OO000OOO ,0 ,O0O0O0O00OO000OOO )#line:1313
def TOOLS_pinzhong (OO0OOOOO00OOO0OOO ):#line:1316
    ""#line:1317
    OO0OOOOO00OOO0OOO ["患者姓名"]=OO0OOOOO00OOO0OOO ["报告表编码"]#line:1318
    OO0OOOOO00OOO0OOO ["用量"]=OO0OOOOO00OOO0OOO ["用法用量"]#line:1319
    OO0OOOOO00OOO0OOO ["评价状态"]=OO0OOOOO00OOO0OOO ["报告单位评价"]#line:1320
    OO0OOOOO00OOO0OOO ["用量单位"]=""#line:1321
    OO0OOOOO00OOO0OOO ["单位名称"]="不适用"#line:1322
    OO0OOOOO00OOO0OOO ["报告地区名称"]="不适用"#line:1323
    OO0OOOOO00OOO0OOO ["用法-日"]="不适用"#line:1324
    OO0OOOOO00OOO0OOO ["用法-次"]="不适用"#line:1325
    OO0OOOOO00OOO0OOO ["不良反应发生时间"]=OO0OOOOO00OOO0OOO ["不良反应发生时间"].str [0 :10 ]#line:1326
    OO0OOOOO00OOO0OOO ["持有人报告状态"]="待评价"#line:1328
    OO0OOOOO00OOO0OOO =OO0OOOOO00OOO0OOO .rename (columns ={"是否非预期":"报告类型-新的","不良反应-术语":"不良反应名称","持有人/生产厂家":"上市许可持有人名称"})#line:1333
    return OO0OOOOO00OOO0OOO #line:1334
def Useful_tools_openfiles (OOO0O0OOO0O0OO0O0 ,OO00OO00OOO000O0O ):#line:1339
    ""#line:1340
    O0OO0O0O0OOO0OOOO =[pd .read_excel (OOO0O00O0O0OO0000 ,header =0 ,sheet_name =OO00OO00OOO000O0O )for OOO0O00O0O0OO0000 in OOO0O0OOO0O0OO0O0 ]#line:1341
    OO0O0000O00O0O00O =pd .concat (O0OO0O0O0OOO0OOOO ,ignore_index =True ).drop_duplicates ()#line:1342
    return OO0O0000O00O0O00O #line:1343
def TOOLS_allfileopen ():#line:1345
    ""#line:1346
    global ori #line:1347
    global ini #line:1348
    global data #line:1349
    ini ["原始模式"]="否"#line:1350
    warnings .filterwarnings ('ignore')#line:1351
    OO000OOO0OOO0O0O0 =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:1353
    ori =Useful_tools_openfiles (OO000OOO0OOO0O0O0 ,0 )#line:1354
    try :#line:1358
        O0O00OOOOOOO00OO0 =Useful_tools_openfiles (OO000OOO0OOO0O0O0 ,"报告信息")#line:1359
        if "是否非预期"in O0O00OOOOOOO00OO0 .columns :#line:1360
            ori =TOOLS_pinzhong (O0O00OOOOOOO00OO0 )#line:1361
    except :#line:1362
        pass #line:1363
    ini ["模式"]="其他"#line:1365
    try :#line:1367
        ori =Useful_tools_openfiles (OO000OOO0OOO0O0O0 ,"字典数据")#line:1368
        ini ["原始模式"]="是"#line:1369
        if "UDI"in ori .columns :#line:1370
            ini ["模式"]="器械"#line:1371
            data =ori #line:1372
        if "报告类型-新的"in ori .columns :#line:1373
            ini ["模式"]="药品"#line:1374
            data =ori #line:1375
        else :#line:1376
            ini ["模式"]="其他"#line:1377
    except :#line:1378
        pass #line:1379
    try :#line:1382
        ori =ori .loc [:,~ori .columns .str .contains ("^Unnamed")]#line:1383
    except :#line:1384
        pass #line:1385
    if "UDI"in ori .columns and ini ["原始模式"]!="是":#line:1389
        text .insert (END ,"识别出为器械报表,正在进行数据规整...")#line:1390
        ini ["模式"]="器械"#line:1391
        ori =CLEAN_qx (ori )#line:1392
        data =ori #line:1393
    if "报告类型-新的"in ori .columns and ini ["原始模式"]!="是":#line:1394
        text .insert (END ,"识别出为药品报表,正在进行数据规整...")#line:1395
        ini ["模式"]="药品"#line:1396
        ori =CLEAN_yp (ori )#line:1397
        ori =CLEAN_qx (ori )#line:1398
        data =ori #line:1399
    if "光斑贴试验"in ori .columns and ini ["原始模式"]!="是":#line:1400
        text .insert (END ,"识别出为化妆品报表,正在进行数据规整...")#line:1401
        ini ["模式"]="化妆品"#line:1402
        ori =CLEAN_hzp (ori )#line:1403
        ori =CLEAN_qx (ori )#line:1404
        data =ori #line:1405
    if ini ["模式"]=="其他":#line:1408
        text .insert (END ,"\n数据读取成功，行数："+str (len (ori )))#line:1409
        data =ori #line:1410
        PROGRAM_Menubar (root ,data ,0 ,data )#line:1411
        try :#line:1412
            ini ["button"][0 ].pack_forget ()#line:1413
            ini ["button"][1 ].pack_forget ()#line:1414
            ini ["button"][2 ].pack_forget ()#line:1415
            ini ["button"][3 ].pack_forget ()#line:1416
            ini ["button"][4 ].pack_forget ()#line:1417
        except :#line:1418
            pass #line:1419
    else :#line:1421
        ini ["清洗后的文件"]=data #line:1422
        ini ["证号"]=Countall (data ).df_zhenghao ()#line:1423
        text .insert (END ,"\n数据读取成功，行数："+str (len (data )))#line:1424
        PROGRAM_Menubar (root ,data ,0 ,data )#line:1425
        try :#line:1426
            ini ["button"][0 ].pack_forget ()#line:1427
            ini ["button"][1 ].pack_forget ()#line:1428
            ini ["button"][2 ].pack_forget ()#line:1429
            ini ["button"][3 ].pack_forget ()#line:1430
            ini ["button"][4 ].pack_forget ()#line:1431
        except :#line:1432
            pass #line:1433
        O0OOOO0O0000000OO =Button (frame0 ,text ="地市统计",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (data ).df_org ("市级监测机构"),1 ,ori ),)#line:1444
        O0OOOO0O0000000OO .pack ()#line:1445
        OO0000OOOOO0000O0 =Button (frame0 ,text ="县区统计",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (data ).df_org ("监测机构"),1 ,ori ),)#line:1458
        OO0000OOOOO0000O0 .pack ()#line:1459
        OOOO000O0OOOO00O0 =Button (frame0 ,text ="上报单位",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (data ).df_user (),1 ,ori ),)#line:1472
        OOOO000O0OOOO00O0 .pack ()#line:1473
        OO0OOO0O000O00O0O =Button (frame0 ,text ="生产企业",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (data ).df_chiyouren (),1 ,ori ),)#line:1484
        OO0OOO0O000O00O0O .pack ()#line:1485
        O00O000OO00O00O00 =Button (frame0 ,text ="产品统计",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (ini ["证号"],1 ,ori ,ori ,"dfx_zhenghao"),)#line:1496
        O00O000OO00O00O00 .pack ()#line:1497
        ini ["button"]=[O0OOOO0O0000000OO ,OO0000OOOOO0000O0 ,OOOO000O0OOOO00O0 ,OO0OOO0O000O00O0O ,O00O000OO00O00O00 ]#line:1498
    text .insert (END ,"\n")#line:1500
def TOOLS_sql (O0000OOOO000O0O00 ):#line:1502
    ""#line:1503
    warnings .filterwarnings ("ignore")#line:1504
    try :#line:1505
        O0000O000O00O0O0O =O0000OOOO000O0O00 .columns #line:1506
    except :#line:1507
        return 0 #line:1508
    def OO00O00000OOOOO00 (O0O0O0OO0OOO0OO0O ):#line:1510
        try :#line:1511
            O00O00O0OO0OOOOO0 =pd .read_sql_query (sqltext (O0O0O0OO0OOO0OO0O ),con =OO0O000OO000O0O00 )#line:1512
        except :#line:1513
            showinfo (title ="提示",message ="SQL语句有误。")#line:1514
            return 0 #line:1515
        try :#line:1516
            del O00O00O0OO0OOOOO0 ["level_0"]#line:1517
        except :#line:1518
            pass #line:1519
        TABLE_tree_Level_2 (O00O00O0OO0OOOOO0 ,1 ,O0000OOOO000O0O00 )#line:1520
    OOOO00OOO0O00O000 ='sqlite://'#line:1524
    OOOOO0O0OO0OOO0OO =create_engine (OOOO00OOO0O00O000 )#line:1525
    try :#line:1526
        O0000OOOO000O0O00 .to_sql ('data',con =OOOOO0O0OO0OOO0OO ,chunksize =10000 ,if_exists ='replace',index =True )#line:1527
    except :#line:1528
        showinfo (title ="提示",message ="不支持该表格。")#line:1529
        return 0 #line:1530
    OO0O000OO000O0O00 =OOOOO0O0OO0OOO0OO .connect ()#line:1532
    OOOOOO0O0O0O00O0O ="select * from data"#line:1533
    OO00O000O0O0O0000 =Toplevel ()#line:1536
    OO00O000O0O0O0000 .title ("SQL查询")#line:1537
    OO00O000O0O0O0000 .geometry ("700x500")#line:1538
    O00OOOOO00OO00OO0 =ttk .Frame (OO00O000O0O0O0000 ,width =700 ,height =20 )#line:1540
    O00OOOOO00OO00OO0 .pack (side =TOP )#line:1541
    O00O0OOO000OO0OO0 =ttk .Frame (OO00O000O0O0O0000 ,width =700 ,height =20 )#line:1542
    O00O0OOO000OO0OO0 .pack (side =BOTTOM )#line:1543
    try :#line:1546
        OO0OO0OO00OO0O000 =StringVar ()#line:1547
        OO0OO0OO00OO0O000 .set ("select * from data WHERE 单位名称='佛山市第一人民医院'")#line:1548
        O0O0O0O0OOO000O00 =Label (O00OOOOO00OO00OO0 ,text ="SQL查询",anchor ='w')#line:1550
        O0O0O0O0OOO000O00 .pack (side =LEFT )#line:1551
        OOOO0O0O0000OO0OO =Label (O00OOOOO00OO00OO0 ,text ="检索：")#line:1552
        O000OO000O000O00O =Button (O00O0OOO000OO0OO0 ,text ="执行",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",width =700 ,command =lambda :OO00O00000OOOOO00 (O000O0OOO0OOOOO00 .get ("1.0","end")),)#line:1566
        O000OO000O000O00O .pack (side =LEFT )#line:1567
    except EE :#line:1570
        pass #line:1571
    OO0OO0OOO00OOOOO0 =Scrollbar (OO00O000O0O0O0000 )#line:1573
    O000O0OOO0OOOOO00 =Text (OO00O000O0O0O0000 ,height =80 ,width =150 ,bg ="#FFFFFF",font ="微软雅黑")#line:1574
    OO0OO0OOO00OOOOO0 .pack (side =RIGHT ,fill =Y )#line:1575
    O000O0OOO0OOOOO00 .pack ()#line:1576
    OO0OO0OOO00OOOOO0 .config (command =O000O0OOO0OOOOO00 .yview )#line:1577
    O000O0OOO0OOOOO00 .config (yscrollcommand =OO0OO0OOO00OOOOO0 .set )#line:1578
    def O00O00OOO000OO00O (event =None ):#line:1579
        O000O0OOO0OOOOO00 .event_generate ('<<Copy>>')#line:1580
    def OOOO0000000OO0O0O (event =None ):#line:1581
        O000O0OOO0OOOOO00 .event_generate ('<<Paste>>')#line:1582
    def O0O0O0000O0000O0O (OO00O0OOOO00O00OO ,OO000O0O00000O000 ):#line:1583
         TOOLS_savetxt (OO00O0OOOO00O00OO ,OO000O0O00000O000 ,1 )#line:1584
    OO00OO000O0OOO00O =Menu (O000O0OOO0OOOOO00 ,tearoff =False ,)#line:1585
    OO00OO000O0OOO00O .add_command (label ="复制",command =O00O00OOO000OO00O )#line:1586
    OO00OO000O0OOO00O .add_command (label ="粘贴",command =OOOO0000000OO0O0O )#line:1587
    OO00OO000O0OOO00O .add_command (label ="源文件列",command =lambda :PROGRAM_helper (O0000OOOO000O0O00 .columns .to_list ()))#line:1588
    def OO0OO00O000O000O0 (O00000O0O00OO0000 ):#line:1589
         OO00OO000O0OOO00O .post (O00000O0O00OO0000 .x_root ,O00000O0O00OO0000 .y_root )#line:1590
    O000O0OOO0OOOOO00 .bind ("<Button-3>",OO0OO00O000O000O0 )#line:1591
    O000O0OOO0OOOOO00 .insert (END ,OOOOOO0O0O0O00O0O )#line:1595
def TOOLS_view_dict (O000O0OOOOO00O0OO ,OOOO0O0O0OO0OO000 ):#line:1599
    ""#line:1600
    OO00O0OOO00O000OO =Toplevel ()#line:1601
    OO00O0OOO00O000OO .title ("查看数据")#line:1602
    OO00O0OOO00O000OO .geometry ("700x500")#line:1603
    OOOOOOO0OO0O0OOOO =Scrollbar (OO00O0OOO00O000OO )#line:1605
    OOOO000OOO0O00OOO =Text (OO00O0OOO00O000OO ,height =100 ,width =150 )#line:1606
    OOOOOOO0OO0O0OOOO .pack (side =RIGHT ,fill =Y )#line:1607
    OOOO000OOO0O00OOO .pack ()#line:1608
    OOOOOOO0OO0O0OOOO .config (command =OOOO000OOO0O00OOO .yview )#line:1609
    OOOO000OOO0O00OOO .config (yscrollcommand =OOOOOOO0OO0O0OOOO .set )#line:1610
    if OOOO0O0O0OO0OO000 ==1 :#line:1611
        OOOO000OOO0O00OOO .insert (END ,O000O0OOOOO00O0OO )#line:1613
        OOOO000OOO0O00OOO .insert (END ,"\n\n")#line:1614
        return 0 #line:1615
    for O0O000000OO0OOO0O in range (len (O000O0OOOOO00O0OO )):#line:1616
        OOOO000OOO0O00OOO .insert (END ,O000O0OOOOO00O0OO .iloc [O0O000000OO0OOO0O ,0 ])#line:1617
        OOOO000OOO0O00OOO .insert (END ,":")#line:1618
        OOOO000OOO0O00OOO .insert (END ,O000O0OOOOO00O0OO .iloc [O0O000000OO0OOO0O ,1 ])#line:1619
        OOOO000OOO0O00OOO .insert (END ,"\n\n")#line:1620
def TOOLS_save_dict (O00000O0OOOOO00OO ):#line:1622
    ""#line:1623
    OOOOOO0000O0OOO00 =filedialog .asksaveasfilename (title =u"保存文件",initialfile ="排序后的原始数据",defaultextension ="xls",filetypes =[("Excel 97-2003 工作簿","*.xls")],)#line:1629
    try :#line:1630
        O00000O0OOOOO00OO ["详细描述T"]=O00000O0OOOOO00OO ["详细描述T"].astype (str )#line:1631
    except :#line:1632
        pass #line:1633
    try :#line:1634
        O00000O0OOOOO00OO ["报告编码"]=O00000O0OOOOO00OO ["报告编码"].astype (str )#line:1635
    except :#line:1636
        pass #line:1637
    OO0O0OOOOOO000O0O =pd .ExcelWriter (OOOOOO0000O0OOO00 ,engine ="xlsxwriter")#line:1639
    O00000O0OOOOO00OO .to_excel (OO0O0OOOOOO000O0O ,sheet_name ="字典数据")#line:1640
    OO0O0OOOOOO000O0O .close ()#line:1641
    showinfo (title ="提示",message ="文件写入成功。")#line:1642
def TOOLS_savetxt (OO00O00OOO00OO000 ,O00OO0OO000O000OO ,O0OO0O0000OOO00OO ):#line:1644
	""#line:1645
	O0OOO0O00000OOO00 =open (O00OO0OO000O000OO ,"w",encoding ='utf-8')#line:1646
	O0OOO0O00000OOO00 .write (OO00O00OOO00OO000 )#line:1647
	O0OOO0O00000OOO00 .flush ()#line:1649
	if O0OO0O0000OOO00OO ==1 :#line:1650
		showinfo (title ="提示信息",message ="保存成功。")#line:1651
def TOOLS_deep_view (OO0OO0O00OO000O00 ,O0OOO0OO0OO0000O0 ,OO0OOO0O0O000000O ,OO0000000OOO000OO ):#line:1654
    ""#line:1655
    if OO0000000OOO000OO ==0 :#line:1656
        try :#line:1657
            OO0OO0O00OO000O00 [O0OOO0OO0OO0000O0 ]=OO0OO0O00OO000O00 [O0OOO0OO0OO0000O0 ].fillna ("这个没有填写")#line:1658
        except :#line:1659
            pass #line:1660
        OO00OOOOOO00OO0O0 =OO0OO0O00OO000O00 .groupby (O0OOO0OO0OO0000O0 ).agg (计数 =(OO0OOO0O0O000000O [0 ],OO0OOO0O0O000000O [1 ]))#line:1661
    if OO0000000OOO000OO ==1 :#line:1662
            OO00OOOOOO00OO0O0 =pd .pivot_table (OO0OO0O00OO000O00 ,index =O0OOO0OO0OO0000O0 [:-1 ],columns =O0OOO0OO0OO0000O0 [-1 ],values =[OO0OOO0O0O000000O [0 ]],aggfunc ={OO0OOO0O0O000000O [0 ]:OO0OOO0O0O000000O [1 ]},fill_value ="0",margins =True ,dropna =False ,)#line:1673
            OO00OOOOOO00OO0O0 .columns =OO00OOOOOO00OO0O0 .columns .droplevel (0 )#line:1674
            OO00OOOOOO00OO0O0 =OO00OOOOOO00OO0O0 .rename (columns ={"All":"计数"})#line:1675
    if "日期"in O0OOO0OO0OO0000O0 or "时间"in O0OOO0OO0OO0000O0 or "季度"in O0OOO0OO0OO0000O0 :#line:1678
        OO00OOOOOO00OO0O0 =OO00OOOOOO00OO0O0 .sort_values ([O0OOO0OO0OO0000O0 ],ascending =False ,na_position ="last")#line:1681
    else :#line:1682
        OO00OOOOOO00OO0O0 =OO00OOOOOO00OO0O0 .sort_values (by =["计数"],ascending =False ,na_position ="last")#line:1686
    OO00OOOOOO00OO0O0 =OO00OOOOOO00OO0O0 .reset_index ()#line:1687
    OO00OOOOOO00OO0O0 ["构成比(%)"]=round (100 *OO00OOOOOO00OO0O0 ["计数"]/OO00OOOOOO00OO0O0 ["计数"].sum (),2 )#line:1688
    if OO0000000OOO000OO ==0 :#line:1689
        OO00OOOOOO00OO0O0 ["报表类型"]="dfx_deepview"+"_"+str (O0OOO0OO0OO0000O0 )#line:1690
    if OO0000000OOO000OO ==1 :#line:1691
        OO00OOOOOO00OO0O0 ["报表类型"]="dfx_deepview"+"_"+str (O0OOO0OO0OO0000O0 [:-1 ])#line:1692
    return OO00OOOOOO00OO0O0 #line:1693
def TOOLS_easyreadT (OOO0O0OO00OO00000 ):#line:1697
    ""#line:1698
    OOO0O0OO00OO00000 ["#####分隔符#########"]="######################################################################"#line:1701
    O0000O0O00OO0O0OO =OOO0O0OO00OO00000 .stack (dropna =False )#line:1702
    O0000O0O00OO0O0OO =pd .DataFrame (O0000O0O00OO0O0OO ).reset_index ()#line:1703
    O0000O0O00OO0O0OO .columns =["序号","条目","详细描述T"]#line:1704
    O0000O0O00OO0O0OO ["逐条查看"]="逐条查看"#line:1705
    return O0000O0O00OO0O0OO #line:1706
def TOOLS_data_masking (OOOOO0000O0O0O00O ):#line:1708
    ""#line:1709
    from random import choices #line:1710
    from string import ascii_letters ,digits #line:1711
    OOOOO0000O0O0O00O =OOOOO0000O0O0O00O .reset_index (drop =True )#line:1713
    if "单位名称.1"in OOOOO0000O0O0O00O .columns :#line:1714
        OOOO0OOOOOO000O00 ="器械"#line:1715
    else :#line:1716
        OOOO0OOOOOO000O00 ="药品"#line:1717
    OO0O00OOO0OOOOO0O =peizhidir +""+"0（范例）数据脱敏"+".xls"#line:1718
    try :#line:1719
        O0OOO0OOOOOO0OOO0 =pd .read_excel (OO0O00OOO0OOOOO0O ,sheet_name =OOOO0OOOOOO000O00 ,header =0 ,index_col =0 ).reset_index ()#line:1722
    except :#line:1723
        showinfo (title ="错误信息",message ="该功能需要配置文件才能使用！")#line:1724
        return 0 #line:1725
    OOOO0O00OOO000O00 =0 #line:1726
    O00O00OOOOOOOO0O0 =len (OOOOO0000O0O0O00O )#line:1727
    OOOOO0000O0O0O00O ["abcd"]="□"#line:1728
    for O000000OOOO0O0O00 in O0OOO0OOOOOO0OOO0 ["要脱敏的列"]:#line:1729
        OOOO0O00OOO000O00 =OOOO0O00OOO000O00 +1 #line:1730
        PROGRAM_change_schedule (OOOO0O00OOO000O00 ,O00O00OOOOOOOO0O0 )#line:1731
        text .insert (END ,"\n正在对以下列进行脱敏处理：")#line:1732
        text .see (END )#line:1733
        text .insert (END ,O000000OOOO0O0O00 )#line:1734
        try :#line:1735
            OO0000O0O00OOOO00 =set (OOOOO0000O0O0O00O [O000000OOOO0O0O00 ])#line:1736
        except :#line:1737
            showinfo (title ="提示",message ="脱敏文件配置错误，请修改配置表。")#line:1738
            return 0 #line:1739
        O0OOO00000O00OO00 ={OO000OOOO0O0OOO0O :"".join (choices (digits ,k =10 ))for OO000OOOO0O0OOO0O in OO0000O0O00OOOO00 }#line:1740
        OOOOO0000O0O0O00O [O000000OOOO0O0O00 ]=OOOOO0000O0O0O00O [O000000OOOO0O0O00 ].map (O0OOO00000O00OO00 )#line:1741
        OOOOO0000O0O0O00O [O000000OOOO0O0O00 ]=OOOOO0000O0O0O00O ["abcd"]+OOOOO0000O0O0O00O [O000000OOOO0O0O00 ].astype (str )#line:1742
    try :#line:1743
        PROGRAM_change_schedule (10 ,10 )#line:1744
        del OOOOO0000O0O0O00O ["abcd"]#line:1745
        OO0O000OOO000O0OO =filedialog .asksaveasfilename (title =u"保存脱敏后的文件",initialfile ="脱敏后的文件",defaultextension ="xlsx",filetypes =[("Excel 工作簿","*.xlsx"),("Excel 97-2003 工作簿","*.xls")],)#line:1751
        O0O0OOO000OOOOOO0 =pd .ExcelWriter (OO0O000OOO000O0OO ,engine ="xlsxwriter")#line:1752
        OOOOO0000O0O0O00O .to_excel (O0O0OOO000OOOOOO0 ,sheet_name ="sheet0")#line:1753
        O0O0OOO000OOOOOO0 .close ()#line:1754
    except :#line:1755
        text .insert (END ,"\n文件未保存，但导入的数据已按要求脱敏。")#line:1756
    text .insert (END ,"\n脱敏操作完成。")#line:1757
    text .see (END )#line:1758
    return OOOOO0000O0O0O00O #line:1759
def TOOLS_get_new (O0O00OOO0O0OOO0O0 ,OO000OO0O0O000OOO ):#line:1761
	""#line:1762
	def OOOOO00000OOOOO00 (O0O00O00O0O0OOO0O ):#line:1763
		""#line:1764
		O0O00O00O0O0OOO0O =O0O00O00O0O0OOO0O .drop_duplicates ("报告编码")#line:1765
		OOO000O00O000OO00 =str (Counter (TOOLS_get_list0 ("use(器械故障表现).file",O0O00O00O0O0OOO0O ,1000 ))).replace ("Counter({","{")#line:1766
		OOO000O00O000OO00 =OOO000O00O000OO00 .replace ("})","}")#line:1767
		import ast #line:1768
		O0OO0000OOOOOO0O0 =ast .literal_eval (OOO000O00O000OO00 )#line:1769
		OOOO0O00OOOOOO00O =TOOLS_easyreadT (pd .DataFrame ([O0OO0000OOOOOO0O0 ]))#line:1770
		OOOO0O00OOOOOO00O =OOOO0O00OOOOOO00O .rename (columns ={"逐条查看":"ADR名称规整"})#line:1771
		return OOOO0O00OOOOOO00O #line:1772
	if OO000OO0O0O000OOO =="证号":#line:1773
		root .attributes ("-topmost",True )#line:1774
		root .attributes ("-topmost",False )#line:1775
		OO00O000O0OOO0OOO =O0O00OOO0O0OOO0O0 .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"]).agg (计数 =("报告编码","nunique")).reset_index ()#line:1776
		O0O0OOO0O0O00O00O =OO00O000O0OOO0OOO .drop_duplicates ("注册证编号/曾用注册证编号").copy ()#line:1777
		O0O0OOO0O0O00O00O ["所有不良反应"]=""#line:1778
		O0O0OOO0O0O00O00O ["关注建议"]=""#line:1779
		O0O0OOO0O0O00O00O ["疑似新的"]=""#line:1780
		O0O0OOO0O0O00O00O ["疑似旧的"]=""#line:1781
		O0O0OOO0O0O00O00O ["疑似新的（高敏）"]=""#line:1782
		O0O0OOO0O0O00O00O ["疑似旧的（高敏）"]=""#line:1783
		OOO0O0OO0O00000OO =1 #line:1784
		O0OOOOO0000OOOO00 =int (len (O0O0OOO0O0O00O00O ))#line:1785
		for O00OO0000O000OO00 ,O00OO0O00O0O000OO in O0O0OOO0O0O00O00O .iterrows ():#line:1786
			OOO00O0000OO00O0O =O0O00OOO0O0OOO0O0 [(O0O00OOO0O0OOO0O0 ["注册证编号/曾用注册证编号"]==O00OO0O00O0O000OO ["注册证编号/曾用注册证编号"])]#line:1787
			OOO0OO0OO0O0O00OO =OOO00O0000OO00O0O .loc [OOO00O0000OO00O0O ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1788
			O00O000OOO00OO00O =OOO00O0000OO00O0O .loc [~OOO00O0000OO00O0O ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1789
			O0O00000OOOOOO000 =OOOOO00000OOOOO00 (OOO0OO0OO0O0O00OO )#line:1790
			OO0OOOOO0O00000OO =OOOOO00000OOOOO00 (O00O000OOO00OO00O )#line:1791
			O0000OO00O0O000O0 =OOOOO00000OOOOO00 (OOO00O0000OO00O0O )#line:1792
			PROGRAM_change_schedule (OOO0O0OO0O00000OO ,O0OOOOO0000OOOO00 )#line:1793
			OOO0O0OO0O00000OO =OOO0O0OO0O00000OO +1 #line:1794
			for O0O0O00O00O00OOO0 ,OO000O0OO00O0O00O in O0000OO00O0O000O0 .iterrows ():#line:1796
					if "分隔符"not in OO000O0OO00O0O00O ["条目"]:#line:1797
						O0O0OO000000OOO0O ="'"+str (OO000O0OO00O0O00O ["条目"])+"':"+str (OO000O0OO00O0O00O ["详细描述T"])+","#line:1798
						O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"所有不良反应"]=O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"所有不良反应"]+O0O0OO000000OOO0O #line:1799
			for O0O0O00O00O00OOO0 ,OO000O0OO00O0O00O in OO0OOOOO0O00000OO .iterrows ():#line:1801
					if "分隔符"not in OO000O0OO00O0O00O ["条目"]:#line:1802
						O0O0OO000000OOO0O ="'"+str (OO000O0OO00O0O00O ["条目"])+"':"+str (OO000O0OO00O0O00O ["详细描述T"])+","#line:1803
						O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"疑似旧的"]=O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"疑似旧的"]+O0O0OO000000OOO0O #line:1804
					if "分隔符"not in OO000O0OO00O0O00O ["条目"]and int (OO000O0OO00O0O00O ["详细描述T"])>=2 :#line:1806
						O0O0OO000000OOO0O ="'"+str (OO000O0OO00O0O00O ["条目"])+"':"+str (OO000O0OO00O0O00O ["详细描述T"])+","#line:1807
						O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"疑似旧的（高敏）"]=O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"疑似旧的（高敏）"]+O0O0OO000000OOO0O #line:1808
			for O0O0O00O00O00OOO0 ,OO000O0OO00O0O00O in O0O00000OOOOOO000 .iterrows ():#line:1810
				if str (OO000O0OO00O0O00O ["条目"]).strip ()not in str (O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"疑似旧的"])and "分隔符"not in str (OO000O0OO00O0O00O ["条目"]):#line:1811
					O0O0OO000000OOO0O ="'"+str (OO000O0OO00O0O00O ["条目"])+"':"+str (OO000O0OO00O0O00O ["详细描述T"])+","#line:1812
					O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"疑似新的"]=O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"疑似新的"]+O0O0OO000000OOO0O #line:1813
					if int (OO000O0OO00O0O00O ["详细描述T"])>=3 :#line:1814
						O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"关注建议"]=O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"关注建议"]+"！"#line:1815
					if int (OO000O0OO00O0O00O ["详细描述T"])>=5 :#line:1816
						O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"关注建议"]=O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"关注建议"]+"●"#line:1817
				if str (OO000O0OO00O0O00O ["条目"]).strip ()not in str (O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"疑似旧的（高敏）"])and "分隔符"not in str (OO000O0OO00O0O00O ["条目"])and int (OO000O0OO00O0O00O ["详细描述T"])>=2 :#line:1819
					O0O0OO000000OOO0O ="'"+str (OO000O0OO00O0O00O ["条目"])+"':"+str (OO000O0OO00O0O00O ["详细描述T"])+","#line:1820
					O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"疑似新的（高敏）"]=O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"疑似新的（高敏）"]+O0O0OO000000OOO0O #line:1821
		O0O0OOO0O0O00O00O ["疑似新的"]="{"+O0O0OOO0O0O00O00O ["疑似新的"]+"}"#line:1823
		O0O0OOO0O0O00O00O ["疑似旧的"]="{"+O0O0OOO0O0O00O00O ["疑似旧的"]+"}"#line:1824
		O0O0OOO0O0O00O00O ["所有不良反应"]="{"+O0O0OOO0O0O00O00O ["所有不良反应"]+"}"#line:1825
		O0O0OOO0O0O00O00O ["疑似新的（高敏）"]="{"+O0O0OOO0O0O00O00O ["疑似新的（高敏）"]+"}"#line:1826
		O0O0OOO0O0O00O00O ["疑似旧的（高敏）"]="{"+O0O0OOO0O0O00O00O ["疑似旧的（高敏）"]+"}"#line:1827
		O0O0OOO0O0O00O00O =O0O0OOO0O0O00O00O .rename (columns ={"器械待评价(药品新的报告比例)":"新的报告比例"})#line:1829
		O0O0OOO0O0O00O00O =O0O0OOO0O0O00O00O .rename (columns ={"严重伤害待评价比例(药品严重中新的比例)":"严重报告中新的比例"})#line:1830
		O0O0OOO0O0O00O00O ["报表类型"]="dfx_zhenghao"#line:1831
		O000OOOO0O00O0OOO =pd .pivot_table (O0O00OOO0O0OOO0O0 ,values =["报告编码"],index =["注册证编号/曾用注册证编号"],columns ="报告单位评价",aggfunc ={"报告编码":"nunique"},fill_value ="0",margins =True ,dropna =False ,).rename (columns ={"报告编码":"数量"})#line:1833
		O000OOOO0O00O0OOO .columns =O000OOOO0O00O0OOO .columns .droplevel (0 )#line:1834
		O0O0OOO0O0O00O00O =pd .merge (O0O0OOO0O0O00O00O ,O000OOOO0O00O0OOO .reset_index (),on =["注册证编号/曾用注册证编号"],how ="left")#line:1835
		TABLE_tree_Level_2 (O0O0OOO0O0O00O00O .sort_values (by ="计数",ascending =[False ],na_position ="last"),1 ,O0O00OOO0O0OOO0O0 )#line:1839
	if OO000OO0O0O000OOO =="品种":#line:1840
		root .attributes ("-topmost",True )#line:1841
		root .attributes ("-topmost",False )#line:1842
		OO00O000O0OOO0OOO =O0O00OOO0O0OOO0O0 .groupby (["产品类别","产品名称"]).agg (计数 =("报告编码","nunique")).reset_index ()#line:1843
		O0O0OOO0O0O00O00O =OO00O000O0OOO0OOO .drop_duplicates ("产品名称").copy ()#line:1844
		O0O0OOO0O0O00O00O ["产品名称"]=O0O0OOO0O0O00O00O ["产品名称"].str .replace ("*","",regex =False )#line:1845
		O0O0OOO0O0O00O00O ["所有不良反应"]=""#line:1846
		O0O0OOO0O0O00O00O ["关注建议"]=""#line:1847
		O0O0OOO0O0O00O00O ["疑似新的"]=""#line:1848
		O0O0OOO0O0O00O00O ["疑似旧的"]=""#line:1849
		O0O0OOO0O0O00O00O ["疑似新的（高敏）"]=""#line:1850
		O0O0OOO0O0O00O00O ["疑似旧的（高敏）"]=""#line:1851
		OOO0O0OO0O00000OO =1 #line:1852
		O0OOOOO0000OOOO00 =int (len (O0O0OOO0O0O00O00O ))#line:1853
		for O00OO0000O000OO00 ,O00OO0O00O0O000OO in O0O0OOO0O0O00O00O .iterrows ():#line:1856
			OOO00O0000OO00O0O =O0O00OOO0O0OOO0O0 [(O0O00OOO0O0OOO0O0 ["产品名称"]==O00OO0O00O0O000OO ["产品名称"])]#line:1858
			OOO0OO0OO0O0O00OO =OOO00O0000OO00O0O .loc [OOO00O0000OO00O0O ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1860
			O00O000OOO00OO00O =OOO00O0000OO00O0O .loc [~OOO00O0000OO00O0O ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1861
			O0000OO00O0O000O0 =OOOOO00000OOOOO00 (OOO00O0000OO00O0O )#line:1862
			O0O00000OOOOOO000 =OOOOO00000OOOOO00 (OOO0OO0OO0O0O00OO )#line:1863
			OO0OOOOO0O00000OO =OOOOO00000OOOOO00 (O00O000OOO00OO00O )#line:1864
			PROGRAM_change_schedule (OOO0O0OO0O00000OO ,O0OOOOO0000OOOO00 )#line:1865
			OOO0O0OO0O00000OO =OOO0O0OO0O00000OO +1 #line:1866
			for O0O0O00O00O00OOO0 ,OO000O0OO00O0O00O in O0000OO00O0O000O0 .iterrows ():#line:1868
					if "分隔符"not in OO000O0OO00O0O00O ["条目"]:#line:1869
						O0O0OO000000OOO0O ="'"+str (OO000O0OO00O0O00O ["条目"])+"':"+str (OO000O0OO00O0O00O ["详细描述T"])+","#line:1870
						O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"所有不良反应"]=O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"所有不良反应"]+O0O0OO000000OOO0O #line:1871
			for O0O0O00O00O00OOO0 ,OO000O0OO00O0O00O in OO0OOOOO0O00000OO .iterrows ():#line:1874
					if "分隔符"not in OO000O0OO00O0O00O ["条目"]:#line:1875
						O0O0OO000000OOO0O ="'"+str (OO000O0OO00O0O00O ["条目"])+"':"+str (OO000O0OO00O0O00O ["详细描述T"])+","#line:1876
						O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"疑似旧的"]=O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"疑似旧的"]+O0O0OO000000OOO0O #line:1877
					if "分隔符"not in OO000O0OO00O0O00O ["条目"]and int (OO000O0OO00O0O00O ["详细描述T"])>=2 :#line:1879
						O0O0OO000000OOO0O ="'"+str (OO000O0OO00O0O00O ["条目"])+"':"+str (OO000O0OO00O0O00O ["详细描述T"])+","#line:1880
						O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"疑似旧的（高敏）"]=O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"疑似旧的（高敏）"]+O0O0OO000000OOO0O #line:1881
			for O0O0O00O00O00OOO0 ,OO000O0OO00O0O00O in O0O00000OOOOOO000 .iterrows ():#line:1883
				if str (OO000O0OO00O0O00O ["条目"]).strip ()not in str (O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"疑似旧的"])and "分隔符"not in str (OO000O0OO00O0O00O ["条目"]):#line:1884
					O0O0OO000000OOO0O ="'"+str (OO000O0OO00O0O00O ["条目"])+"':"+str (OO000O0OO00O0O00O ["详细描述T"])+","#line:1885
					O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"疑似新的"]=O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"疑似新的"]+O0O0OO000000OOO0O #line:1886
					if int (OO000O0OO00O0O00O ["详细描述T"])>=3 :#line:1887
						O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"关注建议"]=O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"关注建议"]+"！"#line:1888
					if int (OO000O0OO00O0O00O ["详细描述T"])>=5 :#line:1889
						O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"关注建议"]=O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"关注建议"]+"●"#line:1890
				if str (OO000O0OO00O0O00O ["条目"]).strip ()not in str (O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"疑似旧的（高敏）"])and "分隔符"not in str (OO000O0OO00O0O00O ["条目"])and int (OO000O0OO00O0O00O ["详细描述T"])>=2 :#line:1892
					O0O0OO000000OOO0O ="'"+str (OO000O0OO00O0O00O ["条目"])+"':"+str (OO000O0OO00O0O00O ["详细描述T"])+","#line:1893
					O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"疑似新的（高敏）"]=O0O0OOO0O0O00O00O .loc [O00OO0000O000OO00 ,"疑似新的（高敏）"]+O0O0OO000000OOO0O #line:1894
		O0O0OOO0O0O00O00O ["疑似新的"]="{"+O0O0OOO0O0O00O00O ["疑似新的"]+"}"#line:1896
		O0O0OOO0O0O00O00O ["疑似旧的"]="{"+O0O0OOO0O0O00O00O ["疑似旧的"]+"}"#line:1897
		O0O0OOO0O0O00O00O ["所有不良反应"]="{"+O0O0OOO0O0O00O00O ["所有不良反应"]+"}"#line:1898
		O0O0OOO0O0O00O00O ["疑似新的（高敏）"]="{"+O0O0OOO0O0O00O00O ["疑似新的（高敏）"]+"}"#line:1899
		O0O0OOO0O0O00O00O ["疑似旧的（高敏）"]="{"+O0O0OOO0O0O00O00O ["疑似旧的（高敏）"]+"}"#line:1900
		O0O0OOO0O0O00O00O ["报表类型"]="dfx_chanpin"#line:1901
		O000OOOO0O00O0OOO =pd .pivot_table (O0O00OOO0O0OOO0O0 ,values =["报告编码"],index =["产品名称"],columns ="报告单位评价",aggfunc ={"报告编码":"nunique"},fill_value ="0",margins =True ,dropna =False ,).rename (columns ={"报告编码":"数量"})#line:1903
		O000OOOO0O00O0OOO .columns =O000OOOO0O00O0OOO .columns .droplevel (0 )#line:1904
		O0O0OOO0O0O00O00O =pd .merge (O0O0OOO0O0O00O00O ,O000OOOO0O00O0OOO .reset_index (),on =["产品名称"],how ="left")#line:1905
		TABLE_tree_Level_2 (O0O0OOO0O0O00O00O .sort_values (by ="计数",ascending =[False ],na_position ="last"),1 ,O0O00OOO0O0OOO0O0 )#line:1906
	if OO000OO0O0O000OOO =="页面":#line:1908
		O0O000000OOO00O00 =""#line:1909
		O0000000O0O0O00OO =""#line:1910
		OOO0OO0OO0O0O00OO =O0O00OOO0O0OOO0O0 .loc [O0O00OOO0O0OOO0O0 ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1911
		O00O000OOO00OO00O =O0O00OOO0O0OOO0O0 .loc [~O0O00OOO0O0OOO0O0 ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1912
		O0O00000OOOOOO000 =OOOOO00000OOOOO00 (OOO0OO0OO0O0O00OO )#line:1913
		OO0OOOOO0O00000OO =OOOOO00000OOOOO00 (O00O000OOO00OO00O )#line:1914
		if 1 ==1 :#line:1915
			for O0O0O00O00O00OOO0 ,OO000O0OO00O0O00O in OO0OOOOO0O00000OO .iterrows ():#line:1916
					if "分隔符"not in OO000O0OO00O0O00O ["条目"]:#line:1917
						O0O0OO000000OOO0O ="'"+str (OO000O0OO00O0O00O ["条目"])+"':"+str (OO000O0OO00O0O00O ["详细描述T"])+","#line:1918
						O0000000O0O0O00OO =O0000000O0O0O00OO +O0O0OO000000OOO0O #line:1919
			for O0O0O00O00O00OOO0 ,OO000O0OO00O0O00O in O0O00000OOOOOO000 .iterrows ():#line:1920
				if str (OO000O0OO00O0O00O ["条目"]).strip ()not in O0000000O0O0O00OO and "分隔符"not in str (OO000O0OO00O0O00O ["条目"]):#line:1921
					O0O0OO000000OOO0O ="'"+str (OO000O0OO00O0O00O ["条目"])+"':"+str (OO000O0OO00O0O00O ["详细描述T"])+","#line:1922
					O0O000000OOO00O00 =O0O000000OOO00O00 +O0O0OO000000OOO0O #line:1923
		O0000000O0O0O00OO ="{"+O0000000O0O0O00OO +"}"#line:1924
		O0O000000OOO00O00 ="{"+O0O000000OOO00O00 +"}"#line:1925
		O00O0OOO0O0OO000O ="\n可能是新的不良反应：\n\n"+O0O000000OOO00O00 +"\n\n\n可能不是新的不良反应：\n\n"+O0000000O0O0O00OO #line:1926
		TOOLS_view_dict (O00O0OOO0O0OO000O ,1 )#line:1927
def TOOLS_strdict_to_pd (OOO00OO0O000000OO ):#line:1929
	""#line:1930
	return pd .DataFrame .from_dict (eval (OOO00OO0O000000OO ),orient ="index",columns =["content"]).reset_index ()#line:1931
def TOOLS_xuanze (O00O00O000O0OOOOO ,O0OOOOOOO000000OO ):#line:1933
    ""#line:1934
    if O0OOOOOOO000000OO ==0 :#line:1935
        O0000OOOOO0OO0OOO =pd .read_excel (filedialog .askopenfilename (filetypes =[("XLS",".xls")]),sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:1936
    else :#line:1937
        O0000OOOOO0OO0OOO =pd .read_excel (peizhidir +"0（范例）批量筛选.xls",sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:1938
    O00O00O000O0OOOOO ["temppr"]=""#line:1939
    for OO0O0O00OO0O00OOO in O0000OOOOO0OO0OOO .columns .tolist ():#line:1940
        O00O00O000O0OOOOO ["temppr"]=O00O00O000O0OOOOO ["temppr"]+"----"+O00O00O000O0OOOOO [OO0O0O00OO0O00OOO ]#line:1941
    O0OOO0OOO00O0OO0O ="测试字段MMMMM"#line:1942
    for OO0O0O00OO0O00OOO in O0000OOOOO0OO0OOO .columns .tolist ():#line:1943
        for OO0O0OO0O00OOO0OO in O0000OOOOO0OO0OOO [OO0O0O00OO0O00OOO ].drop_duplicates ():#line:1945
            if OO0O0OO0O00OOO0OO :#line:1946
                O0OOO0OOO00O0OO0O =O0OOO0OOO00O0OO0O +"|"+str (OO0O0OO0O00OOO0OO )#line:1947
    O00O00O000O0OOOOO =O00O00O000O0OOOOO .loc [O00O00O000O0OOOOO ["temppr"].str .contains (O0OOO0OOO00O0OO0O ,na =False )].copy ()#line:1948
    del O00O00O000O0OOOOO ["temppr"]#line:1949
    O00O00O000O0OOOOO =O00O00O000O0OOOOO .reset_index (drop =True )#line:1950
    TABLE_tree_Level_2 (O00O00O000O0OOOOO ,0 ,O00O00O000O0OOOOO )#line:1952
def TOOLS_add_c (OOOOO000O0O00O0OO ,OO000000O0O0OO0O0 ):#line:1954
			OOOOO000O0O00O0OO ["关键字查找列o"]=""#line:1955
			for OOO000OOO0OOO0000 in TOOLS_get_list (OO000000O0O0OO0O0 ["查找列"]):#line:1956
				OOOOO000O0O00O0OO ["关键字查找列o"]=OOOOO000O0O00O0OO ["关键字查找列o"]+OOOOO000O0O00O0OO [OOO000OOO0OOO0000 ].astype ("str")#line:1957
			if OO000000O0O0OO0O0 ["条件"]=="等于":#line:1958
				OOOOO000O0O00O0OO .loc [(OOOOO000O0O00O0OO [OO000000O0O0OO0O0 ["查找列"]].astype (str )==str (OO000000O0O0OO0O0 ["条件值"])),OO000000O0O0OO0O0 ["赋值列名"]]=OO000000O0O0OO0O0 ["赋值"]#line:1959
			if OO000000O0O0OO0O0 ["条件"]=="大于":#line:1960
				OOOOO000O0O00O0OO .loc [(OOOOO000O0O00O0OO [OO000000O0O0OO0O0 ["查找列"]].astype (float )>OO000000O0O0OO0O0 ["条件值"]),OO000000O0O0OO0O0 ["赋值列名"]]=OO000000O0O0OO0O0 ["赋值"]#line:1961
			if OO000000O0O0OO0O0 ["条件"]=="小于":#line:1962
				OOOOO000O0O00O0OO .loc [(OOOOO000O0O00O0OO [OO000000O0O0OO0O0 ["查找列"]].astype (float )<OO000000O0O0OO0O0 ["条件值"]),OO000000O0O0OO0O0 ["赋值列名"]]=OO000000O0O0OO0O0 ["赋值"]#line:1963
			if OO000000O0O0OO0O0 ["条件"]=="介于":#line:1964
				OO00OO00OO0O0O0OO =TOOLS_get_list (OO000000O0O0OO0O0 ["条件值"])#line:1965
				OOOOO000O0O00O0OO .loc [((OOOOO000O0O00O0OO [OO000000O0O0OO0O0 ["查找列"]].astype (float )<float (OO00OO00OO0O0O0OO [1 ]))&(OOOOO000O0O00O0OO [OO000000O0O0OO0O0 ["查找列"]].astype (float )>float (OO00OO00OO0O0O0OO [0 ]))),OO000000O0O0OO0O0 ["赋值列名"]]=OO000000O0O0OO0O0 ["赋值"]#line:1966
			if OO000000O0O0OO0O0 ["条件"]=="不含":#line:1967
				OOOOO000O0O00O0OO .loc [(~OOOOO000O0O00O0OO ["关键字查找列o"].str .contains (OO000000O0O0OO0O0 ["条件值"])),OO000000O0O0OO0O0 ["赋值列名"]]=OO000000O0O0OO0O0 ["赋值"]#line:1968
			if OO000000O0O0OO0O0 ["条件"]=="包含":#line:1969
				OOOOO000O0O00O0OO .loc [OOOOO000O0O00O0OO ["关键字查找列o"].str .contains (OO000000O0O0OO0O0 ["条件值"],na =False ),OO000000O0O0OO0O0 ["赋值列名"]]=OO000000O0O0OO0O0 ["赋值"]#line:1970
			if OO000000O0O0OO0O0 ["条件"]=="同时包含":#line:1971
				O0OO0O0000OOO0O00 =TOOLS_get_list0 (OO000000O0O0OO0O0 ["条件值"],0 )#line:1972
				if len (O0OO0O0000OOO0O00 )==1 :#line:1973
				    OOOOO000O0O00O0OO .loc [OOOOO000O0O00O0OO ["关键字查找列o"].str .contains (O0OO0O0000OOO0O00 [0 ],na =False ),OO000000O0O0OO0O0 ["赋值列名"]]=OO000000O0O0OO0O0 ["赋值"]#line:1974
				if len (O0OO0O0000OOO0O00 )==2 :#line:1975
				    OOOOO000O0O00O0OO .loc [(OOOOO000O0O00O0OO ["关键字查找列o"].str .contains (O0OO0O0000OOO0O00 [0 ],na =False ))&(OOOOO000O0O00O0OO ["关键字查找列o"].str .contains (O0OO0O0000OOO0O00 [1 ],na =False )),OO000000O0O0OO0O0 ["赋值列名"]]=OO000000O0O0OO0O0 ["赋值"]#line:1976
				if len (O0OO0O0000OOO0O00 )==3 :#line:1977
				    OOOOO000O0O00O0OO .loc [(OOOOO000O0O00O0OO ["关键字查找列o"].str .contains (O0OO0O0000OOO0O00 [0 ],na =False ))&(OOOOO000O0O00O0OO ["关键字查找列o"].str .contains (O0OO0O0000OOO0O00 [1 ],na =False ))&(OOOOO000O0O00O0OO ["关键字查找列o"].str .contains (O0OO0O0000OOO0O00 [2 ],na =False )),OO000000O0O0OO0O0 ["赋值列名"]]=OO000000O0O0OO0O0 ["赋值"]#line:1978
				if len (O0OO0O0000OOO0O00 )==4 :#line:1979
				    OOOOO000O0O00O0OO .loc [(OOOOO000O0O00O0OO ["关键字查找列o"].str .contains (O0OO0O0000OOO0O00 [0 ],na =False ))&(OOOOO000O0O00O0OO ["关键字查找列o"].str .contains (O0OO0O0000OOO0O00 [1 ],na =False ))&(OOOOO000O0O00O0OO ["关键字查找列o"].str .contains (O0OO0O0000OOO0O00 [2 ],na =False ))&(OOOOO000O0O00O0OO ["关键字查找列o"].str .contains (O0OO0O0000OOO0O00 [3 ],na =False )),OO000000O0O0OO0O0 ["赋值列名"]]=OO000000O0O0OO0O0 ["赋值"]#line:1980
				if len (O0OO0O0000OOO0O00 )==5 :#line:1981
				    OOOOO000O0O00O0OO .loc [(OOOOO000O0O00O0OO ["关键字查找列o"].str .contains (O0OO0O0000OOO0O00 [0 ],na =False ))&(OOOOO000O0O00O0OO ["关键字查找列o"].str .contains (O0OO0O0000OOO0O00 [1 ],na =False ))&(OOOOO000O0O00O0OO ["关键字查找列o"].str .contains (O0OO0O0000OOO0O00 [2 ],na =False ))&(OOOOO000O0O00O0OO ["关键字查找列o"].str .contains (O0OO0O0000OOO0O00 [3 ],na =False ))&(OOOOO000O0O00O0OO ["关键字查找列o"].str .contains (O0OO0O0000OOO0O00 [4 ],na =False )),OO000000O0O0OO0O0 ["赋值列名"]]=OO000000O0O0OO0O0 ["赋值"]#line:1982
			return OOOOO000O0O00O0OO #line:1983
def TOOL_guizheng (O00000O0000000O0O ,OO0000OOOOOOO0O00 ,O0O0OOO00OOO0O00O ):#line:1986
	""#line:1987
	if OO0000OOOOOOO0O00 ==0 :#line:1988
		OOO0OOO0000OOOOOO =pd .read_excel (filedialog .askopenfilename (filetypes =[("XLSX",".xlsx")]),sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:1989
		OOO0OOO0000OOOOOO =OOO0OOO0000OOOOOO [(OOO0OOO0000OOOOOO ["执行标记"]=="是")].reset_index ()#line:1990
		for O0O0OO0O00OOO0000 ,OOOO0OO0O00OO000O in OOO0OOO0000OOOOOO .iterrows ():#line:1991
			O00000O0000000O0O =TOOLS_add_c (O00000O0000000O0O ,OOOO0OO0O00OO000O )#line:1992
		del O00000O0000000O0O ["关键字查找列o"]#line:1993
	elif OO0000OOOOOOO0O00 ==1 :#line:1995
		OOO0OOO0000OOOOOO =pd .read_excel (peizhidir +"0（范例）数据规整.xlsx",sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:1996
		OOO0OOO0000OOOOOO =OOO0OOO0000OOOOOO [(OOO0OOO0000OOOOOO ["执行标记"]=="是")].reset_index ()#line:1997
		for O0O0OO0O00OOO0000 ,OOOO0OO0O00OO000O in OOO0OOO0000OOOOOO .iterrows ():#line:1998
			O00000O0000000O0O =TOOLS_add_c (O00000O0000000O0O ,OOOO0OO0O00OO000O )#line:1999
		del O00000O0000000O0O ["关键字查找列o"]#line:2000
	elif OO0000OOOOOOO0O00 =="课题":#line:2002
		OOO0OOO0000OOOOOO =pd .read_excel (peizhidir +"0（范例）品类规整.xlsx",sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:2003
		OOO0OOO0000OOOOOO =OOO0OOO0000OOOOOO [(OOO0OOO0000OOOOOO ["执行标记"]=="是")].reset_index ()#line:2004
		for O0O0OO0O00OOO0000 ,OOOO0OO0O00OO000O in OOO0OOO0000OOOOOO .iterrows ():#line:2005
			O00000O0000000O0O =TOOLS_add_c (O00000O0000000O0O ,OOOO0OO0O00OO000O )#line:2006
		del O00000O0000000O0O ["关键字查找列o"]#line:2007
	elif OO0000OOOOOOO0O00 ==2 :#line:2009
		text .insert (END ,"\n开展报告单位和监测机构名称规整...")#line:2010
		O00000OO00O0000OO =pd .read_excel (peizhidir +"0（范例）上报单位.xls",sheet_name ="报告单位",header =0 ,index_col =0 ,).fillna ("没有定义好X").reset_index ()#line:2011
		O00O0OOO0OOO00O00 =pd .read_excel (peizhidir +"0（范例）上报单位.xls",sheet_name ="监测机构",header =0 ,index_col =0 ,).fillna ("没有定义好X").reset_index ()#line:2012
		O000OOOOOOO0O0000 =pd .read_excel (peizhidir +"0（范例）上报单位.xls",sheet_name ="地市清单",header =0 ,index_col =0 ,).fillna ("没有定义好X").reset_index ()#line:2013
		for O0O0OO0O00OOO0000 ,OOOO0OO0O00OO000O in O00000OO00O0000OO .iterrows ():#line:2014
			O00000O0000000O0O .loc [(O00000O0000000O0O ["单位名称"]==OOOO0OO0O00OO000O ["曾用名1"]),"单位名称"]=OOOO0OO0O00OO000O ["单位名称"]#line:2015
			O00000O0000000O0O .loc [(O00000O0000000O0O ["单位名称"]==OOOO0OO0O00OO000O ["曾用名2"]),"单位名称"]=OOOO0OO0O00OO000O ["单位名称"]#line:2016
			O00000O0000000O0O .loc [(O00000O0000000O0O ["单位名称"]==OOOO0OO0O00OO000O ["曾用名3"]),"单位名称"]=OOOO0OO0O00OO000O ["单位名称"]#line:2017
			O00000O0000000O0O .loc [(O00000O0000000O0O ["单位名称"]==OOOO0OO0O00OO000O ["曾用名4"]),"单位名称"]=OOOO0OO0O00OO000O ["单位名称"]#line:2018
			O00000O0000000O0O .loc [(O00000O0000000O0O ["单位名称"]==OOOO0OO0O00OO000O ["曾用名5"]),"单位名称"]=OOOO0OO0O00OO000O ["单位名称"]#line:2019
			O00000O0000000O0O .loc [(O00000O0000000O0O ["单位名称"]==OOOO0OO0O00OO000O ["单位名称"]),"医疗机构类别"]=OOOO0OO0O00OO000O ["医疗机构类别"]#line:2021
			O00000O0000000O0O .loc [(O00000O0000000O0O ["单位名称"]==OOOO0OO0O00OO000O ["单位名称"]),"监测机构"]=OOOO0OO0O00OO000O ["监测机构"]#line:2022
		for O0O0OO0O00OOO0000 ,OOOO0OO0O00OO000O in O00O0OOO0OOO00O00 .iterrows ():#line:2024
			O00000O0000000O0O .loc [(O00000O0000000O0O ["监测机构"]==OOOO0OO0O00OO000O ["曾用名1"]),"监测机构"]=OOOO0OO0O00OO000O ["监测机构"]#line:2025
			O00000O0000000O0O .loc [(O00000O0000000O0O ["监测机构"]==OOOO0OO0O00OO000O ["曾用名2"]),"监测机构"]=OOOO0OO0O00OO000O ["监测机构"]#line:2026
			O00000O0000000O0O .loc [(O00000O0000000O0O ["监测机构"]==OOOO0OO0O00OO000O ["曾用名3"]),"监测机构"]=OOOO0OO0O00OO000O ["监测机构"]#line:2027
		for O00O00O00O00000O0 in O000OOOOOOO0O0000 ["地市列表"]:#line:2029
			O00000O0000000O0O .loc [(O00000O0000000O0O ["上报单位所属地区"].str .contains (O00O00O00O00000O0 ,na =False )),"市级监测机构"]=O00O00O00O00000O0 #line:2030
		O00000O0000000O0O .loc [(O00000O0000000O0O ["上报单位所属地区"].str .contains ("顺德",na =False )),"市级监测机构"]="佛山"#line:2033
		O00000O0000000O0O ["市级监测机构"]=O00000O0000000O0O ["市级监测机构"].fillna ("-未规整的-")#line:2034
	elif OO0000OOOOOOO0O00 ==3 :#line:2036
			O00OO0OOO0OOOOOOO =(O00000O0000000O0O .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"]).aggregate ({"报告编码":"count"}).reset_index ())#line:2041
			O00OO0OOO0OOOOOOO =O00OO0OOO0OOOOOOO .sort_values (by =["注册证编号/曾用注册证编号","报告编码"],ascending =[False ,False ],na_position ="last").reset_index ()#line:2044
			text .insert (END ,"\n开展产品名称规整..")#line:2045
			del O00OO0OOO0OOOOOOO ["报告编码"]#line:2046
			O00OO0OOO0OOOOOOO =O00OO0OOO0OOOOOOO .drop_duplicates (["注册证编号/曾用注册证编号"])#line:2047
			O00000O0000000O0O =O00000O0000000O0O .rename (columns ={"上市许可持有人名称":"上市许可持有人名称（规整前）","产品类别":"产品类别（规整前）","产品名称":"产品名称（规整前）"})#line:2049
			O00000O0000000O0O =pd .merge (O00000O0000000O0O ,O00OO0OOO0OOOOOOO ,on =["注册证编号/曾用注册证编号"],how ="left")#line:2050
	elif OO0000OOOOOOO0O00 ==4 :#line:2052
		text .insert (END ,"\n正在开展化妆品注册单位规整...")#line:2053
		O00O0OOO0OOO00O00 =pd .read_excel (peizhidir +"0（范例）注册单位.xlsx",sheet_name ="机构列表",header =0 ,index_col =0 ,).reset_index ()#line:2054
		for O0O0OO0O00OOO0000 ,OOOO0OO0O00OO000O in O00O0OOO0OOO00O00 .iterrows ():#line:2056
			O00000O0000000O0O .loc [(O00000O0000000O0O ["单位名称"]==OOOO0OO0O00OO000O ["中文全称"]),"监测机构"]=OOOO0OO0O00OO000O ["归属地区"]#line:2057
			O00000O0000000O0O .loc [(O00000O0000000O0O ["单位名称"]==OOOO0OO0O00OO000O ["中文全称"]),"市级监测机构"]=OOOO0OO0O00OO000O ["地市"]#line:2058
		O00000O0000000O0O ["监测机构"]=O00000O0000000O0O ["监测机构"].fillna ("未规整")#line:2059
		O00000O0000000O0O ["市级监测机构"]=O00000O0000000O0O ["市级监测机构"].fillna ("未规整")#line:2060
	if O0O0OOO00OOO0O00O ==True :#line:2061
		return O00000O0000000O0O #line:2062
	else :#line:2063
		TABLE_tree_Level_2 (O00000O0000000O0O ,0 ,O00000O0000000O0O )#line:2064
def TOOL_person (O0OO0O0O00O00O0O0 ):#line:2066
	""#line:2067
	OOO00OOO0O000OOO0 =pd .read_excel (peizhidir +"0（范例）注册单位.xlsx",sheet_name ="专家列表",header =0 ,index_col =0 ,).reset_index ()#line:2068
	for O0OOOOO0OO00OOO0O ,OOO0O0OOOOO0O0O0O in OOO00OOO0O000OOO0 .iterrows ():#line:2069
		O0OO0O0O00O00O0O0 .loc [(O0OO0O0O00O00O0O0 ["市级监测机构"]==OOO0O0OOOOO0O0O0O ["市级监测机构"]),"评表人员"]=OOO0O0OOOOO0O0O0O ["评表人员"]#line:2070
		O0OO0O0O00O00O0O0 ["评表人员"]=O0OO0O0O00O00O0O0 ["评表人员"].fillna ("未规整")#line:2071
		OO0O0000OO00000OO =O0OO0O0O00O00O0O0 .groupby (["评表人员"]).agg (报告数量 =("报告编码","nunique"),地市 =("市级监测机构",STAT_countx ),).sort_values (by ="报告数量",ascending =[False ],na_position ="last").reset_index ()#line:2075
	TABLE_tree_Level_2 (OO0O0000OO00000OO ,0 ,OO0O0000OO00000OO )#line:2076
def TOOLS_get_list (OOO0OOOOO0O0O00O0 ):#line:2078
    ""#line:2079
    OOO0OOOOO0O0O00O0 =str (OOO0OOOOO0O0O00O0 )#line:2080
    OO000OOOOO0OO00OO =[]#line:2081
    OO000OOOOO0OO00OO .append (OOO0OOOOO0O0O00O0 )#line:2082
    OO000OOOOO0OO00OO =",".join (OO000OOOOO0OO00OO )#line:2083
    OO000OOOOO0OO00OO =OO000OOOOO0OO00OO .split ("|")#line:2084
    O0O0O000O0O00O0OO =OO000OOOOO0OO00OO [:]#line:2085
    OO000OOOOO0OO00OO =list (set (OO000OOOOO0OO00OO ))#line:2086
    OO000OOOOO0OO00OO .sort (key =O0O0O000O0O00O0OO .index )#line:2087
    return OO000OOOOO0OO00OO #line:2088
def TOOLS_get_list0 (OO0000O0O00000OOO ,OOOOO00O0000OOO00 ,*OO000O000000O00O0 ):#line:2090
    ""#line:2091
    OO0000O0O00000OOO =str (OO0000O0O00000OOO )#line:2092
    if pd .notnull (OO0000O0O00000OOO ):#line:2094
        try :#line:2095
            if "use("in str (OO0000O0O00000OOO ):#line:2096
                OOOO0000OOOOO0O0O =OO0000O0O00000OOO #line:2097
                OO00O0O0OOO0O0OO0 =re .compile (r"[(](.*?)[)]",re .S )#line:2098
                O0O0O0OOO0OOO0000 =re .findall (OO00O0O0OOO0O0OO0 ,OOOO0000OOOOO0O0O )#line:2099
                OOOOOO00OOO0OOOOO =[]#line:2100
                if ").list"in OO0000O0O00000OOO :#line:2101
                    O0000O00O0OO00O00 =peizhidir +""+str (O0O0O0OOO0OOO0000 [0 ])+".xls"#line:2102
                    O00O0OO0O0OO0OO00 =pd .read_excel (O0000O00O0OO00O00 ,sheet_name =O0O0O0OOO0OOO0000 [0 ],header =0 ,index_col =0 ).reset_index ()#line:2105
                    O00O0OO0O0OO0OO00 ["检索关键字"]=O00O0OO0O0OO0OO00 ["检索关键字"].astype (str )#line:2106
                    OOOOOO00OOO0OOOOO =O00O0OO0O0OO0OO00 ["检索关键字"].tolist ()+OOOOOO00OOO0OOOOO #line:2107
                if ").file"in OO0000O0O00000OOO :#line:2108
                    OOOOOO00OOO0OOOOO =OOOOO00O0000OOO00 [O0O0O0OOO0OOO0000 [0 ]].astype (str ).tolist ()+OOOOOO00OOO0OOOOO #line:2110
                try :#line:2113
                    if "报告类型-新的"in OOOOO00O0000OOO00 .columns :#line:2114
                        OOOOOO00OOO0OOOOO =",".join (OOOOOO00OOO0OOOOO )#line:2115
                        OOOOOO00OOO0OOOOO =OOOOOO00OOO0OOOOO .split (";")#line:2116
                        OOOOOO00OOO0OOOOO =",".join (OOOOOO00OOO0OOOOO )#line:2117
                        OOOOOO00OOO0OOOOO =OOOOOO00OOO0OOOOO .split ("；")#line:2118
                        OOOOOO00OOO0OOOOO =[OOO00OO0O00OO0000 .replace ("（严重）","")for OOO00OO0O00OO0000 in OOOOOO00OOO0OOOOO ]#line:2119
                        OOOOOO00OOO0OOOOO =[O0OOOOO0O0OO0O000 .replace ("（一般）","")for O0OOOOO0O0OO0O000 in OOOOOO00OOO0OOOOO ]#line:2120
                except :#line:2121
                    pass #line:2122
                OOOOOO00OOO0OOOOO =",".join (OOOOOO00OOO0OOOOO )#line:2124
                OOOOOO00OOO0OOOOO =OOOOOO00OOO0OOOOO .split ("┋")#line:2125
                OOOOOO00OOO0OOOOO =",".join (OOOOOO00OOO0OOOOO )#line:2126
                OOOOOO00OOO0OOOOO =OOOOOO00OOO0OOOOO .split (";")#line:2127
                OOOOOO00OOO0OOOOO =",".join (OOOOOO00OOO0OOOOO )#line:2128
                OOOOOO00OOO0OOOOO =OOOOOO00OOO0OOOOO .split ("；")#line:2129
                OOOOOO00OOO0OOOOO =",".join (OOOOOO00OOO0OOOOO )#line:2130
                OOOOOO00OOO0OOOOO =OOOOOO00OOO0OOOOO .split ("、")#line:2131
                OOOOOO00OOO0OOOOO =",".join (OOOOOO00OOO0OOOOO )#line:2132
                OOOOOO00OOO0OOOOO =OOOOOO00OOO0OOOOO .split ("，")#line:2133
                OOOOOO00OOO0OOOOO =",".join (OOOOOO00OOO0OOOOO )#line:2134
                OOOOOO00OOO0OOOOO =OOOOOO00OOO0OOOOO .split (",")#line:2135
                OOOOO00OOO00OOOOO =OOOOOO00OOO0OOOOO [:]#line:2138
                try :#line:2139
                    if OO000O000000O00O0 [0 ]==1000 :#line:2140
                      pass #line:2141
                except :#line:2142
                      OOOOOO00OOO0OOOOO =list (set (OOOOOO00OOO0OOOOO ))#line:2143
                OOOOOO00OOO0OOOOO .sort (key =OOOOO00OOO00OOOOO .index )#line:2144
            else :#line:2146
                OO0000O0O00000OOO =str (OO0000O0O00000OOO )#line:2147
                OOOOOO00OOO0OOOOO =[]#line:2148
                OOOOOO00OOO0OOOOO .append (OO0000O0O00000OOO )#line:2149
                OOOOOO00OOO0OOOOO =",".join (OOOOOO00OOO0OOOOO )#line:2150
                OOOOOO00OOO0OOOOO =OOOOOO00OOO0OOOOO .split ("┋")#line:2151
                OOOOOO00OOO0OOOOO =",".join (OOOOOO00OOO0OOOOO )#line:2152
                OOOOOO00OOO0OOOOO =OOOOOO00OOO0OOOOO .split ("、")#line:2153
                OOOOOO00OOO0OOOOO =",".join (OOOOOO00OOO0OOOOO )#line:2154
                OOOOOO00OOO0OOOOO =OOOOOO00OOO0OOOOO .split ("，")#line:2155
                OOOOOO00OOO0OOOOO =",".join (OOOOOO00OOO0OOOOO )#line:2156
                OOOOOO00OOO0OOOOO =OOOOOO00OOO0OOOOO .split (",")#line:2157
                OOOOO00OOO00OOOOO =OOOOOO00OOO0OOOOO [:]#line:2159
                try :#line:2160
                    if OO000O000000O00O0 [0 ]==1000 :#line:2161
                      OOOOOO00OOO0OOOOO =list (set (OOOOOO00OOO0OOOOO ))#line:2162
                except :#line:2163
                      pass #line:2164
                OOOOOO00OOO0OOOOO .sort (key =OOOOO00OOO00OOOOO .index )#line:2165
                OOOOOO00OOO0OOOOO .sort (key =OOOOO00OOO00OOOOO .index )#line:2166
        except ValueError2 :#line:2168
            showinfo (title ="提示信息",message ="创建单元格支持多个甚至表单（文件）传入的方法，返回一个经过整理的清单出错，任务终止。")#line:2169
            return False #line:2170
    return OOOOOO00OOO0OOOOO #line:2172
def TOOLS_easyread2 (O0OOOOO0OOO0O0O0O ):#line:2174
    ""#line:2175
    O0OOOOO0OOO0O0O0O ["分隔符"]="●"#line:2177
    O0OOOOO0OOO0O0O0O ["上报机构描述"]=(O0OOOOO0OOO0O0O0O ["使用过程"].astype ("str")+O0OOOOO0OOO0O0O0O ["分隔符"]+O0OOOOO0OOO0O0O0O ["事件原因分析"].astype ("str")+O0OOOOO0OOO0O0O0O ["分隔符"]+O0OOOOO0OOO0O0O0O ["事件原因分析描述"].astype ("str")+O0OOOOO0OOO0O0O0O ["分隔符"]+O0OOOOO0OOO0O0O0O ["初步处置情况"].astype ("str"))#line:2186
    O0OOOOO0OOO0O0O0O ["持有人处理描述"]=(O0OOOOO0OOO0O0O0O ["关联性评价"].astype ("str")+O0OOOOO0OOO0O0O0O ["分隔符"]+O0OOOOO0OOO0O0O0O ["调查情况"].astype ("str")+O0OOOOO0OOO0O0O0O ["分隔符"]+O0OOOOO0OOO0O0O0O ["事件原因分析"].astype ("str")+O0OOOOO0OOO0O0O0O ["分隔符"]+O0OOOOO0OOO0O0O0O ["具体控制措施"].astype ("str")+O0OOOOO0OOO0O0O0O ["分隔符"]+O0OOOOO0OOO0O0O0O ["未采取控制措施原因"].astype ("str"))#line:2197
    OO000OOO000OO0OO0 =O0OOOOO0OOO0O0O0O [["报告编码","事件发生日期","报告日期","单位名称","产品名称","注册证编号/曾用注册证编号","产品批号","型号","规格","上市许可持有人名称","管理类别","伤害","伤害表现","器械故障表现","上报机构描述","持有人处理描述","经营企业使用单位报告状态","监测机构","产品类别","医疗机构类别","年龄","年龄类型","性别"]]#line:2224
    OO000OOO000OO0OO0 =OO000OOO000OO0OO0 .sort_values (by =["事件发生日期"],ascending =[False ],na_position ="last",)#line:2229
    OO000OOO000OO0OO0 =OO000OOO000OO0OO0 .rename (columns ={"报告编码":"规整编码"})#line:2230
    return OO000OOO000OO0OO0 #line:2231
def fenci0 (O00OO00O0O0OOO0O0 ):#line:2234
	""#line:2235
	O0OO00000O0OOO000 =Toplevel ()#line:2236
	O0OO00000O0OOO000 .title ('词频统计')#line:2237
	O000OOO00OO000O00 =O0OO00000O0OOO000 .winfo_screenwidth ()#line:2238
	OO0O00000O00O0OOO =O0OO00000O0OOO000 .winfo_screenheight ()#line:2240
	O0O0O0OO0000OO0O0 =400 #line:2242
	OO000O00OOOO00OOO =120 #line:2243
	OO00OO00OOOO000OO =(O000OOO00OO000O00 -O0O0O0OO0000OO0O0 )/2 #line:2245
	O00OO00O000O0000O =(OO0O00000O00O0OOO -OO000O00OOOO00OOO )/2 #line:2246
	O0OO00000O0OOO000 .geometry ("%dx%d+%d+%d"%(O0O0O0OO0000OO0O0 ,OO000O00OOOO00OOO ,OO00OO00OOOO000OO ,O00OO00O000O0000O ))#line:2247
	O0OO0000OOOOOO00O =Label (O0OO00000O0OOO000 ,text ="配置文件：")#line:2248
	O0OO0000OOOOOO00O .pack ()#line:2249
	O0000O0O000OO00OO =Label (O0OO00000O0OOO000 ,text ="需要分词的列：")#line:2250
	O0O0O00OO0O00OO0O =Entry (O0OO00000O0OOO000 ,width =80 )#line:2252
	O0O0O00OO0O00OO0O .insert (0 ,peizhidir +"0（范例）中文分词工作文件.xls")#line:2253
	O00OOOO0OO0O0O000 =Entry (O0OO00000O0OOO000 ,width =80 )#line:2254
	O00OOOO0OO0O0O000 .insert (0 ,"器械故障表现，伤害表现")#line:2255
	O0O0O00OO0O00OO0O .pack ()#line:2256
	O0000O0O000OO00OO .pack ()#line:2257
	O00OOOO0OO0O0O000 .pack ()#line:2258
	O00O000000O0OOO00 =LabelFrame (O0OO00000O0OOO000 )#line:2259
	O0OOO0000O0O0O0OO =Button (O00O000000O0OOO00 ,text ="确定",width =10 ,command =lambda :PROGRAM_thread_it (tree_Level_2 ,fenci (O0O0O00OO0O00OO0O .get (),O00OOOO0OO0O0O000 .get (),O00OO00O0O0OOO0O0 ),1 ,0 ))#line:2260
	O0OOO0000O0O0O0OO .pack (side =LEFT ,padx =1 ,pady =1 )#line:2261
	O00O000000O0OOO00 .pack ()#line:2262
def fenci (O0O0OO00OOO00OOOO ,OO0OOO00OOOO0O000 ,OOOOOOO0O000OOO00 ):#line:2264
    ""#line:2265
    import glob #line:2266
    import jieba #line:2267
    import random #line:2268
    try :#line:2270
        OOOOOOO0O000OOO00 =OOOOOOO0O000OOO00 .drop_duplicates (["报告编码"])#line:2271
    except :#line:2272
        pass #line:2273
    def OOO000OO00O00OO0O (O0O000OO0OO0OO0O0 ,OOO0O00O0O0000O0O ):#line:2274
        OO00O0O0O00000000 ={}#line:2275
        for OO000O000O000OOO0 in O0O000OO0OO0OO0O0 :#line:2276
            OO00O0O0O00000000 [OO000O000O000OOO0 ]=OO00O0O0O00000000 .get (OO000O000O000OOO0 ,0 )+1 #line:2277
        return sorted (OO00O0O0O00000000 .items (),key =lambda O0O000OO0O00000O0 :O0O000OO0O00000O0 [1 ],reverse =True )[:OOO0O00O0O0000O0O ]#line:2278
    O000OO00O0OO00O0O =pd .read_excel (O0O0OO00OOO00OOOO ,sheet_name ="初始化",header =0 ,index_col =0 ).reset_index ()#line:2282
    OOOO0OO00O0O00OO0 =O000OO00O0OO00O0O .iloc [0 ,2 ]#line:2284
    O00O00O0OOO0OO0OO =pd .read_excel (O0O0OO00OOO00OOOO ,sheet_name ="停用词",header =0 ,index_col =0 ).reset_index ()#line:2287
    O00O00O0OOO0OO0OO ["停用词"]=O00O00O0OOO0OO0OO ["停用词"].astype (str )#line:2289
    OOO00000000O0O000 =[OO0000O0OO0O0OOOO .strip ()for OO0000O0OO0O0OOOO in O00O00O0OOO0OO0OO ["停用词"]]#line:2290
    O00OO0000OO00O0OO =pd .read_excel (O0O0OO00OOO00OOOO ,sheet_name ="本地词库",header =0 ,index_col =0 ).reset_index ()#line:2293
    OOOOO000000O00O0O =O00OO0000OO00O0OO ["本地词库"]#line:2294
    jieba .load_userdict (OOOOO000000O00O0O )#line:2295
    O0O00O0OO000O000O =""#line:2298
    O0OOO0OOOO0OOOO00 =get_list0 (OO0OOO00OOOO0O000 ,OOOOOOO0O000OOO00 )#line:2301
    try :#line:2302
        for O0000O00OO00O0O00 in O0OOO0OOOO0OOOO00 :#line:2303
            for OOO0000OO00O000OO in OOOOOOO0O000OOO00 [O0000O00OO00O0O00 ]:#line:2304
                O0O00O0OO000O000O =O0O00O0OO000O000O +str (OOO0000OO00O000OO )#line:2305
    except :#line:2306
        text .insert (END ,"分词配置文件未正确设置，将对整个表格进行分词。")#line:2307
        for O0000O00OO00O0O00 in OOOOOOO0O000OOO00 .columns .tolist ():#line:2308
            for OOO0000OO00O000OO in OOOOOOO0O000OOO00 [O0000O00OO00O0O00 ]:#line:2309
                O0O00O0OO000O000O =O0O00O0OO000O000O +str (OOO0000OO00O000OO )#line:2310
    O0OO0OOOOOOO0O0O0 =[]#line:2311
    O0OO0OOOOOOO0O0O0 =O0OO0OOOOOOO0O0O0 +[O000O0O00OOOOOOOO for O000O0O00OOOOOOOO in jieba .cut (O0O00O0OO000O000O )if O000O0O00OOOOOOOO not in OOO00000000O0O000 ]#line:2312
    OOOOOOO0O000O0OO0 =dict (OOO000OO00O00OO0O (O0OO0OOOOOOO0O0O0 ,OOOO0OO00O0O00OO0 ))#line:2313
    O00OOO0OOOO0OOOOO =pd .DataFrame ([OOOOOOO0O000O0OO0 ]).T #line:2314
    O00OOO0OOOO0OOOOO =O00OOO0OOOO0OOOOO .reset_index ()#line:2315
    return O00OOO0OOOO0OOOOO #line:2316
def TOOLS_time (O0OO0OOO000O0O0O0 ,O000O0O0O0O0O00O0 ,O000OOOO0OO00OO00 ):#line:2318
	""#line:2319
	O0OO0O0O00OOOOO00 =O0OO0OOO000O0O0O0 .drop_duplicates (["报告编码"]).groupby ([O000O0O0O0O0O00O0 ]).agg (报告总数 =("报告编码","nunique"),严重伤害数 =("伤害",lambda O000O00OO00OO0000 :STAT_countpx (O000O00OO00OO0000 .values ,"严重伤害")),死亡数量 =("伤害",lambda O00OO0000O0OOO00O :STAT_countpx (O00OO0000O0OOO00O .values ,"死亡")),).sort_values (by =O000O0O0O0O0O00O0 ,ascending =[True ],na_position ="last").reset_index ()#line:2324
	O0OO0O0O00OOOOO00 =O0OO0O0O00OOOOO00 .set_index (O000O0O0O0O0O00O0 )#line:2328
	O0OO0O0O00OOOOO00 =O0OO0O0O00OOOOO00 .resample ('D').asfreq (fill_value =0 )#line:2330
	O0OO0O0O00OOOOO00 ["time"]=O0OO0O0O00OOOOO00 .index .values #line:2332
	O0OO0O0O00OOOOO00 ["time"]=pd .to_datetime (O0OO0O0O00OOOOO00 ["time"],format ="%Y/%m/%d").dt .date #line:2333
	if O000OOOO0OO00OO00 ==1 :#line:2335
		return O0OO0O0O00OOOOO00 .reset_index (drop =True )#line:2337
	O0OO0O0O00OOOOO00 ["30天累计数"]=O0OO0O0O00OOOOO00 ["报告总数"].rolling (30 ,min_periods =1 ).agg (lambda OOOO000O0O0000O0O :sum (OOOO000O0O0000O0O )).astype (int )#line:2339
	O0OO0O0O00OOOOO00 ["30天严重伤害累计数"]=O0OO0O0O00OOOOO00 ["严重伤害数"].rolling (30 ,min_periods =1 ).agg (lambda O0O0OOOO0O0O000O0 :sum (O0O0OOOO0O0O000O0 )).astype (int )#line:2340
	O0OO0O0O00OOOOO00 ["30天死亡累计数"]=O0OO0O0O00OOOOO00 ["死亡数量"].rolling (30 ,min_periods =1 ).agg (lambda OOOO0O000O0OOOO00 :sum (OOOO0O000O0OOOO00 )).astype (int )#line:2341
	O0OO0O0O00OOOOO00 .loc [(((O0OO0O0O00OOOOO00 ["30天累计数"]>=3 )&(O0OO0O0O00OOOOO00 ["30天严重伤害累计数"]>=1 ))|(O0OO0O0O00OOOOO00 ["30天累计数"]>=5 )|(O0OO0O0O00OOOOO00 ["30天死亡累计数"]>=1 )),"关注区域"]=O0OO0O0O00OOOOO00 ["30天累计数"]#line:2362
	DRAW_make_risk_plot (O0OO0O0O00OOOOO00 ,"time",["30天累计数","30天严重伤害累计数","关注区域"],"折线图",999 )#line:2367
def TOOLS_keti (OOOOOO000OO00OO00 ):#line:2371
	""#line:2372
	import datetime #line:2373
	def O0OO0O000O0O00000 (OOOO0OOOOOO00OO00 ,OO0000OOOO00OOOOO ):#line:2375
		if ini ["模式"]=="药品":#line:2376
			OOOOO0OO0OOOO0O0O =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="药品").reset_index (drop =True )#line:2377
		if ini ["模式"]=="器械":#line:2378
			OOOOO0OO0OOOO0O0O =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="器械").reset_index (drop =True )#line:2379
		if ini ["模式"]=="化妆品":#line:2380
			OOOOO0OO0OOOO0O0O =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="化妆品").reset_index (drop =True )#line:2381
		O0OO00000OOOO0OOO =OOOOO0OO0OOOO0O0O ["权重"][0 ]#line:2382
		OO0O0O00O00O0OO00 =OOOOO0OO0OOOO0O0O ["权重"][1 ]#line:2383
		OOO00OO0O000OO00O =OOOOO0OO0OOOO0O0O ["权重"][2 ]#line:2384
		O0OO0OOOO0OO0O0O0 =OOOOO0OO0OOOO0O0O ["权重"][3 ]#line:2385
		O0O0O0O00O0OOOO0O =OOOOO0OO0OOOO0O0O ["值"][3 ]#line:2386
		OO000OOO0OO0OO0OO =OOOOO0OO0OOOO0O0O ["权重"][4 ]#line:2388
		OO0O00O00OO000OOO =OOOOO0OO0OOOO0O0O ["值"][4 ]#line:2389
		OO00OOOO0O0O00O00 =OOOOO0OO0OOOO0O0O ["权重"][5 ]#line:2391
		O00O0O0O00OOO0000 =OOOOO0OO0OOOO0O0O ["值"][5 ]#line:2392
		OOO0O00OOO00OOOO0 =OOOOO0OO0OOOO0O0O ["权重"][6 ]#line:2394
		OOOOOO00OO0000000 =OOOOO0OO0OOOO0O0O ["值"][6 ]#line:2395
		O0000OOOO00O000O0 =pd .to_datetime (OOOO0OOOOOO00OO00 )#line:2397
		O00O0OOO0O0OOOO00 =OO0000OOOO00OOOOO .copy ().set_index ('报告日期')#line:2398
		O00O0OOO0O0OOOO00 =O00O0OOO0O0OOOO00 .sort_index ()#line:2399
		if ini ["模式"]=="器械":#line:2400
			O00O0OOO0O0OOOO00 ["关键字查找列"]=O00O0OOO0O0OOOO00 ["器械故障表现"].astype (str )+O00O0OOO0O0OOOO00 ["伤害表现"].astype (str )+O00O0OOO0O0OOOO00 ["使用过程"].astype (str )+O00O0OOO0O0OOOO00 ["事件原因分析描述"].astype (str )+O00O0OOO0O0OOOO00 ["初步处置情况"].astype (str )#line:2401
		else :#line:2402
			O00O0OOO0O0OOOO00 ["关键字查找列"]=O00O0OOO0O0OOOO00 ["器械故障表现"].astype (str )#line:2403
		O00O0OOO0O0OOOO00 .loc [O00O0OOO0O0OOOO00 ["关键字查找列"].str .contains (O0O0O0O00O0OOOO0O ,na =False ),"高度关注关键字"]=1 #line:2404
		O00O0OOO0O0OOOO00 .loc [O00O0OOO0O0OOOO00 ["关键字查找列"].str .contains (OO0O00O00OO000OOO ,na =False ),"二级敏感词"]=1 #line:2405
		O00O0OOO0O0OOOO00 .loc [O00O0OOO0O0OOOO00 ["关键字查找列"].str .contains (O00O0O0O00OOO0000 ,na =False ),"减分项"]=1 #line:2406
		O00O0OO00OO000O0O =O00O0OOO0O0OOOO00 .loc [O0000OOOO00O000O0 -pd .Timedelta (days =30 ):O0000OOOO00O000O0 ].reset_index ()#line:2408
		O0000000O0OO0O0O0 =O00O0OOO0O0OOOO00 .loc [O0000OOOO00O000O0 -pd .Timedelta (days =365 ):O0000OOOO00O000O0 ].reset_index ()#line:2409
		OOO00O000O0O0OOOO =O00O0OO00OO000O0O .groupby (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"]).agg (证号计数 =("报告编码","nunique"),批号个数 =("产品批号","nunique"),批号列表 =("产品批号",STAT_countx ),型号个数 =("型号","nunique"),型号列表 =("型号",STAT_countx ),规格个数 =("规格","nunique"),规格列表 =("规格",STAT_countx ),).sort_values (by ="证号计数",ascending =[False ],na_position ="last").reset_index ()#line:2422
		O0O0OO0O0OOOOOO0O =O00O0OO00OO000O0O .drop_duplicates (["报告编码"]).groupby (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"]).agg (严重伤害数 =("伤害",lambda O0OOOOO0O0OO0000O :STAT_countpx (O0OOOOO0O0OO0000O .values ,"严重伤害")),死亡数量 =("伤害",lambda OO00OOO000O00O0O0 :STAT_countpx (OO00OOO000O00O0O0 .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),待评价数 =("持有人报告状态",lambda OOOOOO0000OOO0OOO :STAT_countpx (OOOOOO0000OOO0OOO .values ,"待评价")),严重伤害待评价数 =("伤害与评价",lambda O0O00OOOOO0OO000O :STAT_countpx (O0O00OOOOO0OO000O .values ,"严重伤害待评价")),高度关注关键字 =("高度关注关键字","sum"),二级敏感词 =("二级敏感词","sum"),减分项 =("减分项","sum"),).reset_index ()#line:2434
		OOO0O00O0OOO0O0OO =pd .merge (OOO00O000O0O0OOOO ,O0O0OO0O0OOOOOO0O ,on =["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"],how ="left")#line:2436
		O0O0OO0O000OOOOO0 =O00O0OO00OO000O0O .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","型号"]).agg (型号计数 =("报告编码","nunique"),).sort_values (by ="型号计数",ascending =[False ],na_position ="last").reset_index ()#line:2443
		O0O0OO0O000OOOOO0 =O0O0OO0O000OOOOO0 .drop_duplicates ("注册证编号/曾用注册证编号")#line:2444
		O00O0O0OO00O00OOO =O00O0OO00OO000O0O .drop_duplicates (["报告编码"]).groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","产品批号"]).agg (批号计数 =("报告编码","nunique"),严重伤害数 =("伤害",lambda O0O000OO0O0O0O0OO :STAT_countpx (O0O000OO0O0O0O0OO .values ,"严重伤害")),).sort_values (by ="批号计数",ascending =[False ],na_position ="last").reset_index ()#line:2449
		O00O0O0OO00O00OOO ["风险评分-影响"]=0 #line:2453
		O00O0O0OO00O00OOO ["评分说明"]=""#line:2454
		O00O0O0OO00O00OOO .loc [((O00O0O0OO00O00OOO ["批号计数"]>=3 )&(O00O0O0OO00O00OOO ["严重伤害数"]>=1 )&(O00O0O0OO00O00OOO ["产品类别"]!="有源"))|((O00O0O0OO00O00OOO ["批号计数"]>=5 )&(O00O0O0OO00O00OOO ["产品类别"]!="有源")),"风险评分-影响"]=O00O0O0OO00O00OOO ["风险评分-影响"]+3 #line:2455
		O00O0O0OO00O00OOO .loc [(O00O0O0OO00O00OOO ["风险评分-影响"]>=3 ),"评分说明"]=O00O0O0OO00O00OOO ["评分说明"]+"●符合省中心无源规则+3;"#line:2456
		O00O0O0OO00O00OOO =O00O0O0OO00O00OOO .sort_values (by ="风险评分-影响",ascending =[False ],na_position ="last").reset_index (drop =True )#line:2460
		O00O0O0OO00O00OOO =O00O0O0OO00O00OOO .drop_duplicates ("注册证编号/曾用注册证编号")#line:2461
		O0O0OO0O000OOOOO0 =O0O0OO0O000OOOOO0 [["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","型号","型号计数"]]#line:2462
		O00O0O0OO00O00OOO =O00O0O0OO00O00OOO [["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","产品批号","批号计数","风险评分-影响","评分说明"]]#line:2463
		OOO0O00O0OOO0O0OO =pd .merge (OOO0O00O0OOO0O0OO ,O0O0OO0O000OOOOO0 ,on =["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"],how ="left")#line:2464
		OOO0O00O0OOO0O0OO =pd .merge (OOO0O00O0OOO0O0OO ,O00O0O0OO00O00OOO ,on =["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"],how ="left")#line:2466
		OOO0O00O0OOO0O0OO .loc [((OOO0O00O0OOO0O0OO ["证号计数"]>=3 )&(OOO0O00O0OOO0O0OO ["严重伤害数"]>=1 )&(OOO0O00O0OOO0O0OO ["产品类别"]=="有源"))|((OOO0O00O0OOO0O0OO ["证号计数"]>=5 )&(OOO0O00O0OOO0O0OO ["产品类别"]=="有源")),"风险评分-影响"]=OOO0O00O0OOO0O0OO ["风险评分-影响"]+3 #line:2470
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["风险评分-影响"]>=3 )&(OOO0O00O0OOO0O0OO ["产品类别"]=="有源"),"评分说明"]=OOO0O00O0OOO0O0OO ["评分说明"]+"●符合省中心有源规则+3;"#line:2471
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["死亡数量"]>=1 ),"风险评分-影响"]=OOO0O00O0OOO0O0OO ["风险评分-影响"]+10 #line:2476
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["风险评分-影响"]>=10 ),"评分说明"]=OOO0O00O0OOO0O0OO ["评分说明"]+"存在死亡报告;"#line:2477
		O0OO0O0OOOO0O0OO0 =round (O0OO00000OOOO0OOO *(OOO0O00O0OOO0O0OO ["严重伤害数"]/OOO0O00O0OOO0O0OO ["证号计数"]),2 )#line:2480
		OOO0O00O0OOO0O0OO ["风险评分-影响"]=OOO0O00O0OOO0O0OO ["风险评分-影响"]+O0OO0O0OOOO0O0OO0 #line:2481
		OOO0O00O0OOO0O0OO ["评分说明"]=OOO0O00O0OOO0O0OO ["评分说明"]+"严重比评分"+O0OO0O0OOOO0O0OO0 .astype (str )+";"#line:2482
		OO000O0O0O0OO0O00 =round (OO0O0O00O00O0OO00 *(np .log (OOO0O00O0OOO0O0OO ["单位个数"])),2 )#line:2485
		OOO0O00O0OOO0O0OO ["风险评分-影响"]=OOO0O00O0OOO0O0OO ["风险评分-影响"]+OO000O0O0O0OO0O00 #line:2486
		OOO0O00O0OOO0O0OO ["评分说明"]=OOO0O00O0OOO0O0OO ["评分说明"]+"报告单位评分"+OO000O0O0O0OO0O00 .astype (str )+";"#line:2487
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["产品类别"]=="有源")&(OOO0O00O0OOO0O0OO ["证号计数"]>=3 ),"风险评分-影响"]=OOO0O00O0OOO0O0OO ["风险评分-影响"]+OOO00OO0O000OO00O *OOO0O00O0OOO0O0OO ["型号计数"]/OOO0O00O0OOO0O0OO ["证号计数"]#line:2490
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["产品类别"]=="有源")&(OOO0O00O0OOO0O0OO ["证号计数"]>=3 ),"评分说明"]=OOO0O00O0OOO0O0OO ["评分说明"]+"型号集中度评分"+(round (OOO00OO0O000OO00O *OOO0O00O0OOO0O0OO ["型号计数"]/OOO0O00O0OOO0O0OO ["证号计数"],2 )).astype (str )+";"#line:2491
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["产品类别"]!="有源")&(OOO0O00O0OOO0O0OO ["证号计数"]>=3 ),"风险评分-影响"]=OOO0O00O0OOO0O0OO ["风险评分-影响"]+OOO00OO0O000OO00O *OOO0O00O0OOO0O0OO ["批号计数"]/OOO0O00O0OOO0O0OO ["证号计数"]#line:2492
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["产品类别"]!="有源")&(OOO0O00O0OOO0O0OO ["证号计数"]>=3 ),"评分说明"]=OOO0O00O0OOO0O0OO ["评分说明"]+"批号集中度评分"+(round (OOO00OO0O000OO00O *OOO0O00O0OOO0O0OO ["批号计数"]/OOO0O00O0OOO0O0OO ["证号计数"],2 )).astype (str )+";"#line:2493
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["高度关注关键字"]>=1 ),"风险评分-影响"]=OOO0O00O0OOO0O0OO ["风险评分-影响"]+O0OO0OOOO0OO0O0O0 #line:2496
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["高度关注关键字"]>=1 ),"评分说明"]=OOO0O00O0OOO0O0OO ["评分说明"]+"●含有高度关注关键字评分"+str (O0OO0OOOO0OO0O0O0 )+"；"#line:2497
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["二级敏感词"]>=1 ),"风险评分-影响"]=OOO0O00O0OOO0O0OO ["风险评分-影响"]+OO000OOO0OO0OO0OO #line:2500
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["二级敏感词"]>=1 ),"评分说明"]=OOO0O00O0OOO0O0OO ["评分说明"]+"含有二级敏感词评分"+str (OO000OOO0OO0OO0OO )+"；"#line:2501
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["减分项"]>=1 ),"风险评分-影响"]=OOO0O00O0OOO0O0OO ["风险评分-影响"]+OO00OOOO0O0O00O00 #line:2504
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["减分项"]>=1 ),"评分说明"]=OOO0O00O0OOO0O0OO ["评分说明"]+"减分项评分"+str (OO00OOOO0O0O00O00 )+"；"#line:2505
		O0OO0000000000O0O =Countall (O0000000O0OO0O0O0 ).df_findrisk ("事件发生月份")#line:2508
		O0OO0000000000O0O =O0OO0000000000O0O .drop_duplicates ("注册证编号/曾用注册证编号")#line:2509
		O0OO0000000000O0O =O0OO0000000000O0O [["注册证编号/曾用注册证编号","均值","标准差","CI上限"]]#line:2510
		OOO0O00O0OOO0O0OO =pd .merge (OOO0O00O0OOO0O0OO ,O0OO0000000000O0O ,on =["注册证编号/曾用注册证编号"],how ="left")#line:2511
		OOO0O00O0OOO0O0OO ["风险评分-月份"]=1 #line:2513
		OOO0O00O0OOO0O0OO ["mfc"]=""#line:2514
		OOO0O00O0OOO0O0OO .loc [((OOO0O00O0OOO0O0OO ["证号计数"]>OOO0O00O0OOO0O0OO ["均值"])&(OOO0O00O0OOO0O0OO ["标准差"].astype (str )=="nan")),"风险评分-月份"]=OOO0O00O0OOO0O0OO ["风险评分-月份"]+1 #line:2515
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["证号计数"]>OOO0O00O0OOO0O0OO ["均值"]),"mfc"]="月份计数超过历史均值"+OOO0O00O0OOO0O0OO ["均值"].astype (str )+"；"#line:2516
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["证号计数"]>=(OOO0O00O0OOO0O0OO ["均值"]+OOO0O00O0OOO0O0OO ["标准差"]))&(OOO0O00O0OOO0O0OO ["证号计数"]>=3 ),"风险评分-月份"]=OOO0O00O0OOO0O0OO ["风险评分-月份"]+1 #line:2518
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["证号计数"]>=(OOO0O00O0OOO0O0OO ["均值"]+OOO0O00O0OOO0O0OO ["标准差"]))&(OOO0O00O0OOO0O0OO ["证号计数"]>=3 ),"mfc"]="月份计数超过3例超过历史均值一个标准差("+OOO0O00O0OOO0O0OO ["标准差"].astype (str )+")；"#line:2519
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["证号计数"]>=OOO0O00O0OOO0O0OO ["CI上限"])&(OOO0O00O0OOO0O0OO ["证号计数"]>=3 ),"风险评分-月份"]=OOO0O00O0OOO0O0OO ["风险评分-月份"]+2 #line:2521
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["证号计数"]>=OOO0O00O0OOO0O0OO ["CI上限"])&(OOO0O00O0OOO0O0OO ["证号计数"]>=3 ),"mfc"]="月份计数超过3例且超过历史95%CI上限("+OOO0O00O0OOO0O0OO ["CI上限"].astype (str )+")；"#line:2522
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["证号计数"]>=OOO0O00O0OOO0O0OO ["CI上限"])&(OOO0O00O0OOO0O0OO ["证号计数"]>=5 ),"风险评分-月份"]=OOO0O00O0OOO0O0OO ["风险评分-月份"]+1 #line:2524
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["证号计数"]>=OOO0O00O0OOO0O0OO ["CI上限"])&(OOO0O00O0OOO0O0OO ["证号计数"]>=5 ),"mfc"]="月份计数超过5例且超过历史95%CI上限("+OOO0O00O0OOO0O0OO ["CI上限"].astype (str )+")；"#line:2525
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["证号计数"]>=OOO0O00O0OOO0O0OO ["CI上限"])&(OOO0O00O0OOO0O0OO ["证号计数"]>=7 ),"风险评分-月份"]=OOO0O00O0OOO0O0OO ["风险评分-月份"]+1 #line:2527
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["证号计数"]>=OOO0O00O0OOO0O0OO ["CI上限"])&(OOO0O00O0OOO0O0OO ["证号计数"]>=7 ),"mfc"]="月份计数超过7例且超过历史95%CI上限("+OOO0O00O0OOO0O0OO ["CI上限"].astype (str )+")；"#line:2528
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["证号计数"]>=OOO0O00O0OOO0O0OO ["CI上限"])&(OOO0O00O0OOO0O0OO ["证号计数"]>=9 ),"风险评分-月份"]=OOO0O00O0OOO0O0OO ["风险评分-月份"]+1 #line:2530
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["证号计数"]>=OOO0O00O0OOO0O0OO ["CI上限"])&(OOO0O00O0OOO0O0OO ["证号计数"]>=9 ),"mfc"]="月份计数超过9例且超过历史95%CI上限("+OOO0O00O0OOO0O0OO ["CI上限"].astype (str )+")；"#line:2531
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["证号计数"]>=3 )&(OOO0O00O0OOO0O0OO ["标准差"].astype (str )=="nan"),"风险评分-月份"]=3 #line:2535
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["证号计数"]>=3 )&(OOO0O00O0OOO0O0OO ["标准差"].astype (str )=="nan"),"mfc"]="无历史数据但数量超过3例；"#line:2536
		OOO0O00O0OOO0O0OO ["评分说明"]=OOO0O00O0OOO0O0OO ["评分说明"]+"●●证号数量："+OOO0O00O0OOO0O0OO ["证号计数"].astype (str )+";"+OOO0O00O0OOO0O0OO ["mfc"]#line:2539
		del OOO0O00O0OOO0O0OO ["mfc"]#line:2540
		OOO0O00O0OOO0O0OO =OOO0O00O0OOO0O0OO .rename (columns ={"均值":"月份均值","标准差":"月份标准差","CI上限":"月份CI上限"})#line:2541
		O0OO0000000000O0O =Countall (O0000000O0OO0O0O0 ).df_findrisk ("产品批号")#line:2545
		O0OO0000000000O0O =O0OO0000000000O0O .drop_duplicates ("注册证编号/曾用注册证编号")#line:2546
		O0OO0000000000O0O =O0OO0000000000O0O [["注册证编号/曾用注册证编号","均值","标准差","CI上限"]]#line:2547
		OOO0O00O0OOO0O0OO =pd .merge (OOO0O00O0OOO0O0OO ,O0OO0000000000O0O ,on =["注册证编号/曾用注册证编号"],how ="left")#line:2548
		OOO0O00O0OOO0O0OO ["风险评分-批号"]=1 #line:2550
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["产品类别"]!="有源"),"评分说明"]=OOO0O00O0OOO0O0OO ["评分说明"]+"●●高峰批号数量："+OOO0O00O0OOO0O0OO ["批号计数"].astype (str )+";"#line:2551
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["批号计数"]>OOO0O00O0OOO0O0OO ["均值"]),"风险评分-批号"]=OOO0O00O0OOO0O0OO ["风险评分-批号"]+1 #line:2553
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["批号计数"]>OOO0O00O0OOO0O0OO ["均值"]),"评分说明"]=OOO0O00O0OOO0O0OO ["评分说明"]+"高峰批号计数超过历史均值"+OOO0O00O0OOO0O0OO ["均值"].astype (str )+"；"#line:2554
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["批号计数"]>(OOO0O00O0OOO0O0OO ["均值"]+OOO0O00O0OOO0O0OO ["标准差"]))&(OOO0O00O0OOO0O0OO ["批号计数"]>=3 ),"风险评分-批号"]=OOO0O00O0OOO0O0OO ["风险评分-批号"]+1 #line:2555
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["批号计数"]>(OOO0O00O0OOO0O0OO ["均值"]+OOO0O00O0OOO0O0OO ["标准差"]))&(OOO0O00O0OOO0O0OO ["批号计数"]>=3 ),"评分说明"]=OOO0O00O0OOO0O0OO ["评分说明"]+"高峰批号计数超过3例超过历史均值一个标准差("+OOO0O00O0OOO0O0OO ["标准差"].astype (str )+")；"#line:2556
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["批号计数"]>OOO0O00O0OOO0O0OO ["CI上限"])&(OOO0O00O0OOO0O0OO ["批号计数"]>=3 ),"风险评分-批号"]=OOO0O00O0OOO0O0OO ["风险评分-批号"]+1 #line:2557
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["批号计数"]>OOO0O00O0OOO0O0OO ["CI上限"])&(OOO0O00O0OOO0O0OO ["批号计数"]>=3 ),"评分说明"]=OOO0O00O0OOO0O0OO ["评分说明"]+"高峰批号计数超过3例且超过历史95%CI上限("+OOO0O00O0OOO0O0OO ["CI上限"].astype (str )+")；"#line:2558
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["批号计数"]>=3 )&(OOO0O00O0OOO0O0OO ["标准差"].astype (str )=="nan"),"风险评分-月份"]=3 #line:2560
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["批号计数"]>=3 )&(OOO0O00O0OOO0O0OO ["标准差"].astype (str )=="nan"),"评分说明"]=OOO0O00O0OOO0O0OO ["评分说明"]+"无历史数据但数量超过3例；"#line:2561
		OOO0O00O0OOO0O0OO =OOO0O00O0OOO0O0OO .rename (columns ={"均值":"高峰批号均值","标准差":"高峰批号标准差","CI上限":"高峰批号CI上限"})#line:2562
		OOO0O00O0OOO0O0OO ["风险评分-影响"]=round (OOO0O00O0OOO0O0OO ["风险评分-影响"],2 )#line:2565
		OOO0O00O0OOO0O0OO ["风险评分-月份"]=round (OOO0O00O0OOO0O0OO ["风险评分-月份"],2 )#line:2566
		OOO0O00O0OOO0O0OO ["风险评分-批号"]=round (OOO0O00O0OOO0O0OO ["风险评分-批号"],2 )#line:2567
		OOO0O00O0OOO0O0OO ["总体评分"]=OOO0O00O0OOO0O0OO ["风险评分-影响"].copy ()#line:2569
		OOO0O00O0OOO0O0OO ["关注建议"]=""#line:2570
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["风险评分-影响"]>=3 ),"关注建议"]=OOO0O00O0OOO0O0OO ["关注建议"]+"●建议关注(影响范围)；"#line:2571
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["风险评分-月份"]>=3 ),"关注建议"]=OOO0O00O0OOO0O0OO ["关注建议"]+"●建议关注(当月数量异常)；"#line:2572
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["风险评分-批号"]>=3 ),"关注建议"]=OOO0O00O0OOO0O0OO ["关注建议"]+"●建议关注(高峰批号数量异常)。"#line:2573
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["风险评分-月份"]>=OOO0O00O0OOO0O0OO ["风险评分-批号"]),"总体评分"]=OOO0O00O0OOO0O0OO ["风险评分-影响"]*OOO0O00O0OOO0O0OO ["风险评分-月份"]#line:2577
		OOO0O00O0OOO0O0OO .loc [(OOO0O00O0OOO0O0OO ["风险评分-月份"]<OOO0O00O0OOO0O0OO ["风险评分-批号"]),"总体评分"]=OOO0O00O0OOO0O0OO ["风险评分-影响"]*OOO0O00O0OOO0O0OO ["风险评分-批号"]#line:2578
		OOO0O00O0OOO0O0OO ["总体评分"]=round (OOO0O00O0OOO0O0OO ["总体评分"],2 )#line:2580
		OOO0O00O0OOO0O0OO ["评分说明"]=OOO0O00O0OOO0O0OO ["关注建议"]+OOO0O00O0OOO0O0OO ["评分说明"]#line:2581
		OOO0O00O0OOO0O0OO =OOO0O00O0OOO0O0OO .sort_values (by =["总体评分","风险评分-影响"],ascending =[False ,False ],na_position ="last").reset_index (drop =True )#line:2582
		OOO0O00O0OOO0O0OO ["主要故障分类"]=""#line:2585
		for OO00OOO0O00OO0000 ,OOO000O0O0000OO0O in OOO0O00O0OOO0O0OO .iterrows ():#line:2586
			O0O0O0OOO0000O000 =O00O0OO00OO000O0O [(O00O0OO00OO000O0O ["注册证编号/曾用注册证编号"]==OOO000O0O0000OO0O ["注册证编号/曾用注册证编号"])].copy ()#line:2587
			if OOO000O0O0000OO0O ["总体评分"]>=float (OOO0O00OOO00OOOO0 ):#line:2588
				if OOO000O0O0000OO0O ["规整后品类"]!="N":#line:2589
					OOOO00OOOOO000000 =Countall (O0O0O0OOO0000O000 ).df_psur ("特定品种",OOO000O0O0000OO0O ["规整后品类"])#line:2590
				elif OOO000O0O0000OO0O ["产品类别"]=="无源":#line:2591
					OOOO00OOOOO000000 =Countall (O0O0O0OOO0000O000 ).df_psur ("通用无源")#line:2592
				elif OOO000O0O0000OO0O ["产品类别"]=="有源":#line:2593
					OOOO00OOOOO000000 =Countall (O0O0O0OOO0000O000 ).df_psur ("通用有源")#line:2594
				elif OOO000O0O0000OO0O ["产品类别"]=="体外诊断试剂":#line:2595
					OOOO00OOOOO000000 =Countall (O0O0O0OOO0000O000 ).df_psur ("体外诊断试剂")#line:2596
				OOO00000000O0O00O =OOOO00OOOOO000000 [["事件分类","总数量"]].copy ()#line:2598
				OOOO0O0OOO0OOO0O0 =""#line:2599
				for O0O0O00OOO00O0000 ,OOOOO00OO000OO00O in OOO00000000O0O00O .iterrows ():#line:2600
					OOOO0O0OOO0OOO0O0 =OOOO0O0OOO0OOO0O0 +str (OOOOO00OO000OO00O ["事件分类"])+":"+str (OOOOO00OO000OO00O ["总数量"])+";"#line:2601
				OOO0O00O0OOO0O0OO .loc [OO00OOO0O00OO0000 ,"主要故障分类"]=OOOO0O0OOO0OOO0O0 #line:2602
			else :#line:2603
				break #line:2604
		OOO0O00O0OOO0O0OO =OOO0O00O0OOO0O0OO [["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","证号计数","严重伤害数","死亡数量","总体评分","风险评分-影响","风险评分-月份","风险评分-批号","主要故障分类","评分说明","单位个数","单位列表","批号个数","批号列表","型号个数","型号列表","规格个数","规格列表","待评价数","严重伤害待评价数","高度关注关键字","二级敏感词","月份均值","月份标准差","月份CI上限","高峰批号均值","高峰批号标准差","高峰批号CI上限","型号","型号计数","产品批号","批号计数"]]#line:2608
		OOO0O00O0OOO0O0OO ["报表类型"]="dfx_zhenghao"#line:2609
		TABLE_tree_Level_2 (OOO0O00O0OOO0O0OO ,1 ,O00O0OO00OO000O0O ,O0000000O0OO0O0O0 )#line:2610
		pass #line:2611
	OOO00O00OO0OOOOO0 =Toplevel ()#line:2614
	OOO00O00OO0OOOOO0 .title ('风险预警')#line:2615
	OO0OO0O0OOOOOOOO0 =OOO00O00OO0OOOOO0 .winfo_screenwidth ()#line:2616
	O0O0O00O0000000O0 =OOO00O00OO0OOOOO0 .winfo_screenheight ()#line:2618
	O0O00O00OOO00OO0O =350 #line:2620
	OO0OO000O00OOOOO0 =35 #line:2621
	OO0OOOO000O0O0O00 =(OO0OO0O0OOOOOOOO0 -O0O00O00OOO00OO0O )/2 #line:2623
	OO00O0O0O0OOO0O0O =(O0O0O00O0000000O0 -OO0OO000O00OOOOO0 )/2 #line:2624
	OOO00O00OO0OOOOO0 .geometry ("%dx%d+%d+%d"%(O0O00O00OOO00OO0O ,OO0OO000O00OOOOO0 ,OO0OOOO000O0O0O00 ,OO00O0O0O0OOO0O0O ))#line:2625
	O0O000OOO00O00O0O =Label (OOO00O00OO0OOOOO0 ,text ="预警日期：")#line:2627
	O0O000OOO00O00O0O .grid (row =1 ,column =0 ,sticky ="w")#line:2628
	O0O0O0O0OOOO0000O =Entry (OOO00O00OO0OOOOO0 ,width =30 )#line:2629
	O0O0O0O0OOOO0000O .insert (0 ,datetime .date .today ())#line:2630
	O0O0O0O0OOOO0000O .grid (row =1 ,column =1 ,sticky ="w")#line:2631
	OO0O0OO0OOOOO000O =Button (OOO00O00OO0OOOOO0 ,text ="确定",width =10 ,command =lambda :TABLE_tree_Level_2 (O0OO0O000O0O00000 (O0O0O0O0OOOO0000O .get (),OOOOOO000OO00OO00 ),1 ,OOOOOO000OO00OO00 ))#line:2635
	OO0O0OO0OOOOO000O .grid (row =1 ,column =3 ,sticky ="w")#line:2636
	pass #line:2638
def TOOLS_count_elements (O0OOO000OO000O000 ,OOOOO00O0O00O0OOO ,OO000OO00000O000O ):#line:2640
    ""#line:2641
    OO00O0OO00O000O00 =pd .DataFrame (columns =[OO000OO00000O000O ,'count'])#line:2643
    OOOO0OOO00OO0O0OO =[]#line:2644
    OOOOOO000O0O0000O =[]#line:2645
    for O000OOOO0000O0O00 in TOOLS_get_list (OOOOO00O0O00O0OOO ):#line:2648
        OO00OO0O0OOO0000O =O0OOO000OO000O000 [O0OOO000OO000O000 [OO000OO00000O000O ].str .contains (O000OOOO0000O0O00 )].shape [0 ]#line:2650
        if OO00OO0O0OOO0000O >0 :#line:2653
            OOOO0OOO00OO0O0OO .append (OO00OO0O0OOO0000O )#line:2654
            OOOOOO000O0O0000O .append (O000OOOO0000O0O00 )#line:2655
    OO0OOO0OOOO00O000 =pd .DataFrame ({"index":OOOOOO000O0O0000O ,'计数':OOOO0OOO00OO0O0OO })#line:2656
    OO0OOO0OOOO00O000 ["构成比(%)"]=round (100 *OO0OOO0OOOO00O000 ["计数"]/OO0OOO0OOOO00O000 ["计数"].sum (),2 )#line:2657
    OO0OOO0OOOO00O000 ["报表类型"]="dfx_deepvie2"+"_"+str ([OO000OO00000O000O ])#line:2658
    return OO0OOO0OOOO00O000 #line:2660
def TOOLS_autocount (O0O0000O0000OO000 ,OO0OO0OOO0000OO0O ):#line:2662
    ""#line:2663
    O0000O0O0O0OO0OO0 =pd .read_excel (peizhidir +"0（范例）上报单位.xls",sheet_name ="监测机构",header =0 ,index_col =0 ).reset_index ()#line:2666
    O00O0OOO0O0O000OO =pd .read_excel (peizhidir +"0（范例）上报单位.xls",sheet_name ="报告单位",header =0 ,index_col =0 ).reset_index ()#line:2669
    OOOOO0OO00O00O000 =O00O0OOO0O0O000OO [(O00O0OOO0O0O000OO ["是否属于二级以上医疗机构"]=="是")]#line:2670
    if OO0OO0OOO0000OO0O =="药品":#line:2673
        O0O0000O0000OO000 =O0O0000O0000OO000 .reset_index (drop =True )#line:2674
        if "再次使用可疑药是否出现同样反应"not in O0O0000O0000OO000 .columns :#line:2675
            showinfo (title ="错误信息",message ="导入的疑似不是药品报告表。")#line:2676
            return 0 #line:2677
        O0O0OOOO0O0O00OO0 =Countall (O0O0000O0000OO000 ).df_org ("监测机构")#line:2679
        O0O0OOOO0O0O00OO0 =pd .merge (O0O0OOOO0O0O00OO0 ,O0000O0O0O0OO0OO0 ,on ="监测机构",how ="left")#line:2680
        O0O0OOOO0O0O00OO0 =O0O0OOOO0O0O00OO0 [["监测机构序号","监测机构","药品数量指标","报告数量","审核通过数","新严比","严重比","超时比"]].sort_values (by =["监测机构序号"],ascending =True ,na_position ="last").fillna (0 )#line:2681
        O0OO0O000OO0OOOOO =["药品数量指标","审核通过数","报告数量"]#line:2682
        O0O0OOOO0O0O00OO0 [O0OO0O000OO0OOOOO ]=O0O0OOOO0O0O00OO0 [O0OO0O000OO0OOOOO ].apply (lambda O0OOOOOO0OOO0OOOO :O0OOOOOO0OOO0OOOO .astype (int ))#line:2683
        OO0OOO0OOOOO0OO00 =Countall (O0O0000O0000OO000 ).df_user ()#line:2685
        OO0OOO0OOOOO0OO00 =pd .merge (OO0OOO0OOOOO0OO00 ,O00O0OOO0O0O000OO ,on =["监测机构","单位名称"],how ="left")#line:2686
        OO0OOO0OOOOO0OO00 =pd .merge (OO0OOO0OOOOO0OO00 ,O0000O0O0O0OO0OO0 [["监测机构序号","监测机构"]],on ="监测机构",how ="left")#line:2687
        OO0OOO0OOOOO0OO00 =OO0OOO0OOOOO0OO00 [["监测机构序号","监测机构","单位名称","药品数量指标","报告数量","审核通过数","新严比","严重比","超时比"]].sort_values (by =["监测机构序号","报告数量"],ascending =[True ,False ],na_position ="last").fillna (0 )#line:2689
        O0OO0O000OO0OOOOO =["药品数量指标","审核通过数","报告数量"]#line:2690
        OO0OOO0OOOOO0OO00 [O0OO0O000OO0OOOOO ]=OO0OOO0OOOOO0OO00 [O0OO0O000OO0OOOOO ].apply (lambda O0OOO0O000OOO0000 :O0OOO0O000OOO0000 .astype (int ))#line:2691
        OO0O00000OOO00O0O =pd .merge (OOOOO0OO00O00O000 ,OO0OOO0OOOOO0OO00 ,on =["监测机构","单位名称"],how ="left").sort_values (by =["监测机构"],ascending =True ,na_position ="last").fillna (0 )#line:2693
        OO0O00000OOO00O0O =OO0O00000OOO00O0O [(OO0O00000OOO00O0O ["审核通过数"]<1 )]#line:2694
        OO0O00000OOO00O0O =OO0O00000OOO00O0O [["监测机构","单位名称","报告数量","审核通过数","严重比","超时比"]]#line:2695
    if OO0OO0OOO0000OO0O =="器械":#line:2697
        O0O0000O0000OO000 =O0O0000O0000OO000 .reset_index (drop =True )#line:2698
        if "产品编号"not in O0O0000O0000OO000 .columns :#line:2699
            showinfo (title ="错误信息",message ="导入的疑似不是器械报告表。")#line:2700
            return 0 #line:2701
        O0O0OOOO0O0O00OO0 =Countall (O0O0000O0000OO000 ).df_org ("监测机构")#line:2703
        O0O0OOOO0O0O00OO0 =pd .merge (O0O0OOOO0O0O00OO0 ,O0000O0O0O0OO0OO0 ,on ="监测机构",how ="left")#line:2704
        O0O0OOOO0O0O00OO0 =O0O0OOOO0O0O00OO0 [["监测机构序号","监测机构","器械数量指标","报告数量","审核通过数","严重比","超时比"]].sort_values (by =["监测机构序号"],ascending =True ,na_position ="last").fillna (0 )#line:2705
        O0OO0O000OO0OOOOO =["器械数量指标","审核通过数","报告数量"]#line:2706
        O0O0OOOO0O0O00OO0 [O0OO0O000OO0OOOOO ]=O0O0OOOO0O0O00OO0 [O0OO0O000OO0OOOOO ].apply (lambda OO0O0O0O00OOOOO00 :OO0O0O0O00OOOOO00 .astype (int ))#line:2707
        OO0OOO0OOOOO0OO00 =Countall (O0O0000O0000OO000 ).df_user ()#line:2709
        OO0OOO0OOOOO0OO00 =pd .merge (OO0OOO0OOOOO0OO00 ,O00O0OOO0O0O000OO ,on =["监测机构","单位名称"],how ="left")#line:2710
        OO0OOO0OOOOO0OO00 =pd .merge (OO0OOO0OOOOO0OO00 ,O0000O0O0O0OO0OO0 [["监测机构序号","监测机构"]],on ="监测机构",how ="left")#line:2711
        OO0OOO0OOOOO0OO00 =OO0OOO0OOOOO0OO00 [["监测机构序号","监测机构","单位名称","器械数量指标","报告数量","审核通过数","严重比","超时比"]].sort_values (by =["监测机构序号","报告数量"],ascending =[True ,False ],na_position ="last").fillna (0 )#line:2713
        O0OO0O000OO0OOOOO =["器械数量指标","审核通过数","报告数量"]#line:2714
        OO0OOO0OOOOO0OO00 [O0OO0O000OO0OOOOO ]=OO0OOO0OOOOO0OO00 [O0OO0O000OO0OOOOO ].apply (lambda O0O0OO0OOO0O0OO0O :O0O0OO0OOO0O0OO0O .astype (int ))#line:2716
        OO0O00000OOO00O0O =pd .merge (OOOOO0OO00O00O000 ,OO0OOO0OOOOO0OO00 ,on =["监测机构","单位名称"],how ="left").sort_values (by =["监测机构"],ascending =True ,na_position ="last").fillna (0 )#line:2718
        OO0O00000OOO00O0O =OO0O00000OOO00O0O [(OO0O00000OOO00O0O ["审核通过数"]<1 )]#line:2719
        OO0O00000OOO00O0O =OO0O00000OOO00O0O [["监测机构","单位名称","报告数量","审核通过数","严重比","超时比"]]#line:2720
    if OO0OO0OOO0000OO0O =="化妆品":#line:2723
        O0O0000O0000OO000 =O0O0000O0000OO000 .reset_index (drop =True )#line:2724
        if "初步判断"not in O0O0000O0000OO000 .columns :#line:2725
            showinfo (title ="错误信息",message ="导入的疑似不是化妆品报告表。")#line:2726
            return 0 #line:2727
        O0O0OOOO0O0O00OO0 =Countall (O0O0000O0000OO000 ).df_org ("监测机构")#line:2729
        O0O0OOOO0O0O00OO0 =pd .merge (O0O0OOOO0O0O00OO0 ,O0000O0O0O0OO0OO0 ,on ="监测机构",how ="left")#line:2730
        O0O0OOOO0O0O00OO0 =O0O0OOOO0O0O00OO0 [["监测机构序号","监测机构","化妆品数量指标","报告数量","审核通过数"]].sort_values (by =["监测机构序号"],ascending =True ,na_position ="last").fillna (0 )#line:2731
        O0OO0O000OO0OOOOO =["化妆品数量指标","审核通过数","报告数量"]#line:2732
        O0O0OOOO0O0O00OO0 [O0OO0O000OO0OOOOO ]=O0O0OOOO0O0O00OO0 [O0OO0O000OO0OOOOO ].apply (lambda OO000O00O000O0OOO :OO000O00O000O0OOO .astype (int ))#line:2733
        OO0OOO0OOOOO0OO00 =Countall (O0O0000O0000OO000 ).df_user ()#line:2735
        OO0OOO0OOOOO0OO00 =pd .merge (OO0OOO0OOOOO0OO00 ,O00O0OOO0O0O000OO ,on =["监测机构","单位名称"],how ="left")#line:2736
        OO0OOO0OOOOO0OO00 =pd .merge (OO0OOO0OOOOO0OO00 ,O0000O0O0O0OO0OO0 [["监测机构序号","监测机构"]],on ="监测机构",how ="left")#line:2737
        OO0OOO0OOOOO0OO00 =OO0OOO0OOOOO0OO00 [["监测机构序号","监测机构","单位名称","化妆品数量指标","报告数量","审核通过数"]].sort_values (by =["监测机构序号","报告数量"],ascending =[True ,False ],na_position ="last").fillna (0 )#line:2738
        O0OO0O000OO0OOOOO =["化妆品数量指标","审核通过数","报告数量"]#line:2739
        OO0OOO0OOOOO0OO00 [O0OO0O000OO0OOOOO ]=OO0OOO0OOOOO0OO00 [O0OO0O000OO0OOOOO ].apply (lambda OO0O0OO0O0OO00O00 :OO0O0OO0O0OO00O00 .astype (int ))#line:2740
        OO0O00000OOO00O0O =pd .merge (OOOOO0OO00O00O000 ,OO0OOO0OOOOO0OO00 ,on =["监测机构","单位名称"],how ="left").sort_values (by =["监测机构"],ascending =True ,na_position ="last").fillna (0 )#line:2742
        OO0O00000OOO00O0O =OO0O00000OOO00O0O [(OO0O00000OOO00O0O ["审核通过数"]<1 )]#line:2743
        OO0O00000OOO00O0O =OO0O00000OOO00O0O [["监测机构","单位名称","报告数量","审核通过数"]]#line:2744
    O0O00OO0OOOO0000O =filedialog .asksaveasfilename (title =u"保存文件",initialfile =OO0OO0OOO0000OO0O ,defaultextension ="xls",filetypes =[("Excel 97-2003 工作簿","*.xls")],)#line:2751
    O000O0OO0OO00O0O0 =pd .ExcelWriter (O0O00OO0OOOO0000O ,engine ="xlsxwriter")#line:2752
    O0O0OOOO0O0O00OO0 .to_excel (O000O0OO0OO00O0O0 ,sheet_name ="监测机构")#line:2753
    OO0OOO0OOOOO0OO00 .to_excel (O000O0OO0OO00O0O0 ,sheet_name ="上报单位")#line:2754
    OO0O00000OOO00O0O .to_excel (O000O0OO0OO00O0O0 ,sheet_name ="未上报的二级以上医疗机构")#line:2755
    O000O0OO0OO00O0O0 .close ()#line:2756
    showinfo (title ="提示",message ="文件写入成功。")#line:2757
def TOOLS_web_view (OOOOO000O0O0O0O00 ):#line:2759
    ""#line:2760
    import pybi as pbi #line:2761
    OOO00OO0000O00O0O =pd .ExcelWriter ("temp_webview.xls")#line:2762
    OOOOO000O0O0O0O00 .to_excel (OOO00OO0000O00O0O ,sheet_name ="temp_webview")#line:2763
    OOO00OO0000O00O0O .close ()#line:2764
    OOOOO000O0O0O0O00 =pd .read_excel ("temp_webview.xls",header =0 ,sheet_name =0 ).reset_index (drop =True )#line:2765
    O000O00O00OOOO0O0 =pbi .set_source (OOOOO000O0O0O0O00 )#line:2766
    with pbi .flowBox ():#line:2767
        for OO00OO00000OOOO0O in OOOOO000O0O0O0O00 .columns :#line:2768
            pbi .add_slicer (O000O00O00OOOO0O0 [OO00OO00000OOOO0O ])#line:2769
    pbi .add_table (O000O00O00OOOO0O0 )#line:2770
    O0OOOOO000O0O0O0O ="temp_webview.html"#line:2771
    pbi .to_html (O0OOOOO000O0O0O0O )#line:2772
    webbrowser .open_new_tab (O0OOOOO000O0O0O0O )#line:2773
def TOOLS_Autotable_0 (OO000O0OOO000O000 ,O0O0OO000O0000000 ,*OO00000O000OOOO0O ):#line:2778
    ""#line:2779
    OO00O0O0OO00OO000 =[OO00000O000OOOO0O [0 ],OO00000O000OOOO0O [1 ],OO00000O000OOOO0O [2 ]]#line:2781
    O000O000000OO0O0O =list (set ([OOO0OO00OOO00O000 for OOO0OO00OOO00O000 in OO00O0O0OO00OO000 if OOO0OO00OOO00O000 !='']))#line:2783
    O000O000000OO0O0O .sort (key =OO00O0O0OO00OO000 .index )#line:2784
    if len (O000O000000OO0O0O )==0 :#line:2785
        showinfo (title ="提示信息",message ="分组项请选择至少一列。")#line:2786
        return 0 #line:2787
    OO0OOO000OO0OO0OO =[OO00000O000OOOO0O [3 ],OO00000O000OOOO0O [4 ]]#line:2788
    if (OO00000O000OOOO0O [3 ]==""or OO00000O000OOOO0O [4 ]=="")and O0O0OO000O0000000 in ["数据透视","分组统计"]:#line:2789
        if "报告编码"in OO000O0OOO000O000 .columns :#line:2790
            OO0OOO000OO0OO0OO [0 ]="报告编码"#line:2791
            OO0OOO000OO0OO0OO [1 ]="nunique"#line:2792
            text .insert (END ,"值项未配置,将使用报告编码进行唯一值计数。")#line:2793
        else :#line:2794
            showinfo (title ="提示信息",message ="值项未配置。")#line:2795
            return 0 #line:2796
    if OO00000O000OOOO0O [4 ]=="计数":#line:2798
        OO0OOO000OO0OO0OO [1 ]="count"#line:2799
    elif OO00000O000OOOO0O [4 ]=="求和":#line:2800
        OO0OOO000OO0OO0OO [1 ]="sum"#line:2801
    elif OO00000O000OOOO0O [4 ]=="唯一值计数":#line:2802
        OO0OOO000OO0OO0OO [1 ]="nunique"#line:2803
    if O0O0OO000O0000000 =="分组统计":#line:2806
        TABLE_tree_Level_2 (TOOLS_deep_view (OO000O0OOO000O000 ,O000O000000OO0O0O ,OO0OOO000OO0OO0OO ,0 ),1 ,OO000O0OOO000O000 )#line:2807
    if O0O0OO000O0000000 =="数据透视":#line:2809
        TABLE_tree_Level_2 (TOOLS_deep_view (OO000O0OOO000O000 ,O000O000000OO0O0O ,OO0OOO000OO0OO0OO ,1 ),1 ,OO000O0OOO000O000 )#line:2810
    if O0O0OO000O0000000 =="描述性统计":#line:2812
        TABLE_tree_Level_2 (OO000O0OOO000O000 [O000O000000OO0O0O ].describe ().reset_index (),1 ,OO000O0OOO000O000 )#line:2813
    if O0O0OO000O0000000 =="单列多项拆分统计(统计列)":#line:2816
        TABLE_tree_Level_2 (STAT_pinzhong (OO000O0OOO000O000 ,OO00000O000OOOO0O [0 ],0 ))#line:2817
    if O0O0OO000O0000000 =="单列多项拆分统计(透视列-统计列)":#line:2818
        TABLE_tree_Level_2 (Countall (OO000O0OOO000O000 ).df_psur2 (OO00000O000OOOO0O [0 ],OO00000O000OOOO0O [1 ]),1 ,0 )#line:2819
    if O0O0OO000O0000000 =="单列多项拆分统计(透视列-统计列-字典)":#line:2821
        OOOOO0OOOOO0OO0O0 =OO000O0OOO000O000 .copy ()#line:2824
        OOOOO0OOOOO0OO0O0 ["c"]="c"#line:2825
        OO0OO00000OO000OO =OOOOO0OOOOO0OO0O0 .groupby ([OO00000O000OOOO0O [0 ]]).agg (计数 =("c","count")).reset_index ()#line:2826
        O00OOOO000O00O0O0 =OO0OO00000OO000OO .copy ()#line:2827
        O00OOOO000O00O0O0 [OO00000O000OOOO0O [0 ]]=O00OOOO000O00O0O0 [OO00000O000OOOO0O [0 ]].str .replace ("*","",regex =False )#line:2828
        O00OOOO000O00O0O0 ["所有项目"]=""#line:2829
        O0O0O00O0OOO0O0OO =1 #line:2830
        OO0000OOO0OO000OO =int (len (O00OOOO000O00O0O0 ))#line:2831
        for OOOOO0O0OOOOOO00O ,OOO000OOO00O0O0OO in O00OOOO000O00O0O0 .iterrows ():#line:2832
            O0O0OOO0000O000OO =OOOOO0OOOOO0OO0O0 [(OOOOO0OOOOO0OO0O0 [OO00000O000OOOO0O [0 ]]==OOO000OOO00O0O0OO [OO00000O000OOOO0O [0 ]])]#line:2834
            OOO0O0O00OO0O0OO0 =str (Counter (TOOLS_get_list0 ("use("+str (OO00000O000OOOO0O [1 ])+").file",O0O0OOO0000O000OO ,1000 ))).replace ("Counter({","{")#line:2836
            OOO0O0O00OO0O0OO0 =OOO0O0O00OO0O0OO0 .replace ("})","}")#line:2837
            import ast #line:2838
            OO0O00000OO0O0O0O =ast .literal_eval (OOO0O0O00OO0O0OO0 )#line:2839
            O0OO000O0O0000O00 =TOOLS_easyreadT (pd .DataFrame ([OO0O00000OO0O0O0O ]))#line:2840
            O0OO000O0O0000O00 =O0OO000O0O0000O00 .rename (columns ={"逐条查看":"名称规整"})#line:2841
            PROGRAM_change_schedule (O0O0O00O0OOO0O0OO ,OO0000OOO0OO000OO )#line:2843
            O0O0O00O0OOO0O0OO =O0O0O00O0OOO0O0OO +1 #line:2844
            for O0OOO0O00OO00O0OO ,OOO0O0O0OO0O0OOO0 in O0OO000O0O0000O00 .iterrows ():#line:2845
                    if "分隔符"not in OOO0O0O0OO0O0OOO0 ["条目"]:#line:2846
                        O00O00OO00OO00OO0 ="'"+str (OOO0O0O0OO0O0OOO0 ["条目"])+"':"+str (OOO0O0O0OO0O0OOO0 ["详细描述T"])+","#line:2847
                        O00OOOO000O00O0O0 .loc [OOOOO0O0OOOOOO00O ,"所有项目"]=O00OOOO000O00O0O0 .loc [OOOOO0O0OOOOOO00O ,"所有项目"]+O00O00OO00OO00OO0 #line:2848
        O00OOOO000O00O0O0 ["所有项目"]="{"+O00OOOO000O00O0O0 ["所有项目"]+"}"#line:2850
        O00OOOO000O00O0O0 ["报表类型"]="dfx_chanpin"#line:2851
        TABLE_tree_Level_2 (O00OOOO000O00O0O0 .sort_values (by ="计数",ascending =[False ],na_position ="last"),1 ,OOOOO0OOOOO0OO0O0 )#line:2853
    if O0O0OO000O0000000 =="追加外部表格信息":#line:2855
        O0OO00O00O0OO000O =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:2858
        O0O0O00O0OOO0O0OO =[pd .read_excel (OOOOOOO000OO000OO ,header =0 ,sheet_name =0 )for OOOOOOO000OO000OO in O0OO00O00O0OO000O ]#line:2859
        O00O0000OO0OOO000 =pd .concat (O0O0O00O0OOO0O0OO ,ignore_index =True ).drop_duplicates (O000O000000OO0O0O )#line:2860
        OO00O0O0O000OO00O =pd .merge (OO000O0OOO000O000 ,O00O0000OO0OOO000 ,on =O000O000000OO0O0O ,how ="left")#line:2861
        TABLE_tree_Level_2 (OO00O0O0O000OO00O ,1 ,OO00O0O0O000OO00O )#line:2862
    if O0O0OO000O0000000 =="添加到外部表格":#line:2864
        O0OO00O00O0OO000O =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:2867
        O0O0O00O0OOO0O0OO =[pd .read_excel (O0OO0OOOOO0000000 ,header =0 ,sheet_name =0 )for O0OO0OOOOO0000000 in O0OO00O00O0OO000O ]#line:2868
        O00O0000OO0OOO000 =pd .concat (O0O0O00O0OOO0O0OO ,ignore_index =True ).drop_duplicates ()#line:2869
        OO00O0O0O000OO00O =pd .merge (O00O0000OO0OOO000 ,OO000O0OOO000O000 .drop_duplicates (O000O000000OO0O0O ),on =O000O000000OO0O0O ,how ="left")#line:2870
        TABLE_tree_Level_2 (OO00O0O0O000OO00O ,1 ,OO00O0O0O000OO00O )#line:2871
    if O0O0OO000O0000000 =="饼图(XY)":#line:2874
        DRAW_make_one (OO000O0OOO000O000 ,"饼图",OO00000O000OOOO0O [0 ],OO00000O000OOOO0O [1 ],"饼图")#line:2875
    if O0O0OO000O0000000 =="柱状图(XY)":#line:2876
        DRAW_make_one (OO000O0OOO000O000 ,"柱状图",OO00000O000OOOO0O [0 ],OO00000O000OOOO0O [1 ],"柱状图")#line:2877
    if O0O0OO000O0000000 =="折线图(XY)":#line:2878
        DRAW_make_one (OO000O0OOO000O000 ,"折线图",OO00000O000OOOO0O [0 ],OO00000O000OOOO0O [1 ],"折线图")#line:2879
    if O0O0OO000O0000000 =="托帕斯图(XY)":#line:2880
        DRAW_make_one (OO000O0OOO000O000 ,"托帕斯图",OO00000O000OOOO0O [0 ],OO00000O000OOOO0O [1 ],"托帕斯图")#line:2881
    if O0O0OO000O0000000 =="堆叠柱状图（X-YZ）":#line:2882
        DRAW_make_mutibar (OO000O0OOO000O000 ,OO00O0O0OO00OO000 [1 ],OO00O0O0OO00OO000 [2 ],OO00O0O0OO00OO000 [0 ],OO00O0O0OO00OO000 [1 ],OO00O0O0OO00OO000 [2 ],"堆叠柱状图")#line:2883
def STAT_countx (O0O0O0OO00O0OOOO0 ):#line:2893
	""#line:2894
	return O0O0O0OO00O0OOOO0 .value_counts ().to_dict ()#line:2895
def STAT_countpx (OOO00O0O0OOO00O0O ,OOOOO0O00OOOOO0OO ):#line:2897
	""#line:2898
	return len (OOO00O0O0OOO00O0O [(OOO00O0O0OOO00O0O ==OOOOO0O00OOOOO0OO )])#line:2899
def STAT_countnpx (OO000O00000000O00 ,OOO00000O0O0000OO ):#line:2901
	""#line:2902
	return len (OO000O00000000O00 [(OO000O00000000O00 not in OOO00000O0O0000OO )])#line:2903
def STAT_get_max (O0O0OO0000000O000 ):#line:2905
	""#line:2906
	return O0O0OO0000000O000 .value_counts ().max ()#line:2907
def STAT_get_mean (OO00000O00OO0O000 ):#line:2909
	""#line:2910
	return round (OO00000O00OO0O000 .value_counts ().mean (),2 )#line:2911
def STAT_get_std (OOO0000OOOO000OO0 ):#line:2913
	""#line:2914
	return round (OOO0000OOOO000OO0 .value_counts ().std (ddof =1 ),2 )#line:2915
def STAT_get_95ci (OO000000OOOOO0OOO ):#line:2917
	""#line:2918
	OOOOO0O000OOO0000 =0.95 #line:2919
	O0O0OO0O0OO0O0O0O =OO000000OOOOO0OOO .value_counts ().tolist ()#line:2920
	if len (O0O0OO0O0OO0O0O0O )<30 :#line:2921
		OO00O0OO0O00OOOOO =st .t .interval (OOOOO0O000OOO0000 ,df =len (O0O0OO0O0OO0O0O0O )-1 ,loc =np .mean (O0O0OO0O0OO0O0O0O ),scale =st .sem (O0O0OO0O0OO0O0O0O ))#line:2922
	else :#line:2923
		OO00O0OO0O00OOOOO =st .norm .interval (OOOOO0O000OOO0000 ,loc =np .mean (O0O0OO0O0OO0O0O0O ),scale =st .sem (O0O0OO0O0OO0O0O0O ))#line:2924
	return round (OO00O0OO0O00OOOOO [1 ],2 )#line:2925
def STAT_get_mean_std_ci (O00OO0O0OOO00O0O0 ,OOOOO0O0O00OO0O00 ):#line:2927
	""#line:2928
	warnings .filterwarnings ("ignore")#line:2929
	O000OOO00000O00OO =TOOLS_strdict_to_pd (str (O00OO0O0OOO00O0O0 ))["content"].values /OOOOO0O0O00OO0O00 #line:2930
	O00O0O0OOOOO00000 =round (O000OOO00000O00OO .mean (),2 )#line:2931
	O0OO0OOO000OO0000 =round (O000OOO00000O00OO .std (ddof =1 ),2 )#line:2932
	if len (O000OOO00000O00OO )<30 :#line:2934
		O0000O0O0000OOO0O =st .t .interval (0.95 ,df =len (O000OOO00000O00OO )-1 ,loc =np .mean (O000OOO00000O00OO ),scale =st .sem (O000OOO00000O00OO ))#line:2935
	else :#line:2936
		O0000O0O0000OOO0O =st .norm .interval (0.95 ,loc =np .mean (O000OOO00000O00OO ),scale =st .sem (O000OOO00000O00OO ))#line:2937
	return pd .Series ((O00O0O0OOOOO00000 ,O0OO0OOO000OO0000 ,O0000O0O0000OOO0O [1 ]))#line:2941
def STAT_findx_value (OOOO0OOOO0O0OO00O ,O00OOO00OOO0OO00O ):#line:2943
	""#line:2944
	warnings .filterwarnings ("ignore")#line:2945
	O0O00O0OO0OOO00OO =TOOLS_strdict_to_pd (str (OOOO0OOOO0O0OO00O ))#line:2946
	OOO0O0000OO0000OO =O0O00O0OO0OOO00OO .where (O0O00O0OO0OOO00OO ["index"]==str (O00OOO00OOO0OO00O ))#line:2948
	print (OOO0O0000OO0000OO )#line:2949
	return OOO0O0000OO0000OO #line:2950
def STAT_judge_x (OO0O00O0O0000000O ,OOOO000OOO0O0OOOO ):#line:2952
	""#line:2953
	for OOO0OOOOO00O000O0 in OOOO000OOO0O0OOOO :#line:2954
		if OO0O00O0O0000000O .find (OOO0OOOOO00O000O0 )>-1 :#line:2955
			return 1 #line:2956
def STAT_recent30 (O00O0O00OO0O0O000 ,O0OO0OOO0OO0O0OOO ):#line:2958
	""#line:2959
	import datetime #line:2960
	O0O00000O0O000O0O =O00O0O00OO0O0O000 [(O00O0O00OO0O0O000 ["报告日期"].dt .date >(datetime .date .today ()-datetime .timedelta (days =30 )))]#line:2964
	O00O0OOOO0O0O000O =O0O00000O0O000O0O .drop_duplicates (["报告编码"]).groupby (O0OO0OOO0OO0O0OOO ).agg (最近30天报告数 =("报告编码","nunique"),最近30天报告严重伤害数 =("伤害",lambda OOO00000O00000000 :STAT_countpx (OOO00000O00000000 .values ,"严重伤害")),最近30天报告死亡数量 =("伤害",lambda O00OO0OOO0OOOO000 :STAT_countpx (O00OO0OOO0OOOO000 .values ,"死亡")),最近30天报告单位个数 =("单位名称","nunique"),).reset_index ()#line:2971
	O00O0OOOO0O0O000O =STAT_basic_risk (O00O0OOOO0O0O000O ,"最近30天报告数","最近30天报告严重伤害数","最近30天报告死亡数量","最近30天报告单位个数").fillna (0 )#line:2972
	O00O0OOOO0O0O000O =O00O0OOOO0O0O000O .rename (columns ={"风险评分":"最近30天风险评分"})#line:2974
	return O00O0OOOO0O0O000O #line:2975
def STAT_PPR_ROR_1 (OO0O000O00O000O00 ,O00OO0O0O0O00OO00 ,OO00O0OO00000OO00 ,O0OOO00O0OO00OO00 ,O0O000O0OO0O00000 ):#line:2978
    ""#line:2979
    OO0OOO0O0O000OOOO =O0O000O0OO0O00000 [(O0O000O0OO0O00000 [OO0O000O00O000O00 ]==O00OO0O0O0O00OO00 )]#line:2982
    OOOOO00OO0OO00O00 =OO0OOO0O0O000OOOO .loc [OO0OOO0O0O000OOOO [OO00O0OO00000OO00 ].str .contains (O0OOO00O0OO00OO00 ,na =False )]#line:2983
    O0O0OO0O0OO0O000O =O0O000O0OO0O00000 [(O0O000O0OO0O00000 [OO0O000O00O000O00 ]!=O00OO0O0O0O00OO00 )]#line:2984
    O0OO0O0O000000O0O =O0O0OO0O0OO0O000O .loc [O0O0OO0O0OO0O000O [OO00O0OO00000OO00 ].str .contains (O0OOO00O0OO00OO00 ,na =False )]#line:2985
    OOOOOOOOO000OOOOO =(len (OOOOO00OO0OO00O00 ),(len (OO0OOO0O0O000OOOO )-len (OOOOO00OO0OO00O00 )),len (O0OO0O0O000000O0O ),(len (O0O0OO0O0OO0O000O )-len (O0OO0O0O000000O0O )))#line:2986
    if len (OOOOO00OO0OO00O00 )>0 :#line:2987
        OO0O0OOOOOO0O0O00 =STAT_PPR_ROR_0 (len (OOOOO00OO0OO00O00 ),(len (OO0OOO0O0O000OOOO )-len (OOOOO00OO0OO00O00 )),len (O0OO0O0O000000O0O ),(len (O0O0OO0O0OO0O000O )-len (O0OO0O0O000000O0O )))#line:2988
    else :#line:2989
        OO0O0OOOOOO0O0O00 =(0 ,0 ,0 ,0 ,0 )#line:2990
    OO0O0OO00O00OOOO0 =len (OO0OOO0O0O000OOOO )#line:2993
    if OO0O0OO00O00OOOO0 ==0 :#line:2994
        OO0O0OO00O00OOOO0 =0.5 #line:2995
    return (O0OOO00O0OO00OO00 ,len (OOOOO00OO0OO00O00 ),round (len (OOOOO00OO0OO00O00 )/OO0O0OO00O00OOOO0 *100 ,2 ),round (OO0O0OOOOOO0O0O00 [0 ],2 ),round (OO0O0OOOOOO0O0O00 [1 ],2 ),round (OO0O0OOOOOO0O0O00 [2 ],2 ),round (OO0O0OOOOOO0O0O00 [3 ],2 ),round (OO0O0OOOOOO0O0O00 [4 ],2 ),str (OOOOOOOOO000OOOOO ),)#line:3006
def STAT_basic_risk (O0OO00OOO0O0OO00O ,OOOOOO00O0OOO000O ,OOO0OOOO00O000000 ,O000OO0O0O00OO0OO ,OOOOOOO0O0O0O0O00 ):#line:3010
	""#line:3011
	O0OO00OOO0O0OO00O ["风险评分"]=0 #line:3012
	O0OO00OOO0O0OO00O .loc [((O0OO00OOO0O0OO00O [OOOOOO00O0OOO000O ]>=3 )&(O0OO00OOO0O0OO00O [OOO0OOOO00O000000 ]>=1 ))|(O0OO00OOO0O0OO00O [OOOOOO00O0OOO000O ]>=5 ),"风险评分"]=O0OO00OOO0O0OO00O ["风险评分"]+5 #line:3013
	O0OO00OOO0O0OO00O .loc [(O0OO00OOO0O0OO00O [OOO0OOOO00O000000 ]>=3 ),"风险评分"]=O0OO00OOO0O0OO00O ["风险评分"]+1 #line:3014
	O0OO00OOO0O0OO00O .loc [(O0OO00OOO0O0OO00O [O000OO0O0O00OO0OO ]>=1 ),"风险评分"]=O0OO00OOO0O0OO00O ["风险评分"]+10 #line:3015
	O0OO00OOO0O0OO00O ["风险评分"]=O0OO00OOO0O0OO00O ["风险评分"]+O0OO00OOO0O0OO00O [OOOOOOO0O0O0O0O00 ]/100 #line:3016
	return O0OO00OOO0O0OO00O #line:3017
def STAT_PPR_ROR_0 (O00O0OOO000O0OO00 ,O00OOOOOOO0O0OOOO ,O0O00000O0O0O0000 ,O00OOOO00000OOO0O ):#line:3020
    ""#line:3021
    if O00O0OOO000O0OO00 *O00OOOOOOO0O0OOOO *O0O00000O0O0O0000 *O00OOOO00000OOO0O ==0 :#line:3026
        O00O0OOO000O0OO00 =O00O0OOO000O0OO00 +1 #line:3027
        O00OOOOOOO0O0OOOO =O00OOOOOOO0O0OOOO +1 #line:3028
        O0O00000O0O0O0000 =O0O00000O0O0O0000 +1 #line:3029
        O00OOOO00000OOO0O =O00OOOO00000OOO0O +1 #line:3030
    OO00O00OOOO000O0O =(O00O0OOO000O0OO00 /(O00O0OOO000O0OO00 +O00OOOOOOO0O0OOOO ))/(O0O00000O0O0O0000 /(O0O00000O0O0O0000 +O00OOOO00000OOO0O ))#line:3031
    OO00O0O00O0OOOOO0 =math .sqrt (1 /O00O0OOO000O0OO00 -1 /(O00O0OOO000O0OO00 +O00OOOOOOO0O0OOOO )+1 /O0O00000O0O0O0000 -1 /(O0O00000O0O0O0000 +O00OOOO00000OOO0O ))#line:3032
    O00O00OO00OO000O0 =(math .exp (math .log (OO00O00OOOO000O0O )-1.96 *OO00O0O00O0OOOOO0 ),math .exp (math .log (OO00O00OOOO000O0O )+1.96 *OO00O0O00O0OOOOO0 ),)#line:3036
    O0O0O00OO0OO0O0OO =(O00O0OOO000O0OO00 /O0O00000O0O0O0000 )/(O00OOOOOOO0O0OOOO /O00OOOO00000OOO0O )#line:3037
    O0O0OO0O00OO00OOO =math .sqrt (1 /O00O0OOO000O0OO00 +1 /O00OOOOOOO0O0OOOO +1 /O0O00000O0O0O0000 +1 /O00OOOO00000OOO0O )#line:3038
    OOO0000O0OO0OO0OO =(math .exp (math .log (O0O0O00OO0OO0O0OO )-1.96 *O0O0OO0O00OO00OOO ),math .exp (math .log (O0O0O00OO0OO0O0OO )+1.96 *O0O0OO0O00OO00OOO ),)#line:3042
    O0OOOO000OO0OOO0O =((O00O0OOO000O0OO00 *O00OOOOOOO0O0OOOO -O00OOOOOOO0O0OOOO *O0O00000O0O0O0000 )*(O00O0OOO000O0OO00 *O00OOOOOOO0O0OOOO -O00OOOOOOO0O0OOOO *O0O00000O0O0O0000 )*(O00O0OOO000O0OO00 +O00OOOOOOO0O0OOOO +O0O00000O0O0O0000 +O00OOOO00000OOO0O ))/((O00O0OOO000O0OO00 +O00OOOOOOO0O0OOOO )*(O0O00000O0O0O0000 +O00OOOO00000OOO0O )*(O00O0OOO000O0OO00 +O0O00000O0O0O0000 )*(O00OOOOOOO0O0OOOO +O00OOOO00000OOO0O ))#line:3045
    return O0O0O00OO0OO0O0OO ,OOO0000O0OO0OO0OO [0 ],OO00O00OOOO000O0O ,O00O00OO00OO000O0 [0 ],O0OOOO000OO0OOO0O #line:3046
def STAT_find_keyword_risk (OOO0OO000O0O00OOO ,OOOOOO00OOOOO0OOO ,OO000O0OOOO000000 ,OO000OO0O0OOO00O0 ,OO0O000OO0OO0000O ):#line:3048
		""#line:3049
		OOO0OO000O0O00OOO =OOO0OO000O0O00OOO .drop_duplicates (["报告编码"]).reset_index (drop =True )#line:3050
		OO0O00O00OOO0OOO0 =OOO0OO000O0O00OOO .groupby (OOOOOO00OOOOO0OOO ).agg (证号关键字总数量 =(OO000O0OOOO000000 ,"count"),包含元素个数 =(OO000OO0O0OOO00O0 ,"nunique"),包含元素 =(OO000OO0O0OOO00O0 ,STAT_countx ),).reset_index ()#line:3055
		O0O0000OO000O00OO =OOOOOO00OOOOO0OOO .copy ()#line:3057
		O0O0000OO000O00OO .append (OO000OO0O0OOO00O0 )#line:3058
		OO0OOOOOO000O0O00 =OOO0OO000O0O00OOO .groupby (O0O0000OO000O00OO ).agg (计数 =(OO000OO0O0OOO00O0 ,"count"),严重伤害数 =("伤害",lambda O00OOO00000OOO0O0 :STAT_countpx (O00OOO00000OOO0O0 .values ,"严重伤害")),死亡数量 =("伤害",lambda OO000OO0OO0O0O0OO :STAT_countpx (OO000OO0OO0O0O0OO .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),).reset_index ()#line:3065
		OOOO0O0000O00OO00 =O0O0000OO000O00OO .copy ()#line:3068
		OOOO0O0000O00OO00 .remove ("关键字")#line:3069
		OO0OOOOO00O00O00O =OOO0OO000O0O00OOO .groupby (OOOO0O0000O00OO00 ).agg (该元素总数 =(OO000OO0O0OOO00O0 ,"count"),).reset_index ()#line:3072
		OO0OOOOOO000O0O00 ["证号总数"]=OO0O000OO0OO0000O #line:3074
		OOO00OOO0OO0OOOO0 =pd .merge (OO0OOOOOO000O0O00 ,OO0O00O00OOO0OOO0 ,on =OOOOOO00OOOOO0OOO ,how ="left")#line:3075
		if len (OOO00OOO0OO0OOOO0 )>0 :#line:3080
			OOO00OOO0OO0OOOO0 [['数量均值','数量标准差','数量CI']]=OOO00OOO0OO0OOOO0 .包含元素 .apply (lambda O0000OOO0OO00O0O0 :STAT_get_mean_std_ci (O0000OOO0OO00O0O0 ,1 ))#line:3081
		return OOO00OOO0OO0OOOO0 #line:3084
def STAT_find_risk (OOO0OO0O0OO0O0000 ,OO0OO0O00OO000OOO ,OOO00OOOO0O0OO00O ,O0OOOO0OO0O0OOOOO ):#line:3090
		""#line:3091
		OOO0OO0O0OO0O0000 =OOO0OO0O0OO0O0000 .drop_duplicates (["报告编码"]).reset_index (drop =True )#line:3092
		O00000O0O0O0OO000 =OOO0OO0O0OO0O0000 .groupby (OO0OO0O00OO000OOO ).agg (证号总数量 =(OOO00OOOO0O0OO00O ,"count"),包含元素个数 =(O0OOOO0OO0O0OOOOO ,"nunique"),包含元素 =(O0OOOO0OO0O0OOOOO ,STAT_countx ),均值 =(O0OOOO0OO0O0OOOOO ,STAT_get_mean ),标准差 =(O0OOOO0OO0O0OOOOO ,STAT_get_std ),CI上限 =(O0OOOO0OO0O0OOOOO ,STAT_get_95ci ),).reset_index ()#line:3100
		OO0O0OO00O0OOOO00 =OO0OO0O00OO000OOO .copy ()#line:3102
		OO0O0OO00O0OOOO00 .append (O0OOOO0OO0O0OOOOO )#line:3103
		OO0O0OOO0OO0OO00O =OOO0OO0O0OO0O0000 .groupby (OO0O0OO00O0OOOO00 ).agg (计数 =(O0OOOO0OO0O0OOOOO ,"count"),严重伤害数 =("伤害",lambda O0OOO0O000OO0O000 :STAT_countpx (O0OOO0O000OO0O000 .values ,"严重伤害")),死亡数量 =("伤害",lambda O00O0O0000000OOOO :STAT_countpx (O00O0O0000000OOOO .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),).reset_index ()#line:3110
		O0O0OO0000OO000O0 =pd .merge (OO0O0OOO0OO0OO00O ,O00000O0O0O0OO000 ,on =OO0OO0O00OO000OOO ,how ="left")#line:3112
		O0O0OO0000OO000O0 ["风险评分"]=0 #line:3114
		O0O0OO0000OO000O0 ["报表类型"]="dfx_findrisk"+O0OOOO0OO0O0OOOOO #line:3115
		O0O0OO0000OO000O0 .loc [((O0O0OO0000OO000O0 ["计数"]>=3 )&(O0O0OO0000OO000O0 ["严重伤害数"]>=1 )|(O0O0OO0000OO000O0 ["计数"]>=5 )),"风险评分"]=O0O0OO0000OO000O0 ["风险评分"]+5 #line:3116
		O0O0OO0000OO000O0 .loc [(O0O0OO0000OO000O0 ["计数"]>=(O0O0OO0000OO000O0 ["均值"]+O0O0OO0000OO000O0 ["标准差"])),"风险评分"]=O0O0OO0000OO000O0 ["风险评分"]+1 #line:3117
		O0O0OO0000OO000O0 .loc [(O0O0OO0000OO000O0 ["计数"]>=O0O0OO0000OO000O0 ["CI上限"]),"风险评分"]=O0O0OO0000OO000O0 ["风险评分"]+1 #line:3118
		O0O0OO0000OO000O0 .loc [(O0O0OO0000OO000O0 ["严重伤害数"]>=3 )&(O0O0OO0000OO000O0 ["风险评分"]>=7 ),"风险评分"]=O0O0OO0000OO000O0 ["风险评分"]+1 #line:3119
		O0O0OO0000OO000O0 .loc [(O0O0OO0000OO000O0 ["死亡数量"]>=1 ),"风险评分"]=O0O0OO0000OO000O0 ["风险评分"]+10 #line:3120
		O0O0OO0000OO000O0 ["风险评分"]=O0O0OO0000OO000O0 ["风险评分"]+O0O0OO0000OO000O0 ["单位个数"]/100 #line:3121
		O0O0OO0000OO000O0 =O0O0OO0000OO000O0 .sort_values (by ="风险评分",ascending =[False ],na_position ="last").reset_index (drop =True )#line:3122
		return O0O0OO0000OO000O0 #line:3124
def TABLE_tree_Level_2 (OOO0OOO0OOOOO00OO ,O0OO000O0OOOO00OO ,OO00O0O0O00OO00O0 ,*O0O00000O000OO0O0 ):#line:3131
    ""#line:3132
    try :#line:3134
        OO0O0O00O0OO00O0O =OOO0OOO0OOOOO00OO .columns #line:3135
    except :#line:3136
        return 0 #line:3137
    if "报告编码"in OOO0OOO0OOOOO00OO .columns :#line:3139
        O0OO000O0OOOO00OO =0 #line:3140
    try :#line:3141
        O00OOOO00O0O0O00O =len (np .unique (OOO0OOO0OOOOO00OO ["注册证编号/曾用注册证编号"].values ))#line:3142
    except :#line:3143
        O00OOOO00O0O0O00O =10 #line:3144
    O00000OO0OO000OOO =Toplevel ()#line:3147
    O00000OO0OO000OOO .title ("报表查看器")#line:3148
    O0000OO00OOO000OO =O00000OO0OO000OOO .winfo_screenwidth ()#line:3149
    O0O0OOOOOOO000OO0 =O00000OO0OO000OOO .winfo_screenheight ()#line:3151
    O0O0OO0OOO000OO00 =1310 #line:3153
    OO0O0OO000O0OOOOO =600 #line:3154
    try :#line:3155
        if O0O00000O000OO0O0 [0 ]=="tools_x":#line:3156
           OO0O0OO000O0OOOOO =60 #line:3157
    except :#line:3158
            pass #line:3159
    O0OOOO0O000O0OOOO =(O0000OO00OOO000OO -O0O0OO0OOO000OO00 )/2 #line:3162
    OOOO00O0OO0OO00OO =(O0O0OOOOOOO000OO0 -OO0O0OO000O0OOOOO )/2 #line:3163
    O00000OO0OO000OOO .geometry ("%dx%d+%d+%d"%(O0O0OO0OOO000OO00 ,OO0O0OO000O0OOOOO ,O0OOOO0O000O0OOOO ,OOOO00O0OO0OO00OO ))#line:3164
    OOO0OOO000O000000 =ttk .Frame (O00000OO0OO000OOO ,width =1310 ,height =20 )#line:3167
    OOO0OOO000O000000 .pack (side =TOP )#line:3168
    O000OOO0O00000O00 =ttk .Frame (O00000OO0OO000OOO ,width =1310 ,height =20 )#line:3169
    O000OOO0O00000O00 .pack (side =BOTTOM )#line:3170
    O0OOO00OO0O00O0OO =ttk .Frame (O00000OO0OO000OOO ,width =1310 ,height =600 )#line:3171
    O0OOO00OO0O00O0OO .pack (fill ="both",expand ="false")#line:3172
    if O0OO000O0OOOO00OO ==0 :#line:3176
        PROGRAM_Menubar (O00000OO0OO000OOO ,OOO0OOO0OOOOO00OO ,O0OO000O0OOOO00OO ,OO00O0O0O00OO00O0 )#line:3177
    try :#line:3180
        O00000O000O0O0OOO =StringVar ()#line:3181
        O00000O000O0O0OOO .set ("产品类别")#line:3182
        def O0OO0OO00OO0O0O0O (*O0O0OOOOOOOOOOO0O ):#line:3183
            O00000O000O0O0OOO .set (O000OO00O0O0O0000 .get ())#line:3184
        OO00OOO0O0000OOO0 =StringVar ()#line:3185
        OO00OOO0O0000OOO0 .set ("无源|诊断试剂")#line:3186
        OOOO0O0OOOOO00000 =Label (OOO0OOO000O000000 ,text ="")#line:3187
        OOOO0O0OOOOO00000 .pack (side =LEFT )#line:3188
        OOOO0O0OOOOO00000 =Label (OOO0OOO000O000000 ,text ="位置：")#line:3189
        OOOO0O0OOOOO00000 .pack (side =LEFT )#line:3190
        O0OOOO0OOOO00OO00 =StringVar ()#line:3191
        O000OO00O0O0O0000 =ttk .Combobox (OOO0OOO000O000000 ,width =12 ,height =30 ,state ="readonly",textvariable =O0OOOO0OOOO00OO00 )#line:3194
        O000OO00O0O0O0000 ["values"]=OOO0OOO0OOOOO00OO .columns .tolist ()#line:3195
        O000OO00O0O0O0000 .current (0 )#line:3196
        O000OO00O0O0O0000 .bind ("<<ComboboxSelected>>",O0OO0OO00OO0O0O0O )#line:3197
        O000OO00O0O0O0000 .pack (side =LEFT )#line:3198
        O00O000OO0O0O000O =Label (OOO0OOO000O000000 ,text ="检索：")#line:3199
        O00O000OO0O0O000O .pack (side =LEFT )#line:3200
        O0O0O000O0O00OOOO =Entry (OOO0OOO000O000000 ,width =12 ,textvariable =OO00OOO0O0000OOO0 ).pack (side =LEFT )#line:3201
        def O0OO0OO0O0OOOOOOO ():#line:3203
            pass #line:3204
        O0OO000O0000000O0 =Button (OOO0OOO000O000000 ,text ="导出",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_save_dict (OOO0OOO0OOOOO00OO ),)#line:3218
        O0OO000O0000000O0 .pack (side =LEFT )#line:3219
        O00O0OO0O0OOOOO00 =Button (OOO0OOO000O000000 ,text ="视图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (TOOLS_easyreadT (OOO0OOO0OOOOO00OO ),1 ,OO00O0O0O00OO00O0 ),)#line:3228
        if "详细描述T"not in OOO0OOO0OOOOO00OO .columns :#line:3229
            O00O0OO0O0OOOOO00 .pack (side =LEFT )#line:3230
        O00O0OO0O0OOOOO00 =Button (OOO0OOO000O000000 ,text ="网",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_web_view (OOO0OOO0OOOOO00OO ),)#line:3240
        if "详细描述T"not in OOO0OOO0OOOOO00OO .columns :#line:3241
            O00O0OO0O0OOOOO00 .pack (side =LEFT )#line:3242
        OO0OO0O00O0000OOO =Button (OOO0OOO000O000000 ,text ="含",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (OOO0OOO0OOOOO00OO .loc [OOO0OOO0OOOOO00OO [O00000O000O0O0OOO .get ()].astype (str ).str .contains (str (OO00OOO0O0000OOO0 .get ()),na =False )],1 ,OO00O0O0O00OO00O0 ,),)#line:3260
        OO0OO0O00O0000OOO .pack (side =LEFT )#line:3261
        OO0OO0O00O0000OOO =Button (OOO0OOO000O000000 ,text ="无",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (OOO0OOO0OOOOO00OO .loc [~OOO0OOO0OOOOO00OO [O00000O000O0O0OOO .get ()].astype (str ).str .contains (str (OO00OOO0O0000OOO0 .get ()),na =False )],1 ,OO00O0O0O00OO00O0 ,),)#line:3278
        OO0OO0O00O0000OOO .pack (side =LEFT )#line:3279
        OO0OO0O00O0000OOO =Button (OOO0OOO000O000000 ,text ="大",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (OOO0OOO0OOOOO00OO .loc [OOO0OOO0OOOOO00OO [O00000O000O0O0OOO .get ()].astype (float )>float (OO00OOO0O0000OOO0 .get ())],1 ,OO00O0O0O00OO00O0 ,),)#line:3294
        OO0OO0O00O0000OOO .pack (side =LEFT )#line:3295
        OO0OO0O00O0000OOO =Button (OOO0OOO000O000000 ,text ="小",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (OOO0OOO0OOOOO00OO .loc [OOO0OOO0OOOOO00OO [O00000O000O0O0OOO .get ()].astype (float )<float (OO00OOO0O0000OOO0 .get ())],1 ,OO00O0O0O00OO00O0 ,),)#line:3310
        OO0OO0O00O0000OOO .pack (side =LEFT )#line:3311
        OO0OO0O00O0000OOO =Button (OOO0OOO000O000000 ,text ="等",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (OOO0OOO0OOOOO00OO .loc [OOO0OOO0OOOOO00OO [O00000O000O0O0OOO .get ()].astype (float )==float (OO00OOO0O0000OOO0 .get ())],1 ,OO00O0O0O00OO00O0 ,),)#line:3326
        OO0OO0O00O0000OOO .pack (side =LEFT )#line:3327
        OO0OO0O00O0000OOO =Button (OOO0OOO000O000000 ,text ="式",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_findin (OOO0OOO0OOOOO00OO ,OO00O0O0O00OO00O0 ))#line:3336
        OO0OO0O00O0000OOO .pack (side =LEFT )#line:3337
        OO0OO0O00O0000OOO =Button (OOO0OOO000O000000 ,text ="前",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (OOO0OOO0OOOOO00OO .head (int (OO00OOO0O0000OOO0 .get ())),1 ,OO00O0O0O00OO00O0 ,),)#line:3352
        OO0OO0O00O0000OOO .pack (side =LEFT )#line:3353
        OO0OO0O00O0000OOO =Button (OOO0OOO000O000000 ,text ="升",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (OOO0OOO0OOOOO00OO .sort_values (by =(O00000O000O0O0OOO .get ()),ascending =[True ],na_position ="last"),1 ,OO00O0O0O00OO00O0 ,),)#line:3368
        OO0OO0O00O0000OOO .pack (side =LEFT )#line:3369
        OO0OO0O00O0000OOO =Button (OOO0OOO000O000000 ,text ="降",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (OOO0OOO0OOOOO00OO .sort_values (by =(O00000O000O0O0OOO .get ()),ascending =[False ],na_position ="last"),1 ,OO00O0O0O00OO00O0 ,),)#line:3384
        OO0OO0O00O0000OOO .pack (side =LEFT )#line:3385
        OO0OO0O00O0000OOO =Button (OOO0OOO000O000000 ,text ="SQL",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_sql (OOO0OOO0OOOOO00OO ),)#line:3395
        OO0OO0O00O0000OOO .pack (side =LEFT )#line:3396
    except :#line:3399
        pass #line:3400
    if ini ["模式"]!="其他":#line:3403
        OOOOOO000O00OOO0O =Button (OOO0OOO000O000000 ,text ="近月",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (OOO0OOO0OOOOO00OO [(OOO0OOO0OOOOO00OO ["最近30天报告单位个数"]>=1 )],1 ,OO00O0O0O00OO00O0 ,),)#line:3416
        if "最近30天报告数"in OOO0OOO0OOOOO00OO .columns :#line:3417
            OOOOOO000O00OOO0O .pack (side =LEFT )#line:3418
        OO0OO0O00O0000OOO =Button (OOO0OOO000O000000 ,text ="图表",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_pre (OOO0OOO0OOOOO00OO ),)#line:3430
        if O0OO000O0OOOO00OO !=0 :#line:3431
            OO0OO0O00O0000OOO .pack (side =LEFT )#line:3432
        def OOOO000O00000OO00 ():#line:3437
            pass #line:3438
        if O0OO000O0OOOO00OO ==0 :#line:3441
            OOOOOO000O00OOO0O =Button (OOO0OOO000O000000 ,text ="精简",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (TOOLS_easyread2 (OOO0OOO0OOOOO00OO ),1 ,OO00O0O0O00OO00O0 ,),)#line:3455
            OOOOOO000O00OOO0O .pack (side =LEFT )#line:3456
        if O0OO000O0OOOO00OO ==0 :#line:3459
            OOOOOO000O00OOO0O =Button (OOO0OOO000O000000 ,text ="证号",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (OOO0OOO0OOOOO00OO ).df_zhenghao (),1 ,OO00O0O0O00OO00O0 ,),)#line:3473
            OOOOOO000O00OOO0O .pack (side =LEFT )#line:3474
            OOOOOO000O00OOO0O =Button (OOO0OOO000O000000 ,text ="图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_pre (Countall (OOO0OOO0OOOOO00OO ).df_zhenghao ()))#line:3483
            OOOOOO000O00OOO0O .pack (side =LEFT )#line:3484
            OOOOOO000O00OOO0O =Button (OOO0OOO000O000000 ,text ="批号",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (OOO0OOO0OOOOO00OO ).df_pihao (),1 ,OO00O0O0O00OO00O0 ,),)#line:3499
            OOOOOO000O00OOO0O .pack (side =LEFT )#line:3500
            OOOOOO000O00OOO0O =Button (OOO0OOO000O000000 ,text ="图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_pre (Countall (OOO0OOO0OOOOO00OO ).df_pihao ()))#line:3509
            OOOOOO000O00OOO0O .pack (side =LEFT )#line:3510
            OOOOOO000O00OOO0O =Button (OOO0OOO000O000000 ,text ="型号",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (OOO0OOO0OOOOO00OO ).df_xinghao (),1 ,OO00O0O0O00OO00O0 ,),)#line:3525
            OOOOOO000O00OOO0O .pack (side =LEFT )#line:3526
            OOOOOO000O00OOO0O =Button (OOO0OOO000O000000 ,text ="图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_pre (Countall (OOO0OOO0OOOOO00OO ).df_xinghao ()))#line:3535
            OOOOOO000O00OOO0O .pack (side =LEFT )#line:3536
            OOOOOO000O00OOO0O =Button (OOO0OOO000O000000 ,text ="规格",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (OOO0OOO0OOOOO00OO ).df_guige (),1 ,OO00O0O0O00OO00O0 ,),)#line:3551
            OOOOOO000O00OOO0O .pack (side =LEFT )#line:3552
            OOOOOO000O00OOO0O =Button (OOO0OOO000O000000 ,text ="图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_pre (Countall (OOO0OOO0OOOOO00OO ).df_guige ()))#line:3561
            OOOOOO000O00OOO0O .pack (side =LEFT )#line:3562
            OOOOOO000O00OOO0O =Button (OOO0OOO000O000000 ,text ="企业",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (OOO0OOO0OOOOO00OO ).df_chiyouren (),1 ,OO00O0O0O00OO00O0 ,),)#line:3577
            OOOOOO000O00OOO0O .pack (side =LEFT )#line:3578
            OOOOOO000O00OOO0O =Button (OOO0OOO000O000000 ,text ="县区",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (OOO0OOO0OOOOO00OO ).df_org ("监测机构"),1 ,OO00O0O0O00OO00O0 ,),)#line:3594
            OOOOOO000O00OOO0O .pack (side =LEFT )#line:3595
            OOOOOO000O00OOO0O =Button (OOO0OOO000O000000 ,text ="单位",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (OOO0OOO0OOOOO00OO ).df_user (),1 ,OO00O0O0O00OO00O0 ,),)#line:3608
            OOOOOO000O00OOO0O .pack (side =LEFT )#line:3609
            OOOOOO000O00OOO0O =Button (OOO0OOO000O000000 ,text ="年龄",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (OOO0OOO0OOOOO00OO ).df_age (),1 ,OO00O0O0O00OO00O0 ,),)#line:3623
            OOOOOO000O00OOO0O .pack (side =LEFT )#line:3624
            OOOOOO000O00OOO0O =Button (OOO0OOO000O000000 ,text ="时隔",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (TOOLS_deep_view (OOO0OOO0OOOOO00OO ,["时隔"],["报告编码","nunique"],0 ),1 ,OO00O0O0O00OO00O0 ,),)#line:3638
            OOOOOO000O00OOO0O .pack (side =LEFT )#line:3639
            OOOOOO000O00OOO0O =Button (OOO0OOO000O000000 ,text ="表现",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (OOO0OOO0OOOOO00OO ).df_psur (),1 ,OO00O0O0O00OO00O0 ,),)#line:3653
            if "UDI"not in OOO0OOO0OOOOO00OO .columns :#line:3654
                OOOOOO000O00OOO0O .pack (side =LEFT )#line:3655
            OOOOOO000O00OOO0O =Button (OOO0OOO000O000000 ,text ="表现",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (TOOLS_get_guize2 (OOO0OOO0OOOOO00OO ),1 ,OO00O0O0O00OO00O0 ,),)#line:3668
            if "UDI"in OOO0OOO0OOOOO00OO .columns :#line:3669
                OOOOOO000O00OOO0O .pack (side =LEFT )#line:3670
            OOOOOO000O00OOO0O =Button (OOO0OOO000O000000 ,text ="发生时间",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_time (OOO0OOO0OOOOO00OO ,"事件发生日期",0 ),)#line:3679
            OOOOOO000O00OOO0O .pack (side =LEFT )#line:3680
            OOOOOO000O00OOO0O =Button (OOO0OOO000O000000 ,text ="报告时间",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_make_one (TOOLS_time (OOO0OOO0OOOOO00OO ,"报告日期",1 ),"时间托帕斯图","time","报告总数","超级托帕斯图(严重伤害数)"),)#line:3690
            OOOOOO000O00OOO0O .pack (side =LEFT )#line:3691
    try :#line:3697
        OO000000OOO000O00 =ttk .Label (O000OOO0O00000O00 ,text ="方法：")#line:3699
        OO000000OOO000O00 .pack (side =LEFT )#line:3700
        O0O00O0OO0O00000O =StringVar ()#line:3701
        OOOOO0O00000O0OO0 =ttk .Combobox (O000OOO0O00000O00 ,width =15 ,textvariable =O0O00O0OO0O00000O ,state ='readonly')#line:3702
        OOOOO0O00000O0OO0 ['values']=("分组统计","数据透视","描述性统计","饼图(XY)","柱状图(XY)","折线图(XY)","托帕斯图(XY)","堆叠柱状图（X-YZ）","单列多项拆分统计(统计列)","单列多项拆分统计(透视列-统计列)","单列多项拆分统计(透视列-统计列-字典)","追加外部表格信息","添加到外部表格")#line:3703
        OOOOO0O00000O0OO0 .pack (side =LEFT )#line:3707
        OOOOO0O00000O0OO0 .current (0 )#line:3708
        OOO0000000O0OOO0O =ttk .Label (O000OOO0O00000O00 ,text ="分组列（X-Y-Z）:")#line:3709
        OOO0000000O0OOO0O .pack (side =LEFT )#line:3710
        O00O0OOO0O0O0O0O0 =StringVar ()#line:3713
        O0O00000000O0OOOO =ttk .Combobox (O000OOO0O00000O00 ,width =15 ,textvariable =O00O0OOO0O0O0O0O0 ,state ='readonly')#line:3714
        O0O00000000O0OOOO ['values']=OOO0OOO0OOOOO00OO .columns .tolist ()#line:3715
        O0O00000000O0OOOO .pack (side =LEFT )#line:3716
        OO0O0OOOOO0O000O0 =StringVar ()#line:3717
        OO0O0OOOO000O0O00 =ttk .Combobox (O000OOO0O00000O00 ,width =15 ,textvariable =OO0O0OOOOO0O000O0 ,state ='readonly')#line:3718
        OO0O0OOOO000O0O00 ['values']=OOO0OOO0OOOOO00OO .columns .tolist ()#line:3719
        OO0O0OOOO000O0O00 .pack (side =LEFT )#line:3720
        OOO0O00000OO00O00 =StringVar ()#line:3721
        OO000000O00O0000O =ttk .Combobox (O000OOO0O00000O00 ,width =15 ,textvariable =OOO0O00000OO00O00 ,state ='readonly')#line:3722
        OO000000O00O0000O ['values']=OOO0OOO0OOOOO00OO .columns .tolist ()#line:3723
        OO000000O00O0000O .pack (side =LEFT )#line:3724
        O0O0OOO000OOOOO0O =StringVar ()#line:3725
        O0OOO00OOO0OO0O00 =StringVar ()#line:3726
        OOO0000000O0OOO0O =ttk .Label (O000OOO0O00000O00 ,text ="计算列（V-M）:")#line:3727
        OOO0000000O0OOO0O .pack (side =LEFT )#line:3728
        OO00O000O0O000OO0 =ttk .Combobox (O000OOO0O00000O00 ,width =10 ,textvariable =O0O0OOO000OOOOO0O ,state ='readonly')#line:3730
        OO00O000O0O000OO0 ['values']=OOO0OOO0OOOOO00OO .columns .tolist ()#line:3731
        OO00O000O0O000OO0 .pack (side =LEFT )#line:3732
        OOOOO00O0OO000O00 =ttk .Combobox (O000OOO0O00000O00 ,width =10 ,textvariable =O0OOO00OOO0OO0O00 ,state ='readonly')#line:3733
        OOOOO00O0OO000O00 ['values']=["计数","求和","唯一值计数"]#line:3734
        OOOOO00O0OO000O00 .pack (side =LEFT )#line:3735
        OOOOOOO0OO0OO00O0 =Button (O000OOO0O00000O00 ,text ="自助报表",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_Autotable_0 (OOO0OOO0OOOOO00OO ,OOOOO0O00000O0OO0 .get (),O00O0OOO0O0O0O0O0 .get (),OO0O0OOOOO0O000O0 .get (),OOO0O00000OO00O00 .get (),O0O0OOO000OOOOO0O .get (),O0OOO00OOO0OO0O00 .get (),OOO0OOO0OOOOO00OO ))#line:3737
        OOOOOOO0OO0OO00O0 .pack (side =LEFT )#line:3738
        OO0OO0O00O0000OOO =Button (O000OOO0O00000O00 ,text ="去首行",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (OOO0OOO0OOOOO00OO [1 :],1 ,OO00O0O0O00OO00O0 ,))#line:3755
        OO0OO0O00O0000OOO .pack (side =LEFT )#line:3756
        OO0OO0O00O0000OOO =Button (O000OOO0O00000O00 ,text ="去尾行",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (OOO0OOO0OOOOO00OO [:-1 ],1 ,OO00O0O0O00OO00O0 ,),)#line:3771
        OO0OO0O00O0000OOO .pack (side =LEFT )#line:3772
        OOOOOO000O00OOO0O =Button (O000OOO0O00000O00 ,text ="行数:"+str (len (OOO0OOO0OOOOO00OO )),bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",)#line:3782
        OOOOOO000O00OOO0O .pack (side =LEFT )#line:3783
    except :#line:3786
        showinfo (title ="提示信息",message ="界面初始化失败。")#line:3787
    try :#line:3792
        if O0O00000O000OO0O0 [0 ]=="tools_x":#line:3793
           return 0 #line:3794
    except :#line:3795
            pass #line:3796
    OO0O0OO00O0O0OO0O =OOO0OOO0OOOOO00OO .values .tolist ()#line:3799
    OOOO00O0000O0000O =OOO0OOO0OOOOO00OO .columns .values .tolist ()#line:3800
    O00O000000000O000 =ttk .Treeview (O0OOO00OO0O00O0OO ,columns =OOOO00O0000O0000O ,show ="headings",height =45 )#line:3801
    for OO0O0O000O000O0OO in OOOO00O0000O0000O :#line:3804
        O00O000000000O000 .heading (OO0O0O000O000O0OO ,text =OO0O0O000O000O0OO )#line:3805
    for OOOO00OO0O0O00O00 in OO0O0OO00O0O0OO0O :#line:3806
        O00O000000000O000 .insert ("","end",values =OOOO00OO0O0O00O00 )#line:3807
    for OOOO0O00O0OO00OOO in OOOO00O0000O0000O :#line:3809
        try :#line:3810
            O00O000000000O000 .column (OOOO0O00O0OO00OOO ,minwidth =0 ,width =80 ,stretch =NO )#line:3811
            if "只剩"in OOOO0O00O0OO00OOO :#line:3812
                O00O000000000O000 .column (OOOO0O00O0OO00OOO ,minwidth =0 ,width =150 ,stretch =NO )#line:3813
        except :#line:3814
            pass #line:3815
    OO0OOO0OO0OOO0OO0 =["评分说明"]#line:3819
    OO0OOOOO0O00O0000 =["该单位喜好上报的品种统计","报告编码","产品名称","上报机构描述","持有人处理描述","该注册证编号/曾用注册证编号报告数量","通用名称","该批准文号报告数量","上市许可持有人名称",]#line:3832
    OO0OOO0O0O0O0OO0O =["注册证编号/曾用注册证编号","监测机构","报告月份","报告季度","单位列表","单位名称",]#line:3840
    O0O0OO0OO00OO0O0O =["管理类别",]#line:3844
    for OOOO0O00O0OO00OOO in OO0OOOOO0O00O0000 :#line:3847
        try :#line:3848
            O00O000000000O000 .column (OOOO0O00O0OO00OOO ,minwidth =0 ,width =200 ,stretch =NO )#line:3849
        except :#line:3850
            pass #line:3851
    for OOOO0O00O0OO00OOO in OO0OOO0O0O0O0OO0O :#line:3854
        try :#line:3855
            O00O000000000O000 .column (OOOO0O00O0OO00OOO ,minwidth =0 ,width =140 ,stretch =NO )#line:3856
        except :#line:3857
            pass #line:3858
    for OOOO0O00O0OO00OOO in O0O0OO0OO00OO0O0O :#line:3859
        try :#line:3860
            O00O000000000O000 .column (OOOO0O00O0OO00OOO ,minwidth =0 ,width =40 ,stretch =NO )#line:3861
        except :#line:3862
            pass #line:3863
    for OOOO0O00O0OO00OOO in OO0OOO0OO0OOO0OO0 :#line:3864
        try :#line:3865
            O00O000000000O000 .column (OOOO0O00O0OO00OOO ,minwidth =0 ,width =800 ,stretch =NO )#line:3866
        except :#line:3867
            pass #line:3868
    try :#line:3870
        O00O000000000O000 .column ("请选择需要查看的表格",minwidth =1 ,width =300 ,stretch =NO )#line:3873
    except :#line:3874
        pass #line:3875
    try :#line:3877
        O00O000000000O000 .column ("详细描述T",minwidth =1 ,width =2300 ,stretch =NO )#line:3880
    except :#line:3881
        pass #line:3882
    OOOO0O0O0O0OOO000 =Scrollbar (O0OOO00OO0O00O0OO ,orient ="vertical")#line:3884
    OOOO0O0O0O0OOO000 .pack (side =RIGHT ,fill =Y )#line:3885
    OOOO0O0O0O0OOO000 .config (command =O00O000000000O000 .yview )#line:3886
    O00O000000000O000 .config (yscrollcommand =OOOO0O0O0O0OOO000 .set )#line:3887
    OOOO000000O0OO0OO =Scrollbar (O0OOO00OO0O00O0OO ,orient ="horizontal")#line:3889
    OOOO000000O0OO0OO .pack (side =BOTTOM ,fill =X )#line:3890
    OOOO000000O0OO0OO .config (command =O00O000000000O000 .xview )#line:3891
    O00O000000000O000 .config (yscrollcommand =OOOO0O0O0O0OOO000 .set )#line:3892
    def O0O0O00O00000OO00 (OOOOOOOO00O0OO0OO ,OO00000OO0OOO0OOO ,O0OO0OOOOO00O000O ):#line:3895
        for OO0OO0OO0OO0OOOO0 in O00O000000000O000 .selection ():#line:3897
            O0000O0O00OO0000O =O00O000000000O000 .item (OO0OO0OO0OO0OOOO0 ,"values")#line:3898
        OO00O00O0000O000O =dict (zip (OO00000OO0OOO0OOO ,O0000O0O00OO0000O ))#line:3899
        if "详细描述T"in OO00000OO0OOO0OOO and "{"in OO00O00O0000O000O ["详细描述T"]:#line:3903
            O0OO00O0OO000OO00 =eval (OO00O00O0000O000O ["详细描述T"])#line:3904
            O0OO00O0OO000OO00 =pd .DataFrame .from_dict (O0OO00O0OO000OO00 ,orient ="index",columns =["content"]).reset_index ()#line:3905
            O0OO00O0OO000OO00 =O0OO00O0OO000OO00 .sort_values (by ="content",ascending =[False ],na_position ="last")#line:3906
            DRAW_make_one (O0OO00O0OO000OO00 ,OO00O00O0000O000O ["条目"],"index","content","饼图")#line:3907
            return 0 #line:3908
        if "dfx_deepview"in OO00O00O0000O000O ["报表类型"]:#line:3913
            OO000O0O00OO0OO00 =eval (OO00O00O0000O000O ["报表类型"][13 :])#line:3914
            OOOOO0O0O0O00O00O =O0OO0OOOOO00O000O .copy ()#line:3915
            for OO000000000OOOO00 in OO000O0O00OO0OO00 :#line:3916
                OOOOO0O0O0O00O00O =OOOOO0O0O0O00O00O [(OOOOO0O0O0O00O00O [OO000000000OOOO00 ].astype (str )==O0000O0O00OO0000O [OO000O0O00OO0OO00 .index (OO000000000OOOO00 )])].copy ()#line:3917
            OOOOO0O0O0O00O00O ["报表类型"]="ori_dfx_deepview"#line:3918
            TABLE_tree_Level_2 (OOOOO0O0O0O00O00O ,0 ,OOOOO0O0O0O00O00O )#line:3919
            return 0 #line:3920
        if "dfx_deepvie2"in OO00O00O0000O000O ["报表类型"]:#line:3923
            OO000O0O00OO0OO00 =eval (OO00O00O0000O000O ["报表类型"][13 :])#line:3924
            OOOOO0O0O0O00O00O =O0OO0OOOOO00O000O .copy ()#line:3925
            for OO000000000OOOO00 in OO000O0O00OO0OO00 :#line:3926
                OOOOO0O0O0O00O00O =OOOOO0O0O0O00O00O [OOOOO0O0O0O00O00O [OO000000000OOOO00 ].str .contains (O0000O0O00OO0000O [OO000O0O00OO0OO00 .index (OO000000000OOOO00 )],na =False )].copy ()#line:3927
            OOOOO0O0O0O00O00O ["报表类型"]="ori_dfx_deepview"#line:3928
            TABLE_tree_Level_2 (OOOOO0O0O0O00O00O ,0 ,OOOOO0O0O0O00O00O )#line:3929
            return 0 #line:3930
        if "dfx_zhenghao"in OO00O00O0000O000O ["报表类型"]:#line:3934
            OOOOO0O0O0O00O00O =O0OO0OOOOO00O000O [(O0OO0OOOOO00O000O ["注册证编号/曾用注册证编号"]==OO00O00O0000O000O ["注册证编号/曾用注册证编号"])].copy ()#line:3935
            OOOOO0O0O0O00O00O ["报表类型"]="ori_dfx_zhenghao"#line:3936
            TABLE_tree_Level_2 (OOOOO0O0O0O00O00O ,0 ,OOOOO0O0O0O00O00O )#line:3937
            return 0 #line:3938
        if ("dfx_pihao"in OO00O00O0000O000O ["报表类型"]or "dfx_findrisk"in OO00O00O0000O000O ["报表类型"]or "dfx_xinghao"in OO00O00O0000O000O ["报表类型"]or "dfx_guige"in OO00O00O0000O000O ["报表类型"])and O00OOOO00O0O0O00O ==1 :#line:3942
            O0OO000O00OOOO0O0 ="CLT"#line:3943
            if "pihao"in OO00O00O0000O000O ["报表类型"]or "产品批号"in OO00O00O0000O000O ["报表类型"]:#line:3944
                O0OO000O00OOOO0O0 ="产品批号"#line:3945
            if "xinghao"in OO00O00O0000O000O ["报表类型"]or "型号"in OO00O00O0000O000O ["报表类型"]:#line:3946
                O0OO000O00OOOO0O0 ="型号"#line:3947
            if "guige"in OO00O00O0000O000O ["报表类型"]or "规格"in OO00O00O0000O000O ["报表类型"]:#line:3948
                O0OO000O00OOOO0O0 ="规格"#line:3949
            if "事件发生季度"in OO00O00O0000O000O ["报表类型"]:#line:3950
                O0OO000O00OOOO0O0 ="事件发生季度"#line:3951
            if "事件发生月份"in OO00O00O0000O000O ["报表类型"]:#line:3952
                O0OO000O00OOOO0O0 ="事件发生月份"#line:3953
            if "性别"in OO00O00O0000O000O ["报表类型"]:#line:3954
                O0OO000O00OOOO0O0 ="性别"#line:3955
            if "年龄段"in OO00O00O0000O000O ["报表类型"]:#line:3956
                O0OO000O00OOOO0O0 ="年龄段"#line:3957
            OOOOO0O0O0O00O00O =O0OO0OOOOO00O000O [(O0OO0OOOOO00O000O ["注册证编号/曾用注册证编号"]==OO00O00O0000O000O ["注册证编号/曾用注册证编号"])&(O0OO0OOOOO00O000O [O0OO000O00OOOO0O0 ]==OO00O00O0000O000O [O0OO000O00OOOO0O0 ])].copy ()#line:3958
            OOOOO0O0O0O00O00O ["报表类型"]="ori_pihao"#line:3959
            TABLE_tree_Level_2 (OOOOO0O0O0O00O00O ,0 ,OOOOO0O0O0O00O00O )#line:3960
            return 0 #line:3961
        if ("findrisk"in OO00O00O0000O000O ["报表类型"]or "dfx_pihao"in OO00O00O0000O000O ["报表类型"]or "dfx_xinghao"in OO00O00O0000O000O ["报表类型"]or "dfx_guige"in OO00O00O0000O000O ["报表类型"])and O00OOOO00O0O0O00O !=1 :#line:3965
            OOOOO0O0O0O00O00O =OOO0OOO0OOOOO00OO [(OOO0OOO0OOOOO00OO ["注册证编号/曾用注册证编号"]==OO00O00O0000O000O ["注册证编号/曾用注册证编号"])].copy ()#line:3966
            OOOOO0O0O0O00O00O ["报表类型"]=OO00O00O0000O000O ["报表类型"]+"1"#line:3967
            TABLE_tree_Level_2 (OOOOO0O0O0O00O00O ,1 ,O0OO0OOOOO00O000O )#line:3968
            return 0 #line:3970
        if "dfx_org监测机构"in OO00O00O0000O000O ["报表类型"]:#line:3973
            OOOOO0O0O0O00O00O =O0OO0OOOOO00O000O [(O0OO0OOOOO00O000O ["监测机构"]==OO00O00O0000O000O ["监测机构"])].copy ()#line:3974
            OOOOO0O0O0O00O00O ["报表类型"]="ori_dfx_org"#line:3975
            TABLE_tree_Level_2 (OOOOO0O0O0O00O00O ,0 ,OOOOO0O0O0O00O00O )#line:3976
            return 0 #line:3977
        if "dfx_org市级监测机构"in OO00O00O0000O000O ["报表类型"]:#line:3979
            OOOOO0O0O0O00O00O =O0OO0OOOOO00O000O [(O0OO0OOOOO00O000O ["市级监测机构"]==OO00O00O0000O000O ["市级监测机构"])].copy ()#line:3980
            OOOOO0O0O0O00O00O ["报表类型"]="ori_dfx_org"#line:3981
            TABLE_tree_Level_2 (OOOOO0O0O0O00O00O ,0 ,OOOOO0O0O0O00O00O )#line:3982
            return 0 #line:3983
        if "dfx_user"in OO00O00O0000O000O ["报表类型"]:#line:3986
            OOOOO0O0O0O00O00O =O0OO0OOOOO00O000O [(O0OO0OOOOO00O000O ["单位名称"]==OO00O00O0000O000O ["单位名称"])].copy ()#line:3987
            OOOOO0O0O0O00O00O ["报表类型"]="ori_dfx_user"#line:3988
            TABLE_tree_Level_2 (OOOOO0O0O0O00O00O ,0 ,OOOOO0O0O0O00O00O )#line:3989
            return 0 #line:3990
        if "dfx_chiyouren"in OO00O00O0000O000O ["报表类型"]:#line:3994
            OOOOO0O0O0O00O00O =O0OO0OOOOO00O000O [(O0OO0OOOOO00O000O ["上市许可持有人名称"]==OO00O00O0000O000O ["上市许可持有人名称"])].copy ()#line:3995
            OOOOO0O0O0O00O00O ["报表类型"]="ori_dfx_chiyouren"#line:3996
            TABLE_tree_Level_2 (OOOOO0O0O0O00O00O ,0 ,OOOOO0O0O0O00O00O )#line:3997
            return 0 #line:3998
        if "dfx_chanpin"in OO00O00O0000O000O ["报表类型"]:#line:4000
            OOOOO0O0O0O00O00O =O0OO0OOOOO00O000O [(O0OO0OOOOO00O000O ["产品名称"]==OO00O00O0000O000O ["产品名称"])].copy ()#line:4001
            OOOOO0O0O0O00O00O ["报表类型"]="ori_dfx_chanpin"#line:4002
            TABLE_tree_Level_2 (OOOOO0O0O0O00O00O ,0 ,OOOOO0O0O0O00O00O )#line:4003
            return 0 #line:4004
        if "dfx_findrisk事件发生季度1"in OO00O00O0000O000O ["报表类型"]:#line:4009
            OOOOO0O0O0O00O00O =O0OO0OOOOO00O000O [(O0OO0OOOOO00O000O ["注册证编号/曾用注册证编号"]==OO00O00O0000O000O ["注册证编号/曾用注册证编号"])&(O0OO0OOOOO00O000O ["事件发生季度"]==OO00O00O0000O000O ["事件发生季度"])].copy ()#line:4010
            OOOOO0O0O0O00O00O ["报表类型"]="ori_dfx_findrisk事件发生季度"#line:4011
            TABLE_tree_Level_2 (OOOOO0O0O0O00O00O ,0 ,OOOOO0O0O0O00O00O )#line:4012
            return 0 #line:4013
        if "dfx_findrisk事件发生月份1"in OO00O00O0000O000O ["报表类型"]:#line:4016
            OOOOO0O0O0O00O00O =O0OO0OOOOO00O000O [(O0OO0OOOOO00O000O ["注册证编号/曾用注册证编号"]==OO00O00O0000O000O ["注册证编号/曾用注册证编号"])&(O0OO0OOOOO00O000O ["事件发生月份"]==OO00O00O0000O000O ["事件发生月份"])].copy ()#line:4017
            OOOOO0O0O0O00O00O ["报表类型"]="ori_dfx_findrisk事件发生月份"#line:4018
            TABLE_tree_Level_2 (OOOOO0O0O0O00O00O ,0 ,OOOOO0O0O0O00O00O )#line:4019
            return 0 #line:4020
        if ("keyword_findrisk"in OO00O00O0000O000O ["报表类型"])and O00OOOO00O0O0O00O ==1 :#line:4023
            O0OO000O00OOOO0O0 ="CLT"#line:4024
            if "批号"in OO00O00O0000O000O ["报表类型"]:#line:4025
                O0OO000O00OOOO0O0 ="产品批号"#line:4026
            if "事件发生季度"in OO00O00O0000O000O ["报表类型"]:#line:4027
                O0OO000O00OOOO0O0 ="事件发生季度"#line:4028
            if "事件发生月份"in OO00O00O0000O000O ["报表类型"]:#line:4029
                O0OO000O00OOOO0O0 ="事件发生月份"#line:4030
            if "性别"in OO00O00O0000O000O ["报表类型"]:#line:4031
                O0OO000O00OOOO0O0 ="性别"#line:4032
            if "年龄段"in OO00O00O0000O000O ["报表类型"]:#line:4033
                O0OO000O00OOOO0O0 ="年龄段"#line:4034
            OOOOO0O0O0O00O00O =O0OO0OOOOO00O000O [(O0OO0OOOOO00O000O ["注册证编号/曾用注册证编号"]==OO00O00O0000O000O ["注册证编号/曾用注册证编号"])&(O0OO0OOOOO00O000O [O0OO000O00OOOO0O0 ]==OO00O00O0000O000O [O0OO000O00OOOO0O0 ])].copy ()#line:4035
            OOOOO0O0O0O00O00O ["关键字查找列"]=""#line:4036
            for O0000OO0O0OO0O0O0 in TOOLS_get_list (OO00O00O0000O000O ["关键字查找列"]):#line:4037
                OOOOO0O0O0O00O00O ["关键字查找列"]=OOOOO0O0O0O00O00O ["关键字查找列"]+OOOOO0O0O0O00O00O [O0000OO0O0OO0O0O0 ].astype ("str")#line:4038
            OOOOO0O0O0O00O00O =OOOOO0O0O0O00O00O [(OOOOO0O0O0O00O00O ["关键字查找列"].str .contains (OO00O00O0000O000O ["关键字组合"],na =False ))]#line:4039
            if str (OO00O00O0000O000O ["排除值"])!="nan":#line:4041
                OOOOO0O0O0O00O00O =OOOOO0O0O0O00O00O .loc [~OOOOO0O0O0O00O00O ["关键字查找列"].str .contains (OO00O00O0000O000O ["排除值"],na =False )]#line:4042
            OOOOO0O0O0O00O00O ["报表类型"]="ori_"+OO00O00O0000O000O ["报表类型"]#line:4044
            TABLE_tree_Level_2 (OOOOO0O0O0O00O00O ,0 ,OOOOO0O0O0O00O00O )#line:4045
            return 0 #line:4046
        if ("PSUR"in OO00O00O0000O000O ["报表类型"]):#line:4051
            OOOOO0O0O0O00O00O =O0OO0OOOOO00O000O .copy ()#line:4052
            if ini ["模式"]=="器械":#line:4053
                OOOOO0O0O0O00O00O ["关键字查找列"]=OOOOO0O0O0O00O00O ["器械故障表现"].astype (str )+OOOOO0O0O0O00O00O ["伤害表现"].astype (str )+OOOOO0O0O0O00O00O ["使用过程"].astype (str )+OOOOO0O0O0O00O00O ["事件原因分析描述"].astype (str )+OOOOO0O0O0O00O00O ["初步处置情况"].astype (str )#line:4054
            else :#line:4055
                OOOOO0O0O0O00O00O ["关键字查找列"]=OOOOO0O0O0O00O00O ["器械故障表现"]#line:4056
            if "-其他关键字-"in str (OO00O00O0000O000O ["关键字标记"]):#line:4058
                OOOOO0O0O0O00O00O =OOOOO0O0O0O00O00O .loc [~OOOOO0O0O0O00O00O ["关键字查找列"].str .contains (OO00O00O0000O000O ["关键字标记"],na =False )].copy ()#line:4059
                TABLE_tree_Level_2 (OOOOO0O0O0O00O00O ,0 ,OOOOO0O0O0O00O00O )#line:4060
                return 0 #line:4061
            OOOOO0O0O0O00O00O =OOOOO0O0O0O00O00O [(OOOOO0O0O0O00O00O ["关键字查找列"].str .contains (OO00O00O0000O000O ["关键字标记"],na =False ))]#line:4064
            if str (OO00O00O0000O000O ["排除值"])!="没有排除值":#line:4065
                OOOOO0O0O0O00O00O =OOOOO0O0O0O00O00O .loc [~OOOOO0O0O0O00O00O ["关键字查找列"].str .contains (OO00O00O0000O000O ["排除值"],na =False )]#line:4066
            TABLE_tree_Level_2 (OOOOO0O0O0O00O00O ,0 ,OOOOO0O0O0O00O00O )#line:4070
            return 0 #line:4071
        if ("ROR"in OO00O00O0000O000O ["报表类型"]):#line:4074
            OOO00OO00OO00OOOO ={'nan':"-未定义-"}#line:4075
            O00000OO0O00O0OO0 =eval (OO00O00O0000O000O ["报表定位"],OOO00OO00OO00OOOO )#line:4076
            OOOOO0O0O0O00O00O =O0OO0OOOOO00O000O .copy ()#line:4077
            for OOOO00O0OO00O0O0O ,O0O0OO0OOOO0OOOOO in O00000OO0O00O0OO0 .items ():#line:4079
                if OOOO00O0OO00O0O0O =="合并列"and O0O0OO0OOOO0OOOOO !={}:#line:4081
                    for O00O0000O000000OO ,OO00O000O0000O00O in O0O0OO0OOOO0OOOOO .items ():#line:4082
                        if OO00O000O0000O00O !="-未定义-":#line:4083
                            O00O00O0000OOO00O =TOOLS_get_list (OO00O000O0000O00O )#line:4084
                            OOOOO0O0O0O00O00O [O00O0000O000000OO ]=""#line:4085
                            for O00OOOO00000O000O in O00O00O0000OOO00O :#line:4086
                                OOOOO0O0O0O00O00O [O00O0000O000000OO ]=OOOOO0O0O0O00O00O [O00O0000O000000OO ]+OOOOO0O0O0O00O00O [O00OOOO00000O000O ].astype ("str")#line:4087
                if OOOO00O0OO00O0O0O =="等于"and O0O0OO0OOOO0OOOOO !={}:#line:4089
                    for O00O0000O000000OO ,OO00O000O0000O00O in O0O0OO0OOOO0OOOOO .items ():#line:4090
                        OOOOO0O0O0O00O00O =OOOOO0O0O0O00O00O [(OOOOO0O0O0O00O00O [O00O0000O000000OO ]==OO00O000O0000O00O )]#line:4091
                if OOOO00O0OO00O0O0O =="不等于"and O0O0OO0OOOO0OOOOO !={}:#line:4093
                    for O00O0000O000000OO ,OO00O000O0000O00O in O0O0OO0OOOO0OOOOO .items ():#line:4094
                        if OO00O000O0000O00O !="-未定义-":#line:4095
                            OOOOO0O0O0O00O00O =OOOOO0O0O0O00O00O [(OOOOO0O0O0O00O00O [O00O0000O000000OO ]!=OO00O000O0000O00O )]#line:4096
                if OOOO00O0OO00O0O0O =="包含"and O0O0OO0OOOO0OOOOO !={}:#line:4098
                    for O00O0000O000000OO ,OO00O000O0000O00O in O0O0OO0OOOO0OOOOO .items ():#line:4099
                        if OO00O000O0000O00O !="-未定义-":#line:4100
                            OOOOO0O0O0O00O00O =OOOOO0O0O0O00O00O .loc [OOOOO0O0O0O00O00O [O00O0000O000000OO ].str .contains (OO00O000O0000O00O ,na =False )]#line:4101
                if OOOO00O0OO00O0O0O =="不包含"and O0O0OO0OOOO0OOOOO !={}:#line:4103
                    for O00O0000O000000OO ,OO00O000O0000O00O in O0O0OO0OOOO0OOOOO .items ():#line:4104
                        if OO00O000O0000O00O !="-未定义-":#line:4105
                            OOOOO0O0O0O00O00O =OOOOO0O0O0O00O00O .loc [~OOOOO0O0O0O00O00O [O00O0000O000000OO ].str .contains (OO00O000O0000O00O ,na =False )]#line:4106
            TABLE_tree_Level_2 (OOOOO0O0O0O00O00O ,0 ,OOOOO0O0O0O00O00O )#line:4108
            return 0 #line:4109
    if ("关键字标记"in O000OO00O0O0O0000 ["values"])and ("该类别不良事件计数"in O000OO00O0O0O0000 ["values"]):#line:4112
            def OOO0OOOOO0O0OO0O0 (event =None ):#line:4113
                for O0O00OOOOO00OOOO0 in O00O000000000O000 .selection ():#line:4114
                    OO00000000OOOO000 =O00O000000000O000 .item (O0O00OOOOO00OOOO0 ,"values")#line:4115
                OO0OO000OOO0OO000 =dict (zip (OOOO00O0000O0000O ,OO00000000OOOO000 ))#line:4116
                OOO0OOO000OOO00OO =OO00O0O0O00OO00O0 .copy ()#line:4117
                if ini ["模式"]=="器械":#line:4118
                    OOO0OOO000OOO00OO ["关键字查找列"]=OOO0OOO000OOO00OO ["器械故障表现"].astype (str )+OOO0OOO000OOO00OO ["伤害表现"].astype (str )+OOO0OOO000OOO00OO ["使用过程"].astype (str )+OOO0OOO000OOO00OO ["事件原因分析描述"].astype (str )+OOO0OOO000OOO00OO ["初步处置情况"].astype (str )#line:4119
                else :#line:4120
                    OOO0OOO000OOO00OO ["关键字查找列"]=OOO0OOO000OOO00OO ["器械故障表现"]#line:4121
                if "-其他关键字-"in str (OO0OO000OOO0OO000 ["关键字标记"]):#line:4122
                    OOO0OOO000OOO00OO =OOO0OOO000OOO00OO .loc [~OOO0OOO000OOO00OO ["关键字查找列"].str .contains (OO0OO000OOO0OO000 ["关键字标记"],na =False )].copy ()#line:4123
                OOO0OOO000OOO00OO =OOO0OOO000OOO00OO [(OOO0OOO000OOO00OO ["关键字查找列"].str .contains (OO0OO000OOO0OO000 ["关键字标记"],na =False ))]#line:4125
                if str (OO0OO000OOO0OO000 ["排除值"])!="没有排除值":#line:4126
                    OOO0OOO000OOO00OO =OOO0OOO000OOO00OO .loc [~OOO0OOO000OOO00OO ["关键字查找列"].str .contains (OO0OO000OOO0OO000 ["排除值"],na =False )]#line:4127
                O00OO0000O0OOOO0O =TOOLS_count_elements (OOO0OOO000OOO00OO ,OO0OO000OOO0OO000 ["关键字标记"],"关键字查找列")#line:4128
                O00OO0000O0OOOO0O =O00OO0000O0OOOO0O .sort_values (by ="计数",ascending =[False ],na_position ="last").reset_index (drop =True )#line:4129
                TABLE_tree_Level_2 (O00OO0000O0OOOO0O ,1 ,OOO0OOO000OOO00OO )#line:4130
            O0OO0OOO0000O0OO0 =Menu (O00000OO0OO000OOO ,tearoff =False ,)#line:4131
            O0OO0OOO0000O0OO0 .add_command (label ="表现具体细项",command =OOO0OOOOO0O0OO0O0 )#line:4132
            def O0OO0O000OO00O0OO (OO00000000OO00O0O ):#line:4133
                O0OO0OOO0000O0OO0 .post (OO00000000OO00O0O .x_root ,OO00000000OO00O0O .y_root )#line:4134
            O00000OO0OO000OOO .bind ("<Button-3>",O0OO0O000OO00O0OO )#line:4135
    try :#line:4139
        if O0O00000O000OO0O0 [1 ]=="dfx_zhenghao":#line:4140
            OO0O00O0O0OOOOO0O ="dfx_zhenghao"#line:4141
            OO0000OO0O00O0000 =""#line:4142
    except :#line:4143
            OO0O00O0O0OOOOO0O =""#line:4144
            OO0000OO0O00O0000 ="近一年"#line:4145
    if (("总体评分"in O000OO00O0O0O0000 ["values"])and ("高峰批号均值"in O000OO00O0O0O0000 ["values"])and ("月份均值"in O000OO00O0O0O0000 ["values"]))or OO0O00O0O0OOOOO0O =="dfx_zhenghao":#line:4147
            def OO00OO000OO0OO000 (event =None ):#line:4150
                for OOO00O0OO0O0O0OO0 in O00O000000000O000 .selection ():#line:4151
                    O00O00O0O0O0000OO =O00O000000000O000 .item (OOO00O0OO0O0O0OO0 ,"values")#line:4152
                O00000OO0O0OOOO00 =dict (zip (OOOO00O0000O0000O ,O00O00O0O0O0000OO ))#line:4153
                O000OO00O000O00OO =OO00O0O0O00OO00O0 [(OO00O0O0O00OO00O0 ["注册证编号/曾用注册证编号"]==O00000OO0O0OOOO00 ["注册证编号/曾用注册证编号"])].copy ()#line:4154
                O000OO00O000O00OO ["报表类型"]=O00000OO0O0OOOO00 ["报表类型"]+"1"#line:4155
                TABLE_tree_Level_2 (O000OO00O000O00OO ,1 ,OO00O0O0O00OO00O0 )#line:4156
            def O00OOO0O000OO00O0 (event =None ):#line:4157
                for OOO0OO00O0O0O0000 in O00O000000000O000 .selection ():#line:4158
                    OOOOOOO0000000O0O =O00O000000000O000 .item (OOO0OO00O0O0O0000 ,"values")#line:4159
                OOOO0O0000OO00OOO =dict (zip (OOOO00O0000O0000O ,OOOOOOO0000000O0O ))#line:4160
                O000O00O0OO0000O0 =O0O00000O000OO0O0 [0 ][(O0O00000O000OO0O0 [0 ]["注册证编号/曾用注册证编号"]==OOOO0O0000OO00OOO ["注册证编号/曾用注册证编号"])].copy ()#line:4161
                O000O00O0OO0000O0 ["报表类型"]=OOOO0O0000OO00OOO ["报表类型"]+"1"#line:4162
                TABLE_tree_Level_2 (O000O00O0OO0000O0 ,1 ,O0O00000O000OO0O0 [0 ])#line:4163
            def OO0O00O000O0O000O (OO0O0000000OOOO00 ):#line:4164
                for O0O0OOO0OO0OO0000 in O00O000000000O000 .selection ():#line:4165
                    OO0000OO00000OOOO =O00O000000000O000 .item (O0O0OOO0OO0OO0000 ,"values")#line:4166
                O000O0O000O0O000O =dict (zip (OOOO00O0000O0000O ,OO0000OO00000OOOO ))#line:4167
                OOOOOO0OO0000000O =OO00O0O0O00OO00O0 [(OO00O0O0O00OO00O0 ["注册证编号/曾用注册证编号"]==O000O0O000O0O000O ["注册证编号/曾用注册证编号"])].copy ()#line:4170
                OOOOOO0OO0000000O ["报表类型"]=O000O0O000O0O000O ["报表类型"]+"1"#line:4171
                OOOO0OO000O0OOOOO =Countall (OOOOOO0OO0000000O ).df_psur (OO0O0000000OOOO00 ,O000O0O000O0O000O ["规整后品类"])[["关键字标记","总数量","严重比"]]#line:4172
                OOOO0OO000O0OOOOO =OOOO0OO000O0OOOOO .rename (columns ={"总数量":"最近30天总数量"})#line:4173
                OOOO0OO000O0OOOOO =OOOO0OO000O0OOOOO .rename (columns ={"严重比":"最近30天严重比"})#line:4174
                OOOOOO0OO0000000O =O0O00000O000OO0O0 [0 ][(O0O00000O000OO0O0 [0 ]["注册证编号/曾用注册证编号"]==O000O0O000O0O000O ["注册证编号/曾用注册证编号"])].copy ()#line:4176
                OOOOOO0OO0000000O ["报表类型"]=O000O0O000O0O000O ["报表类型"]+"1"#line:4177
                OO00OO0O00OOOO0O0 =Countall (OOOOOO0OO0000000O ).df_psur (OO0O0000000OOOO00 ,O000O0O000O0O000O ["规整后品类"])#line:4178
                O0000O0O0OO0000O0 =pd .merge (OO00OO0O00OOOO0O0 ,OOOO0OO000O0OOOOO ,on ="关键字标记",how ="left")#line:4180
                del O0000O0O0OO0000O0 ["报表类型"]#line:4181
                O0000O0O0OO0000O0 ["报表类型"]="PSUR"#line:4182
                TABLE_tree_Level_2 (O0000O0O0OO0000O0 ,1 ,OOOOOO0OO0000000O )#line:4184
            def OOOO0O000O00O0O0O (OO0O0OOO0O000OO0O ):#line:4187
                for O0O0O0OOOO00O0O00 in O00O000000000O000 .selection ():#line:4188
                    O0000OO0OOOOOOO00 =O00O000000000O000 .item (O0O0O0OOOO00O0O00 ,"values")#line:4189
                O0OO00OO0000OO00O =dict (zip (OOOO00O0000O0000O ,O0000OO0OOOOOOO00 ))#line:4190
                OOO0O00OO000O0OOO =O0O00000O000OO0O0 [0 ]#line:4191
                if O0OO00OO0000OO00O ["规整后品类"]=="N":#line:4192
                    if OO0O0OOO0O000OO0O =="特定品种":#line:4193
                        showinfo (title ="关于",message ="未能适配该品种规则，可能未制定或者数据规整不完善。")#line:4194
                        return 0 #line:4195
                    OOO0O00OO000O0OOO =OOO0O00OO000O0OOO .loc [OOO0O00OO000O0OOO ["产品名称"].str .contains (O0OO00OO0000OO00O ["产品名称"],na =False )].copy ()#line:4196
                else :#line:4197
                    OOO0O00OO000O0OOO =OOO0O00OO000O0OOO .loc [OOO0O00OO000O0OOO ["规整后品类"].str .contains (O0OO00OO0000OO00O ["规整后品类"],na =False )].copy ()#line:4198
                OOO0O00OO000O0OOO =OOO0O00OO000O0OOO .loc [OOO0O00OO000O0OOO ["产品类别"].str .contains (O0OO00OO0000OO00O ["产品类别"],na =False )].copy ()#line:4199
                OOO0O00OO000O0OOO ["报表类型"]=O0OO00OO0000OO00O ["报表类型"]+"1"#line:4201
                if OO0O0OOO0O000OO0O =="特定品种":#line:4202
                    TABLE_tree_Level_2 (Countall (OOO0O00OO000O0OOO ).df_ror (["产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"],O0OO00OO0000OO00O ["规整后品类"],O0OO00OO0000OO00O ["注册证编号/曾用注册证编号"]),1 ,OOO0O00OO000O0OOO )#line:4203
                else :#line:4204
                    TABLE_tree_Level_2 (Countall (OOO0O00OO000O0OOO ).df_ror (["产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"],OO0O0OOO0O000OO0O ,O0OO00OO0000OO00O ["注册证编号/曾用注册证编号"]),1 ,OOO0O00OO000O0OOO )#line:4205
            def O000O00OO000O0000 (event =None ):#line:4207
                for O0OO0O00OO000O0O0 in O00O000000000O000 .selection ():#line:4208
                    O000O00O0O000O00O =O00O000000000O000 .item (O0OO0O00OO000O0O0 ,"values")#line:4209
                OOO00OO00OOOO0000 =dict (zip (OOOO00O0000O0000O ,O000O00O0O000O00O ))#line:4210
                O000O000000O0OO0O =O0O00000O000OO0O0 [0 ][(O0O00000O000OO0O0 [0 ]["注册证编号/曾用注册证编号"]==OOO00OO00OOOO0000 ["注册证编号/曾用注册证编号"])].copy ()#line:4211
                O000O000000O0OO0O ["报表类型"]=OOO00OO00OOOO0000 ["报表类型"]+"1"#line:4212
                TABLE_tree_Level_2 (Countall (O000O000000O0OO0O ).df_pihao (),1 ,O000O000000O0OO0O ,)#line:4217
            def O0OO000000OOO00OO (event =None ):#line:4219
                for OO00O0000OOOOO000 in O00O000000000O000 .selection ():#line:4220
                    O00O0OOO0000OOO0O =O00O000000000O000 .item (OO00O0000OOOOO000 ,"values")#line:4221
                O00OO0O0OOOO00O00 =dict (zip (OOOO00O0000O0000O ,O00O0OOO0000OOO0O ))#line:4222
                OOO00O0O0O00000O0 =O0O00000O000OO0O0 [0 ][(O0O00000O000OO0O0 [0 ]["注册证编号/曾用注册证编号"]==O00OO0O0OOOO00O00 ["注册证编号/曾用注册证编号"])].copy ()#line:4223
                OOO00O0O0O00000O0 ["报表类型"]=O00OO0O0OOOO00O00 ["报表类型"]+"1"#line:4224
                TABLE_tree_Level_2 (Countall (OOO00O0O0O00000O0 ).df_xinghao (),1 ,OOO00O0O0O00000O0 ,)#line:4229
            def OOO000000000000OO (event =None ):#line:4231
                for O00O00O0OO0O0O000 in O00O000000000O000 .selection ():#line:4232
                    O0OOOO000O000OO00 =O00O000000000O000 .item (O00O00O0OO0O0O000 ,"values")#line:4233
                OOO00OOO00000OO0O =dict (zip (OOOO00O0000O0000O ,O0OOOO000O000OO00 ))#line:4234
                OO00000OO00OOOO00 =O0O00000O000OO0O0 [0 ][(O0O00000O000OO0O0 [0 ]["注册证编号/曾用注册证编号"]==OOO00OOO00000OO0O ["注册证编号/曾用注册证编号"])].copy ()#line:4235
                OO00000OO00OOOO00 ["报表类型"]=OOO00OOO00000OO0O ["报表类型"]+"1"#line:4236
                TABLE_tree_Level_2 (Countall (OO00000OO00OOOO00 ).df_user (),1 ,OO00000OO00OOOO00 ,)#line:4241
            def O00OO00O000OO0000 (event =None ):#line:4243
                for O0OOOO0OO00OOO0O0 in O00O000000000O000 .selection ():#line:4245
                    OO00O00OOO0000O00 =O00O000000000O000 .item (O0OOOO0OO00OOO0O0 ,"values")#line:4246
                OOO000OOOO00O000O =dict (zip (OOOO00O0000O0000O ,OO00O00OOO0000O00 ))#line:4247
                O00OO00OO0OO00O0O =O0O00000O000OO0O0 [0 ][(O0O00000O000OO0O0 [0 ]["注册证编号/曾用注册证编号"]==OOO000OOOO00O000O ["注册证编号/曾用注册证编号"])].copy ()#line:4248
                O00OO00OO0OO00O0O ["报表类型"]=OOO000OOOO00O000O ["报表类型"]+"1"#line:4249
                OOOO0OO0OO000O0OO =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name =0 ).reset_index (drop =True )#line:4250
                if ini ["模式"]=="药品":#line:4251
                    OOOO0OO0OO000O0OO =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="药品").reset_index (drop =True )#line:4252
                if ini ["模式"]=="器械":#line:4253
                    OOOO0OO0OO000O0OO =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="器械").reset_index (drop =True )#line:4254
                if ini ["模式"]=="化妆品":#line:4255
                    OOOO0OO0OO000O0OO =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="化妆品").reset_index (drop =True )#line:4256
                O0O0000OOO0O0000O =OOOO0OO0OO000O0OO ["值"][3 ]+"|"+OOOO0OO0OO000O0OO ["值"][4 ]#line:4257
                if ini ["模式"]=="器械":#line:4258
                    O00OO00OO0OO00O0O ["关键字查找列"]=O00OO00OO0OO00O0O ["器械故障表现"].astype (str )+O00OO00OO0OO00O0O ["伤害表现"].astype (str )+O00OO00OO0OO00O0O ["使用过程"].astype (str )+O00OO00OO0OO00O0O ["事件原因分析描述"].astype (str )+O00OO00OO0OO00O0O ["初步处置情况"].astype (str )#line:4259
                else :#line:4260
                    O00OO00OO0OO00O0O ["关键字查找列"]=O00OO00OO0OO00O0O ["器械故障表现"].astype (str )#line:4261
                O00OO00OO0OO00O0O =O00OO00OO0OO00O0O .loc [O00OO00OO0OO00O0O ["关键字查找列"].str .contains (O0O0000OOO0O0000O ,na =False )].copy ().reset_index (drop =True )#line:4262
                TABLE_tree_Level_2 (O00OO00OO0OO00O0O ,0 ,O00OO00OO0OO00O0O ,)#line:4268
            def O0O0O0O0O000OOO0O (event =None ):#line:4271
                for OO00OO0OO0OOO00O0 in O00O000000000O000 .selection ():#line:4272
                    O0OOOOO0O0O0O00OO =O00O000000000O000 .item (OO00OO0OO0OOO00O0 ,"values")#line:4273
                OOO000OOO0O0O00OO =dict (zip (OOOO00O0000O0000O ,O0OOOOO0O0O0O00OO ))#line:4274
                OOOOO00O00000OOO0 =O0O00000O000OO0O0 [0 ][(O0O00000O000OO0O0 [0 ]["注册证编号/曾用注册证编号"]==OOO000OOO0O0O00OO ["注册证编号/曾用注册证编号"])].copy ()#line:4275
                OOOOO00O00000OOO0 ["报表类型"]=OOO000OOO0O0O00OO ["报表类型"]+"1"#line:4276
                TOOLS_time (OOOOO00O00000OOO0 ,"事件发生日期",0 )#line:4277
            def OOOO00OOOOO0O0OO0 (OOOOOOOOO0OO0OOOO ,O00OO0O0000OOO000 ):#line:4279
                for O0O0000000O00O000 in O00O000000000O000 .selection ():#line:4281
                    OOO0O0OO00OO0000O =O00O000000000O000 .item (O0O0000000O00O000 ,"values")#line:4282
                OO0OO00OOO000OO00 =dict (zip (OOOO00O0000O0000O ,OOO0O0OO00OO0000O ))#line:4283
                O00O0OO0O0O00OO0O =O0O00000O000OO0O0 [0 ]#line:4284
                if OO0OO00OOO000OO00 ["规整后品类"]=="N":#line:4285
                    if OOOOOOOOO0OO0OOOO =="特定品种":#line:4286
                        showinfo (title ="关于",message ="未能适配该品种规则，可能未制定或者数据规整不完善。")#line:4287
                        return 0 #line:4288
                O00O0OO0O0O00OO0O =O00O0OO0O0O00OO0O .loc [O00O0OO0O0O00OO0O ["注册证编号/曾用注册证编号"].str .contains (OO0OO00OOO000OO00 ["注册证编号/曾用注册证编号"],na =False )].copy ()#line:4289
                O00O0OO0O0O00OO0O ["报表类型"]=OO0OO00OOO000OO00 ["报表类型"]+"1"#line:4290
                if OOOOOOOOO0OO0OOOO =="特定品种":#line:4291
                    TABLE_tree_Level_2 (Countall (O00O0OO0O0O00OO0O ).df_find_all_keword_risk (O00OO0O0000OOO000 ,OO0OO00OOO000OO00 ["规整后品类"]),1 ,O00O0OO0O0O00OO0O )#line:4292
                else :#line:4293
                    TABLE_tree_Level_2 (Countall (O00O0OO0O0O00OO0O ).df_find_all_keword_risk (O00OO0O0000OOO000 ,OOOOOOOOO0OO0OOOO ),1 ,O00O0OO0O0O00OO0O )#line:4294
            O0OO0OOO0000O0OO0 =Menu (O00000OO0OO000OOO ,tearoff =False ,)#line:4298
            O0OO0OOO0000O0OO0 .add_command (label =OO0000OO0O00O0000 +"故障表现分类（无源）",command =lambda :OO0O00O000O0O000O ("通用无源"))#line:4299
            O0OO0OOO0000O0OO0 .add_command (label =OO0000OO0O00O0000 +"故障表现分类（有源）",command =lambda :OO0O00O000O0O000O ("通用有源"))#line:4300
            O0OO0OOO0000O0OO0 .add_command (label =OO0000OO0O00O0000 +"故障表现分类（特定品种）",command =lambda :OO0O00O000O0O000O ("特定品种"))#line:4301
            O0OO0OOO0000O0OO0 .add_separator ()#line:4303
            if OO0O00O0O0OOOOO0O =="":#line:4304
                O0OO0OOO0000O0OO0 .add_command (label =OO0000OO0O00O0000 +"同类比较(ROR-无源)",command =lambda :OOOO0O000O00O0O0O ("无源"))#line:4305
                O0OO0OOO0000O0OO0 .add_command (label =OO0000OO0O00O0000 +"同类比较(ROR-有源)",command =lambda :OOOO0O000O00O0O0O ("有源"))#line:4306
                O0OO0OOO0000O0OO0 .add_command (label =OO0000OO0O00O0000 +"同类比较(ROR-特定品种)",command =lambda :OOOO0O000O00O0O0O ("特定品种"))#line:4307
            O0OO0OOO0000O0OO0 .add_separator ()#line:4309
            O0OO0OOO0000O0OO0 .add_command (label =OO0000OO0O00O0000 +"关键字趋势(批号-无源)",command =lambda :OOOO00OOOOO0O0OO0 ("无源","产品批号"))#line:4310
            O0OO0OOO0000O0OO0 .add_command (label =OO0000OO0O00O0000 +"关键字趋势(批号-特定品种)",command =lambda :OOOO00OOOOO0O0OO0 ("特定品种","产品批号"))#line:4311
            O0OO0OOO0000O0OO0 .add_command (label =OO0000OO0O00O0000 +"关键字趋势(月份-无源)",command =lambda :OOOO00OOOOO0O0OO0 ("无源","事件发生月份"))#line:4312
            O0OO0OOO0000O0OO0 .add_command (label =OO0000OO0O00O0000 +"关键字趋势(月份-有源)",command =lambda :OOOO00OOOOO0O0OO0 ("有源","事件发生月份"))#line:4313
            O0OO0OOO0000O0OO0 .add_command (label =OO0000OO0O00O0000 +"关键字趋势(月份-特定品种)",command =lambda :OOOO00OOOOO0O0OO0 ("特定品种","事件发生月份"))#line:4314
            O0OO0OOO0000O0OO0 .add_command (label =OO0000OO0O00O0000 +"关键字趋势(季度-无源)",command =lambda :OOOO00OOOOO0O0OO0 ("无源","事件发生季度"))#line:4315
            O0OO0OOO0000O0OO0 .add_command (label =OO0000OO0O00O0000 +"关键字趋势(季度-有源)",command =lambda :OOOO00OOOOO0O0OO0 ("有源","事件发生季度"))#line:4316
            O0OO0OOO0000O0OO0 .add_command (label =OO0000OO0O00O0000 +"关键字趋势(季度-特定品种)",command =lambda :OOOO00OOOOO0O0OO0 ("特定品种","事件发生季度"))#line:4317
            O0OO0OOO0000O0OO0 .add_separator ()#line:4319
            O0OO0OOO0000O0OO0 .add_command (label =OO0000OO0O00O0000 +"各批号报送情况",command =O000O00OO000O0000 )#line:4320
            O0OO0OOO0000O0OO0 .add_command (label =OO0000OO0O00O0000 +"各型号报送情况",command =O0OO000000OOO00OO )#line:4321
            O0OO0OOO0000O0OO0 .add_command (label =OO0000OO0O00O0000 +"报告单位情况",command =OOO000000000000OO )#line:4322
            O0OO0OOO0000O0OO0 .add_command (label =OO0000OO0O00O0000 +"事件发生时间曲线",command =O0O0O0O0O000OOO0O )#line:4323
            O0OO0OOO0000O0OO0 .add_separator ()#line:4324
            O0OO0OOO0000O0OO0 .add_command (label =OO0000OO0O00O0000 +"原始数据",command =O00OOO0O000OO00O0 )#line:4325
            if OO0O00O0O0OOOOO0O =="":#line:4326
                O0OO0OOO0000O0OO0 .add_command (label ="近30天原始数据",command =OO00OO000OO0OO000 )#line:4327
            O0OO0OOO0000O0OO0 .add_command (label =OO0000OO0O00O0000 +"高度关注(一级和二级)",command =O00OO00O000OO0000 )#line:4328
            def O0OO0O000OO00O0OO (O0O0OOOOO0O0OOOOO ):#line:4330
                O0OO0OOO0000O0OO0 .post (O0O0OOOOO0O0OOOOO .x_root ,O0O0OOOOO0O0OOOOO .y_root )#line:4331
            O00000OO0OO000OOO .bind ("<Button-3>",O0OO0O000OO00O0OO )#line:4332
    if O0OO000O0OOOO00OO ==0 or "规整编码"in OOO0OOO0OOOOO00OO .columns :#line:4335
        O00O000000000O000 .bind ("<Double-1>",lambda O00OO00O00O0O0O00 :OOO0OOOOOO00OO00O (O00OO00O00O0O0O00 ,OOO0OOO0OOOOO00OO ))#line:4336
    if O0OO000O0OOOO00OO ==1 and "规整编码"not in OOO0OOO0OOOOO00OO .columns :#line:4337
        O00O000000000O000 .bind ("<Double-1>",lambda OO000000OOOO00OOO :O0O0O00O00000OO00 (OO000000OOOO00OOO ,OOOO00O0000O0000O ,OO00O0O0O00OO00O0 ))#line:4338
    def OO0OOOOOOOO0O0O00 (O0OOOOOOOOO00O000 ,O0O00O0O00O0O0000 ,O0O00OOO0OOOOO000 ):#line:4341
        OO0000OOOOOO0OOOO =[(O0OOOOOOOOO00O000 .set (OOOO0000OO0OO0OO0 ,O0O00O0O00O0O0000 ),OOOO0000OO0OO0OO0 )for OOOO0000OO0OO0OO0 in O0OOOOOOOOO00O000 .get_children ("")]#line:4342
        OO0000OOOOOO0OOOO .sort (reverse =O0O00OOO0OOOOO000 )#line:4343
        for O0O00000000OO0000 ,(O0O00O0OOOOO0O00O ,O0O00OOO0O0OO00O0 )in enumerate (OO0000OOOOOO0OOOO ):#line:4345
            O0OOOOOOOOO00O000 .move (O0O00OOO0O0OO00O0 ,"",O0O00000000OO0000 )#line:4346
        O0OOOOOOOOO00O000 .heading (O0O00O0O00O0O0000 ,command =lambda :OO0OOOOOOOO0O0O00 (O0OOOOOOOOO00O000 ,O0O00O0O00O0O0000 ,not O0O00OOO0OOOOO000 ))#line:4349
    for OOOOOOO00000O0OOO in OOOO00O0000O0000O :#line:4351
        O00O000000000O000 .heading (OOOOOOO00000O0OOO ,text =OOOOOOO00000O0OOO ,command =lambda _col =OOOOOOO00000O0OOO :OO0OOOOOOOO0O0O00 (O00O000000000O000 ,_col ,False ),)#line:4356
    def OOO0OOOOOO00OO00O (OO0000O0OOO0O000O ,O00OOO0O00OO000O0 ):#line:4360
        if "规整编码"in O00OOO0O00OO000O0 .columns :#line:4362
            O00OOO0O00OO000O0 =O00OOO0O00OO000O0 .rename (columns ={"规整编码":"报告编码"})#line:4363
        for O000O00O0O00O0OOO in O00O000000000O000 .selection ():#line:4365
            O00O0000O00OO0OOO =O00O000000000O000 .item (O000O00O0O00O0OOO ,"values")#line:4366
            O0O000000OO0O0OO0 =Toplevel ()#line:4369
            OO00OOOOO00O00O0O =O0O000000OO0O0OO0 .winfo_screenwidth ()#line:4371
            OOO000O000OOOOO00 =O0O000000OO0O0OO0 .winfo_screenheight ()#line:4373
            OO00OO00OOO000OO0 =800 #line:4375
            OOOO0000O0O000OOO =600 #line:4376
            O00O000O0O000OO00 =(OO00OOOOO00O00O0O -OO00OO00OOO000OO0 )/2 #line:4378
            OOOOO0OOOO0O0OO0O =(OOO000O000OOOOO00 -OOOO0000O0O000OOO )/2 #line:4379
            O0O000000OO0O0OO0 .geometry ("%dx%d+%d+%d"%(OO00OO00OOO000OO0 ,OOOO0000O0O000OOO ,O00O000O0O000OO00 ,OOOOO0OOOO0O0OO0O ))#line:4380
            O0O0000OO0O0O00OO =ScrolledText (O0O000000OO0O0OO0 ,height =1100 ,width =1100 ,bg ="#FFFFFF")#line:4384
            O0O0000OO0O0O00OO .pack (padx =10 ,pady =10 )#line:4385
            def O00OOO00OOO0OOOO0 (event =None ):#line:4386
                O0O0000OO0O0O00OO .event_generate ('<<Copy>>')#line:4387
            def O0O0OO0OOO000O0OO (OOO0O0O0000OO0OO0 ,OO0OOO0000OOO000O ):#line:4388
                TOOLS_savetxt (OOO0O0O0000OO0OO0 ,OO0OOO0000OOO000O ,1 )#line:4389
            O00OO0O000000O00O =Menu (O0O0000OO0O0O00OO ,tearoff =False ,)#line:4390
            O00OO0O000000O00O .add_command (label ="复制",command =O00OOO00OOO0OOOO0 )#line:4391
            O00OO0O000000O00O .add_command (label ="导出",command =lambda :PROGRAM_thread_it (O0O0OO0OOO000O0OO ,O0O0000OO0O0O00OO .get (1.0 ,'end'),filedialog .asksaveasfilename (title =u"保存文件",initialfile =O00OOO0O00OO000O0 .iloc [0 ,0 ],defaultextension ="txt",filetypes =[("txt","*.txt")])))#line:4392
            def O0OOO00O00000OO00 (O000O0O0O00OOOOO0 ):#line:4394
                O00OO0O000000O00O .post (O000O0O0O00OOOOO0 .x_root ,O000O0O0O00OOOOO0 .y_root )#line:4395
            O0O0000OO0O0O00OO .bind ("<Button-3>",O0OOO00O00000OO00 )#line:4396
            try :#line:4398
                O0O000000OO0O0OO0 .title (str (O00O0000O00OO0OOO [0 ]))#line:4399
                O00OOO0O00OO000O0 ["报告编码"]=O00OOO0O00OO000O0 ["报告编码"].astype ("str")#line:4400
                O00O0O000000O000O =O00OOO0O00OO000O0 [(O00OOO0O00OO000O0 ["报告编码"]==str (O00O0000O00OO0OOO [0 ]))]#line:4401
            except :#line:4402
                pass #line:4403
            O0000000OOOOOO00O =O00OOO0O00OO000O0 .columns .values .tolist ()#line:4405
            for OO0OOOO00OO0O000O in range (len (O0000000OOOOOO00O )):#line:4406
                try :#line:4408
                    if O0000000OOOOOO00O [OO0OOOO00OO0O000O ]=="报告编码.1":#line:4409
                        O0O0000OO0O0O00OO .insert (END ,"\n\n")#line:4410
                    if O0000000OOOOOO00O [OO0OOOO00OO0O000O ]=="产品名称":#line:4411
                        O0O0000OO0O0O00OO .insert (END ,"\n\n")#line:4412
                    if O0000000OOOOOO00O [OO0OOOO00OO0O000O ]=="事件发生日期":#line:4413
                        O0O0000OO0O0O00OO .insert (END ,"\n\n")#line:4414
                    if O0000000OOOOOO00O [OO0OOOO00OO0O000O ]=="是否开展了调查":#line:4415
                        O0O0000OO0O0O00OO .insert (END ,"\n\n")#line:4416
                    if O0000000OOOOOO00O [OO0OOOO00OO0O000O ]=="市级监测机构":#line:4417
                        O0O0000OO0O0O00OO .insert (END ,"\n\n")#line:4418
                    if O0000000OOOOOO00O [OO0OOOO00OO0O000O ]=="上报机构描述":#line:4419
                        O0O0000OO0O0O00OO .insert (END ,"\n\n")#line:4420
                    if O0000000OOOOOO00O [OO0OOOO00OO0O000O ]=="持有人处理描述":#line:4421
                        O0O0000OO0O0O00OO .insert (END ,"\n\n")#line:4422
                    if OO0OOOO00OO0O000O >1 and O0000000OOOOOO00O [OO0OOOO00OO0O000O -1 ]=="持有人处理描述":#line:4423
                        O0O0000OO0O0O00OO .insert (END ,"\n\n")#line:4424
                except :#line:4426
                    pass #line:4427
                try :#line:4428
                    if O0000000OOOOOO00O [OO0OOOO00OO0O000O ]in ["单位名称","产品名称ori","上报机构描述","持有人处理描述","产品名称","注册证编号/曾用注册证编号","型号","规格","产品批号","上市许可持有人名称ori","上市许可持有人名称","伤害","伤害表现","器械故障表现","使用过程","事件原因分析描述","初步处置情况","调查情况","关联性评价","事件原因分析.1","具体控制措施"]:#line:4429
                        O0O0000OO0O0O00OO .insert (END ,"●")#line:4430
                except :#line:4431
                    pass #line:4432
                O0O0000OO0O0O00OO .insert (END ,O0000000OOOOOO00O [OO0OOOO00OO0O000O ])#line:4433
                O0O0000OO0O0O00OO .insert (END ,"：")#line:4434
                try :#line:4435
                    O0O0000OO0O0O00OO .insert (END ,O00O0O000000O000O .iloc [0 ,OO0OOOO00OO0O000O ])#line:4436
                except :#line:4437
                    O0O0000OO0O0O00OO .insert (END ,O00O0000O00OO0OOO [OO0OOOO00OO0O000O ])#line:4438
                O0O0000OO0O0O00OO .insert (END ,"\n")#line:4439
            O0O0000OO0O0O00OO .config (state =DISABLED )#line:4440
    O00O000000000O000 .pack ()#line:4442
def TOOLS_get_guize2 (OO0O000OO00000O0O ):#line:4445
	""#line:4446
	O000OOOO0OOO0OO00 =peizhidir +"0（范例）比例失衡关键字库.xls"#line:4447
	OOO00O0OO00000O00 =pd .read_excel (O000OOOO0OOO0OO00 ,header =0 ,sheet_name ="器械")#line:4448
	O0000O00O0O0O00OO =OOO00O0OO00000O00 [["适用范围列","适用范围"]].drop_duplicates ("适用范围")#line:4449
	text .insert (END ,O0000O00O0O0O00OO )#line:4450
	text .see (END )#line:4451
	O0O00OOOOOOOOOO0O =Toplevel ()#line:4452
	O0O00OOOOOOOOOO0O .title ('切换通用规则')#line:4453
	O00O000O0OOO0O00O =O0O00OOOOOOOOOO0O .winfo_screenwidth ()#line:4454
	OO000O0O00O00000O =O0O00OOOOOOOOOO0O .winfo_screenheight ()#line:4456
	O0O0O0O0OOO0O0O00 =450 #line:4458
	O0O000OOOOOOOOOOO =100 #line:4459
	O0O00OOO00O000O0O =(O00O000O0OOO0O00O -O0O0O0O0OOO0O0O00 )/2 #line:4461
	OOO0OOOO000OOO0O0 =(OO000O0O00O00000O -O0O000OOOOOOOOOOO )/2 #line:4462
	O0O00OOOOOOOOOO0O .geometry ("%dx%d+%d+%d"%(O0O0O0O0OOO0O0O00 ,O0O000OOOOOOOOOOO ,O0O00OOO00O000O0O ,OOO0OOOO000OOO0O0 ))#line:4463
	OOOOO0OO0O0000OOO =Label (O0O00OOOOOOOOOO0O ,text ="查找位置：器械故障表现+伤害表现+使用过程+事件原因分析描述+初步处置情况")#line:4464
	OOOOO0OO0O0000OOO .pack ()#line:4465
	O000OO0O0OO00OO0O =Label (O0O00OOOOOOOOOO0O ,text ="请选择您所需要的通用规则关键字：")#line:4466
	O000OO0O0OO00OO0O .pack ()#line:4467
	def OOO0O000O0O00O0O0 (*O0O0O00OOOOOOOOO0 ):#line:4468
		O00OO00O000O00O0O .set (OOOO000OOOOOO00OO .get ())#line:4469
	O00OO00O000O00O0O =StringVar ()#line:4470
	OOOO000OOOOOO00OO =ttk .Combobox (O0O00OOOOOOOOOO0O ,width =14 ,height =30 ,state ="readonly",textvariable =O00OO00O000O00O0O )#line:4471
	OOOO000OOOOOO00OO ["values"]=O0000O00O0O0O00OO ["适用范围"].to_list ()#line:4472
	OOOO000OOOOOO00OO .current (0 )#line:4473
	OOOO000OOOOOO00OO .bind ("<<ComboboxSelected>>",OOO0O000O0O00O0O0 )#line:4474
	OOOO000OOOOOO00OO .pack ()#line:4475
	OO000OO00000O0OOO =LabelFrame (O0O00OOOOOOOOOO0O )#line:4478
	OOO0OOO0OO0000000 =Button (OO000OO00000O0OOO ,text ="确定",width =10 ,command =lambda :O0OOO0O0O000O00O0 (OOO00O0OO00000O00 ,O00OO00O000O00O0O .get ()))#line:4479
	OOO0OOO0OO0000000 .pack (side =LEFT ,padx =1 ,pady =1 )#line:4480
	OO000OO00000O0OOO .pack ()#line:4481
	def O0OOO0O0O000O00O0 (O0OO0O00O00OO0OO0 ,O00OOOOO0OO0OO000 ):#line:4483
		OOO0OOO00O0000O00 =O0OO0O00O00OO0OO0 .loc [O0OO0O00O00OO0OO0 ["适用范围"].str .contains (O00OOOOO0OO0OO000 ,na =False )].copy ().reset_index (drop =True )#line:4484
		TABLE_tree_Level_2 (Countall (OO0O000OO00000O0O ).df_psur ("特定品种作为通用关键字",OOO0OOO00O0000O00 ),1 ,OO0O000OO00000O0O )#line:4485
def TOOLS_findin (O0000OO00OOOOO0OO ,OO0O0O0OO00OOOO00 ):#line:4486
	""#line:4487
	OOO000OO0OO0O0O00 =Toplevel ()#line:4488
	OOO000OO0OO0O0O00 .title ('高级查找')#line:4489
	OOOOO0O0OOO00O0OO =OOO000OO0OO0O0O00 .winfo_screenwidth ()#line:4490
	O00O0O0000OO000O0 =OOO000OO0OO0O0O00 .winfo_screenheight ()#line:4492
	O0O0OOOOOO0OOOO00 =400 #line:4494
	O0O0OO00OO0OO0OOO =120 #line:4495
	OOOOOOOOO0O00O0O0 =(OOOOO0O0OOO00O0OO -O0O0OOOOOO0OOOO00 )/2 #line:4497
	OO0OO00O0O0O00OOO =(O00O0O0000OO000O0 -O0O0OO00OO0OO0OOO )/2 #line:4498
	OOO000OO0OO0O0O00 .geometry ("%dx%d+%d+%d"%(O0O0OOOOOO0OOOO00 ,O0O0OO00OO0OO0OOO ,OOOOOOOOO0O00O0O0 ,OO0OO00O0O0O00OOO ))#line:4499
	OOOOOO0OOO0000O00 =Label (OOO000OO0OO0O0O00 ,text ="需要查找的关键字（用|隔开）：")#line:4500
	OOOOOO0OOO0000O00 .pack ()#line:4501
	O0O0OOO00O000O00O =Label (OOO000OO0OO0O0O00 ,text ="在哪些列查找（用|隔开）：")#line:4502
	OOO00O00OO00O00OO =Entry (OOO000OO0OO0O0O00 ,width =80 )#line:4504
	OOO00O00OO00O00OO .insert (0 ,"破裂|断裂")#line:4505
	O000OOOOOOO0000O0 =Entry (OOO000OO0OO0O0O00 ,width =80 )#line:4506
	O000OOOOOOO0000O0 .insert (0 ,"器械故障表现|伤害表现")#line:4507
	OOO00O00OO00O00OO .pack ()#line:4508
	O0O0OOO00O000O00O .pack ()#line:4509
	O000OOOOOOO0000O0 .pack ()#line:4510
	OOO0O000O0O000OO0 =LabelFrame (OOO000OO0OO0O0O00 )#line:4511
	OO00OO00000OOO00O =Button (OOO0O000O0O000OO0 ,text ="确定",width =10 ,command =lambda :PROGRAM_thread_it (TABLE_tree_Level_2 ,O0O0000O000OO0000 (OOO00O00OO00O00OO .get (),O000OOOOOOO0000O0 .get (),O0000OO00OOOOO0OO ),1 ,OO0O0O0OO00OOOO00 ))#line:4512
	OO00OO00000OOO00O .pack (side =LEFT ,padx =1 ,pady =1 )#line:4513
	OOO0O000O0O000OO0 .pack ()#line:4514
	def O0O0000O000OO0000 (OOOO0OOOOO0O000O0 ,OOO000OO00000O000 ,OOO00O0O000OOO0OO ):#line:4517
		OOO00O0O000OOO0OO ["关键字查找列10"]="######"#line:4518
		for O0O0OOOOO0O0O0OOO in TOOLS_get_list (OOO000OO00000O000 ):#line:4519
			OOO00O0O000OOO0OO ["关键字查找列10"]=OOO00O0O000OOO0OO ["关键字查找列10"].astype (str )+OOO00O0O000OOO0OO [O0O0OOOOO0O0O0OOO ].astype (str )#line:4520
		OOO00O0O000OOO0OO =OOO00O0O000OOO0OO .loc [OOO00O0O000OOO0OO ["关键字查找列10"].str .contains (OOOO0OOOOO0O000O0 ,na =False )]#line:4521
		del OOO00O0O000OOO0OO ["关键字查找列10"]#line:4522
		return OOO00O0O000OOO0OO #line:4523
def PROGRAM_about ():#line:4525
    ""#line:4526
    OOO0OOO00OO000OO0 =" 佛山市食品药品检验检测中心 \n(佛山市药品不良反应监测中心)\n蔡权周（QQ或微信411703730）\n仅供政府设立的不良反应监测机构使用。"#line:4527
    showinfo (title ="关于",message =OOO0OOO00OO000OO0 )#line:4528
def PROGRAM_thread_it (OO0O000OO0OOO0O0O ,*OOO0OO00O00OO00OO ):#line:4531
    ""#line:4532
    OO00O0000000O0000 =threading .Thread (target =OO0O000OO0OOO0O0O ,args =OOO0OO00O00OO00OO )#line:4534
    OO00O0000000O0000 .setDaemon (True )#line:4536
    OO00O0000000O0000 .start ()#line:4538
def PROGRAM_Menubar (O0OOOOOOO0OO00000 ,OO00OO0000OO000OO ,OOO000O0O00OOOO0O ,OO00OO0OOOO0O0000 ):#line:4539
	""#line:4540
	O0O0O0OOOO000O0OO =Menu (O0OOOOOOO0OO00000 )#line:4542
	O0OOOOOOO0OO00000 .config (menu =O0O0O0OOOO000O0OO )#line:4544
	O0OO0O0OOO0000O00 =Menu (O0O0O0OOOO000O0OO ,tearoff =0 )#line:4546
	O0O0O0OOOO000O0OO .add_cascade (label ="实用工具",menu =O0OO0O0OOO0000O00 )#line:4547
	O0OO0O0OOO0000O00 .add_command (label ="统计工具箱",command =lambda :TABLE_tree_Level_2 (OO00OO0000OO000OO ,1 ,OO00OO0OOOO0O0000 ,"tools_x"))#line:4549
	O0OO0O0OOO0000O00 .add_command (label ="数据规整（自定义）",command =lambda :TOOL_guizheng (OO00OO0000OO000OO ,0 ,False ))#line:4551
	O0OO0O0OOO0000O00 .add_command (label ="批量筛选（自定义）",command =lambda :TOOLS_xuanze (OO00OO0000OO000OO ,0 ))#line:4553
	O0OO0O0OOO0000O00 .add_separator ()#line:4554
	O0OO0O0OOO0000O00 .add_command (label ="原始导入",command =TOOLS_fileopen )#line:4556
	if ini ["模式"]=="其他":#line:4561
		return 0 #line:4562
	if ini ["模式"]=="药品"or ini ["模式"]=="器械":#line:4564
		OOO000O0OOO000000 =Menu (O0O0O0OOOO000O0OO ,tearoff =0 )#line:4565
		O0O0O0OOOO000O0OO .add_cascade (label ="信号检测",menu =OOO000O0OOO000000 )#line:4566
		OOO000O0OOO000000 .add_command (label ="预警（单日）",command =lambda :TOOLS_keti (OO00OO0000OO000OO ))#line:4568
		OOO000O0OOO000000 .add_command (label ="数量比例失衡监测-证号内批号",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0000OO000OO ).df_findrisk ("产品批号"),1 ,OO00OO0OOOO0O0000 ))#line:4570
		OOO000O0OOO000000 .add_command (label ="数量比例失衡监测-证号内季度",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0000OO000OO ).df_findrisk ("事件发生季度"),1 ,OO00OO0OOOO0O0000 ))#line:4572
		OOO000O0OOO000000 .add_command (label ="数量比例失衡监测-证号内月份",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0000OO000OO ).df_findrisk ("事件发生月份"),1 ,OO00OO0OOOO0O0000 ))#line:4574
		OOO000O0OOO000000 .add_command (label ="数量比例失衡监测-证号内性别",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0000OO000OO ).df_findrisk ("性别"),1 ,OO00OO0OOOO0O0000 ))#line:4576
		OOO000O0OOO000000 .add_command (label ="数量比例失衡监测-证号内年龄段",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0000OO000OO ).df_findrisk ("年龄段"),1 ,OO00OO0OOOO0O0000 ))#line:4578
		OOO000O0OOO000000 .add_separator ()#line:4580
		OOO000O0OOO000000 .add_command (label ="关键字检测（同证号内不同批号比对）",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0000OO000OO ).df_find_all_keword_risk ("产品批号"),1 ,OO00OO0OOOO0O0000 ))#line:4582
		OOO000O0OOO000000 .add_command (label ="关键字检测（同证号内不同月份比对）",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0000OO000OO ).df_find_all_keword_risk ("事件发生月份"),1 ,OO00OO0OOOO0O0000 ))#line:4584
		OOO000O0OOO000000 .add_command (label ="关键字检测（同证号内不同季度比对）",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0000OO000OO ).df_find_all_keword_risk ("事件发生季度"),1 ,OO00OO0OOOO0O0000 ))#line:4586
		OOO000O0OOO000000 .add_command (label ="关键字检测（同证号内不同性别比对）",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0000OO000OO ).df_find_all_keword_risk ("性别"),1 ,OO00OO0OOOO0O0000 ))#line:4588
		OOO000O0OOO000000 .add_command (label ="关键字检测（同证号内不同年龄段比对）",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0000OO000OO ).df_find_all_keword_risk ("年龄段"),1 ,OO00OO0OOOO0O0000 ))#line:4590
		OOO000O0OOO000000 .add_separator ()#line:4592
		OOO000O0OOO000000 .add_command (label ="关键字ROR-页面内同证号的批号间比对",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0000OO000OO ).df_ror (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","产品批号"]),1 ,OO00OO0OOOO0O0000 ))#line:4594
		OOO000O0OOO000000 .add_command (label ="关键字ROR-页面内同证号的月份间比对",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0000OO000OO ).df_ror (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","事件发生月份"]),1 ,OO00OO0OOOO0O0000 ))#line:4596
		OOO000O0OOO000000 .add_command (label ="关键字ROR-页面内同证号的季度间比对",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0000OO000OO ).df_ror (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","事件发生季度"]),1 ,OO00OO0OOOO0O0000 ))#line:4598
		OOO000O0OOO000000 .add_command (label ="关键字ROR-页面内同证号的年龄段间比对",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0000OO000OO ).df_ror (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","年龄段"]),1 ,OO00OO0OOOO0O0000 ))#line:4600
		OOO000O0OOO000000 .add_command (label ="关键字ROR-页面内同证号的性别间比对",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0000OO000OO ).df_ror (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","性别"]),1 ,OO00OO0OOOO0O0000 ))#line:4602
		OOO000O0OOO000000 .add_separator ()#line:4604
		OOO000O0OOO000000 .add_command (label ="关键字ROR-页面内同品名的证号间比对",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0000OO000OO ).df_ror (["产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"]),1 ,OO00OO0OOOO0O0000 ))#line:4606
		OOO000O0OOO000000 .add_command (label ="关键字ROR-页面内同品名的年龄段间比对",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0000OO000OO ).df_ror (["产品类别","规整后品类","产品名称","年龄段"]),1 ,OO00OO0OOOO0O0000 ))#line:4608
		OOO000O0OOO000000 .add_command (label ="关键字ROR-页面内同品名的性别间比对",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0000OO000OO ).df_ror (["产品类别","规整后品类","产品名称","性别"]),1 ,OO00OO0OOOO0O0000 ))#line:4610
		OOO000O0OOO000000 .add_separator ()#line:4612
		OOO000O0OOO000000 .add_command (label ="关键字ROR-页面内同类别的名称间比对",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0000OO000OO ).df_ror (["产品类别","产品名称"]),1 ,OO00OO0OOOO0O0000 ))#line:4614
		OOO000O0OOO000000 .add_command (label ="关键字ROR-页面内同类别的年龄段间比对",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0000OO000OO ).df_ror (["产品类别","年龄段"]),1 ,OO00OO0OOOO0O0000 ))#line:4616
		OOO000O0OOO000000 .add_command (label ="关键字ROR-页面内同类别的性别间比对",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0000OO000OO ).df_ror (["产品类别","性别"]),1 ,OO00OO0OOOO0O0000 ))#line:4618
	O0OO00O0O0O000O0O =Menu (O0O0O0OOOO000O0OO ,tearoff =0 )#line:4622
	O0O0O0OOOO000O0OO .add_cascade (label ="简报制作",menu =O0OO00O0O0O000O0O )#line:4623
	O0OO00O0O0O000O0O .add_command (label ="药品简报",command =lambda :TOOLS_autocount (OO00OO0000OO000OO ,"药品"))#line:4626
	O0OO00O0O0O000O0O .add_command (label ="器械简报",command =lambda :TOOLS_autocount (OO00OO0000OO000OO ,"器械"))#line:4628
	O0OO00O0O0O000O0O .add_command (label ="化妆品简报",command =lambda :TOOLS_autocount (OO00OO0000OO000OO ,"化妆品"))#line:4630
	O00OO000O0OOO000O =Menu (O0O0O0OOOO000O0OO ,tearoff =0 )#line:4634
	O0O0O0OOOO000O0OO .add_cascade (label ="品种评价",menu =O00OO000O0OOO000O )#line:4635
	O00OO000O0OOO000O .add_command (label ="报告年份",command =lambda :STAT_pinzhong (OO00OO0000OO000OO ,"报告年份",-1 ))#line:4637
	O00OO000O0OOO000O .add_command (label ="发生年份",command =lambda :STAT_pinzhong (OO00OO0000OO000OO ,"事件发生年份",-1 ))#line:4639
	O00OO000O0OOO000O .add_separator ()#line:4640
	O00OO000O0OOO000O .add_command (label ="涉及企业",command =lambda :STAT_pinzhong (OO00OO0000OO000OO ,"上市许可持有人名称",1 ))#line:4643
	O00OO000O0OOO000O .add_command (label ="产品名称",command =lambda :STAT_pinzhong (OO00OO0000OO000OO ,"产品名称",1 ))#line:4645
	O00OO000O0OOO000O .add_command (label ="注册证号",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0000OO000OO ).df_zhenghao (),1 ,OO00OO0OOOO0O0000 ))#line:4647
	O00OO000O0OOO000O .add_separator ()#line:4648
	O00OO000O0OOO000O .add_command (label ="年龄段分布",command =lambda :STAT_pinzhong (OO00OO0000OO000OO ,"年龄段",1 ))#line:4650
	O00OO000O0OOO000O .add_command (label ="性别分布",command =lambda :STAT_pinzhong (OO00OO0000OO000OO ,"性别",1 ))#line:4652
	O00OO000O0OOO000O .add_command (label ="年龄性别分布",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0000OO000OO ).df_age (),1 ,OO00OO0OOOO0O0000 ,))#line:4654
	O00OO000O0OOO000O .add_separator ()#line:4655
	O00OO000O0OOO000O .add_command (label ="事件发生时间",command =lambda :STAT_pinzhong (OO00OO0000OO000OO ,"时隔",1 ))#line:4657
	if ini ["模式"]=="器械":#line:4658
		O00OO000O0OOO000O .add_command (label ="事件分布（故障表现）",command =lambda :STAT_pinzhong (OO00OO0000OO000OO ,"器械故障表现",0 ))#line:4660
		O00OO000O0OOO000O .add_command (label ="事件分布（关键词）",command =lambda :TOOLS_get_guize2 (OO00OO0000OO000OO ))#line:4662
	if ini ["模式"]=="药品":#line:4663
		O00OO000O0OOO000O .add_command (label ="怀疑/并用",command =lambda :STAT_pinzhong (OO00OO0000OO000OO ,"怀疑/并用",1 ))#line:4665
		O00OO000O0OOO000O .add_command (label ="报告类型-严重程度",command =lambda :STAT_pinzhong (OO00OO0000OO000OO ,"报告类型-严重程度",1 ))#line:4667
		O00OO000O0OOO000O .add_command (label ="停药减药后反应是否减轻或消失",command =lambda :STAT_pinzhong (OO00OO0000OO000OO ,"停药减药后反应是否减轻或消失",1 ))#line:4669
		O00OO000O0OOO000O .add_command (label ="再次使用可疑药是否出现同样反应",command =lambda :STAT_pinzhong (OO00OO0000OO000OO ,"再次使用可疑药是否出现同样反应",1 ))#line:4671
		O00OO000O0OOO000O .add_command (label ="对原患疾病影响",command =lambda :STAT_pinzhong (OO00OO0000OO000OO ,"对原患疾病影响",1 ))#line:4673
		O00OO000O0OOO000O .add_command (label ="不良反应结果",command =lambda :STAT_pinzhong (OO00OO0000OO000OO ,"不良反应结果",1 ))#line:4675
		O00OO000O0OOO000O .add_command (label ="报告单位关联性评价",command =lambda :STAT_pinzhong (OO00OO0000OO000OO ,"关联性评价",1 ))#line:4677
		O00OO000O0OOO000O .add_separator ()#line:4678
		O00OO000O0OOO000O .add_command (label ="不良反应转归情况",command =lambda :STAT_pinzhong (OO00OO0000OO000OO ,"不良反应结果2",4 ))#line:4680
		O00OO000O0OOO000O .add_command (label ="品种评价-关联性评价汇总",command =lambda :STAT_pinzhong (OO00OO0000OO000OO ,"关联性评价汇总",5 ))#line:4682
		O00OO000O0OOO000O .add_separator ()#line:4686
		O00OO000O0OOO000O .add_command (label ="不良反应-术语",command =lambda :STAT_pinzhong (OO00OO0000OO000OO ,"器械故障表现",0 ))#line:4688
		O00OO000O0OOO000O .add_command (label ="不良反应器官系统-术语",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0000OO000OO ).df_psur (),1 ,OO00OO0OOOO0O0000 ))#line:4690
		if "不良反应-code"in OO00OO0000OO000OO .columns :#line:4691
			O00OO000O0OOO000O .add_command (label ="不良反应-由code转化",command =lambda :STAT_pinzhong (OO00OO0000OO000OO ,"不良反应-code",2 ))#line:4693
			O00OO000O0OOO000O .add_command (label ="不良反应器官系统-由code转化",command =lambda :STAT_pinzhong (OO00OO0000OO000OO ,"不良反应-code",3 ))#line:4695
			O00OO000O0OOO000O .add_separator ()#line:4696
		O00OO000O0OOO000O .add_command (label ="疾病名称-术语",command =lambda :STAT_pinzhong (OO00OO0000OO000OO ,"相关疾病信息[疾病名称]-术语",0 ))#line:4698
		if "不良反应-code"in OO00OO0000OO000OO .columns :#line:4699
			O00OO000O0OOO000O .add_command (label ="疾病名称-由code转化",command =lambda :STAT_pinzhong (OO00OO0000OO000OO ,"相关疾病信息[疾病名称]-code",2 ))#line:4701
			O00OO000O0OOO000O .add_command (label ="疾病器官系统-由code转化",command =lambda :STAT_pinzhong (OO00OO0000OO000OO ,"相关疾病信息[疾病名称]-code",3 ))#line:4703
			O00OO000O0OOO000O .add_separator ()#line:4704
		O00OO000O0OOO000O .add_command (label ="适应症-术语",command =lambda :STAT_pinzhong (OO00OO0000OO000OO ,"治疗适应症-术语",0 ))#line:4706
		if "不良反应-code"in OO00OO0000OO000OO .columns :#line:4707
			O00OO000O0OOO000O .add_command (label ="适应症-由code转化",command =lambda :STAT_pinzhong (OO00OO0000OO000OO ,"治疗适应症-code",2 ))#line:4709
			O00OO000O0OOO000O .add_command (label ="适应症器官系统-由code转化",command =lambda :STAT_pinzhong (OO00OO0000OO000OO ,"治疗适应症-code",3 ))#line:4711
	if ini ["模式"]=="药品":#line:4713
		OO0OOO00O00OO00OO =Menu (O0O0O0OOOO000O0OO ,tearoff =0 )#line:4714
		O0O0O0OOOO000O0OO .add_cascade (label ="药品探索",menu =OO0OOO00O00OO00OO )#line:4715
		OO0OOO00O00OO00OO .add_command (label ="新的不良反应检测(证号)",command =lambda :PROGRAM_thread_it (TOOLS_get_new ,OO00OO0OOOO0O0000 ,"证号"))#line:4716
		OO0OOO00O00OO00OO .add_command (label ="新的不良反应检测(品种)",command =lambda :PROGRAM_thread_it (TOOLS_get_new ,OO00OO0OOOO0O0000 ,"品种"))#line:4717
		OO0OOO00O00OO00OO .add_separator ()#line:4718
		OO0OOO00O00OO00OO .add_command (label ="基础信息批量操作（品名）",command =lambda :TOOLS_ror_mode1 (OO00OO0000OO000OO ,"产品名称"))#line:4720
		OO0OOO00O00OO00OO .add_command (label ="器官系统分类批量操作（品名）",command =lambda :TOOLS_ror_mode4 (OO00OO0000OO000OO ,"产品名称"))#line:4722
		OO0OOO00O00OO00OO .add_command (label ="器官系统ROR批量操作（品名）",command =lambda :TOOLS_ror_mode2 (OO00OO0000OO000OO ,"产品名称"))#line:4724
		OO0OOO00O00OO00OO .add_command (label ="ADR-ROR批量操作（品名）",command =lambda :TOOLS_ror_mode3 (OO00OO0000OO000OO ,"产品名称"))#line:4726
		OO0OOO00O00OO00OO .add_separator ()#line:4727
		OO0OOO00O00OO00OO .add_command (label ="基础信息批量操作（批准文号）",command =lambda :TOOLS_ror_mode1 (OO00OO0000OO000OO ,"注册证编号/曾用注册证编号"))#line:4729
		OO0OOO00O00OO00OO .add_command (label ="器官系统分类批量操作（批准文号）",command =lambda :TOOLS_ror_mode4 (OO00OO0000OO000OO ,"注册证编号/曾用注册证编号"))#line:4731
		OO0OOO00O00OO00OO .add_command (label ="器官系统ROR批量操作（批准文号）",command =lambda :TOOLS_ror_mode2 (OO00OO0000OO000OO ,"注册证编号/曾用注册证编号"))#line:4733
		OO0OOO00O00OO00OO .add_command (label ="ADR-ROR批量操作（批准文号）",command =lambda :TOOLS_ror_mode3 (OO00OO0000OO000OO ,"注册证编号/曾用注册证编号"))#line:4735
	OO0OO0OOOOO0O0O0O =Menu (O0O0O0OOOO000O0OO ,tearoff =0 )#line:4752
	O0O0O0OOOO000O0OO .add_cascade (label ="其他",menu =OO0OO0OOOOO0O0O0O )#line:4753
	OO0OO0OOOOO0O0O0O .add_command (label ="数据规整（报告单位）",command =lambda :TOOL_guizheng (OO00OO0000OO000OO ,2 ,False ))#line:4757
	OO0OO0OOOOO0O0O0O .add_command (label ="数据规整（产品名称）",command =lambda :TOOL_guizheng (OO00OO0000OO000OO ,3 ,False ))#line:4759
	OO0OO0OOOOO0O0O0O .add_command (label ="脱敏保存",command =lambda :TOOLS_data_masking (OO00OO0000OO000OO ))#line:4761
	OO0OO0OOOOO0O0O0O .add_separator ()#line:4762
	OO0OO0OOOOO0O0O0O .add_command (label ="评价人员（广东化妆品）",command =lambda :TOOL_person (OO00OO0000OO000OO ))#line:4764
	OO0OO0OOOOO0O0O0O .add_command (label ="意见反馈",command =lambda :PROGRAM_helper (["","  药械妆不良反应报表统计分析工作站","  开发者：蔡权周","  邮箱：411703730@qq.com","  微信号：sysucai","  手机号：18575757461"]))#line:4766
	OO0OO0OOOOO0O0O0O .add_command (label ="更改用户组",command =lambda :PROGRAM_thread_it (display_random_number ))#line:4768
def PROGRAM_helper (OOO0O00O00O0OOOO0 ):#line:4772
    ""#line:4773
    O0000000OOO00O0O0 =Toplevel ()#line:4774
    O0000000OOO00O0O0 .title ("信息查看")#line:4775
    O0000000OOO00O0O0 .geometry ("700x500")#line:4776
    OOOO0OO0OOOOOOO00 =Scrollbar (O0000000OOO00O0O0 )#line:4778
    O0OO00O0O0000O0O0 =Text (O0000000OOO00O0O0 ,height =80 ,width =150 ,bg ="#FFFFFF",font ="微软雅黑")#line:4779
    OOOO0OO0OOOOOOO00 .pack (side =RIGHT ,fill =Y )#line:4780
    O0OO00O0O0000O0O0 .pack ()#line:4781
    OOOO0OO0OOOOOOO00 .config (command =O0OO00O0O0000O0O0 .yview )#line:4782
    O0OO00O0O0000O0O0 .config (yscrollcommand =OOOO0OO0OOOOOOO00 .set )#line:4783
    for OO0OO0OOO0OO00OOO in OOO0O00O00O0OOOO0 :#line:4785
        O0OO00O0O0000O0O0 .insert (END ,OO0OO0OOO0OO00OOO )#line:4786
        O0OO00O0O0000O0O0 .insert (END ,"\n")#line:4787
    def O000OOO00OOOOO000 (event =None ):#line:4790
        O0OO00O0O0000O0O0 .event_generate ('<<Copy>>')#line:4791
    OOOOO00OOOO00O000 =Menu (O0OO00O0O0000O0O0 ,tearoff =False ,)#line:4794
    OOOOO00OOOO00O000 .add_command (label ="复制",command =O000OOO00OOOOO000 )#line:4795
    def OO0OO00OOO0O0OO0O (OOOOOO0OO0000O000 ):#line:4796
         OOOOO00OOOO00O000 .post (OOOOOO0OO0000O000 .x_root ,OOOOOO0OO0000O000 .y_root )#line:4797
    O0OO00O0O0000O0O0 .bind ("<Button-3>",OO0OO00OOO0O0OO0O )#line:4798
    O0OO00O0O0000O0O0 .config (state =DISABLED )#line:4800
def PROGRAM_change_schedule (OO000O000OOO00000 ,OOOOOO00OOOOO00OO ):#line:4802
    ""#line:4803
    canvas .coords (fill_rec ,(5 ,5 ,(OO000O000OOO00000 /OOOOOO00OOOOO00OO )*680 ,25 ))#line:4805
    root .update ()#line:4806
    x .set (str (round (OO000O000OOO00000 /OOOOOO00OOOOO00OO *100 ,2 ))+"%")#line:4807
    if round (OO000O000OOO00000 /OOOOOO00OOOOO00OO *100 ,2 )==100.00 :#line:4808
        x .set ("完成")#line:4809
def PROGRAM_showWelcome ():#line:4812
    ""#line:4813
    O00O0000O0O000O0O =roox .winfo_screenwidth ()#line:4814
    O0O0O0OO000OO00OO =roox .winfo_screenheight ()#line:4816
    roox .overrideredirect (True )#line:4818
    roox .attributes ("-alpha",1 )#line:4819
    O0OO0OOO00O00O0OO =(O00O0000O0O000O0O -475 )/2 #line:4820
    OO00OO000OO0O0O00 =(O0O0O0OO000OO00OO -200 )/2 #line:4821
    roox .geometry ("675x130+%d+%d"%(O0OO0OOO00O00O0OO ,OO00OO000OO0O0O00 ))#line:4823
    roox ["bg"]="royalblue"#line:4824
    O0O0O00000O0OO00O =Label (roox ,text =title_all2 ,fg ="white",bg ="royalblue",font =("微软雅黑",20 ))#line:4827
    O0O0O00000O0OO00O .place (x =0 ,y =15 ,width =675 ,height =90 )#line:4828
    OO0OOOOOO0O00000O =Label (roox ,text ="仅供监测机构使用 ",fg ="white",bg ="cornflowerblue",font =("微软雅黑",15 ))#line:4831
    OO0OOOOOO0O00000O .place (x =0 ,y =90 ,width =675 ,height =40 )#line:4832
def PROGRAM_closeWelcome ():#line:4835
    ""#line:4836
    for O0000OO000OO000O0 in range (2 ):#line:4837
        root .attributes ("-alpha",0 )#line:4838
        time .sleep (1 )#line:4839
    root .attributes ("-alpha",1 )#line:4840
    roox .destroy ()#line:4841
class Countall ():#line:4856
	""#line:4857
	def __init__ (O0000OOO000O0O0OO ,OO00O000OOO000000 ):#line:4858
		""#line:4859
		O0000OOO000O0O0OO .df =OO00O000OOO000000 #line:4860
		O0000OOO000O0O0OO .mode =ini ["模式"]#line:4861
	def df_org (O000OO00OO0OOO0O0 ,OO00O0OOO0O0O00OO ):#line:4863
		""#line:4864
		OOOOO00OO0OOOOO00 =O000OO00OO0OOO0O0 .df .drop_duplicates (["报告编码"]).groupby ([OO00O0OOO0O0O00OO ]).agg (报告数量 =("注册证编号/曾用注册证编号","count"),审核通过数 =("有效报告","sum"),严重伤害数 =("伤害",lambda OOOO00O0O000000O0 :STAT_countpx (OOOO00O0O000000O0 .values ,"严重伤害")),死亡数量 =("伤害",lambda OOO0O0OO0000OOOOO :STAT_countpx (OOO0O0OO0000OOOOO .values ,"死亡")),超时报告数 =("超时标记",lambda O0OOOO0O0OOO0OO0O :STAT_countpx (O0OOOO0O0OOO0OO0O .values ,1 )),有源 =("产品类别",lambda OO0OOOO00OO0000O0 :STAT_countpx (OO0OOOO00OO0000O0 .values ,"有源")),无源 =("产品类别",lambda O0O00O0OO0O0O00OO :STAT_countpx (O0O00O0OO0O0O00OO .values ,"无源")),体外诊断试剂 =("产品类别",lambda OOO0OOO00O0OOO0OO :STAT_countpx (OOO0OOO00O0OOO0OO .values ,"体外诊断试剂")),三类数量 =("管理类别",lambda O00OO00OO00OO000O :STAT_countpx (O00OO00OO00OO000O .values ,"Ⅲ类")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),报告季度 =("报告季度",STAT_countx ),报告月份 =("报告月份",STAT_countx ),).sort_values (by ="报告数量",ascending =[False ],na_position ="last").reset_index ()#line:4879
		O000000OO00OO0OO0 =["报告数量","审核通过数","严重伤害数","死亡数量","超时报告数","有源","无源","体外诊断试剂","三类数量","单位个数"]#line:4881
		OOOOO00OO0OOOOO00 .loc ["合计"]=OOOOO00OO0OOOOO00 [O000000OO00OO0OO0 ].apply (lambda O0000O0O0O00O0O0O :O0000O0O0O00O0O0O .sum ())#line:4882
		OOOOO00OO0OOOOO00 [O000000OO00OO0OO0 ]=OOOOO00OO0OOOOO00 [O000000OO00OO0OO0 ].apply (lambda OO000O00OO0O0000O :OO000O00OO0O0000O .astype (int ))#line:4883
		OOOOO00OO0OOOOO00 .iloc [-1 ,0 ]="合计"#line:4884
		OOOOO00OO0OOOOO00 ["严重比"]=round ((OOOOO00OO0OOOOO00 ["严重伤害数"]+OOOOO00OO0OOOOO00 ["死亡数量"])/OOOOO00OO0OOOOO00 ["报告数量"]*100 ,2 )#line:4886
		OOOOO00OO0OOOOO00 ["Ⅲ类比"]=round ((OOOOO00OO0OOOOO00 ["三类数量"])/OOOOO00OO0OOOOO00 ["报告数量"]*100 ,2 )#line:4887
		OOOOO00OO0OOOOO00 ["超时比"]=round ((OOOOO00OO0OOOOO00 ["超时报告数"])/OOOOO00OO0OOOOO00 ["报告数量"]*100 ,2 )#line:4888
		OOOOO00OO0OOOOO00 ["报表类型"]="dfx_org"+OO00O0OOO0O0O00OO #line:4889
		if ini ["模式"]=="药品":#line:4892
			del OOOOO00OO0OOOOO00 ["有源"]#line:4894
			del OOOOO00OO0OOOOO00 ["无源"]#line:4895
			del OOOOO00OO0OOOOO00 ["体外诊断试剂"]#line:4896
			OOOOO00OO0OOOOO00 =OOOOO00OO0OOOOO00 .rename (columns ={"三类数量":"新的和严重的数量"})#line:4897
			OOOOO00OO0OOOOO00 =OOOOO00OO0OOOOO00 .rename (columns ={"Ⅲ类比":"新严比"})#line:4898
		return OOOOO00OO0OOOOO00 #line:4900
	def df_user (OO0O0OO00OO0OO0O0 ):#line:4904
		""#line:4905
		OO0O0OO00OO0OO0O0 .df ["医疗机构类别"]=OO0O0OO00OO0OO0O0 .df ["医疗机构类别"].fillna ("未填写")#line:4906
		O000000O0000OOOO0 =OO0O0OO00OO0OO0O0 .df .drop_duplicates (["报告编码"]).groupby (["监测机构","单位名称","医疗机构类别"]).agg (报告数量 =("注册证编号/曾用注册证编号","count"),审核通过数 =("有效报告","sum"),严重伤害数 =("伤害",lambda OOOO0O00O000OO0O0 :STAT_countpx (OOOO0O00O000OO0O0 .values ,"严重伤害")),死亡数量 =("伤害",lambda OOOO0OO000000O000 :STAT_countpx (OOOO0OO000000O000 .values ,"死亡")),超时报告数 =("超时标记",lambda OOOO0OO0O0OO000O0 :STAT_countpx (OOOO0OO0O0OO000O0 .values ,1 )),有源 =("产品类别",lambda OO000OOO0O000O000 :STAT_countpx (OO000OOO0O000O000 .values ,"有源")),无源 =("产品类别",lambda OO0OOO000O0OOO000 :STAT_countpx (OO0OOO000O0OOO000 .values ,"无源")),体外诊断试剂 =("产品类别",lambda OO00000OOO00O0OO0 :STAT_countpx (OO00000OOO00O0OO0 .values ,"体外诊断试剂")),三类数量 =("管理类别",lambda OO0OO0OO00OOO0O00 :STAT_countpx (OO0OO0OO00OOO0O00 .values ,"Ⅲ类")),产品数量 =("产品名称","nunique"),产品清单 =("产品名称",STAT_countx ),报告季度 =("报告季度",STAT_countx ),报告月份 =("报告月份",STAT_countx ),).sort_values (by ="报告数量",ascending =[False ],na_position ="last").reset_index ()#line:4921
		O00O00OO0O000OOO0 =["报告数量","审核通过数","严重伤害数","死亡数量","超时报告数","有源","无源","体外诊断试剂","三类数量"]#line:4924
		O000000O0000OOOO0 .loc ["合计"]=O000000O0000OOOO0 [O00O00OO0O000OOO0 ].apply (lambda O000OO0O000O000OO :O000OO0O000O000OO .sum ())#line:4925
		O000000O0000OOOO0 [O00O00OO0O000OOO0 ]=O000000O0000OOOO0 [O00O00OO0O000OOO0 ].apply (lambda OOO0OO000O00O00O0 :OOO0OO000O00O00O0 .astype (int ))#line:4926
		O000000O0000OOOO0 .iloc [-1 ,0 ]="合计"#line:4927
		O000000O0000OOOO0 ["严重比"]=round ((O000000O0000OOOO0 ["严重伤害数"]+O000000O0000OOOO0 ["死亡数量"])/O000000O0000OOOO0 ["报告数量"]*100 ,2 )#line:4929
		O000000O0000OOOO0 ["Ⅲ类比"]=round ((O000000O0000OOOO0 ["三类数量"])/O000000O0000OOOO0 ["报告数量"]*100 ,2 )#line:4930
		O000000O0000OOOO0 ["超时比"]=round ((O000000O0000OOOO0 ["超时报告数"])/O000000O0000OOOO0 ["报告数量"]*100 ,2 )#line:4931
		O000000O0000OOOO0 ["报表类型"]="dfx_user"#line:4932
		if ini ["模式"]=="药品":#line:4934
			del O000000O0000OOOO0 ["有源"]#line:4936
			del O000000O0000OOOO0 ["无源"]#line:4937
			del O000000O0000OOOO0 ["体外诊断试剂"]#line:4938
			O000000O0000OOOO0 =O000000O0000OOOO0 .rename (columns ={"三类数量":"新的和严重的数量"})#line:4939
			O000000O0000OOOO0 =O000000O0000OOOO0 .rename (columns ={"Ⅲ类比":"新严比"})#line:4940
		return O000000O0000OOOO0 #line:4942
	def df_zhenghao (O00000000OO00OO0O ):#line:4947
		""#line:4948
		OO000O0O0OOO00OO0 =O00000000OO00OO0O .df .groupby (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"]).agg (证号计数 =("报告编码","nunique"),批号个数 =("产品批号","nunique"),批号列表 =("产品批号",STAT_countx ),型号个数 =("型号","nunique"),型号列表 =("型号",STAT_countx ),规格个数 =("规格","nunique"),规格列表 =("规格",STAT_countx ),).sort_values (by ="证号计数",ascending =[False ],na_position ="last").reset_index ()#line:4958
		O0O0OOOO0O00OOOOO =O00000000OO00OO0O .df .drop_duplicates (["报告编码"]).groupby (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"]).agg (严重伤害数 =("伤害",lambda O000O0O0O0OOO00O0 :STAT_countpx (O000O0O0O0OOO00O0 .values ,"严重伤害")),死亡数量 =("伤害",lambda O00O0000O0O0000O0 :STAT_countpx (O00O0000O0O0000O0 .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),待评价数 =("持有人报告状态",lambda OOO000OOO0O0OOOOO :STAT_countpx (OOO000OOO0O0OOOOO .values ,"待评价")),严重伤害待评价数 =("伤害与评价",lambda OO00O0O0OOO00OO0O :STAT_countpx (OO00O0O0OOO00OO0O .values ,"严重伤害待评价")),).reset_index ()#line:4967
		OOOOOOOO000O0O0O0 =pd .merge (OO000O0O0OOO00OO0 ,O0O0OOOO0O00OOOOO ,on =["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"],how ="left")#line:4969
		OOOOOOOO000O0O0O0 =STAT_basic_risk (OOOOOOOO000O0O0O0 ,"证号计数","严重伤害数","死亡数量","单位个数")#line:4970
		OOOOOOOO000O0O0O0 =pd .merge (OOOOOOOO000O0O0O0 ,STAT_recent30 (O00000000OO00OO0O .df ,["注册证编号/曾用注册证编号"]),on =["注册证编号/曾用注册证编号"],how ="left")#line:4972
		OOOOOOOO000O0O0O0 ["最近30天报告数"]=OOOOOOOO000O0O0O0 ["最近30天报告数"].fillna (0 ).astype (int )#line:4973
		OOOOOOOO000O0O0O0 ["最近30天报告严重伤害数"]=OOOOOOOO000O0O0O0 ["最近30天报告严重伤害数"].fillna (0 ).astype (int )#line:4974
		OOOOOOOO000O0O0O0 ["最近30天报告死亡数量"]=OOOOOOOO000O0O0O0 ["最近30天报告死亡数量"].fillna (0 ).astype (int )#line:4975
		OOOOOOOO000O0O0O0 ["最近30天报告单位个数"]=OOOOOOOO000O0O0O0 ["最近30天报告单位个数"].fillna (0 ).astype (int )#line:4976
		OOOOOOOO000O0O0O0 ["最近30天风险评分"]=OOOOOOOO000O0O0O0 ["最近30天风险评分"].fillna (0 ).astype (int )#line:4977
		OOOOOOOO000O0O0O0 ["报表类型"]="dfx_zhenghao"#line:4979
		if ini ["模式"]=="药品":#line:4981
			OOOOOOOO000O0O0O0 =OOOOOOOO000O0O0O0 .rename (columns ={"待评价数":"新的数量"})#line:4982
			OOOOOOOO000O0O0O0 =OOOOOOOO000O0O0O0 .rename (columns ={"严重伤害待评价数":"新的严重的数量"})#line:4983
		return OOOOOOOO000O0O0O0 #line:4985
	def df_pihao (OOOOOOO0O0O0OO0OO ):#line:4987
		""#line:4988
		OOOOO0OOO00000OO0 =OOOOOOO0O0O0OO0OO .df .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","产品批号"]).agg (批号计数 =("报告编码","nunique"),型号个数 =("型号","nunique"),型号列表 =("型号",STAT_countx ),规格个数 =("规格","nunique"),规格列表 =("规格",STAT_countx ),).sort_values (by ="批号计数",ascending =[False ],na_position ="last").reset_index ()#line:4995
		O0OO0OO0000OOOOO0 =OOOOOOO0O0O0OO0OO .df .drop_duplicates (["报告编码"]).groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","产品批号"]).agg (严重伤害数 =("伤害",lambda O00OO000O000OO0OO :STAT_countpx (O00OO000O000OO0OO .values ,"严重伤害")),死亡数量 =("伤害",lambda O00OOOO0000O0OO00 :STAT_countpx (O00OOOO0000O0OO00 .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),待评价数 =("持有人报告状态",lambda O0O00O000OO0OO0O0 :STAT_countpx (O0O00O000OO0OO0O0 .values ,"待评价")),严重伤害待评价数 =("伤害与评价",lambda OO000O0O0O0OO0000 :STAT_countpx (OO000O0O0O0OO0000 .values ,"严重伤害待评价")),).reset_index ()#line:5004
		OO0O000OO0O000OO0 =pd .merge (OOOOO0OOO00000OO0 ,O0OO0OO0000OOOOO0 ,on =["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","产品批号"],how ="left")#line:5006
		OO0O000OO0O000OO0 =STAT_basic_risk (OO0O000OO0O000OO0 ,"批号计数","严重伤害数","死亡数量","单位个数")#line:5008
		OO0O000OO0O000OO0 =pd .merge (OO0O000OO0O000OO0 ,STAT_recent30 (OOOOOOO0O0O0OO0OO .df ,["注册证编号/曾用注册证编号","产品批号"]),on =["注册证编号/曾用注册证编号","产品批号"],how ="left")#line:5010
		OO0O000OO0O000OO0 ["最近30天报告数"]=OO0O000OO0O000OO0 ["最近30天报告数"].fillna (0 ).astype (int )#line:5011
		OO0O000OO0O000OO0 ["最近30天报告严重伤害数"]=OO0O000OO0O000OO0 ["最近30天报告严重伤害数"].fillna (0 ).astype (int )#line:5012
		OO0O000OO0O000OO0 ["最近30天报告死亡数量"]=OO0O000OO0O000OO0 ["最近30天报告死亡数量"].fillna (0 ).astype (int )#line:5013
		OO0O000OO0O000OO0 ["最近30天报告单位个数"]=OO0O000OO0O000OO0 ["最近30天报告单位个数"].fillna (0 ).astype (int )#line:5014
		OO0O000OO0O000OO0 ["最近30天风险评分"]=OO0O000OO0O000OO0 ["最近30天风险评分"].fillna (0 ).astype (int )#line:5015
		OO0O000OO0O000OO0 ["报表类型"]="dfx_pihao"#line:5017
		if ini ["模式"]=="药品":#line:5018
			OO0O000OO0O000OO0 =OO0O000OO0O000OO0 .rename (columns ={"待评价数":"新的数量"})#line:5019
			OO0O000OO0O000OO0 =OO0O000OO0O000OO0 .rename (columns ={"严重伤害待评价数":"新的严重的数量"})#line:5020
		return OO0O000OO0O000OO0 #line:5021
	def df_xinghao (OO0OOO000O00OO00O ):#line:5023
		""#line:5024
		OOO000OO00OOO0OO0 =OO0OOO000O00OO00O .df .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","型号"]).agg (型号计数 =("报告编码","nunique"),批号个数 =("产品批号","nunique"),批号列表 =("产品批号",STAT_countx ),规格个数 =("规格","nunique"),规格列表 =("规格",STAT_countx ),).sort_values (by ="型号计数",ascending =[False ],na_position ="last").reset_index ()#line:5031
		OOOOO00OOO00O0OO0 =OO0OOO000O00OO00O .df .drop_duplicates (["报告编码"]).groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","型号"]).agg (严重伤害数 =("伤害",lambda OO0OO0O0O0000OO00 :STAT_countpx (OO0OO0O0O0000OO00 .values ,"严重伤害")),死亡数量 =("伤害",lambda OO00O0O0O0O00O000 :STAT_countpx (OO00O0O0O0O00O000 .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),待评价数 =("持有人报告状态",lambda O0OOOOO000OOO0000 :STAT_countpx (O0OOOOO000OOO0000 .values ,"待评价")),严重伤害待评价数 =("伤害与评价",lambda OO000O0OO0OOOOO0O :STAT_countpx (OO000O0OO0OOOOO0O .values ,"严重伤害待评价")),).reset_index ()#line:5040
		OO0O000OOO0OO000O =pd .merge (OOO000OO00OOO0OO0 ,OOOOO00OOO00O0OO0 ,on =["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","型号"],how ="left")#line:5042
		OO0O000OOO0OO000O ["报表类型"]="dfx_xinghao"#line:5045
		if ini ["模式"]=="药品":#line:5046
			OO0O000OOO0OO000O =OO0O000OOO0OO000O .rename (columns ={"待评价数":"新的数量"})#line:5047
			OO0O000OOO0OO000O =OO0O000OOO0OO000O .rename (columns ={"严重伤害待评价数":"新的严重的数量"})#line:5048
		return OO0O000OOO0OO000O #line:5050
	def df_guige (OO00O0OO00000O0O0 ):#line:5052
		""#line:5053
		O0OO0O0O00OOO00O0 =OO00O0OO00000O0O0 .df .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","规格"]).agg (规格计数 =("报告编码","nunique"),批号个数 =("产品批号","nunique"),批号列表 =("产品批号",STAT_countx ),型号个数 =("型号","nunique"),型号列表 =("型号",STAT_countx ),).sort_values (by ="规格计数",ascending =[False ],na_position ="last").reset_index ()#line:5060
		O00OOO0O0OOOO0O0O =OO00O0OO00000O0O0 .df .drop_duplicates (["报告编码"]).groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","规格"]).agg (严重伤害数 =("伤害",lambda O0O00OOO0O0O000O0 :STAT_countpx (O0O00OOO0O0O000O0 .values ,"严重伤害")),死亡数量 =("伤害",lambda O000OOOOO0O0O0000 :STAT_countpx (O000OOOOO0O0O0000 .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),待评价数 =("持有人报告状态",lambda OO0O00OOOO0O0O000 :STAT_countpx (OO0O00OOOO0O0O000 .values ,"待评价")),严重伤害待评价数 =("伤害与评价",lambda O0O00OOOOO0O0OO00 :STAT_countpx (O0O00OOOOO0O0OO00 .values ,"严重伤害待评价")),).reset_index ()#line:5069
		O00OO000OO0OO00O0 =pd .merge (O0OO0O0O00OOO00O0 ,O00OOO0O0OOOO0O0O ,on =["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","规格"],how ="left")#line:5071
		O00OO000OO0OO00O0 ["报表类型"]="dfx_guige"#line:5073
		if ini ["模式"]=="药品":#line:5074
			O00OO000OO0OO00O0 =O00OO000OO0OO00O0 .rename (columns ={"待评价数":"新的数量"})#line:5075
			O00OO000OO0OO00O0 =O00OO000OO0OO00O0 .rename (columns ={"严重伤害待评价数":"新的严重的数量"})#line:5076
		return O00OO000OO0OO00O0 #line:5078
	def df_findrisk (O0OO0OOO000O0OO00 ,OO0OO0OOOO0O0OOO0 ):#line:5080
		""#line:5081
		if OO0OO0OOOO0O0OOO0 =="产品批号":#line:5082
			return STAT_find_risk (O0OO0OOO000O0OO00 .df [(O0OO0OOO000O0OO00 .df ["产品类别"]!="有源")],["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"],"注册证编号/曾用注册证编号",OO0OO0OOOO0O0OOO0 )#line:5083
		else :#line:5084
			return STAT_find_risk (O0OO0OOO000O0OO00 .df ,["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"],"注册证编号/曾用注册证编号",OO0OO0OOOO0O0OOO0 )#line:5085
	def df_find_all_keword_risk (O0000OO0000O00OO0 ,O000OO000O0000OO0 ,*O0OO00O0O00OO00O0 ):#line:5087
		""#line:5088
		OO0O000O0O000000O =O0000OO0000O00OO0 .df .copy ()#line:5090
		OO0O000O0O000000O =OO0O000O0O000000O .drop_duplicates (["报告编码"]).reset_index (drop =True )#line:5091
		OOO0O0OO00OO0OOOO =time .time ()#line:5092
		OO00OO000OO000000 =peizhidir +"0（范例）比例失衡关键字库.xls"#line:5093
		if "报告类型-新的"in OO0O000O0O000000O .columns :#line:5094
			OOO00OOO00000000O ="药品"#line:5095
		else :#line:5096
			OOO00OOO00000000O ="器械"#line:5097
		O0O00O0OOO0O0OO00 =pd .read_excel (OO00OO000OO000000 ,header =0 ,sheet_name =OOO00OOO00000000O ).reset_index (drop =True )#line:5098
		try :#line:5101
			if len (O0OO00O0O00OO00O0 [0 ])>0 :#line:5102
				O0O00O0OOO0O0OO00 =O0O00O0OOO0O0OO00 .loc [O0O00O0OOO0O0OO00 ["适用范围"].str .contains (O0OO00O0O00OO00O0 [0 ],na =False )].copy ().reset_index (drop =True )#line:5103
		except :#line:5104
			pass #line:5105
		OOO0O0O000OOO00O0 =["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"]#line:5107
		OOOOOO0OO00OO0000 =OOO0O0O000OOO00O0 [-1 ]#line:5108
		OOOO0O000OOOOO00O =OO0O000O0O000000O .groupby (OOO0O0O000OOO00O0 ).agg (总数量 =(OOOOOO0OO00OO0000 ,"count"),严重伤害数 =("伤害",lambda OOO0OOOO00OO0OO00 :STAT_countpx (OOO0OOOO00OO0OO00 .values ,"严重伤害")),死亡数量 =("伤害",lambda OOO0000OOO000OOOO :STAT_countpx (OOO0000OOO000OOOO .values ,"死亡")),)#line:5113
		OOOOOO0OO00OO0000 =OOO0O0O000OOO00O0 [-1 ]#line:5114
		O00OOO0OO0OO0O000 =OOO0O0O000OOO00O0 .copy ()#line:5116
		O00OOO0OO0OO0O000 .append (O000OO000O0000OO0 )#line:5117
		O0OO00OO00O00OOOO =OO0O000O0O000000O .groupby (O00OOO0OO0OO0O000 ).agg (该元素总数量 =(OOOOOO0OO00OO0000 ,"count"),).reset_index ()#line:5120
		OOOO0O000OOOOO00O =OOOO0O000OOOOO00O [(OOOO0O000OOOOO00O ["总数量"]>=3 )].reset_index ()#line:5123
		O00O0O000O00O0OOO =[]#line:5124
		O0OOOO0OO0O0000O0 =0 #line:5128
		OOOOOOO000OO00000 =int (len (OOOO0O000OOOOO00O ))#line:5129
		for O0OOO0O00OO0000OO ,O0OOO0OOOO00O0OOO ,OO0O00O0O000O0000 ,O0O00O00O0000OO00 in zip (OOOO0O000OOOOO00O ["产品名称"].values ,OOOO0O000OOOOO00O ["产品类别"].values ,OOOO0O000OOOOO00O [OOOOOO0OO00OO0000 ].values ,OOOO0O000OOOOO00O ["总数量"].values ):#line:5130
			O0OOOO0OO0O0000O0 +=1 #line:5131
			if (time .time ()-OOO0O0OO00OO0OOOO )>3 :#line:5133
				root .attributes ("-topmost",True )#line:5134
				PROGRAM_change_schedule (O0OOOO0OO0O0000O0 ,OOOOOOO000OO00000 )#line:5135
				root .attributes ("-topmost",False )#line:5136
			OO0OOO0O00OOO0O0O =OO0O000O0O000000O [(OO0O000O0O000000O [OOOOOO0OO00OO0000 ]==OO0O00O0O000O0000 )].copy ()#line:5137
			O0O00O0OOO0O0OO00 ["SELECT"]=O0O00O0OOO0O0OO00 .apply (lambda OO0OOOOO0O0O0O0OO :(OO0OOOOO0O0O0O0OO ["适用范围"]in O0OOO0O00OO0000OO )or (OO0OOOOO0O0O0O0OO ["适用范围"]in O0OOO0OOOO00O0OOO )or (OO0OOOOO0O0O0O0OO ["适用范围"]=="通用"),axis =1 )#line:5138
			OOOO0O0000O0O0000 =O0O00O0OOO0O0OO00 [(O0O00O0OOO0O0OO00 ["SELECT"]==True )].reset_index ()#line:5139
			if len (OOOO0O0000O0O0000 )>0 :#line:5140
				for OO0O0OOO00O00O0O0 ,OOO0O0O00OO000OOO ,OOOO0O00OO00O0O0O in zip (OOOO0O0000O0O0000 ["值"].values ,OOOO0O0000O0O0000 ["查找位置"].values ,OOOO0O0000O0O0000 ["排除值"].values ):#line:5142
					OOO00O00000O0OOO0 =OO0OOO0O00OOO0O0O .copy ()#line:5143
					OO0OOOOO00OO0OOO0 =TOOLS_get_list (OO0O0OOO00O00O0O0 )[0 ]#line:5144
					OOO00O00000O0OOO0 ["关键字查找列"]=""#line:5146
					for O0OO0OO0000OO0OOO in TOOLS_get_list (OOO0O0O00OO000OOO ):#line:5147
						OOO00O00000O0OOO0 ["关键字查找列"]=OOO00O00000O0OOO0 ["关键字查找列"]+OOO00O00000O0OOO0 [O0OO0OO0000OO0OOO ].astype ("str")#line:5148
					OOO00O00000O0OOO0 .loc [OOO00O00000O0OOO0 ["关键字查找列"].str .contains (OO0O0OOO00O00O0O0 ,na =False ),"关键字"]=OO0OOOOO00OO0OOO0 #line:5150
					if str (OOOO0O00OO00O0O0O )!="nan":#line:5153
						OOO00O00000O0OOO0 =OOO00O00000O0OOO0 .loc [~OOO00O00000O0OOO0 ["关键字查找列"].str .contains (OOOO0O00OO00O0O0O ,na =False )].copy ()#line:5154
					if (len (OOO00O00000O0OOO0 ))<1 :#line:5156
						continue #line:5157
					OO000OO00000000O0 =STAT_find_keyword_risk (OOO00O00000O0OOO0 ,["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","关键字"],"关键字",O000OO000O0000OO0 ,int (O0O00O00O0000OO00 ))#line:5159
					if len (OO000OO00000000O0 )>0 :#line:5160
						OO000OO00000000O0 ["关键字组合"]=OO0O0OOO00O00O0O0 #line:5161
						OO000OO00000000O0 ["排除值"]=OOOO0O00OO00O0O0O #line:5162
						OO000OO00000000O0 ["关键字查找列"]=OOO0O0O00OO000OOO #line:5163
						O00O0O000O00O0OOO .append (OO000OO00000000O0 )#line:5164
		OOOO00OO000OO0O0O =pd .concat (O00O0O000O00O0OOO )#line:5168
		OOOO00OO000OO0O0O =pd .merge (OOOO00OO000OO0O0O ,O0OO00OO00O00OOOO ,on =O00OOO0OO0OO0O000 ,how ="left")#line:5171
		OOOO00OO000OO0O0O ["关键字数量比例"]=round (OOOO00OO000OO0O0O ["计数"]/OOOO00OO000OO0O0O ["该元素总数量"],2 )#line:5172
		OOOO00OO000OO0O0O =OOOO00OO000OO0O0O .reset_index (drop =True )#line:5174
		if len (OOOO00OO000OO0O0O )>0 :#line:5175
			OOOO00OO000OO0O0O ["风险评分"]=0 #line:5176
			OOOO00OO000OO0O0O ["报表类型"]="keyword_findrisk"+O000OO000O0000OO0 #line:5177
			OOOO00OO000OO0O0O .loc [(OOOO00OO000OO0O0O ["计数"]>=3 ),"风险评分"]=OOOO00OO000OO0O0O ["风险评分"]+3 #line:5178
			OOOO00OO000OO0O0O .loc [(OOOO00OO000OO0O0O ["计数"]>=(OOOO00OO000OO0O0O ["数量均值"]+OOOO00OO000OO0O0O ["数量标准差"])),"风险评分"]=OOOO00OO000OO0O0O ["风险评分"]+1 #line:5179
			OOOO00OO000OO0O0O .loc [(OOOO00OO000OO0O0O ["计数"]>=OOOO00OO000OO0O0O ["数量CI"]),"风险评分"]=OOOO00OO000OO0O0O ["风险评分"]+1 #line:5180
			OOOO00OO000OO0O0O .loc [(OOOO00OO000OO0O0O ["关键字数量比例"]>0.5 )&(OOOO00OO000OO0O0O ["计数"]>=3 ),"风险评分"]=OOOO00OO000OO0O0O ["风险评分"]+1 #line:5181
			OOOO00OO000OO0O0O .loc [(OOOO00OO000OO0O0O ["严重伤害数"]>=3 ),"风险评分"]=OOOO00OO000OO0O0O ["风险评分"]+1 #line:5182
			OOOO00OO000OO0O0O .loc [(OOOO00OO000OO0O0O ["单位个数"]>=3 ),"风险评分"]=OOOO00OO000OO0O0O ["风险评分"]+1 #line:5183
			OOOO00OO000OO0O0O .loc [(OOOO00OO000OO0O0O ["死亡数量"]>=1 ),"风险评分"]=OOOO00OO000OO0O0O ["风险评分"]+10 #line:5184
			OOOO00OO000OO0O0O ["风险评分"]=OOOO00OO000OO0O0O ["风险评分"]+OOOO00OO000OO0O0O ["单位个数"]/100 #line:5185
			OOOO00OO000OO0O0O =OOOO00OO000OO0O0O .sort_values (by ="风险评分",ascending =[False ],na_position ="last").reset_index (drop =True )#line:5186
		print ("耗时：",(time .time ()-OOO0O0OO00OO0OOOO ))#line:5192
		return OOOO00OO000OO0O0O #line:5193
	def df_ror (O00O00O00O0O0OO0O ,OOOO0OOO0O0OO0OOO ,*OO0OOOOO000O000O0 ):#line:5196
		""#line:5197
		O000OO000O0OOO000 =O00O00O00O0O0OO0O .df .copy ()#line:5199
		OOOO000O00O000O00 =time .time ()#line:5200
		O0O00O0OOOO000O0O =peizhidir +"0（范例）比例失衡关键字库.xls"#line:5201
		if "报告类型-新的"in O000OO000O0OOO000 .columns :#line:5202
			O0000OOO00O0O0OO0 ="药品"#line:5203
		else :#line:5205
			O0000OOO00O0O0OO0 ="器械"#line:5206
		OOOO0OO0OOO0000OO =pd .read_excel (O0O00O0OOOO000O0O ,header =0 ,sheet_name =O0000OOO00O0O0OO0 ).reset_index (drop =True )#line:5207
		if "css"in O000OO000O0OOO000 .columns :#line:5210
			OO0OOOOO0O0O0O00O =O000OO000O0OOO000 .copy ()#line:5211
			OO0OOOOO0O0O0O00O ["器械故障表现"]=OO0OOOOO0O0O0O00O ["器械故障表现"].fillna ("未填写")#line:5212
			OO0OOOOO0O0O0O00O ["器械故障表现"]=OO0OOOOO0O0O0O00O ["器械故障表现"].str .replace ("*","",regex =False )#line:5213
			OOOO0OOO00OOO000O ="use("+str ("器械故障表现")+").file"#line:5214
			OOO0OO0OO0000OO00 =str (Counter (TOOLS_get_list0 (OOOO0OOO00OOO000O ,OO0OOOOO0O0O0O00O ,1000 ))).replace ("Counter({","{")#line:5215
			OOO0OO0OO0000OO00 =OOO0OO0OO0000OO00 .replace ("})","}")#line:5216
			OOO0OO0OO0000OO00 =ast .literal_eval (OOO0OO0OO0000OO00 )#line:5217
			OOOO0OO0OOO0000OO =pd .DataFrame .from_dict (OOO0OO0OO0000OO00 ,orient ="index",columns =["计数"]).reset_index ()#line:5218
			OOOO0OO0OOO0000OO ["适用范围列"]="产品类别"#line:5219
			OOOO0OO0OOO0000OO ["适用范围"]="无源"#line:5220
			OOOO0OO0OOO0000OO ["查找位置"]="伤害表现"#line:5221
			OOOO0OO0OOO0000OO ["值"]=OOOO0OO0OOO0000OO ["index"]#line:5222
			OOOO0OO0OOO0000OO ["排除值"]="-没有排除值-"#line:5223
			del OOOO0OO0OOO0000OO ["index"]#line:5224
		OO0OOO00OO0000OOO =OOOO0OOO0O0OO0OOO [-2 ]#line:5227
		O0000OO0000000OOO =OOOO0OOO0O0OO0OOO [-1 ]#line:5228
		OOO0OO00OOO0OO000 =OOOO0OOO0O0OO0OOO [:-1 ]#line:5229
		try :#line:5232
			if len (OO0OOOOO000O000O0 [0 ])>0 :#line:5233
				OO0OOO00OO0000OOO =OOOO0OOO0O0OO0OOO [-3 ]#line:5234
				OOOO0OO0OOO0000OO =OOOO0OO0OOO0000OO .loc [OOOO0OO0OOO0000OO ["适用范围"].str .contains (OO0OOOOO000O000O0 [0 ],na =False )].copy ().reset_index (drop =True )#line:5235
				OO000O0000O0OO000 =O000OO000O0OOO000 .groupby (["产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"]).agg (该元素总数量 =(O0000OO0000000OOO ,"count"),该元素严重伤害数 =("伤害",lambda O0OOOO0000O00O000 :STAT_countpx (O0OOOO0000O00O000 .values ,"严重伤害")),该元素死亡数量 =("伤害",lambda O0O00O00OO00O0000 :STAT_countpx (O0O00O00OO00O0000 .values ,"死亡")),该元素单位个数 =("单位名称","nunique"),该元素单位列表 =("单位名称",STAT_countx ),).reset_index ()#line:5242
				O0OO0O000O00O0O0O =O000OO000O0OOO000 .groupby (["产品类别","规整后品类"]).agg (所有元素总数量 =(OO0OOO00OO0000OOO ,"count"),所有元素严重伤害数 =("伤害",lambda OOO0O0OO0OO00OOOO :STAT_countpx (OOO0O0OO0OO00OOOO .values ,"严重伤害")),所有元素死亡数量 =("伤害",lambda O000O0O0O0O0OOO00 :STAT_countpx (O000O0O0O0O0OOO00 .values ,"死亡")),)#line:5247
				if len (O0OO0O000O00O0O0O )>1 :#line:5248
					text .insert (END ,"注意，产品类别有两种，产品名称规整疑似不正确！")#line:5249
				OO000O0000O0OO000 =pd .merge (OO000O0000O0OO000 ,O0OO0O000O00O0O0O ,on =["产品类别","规整后品类"],how ="left").reset_index ()#line:5251
		except :#line:5253
			text .insert (END ,"\n目前结果为未进行名称规整的结果！\n")#line:5254
			OO000O0000O0OO000 =O000OO000O0OOO000 .groupby (OOOO0OOO0O0OO0OOO ).agg (该元素总数量 =(O0000OO0000000OOO ,"count"),该元素严重伤害数 =("伤害",lambda OOO0O0OOO00OOO0O0 :STAT_countpx (OOO0O0OOO00OOO0O0 .values ,"严重伤害")),该元素死亡数量 =("伤害",lambda OO00OOO00OO0OO00O :STAT_countpx (OO00OOO00OO0OO00O .values ,"死亡")),该元素单位个数 =("单位名称","nunique"),该元素单位列表 =("单位名称",STAT_countx ),).reset_index ()#line:5261
			O0OO0O000O00O0O0O =O000OO000O0OOO000 .groupby (OOO0OO00OOO0OO000 ).agg (所有元素总数量 =(OO0OOO00OO0000OOO ,"count"),所有元素严重伤害数 =("伤害",lambda OOO0000OOOOOO0O00 :STAT_countpx (OOO0000OOOOOO0O00 .values ,"严重伤害")),所有元素死亡数量 =("伤害",lambda OOO0000OOOO0O0O00 :STAT_countpx (OOO0000OOOO0O0O00 .values ,"死亡")),)#line:5267
			OO000O0000O0OO000 =pd .merge (OO000O0000O0OO000 ,O0OO0O000O00O0O0O ,on =OOO0OO00OOO0OO000 ,how ="left").reset_index ()#line:5271
		O0OO0O000O00O0O0O =O0OO0O000O00O0O0O [(O0OO0O000O00O0O0O ["所有元素总数量"]>=3 )].reset_index ()#line:5273
		O000OO000OOOOOO00 =[]#line:5274
		if ("产品名称"not in O0OO0O000O00O0O0O .columns )and ("规整后品类"not in O0OO0O000O00O0O0O .columns ):#line:5276
			O0OO0O000O00O0O0O ["产品名称"]=O0OO0O000O00O0O0O ["产品类别"]#line:5277
		if "规整后品类"not in O0OO0O000O00O0O0O .columns :#line:5283
			O0OO0O000O00O0O0O ["规整后品类"]="不适用"#line:5284
		O0O000O00OOOO00O0 =0 #line:5287
		OO00OO0OO0O0O0000 =int (len (O0OO0O000O00O0O0O ))#line:5288
		for OOOOO0OO0OO0OO00O ,O0O0O000OOO00O0O0 ,OO000O00000OO00O0 ,OOO00OOO0000O0OO0 in zip (O0OO0O000O00O0O0O ["规整后品类"],O0OO0O000O00O0O0O ["产品类别"],O0OO0O000O00O0O0O [OO0OOO00OO0000OOO ],O0OO0O000O00O0O0O ["所有元素总数量"]):#line:5289
			O0O000O00OOOO00O0 +=1 #line:5290
			if (time .time ()-OOOO000O00O000O00 )>3 :#line:5291
				root .attributes ("-topmost",True )#line:5292
				PROGRAM_change_schedule (O0O000O00OOOO00O0 ,OO00OO0OO0O0O0000 )#line:5293
				root .attributes ("-topmost",False )#line:5294
			O000OO000O00OOOOO =O000OO000O0OOO000 [(O000OO000O0OOO000 [OO0OOO00OO0000OOO ]==OO000O00000OO00O0 )].copy ()#line:5295
			OOOO0OO0OOO0000OO ["SELECT"]=OOOO0OO0OOO0000OO .apply (lambda OO0O000O0OOO0O000 :((OOOOO0OO0OO0OO00O in OO0O000O0OOO0O000 ["适用范围"])or (OO0O000O0OOO0O000 ["适用范围"]in O0O0O000OOO00O0O0 )),axis =1 )#line:5296
			OOO0OOO0O0O000OOO =OOOO0OO0OOO0000OO [(OOOO0OO0OOO0000OO ["SELECT"]==True )].reset_index ()#line:5297
			if len (OOO0OOO0O0O000OOO )>0 :#line:5298
				for O0O0O0OO0O0O00O00 ,O00OOO0O00000O0OO ,OO00OO00O0OO0O00O in zip (OOO0OOO0O0O000OOO ["值"].values ,OOO0OOO0O0O000OOO ["查找位置"].values ,OOO0OOO0O0O000OOO ["排除值"].values ):#line:5300
					O00O00OOO000OO0OO =O000OO000O00OOOOO .copy ()#line:5301
					O00OOO0OOO0OOO00O =TOOLS_get_list (O0O0O0OO0O0O00O00 )[0 ]#line:5302
					OO00O00OOOOOOOO00 ="关键字查找列"#line:5303
					O00O00OOO000OO0OO [OO00O00OOOOOOOO00 ]=""#line:5304
					for O00OO0000OO00OO00 in TOOLS_get_list (O00OOO0O00000O0OO ):#line:5305
						O00O00OOO000OO0OO [OO00O00OOOOOOOO00 ]=O00O00OOO000OO0OO [OO00O00OOOOOOOO00 ]+O00O00OOO000OO0OO [O00OO0000OO00OO00 ].astype ("str")#line:5306
					O00O00OOO000OO0OO .loc [O00O00OOO000OO0OO [OO00O00OOOOOOOO00 ].str .contains (O0O0O0OO0O0O00O00 ,na =False ),"关键字"]=O00OOO0OOO0OOO00O #line:5308
					if str (OO00OO00O0OO0O00O )!="nan":#line:5311
						O00O00OOO000OO0OO =O00O00OOO000OO0OO .loc [~O00O00OOO000OO0OO ["关键字查找列"].str .contains (OO00OO00O0OO0O00O ,na =False )].copy ()#line:5312
					if (len (O00O00OOO000OO0OO ))<1 :#line:5315
						continue #line:5316
					for OO0O0OO00OOOOO00O in zip (O00O00OOO000OO0OO [O0000OO0000000OOO ].drop_duplicates ()):#line:5318
						try :#line:5321
							if OO0O0OO00OOOOO00O [0 ]!=OO0OOOOO000O000O0 [1 ]:#line:5322
								continue #line:5323
						except :#line:5324
							pass #line:5325
						O00000O0O0OO0O00O ={"合并列":{OO00O00OOOOOOOO00 :O00OOO0O00000O0OO },"等于":{OO0OOO00OO0000OOO :OO000O00000OO00O0 ,O0000OO0000000OOO :OO0O0OO00OOOOO00O [0 ]},"不等于":{},"包含":{OO00O00OOOOOOOO00 :O0O0O0OO0O0O00O00 },"不包含":{OO00O00OOOOOOOO00 :OO00OO00O0OO0O00O }}#line:5333
						O000000OO000O000O =STAT_PPR_ROR_1 (O0000OO0000000OOO ,str (OO0O0OO00OOOOO00O [0 ]),"关键字查找列",O0O0O0OO0O0O00O00 ,O00O00OOO000OO0OO )+(O0O0O0OO0O0O00O00 ,OO00OO00O0OO0O00O ,O00OOO0O00000O0OO ,OO000O00000OO00O0 ,OO0O0OO00OOOOO00O [0 ],str (O00000O0O0OO0O00O ))#line:5335
						if O000000OO000O000O [1 ]>0 :#line:5337
							OO00000OO0000O000 =pd .DataFrame (columns =["特定关键字","出现频次","占比","ROR值","ROR值的95%CI下限","PRR值","PRR值的95%CI下限","卡方值","四分表","关键字组合","排除值","关键字查找列",OO0OOO00OO0000OOO ,O0000OO0000000OOO ,"报表定位"])#line:5339
							OO00000OO0000O000 .loc [0 ]=O000000OO000O000O #line:5340
							O000OO000OOOOOO00 .append (OO00000OO0000O000 )#line:5341
		O0O0O0OO0O0OOOOO0 =pd .concat (O000OO000OOOOOO00 )#line:5345
		O0O0O0OO0O0OOOOO0 =pd .merge (OO000O0000O0OO000 ,O0O0O0OO0O0OOOOO0 ,on =[OO0OOO00OO0000OOO ,O0000OO0000000OOO ],how ="right")#line:5349
		O0O0O0OO0O0OOOOO0 =O0O0O0OO0O0OOOOO0 .reset_index (drop =True )#line:5350
		del O0O0O0OO0O0OOOOO0 ["index"]#line:5351
		if len (O0O0O0OO0O0OOOOO0 )>0 :#line:5352
			O0O0O0OO0O0OOOOO0 ["风险评分"]=0 #line:5353
			O0O0O0OO0O0OOOOO0 ["报表类型"]="ROR"#line:5354
			O0O0O0OO0O0OOOOO0 .loc [(O0O0O0OO0O0OOOOO0 ["出现频次"]>=3 ),"风险评分"]=O0O0O0OO0O0OOOOO0 ["风险评分"]+3 #line:5355
			O0O0O0OO0O0OOOOO0 .loc [(O0O0O0OO0O0OOOOO0 ["ROR值的95%CI下限"]>1 ),"风险评分"]=O0O0O0OO0O0OOOOO0 ["风险评分"]+1 #line:5356
			O0O0O0OO0O0OOOOO0 .loc [(O0O0O0OO0O0OOOOO0 ["PRR值的95%CI下限"]>1 ),"风险评分"]=O0O0O0OO0O0OOOOO0 ["风险评分"]+1 #line:5357
			O0O0O0OO0O0OOOOO0 ["风险评分"]=O0O0O0OO0O0OOOOO0 ["风险评分"]+O0O0O0OO0O0OOOOO0 ["该元素单位个数"]/100 #line:5358
			O0O0O0OO0O0OOOOO0 =O0O0O0OO0O0OOOOO0 .sort_values (by ="风险评分",ascending =[False ],na_position ="last").reset_index (drop =True )#line:5359
		print ("耗时：",(time .time ()-OOOO000O00O000O00 ))#line:5365
		return O0O0O0OO0O0OOOOO0 #line:5366
	def df_chiyouren (O000O00O0OO0O000O ):#line:5372
		""#line:5373
		O0OOOO0OOO0O00OO0 =O000O00O0OO0O000O .df .copy ().reset_index (drop =True )#line:5374
		O0OOOO0OOO0O00OO0 ["总报告数"]=data ["报告编码"].copy ()#line:5375
		O0OOOO0OOO0O00OO0 .loc [(O0OOOO0OOO0O00OO0 ["持有人报告状态"]=="待评价"),"总待评价数量"]=data ["报告编码"]#line:5376
		O0OOOO0OOO0O00OO0 .loc [(O0OOOO0OOO0O00OO0 ["伤害"]=="严重伤害"),"严重伤害报告数"]=data ["报告编码"]#line:5377
		O0OOOO0OOO0O00OO0 .loc [(O0OOOO0OOO0O00OO0 ["持有人报告状态"]=="待评价")&(O0OOOO0OOO0O00OO0 ["伤害"]=="严重伤害"),"严重伤害待评价数量"]=data ["报告编码"]#line:5378
		O0OOOO0OOO0O00OO0 .loc [(O0OOOO0OOO0O00OO0 ["持有人报告状态"]=="待评价")&(O0OOOO0OOO0O00OO0 ["伤害"]=="其他"),"其他待评价数量"]=data ["报告编码"]#line:5379
		O00000OO000OO00O0 =O0OOOO0OOO0O00OO0 .groupby (["上市许可持有人名称"]).aggregate ({"总报告数":"nunique","总待评价数量":"nunique","严重伤害报告数":"nunique","严重伤害待评价数量":"nunique","其他待评价数量":"nunique"})#line:5382
		O00000OO000OO00O0 ["严重伤害待评价比例"]=round (O00000OO000OO00O0 ["严重伤害待评价数量"]/O00000OO000OO00O0 ["严重伤害报告数"]*100 ,2 )#line:5387
		O00000OO000OO00O0 ["总待评价比例"]=round (O00000OO000OO00O0 ["总待评价数量"]/O00000OO000OO00O0 ["总报告数"]*100 ,2 )#line:5390
		O00000OO000OO00O0 ["总报告数"]=O00000OO000OO00O0 ["总报告数"].fillna (0 )#line:5391
		O00000OO000OO00O0 ["总待评价比例"]=O00000OO000OO00O0 ["总待评价比例"].fillna (0 )#line:5392
		O00000OO000OO00O0 ["严重伤害报告数"]=O00000OO000OO00O0 ["严重伤害报告数"].fillna (0 )#line:5393
		O00000OO000OO00O0 ["严重伤害待评价比例"]=O00000OO000OO00O0 ["严重伤害待评价比例"].fillna (0 )#line:5394
		O00000OO000OO00O0 ["总报告数"]=O00000OO000OO00O0 ["总报告数"].astype (int )#line:5395
		O00000OO000OO00O0 ["总待评价比例"]=O00000OO000OO00O0 ["总待评价比例"].astype (int )#line:5396
		O00000OO000OO00O0 ["严重伤害报告数"]=O00000OO000OO00O0 ["严重伤害报告数"].astype (int )#line:5397
		O00000OO000OO00O0 ["严重伤害待评价比例"]=O00000OO000OO00O0 ["严重伤害待评价比例"].astype (int )#line:5398
		O00000OO000OO00O0 =O00000OO000OO00O0 .sort_values (by =["总报告数","总待评价比例"],ascending =[False ,False ],na_position ="last")#line:5401
		if "场所名称"in O0OOOO0OOO0O00OO0 .columns :#line:5403
			O0OOOO0OOO0O00OO0 .loc [(O0OOOO0OOO0O00OO0 ["审核日期"]=="未填写"),"审核日期"]=3000 -12 -12 #line:5404
			O0OOOO0OOO0O00OO0 ["报告时限"]=pd .Timestamp .today ()-pd .to_datetime (O0OOOO0OOO0O00OO0 ["审核日期"])#line:5405
			O0OOOO0OOO0O00OO0 ["报告时限2"]=45 -(pd .Timestamp .today ()-pd .to_datetime (O0OOOO0OOO0O00OO0 ["审核日期"])).dt .days #line:5406
			O0OOOO0OOO0O00OO0 ["报告时限"]=O0OOOO0OOO0O00OO0 ["报告时限"].dt .days #line:5407
			O0OOOO0OOO0O00OO0 .loc [(O0OOOO0OOO0O00OO0 ["报告时限"]>45 )&(O0OOOO0OOO0O00OO0 ["伤害"]=="严重伤害")&(O0OOOO0OOO0O00OO0 ["持有人报告状态"]=="待评价"),"待评价且超出当前日期45天（严重）"]=1 #line:5408
			O0OOOO0OOO0O00OO0 .loc [(O0OOOO0OOO0O00OO0 ["报告时限"]>45 )&(O0OOOO0OOO0O00OO0 ["伤害"]=="其他")&(O0OOOO0OOO0O00OO0 ["持有人报告状态"]=="待评价"),"待评价且超出当前日期45天（其他）"]=1 #line:5409
			O0OOOO0OOO0O00OO0 .loc [(O0OOOO0OOO0O00OO0 ["报告时限"]>30 )&(O0OOOO0OOO0O00OO0 ["伤害"]=="死亡")&(O0OOOO0OOO0O00OO0 ["持有人报告状态"]=="待评价"),"待评价且超出当前日期30天（死亡）"]=1 #line:5410
			O0OOOO0OOO0O00OO0 .loc [(O0OOOO0OOO0O00OO0 ["报告时限2"]<=1 )&(O0OOOO0OOO0O00OO0 ["伤害"]=="严重伤害")&(O0OOOO0OOO0O00OO0 ["报告时限2"]>0 )&(O0OOOO0OOO0O00OO0 ["持有人报告状态"]=="待评价"),"严重待评价且只剩1天"]=1 #line:5412
			O0OOOO0OOO0O00OO0 .loc [(O0OOOO0OOO0O00OO0 ["报告时限2"]>1 )&(O0OOOO0OOO0O00OO0 ["报告时限2"]<=3 )&(O0OOOO0OOO0O00OO0 ["伤害"]=="严重伤害")&(O0OOOO0OOO0O00OO0 ["持有人报告状态"]=="待评价"),"严重待评价且只剩1-3天"]=1 #line:5413
			O0OOOO0OOO0O00OO0 .loc [(O0OOOO0OOO0O00OO0 ["报告时限2"]>3 )&(O0OOOO0OOO0O00OO0 ["报告时限2"]<=5 )&(O0OOOO0OOO0O00OO0 ["伤害"]=="严重伤害")&(O0OOOO0OOO0O00OO0 ["持有人报告状态"]=="待评价"),"严重待评价且只剩3-5天"]=1 #line:5414
			O0OOOO0OOO0O00OO0 .loc [(O0OOOO0OOO0O00OO0 ["报告时限2"]>5 )&(O0OOOO0OOO0O00OO0 ["报告时限2"]<=10 )&(O0OOOO0OOO0O00OO0 ["伤害"]=="严重伤害")&(O0OOOO0OOO0O00OO0 ["持有人报告状态"]=="待评价"),"严重待评价且只剩5-10天"]=1 #line:5415
			O0OOOO0OOO0O00OO0 .loc [(O0OOOO0OOO0O00OO0 ["报告时限2"]>10 )&(O0OOOO0OOO0O00OO0 ["报告时限2"]<=20 )&(O0OOOO0OOO0O00OO0 ["伤害"]=="严重伤害")&(O0OOOO0OOO0O00OO0 ["持有人报告状态"]=="待评价"),"严重待评价且只剩10-20天"]=1 #line:5416
			O0OOOO0OOO0O00OO0 .loc [(O0OOOO0OOO0O00OO0 ["报告时限2"]>20 )&(O0OOOO0OOO0O00OO0 ["报告时限2"]<=30 )&(O0OOOO0OOO0O00OO0 ["伤害"]=="严重伤害")&(O0OOOO0OOO0O00OO0 ["持有人报告状态"]=="待评价"),"严重待评价且只剩20-30天"]=1 #line:5417
			O0OOOO0OOO0O00OO0 .loc [(O0OOOO0OOO0O00OO0 ["报告时限2"]>30 )&(O0OOOO0OOO0O00OO0 ["报告时限2"]<=45 )&(O0OOOO0OOO0O00OO0 ["伤害"]=="严重伤害")&(O0OOOO0OOO0O00OO0 ["持有人报告状态"]=="待评价"),"严重待评价且只剩30-45天"]=1 #line:5418
			del O0OOOO0OOO0O00OO0 ["报告时限2"]#line:5419
			OOOOO00OO000OOO00 =(O0OOOO0OOO0O00OO0 .groupby (["上市许可持有人名称"]).aggregate ({"待评价且超出当前日期45天（严重）":"sum","待评价且超出当前日期45天（其他）":"sum","待评价且超出当前日期30天（死亡）":"sum","严重待评价且只剩1天":"sum","严重待评价且只剩1-3天":"sum","严重待评价且只剩3-5天":"sum","严重待评价且只剩5-10天":"sum","严重待评价且只剩10-20天":"sum","严重待评价且只剩20-30天":"sum","严重待评价且只剩30-45天":"sum"}).reset_index ())#line:5421
			O00000OO000OO00O0 =pd .merge (O00000OO000OO00O0 ,OOOOO00OO000OOO00 ,on =["上市许可持有人名称"],how ="outer",)#line:5422
			O00000OO000OO00O0 ["待评价且超出当前日期45天（严重）"]=O00000OO000OO00O0 ["待评价且超出当前日期45天（严重）"].fillna (0 )#line:5423
			O00000OO000OO00O0 ["待评价且超出当前日期45天（严重）"]=O00000OO000OO00O0 ["待评价且超出当前日期45天（严重）"].astype (int )#line:5424
			O00000OO000OO00O0 ["待评价且超出当前日期45天（其他）"]=O00000OO000OO00O0 ["待评价且超出当前日期45天（其他）"].fillna (0 )#line:5425
			O00000OO000OO00O0 ["待评价且超出当前日期45天（其他）"]=O00000OO000OO00O0 ["待评价且超出当前日期45天（其他）"].astype (int )#line:5426
			O00000OO000OO00O0 ["待评价且超出当前日期30天（死亡）"]=O00000OO000OO00O0 ["待评价且超出当前日期30天（死亡）"].fillna (0 )#line:5427
			O00000OO000OO00O0 ["待评价且超出当前日期30天（死亡）"]=O00000OO000OO00O0 ["待评价且超出当前日期30天（死亡）"].astype (int )#line:5428
			O00000OO000OO00O0 ["严重待评价且只剩1天"]=O00000OO000OO00O0 ["严重待评价且只剩1天"].fillna (0 )#line:5430
			O00000OO000OO00O0 ["严重待评价且只剩1天"]=O00000OO000OO00O0 ["严重待评价且只剩1天"].astype (int )#line:5431
			O00000OO000OO00O0 ["严重待评价且只剩1-3天"]=O00000OO000OO00O0 ["严重待评价且只剩1-3天"].fillna (0 )#line:5432
			O00000OO000OO00O0 ["严重待评价且只剩1-3天"]=O00000OO000OO00O0 ["严重待评价且只剩1-3天"].astype (int )#line:5433
			O00000OO000OO00O0 ["严重待评价且只剩3-5天"]=O00000OO000OO00O0 ["严重待评价且只剩3-5天"].fillna (0 )#line:5434
			O00000OO000OO00O0 ["严重待评价且只剩3-5天"]=O00000OO000OO00O0 ["严重待评价且只剩3-5天"].astype (int )#line:5435
			O00000OO000OO00O0 ["严重待评价且只剩5-10天"]=O00000OO000OO00O0 ["严重待评价且只剩5-10天"].fillna (0 )#line:5436
			O00000OO000OO00O0 ["严重待评价且只剩5-10天"]=O00000OO000OO00O0 ["严重待评价且只剩5-10天"].astype (int )#line:5437
			O00000OO000OO00O0 ["严重待评价且只剩10-20天"]=O00000OO000OO00O0 ["严重待评价且只剩10-20天"].fillna (0 )#line:5438
			O00000OO000OO00O0 ["严重待评价且只剩10-20天"]=O00000OO000OO00O0 ["严重待评价且只剩10-20天"].astype (int )#line:5439
			O00000OO000OO00O0 ["严重待评价且只剩20-30天"]=O00000OO000OO00O0 ["严重待评价且只剩20-30天"].fillna (0 )#line:5440
			O00000OO000OO00O0 ["严重待评价且只剩20-30天"]=O00000OO000OO00O0 ["严重待评价且只剩20-30天"].astype (int )#line:5441
			O00000OO000OO00O0 ["严重待评价且只剩30-45天"]=O00000OO000OO00O0 ["严重待评价且只剩30-45天"].fillna (0 )#line:5442
			O00000OO000OO00O0 ["严重待评价且只剩30-45天"]=O00000OO000OO00O0 ["严重待评价且只剩30-45天"].astype (int )#line:5443
		O00000OO000OO00O0 ["总待评价数量"]=O00000OO000OO00O0 ["总待评价数量"].fillna (0 )#line:5445
		O00000OO000OO00O0 ["总待评价数量"]=O00000OO000OO00O0 ["总待评价数量"].astype (int )#line:5446
		O00000OO000OO00O0 ["严重伤害待评价数量"]=O00000OO000OO00O0 ["严重伤害待评价数量"].fillna (0 )#line:5447
		O00000OO000OO00O0 ["严重伤害待评价数量"]=O00000OO000OO00O0 ["严重伤害待评价数量"].astype (int )#line:5448
		O00000OO000OO00O0 ["其他待评价数量"]=O00000OO000OO00O0 ["其他待评价数量"].fillna (0 )#line:5449
		O00000OO000OO00O0 ["其他待评价数量"]=O00000OO000OO00O0 ["其他待评价数量"].astype (int )#line:5450
		OOOOO00OOO0OO0O00 =["总报告数","总待评价数量","严重伤害报告数","严重伤害待评价数量","其他待评价数量"]#line:5453
		O00000OO000OO00O0 .loc ["合计"]=O00000OO000OO00O0 [OOOOO00OOO0OO0O00 ].apply (lambda OOOO0O0OO0000OOO0 :OOOO0O0OO0000OOO0 .sum ())#line:5454
		O00000OO000OO00O0 [OOOOO00OOO0OO0O00 ]=O00000OO000OO00O0 [OOOOO00OOO0OO0O00 ].apply (lambda OO0O0OO0O00000O00 :OO0O0OO0O00000O00 .astype (int ))#line:5455
		O00000OO000OO00O0 .iloc [-1 ,0 ]="合计"#line:5456
		if "场所名称"in O0OOOO0OOO0O00OO0 .columns :#line:5458
			O00000OO000OO00O0 =O00000OO000OO00O0 .reset_index (drop =True )#line:5459
		else :#line:5460
			O00000OO000OO00O0 =O00000OO000OO00O0 .reset_index ()#line:5461
		if ini ["模式"]=="药品":#line:5463
			O00000OO000OO00O0 =O00000OO000OO00O0 .rename (columns ={"总待评价数量":"新的数量"})#line:5464
			O00000OO000OO00O0 =O00000OO000OO00O0 .rename (columns ={"严重伤害待评价数量":"新的严重的数量"})#line:5465
			O00000OO000OO00O0 =O00000OO000OO00O0 .rename (columns ={"严重伤害待评价比例":"新的严重的比例"})#line:5466
			O00000OO000OO00O0 =O00000OO000OO00O0 .rename (columns ={"总待评价比例":"新的比例"})#line:5467
			del O00000OO000OO00O0 ["其他待评价数量"]#line:5469
		O00000OO000OO00O0 ["报表类型"]="dfx_chiyouren"#line:5470
		return O00000OO000OO00O0 #line:5471
	def df_age (OOOO0O00000OOOOOO ):#line:5473
		""#line:5474
		OO000OO0O0OO0OOOO =OOOO0O00000OOOOOO .df .copy ()#line:5475
		OO000OO0O0OO0OOOO =OO000OO0O0OO0OOOO .drop_duplicates ("报告编码").copy ()#line:5476
		OOO000O000O0O0OO0 =pd .pivot_table (OO000OO0O0OO0OOOO .drop_duplicates ("报告编码"),values =["报告编码"],index ="年龄段",columns ="性别",aggfunc ={"报告编码":"nunique"},fill_value ="0",margins =True ,dropna =False ,).rename (columns ={"报告编码":"数量"}).reset_index ()#line:5477
		OOO000O000O0O0OO0 .columns =OOO000O000O0O0OO0 .columns .droplevel (0 )#line:5478
		OOO000O000O0O0OO0 ["构成比(%)"]=round (100 *OOO000O000O0O0OO0 ["All"]/len (OO000OO0O0OO0OOOO ),2 )#line:5479
		OOO000O000O0O0OO0 ["累计构成比(%)"]=OOO000O000O0O0OO0 ["构成比(%)"].cumsum ()#line:5480
		OOO000O000O0O0OO0 ["报表类型"]="年龄性别表"#line:5481
		return OOO000O000O0O0OO0 #line:5482
	def df_psur (OOO0O0OO000O0OO0O ,*O0O00OOO0O00OO000 ):#line:5484
		""#line:5485
		OO000OOOO00O0OO00 =OOO0O0OO000O0OO0O .df .copy ()#line:5486
		OOO0OO0000OO00OO0 =peizhidir +"0（范例）比例失衡关键字库.xls"#line:5487
		OOO0O0O000O0O00OO =len (OO000OOOO00O0OO00 .drop_duplicates ("报告编码"))#line:5488
		if "报告类型-新的"in OO000OOOO00O0OO00 .columns :#line:5492
			O00OOOOOO0O00O00O ="药品"#line:5493
		elif "皮损形态"in OO000OOOO00O0OO00 .columns :#line:5494
			O00OOOOOO0O00O00O ="化妆品"#line:5495
		else :#line:5496
			O00OOOOOO0O00O00O ="器械"#line:5497
		O0O00000O0OO00O0O =pd .read_excel (OOO0OO0000OO00OO0 ,header =0 ,sheet_name =O00OOOOOO0O00O00O )#line:5500
		OO0OO000000OO00O0 =(O0O00000O0OO00O0O .loc [O0O00000O0OO00O0O ["适用范围"].str .contains ("通用监测关键字|无源|有源",na =False )].copy ().reset_index (drop =True ))#line:5503
		try :#line:5506
			if O0O00OOO0O00OO000 [0 ]in ["特定品种","通用无源","通用有源"]:#line:5507
				OOOO0O0O0000O00O0 =""#line:5508
				if O0O00OOO0O00OO000 [0 ]=="特定品种":#line:5509
					OOOO0O0O0000O00O0 =O0O00000O0OO00O0O .loc [O0O00000O0OO00O0O ["适用范围"].str .contains (O0O00OOO0O00OO000 [1 ],na =False )].copy ().reset_index (drop =True )#line:5510
				if O0O00OOO0O00OO000 [0 ]=="通用无源":#line:5512
					OOOO0O0O0000O00O0 =O0O00000O0OO00O0O .loc [O0O00000O0OO00O0O ["适用范围"].str .contains ("通用监测关键字|无源",na =False )].copy ().reset_index (drop =True )#line:5513
				if O0O00OOO0O00OO000 [0 ]=="通用有源":#line:5514
					OOOO0O0O0000O00O0 =O0O00000O0OO00O0O .loc [O0O00000O0OO00O0O ["适用范围"].str .contains ("通用监测关键字|有源",na =False )].copy ().reset_index (drop =True )#line:5515
				if O0O00OOO0O00OO000 [0 ]=="体外诊断试剂":#line:5516
					OOOO0O0O0000O00O0 =O0O00000O0OO00O0O .loc [O0O00000O0OO00O0O ["适用范围"].str .contains ("体外诊断试剂",na =False )].copy ().reset_index (drop =True )#line:5517
				if len (OOOO0O0O0000O00O0 )<1 :#line:5518
					showinfo (title ="提示",message ="未找到相应的自定义规则，任务结束。")#line:5519
					return 0 #line:5520
				else :#line:5521
					OO0OO000000OO00O0 =OOOO0O0O0000O00O0 #line:5522
		except :#line:5524
			pass #line:5525
		try :#line:5529
			if O00OOOOOO0O00O00O =="器械"and O0O00OOO0O00OO000 [0 ]=="特定品种作为通用关键字":#line:5530
				OO0OO000000OO00O0 =O0O00OOO0O00OO000 [1 ]#line:5531
		except dddd :#line:5533
			pass #line:5534
		OO0O0O00O0O00O0OO =""#line:5537
		O00OOO0OOOOO000OO ="-其他关键字-不含："#line:5538
		for OO00O00O0O00OO00O ,OO0O0OOO0OOO000O0 in OO0OO000000OO00O0 .iterrows ():#line:5539
			O00OOO0OOOOO000OO =O00OOO0OOOOO000OO +"|"+str (OO0O0OOO0OOO000O0 ["值"])#line:5540
			OO0O0O0O00O0O0OO0 =OO0O0OOO0OOO000O0 #line:5541
		OO0O0O0O00O0O0OO0 [2 ]="通用监测关键字"#line:5542
		OO0O0O0O00O0O0OO0 [4 ]=O00OOO0OOOOO000OO #line:5543
		OO0OO000000OO00O0 .loc [len (OO0OO000000OO00O0 )]=OO0O0O0O00O0O0OO0 #line:5544
		OO0OO000000OO00O0 =OO0OO000000OO00O0 .reset_index (drop =True )#line:5545
		if ini ["模式"]=="器械":#line:5549
			OO000OOOO00O0OO00 ["关键字查找列"]=OO000OOOO00O0OO00 ["器械故障表现"].astype (str )+OO000OOOO00O0OO00 ["伤害表现"].astype (str )+OO000OOOO00O0OO00 ["使用过程"].astype (str )+OO000OOOO00O0OO00 ["事件原因分析描述"].astype (str )+OO000OOOO00O0OO00 ["初步处置情况"].astype (str )#line:5550
		else :#line:5551
			OO000OOOO00O0OO00 ["关键字查找列"]=OO000OOOO00O0OO00 ["器械故障表现"]#line:5552
		text .insert (END ,"\n药品查找列默认为不良反应表现,药品规则默认为通用规则。\n器械默认查找列为器械故障表现+伤害表现+使用过程+事件原因分析描述+初步处置情况，器械默认规则为无源通用规则+有源通用规则。\n")#line:5553
		OOOOO0000O0O0OOO0 =[]#line:5555
		for OO00O00O0O00OO00O ,OO0O0OOO0OOO000O0 in OO0OO000000OO00O0 .iterrows ():#line:5557
			O0O0OO0O0O00OO00O =OO0O0OOO0OOO000O0 ["值"]#line:5558
			if "-其他关键字-"not in O0O0OO0O0O00OO00O :#line:5560
				OOO0O000O00O00000 =OO000OOOO00O0OO00 .loc [OO000OOOO00O0OO00 ["关键字查找列"].str .contains (O0O0OO0O0O00OO00O ,na =False )].copy ()#line:5563
				if str (OO0O0OOO0OOO000O0 ["排除值"])!="nan":#line:5564
					OOO0O000O00O00000 =OOO0O000O00O00000 .loc [~OOO0O000O00O00000 ["关键字查找列"].str .contains (str (OO0O0OOO0OOO000O0 ["排除值"]),na =False )].copy ()#line:5566
			else :#line:5568
				OOO0O000O00O00000 =OO000OOOO00O0OO00 .loc [~OO000OOOO00O0OO00 ["关键字查找列"].str .contains (O0O0OO0O0O00OO00O ,na =False )].copy ()#line:5571
			OOO0O000O00O00000 ["关键字标记"]=str (O0O0OO0O0O00OO00O )#line:5572
			OOO0O000O00O00000 ["关键字计数"]=1 #line:5573
			if len (OOO0O000O00O00000 )>0 :#line:5579
				try :#line:5580
					O0000O00O0OO0O0O0 =pd .pivot_table (OOO0O000O00O00000 .drop_duplicates ("报告编码"),values =["关键字计数"],index ="关键字标记",columns ="伤害PSUR",aggfunc ={"关键字计数":"count"},fill_value ="0",margins =True ,dropna =False ,)#line:5590
				except :#line:5592
					O0000O00O0OO0O0O0 =pd .pivot_table (OOO0O000O00O00000 .drop_duplicates ("报告编码"),values =["关键字计数"],index ="关键字标记",columns ="伤害",aggfunc ={"关键字计数":"count"},fill_value ="0",margins =True ,dropna =False ,)#line:5602
				O0000O00O0OO0O0O0 =O0000O00O0OO0O0O0 [:-1 ]#line:5603
				O0000O00O0OO0O0O0 .columns =O0000O00O0OO0O0O0 .columns .droplevel (0 )#line:5604
				O0000O00O0OO0O0O0 =O0000O00O0OO0O0O0 .reset_index ()#line:5605
				if len (O0000O00O0OO0O0O0 )>0 :#line:5608
					O0OOO00O00O0OO0O0 =str (Counter (TOOLS_get_list0 ("use(器械故障表现).file",OOO0O000O00O00000 ,1000 ))).replace ("Counter({","{")#line:5609
					O0OOO00O00O0OO0O0 =O0OOO00O00O0OO0O0 .replace ("})","}")#line:5610
					O0OOO00O00O0OO0O0 =ast .literal_eval (O0OOO00O00O0OO0O0 )#line:5611
					O0000O00O0OO0O0O0 .loc [0 ,"事件分类"]=str (TOOLS_get_list (O0000O00O0OO0O0O0 .loc [0 ,"关键字标记"])[0 ])#line:5613
					O0000O00O0OO0O0O0 .loc [0 ,"该类别不良事件计数"]=str ({OOOOO000O000OOOOO :O000O0O0O0O0OO0OO for OOOOO000O000OOOOO ,O000O0O0O0O0OO0OO in O0OOO00O00O0OO0O0 .items ()if STAT_judge_x (str (OOOOO000O000OOOOO ),TOOLS_get_list (O0O0OO0O0O00OO00O ))==1 })#line:5614
					O0000O00O0OO0O0O0 .loc [0 ,"同时存在的其他类别不良事件计数"]=str ({O00OO00O0000O0000 :O0OO0O000O000OO00 for O00OO00O0000O0000 ,O0OO0O000O000OO00 in O0OOO00O00O0OO0O0 .items ()if STAT_judge_x (str (O00OO00O0000O0000 ),TOOLS_get_list (O0O0OO0O0O00OO00O ))!=1 })#line:5615
					if ini ["模式"]=="药品":#line:5626
						for O00OO000OO0O0OOO0 in ["SOC","HLGT","HLT","PT"]:#line:5627
							O0000O00O0OO0O0O0 [O00OO000OO0O0OOO0 ]=OO0O0OOO0OOO000O0 [O00OO000OO0O0OOO0 ]#line:5628
					if ini ["模式"]=="器械":#line:5629
						for O00OO000OO0O0OOO0 in ["国家故障术语集（大类）","国家故障术语集（小类）","IMDRF有关术语（故障）","国家伤害术语集（大类）","国家伤害术语集（小类）","IMDRF有关术语（伤害）"]:#line:5630
							O0000O00O0OO0O0O0 [O00OO000OO0O0OOO0 ]=OO0O0OOO0OOO000O0 [O00OO000OO0O0OOO0 ]#line:5631
					OOOOO0000O0O0OOO0 .append (O0000O00O0OO0O0O0 )#line:5634
		OO0O0O00O0O00O0OO =pd .concat (OOOOO0000O0O0OOO0 )#line:5635
		OO0O0O00O0O00O0OO =OO0O0O00O0O00O0OO .sort_values (by =["All"],ascending =[False ],na_position ="last")#line:5640
		OO0O0O00O0O00O0OO =OO0O0O00O0O00O0OO .reset_index ()#line:5641
		OO0O0O00O0O00O0OO ["All占比"]=round (OO0O0O00O0O00O0OO ["All"]/OOO0O0O000O0O00OO *100 ,2 )#line:5643
		OO0O0O00O0O00O0OO =OO0O0O00O0O00O0OO .rename (columns ={"All":"总数量","All占比":"总数量占比"})#line:5644
		try :#line:5645
			OO0O0O00O0O00O0OO =OO0O0O00O0O00O0OO .rename (columns ={"其他":"一般"})#line:5646
		except :#line:5647
			pass #line:5648
		try :#line:5650
			OO0O0O00O0O00O0OO =OO0O0O00O0O00O0OO .rename (columns ={" 一般":"一般"})#line:5651
		except :#line:5652
			pass #line:5653
		try :#line:5654
			OO0O0O00O0O00O0OO =OO0O0O00O0O00O0OO .rename (columns ={" 严重":"严重"})#line:5655
		except :#line:5656
			pass #line:5657
		try :#line:5658
			OO0O0O00O0O00O0OO =OO0O0O00O0O00O0OO .rename (columns ={"严重伤害":"严重"})#line:5659
		except :#line:5660
			pass #line:5661
		try :#line:5662
			OO0O0O00O0O00O0OO =OO0O0O00O0O00O0OO .rename (columns ={"死亡":"死亡(仅支持器械)"})#line:5663
		except :#line:5664
			pass #line:5665
		for O00OOO00O0OOO00OO in ["一般","新的一般","严重","新的严重"]:#line:5668
			if O00OOO00O0OOO00OO not in OO0O0O00O0O00O0OO .columns :#line:5669
				OO0O0O00O0O00O0OO [O00OOO00O0OOO00OO ]=0 #line:5670
		try :#line:5672
			OO0O0O00O0O00O0OO ["严重比"]=round ((OO0O0O00O0O00O0OO ["严重"].fillna (0 )+OO0O0O00O0O00O0OO ["死亡(仅支持器械)"].fillna (0 ))/OO0O0O00O0O00O0OO ["总数量"]*100 ,2 )#line:5673
		except :#line:5674
			OO0O0O00O0O00O0OO ["严重比"]=round ((OO0O0O00O0O00O0OO ["严重"].fillna (0 )+OO0O0O00O0O00O0OO ["新的严重"].fillna (0 ))/OO0O0O00O0O00O0OO ["总数量"]*100 ,2 )#line:5675
		OO0O0O00O0O00O0OO ["构成比"]=round ((OO0O0O00O0O00O0OO ["总数量"].fillna (0 ))/OO0O0O00O0O00O0OO ["总数量"].sum ()*100 ,2 )#line:5677
		if ini ["模式"]=="药品":#line:5679
			try :#line:5680
				OO0O0O00O0O00O0OO =OO0O0O00O0O00O0OO [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","构成比","严重比","事件分类","该类别不良事件计数","同时存在的其他类别不良事件计数","死亡(仅支持器械)","SOC","HLGT","HLT","PT"]]#line:5681
			except :#line:5682
				OO0O0O00O0O00O0OO =OO0O0O00O0O00O0OO [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","构成比","严重比","事件分类","该类别不良事件计数","同时存在的其他类别不良事件计数","SOC","HLGT","HLT","PT"]]#line:5683
		elif ini ["模式"]=="器械":#line:5684
			try :#line:5685
				OO0O0O00O0O00O0OO =OO0O0O00O0O00O0OO [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","构成比","严重比","事件分类","该类别不良事件计数","同时存在的其他类别不良事件计数","死亡(仅支持器械)","国家故障术语集（大类）","国家故障术语集（小类）","IMDRF有关术语（故障）","国家伤害术语集（大类）","国家伤害术语集（小类）","IMDRF有关术语（伤害）"]]#line:5686
			except :#line:5687
				OO0O0O00O0O00O0OO =OO0O0O00O0O00O0OO [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","构成比","严重比","事件分类","该类别不良事件计数","同时存在的其他类别不良事件计数","国家故障术语集（大类）","国家故障术语集（小类）","IMDRF有关术语（故障）","国家伤害术语集（大类）","国家伤害术语集（小类）","IMDRF有关术语（伤害）"]]#line:5688
		else :#line:5690
			try :#line:5691
				OO0O0O00O0O00O0OO =OO0O0O00O0O00O0OO [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","构成比","严重比","事件分类","该类别不良事件计数","同时存在的其他类别不良事件计数","死亡(仅支持器械)"]]#line:5692
			except :#line:5693
				OO0O0O00O0O00O0OO =OO0O0O00O0O00O0OO [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","构成比","严重比","事件分类","该类别不良事件计数","同时存在的其他类别不良事件计数"]]#line:5694
		for O0OO0O00000OOO0O0 ,OOO0O000000OOO00O in OO0OO000000OO00O0 .iterrows ():#line:5696
			OO0O0O00O0O00O0OO .loc [(OO0O0O00O0O00O0OO ["关键字标记"].astype (str )==str (OOO0O000000OOO00O ["值"])),"排除值"]=OOO0O000000OOO00O ["排除值"]#line:5697
		OO0O0O00O0O00O0OO ["排除值"]=OO0O0O00O0O00O0OO ["排除值"].fillna ("没有排除值")#line:5699
		for OO0OO000O0O0OOOOO in ["一般","新的一般","严重","新的严重","总数量","总数量占比","严重比"]:#line:5703
			OO0O0O00O0O00O0OO [OO0OO000O0O0OOOOO ]=OO0O0O00O0O00O0OO [OO0OO000O0O0OOOOO ].fillna (0 )#line:5704
		for OO0OO000O0O0OOOOO in ["一般","新的一般","严重","新的严重","总数量"]:#line:5706
			OO0O0O00O0O00O0OO [OO0OO000O0O0OOOOO ]=OO0O0O00O0O00O0OO [OO0OO000O0O0OOOOO ].astype (int )#line:5707
		OO0O0O00O0O00O0OO ["RPN"]="未定义"#line:5710
		OO0O0O00O0O00O0OO ["故障原因"]="未定义"#line:5711
		OO0O0O00O0O00O0OO ["可造成的伤害"]="未定义"#line:5712
		OO0O0O00O0O00O0OO ["应采取的措施"]="未定义"#line:5713
		OO0O0O00O0O00O0OO ["发生率"]="未定义"#line:5714
		OO0O0O00O0O00O0OO ["报表类型"]="PSUR"#line:5716
		return OO0O0O00O0O00O0OO #line:5717
	def df_psur2 (OO000OO0000OOO0O0 ,O0O00O0OO000OOO00 ,OOOOO0O000O0O0O0O ):#line:5720
		""#line:5721
		O00O0O00OO000O00O =OO000OO0000OOO0O0 .df .copy ()#line:5723
		O00O0O0OO00OO0O00 =len (O00O0O00OO000O00O )#line:5724
		if O0O00O0OO000OOO00 :#line:5728
			O00O00O00OOO00O0O =O0O00O0OO000OOO00 #line:5729
		else :#line:5730
			O00O00O00OOO00O0O ="透视列"#line:5731
			O00O0O00OO000O00O [O00O00O00OOO00O0O ]="未正确设置"#line:5732
		O00O0O00OO000O00O ["关键字查找列"]=O00O0O00OO000O00O [OOOOO0O000O0O0O0O ]#line:5736
		O0OO0OOOOO000000O =[]#line:5738
		O00O0O00OO000O00O [OOOOO0O000O0O0O0O ]=O00O0O00OO000O00O [OOOOO0O000O0O0O0O ].fillna ("未填写")#line:5739
		O00O0O00OO000O00O [OOOOO0O000O0O0O0O ]=O00O0O00OO000O00O [OOOOO0O000O0O0O0O ].str .replace ("*","",regex =False )#line:5740
		O000OO000O0OO00O0 ="use("+str (OOOOO0O000O0O0O0O )+").file"#line:5741
		OO000O0O00OOOOOO0 =str (Counter (TOOLS_get_list0 (O000OO000O0OO00O0 ,O00O0O00OO000O00O ,1000 ))).replace ("Counter({","{")#line:5742
		OO000O0O00OOOOOO0 =OO000O0O00OOOOOO0 .replace ("})","}")#line:5743
		OO000O0O00OOOOOO0 =ast .literal_eval (OO000O0O00OOOOOO0 )#line:5744
		O0OOO00O00O0O0O00 =pd .DataFrame .from_dict (OO000O0O00OOOOOO0 ,orient ="index",columns =["计数"]).reset_index ()#line:5745
		for OO0O0000000OO0000 ,OOO0000O0OO0000OO in O0OOO00O00O0O0O00 .iterrows ():#line:5747
			OOO0000OO00O0O00O =OOO0000O0OO0000OO ["index"]#line:5748
			OOOOO0OO0O0OOO00O =O00O0O00OO000O00O .loc [O00O0O00OO000O00O ["关键字查找列"].str .contains (OOO0000OO00O0O00O ,na =False )].copy ()#line:5749
			OOOOO0OO0O0OOO00O ["关键字标记"]=str (OOO0000OO00O0O00O )#line:5751
			OOOOO0OO0O0OOO00O ["关键字计数"]=1 #line:5752
			if len (OOOOO0OO0O0OOO00O )>0 :#line:5754
				OOOOO00000O0O0O0O =pd .pivot_table (OOOOO0OO0O0OOO00O ,values =["关键字计数"],index ="关键字标记",columns =O0O00O0OO000OOO00 ,aggfunc ={"关键字计数":"count"},fill_value ="0",margins =True ,dropna =False ,)#line:5764
				OOOOO00000O0O0O0O =OOOOO00000O0O0O0O [:-1 ]#line:5765
				OOOOO00000O0O0O0O .columns =OOOOO00000O0O0O0O .columns .droplevel (0 )#line:5766
				OOOOO00000O0O0O0O =OOOOO00000O0O0O0O .reset_index ()#line:5767
				if len (OOOOO00000O0O0O0O )>0 :#line:5770
					O0OO0OOOOO000000O .append (OOOOO00000O0O0O0O )#line:5771
		O00OO0O00000OOO00 =pd .concat (O0OO0OOOOO000000O )#line:5772
		O00OO0O00000OOO00 =O00OO0O00000OOO00 .sort_values (by =["All"],ascending =[False ],na_position ="last")#line:5777
		O00OO0O00000OOO00 =O00OO0O00000OOO00 .reset_index ()#line:5778
		O00OO0O00000OOO00 ["All占比"]=round (O00OO0O00000OOO00 ["All"]/O00O0O0OO00OO0O00 *100 ,2 )#line:5780
		O00OO0O00000OOO00 =O00OO0O00000OOO00 .rename (columns ={"All":"总数量","All占比":"总数量占比"})#line:5781
		O00OO0O00000OOO00 ["报表类型"]="DSUR"#line:5786
		del O00OO0O00000OOO00 ["index"]#line:5787
		try :#line:5788
			del O00OO0O00000OOO00 ["未正确设置"]#line:5789
		except :#line:5790
			pass #line:5791
		return O00OO0O00000OOO00 #line:5792
def A0000_Main ():#line:5801
	print ("")#line:5802
if __name__ =='__main__':#line:5804
	root =Tk .Tk ()#line:5807
	root .title (title_all )#line:5808
	try :#line:5809
		root .iconphoto (True ,PhotoImage (file =peizhidir +"0（范例）ico.png"))#line:5810
	except :#line:5811
		pass #line:5812
	sw_root =root .winfo_screenwidth ()#line:5813
	sh_root =root .winfo_screenheight ()#line:5815
	ww_root =700 #line:5817
	wh_root =620 #line:5818
	x_root =(sw_root -ww_root )/2 #line:5820
	y_root =(sh_root -wh_root )/2 #line:5821
	root .geometry ("%dx%d+%d+%d"%(ww_root ,wh_root ,x_root ,y_root ))#line:5822
	framecanvas =Frame (root )#line:5827
	canvas =Canvas (framecanvas ,width =680 ,height =30 )#line:5828
	canvas .pack ()#line:5829
	x =StringVar ()#line:5830
	out_rec =canvas .create_rectangle (5 ,5 ,680 ,25 ,outline ="silver",width =1 )#line:5831
	fill_rec =canvas .create_rectangle (5 ,5 ,5 ,25 ,outline ="",width =0 ,fill ="silver")#line:5832
	canvas .create_text (350 ,15 ,text ="总执行进度")#line:5833
	framecanvas .pack ()#line:5834
	try :#line:5841
		frame0 =ttk .Frame (root ,width =90 ,height =20 )#line:5842
		frame0 .pack (side =LEFT )#line:5843
		B_open_files1 =Button (frame0 ,text ="导入数据",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =TOOLS_allfileopen ,)#line:5854
		B_open_files1 .pack ()#line:5855
		B_open_files3 =Button (frame0 ,text ="数据查看",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (ori ,0 ,ori ),)#line:5870
		B_open_files3 .pack ()#line:5871
	except KEY :#line:5874
		pass #line:5875
	text =ScrolledText (root ,height =400 ,width =400 ,bg ="#FFFFFF")#line:5879
	text .pack (padx =5 ,pady =5 )#line:5880
	text .insert (END ,"\n 本程序适用于整理和分析国家医疗器械不良事件信息系统、国家药品不良反应监测系统和国家化妆品不良反应监测系统中导出的监测数据。如您有改进建议，请点击其-意见反馈。\n")#line:5883
	text .insert (END ,"\n\n")#line:5884
	setting_cfg =read_setting_cfg ()#line:5887
	generate_random_file ()#line:5888
	setting_cfg =open_setting_cfg ()#line:5889
	if setting_cfg ["settingdir"]==0 :#line:5890
		showinfo (title ="提示",message ="未发现默认配置文件夹，请选择一个。如该配置文件夹中并无配置文件，将生成默认配置文件。")#line:5891
		filepathu =filedialog .askdirectory ()#line:5892
		path =get_directory_path (filepathu )#line:5893
		update_setting_cfg ("settingdir",path )#line:5894
	setting_cfg =open_setting_cfg ()#line:5895
	random_number =int (setting_cfg ["sidori"])#line:5896
	input_number =int (str (setting_cfg ["sidfinal"])[0 :6 ])#line:5897
	day_end =convert_and_compare_dates (str (setting_cfg ["sidfinal"])[6 :14 ])#line:5898
	sid =random_number *2 +183576 #line:5899
	if input_number ==sid and day_end =="未过期":#line:5900
		usergroup ="用户组=1"#line:5901
		text .insert (END ,usergroup +"   有效期至：")#line:5902
		text .insert (END ,datetime .strptime (str (int (int (str (setting_cfg ["sidfinal"])[6 :14 ])/4 )),"%Y%m%d"))#line:5903
	else :#line:5904
		text .insert (END ,usergroup )#line:5905
	text .insert (END ,"\n配置文件路径："+setting_cfg ["settingdir"]+"\n")#line:5906
	peizhidir =str (setting_cfg ["settingdir"])+csdir .split ("pinggutools")[0 ][-1 ]#line:5907
	roox =Toplevel ()#line:5911
	tMain =threading .Thread (target =PROGRAM_showWelcome )#line:5912
	tMain .start ()#line:5913
	t1 =threading .Thread (target =PROGRAM_closeWelcome )#line:5914
	t1 .start ()#line:5915
	root .lift ()#line:5917
	root .attributes ("-topmost",True )#line:5918
	root .attributes ("-topmost",False )#line:5919
	root .mainloop ()#line:5923
	print ("done.")#line:5924
