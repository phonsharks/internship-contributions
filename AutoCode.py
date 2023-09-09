import datetime as dt
import importlib
import os
import shutil
import time
from datetime import datetime

import pandas as pd
import pyodbc
import win32com.client as win32
from PIL import ImageGrab

con_string = '**;'
timeformat = "%y/%m/%d %H:%M:%S"


def emailgonder_outlook(email_to, email_cc, email_bcc, konu, govde, govde_ekleri, email_ekleri):
    outlook = win32.gencache.EnsureDispatch('Outlook.Application')
    # outlook.DisplayAlerts = False  # uyarıları gösterme..
    bugun = dt.datetime.today().strftime('%Y-%m-%d')
    new_mail = outlook.CreateItem(0)
    new_mail.To = ", ".join(email_to)
    new_mail.CC = ", ".join(email_cc)
    new_mail.BCC = ", ".join(email_bcc)
    new_mail.Subject = konu + ' ' + bugun
    #print("gövde ekleri alınıyor..")
    for govde_eki in govde_ekleri:
        new_mail.Attachments.Add(Source=govde_eki)
    for email_eki in email_ekleri:
        new_mail.Attachments.Add(email_eki)
    new_mail.HTMLBody = (govde)
    new_mail.Attachments
    new_mail.Send()
    # print('email gönderildi..')



#Hata mesajları için ekleme yapıldı.
def sql2df(query):
    try:
        con = pyodbc.connect(con_string)
        df = pd.read_sql(query, con)
        return df
    except pyodbc.Error as e:
        print(f"SQL hatası oluştu:{e}")
        return None
    #Her olası souçta finally kod bloğu çalışmalı...
    finally:
        con.close()
#Hata mesajları için ekleme yapıldı.
def get_query_result(query, con_string):
    try:
        con = pyodbc.connect(con_string)
        cur = con.cursor()
        cur.execute(query)
        r = cur.fetchall()
        return r
    except pyodbc.Error as e:
        print(f"SQL hatası oluştu:{e}")
        return None
    #hata olsun ya da olmasın bu kod dizini her zaman çalıştırılır.
    finally:
        con.close()
#Hata mesajları için ekleme yapıldı.
def exec_sql_query(query):
    try:
        con = pyodbc.connect(con_string)
        cur = con.cursor()
        cur.execute(f""" {query} """)
        con.commit()
        cur.close()
        con.close()
        print(query, ' yürütüldü..')
    except pyodbc.Error as e:
        print(f"SQL hatası oluştu:{e}")
    except Exception as e:
        print(f"Bir hata oluştu:{e}")
#Hata mesajları için ekleme yapıldı.
def dosyaguncelleme_gecensure(dosya):
    try:
        songuncelleme = os.path.getmtime(dosya)
        now = time.time()
        sure_dk = (now - songuncelleme) / 60
        return sure_dk
    except FileNotFoundError:
            print(f"Dosya bulunamadı:{dosya}")
    except Exception as e:
            print(f"Bir hata oluştu:{e}")
##Hata mesajları için ekleme yapıldı.
#Kopyalama işlemi sırasında oluşabilecek hatalar,diğer olası problemlerin referansı olacaktır.
def dosyakopyala(kaynakklasor, hedefklasor, dosya):
    try:
        if not os.path.exists(hedefklasor):
            os.makedirs(hedefklasor)
            shutil.copy(kaynakklasor + dosya, hedefklasor + dosya)
            print(dosya, ' kopyalandı..')
        else:
            shutil.copy(kaynakklasor + dosya, hedefklasor + dosya)
            print(dosya, ' kopyalandı..')
    except FileNotFoundError:
        print(f"Dosya bulunamadı: {kaynakklasor + dosya}")
        return 1
    except shutil.Error as e:
        print(f"Shutil hatası: {e}")
        return 2
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return 3
    return 0
##Hata mesajları için ekleme yapıldı.
def ExcelKapat():
    try:
        win32.GetActiveObject("Excel.Application")
        os.system('TASKKILL /F /IM excel.exe')
        print("Excel kapatıldı..")
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return 1























































































########################################################################################################################
"+"
def ExcelVer():  # visible=True):
    try:
        excel = win32.GetActiveObject("Excel.Application")
        print("Çalışan excel var")
    except:
        #vForDemand parametresi kod tarayarak yalnız ihtiyaç olduğunda oluşum yapar.
        excel = win32.gencache.EnsureDispatch('Excel.Application',bForDemand=True)
        excel.Interactive = False
        excel.Visible = False
        excel.DisplayAlerts = False # uyarıları gösterme..
        print('yeni excel açıldı..')
    return excel

email_ekleri = []
govde_ekleri = []
resimdosyalari = []
def RefreshSheet(sheet):
    try:
        sheet.Refresh()
        print(f"{sheet.Name} sayfası güncellendi.")
    except Exception as e:
        print(f"Hata: {e}")
def ExcelGuncelle(dosyayolu, dosyaadi, timeout, dosyaguncellemegecensure, dosyaguncelliksuresi, pivotguncelle):
    ###### excel güncelle
    excel = ExcelVer()
    if excel is None:
        print("Excel uygulaması başlatılamadı.")
        return
    wb = excel.Workbooks.Open(dosyayolu + dosyaadi)
    if dosyaguncellemegecensure >= dosyaguncelliksuresi:
        #wb.RefreshAll()
        for sheet in wb.Sheets:
            RefreshSheet(sheet)
        wb.Save()
        wb.Close()
        #güncelleme için gerekli zaman geçmesini sağlar ama işlemciyi de yorar.
        time.sleep(timeout)
        #excel hesaplamaları için gerekli ondan dolaylı etkinleştirdi.
        wb.EnableCalculation = True
        excel.Quit()
    if pivotguncelle == 1:
        #count = wb.Sheets.Count
        #for i in range(count):
            #ws = wb.Worksheets(i + 1)
            #ws.Unprotect()  # IF protected
            #pivotCount = ws.PivotTables().Count
            #for j in range(1, pivotCount + 1):
            for ws in wb.Worksheets:
                ws.Unprotect()
                for pt in ws.PivotTable():
                    pt.PivotCache().Refresh()
                try:
                    pt.PivotCache().Refresh()
                except Exception as e:
                    print(f"Error Code:{e}")
                'Burada yeni kodlara uyarlanarak yeni kodlar yazdım.'
        print(dosyaadi, ' dosya güncellendi..', dosyaguncellemegecensure, 'dk')
    if dosyaguncellemegecensure <= dosyaguncelliksuresi:
        print('dosyagüncel..', dosyaguncellemegecensure, 'dk')
    wb.Close(True, dosyayolu + dosyaadi)  # kaydet kapat..
    excel.Quit()

"-"
def ExcelEkAl(raporkodu, excelekle, pdfekle, resimekle, dosyayolu, dosyaadi):
    #excel açık olup oolmadığını kontrol eden fonksiyon.
    excel = ExcelVer()
    wb = excel.Workbooks.Open(dosyayolu + dosyaadi)
    if excelekle == 1:
        email_ekleri.append(dosyayolu + dosyaadi)

    ###### pdf ekle #######

    #burada ayrı bir fonksiyon oluşturdum,daha düzenlenebilir ve dinamik olmsı adına.
    def get_page_numbers_from_text(text):
        page_numbers = list(map(int, text.split("|")))
        return page_numbers

    if pdfekle != '0' and pdfekle != "":
        #pdfsayfalari = list(map(int, pdfekle.split("|")))
        print(pdfekle, get_page_numbers_from_text)
        pdfdosyayolu = os.path.splitext(dosyayolu + dosyaadi)[0][0:] + '.pdf'

        #hata mesajlarının görülebilmesi adına ayrı bir fonksiyonun içinde try-except oluşturdum...
        def remove_file(pdfdosyayolu):
            try:
                if os.path.isfile(pdfdosyayolu):
                    os.remove(pdfdosyayolu)
                    print(f"{pdfdosyayolu} dosyası silindi.")
                else:
                    print(f"{pdfdosyayolu} dosyası bulunamadı.")
            except Exception as e:
                print(f"Hata: {e}")
        print(remove_file(dosyayolu))
        excel.Worksheets[get_page_numbers_from_text].Select()
        excel.ActiveSheet.ExportAsFixedFormat(0, pdfdosyayolu)
        email_ekleri.append(dosyayolu + os.path.splitext(dosyaadi)[0][0:] + '.pdf')
        print(dosyaadi + '..PDF e dönüştürüldü..')

    ####### resimleri al #######
    "openpyxl kullanımı ile birlikte daha kısa olabilir!!"
    resimler = list(resimekle.split(","))
    if len(resimekle) > 6 and len(resimler) > 0:
        for resim in resimler:
            resimno = resimler.index(resim)
            l = resim.split("=")
            sayfa = int(l[0])
            aralik = l[1]
            ws_resim = wb.Worksheets(sayfa)
            win32c = win32.constants
            ws_resim.Range(aralik).CopyPicture(Format=win32c.xlBitmap)
            img = ImageGrab.grabclipboard()
            image_file = str(raporkodu) + "_" + str(sayfa) + str(resimno) + ".png"
            image_path = dosyayolu + image_file
            img.save(image_path)
            govde_ekleri.append(image_path)
            resimdosyalari.append(image_file)
            print(dosyaadi, resim, ' resim alındı..')
    wb.Close(True, dosyayolu + dosyaadi)  # kaydet kapat..
    excel.Quit()


# -------------------------------------------------------------------------------------------------------------------
#                                                RAPORLARI EMAİL İLE GÖNDERME
# -------------------------------------------------------------------------------------------------------------------
def raporgonder(raporkodu):
    ExcelKapat()
    try:
        sql = f"SELECT * FROM rapormaster WHERE RAPORKODU= '{raporkodu}'"
        rapormaster = get_query_result(sql)
        raporadi, execquery, emailgmetin, emailkonu, pythonfile, htmlekle = rapormaster[0][3], rapormaster[0][4], rapormaster[0][5], rapormaster[0][6], \
                                                               rapormaster[0][12], rapormaster[0][13]
        df_raporekleri = sql2df(f"SELECT * FROM raporekleri WHERE RAPORKODU= '{raporkodu}'")
        emailto_df = sql2df(
            f""" SELECT EMAIL FROM raporemailalicilari  WHERE AKTIF='EVET' AND TOCC= 'TO' AND RAPORKODU= '{raporkodu}' """)
        emailcc_df = sql2df(
            f""" SELECT EMAIL FROM raporemailalicilari  WHERE AKTIF='EVET' AND TOCC= 'CC' AND RAPORKODU= '{raporkodu}' """)
        emailbcc_df = sql2df(
            f""" SELECT EMAIL FROM raporemailalicilari  WHERE AKTIF='EVET' AND TOCC= 'BCC' AND RAPORKODU= '{raporkodu}' """)
        email_to = [";".join(emailto_df['EMAIL']) + ";"]
        email_cc = [";".join(emailcc_df['EMAIL']) + ";"]
        email_bcc = [";".join(emailbcc_df['EMAIL']) + ";"]
        #email_to = [""]
        #email_cc = [metin.gundogdu@rebul.com;]
        #email_bcc = [metin.gundogdu@rebul.com;]
        #gani.sengul@rebul.com;ilkan.ates@rebul.com;omer.sahin@rebul.com;

        govde_metni = emailgmetin
        #### PYTHON KODUNU ÇALIŞTIRMA : GÖVDE METNİ HTML AL
        
        if len(pythonfile) > 3 and pythonfile != '':
            pythonfilename = 'excelraporlama.' + pythonfile.split(".")[0]
            if len(pythonfilename) > 0 and pythonfilename != "":
                html_modul = importlib.import_module(pythonfilename)
                if htmlekle == 1:
                    govde_metni = govde_metni + html_modul.get_htmldata()
                    print(htmlekle, pythonfile, ' html data alındı..')
        else:
            print("pythonfile bos")

        #### SQL SORGUSUNU YÜRÜTME
        if len(execquery) > 10:
            exec_sql_query(execquery)

        #### EXCEL RAPOR EKLERİNİ HAZIRLA
        for index, row in df_raporekleri.iterrows():
            raporid = row["ID"]
            dosyayolu = row["DOSYAYOLU"].replace("/", '\\')
            dosyaadi = row["DOSYAADI"]
            excelekle = row["EXCELEKLE"]
            pdfekle = row["PDFEKLE"].replace(".", ",")
            resimekle = row["RESIMEKLE"]
            timeout = row["TIMEOUTSANIYE"]
            dosyaguncelliksuresi = row["GUNCELLEMESURESI"]
            pivotguncelle = row["PIVOTGUNCELLE"]

            ####  EXCEL ŞABLON DOSYASINI KOPYALA
            gonderilenklasoru = dosyayolu + 'gonderilen\\'
            dosyasonguncelleme_gecensure = dosyaguncelleme_gecensure(gonderilenklasoru + dosyaadi)
            if dosyasonguncelleme_gecensure >= dosyaguncelliksuresi:
                dosyakopyala(dosyayolu, gonderilenklasoru, dosyaadi)

            #### EKLERİ HAZIRLA : EXCELİ GÜNCELLE, PDF'e ÇEVİR, RESİM AL..
            ExcelGuncelle(gonderilenklasoru, dosyaadi, timeout, dosyasonguncelleme_gecensure, dosyaguncelliksuresi, pivotguncelle)
            ExcelEkAl(raporkodu, excelekle, pdfekle, resimekle, gonderilenklasoru, dosyaadi)


        #### GÖVDE METNİ OLUŞTURMA \ EXCEL'den ALINAN RESİMLER
        if len(resimekle) > 3:
            govde_metni = govde_metni + f"<h4> {raporadi} </h4>"
            for image in resimdosyalari:
                try:
                    govde_metni = govde_metni + f"<img src = {image} > <br /><br />"
                except Exception as e:
                    print(f"Hata: {e}")
        else:
            pass
            # govde_metni = ""
        # print(govde_metni)
        emailgonder_outlook(email_to, email_cc, email_bcc, emailkonu, govde_metni, govde_ekleri, email_ekleri)
        print(raporkodu, raporadi, 'email gönderildi..')
        govde_ekleri.clear()
        email_ekleri.clear()
        resimdosyalari.clear()
        dosyasonguncelleme_gecensure = 9999

    except Exception as e:
        print(e)

#Burada oluşabilecek hata kodunun nicel anlamda görüntülenmesi için bloklar eklendi...
#topluraporgonder(['bktest'])
def toplu_rapor_gonder(rapor_listesi):
    exec_sql_query("exec p_excelyukle_emailraporlari")
    for rapor in rapor_listesi:
        try:
            t1 = datetime.now()
            print(rapor, t1.strftime('%y-%m-%d %H:%M:%S'), ' başlatıldı...')
            raporgonder(rapor)
            t2 = datetime.now()
            sure = t2 - t1
            print(rapor, 'tamamlandı (süre:', str(sure)[0:7], ')')
        except Exception as e:
            print(f"Hata: {e}")



