# -*- coding: utf-8 -*-
"""
Created on Wed May 17 11:50:39 2020

@author: muki
"""
from bs4 import BeautifulSoup as bs
import requests
#%%
arama=input("anahtar kelimeler girin:")
link="https://pubmed.ncbi.nlm.nih.gov/?term="+arama
#yil filtresi eklenebilir
site=requests.get(link)
soup=bs(site.content,"html.parser")
pdf_adi="makale.pdf"
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
        abstract.append(i.get_text().strip().replace("\n",""))
        
    print(makale_baslik,yazarlar,makalenin_linki, sep="\n")
    
    
    
    #pdf yapma vakti
    #abstract
    
    
    pdf.add_page()
    #baslik
    pdf.set_font("Arial", size = 14) 
    pdf.cell(w=20,h=10,ln = 1, align = 'L')
    pdf.write(6, makale_baslik)
    
    #yazarlar
    pdf.set_font("Arial", size = 12)
    pdf.cell(w=20,h=10,ln = 1, align = 'L')
    pdf.write(6, str(yazarlar))
    
    
    
    #dergi
    pdf.set_font("Arial", size = 12)
    pdf.cell(w=20,h=10,ln = 1, align = 'L')
    pdf.write(6, dergi_adi)
    
    #abstract
    pdf.set_font("Arial", size = 12)
    pdf.cell(w=20,h=10,ln = 1, align = 'L')
    pdf.write(6, str(abstract))
    
    #link
    pdf.set_font("Arial", size = 12)
    pdf.cell(w=20,h=10,ln = 1, align = 'L')
    pdf.write(6, makalenin_linki)
    
pdf.output(pdf_adi)    
    
"""    try:
        print("'makale' ismiyle kaydoldu")
        pdf.output(pdf_adi)
    except OSError:
        pdf_adi="yeni"+pdf_adi
        pdf.output(pdf_adi)
        print(pdf_adi,"ile kaydettim")
"""























