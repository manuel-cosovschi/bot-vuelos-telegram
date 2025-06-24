from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime, timedelta

def scrape_rango(origen, destino, salida_inicio, salida_fin, dias_estadia, umbral):
    resultados = []
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    salida_actual = datetime.strptime(salida_inicio, "%Y-%m-%d")
    fin = datetime.strptime(salida_fin, "%Y-%m-%d")

    while salida_actual <= fin:
        regreso = salida_actual + timedelta(days=dias_estadia)
        fecha_ida = salida_actual.strftime("%Y-%m-%d")
        fecha_vuelta = regreso.strftime("%Y-%m-%d")

        url = f"https://www.kiwi.com/en/search/results/{origen}/{destino}/{fecha_ida}/{fecha_vuelta}"

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        time.sleep(10)

        try:
            price_element = driver.find_element(By.CLASS_NAME, "ResultCardPrice__price")
            precio_texto = price_element.text
            precio = int("".join(filter(str.isdigit, precio_texto)))

            if precio <= umbral:
                resultados.append({
                    "ruta": f"{origen.upper()} → {destino.upper()}",
                    "ida": fecha_ida,
                    "vuelta": fecha_vuelta,
                    "precio": precio,
                    "url": url
                })
        except:
            pass
        driver.quit()
        salida_actual += timedelta(days=2)

    return resultados
