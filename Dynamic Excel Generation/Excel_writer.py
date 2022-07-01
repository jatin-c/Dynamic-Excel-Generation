from Excel_render import master, csv_json, prev_day
from sqlalchemy import create_engine
import pandas as pd
import time
#from modules import pie_chart, stacked_chart, webusage, applications, evaluation_json, master
from sqlalchemy import create_engine
from pandas import ExcelWriter
import uuid
from datetime import date, datetime, timezone
from datetime import timedelta
from influxdb import InfluxDBClient, DataFrameClient
import psycopg2
def xlsx_write(flag):
    try:
        client = DataFrameClient(host='115.164.114.7', port=8086, username='root', password='xxxxxx',ssl=False, verify_ssl=False)
        engine = create_engine("mysql+pymysql://root:123456789@localhost/dlp", echo=True)
        conn = psycopg2.connect(dbname='indefendenterprise.5032548842',user = "postgres", password = "xxxxxx", host ="115.124.111.5" , port=5432, sslmode='require')
        conn.set_session(autocommit=True)
    except Exception as e:
        return str(e)

    today = date.today()
    yr = today.year
    mn= today.month
    print(yr,mn)
    #yesterday = today - timedelta(days = 1)
    #yes_mon=yesterday.month
    #yes_year=yesterday.year
    #prev_dt=[yesterday.strftime('%d-%m-%Y')]
    #datetimeObject = datetime.fromtimestamp(time.time(), timezone.utc)
    #print(datetimeObject.strftime("%d-%m-%Y"))
    #datetimeObject = datetimeObject.replace(tzinfo=None)
    #dt=datetimeObject-timedelta(days=1)
    #yes_mon=dt.month
    #yes_year=dt.year
    #prev_dt=[dt.strftime("%d-%m-%Y")]
    #print(prev_dt)

    dbs=client.get_list_database()

    #prev_db=[]
    db_x=[]

    for i in dbs:
        if str(mn) in i['name'].split("_") and str(yr) in i['name'].split("_"):
            db_x.append(i['name'])

    #for j in dbs:
        #if str(yes_mon) in j['name'].split("_") and str(yes_year) in j['name'].split("_"):
            #prev_db.append(j['name'])
    try:
        print("chlja bhai please")
        query="select agentid, agentname from agentmaster;"
        df_mstr=pd.read_sql(query,con=conn)
    except Exception as e:
        return str(e)+"during postgres"

    master_json=master(engine,flag)
    result =pd.DataFrame()
    prev_result=pd.DataFrame()
    try:
        for name2, name, comp, loc, wk, depar in zip(master_json['namelist'],master_json['name'],master_json['company'],master_json['b_location'],master_json['weekend'],master_json['department']):
            df_idd=df_mstr[df_mstr['agentname']==str(name2)].copy()
            print(df_idd)
            if df_idd.empty:
                pass
            else:
                idd=df_idd['agentid'].to_list()
                eval_json=csv_json(wk,client,db_x,idd)
                if type(eval_json)==list:
                    return eval_json[0]
                else:
                    if eval_json==False:
                        pass
                    else:
                        main = pd.DataFrame(
                            {
                            'Agent Name':name,
                            'Group':comp,
                            'Base Location':loc,
                            'Department':depar,
                            'Date':eval_json['date_list'],
                            'Day': eval_json['weekday_list'],
                            'Login Time': eval_json['logintime_list'],
                            'Logout Time': eval_json['logouttime_list'],
                            'Total Time':eval_json['totaltime_list'],
                            'Total Active Time':eval_json['totalactivetime_list'],
                            'Producitve Time':eval_json['productivetime_list'],
                            'UnProducitve Time':eval_json['unproductivetime_list'],
                            'Idle Time':eval_json['idletime_list'],
                            'Offline Time':eval_json['offlinetime_list'],
                            'Weekend':eval_json['weekends']
                            })
                        frames = [result,main]
                        result = pd.concat(frames)
                        df_prev=main.iloc[-2:-1]
                        pr_frames=[prev_result,df_prev]
                        prev_result=pd.concat(pr_frames)
    except Exception as e:
        return str(e)+"Inside xlsx_write()"
    #result.reset_index(inplace=True)
    #result.index=result.index + 1
    #result.index=result.index.rename('S.No.')
    #namelist=master_json['namelist']
    #company=master_json['company']
    #b_loc=master_json['b_location']
    #a_name=master_json['name']
    #wk_end=master_json['weekend']
    #depart=master_json['department']
    #previous_df=prev_day(namelist,a_name,company,b_loc,wk_end,depart,client,df_mstr,prev_db, prev_dt)

    #if type(previous_df)==dict:
    #    return previous_df['error']
    #else:
    result.index=result.index+1
    result.index=result.index.rename("S.No.")
    prev_result.index=prev_result.index+1
    prev_result.index=prev_result.index.rename("S.No.")
    df_lst=[prev_result,result]
    now_date=datetime.now().date()
    n_date=now_date.strftime('%Y-%m-%d')
    now_time=datetime.now().time()
    time_p =now_time.strftime('%I-%M%p')
    filepath='Daily_Productivity_Report_'+str(n_date)+"_"+str(time_p)+".xlsx"
    path="/home/centos/iassist/bot/dlpexcel/"+filepath
        #filename=str(uuid.UUID())+".xlsx"
    path_dict={}
    path_dict['filepath']=path
    path_dict['filename']=filepath 
    with ExcelWriter(path) as writer:
            for n, df in enumerate(df_lst):
                sheet=['Previous Day Report','Current Month Report']
                df.to_excel(writer, sheet[n],index=True)
            writer.save()
    return path_dict

#if __name__=='__main__':
    #rt=xlsx_write()
    #print(rt)
