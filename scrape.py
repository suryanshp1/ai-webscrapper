from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from bs4 import BeautifulSoup
import time
import random

chrome_driver_path = "./chromedriver.exe"

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.5; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
    "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"
]


# def get_free_proxies():
#     try:
        
#         service = Service(chrome_driver_path)

#         options = Options()
#         options.add_argument('--headless')

#         driver = webdriver.Chrome(service=service, options=options)
#         driver.get('https://sslproxies.org')

#         table = driver.find_element(By.TAG_NAME, 'table')
#         thead = table.find_element(By.TAG_NAME, 'thead').find_elements(By.TAG_NAME, 'th')
#         tbody = table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

#         headers = []
#         for th in thead:
#             headers.append(th.text.strip())

#         proxies = []
#         for tr in tbody:
#             proxy_data = {}
#             do_append = True
#             tds = tr.find_elements(By.TAG_NAME, 'td')
#             for i in range(len(headers)):
#                 if headers[i] == "Google" and tds[i].text.strip() == "no":
#                     do_append = False
#                 proxy_data[headers[i]] = tds[i].text.strip()
#             if do_append:
#                 proxies.append(proxy_data)

#         proxies = [f"{proxy['IP Address']}:{proxy['Port']}" for proxy in proxies]
        
#         return proxies

#     except Exception as e:
#         print(f"Error getting free proxies: {e}")
#     finally:
#         driver.quit()

def scrape_website(url):
    print("launching chrome browser.......")

    random_user_agent = random.choice(user_agents)

    # proxies = get_free_proxies()
    # random_proxy = random.choice(proxies)

    options = webdriver.ChromeOptions()

    options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')

    # if random_proxy:
    #     # options.add_argument('--proxy-server={}'.format(random_proxy))
    #     proxy = Proxy({
    #         'proxyType': ProxyType.MANUAL,
    #         'httpProxy': random_proxy,
    #         'sslProxy': random_proxy,
    #         'noProxy': ''})
    #     options.proxy = proxy

    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    driver.execute_cdp_cmd('Network.setUserAgentOverride', {'userAgent': random_user_agent})

    try:
        driver.get(url)
        print("Page is successfully loaded......")
        html_content = driver.page_source
        time.sleep(3)
        return html_content
    except Exception as e:
        print(f"Error scraping website: {e}")
        driver.quit()

    finally:
        driver.quit()


def scrape_body_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    body_content = soup.find('body')
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, 'html.parser')

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")

    cleaned_content = "\n".join([line.strip() for line in cleaned_content.splitlines() if line.strip()])

    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i:i+max_length] for i in range(0, len(dom_content), max_length)
    ]

