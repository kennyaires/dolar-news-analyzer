import os
import sqlite3
from flask import (
    Flask,
    request,
    render_template,
    redirect
)

from datetime import datetime
from collections import Counter
from news_analyzer import CurrencyAnalyzer


app = Flask(__name__)

DB_NAME = 'noticias.db'
DEFAULT_DATE = '2023-05-10'

# Instancia o analisador de notícias
ai = CurrencyAnalyzer(os.environ.get('OPENAI_API_KEY'))


def analyze_news(news):
    """
    :param news: a list of news
    :return: average of sentiment scores
    """
    sentiments = []
    for n in news:
        sentiments.append(ai.analyze(n))
    counter = Counter(sentiments)
    market_status = counter.most_common(1)[0][0]
    return market_status


@app.route('/', methods=['GET'])
def index():
    return redirect('/news?date={}'.format(DEFAULT_DATE))


@app.route('/news', methods=['GET'])
def get_news():
    """
    :param date: data no formato YYYY-MM-DD
    """
    # Obtém a data da query string
    date = request.args.get('date', DEFAULT_DATE)
    date_instance = datetime.strptime(date, '%Y-%m-%d')
    date_str = date_instance.strftime('%d/%m/%Y')

    # Busca as notícias no banco de dados
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM noticias WHERE pub_date LIKE ? LIMIT 3", (f"%{date}%",))
    news_titles = [row[0] for row in cursor.fetchall()]
    conn.close()

    # Analisa as notícias
    market_status = analyze_news(news_titles)

    return render_template('news.html', news_titles=news_titles, date=date_str, market_status=market_status)


if __name__ == '__main__':
    app.run(debug=True)
