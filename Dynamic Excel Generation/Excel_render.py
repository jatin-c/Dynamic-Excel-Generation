import pandas as pd
from pandas.core.indexes.datetimes import date_range
import seaborn as sns
import matplotlib.pyplot as plt
import calendar
import numpy as np
from datetime import datetime, timedelta
import uuid
import time

def master(engine,flag):
    json={}
    if flag=='P':
        query="select * from modicare where Company in ('Colorbar','Modi Enterprises','Modicare Foundation','24Seven');"
    elif flag=='R':
        query="select * from modicare where Company='Modicare Limited';"
    #query="select * from modicare;"
    #query="select * from modicare where `Base Location` in ('East Region','HO');"
    df_master=pd.read_sql(query,con=engine)
    json['namelist']=df_master['Agent Name'].to_list()
    json['company']=df_master['Company'].to_list()
    json['w_location']=df_master['Working Location'].to_list()
    json['b_location']=df_master['Base Location'].to_list()
    json['department']=df_master['Department'].to_list()
    #json['serial']=df_master['S.No.'].to_list()
    json['mac']=df_master['MAC User'].to_list()
    json['remark']=df_master['Remarks'].to_list()
    json['weekend']=df_master['Weekend'].to_list()
    json['name']=df_master['Name'].to_list()
    return json


def df_preprocess(df_sliced):
    try:
        df_sliced = df_sliced.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        print("sliced")
        df_sliced['Weekday']=df_sliced.apply(lambda x: calendar.day_name[datetime.strptime(x['date'],'%d-%m-%Y').weekday()],axis=1)
        print("weekday")
        df_sliced['UnproductiveTime(Readable)']=df_sliced.apply(lambda x: "{:%Hh %Mm}".format(timedelta(hours=float(x['unProductiveTime']))+datetime.min),axis=1)
        print("unprod")
        df_sliced['productiveTime(Readable)']=df_sliced.apply(lambda x: "{:%Hh %Mm}".format(timedelta(hours=float(x['productiveTime']))+datetime.min),axis=1)
        print("prod")
        df_sliced['IdleTime(Readable)']=df_sliced.apply(lambda x: "{:%Hh %Mm}".format(timedelta(hours=float(x['screenLockTime']))+datetime.min),axis=1)
        print("idletime")
        df_sliced['TotalTime(Readable)']=df_sliced.apply(lambda x: "{:%Hh %Mm}".format(timedelta(hours=float(x['systemUpTime']))+datetime.min),axis=1)
        print("totaltime")
        df_sliced['TotalActiveTime(Readable)']=df_sliced.apply(lambda x: "{:%Hh %Mm}".format(timedelta(hours=float(x['onScreenTime']))+datetime.min),axis=1)
        print("totalactive")
        df_sliced['OfflineTime']=df_sliced.apply(lambda x: x['totalInactiveTime']+x['sessionBreakTime'],axis=1)
        print("offile")
        df_sliced['OfflineTime(Readable)']=df_sliced.apply(lambda x: "{:%Hh %Mm}".format(timedelta(hours=float(x['OfflineTime']))+datetime.min),axis=1)
        print("offlineread")
        df_sliced['Firstlogin']=df_sliced.apply(lambda x: "NaT" if x['loginTime1']=='NA'else datetime.fromtimestamp(int(x['loginTime1'][:10])).strftime("%I:%M %p"),axis=1)
        print("firstlog")
        df_sliced['lastlogin']=df_sliced.apply(lambda x: "NaT" if x['loginTime2']=='NA'else datetime.fromtimestamp(int(x['loginTime2'][:10])).strftime("%I:%M %p"),axis=1)
        print("lastlog")
        df_sliced['Firstlogout']=df_sliced.apply(lambda x: "NaT" if x['logoutTime1']=='NA'else datetime.fromtimestamp(int(x['logoutTime1'][:10])).strftime("%I:%M %p"),axis=1)
        print("firstlogout")
        df_sliced['lastlogout']=df_sliced.apply(lambda x: "NaT" if x['logoutTime2']=='NA'else datetime.fromtimestamp(int(x['logoutTime2'][:10])).strftime("%I:%M %p"),axis=1)
        print("lastlogout")
        filterd_e=df_sliced.filter(['date','Weekday','UnproductiveTime(Readable)','productiveTime(Readable)','IdleTime(Readable)','TotalTime(Readable)','TotalActiveTime(Readable)','OfflineTime(Readable)','Firstlogin','lastlogin','Firstlogout','lastlogout'],axis=1)
        print("filtered")
        return filterd_e
    except Exception as e:
        err={}
        err['error']=str(e)+" Inside function pre_process"
        return err


def x_month(client, db_x, idd):
    try:
        df_x=pd.DataFrame()
        for i in idd:
            query='select * from "agent_productivity_stats" where "agentid"={idd}'.format(idd=repr(str(i)))
            df1=client.query(query, database=db_x[0])
            if bool(df1):
                df_x=df1['agent_productivity_stats'].copy()
                print()
                df_x = df_x.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
                #df_x['Dates']=df_x.apply(lambda x: datetime.fromtimestamp(int(x['date'][:10])).strftime('%d-%m-%Y'),axis=1)
                df_x.reset_index(inplace=True)
                df_x['date']=df_x.apply(lambda x: datetime.fromtimestamp(int(x['date'][:10])).strftime('%d-%m-%Y'),axis=1)
            else:
                pass
        if df_x.empty:
            return False
        else:
            return df_x
    except Exception as e:
        return [str(e)+"inside function x_month"]

def csv_json(wk,client,db_x,idd):
    json={}
    df_month=x_month(client,db_x,idd)
    if type(df_month)==list:
        return df_month
    else:
        if type(df_month)==bool:
            return False
        else:
            df_norm=df_preprocess(df_month)
            if type(df_norm)==dict:
                return df_norm
            else:
                df_norm['Weekends']=df_norm.apply(lambda x: 'Y' if x['Weekday'] in wk.split('/') else 'N',axis=1)
                lst_flgn=df_norm['Firstlogin'].to_list()
                lst_flout=df_norm['Firstlogout'].to_list()
                lst_llgn=df_norm['lastlogin'].to_list()
                lst_llout=df_norm['lastlogout'].to_list()
                json['productivetime_list']=df_norm['productiveTime(Readable)'].to_list()
                json['unproductivetime_list']=df_norm['UnproductiveTime(Readable)'].to_list()
                json['idletime_list']=df_norm['IdleTime(Readable)'].to_list()
                json['logintime_list']=[j if i=='NaT' else i for i, j in zip(lst_flgn, lst_llgn)]
                json['logouttime_list']=[k if l=='NaT' else l for k, l in zip(lst_flout, lst_llout)]
                json['date_list']=df_norm['date'].to_list()
                json['weekday_list']=df_norm['Weekday'].to_list()
                json['totaltime_list']=df_norm['TotalTime(Readable)'].to_list()
                json['totalactivetime_list']=df_norm['TotalActiveTime(Readable)'].to_list()
                json['offlinetime_list']=df_norm['OfflineTime(Readable)'].to_list()
                json['weekends']=df_norm['Weekends'].to_list()
                return json


def previous_slice(client,prev_db,prev_dt, idd):
    try:
        query='select * from "agent_productivity_stats" where "agentid"={idd}'.format(idd=repr(str(idd)))
        df1=client.query(query, database=prev_db[0])
        print(df1)
        if bool(df1):
            print("previous slice begin")
            df_x=df1['agent_productivity_stats'].copy()
            df_x = df_x.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            df_x.reset_index(inplace=True)
            df_x['date']=df_x.apply(lambda x: datetime.fromtimestamp(int(x['date'][:10])).strftime('%d-%m-%Y'),axis=1)
            df_y=df_x[df_x['date']==str(prev_dt[0])].copy()
            if df_y.empty:
                return False
            else:
                return df_y
        else:
            return False
    except Exception as e:
        err={}
        err['error']=str(e)+"Inside previous slice"
        return err



def prev_day(namelist,a_name,company,location,weekend,depart,client,df_mstr,prev_db, prev_dt):
    date_list=[]
    firstlogin=[]
    firstlogout=[]
    lastlogin=[]
    lastlogout=[]
    totaltime=[]
    totalactive=[]
    offlinetime=[]
    productive=[]
    unproductive=[]
    idle=[]
    day_list=[]
    namelst=[]
    comp_lst=[]
    b_loc=[]
    wk_lst=[]
    depart_lst=[]
    try:
        for name2, name, comp, loc, wk, depar in zip(namelist,a_name,company,location,weekend,depart):
            df_idd=df_mstr[df_mstr['agentname']==name2].copy()
            if df_idd.empty:
                pass
            else:
                idd=df_idd['agentid'].values[0]
                df_prev=previous_slice(client,prev_db,prev_dt,idd)
                if type(df_prev)==dict:
                    return df_prev
                else:
                    if type(df_prev)==bool:
                        wk_lst.append("Not Available")
                        date_list.append(prev_dt[0])
                        day_list.append('Not Available')
                        firstlogin.append("Not Available")
                        firstlogout.append("Not Available")
                        lastlogin.append("Not Available")
                        lastlogout.append("Not Available")
                        totaltime.append("Not Available")
                        offlinetime.append("Not Available")
                        totalactive.append("Not Available")
                        productive.append("Not Available")
                        unproductive.append("Not Available")
                        idle.append("Not Available")
                        namelst.append(name)
                        comp_lst.append(comp)
                        depart_lst.append(depar)
                        b_loc.append(loc)
                    else:
                        df_norm=df_preprocess(df_prev)
                        if type(df_norm)==dict:
                            return df_norm
                        else:
                            if df_norm['Weekday'].values[0] in wk.split("/"):
                                wk_lst.append('Y')
                            else:
                                wk_lst.append('N')
                            date_list.append(df_norm['date'].values[0])
                            day_list.append(df_norm['Weekday'].values[0])
                            firstlogin.append(df_norm['Firstlogin'].values[0])
                            firstlogout.append(df_norm['Firstlogout'].values[0])
                            lastlogin.append(df_norm['lastlogin'].values[0])
                            lastlogout.append(df_norm['lastlogout'].values[0])
                            totaltime.append(df_norm['TotalTime(Readable)'].values[0])
                            offlinetime.append(df_norm['OfflineTime(Readable)'].values[0])
                            totalactive.append(df_norm['TotalActiveTime(Readable)'].values[0])
                            productive.append(df_norm['productiveScreentime(Readable)'].values[0])
                            unproductive.append(df_norm['UnproductiveScreentime(Readable)'].values[0])
                            idle.append(df_norm['Idletime(Readable)'].values[0])
                            namelst.append(name)
                            comp_lst.append(comp)
                            depart_lst.append(depar)
                            b_loc.append(loc)

        login=[k if l=='NaT' else l for k, l in zip(firstlogin, lastlogin)]
        logout=[k if l=='NaT' else l for k, l in zip(firstlogout, lastlogout)]

        main = pd.DataFrame({
            'Agent Name':namelst,
            'Group':comp_lst,
            'Base Location':b_loc,
            'Department':depart_lst,
            'Date':date_list,
            'Day':day_list,
            'Login Time':login,
            'Logout Time':logout,
            'Total Time':totaltime,
            'Total Active Time':totalactive,
            'Producitve Time':productive,
            'UnProducitve Time':unproductive,
            'Idle Time':idle,
            'Offline Time':offlinetime,
            'Weekend':wk_lst
            })
        main.index= main.index+1
        main.index = main.index.rename('S.No.')
        return main
    except Exception as e:
        err={}
        err['error']=str(e)
        return err
