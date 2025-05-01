def normalize_url(url):
    # Rimuove http://, https:// e www.
    url = url.lower()
    if url.startswith("http://"):
        url = url[len("http://"):]
    elif url.startswith("https://"):
        url = url[len("https://"):]
    if url.startswith("www."):
        url = url[len("www."):]
    return url.strip().strip('/')

def search_phishing_url():
    search_url = input("Inserisci l'URL da verificare (es: http://example.com): ").strip()
    search_url_norm = normalize_url(search_url)

    with open('unique_phishing_urls.txt', 'r') as file:
        phishing_urls = [normalize_url(line) for line in file if line.strip()]

    if search_url_norm in phishing_urls:
        print(f"❌ Attenzione! {search_url} è un sito di phishing!")
    else:
        print(f"✅ {search_url} il sito è sicuro.")

def main():
    search_phishing_url()

if __name__ == '__main__':
    main()
