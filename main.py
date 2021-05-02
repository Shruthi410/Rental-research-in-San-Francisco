from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from time import sleep

CHROME_DRIVER_PATH = "C:/Development/chromedriver.exe"
FORMS_URL = "https://docs.google.com/forms/d/e/1FAIpQLScsPKLUPOuPe9GIPVvQdvxT8x9aepB2S91QKGgJ9uw7TOp_pA/viewform?usp=sf_link"
ZILLOW_URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,ta;q=0.7"
}

response = requests.get(url=ZILLOW_URL, headers=HEADERS)
soup = BeautifulSoup(response.content, "lxml")

link_tags = soup.select(".list-card-top a")

all_links = []
for link in link_tags:
    href = link["href"]
    if "https" not in href:
        all_links.append(f"https://www.zillow.com{href}")
    else:
        all_links.append(href)

address_tags = soup.select(".list-card-info address")
all_addresses = [address.text.split(" | ")[-1] for address in address_tags]

price_element_text = soup.find_all(name="div", class_="list-card-price")

replaced_element_text = []
for price in price_element_text:
    if "+" in price.text:
        replaced_str = price.text.replace("+", " ")
        replaced_element_text.append(replaced_str)
    elif "/" in price.text:
        replaced_str = price.text.replace("/", " ")
        replaced_element_text.append(replaced_str)
    elif " " in price.text:
        replaced_element_text.append(price.text)

all_prices = [price.split(" ")[0] for price in replaced_element_text]

print(all_prices)
print(all_addresses)
print(all_links)

driver = webdriver.Chrome(CHROME_DRIVER_PATH)
driver.get(FORMS_URL)
sleep(5)


for n in range(len(all_links)):
    driver.get(FORMS_URL)

    sleep(2)
    address = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div')

    address.send_keys(all_addresses[n])
    price.send_keys(all_prices[n])
    link.send_keys(all_links[n])
    submit_button.click()