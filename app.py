from flask import Flask, render_template, request
import csv
from datetime import datetime

app = Flask(__name__)

# Funzione per normalizzare l'URL inserito dall'utente
def normalize_url(url):
    url = url.lower().strip()
    if url.startswith("http://"):
        url = url[7:]
    elif url.startswith("https://"):
        url = url[8:]
    if url.startswith("www."):
        url = url[4:]
    return url.strip('/')

# Caricamento della lista di URL di phishing normalizzati da file
with open('unique_phishing_urls.txt', 'r') as file:
    phishing_list = [normalize_url(line) for line in file if line.strip()]

# Rotta principale della web app
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        input_url = request.form['url']  # Prende l'URL inserito dall'utente
        normalized = normalize_url(input_url)  # Normalizza l'URL

        # Verifica se l'URL è presente nella lista dei siti di phishing
        if normalized in phishing_list:
            result = f'❌ Attenzione! {input_url} è un sito di phishing.'
        else:
            result = f'✅ {input_url} non è un sito di phishing.'

        # Salvataggio del risultato in un file CSV di log
        with open('log_verifiche.csv', 'a', newline='', encoding='utf-8') as log:
            writer = csv.writer(log)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), input_url, result])

    return render_template('index.html', result=result)

# Rotta per visualizzare lo storico delle verifiche effettuate
@app.route('/storico')
def storico():
    dati = []
    try:
        with open('log_verifiche.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            dati = list(reader)  # Legge tutte le righe come lista
    except FileNotFoundError:
        pass  # Nessun file trovato = nessuna verifica ancora effettuata

    return render_template('storico.html', storico=dati)

# Avvio dell'app Flask
if __name__ == '__main__':
    app.run(debug=True)
