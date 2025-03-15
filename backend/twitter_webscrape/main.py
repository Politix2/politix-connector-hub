from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# Twitter handles of German politicians
german_politicians = [
    "Bundeskanzler", "OlafScholz", "ABaerbock", "c_lindner", "NancyFaeser",
    "MarcoBuschmann", "cem_oezdemir", "Karl_Lauterbach", "KevinKuHnert", "Ricarda_Lang",
    "RobertHabeck", "Markus_Soeder", "HendrikWuest", "MPKretschmer", "jensspahn",
    "PaulZiemiak", "Alice_Weidel", "TinoChrupalla", "BjoernHoecke", "SWagenknecht",
    "DieterJanecek", "CarloMasala1"
]

# Set up Selenium WebDriver
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
# For testing purposes, let's comment out headless mode to see what's happening visually
# options.add_argument("--headless")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

tweets_data = []

# Loop through each politician's Twitter profile
for username in german_politicians:
    print(f"Starting to scrape now for {username}")
    try:
        url = f"https://twitter.com/{username}"
        driver.get(url)

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//article[@data-testid="tweet"]'))
        )

        # Optional: Scroll down to load more tweets (to ensure more are loaded)
        for _ in range(5):  # Scroll 5 times
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

        tweets = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')

        for tweet in tweets[:20]:  # CHANGE THE NUMBER OF TWEETS THAT SHOULD BE PULLED PER PERSON HERE
            try:
                timestamp = tweet.find_element(By.TAG_NAME, "time").get_attribute("datetime")
                content = tweet.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text

                tweets_data.append({
                    "TwitterHandle": username,
                    "Timestamp": timestamp,
                    "Content": content
                })
            except Exception as e:
                print(f"Error extracting tweet for {username}: {e}")

    except Exception as e:
        print(f"Error fetching tweets for {username}: {e}")

# Save tweets to JSON
with open("german_politicians_tweets.json", "w", encoding="utf-8") as f:
    json.dump(tweets_data, f, ensure_ascii=False, indent=4)

driver.quit()
print("Tweets saved to german_politicians_tweets.json")
