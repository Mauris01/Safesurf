import requests
import csv
from datetime import datetime

# 1. Scarica una lista vera da GitHub (senza limiti)
def download_file():
    url = 'https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-domains-ACTIVE.txt'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        with open('phishing_urls.txt', 'w') as file:
            file.write(response.text)
        print("✅ Lista phishing scaricata con successo!")
    else:
        print(f"❌ Errore nel download: {response.status_code}")

# 2. Rimuove duplicati
def remove_duplicates():
    with open('phishing_urls.txt', 'r') as file:
        urls = file.readlines()
    
    unique_urls = sorted(set(url.strip() for url in urls if url.strip() and not url.startswith('#')))
    
    with open('unique_phishing_urls.txt', 'w') as file:
        file.write("\n".join(unique_urls))
    
    print(f"✅ Rimosso duplicati. URL unici trovati: {len(unique_urls)}")

# 3. Salva i dati in CSV
def save_to_csv():
    with open('unique_phishing_urls.txt', 'r') as file:
        urls = [line.strip() for line in file if line.strip()]
    
    data = [["URL", "Data di aggiunta"]]
    today = datetime.today().strftime('%Y-%m-%d')
    data += [[url, today] for url in urls]
    
    with open('phishing_sites.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print("✅ Dati salvati in phishing_sites.csv!")

# 4. Esegui tutto
def main():
    download_file()
    remove_duplicates()
    save_to_csv()

if __name__ == '__main__':
    main()
