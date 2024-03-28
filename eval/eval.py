import os
#set your environment variable for SSL certificate
certi_path = certi_path = "C:/laragon/bin/python/python-3.10/Lib/site-packages/pip/_vendor/certifi/cacert.pem"
os.environ['REQUESTS_CA_BUNDLE'] = certi_path
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


import requests
from bs4 import BeautifulSoup

# Initialize Chrome options
options = Options()
#options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
#disable the browser
#options.add_argument("--headless")
options.add_argument("--disable-extensions")
options.add_argument("--ignore-certificate-errors")

# Initialize Chrome WebDriver with the specified options
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


# waits up to 10 seconds before throwing a NoSuchElementException
driver.implicitly_wait(10)


url = "https://www.meshistoiresdusoir.fr/g/contes/"
data       = []

driver.get(url)
soup  = BeautifulSoup(driver.page_source)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

# Scraping des histoires
data = []

while True:
    # Cliquer sur le bouton pour charger plus d'histoires
    try:
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'loadmorebtn')))
        button.click()
        
        time.sleep(2)
    except:
        print("Toutes les histoires ont été chargées.")
        break

# Attendre que l'id "alert_no_more_stories" soit présent
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'alert_no_more_stories')))


# Récupérer toutes les histoires
cc = soup.find_all("h3", class_="h4 card-title")

# Parcourir les histoires et les ajouter à la liste des données
for histoires in cc:
    name = histoires.find("a").text
    print(name)

    data.append({
        "name": name,
    })

import pandas as pd
# Création du DataFrame
df = pd.DataFrame(data)

# Transformation en CSV
df.to_csv('./histoires.csv', index=False)

from sqlalchemy import create_engine
# Mise en base de données
# Définir les informations de connexion à la base de données MySQL
user = 'root'
password = ''
host = 'localhost'
port = '3306'
database = 'Histoires'

# Créer une connexion à la base de données
engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}")

# Créer la table dans la base de données et insérer les données
df.to_sql('histoire', con=engine, if_exists='replace', index=False)

# Fermer la connexion à la base de données
engine.dispose()