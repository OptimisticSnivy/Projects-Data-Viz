# Data Scraping:-
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

page='https://www.transfermarkt.co.in/premier-league/besucherzahlen/wettbewerb/GB1/saison_id/2022/plus/1'
pageTree = requests.get(page, headers=headers)
pageSoup = BeautifulSoup(pageTree.content, 'html.parser')


Stadiums = pageSoup.find_all("td", {"class": "hauptlink"})
Capacity_per = pageSoup.find_all("td", {"class": "rechts hauptlink"})
MetricExtract = pageSoup.find_all("td", {"class": "rechts"})
StadiumsList = []
Capacity_perList = []
MetricExtractList = []
reparr=[]
reparrper=[]

del Stadiums[1::2]
length=len(Stadiums)

for i in range(0,length):
    StadiumsList.append(Stadiums[i].text)
    Capacity_perList.append(Capacity_per[i].text)

for j in range(0,len(MetricExtract)):
    MetricExtractList.append(MetricExtract[j].text)

TotalCapacity=(MetricExtractList[5::4])

for i in range(0,len(TotalCapacity)):
    s2=TotalCapacity[i].replace('.','')
    if(float(s2)!=float(22384)):
        reparr.append(float(s2))

AverageAttend=(MetricExtractList[7::4])

for j in range(0,len(Capacity_perList)):
    s3=Capacity_perList[j].replace(' %','')
    if(float(s3)<100):
        reparrper.append(float(s3))

df = pd.DataFrame({"Stadiums":StadiumsList,"Capacity_per":Capacity_perList,"Total_Capacity":TotalCapacity,"Average_Attendance":AverageAttend})
print(df)

# Plotting:-
plt.scatter(reparrper,reparr)
plt.show()
