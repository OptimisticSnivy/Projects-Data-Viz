# Data Scraping:-
import requests
from bs4 import BeautifulSoup
from PIL import Image

import pandas as pd

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import font_manager
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


def getImage(path):
    return OffsetImage(plt.imread(path), zoom=0.25, alpha = 1)

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

StadiumsList.remove('Craven Cottage')

path=[]
for s in range(1,len(StadiumsList)+1):
    pathstr='./logosforplot/logo'+str(s)+'.png'
    path.append(pathstr)

df = pd.DataFrame({"Stadiums":StadiumsList,"Total_Capacity":reparr,"Capacity_per":reparrper,"path":path})
print(df)

# Plotting:-
bg = '#fafafa'
text_color = '#2C0A3D'
dot_color='#2C0A3D' 

fig, ax = plt.subplots(figsize=(6,4),dpi=120)
fig.set_facecolor(bg)
ax.patch.set_facecolor(bg)

# Fonts;-
main_font = 'Ubuntu'
fig.text(0.195,.925,"How well Premier League fans filled their Stadiums?",fontweight='bold',fontsize=17,color=text_color,fontfamily=main_font)
fig.text(0.195,.90,"Premier League Season 22/23",fontweight='regular',fontsize=16,color=text_color,fontfamily=main_font)
ax.set_xlabel("Capacity Filled by the Fans(in %)",fontweight='bold',fontsize=15,color=text_color,fontfamily=main_font)
ax.set_ylabel("Total Capacity",fontweight='bold',fontsize=15,color=text_color,fontfamily=main_font)

ax.tick_params(axis='x', colors=text_color)
ax.tick_params(axis='y', colors=text_color)

spines=['top','right','bottom','left']
for s in spines:
    if s in ['top','right']:
        ax.spines[s].set_visible(False)
    else:
        ax.spines[s].set_color('#ccc8c8')

ax.scatter(reparrper, reparr, color=text_color)
for index, row in df.iterrows():
    imm = getImage(row["path"])
    ab = AnnotationBbox(imm,(row["Capacity_per"], row["Total_Capacity"]),frameon=False)
    ax.add_artist(ab)
plt.show()
