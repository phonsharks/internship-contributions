import pandas as pd
import requests
from datetime import datetime, timedelta
import json
import sys
import numpy as np


#burada var olan authorization parametrelerini alacağım ve aşağıda apply içinde kullanmak üzere değerlendireceğim.



data={
        "KvkkStore":{
            "Value":0,
            "AuthorizationDate":""
        },
        "KvkkProcess":{
            "Value":0,
            "AuthorizationDate":""
        },
        "KvkkShare":{
            "Value":0,
            "AuthorizationDate":""
        },
        "KvkkInternationalTransfer":{
            "Value":0,
            "AuthorizationDate":""
        },
        "EtkTcknStore":{
            "Value":0,
            "AuthorizationDate":""
        },
        "EtkTcknShare":{
            "Value":0,
            "AuthorizationDate":""
        },
        "EtkTcknSms":{
            "Value":0,
            "AuthorizationDate":"",
            "AuthorizationSpecificData":{
                "IysRecordSource":"HS_WEB",
                "LimitType":"1",
                "LimitValue":"3"
            }
        },
        "EtkMsisdnStore":{
            "Value":0,
            "AuthorizationDate":""
        },
        "EtkMsisdnShare":{
            "Value":0,
            "AuthorizationDate":""
        },
        "EtkMsisdnSms":{
            "Value":0,
            "AuthorizationDate":"",
            "AuthorizationSpecificData":{
                "IysRecordSource":"HS_WEB",
                "LimitType":"1",
                "LimitValue":"3"
            }
        },
        "EtkMsisdnCall":{
            "Value":0,
            "AuthorizationDate":"",
            "AuthorizationSpecificData":{
                "IysRecordSource":"HS_WEB",
                "LimitType":"1",
                "LimitValue":"3"
            }
        },
        "EtkEMailAddressStore":{
            "Value":0,
            "AuthorizationDate":""
        },
        "EtkEMailAddressShare":{
            "Value":0,
            "AuthorizationDate":""
        },
        "EtkEMailAddressEMail":{
            "Value":0,
            "AuthorizationDate":"",
            "AuthorizationSpecificData":{
                "IysRecordSource":"HS_WEB",
                "LimitType":"1",
                "LimitValue":"3"
            }
        }
    
}




def generate_authorization_details(data):
    
    result_list = []
    key = frozenset(data.items())
    for item in data:
        for key, value in item.items():
            result_list.append({
                "AuthorizationDetails": {key: value}
            })
    return result_list


def fetch_subscription_changes():
    today = datetime.today().date().strftime("%Y-%m-%d")
    yesterday = (datetime.today() - timedelta(days=1)).date().strftime("%Y-%m-%d")

    # API'den verileri çekme
    url = 'https://api.personaclick.com/subscriptions/changes'
    
    params = {
        "shop_id": '',
        "shop_secret": '',
        "from": "01-01-2020",
        "to": today,
        "offset": 0,
        "event": 'unsubscribe',
        "limit": 20000
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")

    data = response.json()

    # JSON verisini pandas DataFrame'e dönüştürme
    if data is None or len(data) == 0:
        return pd.DataFrame(data=['NODATA'], columns=['Message'])
    
    #relevant_columns = ['contact_type', 'contact', 'campaign_type', 'event', 'channel', 'datetime', 'ip']
    relevant_columns = ['authDet','contact_type', 'contact', 'campaign_type', 'event', 'channel', 'datetime', 'ip','Value','AuthorizationDate','AuthorizationSpecificData']
    #relevant_columns_diff=[]
    df = pd.DataFrame(data, columns=relevant_columns)
    df = df.rename(columns={
        'contact_type': 'List/CommunicationType',
        #'contact': 'List/Subscriber',
        'contact': 'List/CommunicationTools',
        'campaign_type': 'ChannelCode',
        'event': 'Option',
        'channel': 'UserName',
        'datetime': 'List/RecordDate',
        'ip': 'List/SourceProcessId',
        'authDet':'List/AuthorizationDetails',
        #'commTool':'CommunicationTools/Msisdn',
        'value':'',
        'AuthorizationDate':'',
        'AuthorizationSpecificData':''
        
        
    })
    #df.to_excel(r'C:\Users\nedim.kahraman\Desktop\veriler.xlsx')
    option_mapping = {'sms': '2', 'email': '2'}
    subscriber_type_mapping = {'sms': '1', 'email': '3'}
    df['Option'] = df['Option'].map(option_mapping)
    df['List/SubscriberType'] = df['List/CommunicationType'].map(subscriber_type_mapping)
    df['List/RecordDate'] = df['List/RecordDate'].apply(
        lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.000Z').strftime('%Y%m%d%H%M%S'))
    'Yerine yazılan alternatif kod ıskalama yapmıyor 90 telefon kodunu koyuyor.Burada 3 adet farklı yol var'
    #df.loc[df['List/SubscriberType'] == '0', 'List/Subscriber'] = '90' + df['List/Subscriber']
    #df['NewSubscriber'] = df.apply(lambda row: '90' + row['List/CommunicationTools'] if row['List/SubscriberType'] == '0' else row['List/CommunicationTools'], axis=1)
    df['NewSubscriber'] = np.where(df['List/SubscriberType'] == '0', '90' + df['List/CommunicationTools'], df['List/CommunicationTools'])    
    df = df[['List/CommunicationTools', 'List/RecordDate', 'List/SubscriberType', 'List/SourceProcessId']]
    #df['commTool'] = 'EMailAddress'
    df['SessionId']='1428423117272642315'
    #df['List/AuthorizationDetails']=''
    #df['AuthorizationDetails']=generate_authorization_details(data)
    'Burada yukarıda yapılan tanımlamayı burada döndürmem gerek'
    #df['AuthorizationDetails']=df.apply(generate_authorization_details(data),axis=1)
    df['AuthorizationDetails']=''
    df = df.drop_duplicates(subset=['List/CommunicationTools'])
    # DataFrame'i JSON formatına dönüştürme
    #Burada records ve table arasında deneme ile orient dizin görüntülemede daha mantıklı olmakta.
    json_data = df.to_json(orient='table')

    return json_data

# Fonksiyonu çağırarak JSON verisini alalım
result_json = fetch_subscription_changes()

# JSON çıktısını ekrana yazdıralım
print(result_json)






  