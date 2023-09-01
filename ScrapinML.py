import requests
import io
import re
from bs4 import BeautifulSoup
import tkinter as tk
from PIL import Image, ImageTk
import base64

def scrape_and_display():
    url = 'https://www.mercadolibre.com.ar/ofertas#c_id=/home/promotions-recommendations&c_uid=0908d5b0-83ed-4d6f-ac4f-600c2cdce31f'
    response = requests.get(url)

    if response.status_code == 200:
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')    

        recommendation_elements = soup.find_all('li', class_='promotion-item avg')

        # Eliminar los widgets anteriores dentro de result_frame
        for widget in result_frame.winfo_children():
            widget.destroy()

        for recommendation in recommendation_elements:   
            imagen_tag = recommendation.find('img', class_='promotion-item__img')
            imagen_url = imagen_tag.get('src')  # Obtener la URL de la imagen
            
            # Manejar imágenes base64
            if imagen_url.startswith("data:image"):
                img_data = re.sub('^data:image/.+;base64,', '', imagen_url)
                img_data = base64.b64decode(img_data)
                img = Image.open(io.BytesIO(img_data))
            else:
                img_response = requests.get(imagen_url)
                img_data = img_response.content
                img = Image.open(io.BytesIO(img_data))
            
            
            img = img.resize((150, 150))  # Ajustar el tamaño de la imagen si es necesario
            img = ImageTk.PhotoImage(img)
        
            # Crear un nuevo frame para cada producto
            product_frame = tk.Frame(result_frame)
            product_frame.pack(pady=10)

            img_label = tk.Label(product_frame, image=img)           
            img_label.image = img
            img_label.pack(side='top')

            description = recommendation.find('p', class_='promotion-item__title')
            PrecioActual = recommendation.find('span', class_='andes-money-amount__fraction')
            Descuento = recommendation.find('span', class_='andes-money-amount__discount')
            
            description_label = tk.Label(product_frame, text=f'Descripción: {description.text.strip()}')
            description_label.pack(side='top')

            precio_label = tk.Label(product_frame, text=f'Precio: {PrecioActual.text}')
            precio_label.pack(side='top')

            descuento_label = tk.Label(product_frame, text=f'Descuento: {Descuento.text}')
            descuento_label.pack(side='top')

            separator = tk.Frame(product_frame, height=1, width=300, bd=1, relief='sunken')
            separator.pack(side='top', pady=5, fill='x')

        result_text.insert(tk.END, 'Proceso completado.\n')
    else:
        result_text.insert(tk.END, f'Error al obtener la página: {response.status_code}\n')

# Crear la interfaz de usuario
root = tk.Tk()
root.title('Scraping App')

scrape_button = tk.Button(root, text='Ofertas Mercado Libre', command=scrape_and_display)
scrape_button.pack()

result_text = tk.Text(root, height=2, width=150)
result_text.pack()

# Crear un Canvas y asociarlo con un Scrollbar
canvas = tk.Canvas(root, height=780)
canvas.pack(side='left', fill='both', expand=True)
root.geometry("780x800") 

scrollbar = tk.Scrollbar(root, command=canvas.yview)
scrollbar.pack(side='right', fill='y')
canvas.configure(yscrollcommand=scrollbar.set)

# Crear un Frame dentro del Canvas para contener los productos
result_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=result_frame, anchor='nw')

# Configurar el Scrollbar para que funcione con el Canvas
def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox('all'))
    print('La función on_configure ha sido llamada.')

result_frame.bind('<Configure>', on_configure)
print('quepasara aqui?')

root.mainloop()