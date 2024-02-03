import datetime as d
from pyautogui import *
import numpy as np
import pyautogui,time,random, cv2, datetime
from PIL import ImageGrab
from colorama import Fore, init

#Deneysel
tiklama_kaydi=True;# t�klanan alanlar� k�rm�z� dikd�rtgen i�ine al�p klas�re kaydet

#De�i�tirmeye gerek olmayan de�i�kenler
fare_konumu_x=10;
fare_konumu_y=10;
pyautogui.FAILSAFE=False;

def tarih_saat():
    s=d.datetime.now();
    saniye=s.second
    dakika=s.minute
    saat=s.hour
    gun=s.day
    ay=s.month
    yil=s.year
    return str(gun)+"/"+str(ay)+"/"+str(yil)+" "+str(saat)+":"+str(dakika)+":"+str(saniye);
def fare_konumu(islem=""):
    global fare_konumu_x,fare_konumu_y
    if islem=="kaydet":
       fare_konumu_x, fare_konumu_y= pyautogui.position()
    elif islem=="geri_yukle":
        pyautogui.moveTo(fare_konumu_x,fare_konumu_y)
def bekle(sure):
    time.sleep(sure)
def ekrana_tikla(x_pos,y_pos):
    pyautogui.mouseDown(button='left',x=x_pos,y=y_pos)
    bekle(0.1)
    pyautogui.mouseUp(button='left',x=x_pos,y=y_pos)
def ekran_tarama(dosya_yolu,dosya_turu):#Ekran resmini kaydetme
    ekran= ImageGrab.grab()
    ekran=ekran.convert('RGBA');#32 bit renk derinli�i, bu kod silinirse 24 bit olacak ekran ve hata verecek
    ekran.save(dosya_yolu,dosya_turu)
def hedef_bul(aranacak_resim,benzerlik_yuzdesi,tikla=False,islem="",kaydetme_konumu="",sadece_ilk_benzerlige_tikla=False,ekran_tarama_sonuc_yolu="",cv2_tarama_yontemi=""):
    bekle(0.1)
    ekran_tarama(ekran_tarama_sonuc_yolu,"PNG")
    harita_0= cv2.imread(ekran_tarama_sonuc_yolu, cv2.IMREAD_UNCHANGED)
    hedef_0= cv2.imread(aranacak_resim, cv2.IMREAD_UNCHANGED)
    tarama_sonucu= cv2.matchTemplate(harita_0, hedef_0, cv2_tarama_yontemi)
    #Buradaki min max de�er, arad���nla en �ok e�le�en ve en az e�le�en demek
    min_deg, maks_deg, min_degerin_konumu, maks_degerin_konumu = cv2.minMaxLoc(tarama_sonucu);
    genislik=hedef_0.shape[1]
    yukseklik=hedef_0.shape[0]
    #cv2.rectangle(harita_0, maks_degerin_konumu,(maks_degerin_konumu[0]+genislik,maks_degerin_konumu[1]+yukseklik), (0,0,255), 2 ) #B, G, R
    #cv2.imshow("Hedef Bulundu", tarama_sonucu)
    y_konumu, x_konumu = np.where(tarama_sonucu>=benzerlik_yuzdesi)
    #Ekranda aranan resim bulunamad�.
    if(len(x_konumu)<=0): 
        return
    #Benzer konumlar� birlestirelim
    konumlandirma_dikdortgenleri=[]
    #Burada iki kere eklememizin sebebi dikd�rtgenleri birle�tirirken tek bir tane varsa hata vermesi
    #Bu kod her dikd�rtgeni iki kere kaydederek hatan�n �n�ne ge�iyor
    for(x,y) in zip(x_konumu, y_konumu):
        konumlandirma_dikdortgenleri.append([int(x),int(y),int(genislik), int(yukseklik)])
        konumlandirma_dikdortgenleri.append([int(x),int(y),int(genislik), int(yukseklik)])
    #Ayn� resmi birden fazla defa i�aretlediyse yak�n i�aretleri birle�tirelim
    konumlandirma_dikdortgenleri, yakinlik= cv2.groupRectangles(konumlandirma_dikdortgenleri, 1, 0.2)
    #Dikd�rtgen �izelim
    for (x,y,genislik,yukseklik) in konumlandirma_dikdortgenleri:
        cv2.rectangle(harita_0,(x,y),(x+genislik,y+yukseklik),(0,0,255),2)
        #print("x:"+str(x)+" y:"+str(y)+" genislik:"+str(genislik)+" yukseklik:"+str(yukseklik))
    if(tikla):
        tik_sayisi=0
        for (x,y,gen,yuk) in konumlandirma_dikdortgenleri:
            tik_sayisi=tik_sayisi+1
        print(Fore.LIGHTYELLOW_EX+"(Benzer Alan Bulundu "+str(tik_sayisi)+")"+Fore.WHITE)
        for (x,y,gen,yuk) in konumlandirma_dikdortgenleri:
            print("x:"+str(x)+" y:"+str(y)+" Genislik:"+str(gen)+" Yukseklik:"+str(yuk))
        #Dosya kayd� (Program her t�klad���nda ekran al�nt�s� al�p t�klad��� yeri i�aretlesin)
        if(tiklama_kaydi):
            mevcut_tarih=str(datetime.datetime.now())
            mevcut_tarih=mevcut_tarih.replace("-","_")
            mevcut_tarih=mevcut_tarih.replace(":","_")
            mevcut_tarih=mevcut_tarih.replace(".","_")
            cv2.imwrite(kaydetme_konumu+str(mevcut_tarih)+".png",harita_0)
        #Ekrandaki resimlere t�klayal�m
        for (x,y,genislik,yukseklik) in konumlandirma_dikdortgenleri:
            fare_konumu("kaydet");
            ekrana_tikla(x,y)
            print(Fore.LIGHTGREEN_EX+"(Ekran Tiklamasi Yapildi)"+Fore.WHITE)
            print("x:"+str(x)+" y:"+str(y)+" Genislik:"+str(gen)+" Yukseklik:"+str(yuk))
            print(islem);
            fare_konumu("geri_yukle");
            #bekle(islem_gecikmesi)
            #yapt���m�z i�lemin ad�n� ekrana yazd�ral�m
            #print(islem)
            #e�er iksir, altin topluyorsak ya da tamam tu�una bas�yorsak, yanl�� bir�eye basmam�z ihtimaline kar��
            #varsa �arp� tu�una basal�m ayn� �ekilde yine k�y ekran�ndaysak t�klamay� bo� bir alana t�klayarak s�f�rlayal�m
            if sadece_ilk_benzerlige_tikla:
                break
    if len(konumlandirma_dikdortgenleri)!=0:
        return True
    else: return False
    #Birle�tirmeden sonraki konum say�s�n� ekrana yazd�ral�m
    #if (len(konumlandirma_dikdortgenleri)!=0 and len(konumlandirma_dikdortgenleri)!=1):
    #    print("Yakin konumlari birlestirmeden sonraki sayi:"+str(len(konumlandirma_dikdortgenleri)))
    #��aretlenen yerleri ekranda g�sterelim