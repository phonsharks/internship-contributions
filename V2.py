import pyodbc
import json
import urllib.request
import base64


"+"
def encode_auth(api_key, api_secret):

    
    Encodes the API key and API secret in Base64 format.

    Args:
        api_key (str): The API key.
        api_secret (str): The API secret.

    Returns:
        str: The encoded credentials.
    

    auth_str = f"{api_key}:{api_secret}"
    auth_bytes = auth_str.encode('ascii')
    auth_b64_bytes = base64.b64encode(auth_bytes)
    auth_b64_str = auth_b64_bytes.decode('ascii')
    return auth_b64_str

"+"
def send_request(url, data, headers):

    
    Sends a POST request to the given URL with the given data and headers.

    Args:
        url (str): The URL to send the request to.
        data (bytes): The data to include in the request body.
        headers (dict): The headers to include in the request.

    Returns:
        str: The response content.
        int: The flag indicating whether the request was successful (1) or not (2).
        str: The error message, if any.
    

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

"-"
def insert_into_database(cursor, cnxn, row, error_m, flag):

    
    Inserts the response data into the SQL table if it doesn't already exist.

    Args:
        cursor (pyodbc.Cursor): The cursor object used to execute SQL commands.
        cnxn (pyodbc.Connection): The database connection object.
        row (pyodbc.Row): The row of data to insert.
        error_m (str): The error message to insert.
        flag (int): The flag indicating whether the request was successful (1) or not (2).
    

    cursor.execute(
        f'IF NOT EXISTS (SELECT * FROM zt_trendyol_supplier_invoice_links WHERE OrderNumber=\'{row.OrderNumber}\')\n'
        f'            INSERT INTO zt_trendyol_supplier_invoice_links (Flag, OrderNumber, DocumentNumber, Description, shipmentPackageId, invoiceLink, OfficeCode, InvoiceHeaderID, LastUpdatedTime)\n'
        f'            VALUES ({flag}, \'{row.OrderNumber}\', \'{row.DocumentNumber}\', \'{error_m}\', \'{row.shipmentPackageId}\', \'{row.invoiceLink}\', \'{row.OfficeCode}\', \'{row.InvoiceHeaderID}\', GETDATE())\n'
        f'        ELSE IF (SELECT Flag FROM zt_trendyol_supplier_invoice_links WHERE OrderNumber=\'{row.OrderNumber}\') != 1\n'
        f'            UPDATE zt_trendyol_supplier_invoice_links\n'
        f'            SET Flag = {flag}, Description = \'{error_m}\', invoiceLink = \'{row.invoiceLink}\',InvoiceHeaderID = \'{row.InvoiceHeaderID}\', LastUpdatedTime = GETDATE()\n'
        f'            WHERE OrderNumber = \'{row.OrderNumber}\' AND Flag != 1\n'
        f'        ')
    cnxn.commit()

"+"
def process_rows():
    
    Retrieves data from SQL server and makes API requests.
    
    # Map of OfficeCode values to API key, API secret, and Satıcı Id
    api_key_map = {
        'O-15': {'api_key': '', 'api_secret': '', 'satici_id': ''},
        'O-998': {'api_key': '', 'api_secret': '', 'satici_id': ''},
        'O-999': {'api_key': '', 'api_secret': '', 'satici_id': ''},
        'O-5': {'api_key': '', 'api_secret': '', 'satici_id': ''}
    }

    # Connect to the SQL server and execute the SQL query
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=10.10.5.21;DATABASE=V3_JcrAS;UID=sa;PWD=***')
    cursor = cnxn.cursor()
    cursor.execute('''select * from trendyol_supplier_invoice_links''')

    # Retrieve the data and make API requests
    for row in cursor.fetchall():
        office_code = row.OfficeCode
        api_key = api_key_map.get(office_code, {}).get('api_key')
        api_secret = api_key_map.get(office_code, {}).get('api_secret')
        satici_id = api_key_map.get(office_code, {}).get('satici_id')

        # Encode API key and API secret in Base64 format
        auth_b64_str = encode_auth(api_key, api_secret)

        # Include encoded credentials in the Authorization header
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

        # Send the POST request to the API
        response_content, flag, error_m = send_request(url, data, headers)

        # Insert the response data into the SQL table if it doesn't already exist
        insert_into_database(cursor, cnxn, row, error_m, flag)

        print(f"Row inserted for OrderNumber {row.OrderNumber} with Flag={flag} ")