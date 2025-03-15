import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# 🌍 URL der Bundestagsseite für die Plenarprotokolle der 20. Wahlperiode
URL = "https://www.bundestag.de/services/opendata"

# 📁 Speicherort für XML-Dateien
SAVE_DIR = "bundestag_protokolle"
os.makedirs(SAVE_DIR, exist_ok=True)


def get_xml_links():
    """Findet alle XML-Links mit Selenium"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Läuft unsichtbar im Hintergrund
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(URL)

    time.sleep(5)  # Warten, bis JavaScript die Seite geladen hat

    xml_links = []
    links = driver.find_elements(By.TAG_NAME, "a")

    for link in links:
        url = link.get_attribute("href")
        if url and "/resource/blob/" in url and url.endswith(".xml"):
            xml_links.append(url)

    driver.quit()
    return xml_links


def download_xml_files():
    """Lädt die gefundenen XML-Dateien herunter"""
    xml_links = get_xml_links()

    if not xml_links:
        print("❌ Keine XML-Links gefunden!")
        return

    print(f"📥 {len(xml_links)} XML-Dateien gefunden. Starte Download...")

    for link in xml_links:
        filename = os.path.join(SAVE_DIR, link.split("/")[-1])
        response = requests.get(link)

        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"✅ Gespeichert: {filename}")
        else:
            print(f"⚠️ Fehler beim Download: {link}")


if __name__ == "__main__":
    download_xml_files()