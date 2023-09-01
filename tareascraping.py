import requests
from bs4 import BeautifulSoup

url = 'https://www.mercadolibre.com.ar/ofertas#c_id=/home/promotions-recommendations&c_uid=0908d5b0-83ed-4d6f-ac4f-600c2cdce31f'
response = requests.get(url)

if response.status_code == 200:
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')    

    recommendation_elements = soup.find_all('li', class_='promotion-item avg')

    for recommendation in recommendation_elements:   
        imagen = recommendation.find  ('img')  
        description = recommendation.find('p', class_='promotion-item__title')
        PrecioActual = recommendation.find('span', class_='andes-money-amount__fraction')
        Descuento = recommendation.find('span', class_='andes-money-amount__discount')        

        if description and PrecioActual and Descuento:
            print('Img:', imagen)
            print('Descripción:', description.text.strip())
            print('Precio:', PrecioActual.text)
            print('Descuento:', Descuento.text)

        else:
            print('Información incompleta para este producto')
else:
    print('Error al obtener la página:', response.status_code)
