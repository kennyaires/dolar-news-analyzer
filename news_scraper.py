import json
import sqlite3
import requests
import xml.etree.ElementTree as ET

from datetime import datetime


class Noticia:
    def __init__(self, title, pub_date):
        self.title = title
        self.pub_date = self.parse_date(pub_date)

    def __str__(self):
        return f"{self.pub_date}:{self.title}\n"
    
    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def parse_date(date_str):
        return \
            datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z").isoformat().split('T')[0] # noqa


class RSSScraper:
    def __init__(self, rss_url, sources=[], save_output=True, save_to_db=False):
        self.rss_url = rss_url
        self.sources = sources
        self.save_output = save_output
        self.save_to_db = save_to_db

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.filename = f'noticias-{timestamp}.jl'

    def scrape(self):
        response = requests.get(self.rss_url)
        root = ET.fromstring(response.content)
        noticias = []
        for item in root.findall("./channel/item"):
            source = item.find("source").text
            if self.sources and source not in self.sources:
                continue

            title = item.find("title").text
            pub_date = item.find("pubDate").text
            noticia = Noticia(title, pub_date)
            noticias.append(noticia)
        
        if self.save_output:
            self.generate_output_file(noticias)
        
        if self.save_to_db:
            self.generate_db_file(noticias)

        return noticias

    def generate_output_file(self, noticias):
        with open(self.filename, 'w') as f:
            for noticia in noticias:
                f.write(noticia.to_json())
                f.write("\n")

    def generate_db_file(self, noticias):
        conn = sqlite3.connect('noticias.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS noticias
            (title text, pub_date text)''')

        for noticia in noticias:
            c.execute("INSERT INTO noticias VALUES (?, ?)", (noticia.title, noticia.pub_date))

        conn.commit()
        conn.close()


if __name__ == '__main__':
    pass
#     rss_url = "https://news.google.com/rss/search?q=dolar&hl=pt-BR&gl=BR&ceid=BR:pt-419"
#     scraper = RSSScraper(rss_url, save_to_db=True)
#     noticias = scraper.scrape()

#     for n in noticias:
#         print(n)
