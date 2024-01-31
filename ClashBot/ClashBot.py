# This Python file uses the following encoding: utf-8
from ctypes import Array
import os
#os.execute("pip install pyautogui opencv-python Pillow, colorama")
from pyautogui import *
import numpy as np
import pyautogui,time,random, cv2, datetime
from PIL import ImageGrab
from colorama import Fore, init

#��lem geciktirme
tiklama_gecikmesi=0.1 ### T�klamalar aras�nda ge�en s�re (Saniye cinsinden)
islem_gecikmesi=1 ### Yap�lan i�lemler aras�nda ge�en s�re (Saniye cinsinden)
herseyi_tekrarlama_gecikmesi= 30 #7200 #2 saat

#Dosya yollar�
cwd = os.getcwd()+"\\";

iksir_resim_yolu = cwd+"resources\\elixir_popup.png";
altin_resim_yolu = cwd+"resources\\gold_popup.png";
oyunu_tekrar_yukle_resim_yolu = cwd+"resources\\oyunu_tekrar_yukle.png";
tamam_resim_yolu = cwd+"resources\\tamam.png";
sifirla_resim_yolu = cwd+"resources\\sifirla.png";
carpi_resim_yolu = cwd+"resources\\carpi.png";
kayit_yolu=cwd+"kayit\\";

ekran_tarama_sonuc_yolu=cwd+"ekran_tarama.png";

#Kalibrasyon
cv2_tarama_yontemi=cv2.TM_CCOEFF_NORMED #cv2.TM_SQDIFF_NORMED
iksir_resim_benzerlik_yuzdesi=.61 #
altin_resim_benzerlik_yuzdesi=.61 #
oyunu_tekrar_yukle_resim_benzerlik_yuzdesi = .50
tamam_resim_benzerlik_yuzdesi= .65
sifirla_resim_benzerlik_yuzdesi= .59
carpi_resim_benzerlik_yuzdesi=.60

#Deneysel
hata_ayikla=False; #True t�klanan alanlar� k�rm�z� dikd�rtgen i�ine alarak g�ster.
tiklama_kaydi=True;
cift_tiklama=False;

def bekle(sure):
    time.sleep(sure)

def ekrana_tikla(x_pos,y_pos):
    pyautogui.mouseDown(button='left',x=x_pos,y=y_pos)
    bekle(tiklama_gecikmesi)
    pyautogui.mouseUp(button='left',x=x_pos,y=y_pos)
    #�ift t�klama se�iliyse ikinci defa t�klayal�m
    if(cift_tiklama):
        bekle(tiklama_gecikmesi)
        pyautogui.mouseDown(button='left',x=x_pos,y=y_pos)
        bekle(tiklama_gecikmesi)
        pyautogui.mouseUp(button='left',x=x_pos,y=y_pos)
    bekle(islem_gecikmesi)
    
def ekran_tarama():#Ekran resmini kaydetme
    ekran= ImageGrab.grab()
    ekran=ekran.convert('RGBA');#32 bit renk derinli�i, bu kod silinirse 24 bit olacak ekran ve hata verecek
    ekran.save("ekran_tarama.png","PNG")
    
def hedef_bul(aranacak_resim,benzerlik_yuzdesi,tikla=False,islem=""):
    time.sleep(islem_gecikmesi);
    ekran_tarama()
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
            print(Fore.LIGHTGREEN_EX+"__Ekran Tiklamasi "+str(tik_sayisi)+"__"+Fore.WHITE)
            print("x:"+str(x)+" y:"+str(y)+" Genislik:"+str(gen)+" Yukseklik:"+str(yuk))
        #Dosya kayd� (Program her t�klad���nda ekran al�nt�s� al�p t�klad��� yeri i�aretlesin)
        if(tiklama_kaydi):
            mevcut_tarih=str(datetime.datetime.now())
            mevcut_tarih=mevcut_tarih.replace("-","_")
            mevcut_tarih=mevcut_tarih.replace(":","_")
            mevcut_tarih=mevcut_tarih.replace(".","_")
            cv2.imwrite(kayit_yolu+str(mevcut_tarih)+".png",harita_0)
        #Ekrandaki resimlere t�klayal�m
        for (x,y,genislik,yukseklik) in konumlandirma_dikdortgenleri:
            ekrana_tikla(x,y)
            #yapt���m�z i�lemin ad�n� ekrana yazd�ral�m
            print(islem)
            #e�er iksir, altin topluyorsak ya da tamam tu�una bas�yorsak, yanl�� bir�eye basmam�z ihtimaline kar��
            #varsa �arp� tu�una basal�m ayn� �ekilde yine k�y ekran�ndaysak t�klamay� bo� bir alana t�klayarak s�f�rlayal�m
            if(" iksir" in islem or " altin" in islem or " tamam" in islem):
                hedef_bul(carpi_resim_yolu,carpi_resim_benzerlik_yuzdesi,True,str(datetime.datetime.now())+Fore.RED+" carpi tusuna basildi"+Fore.WHITE)
                hedef_bul(sifirla_resim_yolu,sifirla_resim_benzerlik_yuzdesi,True,str(datetime.datetime.now())+Fore.LIGHTBLUE_EX+" tiklama sifirlandi"+Fore.WHITE)
                break
    #Birle�tirmeden sonraki konum say�s�n� ekrana yazd�ral�m
    if (len(konumlandirma_dikdortgenleri)!=0 and len(konumlandirma_dikdortgenleri)!=1):
        print("\nYakin konumlari birlestirmeden sonraki sayi:"+str(len(konumlandirma_dikdortgenleri)))
    #��aretlenen yerleri ekranda g�sterelim
    if(hata_ayikla):
        cv2.imshow("harita_0",harita_0)
        cv2.waitKey()
        cv2.destroyAllWindows()

init()
#resources ve kayit klas�rleri yoksa olu�tural�m
if(os.path.exists(cwd+"resources") is not True):
    os.makedirs(cwd+"resources")
if(os.path.exists(cwd+"kayit") is not True):
    os.makedirs(cwd+"kayit")
    
while (1):
    for x in range(5):
        hedef_bul(carpi_resim_yolu,carpi_resim_benzerlik_yuzdesi,True,str(datetime.datetime.now())+Fore.RED+" carpi tusuna basildi"+Fore.WHITE)
        hedef_bul(iksir_resim_yolu,iksir_resim_benzerlik_yuzdesi,True,str(datetime.datetime.now())+Fore.MAGENTA+" iksir"+Fore.WHITE)
        hedef_bul(carpi_resim_yolu,carpi_resim_benzerlik_yuzdesi,True,str(datetime.datetime.now())+Fore.RED+" carpi tusuna basildi"+Fore.WHITE)
        hedef_bul(altin_resim_yolu,altin_resim_benzerlik_yuzdesi,True,str(datetime.datetime.now())+Fore.YELLOW+" altin"+Fore.WHITE)
        hedef_bul(carpi_resim_yolu,carpi_resim_benzerlik_yuzdesi,True,str(datetime.datetime.now())+Fore.RED+" carpi tusuna basildi"+Fore.WHITE)
        hedef_bul(oyunu_tekrar_yukle_resim_yolu,oyunu_tekrar_yukle_resim_benzerlik_yuzdesi,True,str(datetime.datetime.now())+Fore.BLUE+" oyuna yeniden baglaniliyor"+Fore.WHITE)
        hedef_bul(carpi_resim_yolu,carpi_resim_benzerlik_yuzdesi,True,str(datetime.datetime.now())+Fore.RED+" carpi tusuna basildi"+Fore.WHITE)
        hedef_bul(tamam_resim_yolu,tamam_resim_benzerlik_yuzdesi,True,str(datetime.datetime.now())+Fore.GREEN+" tamam tusuna basildi"+Fore.WHITE)
        bekle(30);
    bekle(herseyi_tekrarlama_gecikmesi)