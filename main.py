import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from flask import Flask, request, render_template


class WebScraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def scrape_text(self):
        response = requests.get(self.base_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        text_data = soup.get_text()
        return text_data

    def scrape_images(self):
        response = requests.get(self.base_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        images = soup.find_all('img')
        image_urls = [img['src'] for img in images]
        return image_urls

    def scrape_tables(self):
        response = requests.get(self.base_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        tables = soup.find_all('table')
        table_data = []
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                row_data = [cell.get_text() for cell in cells]
                table_data.append(row_data)
        return table_data


class GoogleSearchAPI:
    def __init__(self, api_key, cse_id):
        self.service = build("customsearch", "v1", developerKey=api_key)
        self.cse_id = cse_id

    def search(self, query):
        res = self.service.cse().list(q=query, cx=self.cse_id).execute()
        search_results = res['items']
        return search_results


class DataProcessor:
    def filter_data(self, data, criteria):
        filtered_data = data.loc[criteria]
        return filtered_data

    def sort_data(self, data, sort_by):
        sorted_data = data.sort_values(by=sort_by)
        return sorted_data

    def aggregate_data(self, data, group_by, aggregations):
        aggregated_data = data.groupby(group_by)[aggregations].sum()
        return aggregated_data

    def analyze_data(self, data):
        data_analysis = data.describe()
        return data_analysis


class DataVisualizer:
    def generate_plot(self, data, x, y):
        plt.plot(data[x], data[y])
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(f"{x} vs {y}")
        plt.show()

    def generate_interactive_plot(self, data, x, y):
        fig = px.scatter(data, x=x, y=y)
        fig.show()


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']

    # Creating an instance of the WebScraper class
    scraper = WebScraper(query)

    # Scraping text data from the base URL
    text_data = scraper.scrape_text()

    return render_template('result.html', data=text_data)


if __name__ == '__main__':
    app.run(debug=True)
