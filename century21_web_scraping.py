#!/usr/bin/env python
# coding: utf-8

# In[19]:


import requests
from bs4 import BeautifulSoup


# In[20]:


r = requests.get("https://pythonizing.github.io/data/real-estate/rock-springs-wy/LCWYROCKSPRINGS/", 
        headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0)Gecko/20100101 Firefox/61.0'})
c=r.content

soup=BeautifulSoup(c,"html.parser")

all=soup.find_all("div", {"class":"propertyRow"})

all[0].find("h4", {"class":"propPrice"}).text.replace("\n", "").replace(" ","")

page_nr=soup.find_all("a",{"class":"Page"})[-1].text


# In[21]:


l=[]
base_url = "https://pythonizing.github.io/data/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
for page in range(0,int(page_nr)*10,10):
    print (base_url + str(page) + ".html")
    r=requests.get(base_url + str(page) + ".html")
    c=r.content
    soup = BeautifulSoup(c,"html.parser")
    all=soup.find_all("div",{"class":"propertyRow"})
    for item in all:
        d={}    
        d["Address"]=item.find_all("span", {"class", "propAddressCollapse"})[0].text
        try:
            d["Locality"]=item.find_all("span", {"class", "propAddressCollapse"})[1].text
        except:
            d["Locality"]=None
        d["Price"]=item.find("h4", {"class", "propPrice"}).text.replace("\n", "").replace(" ","")
        try:
            d["Beds"]=item.find("span", {"class", "infoBed"}).find("b").text
        except:
            d["Beds"]=None

        try:
            d["Area"]=item.find("span", {"class", "infoSqFt"}).find("b").text
        except:
            d["Area"]=None    
        try:
            d["Full Baths"]=item.find("span", {"class", "infoValueFullBath"}).find("b").text
        except:
            d["Full Baths"]=None    
        try:
            d["Half Baths"]=item.find("span", {"class", "infoValueHalfBath"}).find("b").text
        except:
            d["Half Baths"]=None
        for column_group in item.find_all("div",{"class": "columnGroup"}):
            #print(column_group)
            for feature_group, feature_name in zip (column_group.find_all("span",{"class":"featureGroup"}), column_group.find_all("span",{"class": "featureName"})):
                #print(feature_group.text, feature_name.text)
                if "Lot Size" in feature_group.text:
                    d["Lot Size"]=feature_name.text                
        l.append(d)    


# In[22]:


import pandas as pd
df=pd.DataFrame(l)


# In[23]:


df


# In[24]:


df.to_csv("Output.csv")


# In[ ]:




