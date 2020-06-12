# -*- coding: utf-8 -*-
"""
Created on Wed May 20 11:50:39 2020

@author: muki
"""
from bs4 import BeautifulSoup as bs
import requests
import random

#%%
arama=input("anahtar kelimeler girin:")
link="https://pubmed.ncbi.nlm.nih.gov/?term="+arama
#yil filtresi eklenebilir
site=requests.get(link)
soup=bs(site.content,"html.parser")
from fpdf import FPDF
pdf = FPDF() 



#%%
sonuclar=soup.find_all("div",{"class":"docsum-content"})
makale_linkleri={}
for num,i in enumerate(sonuclar,1):
    
    baslik=i.find("a").get_text().strip()
    yazar=i.find("span",{"class":"labs-docsum-authors full-authors"}).get_text().strip()
    dergi=i.find("span",
                 {"class":"labs-docsum-journal-citation short-journal-citation"}).get_text().strip()
    on_izleme=i.find("div",{"class":"full-view-snippet"}).get_text().strip()
    
    makale_link="https://pubmed.ncbi.nlm.nih.gov"+i.find("a",{"class":"labs-docsum-title"}).get("href")
    makale_linkleri[num]=makale_link
    
    print("{}.{}\nYazar: {} - Dergi: {}\n{}".format(num,baslik,yazar,dergi,on_izleme))
    print("="*20)

makale_sira=input("Okumak istedigin makalelerin sıra no'sunu gir:\n")

for i in makale_sira:
    i=int(i)
    makalenin_linki=makale_linkleri[i]
    site_makale=requests.get(makale_linkleri[i])
    makale_soup=bs(site_makale.content,"html.parser")
    
    makale_baslik=makale_soup.find("h1",{"class":"heading-title"}).get_text().strip()
    makale_yazar=[]
    yaazar=makale_soup.find("div",{"class":"authors-list"}).find_all("span")
    yazarlar=[]
    for i in makale_soup.find("div",{"class":"authors-list"}).find_all("a"):
        #print(i.get_text().strip(),type(i.get_text().strip()))
        if len(i.get_text().strip()) != 1:
            yazarlar.append(i.get_text().strip())
    
    dergi_adi=makale_soup.find("div", {"class":"journal-actions dropdown-block"}).find("button").get("title")
    abstract_=makale_soup.find("div",{"class":"abstract"}).find_all("p")
    abstract=[]
    for i in abstract_:
        abstract.append(i.get_text().strip().replace("\n","").replace("   ",""))
        
    print(makale_baslik,yazarlar,makalenin_linki, sep="\n")
    
    #pdf yapma vakti
    #abstract
    makale_baslik=makale_baslik
    
    pdf.add_page()
    #baslik
    pdf.set_font("Courier","B", size = 14) 
    pdf.set_text_color(r=15,g=175,b=164)
    pdf.cell(w=20,h=10,ln = 1, align = 'C')
    pdf.write(6, makale_baslik)
   
    #abstract
    pdf.set_font("Courier", size = 12)
    pdf.set_text_color(r=78,g=168,b=123)
    pdf.cell(w=20,h=10,ln = 1, align = 'L')
    pdf.write(6, str(abstract))
    
    #yazarlar
    pdf.set_font("Arial",)
    pdf.set_text_color(r=160,g=160,b=160)
    pdf.cell(w=20,h=10,ln = 1, align = 'L')
    pdf.write(6, "Authors of paper;"+str(yazarlar))
    
    #dergi
    pdf.set_font("Arial", size = 12)
    pdf.set_text_color(r=192,g=192,b=192)
    pdf.cell(w=20,h=10,ln = 1, align = 'L')
    pdf.write(6, "Journal of paper;"+dergi_adi)
    
    #link
    pdf.set_font("Arial", size = 12)
    pdf.set_text_color(r=210,g=210,b=210)
    pdf.cell(w=20,h=10,ln = 1, align = 'L')
    pdf.write(6, makalenin_linki)
    
    
pdf_adi="makale_"+str(random.randint(1, 999))+".pdf"   
pdf.output(pdf_adi)    
print(pdf_adi, "olarak kaydedildi")   
"""    try:
        print("'makale' ismiyle kaydoldu")
        pdf.output(pdf_adi)
    except OSError:
        pdf_adi="yeni"+pdf_adi
        pdf.output(pdf_adi)
        print(pdf_adi,"ile kaydettim")
"""

#%%
from time import sleep
from gtts import gTTS
import os
import random
import PyPDF2

 #%%
sleep(1)
text_to_read="\n Thank you for listening. \n Have a good day"
dil="en"
hiz=False
ses_dosyasi_adi=pdf_adi[0:-4]+".mp3"
# creating a pdf file object 
Pdf_Dosyasi = open(pdf_adi, 'rb') 
# creating a pdf reader object 
Pdf_Okuyucu = PyPDF2.PdfFileReader(Pdf_Dosyasi) 
# printing number of pages in pdf file 
print(Pdf_Okuyucu.numPages) 
for i in range(Pdf_Okuyucu.numPages):
    Sayfa = Pdf_Okuyucu.getPage(i)
    text_to_read=Sayfa.extractText() + text_to_read
    # extractText ile sayfanın yazılarını çekelim
# dosyayı kapıyoruz
Pdf_Dosyasi.close() 

def stringden_oku():
    ses_dosyasi_olus=gTTS(text=text_to_read, lang=dil,slow=hiz)
    ses_dosyasi_olus.save(ses_dosyasi_adi)
    os.startfile(ses_dosyasi_adi)
    
stringden_oku()
print(ses_dosyasi_adi, "oluştu!")

