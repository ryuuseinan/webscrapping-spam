import random
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

# Función para cargar palabras filtradas desde un archivo
def load_filtered_words(filepath):
    """
    Carga palabras de un archivo, filtrando aquellas con 3 o 4 caracteres.
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if 3 <= len(line.strip()) <= 4]

# Función para generar un RUT válido
def generate_valid_rut():
    """Genera un RUT chileno válido con dígito verificador (DV)"""
    number = random.randint(1500000, 22000000)  # Genera un número base para el RUT
    total = 0
    multiplier = 2

    # Cálculo del módulo 11
    for digit in reversed(str(number)):
        total += int(digit) * multiplier
        multiplier += 1
        if multiplier > 7:
            multiplier = 2

    remainder = 11 - (total % 11)
    if remainder == 11:
        dv = '0'
    elif remainder == 10:
        dv = 'K'
    else:
        dv = str(remainder)

    return f"{number}-{dv}"

# Función para generar una contraseña usando palabras filtradas
def generate_password(filtered_words):
    """
    Genera una contraseña combinando una palabra filtrada y números aleatorios.
    """
    word = random.choice(filtered_words)  # Selecciona una palabra de 3 o 4 caracteres
    numbers = ''.join(random.choices('0123456789', k=random.choice([3, 4])))  # Genera 3 o 4 números
    return word + numbers  # Combina la palabra con los números

# Función para generar un código de seis dígitos
def generate_six_digit_code():
    return ''.join(random.choices('0123456789', k=6))

# Función principal para realizar las operaciones
def execute_workflow(filtered_words, website):
    options = Options()
    
    if os.name == 'nt':  # Windows
        options.binary_location = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    else:  # Linux
        options.binary_location = '/usr/bin/google-chrome-stable'

    # Usar Service en lugar de executable_path
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Abrir la URL
        driver.get(website)
        sleep(3)

        # Generar un RUT válido y una contraseña realista
        generated_rut = generate_valid_rut()
        generated_password = generate_password(filtered_words)

        # Interactuar con el formulario de inicio de sesión
        username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="rut"]'))
        )
        password = driver.find_element(By.XPATH, '//*[@id="pass"]')
        login = driver.find_element(By.XPATH, '//*[@id="btnLogin"]')

        username.send_keys(generated_rut)
        password.send_keys(generated_password)
        print(f"Se generó y utilizó el RUT: {generated_rut}")
        print(f"Se generó y utilizó la contraseña: {generated_password}")

        login.click()  # index1

        # Esperar la generación del código de seis dígitos
        sleep(30)  # index2

        # Interactuar con el código de seis dígitos
        bepass_code = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="rut"]'))
        )
        six_digit_code = generate_six_digit_code()

        # Volver a localizar el botón de login si es necesario
        bepass_code.clear()
        bepass_code.send_keys(six_digit_code)
        print(f"Se envió el código de seis dígitos: {six_digit_code}")

        login = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="btnLogin"]'))
        )
        login.click()  # index3

        sleep(75)  # index4

        # Volver a localizar el código de seis dígitos y el botón de login
        bepass_code = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="rut"]'))
        )
        bepass_code.clear()
        bepass_code.send_keys(six_digit_code)
        print(f"Se envió el código de seis dígitos: {six_digit_code}")

        login = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="btnLogin"]'))
        )
        login.click()  # index5

        sleep(30)  # index6

        #accept js alert
        driver.switch_to.alert.accept()
        print("alert accepted")
        sleep(3)

        six_digit_code = generate_six_digit_code()
        # Volver a interactuar con el código y el botón de login
        bepass_code = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="rut"]'))
        )
        bepass_code.clear()
        bepass_code.send_keys(six_digit_code)
        print(f"Se envió el código de seis dígitos bepass: {six_digit_code}")

        login = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="btnLogin"]'))
        )
        login.click()  # index7
        sleep(5)
        
    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Cerrar el navegador
        driver.quit()

# Cargar palabras filtradas desde el archivo
file_path = 'richelieu-french-top5000.txt'  # Cambia esto a la ruta de tu archivo
filtered_words = load_filtered_words(file_path)

if not filtered_words:
    print("No se encontraron palabras válidas en el archivo.")
    exit()

# URL del sitio
website = 'http://bb10bb10bb00.zya.me/?i=1'

# Ejecutar el flujo en bucle
while True:
    execute_workflow(filtered_words, website)
    print("Reiniciando flujo...\n")
