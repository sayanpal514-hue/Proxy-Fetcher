import requests
import concurrent.futures
import threading
import time
import sys

# ==========================================
# CONFIGURATION
# ==========================================
OUTPUT_FILE = "live.txt"
TEST_URL = "http://www.google.com"  
TIMEOUT = 3  
MAX_WORKERS_SCRAPE = 40  
MAX_WORKERS_CHECK = 200  

URLS = [
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://www.proxy-list.download/api/v1/get?type=socks4",
    "https://www.proxy-list.download/api/v1/get?type=socks5",
    "https://api.openproxylist.xyz/http.txt",
    "https://api.openproxylist.xyz/socks4.txt",
    "https://api.openproxylist.xyz/socks5.txt",
    "https://proxyspace.pro/http.txt",
    "https://proxyspace.pro/https.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks4.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/https.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks4.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/https/https.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks4/socks4.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks5/socks5.txt",
    "https://sunny9577.github.io/proxy-scraper/generated/http_proxies.txt",
    "https://sunny9577.github.io/proxy-scraper/generated/socks4_proxies.txt",
    "https://sunny9577.github.io/proxy-scraper/generated/socks5_proxies.txt"
]

file_lock = threading.Lock()
live_count = 0

def print_banner():
    """Prints a large, bold welcome banner with contact info."""
    banner = """
  ███████╗ █████╗ ██╗   ██╗ █████╗ ███╗   ██╗
  ██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗████╗  ██║
  ███████╗███████║ ╚████╔╝ ███████║██╔██╗ ██║
  ╚════██║██╔══██║  ╚██╔╝  ██╔══██║██║╚██╗██║
  ███████║██║  ██║   ██║   ██║  ██║██║ ╚████║
  ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝
                                                                            
=============================================================================
[*] ADVANCED PROXY SCRAPER & LIVE CHECKER 

=============================================================================
    """
    print(banner)

def fetch_proxies_from_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text.replace('\r', '').split('\n')
    except:
        pass
    return []

def check_and_save_proxy(proxy):
    global live_count
    proxy_dict = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }
    
    try:
        response = requests.get(TEST_URL, proxies=proxy_dict, timeout=TIMEOUT, allow_redirects=True)
        if response.status_code == 200 and "google" in response.text.lower():
            print(f"[STILL LIVE] {proxy}")
            with file_lock:
                with open(OUTPUT_FILE, "a", encoding="utf-8") as file:
                    file.write(f"{proxy}\n")
                    file.flush()
                live_count += 1
    except:
        pass

def main():
    if sys.platform.startswith('win'):
        import asyncio
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Print the custom banner first
    print_banner()

    start_time = time.time()
    unique_proxies = set()
    
    print("=" * 77)
    print(" PHASE 1: MASSIVE LIVE SCRAPING ".center(77, "="))
    print("=" * 77)
    print(f"[*] Fetching from {len(URLS)} active APIs & endpoints...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS_SCRAPE) as executor:
        results = executor.map(fetch_proxies_from_url, URLS)
        for result in results:
            for proxy in result:
                proxy = proxy.strip()
                if ":" in proxy and len(proxy) >= 10 and not proxy.startswith("#") and "<" not in proxy:
                    unique_proxies.add(proxy)

    if not unique_proxies:
        print("[!] ERROR: No proxies extracted. Please check your network connection.")
        return

    print(f"[*] SUCCESS: Extracted {len(unique_proxies)} unique candidate proxies.")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        pass

    print("\n" + "=" * 77)
    print(" PHASE 2: REAL-TIME LIVE VERIFICATION ".center(77, "="))
    print("=" * 77)
    print(f"[*] Testing with {MAX_WORKERS_CHECK} parallel threads...")
    print(f"[*] Working proxies are being saved directly to '{OUTPUT_FILE}'\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS_CHECK) as executor:
        executor.map(check_and_save_proxy, list(unique_proxies))

    elapsed_time = time.time() - start_time

    print("\n" + "=" * 77)
    print(" PROCESS SUMMARY ".center(77, "="))
    print("=" * 77)
    print(f"[*] Total Unique Scraped       : {len(unique_proxies)}")
    print(f"[*] Total Verified Live (True) : {live_count}")
    print(f"[*] Total Operational Time     : {elapsed_time:.2f} seconds")
    print(f"[*] Output Saved To            : {OUTPUT_FILE}")
    print("=" * 77)
    print("[*] Thank you for using this Tools.")

if __name__ == "__main__":
    main()
