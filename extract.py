# Data Scraping:-
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import font_manager

bg = '#ebdbb2'
text_color = '#8f3f71'
dot_color='#af3a03' 

fig, ax = plt.subplots(figsize=(8,8))
fig.set_facecolor(bg)
ax.patch.set_facecolor(bg)

ax.grid(color=text_color)

# Fonts;-
main_font = 'Ubuntu'
fig.text(0.125,.925,"How well Premier League fans filled their Stadiums?",fontweight='bold',fontsize=17,color=text_color,fontfamily=main_font)
fig.text(0.125,.90,"Premier League Season 22/23",fontweight='regular',fontsize=16,color=text_color,fontfamily=main_font)
ax.set_xlabel("Capacity Filled by the Fans(in %)",fontweight='bold',fontsize=15,color=text_color,fontfamily=main_font)
ax.set_ylabel("Total Capacity",fontweight='bold',fontsize=15,color=text_color,fontfamily=main_font)

ax.tick_params(axis='x', colors=text_color)
ax.tick_params(axis='y', colors=text_color)

spines=['top','right','bottom','left']
for s in spines:
    if s in ['top','right']:
        ax.spines[s].set_visible(False)
    else:
        ax.spines[s].set_color(text_color)

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
plt.ylabel("Total Capacity")
plt.xlabel("Capacity Filled by the Fans(in %)")
plt.scatter(reparrper,reparr,color=dot_color)
plt.show()
