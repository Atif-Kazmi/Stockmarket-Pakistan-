import requests
import pandas as pd
from bs4 import BeautifulSoup
import streamlit as st
import plotly.express as px

# Function to fetch PSX data
def fetch_psx_data():
    url = 'https://www.psx.com.pk/market-summary'  # Example PSX URL (adjust if needed)
    
    # Send a request to get the page content
    response = requests.get(url)
    
    # Parse the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract stock data - This example assumes a table structure, you need to adjust based on PSX structure
    stock_data = []
    for row in soup.select('table.stock-table-class tr'):  # Adjust the table selector accordingly
        columns = row.find_all('td')
        if len(columns) > 0:
            stock = {
                'symbol': columns[0].text.strip(),
                'company': columns[1].text.strip(),
                'price': float(columns[2].text.strip().replace(',', '')),
                'change': float(columns[3].text.strip().replace(',', '')),
                'volume': int(columns[4].text.strip().replace(',', ''))
            }
            stock_data.append(stock)
    
    # Convert the list to a Pandas DataFrame
    return pd.DataFrame(stock_data)

# Function to get the top stock by positive price change
def get_top_stock(df):
    df = df[df['change'] > 0]  # Filter only stocks with positive price change
    return df.sort_values(by='change', ascending=False).head(1)

# Streamlit app
st.title("Pakistan Stock Exchange Live Stock Market App")

# Fetch stock data
df = fetch_psx_data()

# Check if the dataframe is empty
if df.empty:
    st.write("No stock data available at the moment.")
else:
    # Display the fetched data
    st.subheader("Current Stock Data from PSX")
    st.write(df)
    
    # Get and display the top stock
    top_stock = get_top_stock(df)
    st.subheader("Top Stock to Watch")
    
    if not top_stock.empty:
        st.write(top_stock)
    else:
        st.write("No stock with positive price change found.")
    
    # Optional: Plot stock data using Plotly
    st.subheader("Stock Prices Visualization")
    fig = px.bar(df, x='company', y='price', color='change', title="Stock Prices Overview")
    st.plotly_chart(fig)
