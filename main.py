import os
import time
import requests
import json
import csv
import pandas as pd
import plotly
from plotly.graph_objs import Scatter, Layout

# Initialize Plotly for offline usage
plotly.offline.init_notebook_mode(connected=True)

pd.options.mode.chained_assignment = None  # Suppress SettingWithCopyWarning

def twodigit(n):
    """Convert a single digit to a two-digit string."""
    return f"{n:02}"

def convertDate(date):
    """Convert Taiwanese date format (ROC) to Gregorian date format."""
    year_str = str(date)[:3]  # Extract the ROC year
    real_year = int(year_str) + 1911  # Convert to Gregorian year
    real_date = f"{real_year}{str(date)[4:6]}{str(date)[7:9]}"  # Combine date components
    return real_date

# Base URL for fetching stock data
url_base = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=2017'
url_tail = '01&stockNo=2317&_=1521363562193'  # URL tail
file_path = 'stockyear2017.csv'

# Check if the file already exists, if not create it
if not os.path.isfile(file_path):
    with open(file_path, 'a', newline='', encoding='utf-8') as output_file:  # Use context manager for file handling
        output_writer = csv.writer(output_file)

        for month in range(1, 13):  # Loop through each month
            url_twse = url_base + twodigit(month) + url_tail  # Construct URL
            res = requests.get(url_twse)  # Fetch data
            jdata = json.loads(res.text)  # Parse JSON response
            
            if month == 1:  # Write column names only for January
                output_writer.writerow(jdata['fields'])
            
            # Write monthly data to CSV
            for data_line in jdata['data']:
                output_writer.writerow(data_line)

            time.sleep(0.5)  # Delay to avoid request errors

# Read the CSV file using pandas
pd_stock = pd.read_csv(file_path, encoding='utf-8')

# Convert dates from ROC format to Gregorian format
pd_stock['日期'] = pd_stock['日期'].apply(convertDate)
pd_stock['日期'] = pd.to_datetime(pd_stock['日期'])  # Convert to datetime format

# Prepare data for plotting
data = [
    Scatter(x=pd_stock['日期'], y=pd_stock['收盤價'], name='收盤價'),
    Scatter(x=pd_stock['日期'], y=pd_stock['最低價'], name='最低價'),
    Scatter(x=pd_stock['日期'], y=pd_stock['最高價'], name='最高價')
]


import plotly.graph_objs as go

# Prepare your figure
fig = {
    "data": data,
    "layout": Layout(title='2017年個股統計圖')
}

# Save the plot as an HTML file and open it in a web browser
plotly.offline.plot(fig, filename='stock_plot', auto_open=True)


# Plot the data using Plotly
# plotly.offline.iplot({
#     "data": data,
#     "layout": Layout(title='2017年個股統計圖')
# })