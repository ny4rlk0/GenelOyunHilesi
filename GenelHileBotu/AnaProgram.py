# This Python file uses the following encoding: utf-8
from ctypes import Array
import os
#os.execute("pip install pyautogui opencv-python Pillow colorama")
from pyautogui import *
import numpy as np
import pyautogui,time,random, cv2, datetime
from PIL import ImageGrab
from colorama import Fore, init
import eklentiler.clashofclans as coc
import eklentiler.yardimci_kitaplik as yk

#Dosya yollar�
cwd = os.getcwd()+"\\";
ekran_tarama_sonuc_yolu=cwd+"\\resimler\\ekran_tarama.png";
#Kalibrasyon
cv2_tarama_yontemi=cv2.TM_CCOEFF_NORMED #cv2.TM_SQDIFF_NORMED
#Deneysel
yk.tiklama_kaydi=True;# t�klanan alanlar� k�rm�z� dikd�rtgen i�ine al�p klas�re kaydet

def cwd_ekle(konum):
    return cwd+konum
def clash_hile(): #basit iksir, kara iksir, altin toplama botu. 
    #��lem geciktirme
    coc.tiklama_gecikmesi=0.1 ### T�klamalar aras�nda ge�en s�re (Saniye cinsinden)
    coc.islem_gecikmesi=0.1    #32 ### Yap�lan i�lemler aras�nda ge�en s�re (Saniye cinsinden)
    coc.herseyi_tekrarlama_gecikmesi=30 #4200 #7200 #2 saat
    for x in range(5):
        #                       resim_yolu1,                                benzerlik y�zdesi,                             ekrana tiklansin mi, hangi fonksiyon ca�irdi ekrana ne yazalim,                              ekran g�r�nt�s�n� kaydet,   sadece ilk e�le�meye tikla,     ekran taramasini bu klas�re kaydet  cv2 tarama y�ntemi
        yk.hedef_bul(           cwd_ekle(coc.oyunu_tekrar_yukle_resim_yolu),coc.oyunu_tekrar_yukle_resim_benzerlik_yuzdesi,True,                yk.tarih_saat()+Fore.BLUE+" (coc) oyuna yeniden baglaniliyor."+Fore.WHITE,    cwd_ekle(coc.kayit_yolu),   False,                          ekran_tarama_sonuc_yolu,            cv2_tarama_yontemi)
        yk.hedef_bul(           cwd_ekle(coc.iksir_resim_yolu),             coc.iksir_resim_benzerlik_yuzdesi,             True,                yk.tarih_saat()+Fore.MAGENTA+" (coc) iksir"+Fore.WHITE+" toplandi.",          cwd_ekle(coc.kayit_yolu),   True,                           ekran_tarama_sonuc_yolu,            cv2_tarama_yontemi)
        if(yk.hedef_bul(        cwd_ekle(coc.yukselt_resim_yolu),           coc.yukselt_resim_benzerlik_yuzdesi,           False,                yk.tarih_saat()+Fore.LIGHTBLUE_EX+" (coc) tiklama sifirlandi."+Fore.WHITE,    cwd_ekle(coc.kayit_yolu),   False,                          ekran_tarama_sonuc_yolu,            cv2_tarama_yontemi)):
            yk.hedef_bul(           cwd_ekle(coc.sifirla_resim_yolu),             coc.sifirla_resim_benzerlik_yuzdesi,             True,                yk.tarih_saat()+Fore.LIGHTBLUE_EX+" (coc) tiklama sifirlandi."+Fore.WHITE,         cwd_ekle(coc.kayit_yolu),   False,                          ekran_tarama_sonuc_yolu,            cv2_tarama_yontemi)
        yk.hedef_bul(           cwd_ekle(coc.carpi_resim_yolu),             coc.carpi_resim_benzerlik_yuzdesi,             True,                yk.tarih_saat()+Fore.RED+" (coc) carpi tusuna basildi."+Fore.WHITE,           cwd_ekle(coc.kayit_yolu),   False,                          ekran_tarama_sonuc_yolu,            cv2_tarama_yontemi)
        yk.hedef_bul(           cwd_ekle(coc.altin_resim_yolu),             coc.altin_resim_benzerlik_yuzdesi,             True,                yk.tarih_saat()+Fore.YELLOW+" (coc) altin"+Fore.WHITE+" toplandi.",           cwd_ekle(coc.kayit_yolu),   True,                           ekran_tarama_sonuc_yolu,            cv2_tarama_yontemi)
        if(yk.hedef_bul(        cwd_ekle(coc.yukselt_resim_yolu),           coc.yukselt_resim_benzerlik_yuzdesi,           False,                yk.tarih_saat()+Fore.LIGHTBLUE_EX+" (coc) tiklama sifirlandi."+Fore.WHITE,    cwd_ekle(coc.kayit_yolu),   False,                          ekran_tarama_sonuc_yolu,            cv2_tarama_yontemi)):
                yk.hedef_bul(       cwd_ekle(coc.sifirla_resim_yolu),             coc.sifirla_resim_benzerlik_yuzdesi,             True,                yk.tarih_saat()+Fore.LIGHTBLUE_EX+" (coc) tiklama sifirlandi."+Fore.WHITE,         cwd_ekle(coc.kayit_yolu),   False,                          ekran_tarama_sonuc_yolu,            cv2_tarama_yontemi)
        yk.hedef_bul(           cwd_ekle(coc.tas_resim_yolu),             coc.tas_resim_benzerlik_yuzdesi,                 True,                yk.tarih_saat()+Fore.LIGHTGREEN_EX+" (coc) tas"+Fore.WHITE+" toplandi.",           cwd_ekle(coc.kayit_yolu),   True,                           ekran_tarama_sonuc_yolu,            cv2_tarama_yontemi)
        if(yk.hedef_bul(        cwd_ekle(coc.yukselt_resim_yolu),           coc.yukselt_resim_benzerlik_yuzdesi,           False,                yk.tarih_saat()+Fore.LIGHTBLUE_EX+" (coc) tiklama sifirlandi."+Fore.WHITE,    cwd_ekle(coc.kayit_yolu),   False,                          ekran_tarama_sonuc_yolu,            cv2_tarama_yontemi)):
                yk.hedef_bul(       cwd_ekle(coc.sifirla_resim_yolu),             coc.sifirla_resim_benzerlik_yuzdesi,             True,                yk.tarih_saat()+Fore.LIGHTBLUE_EX+" (coc) tiklama sifirlandi."+Fore.WHITE,         cwd_ekle(coc.kayit_yolu),   False,                          ekran_tarama_sonuc_yolu,            cv2_tarama_yontemi)
        yk.bekle(coc.islem_gecikmesi);
    yk.bekle(coc.herseyi_tekrarlama_gecikmesi)
while (1):
    clash_hile()