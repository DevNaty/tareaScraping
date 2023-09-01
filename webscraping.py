import requests
from bs4 import BeautifulSoup

def web_scraping(url):
    # Hacer una solicitud HTTP a la página web
    response = requests.get(url)
    
    # Analizar el contenido HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Obtener el título de la página
    title = soup.title.string
    print("Título de la página:", title)
    
    # Obtener el primer párrafo del artículo
    primer_parrafo = soup.find('p').text
    print("Primer párrafo:", primer_parrafo)
    
    # Obtener todos los enlaces en la página
    enlaces = soup.find_all('a')
    print("Enlaces:")
    for enlace in enlaces:
        print(enlace['href'])

if __name__ == "__main__":
    url = 'https://www.mercadolibre.com.ar/'
    web_scraping(url)