import time
from datetime import datetime
import numpy as np
import pyodbc
import pandas as pd
from creds import *


## data framedeki nan değerleri sql'e göre doldurur..
def df_replaceNan(df):
    for col in df.columns:
        col_type = df[col].dtype
        if col_type in ['datetime64[ns]']:
            df[col].fillna("1900-01-01", inplace=True)
        if col_type in ['int64', 'float64']:
            df[col].fillna(0, inplace=True)
    df2 = df.replace(np.nan, '', regex=True)
    del df
    return df2


### sql sorgusu yürütür.. (insert, update, delete)
"+"
def exec_sql_query(query):
    con_20 = pyodbc.connect(con_20d365)
    cur_20 = con_20.cursor()
    cur_20.execute(f""" {query} """)
    con_20.commit()
    # print('silindi..')


### data frame'den sql'e hızlı insert : kolon adlarının aynı olması gerekiyor..
"+"
def df2sql(df, table_name):
    "!Fazladan bir atama yapılmış!"
    t1 = datetime.now()
    tuples = [tuple(x) for x in df.to_numpy()]
    col_names = '' + ','.join(list(df.columns)) + ''
    col_params = len(df.columns) * '?,'
    query = "INSERT INTO %s(%s) VALUES (%s)" % (table_name, col_names, col_params[:len(col_params) - 1])
    try:
        cn = pyodbc.connect(con_20d365)
        crsr = cn.cursor()
        crsr.fast_executemany = True
        crsr.executemany(query, tuples)
        crsr.commit()
        crsr.close()
        cn.close()
        # t2 = datetime.now()
        # print(table_name, " sure : " ,t2-t1)
    # except :
    except Exception as e:
        print(e)


"!!!sql üzerinde sorun olduğunda okuma işlemi yapabilir miyiz?!!!"
"+."
def sql2df(query):
    con = pyodbc.connect(con_20d365)
    df = pd.read_sql(query, con)
    return df


### sql sorgu sonucunu tuple olarak döndürür
"+"
def get_query_result(query):
    cn = pyodbc.connect(con_20d365)
    cur = cn.cursor()
    cur.execute(query)
    r = cur.fetchall()
    return r




