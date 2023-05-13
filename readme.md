# App de Notícias do Dólar e seu cenário

Esse é um app que coleta notícias sobre o dólar no Brasil do feed do Google Notícias e as exibe em uma página web e, com base no conteúdo delas, inclui uma análise de sentimento das notícias, indicando se o mercado está em alta ou em baixa usando o modelo de linguagem natural do ChatGPT da OpenAI.

## Requerimentos

- Python 3.6 ou superior
- pipenv

## Instalação

1. Clone este repositório para sua máquina local.
2. Navegue até a pasta raiz do projeto.
3. Execute o comando `pipenv install` para instalar as dependências.

## Utilização

1. Execute o comando `pipenv shell` para ativar o ambiente virtual.
2. Execute `news_scraper.py` para criar o banco de dados de notícias com base no feed do Google Notícias.
3. Execute o comando `python app.py` para iniciar o servidor Flask.
4. Abra o navegador e acesse a URL `http://localhost:5000`.

### Endpoints

- `/news`: Exibe as notícias mais recentes por data.
- `/news?date=YYYY-MM-DD`: Filtra as notícias pela data especificada.

## Tecnologias Utilizadas

- Python
- Flask
- Openai (NLP)
- Webscraping
- SQLite
- Jinja2
- Bootstrap

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo LICENSE para obter mais informações.
