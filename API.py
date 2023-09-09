import pandas as pd
import requests
from datetime import datetime, timedelta
import json
import scrapy




def fetch_subscription_changes():
    today = datetime.today().date().strftime("%Y-%m-%d")
    yesterday = (datetime.today() - timedelta(days=1)).date().strftime("%Y-%m-%d")

    #Burada sadece url değişikliği olur,diğerleri aynı olmalı.
    url = 'https://api.personaclick.com/subscriptions/changes'

    params = {
        "shop_id": '67818ecb062f3999771085f91706f1',
        "shop_secret": '462c97a7bb949b927d0fdccc7e200c22',
        "from": "01-01-2020",
        "to": today,
        "offset": 0,
        "event": 'unsubscribe',
        "limit": 20000
    }

    response = requests.get(url, params=params)

    return response
print(fetch_subscription_changes())

    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")

    data = response.json()

    if data is None or len(data) == 0:
        return pd.DataFrame(data=['NODATA'], columns=['Message'])

    relevant_columns = ['contact_type', 'contact', 'campaign_type', 'event', 'channel', 'datetime', 'ip']

    df = pd.DataFrame(data, columns=relevant_columns)

    df.to_excel('veriler.xlsx')

    df = df.rename(columns={
        'contact_type': 'List/CommunicationType',
        'contact': 'List/Subscriber',
        'campaign_type': 'ChannelCode',
        'event': 'Option',
        'channel': 'UserName',
        'datetime': 'List/RecordDate',
        'ip': 'List/SourceProcessId'
    })

    option_mapping = {'sms': '2', 'email': '2'}
    subscriber_type_mapping = {'sms': '1', 'email': '3'}

    df['Option'] = df['Option'].map(option_mapping)
    df['List/SubscriberType'] = df['List/CommunicationType'].map(subscriber_type_mapping)
    df['List/RecordDate'] = df['List/RecordDate'].apply(
        lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.000Z').strftime('%Y%m%d%H%M%S'))
    #df.loc[df['List/SubscriberType'] == '1', 'List/Subscriber'] = '9' + df['List/Subscriber']
    df = df[['List/Subscriber', 'List/RecordDate', 'List/SubscriberType', 'List/SourceProcessId']]
    df['CommunicationType'] = df['List/SubscriberType']
    df = df.drop_duplicates(subset=['List/Subscriber'])
    df.to_csv()
    return df
print(fetch_subscription_changes())


##########İstek##########

def GET_TST():
    # api-endpoint
    URL = ""

    # location given here
    location = ""

    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'address': location}

    # sending get request and saving the response as response object
    r = requests.get(url=URL, params=PARAMS)

    # extracting data in json format
    data = r.json()

    # extracting latitude, longitude and formatted address
    # of the first matching location
    latitude = data['results'][0]['geometry']['location']['lat']
    longitude = data['results'][0]['geometry']['location']['lng']
    formatted_address = data['results'][0]['formatted_address']

    # printing the output
    print("Latitude:%s\nLongitude:%s\nFormatted Address:%s"
          % (latitude, longitude, formatted_address))



##########Yollamak(POST)##########


def POST_TST():
    # api'ye gönderilecek veriler
    data = [
        {
            "CustomerCode": ,
            "Username": "admrebul4",
            "Password": "rebul@9928"
        },
    ]

    #Post yapılacak alanı bildiriyoruz.
    url = "https://adm.smartadm.net/webservice/api/session"
    #JSON formatında bir dosya olduğunu bildiriyoruz.
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            print("JSON veri başarıyla gönderildi!")
        else:
            print(f"İstek başarısız. Hata kodu: {response.status_code}")
            print(response.text)  # Hata ayrıntılarını yazdır

    except requests.exceptions.RequestException as e:
        print(f"Hata oluştu: {e}")
    return response
response=POST_TST()
print(response.json())



data = {
    "SessionId": "{{}}",
    "CommunicationTools": {
        "Msisdn": "905********"
    },
    "AuthorizationDetails": {
        "KvkkStore": {
            "Value": "1",
            "AuthorizationDate": ""
        },
        "KvkkProcess": {
            "Value": "1",
            "AuthorizationDate": ""
        },
        "KvkkShare": {
            "Value": "1",
            "AuthorizationDate": ""
        },
        "KvkkInternationalTransfer": {
            "Value": "1",
            "AuthorizationDate": ""
        },
        "EtkTcknStore": {
            "Value": "1",
            "AuthorizationDate": ""
        },
        "EtkTcknShare": {
            "Value": "1",
            "AuthorizationDate": ""
        },
        "EtkTcknSms": {
            "Value": "1",
            "AuthorizationDate": "",
            "AuthorizationSpecificData": {
                "IysRecordSource": "HS_WEB",
                "LimitType": "1",
                "LimitValue": "3"
            }
        },
        "EtkMsisdnStore": {
            "Value": "1",
            "AuthorizationDate": ""
        },
        "EtkMsisdnShare": {
            "Value": "1",
            "AuthorizationDate": ""
        },
        "EtkMsisdnSms": {
            "Value": "1",
            "AuthorizationDate": "",
            "AuthorizationSpecificData": {
                "IysRecordSource": "HS_WEB",
                "LimitType": "1",
                "LimitValue": "3"
            }
        },
        "EtkMsisdnCall": {
            "Value": "1",
            "AuthorizationDate": "",
            "AuthorizationSpecificData": {
                "IysRecordSource": "HS_WEB",
                "LimitType": "1",
                "LimitValue": "3"
            }
        },
        "EtkEMailAddressStore": {
            "Value": "1",
            "AuthorizationDate": ""
        },
        "EtkEMailAddressShare": {
            "Value": "1",
            "AuthorizationDate": ""
        },
        "EtkEMailAddressEMail": {
            "Value": "1",
            "AuthorizationDate": "",
            "AuthorizationSpecificData": {
                "IysRecordSource": "HS_WEB",
                "LimitType": "1",
                "LimitValue": "3"
            }
        }
    }
}


def send_post_request(data):
    api_url = "https://adm.smartadm.net/webservice/api/contactapiload"

    headers = {"Content-Type": "application/json"}

    try:
        # response = requests.post(api_url, json=data, headers=headers)

        # İsteğin başarılı olup olmadığını kontrol et
        response.raise_for_status()

        # Hata ayrıntıları bilgilendirmem
        if response.status_code == 200:
            print("POST isteği başarıyla gönderildi!")
        else:
            print(f"İstek başarısız. Hata kodu: {response.status_code}")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Hata oluştu:{e}")


# AuthorizationDetails içerisindeki her bir yetkilendirme detayı için POST isteği gönder
# AuthorizationDetails burada kendi içinde özellik barındıran json alt dosyası içinde bulunan verileri iterative() post yapıyoruz.
for auth_detail, auth_data in data["AuthorizationDetails"].items():
    response = send_post_request(api_url, auth_data)
    # print(response.json())
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(api_url, json=data, headers=headers)
        response.raise_for_status()  # İsteğin başarılı olup olmadığını kontrol et

        if response.status_code != 200:
            raise (f"Request failed with status code {response.status_code}")


        else:
            print(f"İstek başarısız. Hata kodu: {response.status_code}")
            print(response.text)  # Hata ayrıntılarını yazdır


    except requests.exceptions.RequestException as e:
        print(f"Hata oluştu: {e}")







# burada var olan authorization parametrelerini alacağım ve aşağıda apply içinde kullanmak üzere değerlendireceğim.

def generate_authorization_details(data):
    result_list = []
    for key, value in data.items():
        result_list.append({

            "AuthorizationDetails": {key: value}})
    return result_list


def fetch_subscription_changes():
    today = datetime.today().date().strftime("%Y-%m-%d")
    yesterday = (datetime.today() - timedelta(days=1)).date().strftime("%Y-%m-%d")

    # API'den verileri çekme
    url = 'https://api.personaclick.com/subscriptions/changes'

    params = {
        "shop_id": '',
        "shop_secret": '',
        "from": "",
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

    # relevant_columns = ['contact_type', 'contact', 'campaign_type', 'event', 'channel', 'datetime', 'ip']
    relevant_columns = ['authDet', 'contact_type', 'contact', 'campaign_type', 'event', 'channel', 'datetime', 'ip',
                        'Value', 'AuthorizationDate', 'AuthorizationSpecificData']
    # relevant_columns_diff=[]
    df = pd.DataFrame(data, columns=relevant_columns)
    df = df.rename(columns={
        'contact_type': 'List/CommunicationType',
        # 'contact': 'List/Subscriber',
        'contact': 'List/CommunicationTools',
        'campaign_type': 'ChannelCode',
        'event': 'Option',
        'channel': 'UserName',
        'datetime': 'List/RecordDate',
        'ip': 'List/SourceProcessId',
        'authDet': 'List/AuthorizationDetails',
        # 'commTool':'CommunicationTools/Msisdn',
        'value': '',
        'AuthorizationDate': '',
        'AuthorizationSpecificData': ''

    })
    # df.to_excel(r'C:\Users\nedim.kahraman\Desktop\veriler.xlsx')
    option_mapping = {'sms': '2', 'email': '2'}
    subscriber_type_mapping = {'sms': '1', 'email': '3'}
    df['Option'] = df['Option'].map(option_mapping)
    df['List/SubscriberType'] = df['List/CommunicationType'].map(subscriber_type_mapping)
    df['List/RecordDate'] = df['List/RecordDate'].apply(
        lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.000Z').strftime('%Y%m%d%H%M%S'))
    # Yerine yazılan alternatif kod ıskalama yapmıyor 90 telefon kodunu koyuyor.
    # df.loc[df['List/SubscriberType'] == '0', 'List/Subscriber'] = '90' + df['List/Subscriber']
    df['NewSubscriber'] = df.apply(
        lambda row: '90' + row['List/CommunicationTools'] if row['List/SubscriberType'] == '0' else row[
            'List/CommunicationTools'], axis=1)
    df = df[['List/CommunicationTools', 'List/RecordDate', 'List/SubscriberType', 'List/SourceProcessId']]
    # df['commTool'] = 'EMailAddress'
    df['SessionId'] = ''
    # df['List/AuthorizationDetails']=''
    # df['AuthorizationDetails']=generate_authorization_details(data)
    # df['AuthorizationDetails']=df[['list/value','list/AuthorizationDate','list/AuthorizationSpecificData']]
    df = df.drop_duplicates(subset=['List/CommunicationTools'])
    # DataFrame'i JSON formatına dönüştürme
    # Burada records ve table arasında deneme ile orient dizin görüntülemede daha mantıklı olmakta.
    json_data = df.to_json(orient='table')

    return json_data


# Fonksiyonu çağırarak JSON verisini alalım
result_json = fetch_subscription_changes()

# JSON çıktısını ekrana yazdıralım
print(result_json)






