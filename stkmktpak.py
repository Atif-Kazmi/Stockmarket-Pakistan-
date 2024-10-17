import streamlit as st
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Function to fetch data from Pakistan Stock Exchange
def fetch_psx_data():
    url = 'https://www.psx.com.pk/market-summary'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Create a session with retry mechanism
    session = requests.Session()
    retry = Retry(
        total=5,  # Retry up to 5 times
        backoff_factor=1,  # Wait 1 second between retries
        status_forcelist=[500, 502, 503, 504]  # Retry on server errors
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        # Send the request with a timeout of 20 seconds
        response = session.get(url, headers=headers, timeout=20)
        response.raise_for_status()  # Raise exception if the status code is not 200
        
        # Parse the response using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Debug: Print the raw HTML content to understand the structure
        st.text(soup.prettify())  # This will show the structure of the HTML

        # Scrape stock data from the table using specific tags or classes
        stock_data = []
        table = soup.find('table', {'class': 'table table-condensed'})  # Adjusted for table class

        if table:
            rows = table.find_all('tr')
            for row in rows[1:]:  # Skipping header row
                columns = row.find_all('td')
                if len(columns) > 0:
                    stock = {
                        'symbol': columns[0].text.strip(),
                        'company': columns[1].text.strip(),
                        'price': columns[2].text.strip(),
                        'change': columns[3].text.strip(),
                        'volume': columns[4].text.strip()
                    }
                    stock_data.append(stock)

        # Check if data was scraped
        if not stock_data:
            st.warning("No stock data was found.")
        
        return stock_data

    except requests.exceptions.RequestException as e:
        # Display an error message on the Streamlit app if any issues arise
        st.error(f"Error fetching PSX data: {e}")
        return []

# Streamlit app starts here
st.title("Pakistan Stock Exchange Live Stock Market App")

# Fetch the stock data from the PSX website
data = fetch_psx_data()

# Display the stock data if it is available
if data:
    st.write(data)
else:
    st.write("No stock data available at the moment.")
