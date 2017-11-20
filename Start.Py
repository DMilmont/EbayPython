

# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 10:50:30 2017
@author: DMilmont
"""


from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import statsmodels.formula.api as smf

priceRegex = '(0-9*)</span>'

years = ['2013', '2014', '2015', '2016', '2017']
output = {}
for y in years:
    
    url = "https://www.ebay.com/sch/i.html?Screen%2520Size=13%252E3in%252E&_sop=12&_sadis=15&LH_ItemCondition=3000&Release%2520Year="+y+"&_stpos=80239-6007&_odkw=macbook+pro+retina&Memory=8GB&Hard%2520Drive%2520Capacity=256GB&_dmd=1&LH_Complete=1&_dcat=111422&LH_Sold=1&_osacat=0&_ipg=200&_from=R40&_trksid=p2045573.m570.l1313.TR0.TRC0.H0.Xmacbook+pro+retina.TRS0&_nkw=macbook+pro+retina&_sacat=0"
    r = requests.get(url)
    c = r.content

    soup = BeautifulSoup(c)

    prices = []
    for text in soup.find_all("li", class_="lvprice prc"):
        prices.append(text.text)

    prices = [re.findall('(\d,?\d*\.\d{2}){1}',p) for p in prices if re.match('[^\$\d*\.\d{2}]',p)]

    prices = [p[0].replace(',','') for p in prices]
    final = [float(n) for n in prices]
    output[y] = final

PricesDF = pd.DataFrame({k:pd.Series(v[:200]) for k,v in output.items()})

PricesDF.boxplot()
PricesDF.mean()


mPricesDF = pd.melt(PricesDF, value_vars=['2013', '2014', '2015', '2016', '2017'])
mPricesDF.head()
mPricesDF.plot.scatter(x = 'value', y = 'variable')



#------------------------------------below does not work - just experiments 

lmod = smf.ols(formula='value ~ variable', data=mPricesDF)

res = lmod.fit()

print(res.summary())


final.mean()
