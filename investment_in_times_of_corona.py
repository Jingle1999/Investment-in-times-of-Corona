# Activate necessary libraries
'''With these data analysis I would like to analyze the patterns of data from the New York Stock exchange together with the available 
data regarding the Coronavirus disease in the US'''


import csv
import numpy as np
import pandas as pd 
import pandas_datareader.data as web
import matplotlib as mpl
import matplotlib.pyplot as plt
from datetime import datetime


# Download necessary data from finance.yahoo.com
overall_stock_data = {ticker: web.get_data_yahoo(ticker)
                      for ticker in ['DJIA']} # getting the data of the Dow Jones Industrial Average Index (DJIA)
                                              # from Yahoo finance
price  = pd.DataFrame({ticker: data['Adj Close']
                       for ticker, data in overall_stock_data.items()}) # getting stock prices of the DJIA per day

stock_change = price.pct_change() # getting the percentage change of the stock prices as basic data for analyzing 
                                   # the volatility of the stock market



# Saving the data as csv-file 
print(price) # checking stock prices per day
print(stock_change) # checking stock_change-data

price.to_csv(r'dow_jones_industrial_average.csv', index=True) # Writing DJIA stock-data to csv for further analysis
stock_change.to_csv(r'dow_jones_change.csv', index=True) # Writing stock_returns to csv for further analysis

# Plotting the DJIA-data to visualize the Dow Jones

fig1 = plt.figure()
ax1 = fig1.add_subplot(1, 1, 1)

data1 = pd.read_csv('dow_jones_industrial_average.csv', index_col=0, parse_dates=True)
dji = data1['DJIA']

ax1.set_title('Overview over Dow Jones Industrial Average-index \nfrom mid 2015 until mid June 2020')
plt.xlabel('Date')
plt.ylabel('Price')
dji.plot(ax=ax1, style='k')
plt.show()
# Plotting the stock_returns-data to visualize the change and volatility of the market

fig2 = plt.figure()
ax2  = fig2.add_subplot(1, 1, 1)

data2 = pd.read_csv('dow_jones_change.csv', index_col=0, parse_dates=True) # Reading the data from csv with real dates and percentage changes
djia = data2['DJIA']

ax2.set_title('Volatility of the Dow Jones Industrial Average \nfrom mid 2015 until today')
plt.xlabel('Date')
plt.ylabel('Percentage change')
djia.plot(ax=ax2, style='k')

# Watching the data from end 2019 till mid 2020 more closely
fig3 = plt.figure()
ax3 = fig3.add_subplot(1, 1, 1)

data3 = pd.read_csv('dow_jones_industrial_average.csv', index_col=0, parse_dates=True)

dji2 = data3['DJIA']
print(dji2)
plt.xlabel('Date')
plt.ylabel('Price of DJIA')

dji2.plot(ax=ax3, style='k-')



# marking the milestones of the Corona-development in the USA
corona_data = [(datetime(2019,12,31), 'China allerts \n WHO'), # https://www.who.int/emergencies/diseases/novel-coronavirus-2019/events-as-they-happen
               (datetime(2020,2,11), 'Novel coronavirus disease named COVID-19'), # https://www.who.int/emergencies/diseases/novel-coronavirus-2019/events-as-they-happen
               (datetime(2020,2,29), 'First US dead due to Corona'), # https://www.who.int/emergencies/diseases/novel-coronavirus-2019/events-as-they-happen
               (datetime(2020,3,11), 'WHO: COVID-19 is a pandemic'), # https://www.who.int/emergencies/diseases/novel-coronavirus-2019/events-as-they-happen
               (datetime(2020,4,6), 'Peak of new \n US-cases')] # https://www1.nyc.gov/site/doh/covid/covid-19-data.page
for date, label in corona_data:
    ax3.annotate(label, xy=(date, dji2.asof(date) + 500),
                 xytext=(date, dji2.asof(date) + 4000),
                 arrowprops=dict(facecolor = 'red', headwidth=8, width=4,
                                 headlength=8),
                 horizontalalignment='left', verticalalignment='top')

# Zooming into data from end 2019 until mid 2020
ax3.set_ylim([16000, 36000])
ax3.set_xlim(['12/2019', '18/6/2020'])
ax3.set_title('Milestones of the Corona-development\nin the USA vs. Dow Jones Industrial Average')

plt.show()
# Corralation between Corona and DJIA
''' In the next part I am checking the development of the Corona Desease in the USA and want to figure out,
if there is a connection between development of the Corona Desease and the developmentof stock data and in the USA.
That means at first I show the development of the Corona desease in the USA versus the devolopment of uncertainty and then
I am checking the correlation coeffcient, in order to see if the data is somehow connected'''


# plot data4_USA: x-axis = Date, y-axis = total_cases

# Set up DataFrame object regarding Corona-data

fig4 = plt.figure()
ax4 = fig4.add_subplot(1, 1, 1)
data4 = pd.read_csv('covid-data.csv', index_col=('location'), parse_dates=True) # data downloaded on https://data.world/markmarkoh/coronavirus-data/workspace/file?filename=full_data.csv
data4_USA = data4.loc['United States'] # filter the US-data out of covid-data.csv
data4_USA = pd.DataFrame(data4_USA, columns=['Date', 'total_cases'])
print(data4_USA) # check data via print-out

# plot Corona - total cases in the USA 

data4_USA.plot(kind='line',x='Date',y='total_cases',ax=ax4, style='k-')

plt.xlabel('Date')
plt.ylabel('Total Corona Cases(per 100000 inhabitants)')
ax4.set_title('Development of Corona-cases in the USA')
plt.xticks(rotation=25)

# changing font size in order for everything to fit on the plot

for item in ([ax4.xaxis.label, ax4.yaxis.label] +
                ax4.get_xticklabels() + ax4.get_yticklabels()):
       item.set_fontsize(6)

plt.show()

# Using the so-called uncertainty-index in order to analyze the development of uncertainty; 
# Source: 'Measuring Economic Policy Uncertainty' by Scott Baker, Nicholas Bloom and Steven J. Davis at www.PolicyUncertainty.com.  

fig5 = plt.figure()
ax5 = fig5.add_subplot(1, 1, 1)
data5 = pd.read_csv('US_Policy_Uncertainty_Data.csv', index_col=0, parse_dates=True)
analyze_uncertainty = pd.DataFrame(data5, columns=['Three_Component_Index'])
print(data5)
print(analyze_uncertainty)
analyze_uncertainty.plot(ax=ax5, style='k-')

ax5.set_xlim(['2007', '5-2020'])
plt.xlabel('Date')
plt.ylabel('Three component index')
ax5.set_title('Overview over uncertainty-index')
plt.show()

# using correlation coefficiant in order to measure the interconnection of the data
# basically it shows: Corona cases grow > uncertainty grows

print('------------------------------')
data6 =  pd.read_csv('US_Policy_Uncertainty_Data_for_correlation.csv', index_col=0, parse_dates=True)

print('Correlation between total Corona-cases in the US and risk: ',data6.corr())

