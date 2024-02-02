# This Python file uses the following encoding: utf-8
from ctypes import Array
import os
#os.execute("pip install pyautogui opencv-python Pillow colorama")
from pyautogui import *
import numpy as np
import pyautogui,time,random, cv2, datetime
from PIL import ImageGrab
from colorama import Fore, init

#İşlem geciktirme
tiklama_gecikmesi=0.1 ### Tıklamalar arasında geçen süre (Saniye cinsinden)
islem_gecikmesi=30 ### Yapılan işlemler arasında geçen süre (Saniye cinsinden)
herseyi_tekrarlama_gecikmesi= 7200 #7200 #2 saat

#Dosya yolları
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
sifirla_resim_benzerlik_yuzdesi= .60
carpi_resim_benzerlik_yuzdesi=.60

#Deneysel
hata_ayikla=False; #True tıklanan alanları kırmızı dikdörtgen içine alarak göster.
tiklama_kaydi=True;
cift_tiklama=False;

#Değiştirmeye gerek olmayan değişkenler
fare_konumu_x=10;
fare_konumu_y=10;
pyautogui.FAILSAFE=False;

def tarih_saat():
    s=datetime.datetime.now();
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
    bekle(tiklama_gecikmesi)
    pyautogui.mouseUp(button='left',x=x_pos,y=y_pos)
    #Çift tıklama seçiliyse ikinci defa tıklayalım
    if(cift_tiklama):
        bekle(tiklama_gecikmesi)
        pyautogui.mouseDown(button='left',x=x_pos,y=y_pos)
        bekle(tiklama_gecikmesi)
        pyautogui.mouseUp(button='left',x=x_pos,y=y_pos)
    #bekle(islem_gecikmesi)
    
def ekran_tarama():#Ekran resmini kaydetme
    ekran= ImageGrab.grab()
    ekran=ekran.convert('RGBA');#32 bit renk derinliği, bu kod silinirse 24 bit olacak ekran ve hata verecek
    ekran.save("ekran_tarama.png","PNG")
    
def hedef_bul(aranacak_resim,benzerlik_yuzdesi,tikla=False,islem=""):
    bekle(tiklama_gecikmesi)
    ekran_tarama()
    harita_0= cv2.imread(ekran_tarama_sonuc_yolu, cv2.IMREAD_UNCHANGED)
    hedef_0= cv2.imread(aranacak_resim, cv2.IMREAD_UNCHANGED)
    tarama_sonucu= cv2.matchTemplate(harita_0, hedef_0, cv2_tarama_yontemi)
    #Buradaki min max değer, aradığınla en çok eşleşen ve en az eşleşen demek
    min_deg, maks_deg, min_degerin_konumu, maks_degerin_konumu = cv2.minMaxLoc(tarama_sonucu);
    genislik=hedef_0.shape[1]
    yukseklik=hedef_0.shape[0]
    #cv2.rectangle(harita_0, maks_degerin_konumu,(maks_degerin_konumu[0]+genislik,maks_degerin_konumu[1]+yukseklik), (0,0,255), 2 ) #B, G, R
    #cv2.imshow("Hedef Bulundu", tarama_sonucu)
    y_konumu, x_konumu = np.where(tarama_sonucu>=benzerlik_yuzdesi)
    #Ekranda aranan resim bulunamadı.
    if(len(x_konumu)<=0): 
        return
    #Benzer konumları birlestirelim
    konumlandirma_dikdortgenleri=[]
    #Burada iki kere eklememizin sebebi dikdörtgenleri birleştirirken tek bir tane varsa hata vermesi
    #Bu kod her dikdörtgeni iki kere kaydederek hatanın önüne geçiyor
    for(x,y) in zip(x_konumu, y_konumu):
        konumlandirma_dikdortgenleri.append([int(x),int(y),int(genislik), int(yukseklik)])
        konumlandirma_dikdortgenleri.append([int(x),int(y),int(genislik), int(yukseklik)])
    #Aynı resmi birden fazla defa işaretlediyse yakın işaretleri birleştirelim
    konumlandirma_dikdortgenleri, yakinlik= cv2.groupRectangles(konumlandirma_dikdortgenleri, 1, 0.2)
    #Dikdörtgen çizelim
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
        #Dosya kaydı (Program her tıkladığında ekran alıntısı alıp tıkladığı yeri işaretlesin)
        if(tiklama_kaydi):
            mevcut_tarih=str(datetime.datetime.now())
            mevcut_tarih=mevcut_tarih.replace("-","_")
            mevcut_tarih=mevcut_tarih.replace(":","_")
            mevcut_tarih=mevcut_tarih.replace(".","_")
            cv2.imwrite(kayit_yolu+str(mevcut_tarih)+".png",harita_0)
        #Ekrandaki resimlere tıklayalım
        for (x,y,genislik,yukseklik) in konumlandirma_dikdortgenleri:
            fare_konumu("kaydet");
            print(Fore.LIGHTGREEN_EX+"(Ekran Tiklamasi Yapildi)"+Fore.WHITE)
            print("x:"+str(x)+" y:"+str(y)+" Genislik:"+str(gen)+" Yukseklik:"+str(yuk))
            print(islem);
            ekrana_tikla(x,y)
            fare_konumu("geri_yukle");
            #bekle(islem_gecikmesi)
            #yaptığımız işlemin adını ekrana yazdıralım
            #print(islem)
            #eğer iksir, altin topluyorsak ya da tamam tuşuna basıyorsak, yanlış birşeye basmamız ihtimaline karşı
            #varsa çarpı tuşuna basalım aynı şekilde yine köy ekranındaysak tıklamayı boş bir alana tıklayarak sıfırlayalım
            if(" iksir" in islem or " altin" in islem or " tamam" in islem or " tiklama sifirlandi."):
                #hedef_bul(carpi_resim_yolu,carpi_resim_benzerlik_yuzdesi,True,str(datetime.datetime.now())+Fore.RED+" carpi tusuna basildi"+Fore.WHITE)
                if " tiklama sifirlandi." not in islem:
                    hedef_bul(sifirla_resim_yolu,sifirla_resim_benzerlik_yuzdesi,True,str(tarih_saat())+Fore.LIGHTBLUE_EX+" tiklama sifirlandi."+Fore.WHITE)
                break
    #Birleştirmeden sonraki konum sayısını ekrana yazdıralım
    #if (len(konumlandirma_dikdortgenleri)!=0 and len(konumlandirma_dikdortgenleri)!=1):
    #    print("Yakin konumlari birlestirmeden sonraki sayi:"+str(len(konumlandirma_dikdortgenleri)))
    #İşaretlenen yerleri ekranda gösterelim
    if(hata_ayikla):
        cv2.imshow("harita_0",harita_0)
        cv2.waitKey()
        cv2.destroyAllWindows()

init()
#resources ve kayit klasörleri yoksa oluşturalım
if(os.path.exists(cwd+"resources") is not True):
    os.makedirs(cwd+"resources")
if(os.path.exists(cwd+"kayit") is not True):
    os.makedirs(cwd+"kayit")
    
while (1):
    for x in range(5):
        #ekran_tarama();
        hedef_bul(oyunu_tekrar_yukle_resim_yolu,oyunu_tekrar_yukle_resim_benzerlik_yuzdesi,True,str(tarih_saat())+Fore.BLUE+" oyuna yeniden baglaniliyor."+Fore.WHITE)
        hedef_bul(iksir_resim_yolu,iksir_resim_benzerlik_yuzdesi,True,str(tarih_saat())+Fore.MAGENTA+" iksir"+Fore.WHITE+" toplandi.")
        hedef_bul(carpi_resim_yolu,carpi_resim_benzerlik_yuzdesi,True,str(tarih_saat())+Fore.RED+" carpi tusuna basildi."+Fore.WHITE)
        hedef_bul(altin_resim_yolu,altin_resim_benzerlik_yuzdesi,True,str(tarih_saat())+Fore.YELLOW+" altin"+Fore.WHITE+" toplandi.")
        hedef_bul(tamam_resim_yolu,tamam_resim_benzerlik_yuzdesi,True,str(tarih_saat())+Fore.GREEN+" Tamam tusuna basildi."+Fore.WHITE)
        #hedef_bul(sifirla_resim_yolu,sifirla_resim_benzerlik_yuzdesi,True,str(datetime.datetime.now())+Fore.LIGHTBLUE_EX+" tiklama sifirlandi"+Fore.WHITE)
        bekle(islem_gecikmesi);
    bekle(herseyi_tekrarlama_gecikmesi)
