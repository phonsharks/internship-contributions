import pyodbc
import json
import base64
import urllib.request
from typing import Dict


class TrendyolInvoiceLinks:

    "+"
    def __init__(self, api_key_map: Dict):
        self.api_key_map = api_key_map

    "+"
    def encode_auth(self, api_key: str, api_secret: str) -> str:
        auth_str = f"{api_key}:{api_secret}"
        auth_bytes = auth_str.encode('ascii')
        auth_b64_bytes = base64.b64encode(auth_bytes)
        auth_b64_str = auth_b64_bytes.decode('ascii')
        return auth_b64_str

    "+"
    def send_request(self, url: str, data: bytes, headers: Dict) -> Dict:
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        try:
            response = urllib.request.urlopen(req)
            response_content = response.read().decode('utf-8')
            error_m = 'Ok'
            flag = 1
        except urllib.error.HTTPError as e:
            error_m = str(e)
            if "409" in error_m:
                flag = 1
                print("Kayıt zaten işlemiş")
            else:
                flag = 2
                print(error_m)
            response_content = ''
        return response_content, flag, error_m

    "+"
    def insert_into_database(self, cursor, cnxn, row, error_m, flag):
        cursor.execute(
            f'''IF NOT EXISTS (SELECT * FROM zt_trendyol_supplier_invoice_links WHERE OrderNumber='{row.OrderNumber}')
                INSERT INTO zt_trendyol_supplier_invoice_links (Flag, OrderNumber, DocumentNumber, Description, shipmentPackageId, invoiceLink, OfficeCode, InvoiceHeaderID)
                VALUES ({flag}, '{row.OrderNumber}', '{row.DocumentNumber}', '{error_m}', '{row.shipmentPackageId}', '{row.invoiceLink}', '{row.OfficeCode}', '{row.InvoiceHeaderID}')
            ELSE IF (SELECT Flag FROM zt_trendyol_supplier_invoice_links WHERE OrderNumber='{row.OrderNumber}') != 1
                UPDATE zt_trendyol_supplier_invoice_links
                SET Flag = {flag}, Description = '{error_m}', invoiceLink = '{row.invoiceLink}',InvoiceHeaderID = '{row.InvoiceHeaderID}'
                WHERE OrderNumber = '{row.OrderNumber}' AND Flag != 1
            ''')
        cnxn.commit()

    "+"
    def process_rows(self):
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=10.10.5.21;DATABASE=V3_JcrAS;UID=sa;PWD**')
        cursor = cnxn.cursor()
        cursor.execute('''select * from trendyol_supplier_invoice_links''')

        for row in cursor.fetchall():
            office_code = row.OfficeCode
            api_key = self.api_key_map.get(office_code, {}).get('api_key')
            api_secret = self.api_key_map.get(office_code, {}).get('api_secret')
            satici_id = self.api_key_map.get(office_code, {}).get('satici_id')

            auth_b64_str = self.encode_auth(api_key, api_secret)

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Basic {auth_b64_str}'
            }

            payload = {
                "invoiceLink": row.invoiceLink,
                "shipmentPackageId": row.shipmentPackageId
            }
            data = json.dumps(payload).encode('utf-8')
            url = f'https://api.trendyol.com/sapigw/suppliers/{satici_id}/supplier-invoice-links'

            response_content, flag, error_m = self.send_request(url, data, headers)

            self.insert_into_database(cursor, cnxn, row, error_m, flag)