from pyparsing import html_comment
import speech_recognition as sr
import subprocess as sub
import pyttsx3
import pywhatkit
import os
import urllib.request
import json
import datetime
import wikipedia
import webbrowser
import time
from bs4 import BeautifulSoup
import os
import webbrowser
import pyttsx3
import requests
from bs4 import BeautifulSoup
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech.audio import AudioOutputConfig

def synthesize_to_speaker(text):
    speech_config = speechsdk.SpeechConfig(subscription="65d81891799044ecb266b3e853c676b6", region="southcentralus", speech_recognition_language="es-CO")
    audio_config = AudioOutputConfig(use_default_speaker=True)
    speech_config.speech_synthesis_language = "es-CO"
    speech_config.speech_synthesis_voice_name = "es-CO-SalomeNeural"
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    synthesizer.speak_text_async(text)

name = 'samantha'
listener = sr.Recognizer()

sites = {
    'google': 'google.com',
    'yahoo': 'yahoo.com',
    'youtube': 'youtube.com',
    'facebook': 'facebook.com',
    'instagram': 'instagram.com',
    'whatsapp': 'web.whatsapp.com',
    'asistente': 'chat.openai.com',
    'amazon': 'amazon.com',
    'ebay': 'ebay.com',
    'whirlpool': 'whirlpool.com',
}

def talk(text):
    synthesize_to_speaker(text)

def listen():
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source)
            print("Escuchando...")
            voice = listener.listen(source)
            rec = listener.recognize_google(voice, language="es-CO")
            rec = rec.lower()
            if name in rec:
                rec = rec.replace(name, '')
                print(rec)
    except:
        pass
    return rec

def open_store():
    webbrowser.open(url)

def get_product_info():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    product_list = soup.find_all("div", class_="swiper-slide slide")

    if product_list:
        products = []
        for item in product_list:
            product_name_elem = item.find("h3")
            product_price_elem = item.find("div", class_="price")
            if product_name_elem and product_price_elem:
                product_name = product_name_elem.text.strip()
                product_price = product_price_elem.text.strip()
                products.append(f"Nombre: {product_name}, Precio: {product_price}")

        return products
    else:
        return None

def run():
    
    # listening = True  # Variable para controlar la escucha

    while True:
        def pause_listen(seconds):
            time.sleep(seconds)

        rec = listen()
        if 'reproduce' in rec:
            music = rec.replace('reproduce', '')
            talk('Reproduciendo ' + music)
            pywhatkit.playonyt(music)

        elif 'hora' in rec:
            hora = datetime.datetime.now().strftime('%I:%M %p')
            talk("Son las " + hora)

        elif 'busca' in rec:
            search = rec.replace('busca', '')
            wikipedia.set_lang("es")
            info = wikipedia.summary(search, 1)
            print(search + ": " + info)
            talk(info)
            pause_listen(60)

        elif 'abre' in rec:
            for site in sites:
                if site in rec:
                    sub.call(f'start chrome.exe {sites[site]}', shell=True)
                    talk(f'Abriendo {site}')

        elif 'hola' in rec:
            def pause_listen(seconds):
                time.sleep(seconds)
            saludo = rec.replace('hola', '')
            pause_listen(3)
            saludar = saludo + "Hola, mi nombre es Samantha. ¿En qué te puedo ayudar?"
            talk(saludar)

        elif 'amazon' in rec:
            def pause_listen(seconds):
                time.sleep(seconds)
            print("¿Quieres comprar algo en específico?")
            talk("¿Quieres comprar algo en específico?")
            pause_listen(3)
            rec = listen()
            if rec:
                search_query = urllib.parse.quote(rec)
                webbrowser.open("https://www.amazon.es/s?k=" + search_query + "&__mk_es_ES=ÅMÅŽÕÑ&ref=nb_sb_noss_2")
            else:
                webbrowser.open("https://www.amazon.es/")

        elif 'abrir tienda' in rec:
            def pause_listen(seconds):
                time.sleep(seconds)
            talk("Abriendo la tienda en tu navegador...")
            open_store()
            pause_listen(3)
            rec = listen()
                    
        elif 'productos' in rec:
         talk("Obteniendo información de los productos...")
         products = get_product_info()
         pause_listen(3)

         if products:
          talk("Aquí tienes la información de los productos:")
          product_info = '\n'.join(products)
          pause_listen(3)
          talk(product_info)
          pause_listen(60)
         else:
          talk("Lo siento, no se encontraron productos en la tienda.")

        elif 'salir' in rec:
         farewell_message = "Hasta luego. ¡Que tengas un buen día!"
         talk(farewell_message)
         break


if __name__ == "__main__":
    url = "http://localhost/TRAVEL_AGENCY-Final/principal.php#home"
    run()
