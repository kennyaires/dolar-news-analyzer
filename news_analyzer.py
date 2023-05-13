import openai


class CurrencyAnalyzer:

    def __init__(self, openai_apikey):
        """
        :param openai_apikey: API key da OpenAI
        """
        self.openai_instance = openai
        self.openai_instance.api_key = openai_apikey

        self.prompt = \
            "Responda com \"alta\" ou \"baixa\", qual o cenário do dólar "\
            "no Brasil com base nessa notícia: "
        self.chatgpt_engine = "text-davinci-003"

    def analyze(self, news):
        """
        :param news: a list of news
        :return: average of sentiment scores
        """
        result = self.openai_instance.Completion.create(
            engine="text-davinci-003",
            prompt=f"{self.prompt}{news}",
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return self.parse_result(result)

    @staticmethod
    def parse_result(result):
        """
        :param result: OpenAI Completion object
        :return: sentiment score
        """
        sentiment = result.choices[0].text.strip()
        sentiment = 'alta' if 'alta' in sentiment.lower() else 'baixa'
        return sentiment


if __name__ == '__main__':
    pass
#     open_apikey = os.environ.get('OPENAI_API_KEY')
#     ai = CurrencyAnalyzer(open_apikey)

#     news = [
#         'Dólar sobe a R$ 5,163, após falas de Lula sobre salário mínimo...',
#         'Preços da soja têm alta graças à elevação do dólar',
#         'Dólar despenca 2,5% ...'
#     ]
#     for n in news:
#         print(f"\"{n}\": ", ai.analyze(n))
