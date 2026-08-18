import requests
import concurrent.futures
import threading
import time
import sys

# ==========================================
# CONFIGURATION
# ==========================================
OUTPUT_FILE = "live.txt"
TEST_URL = "https://httpbin.org/ip"  # Fast API endpoint
TIMEOUT = 2  # Reduced timeout for faster checks
MAX_WORKERS_SCRAPE = 10  # Reduced workers for scraping
MAX_WORKERS_CHECK = 50  # Reduced workers for checking
TARGET_PROXIES = 300  # Target number of working proxies
PROXIES_PER_SOURCE = 50  # Limit proxies per source

# Best performing sources (reduced list)
URLS = [
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://api.openproxylist.xyz/http.txt",
    "https://proxyspace.pro/http.txt",
]

file_lock = threading.Lock()
live_count = 0
stop_testing = False

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
[*] ADVANCED PROXY SCRAPER & LIVE CHECKER - OPTIMIZED FOR PERFORMANCE

=============================================================================
    """
    print(banner)

def fetch_proxies_from_url(url):
    """Fetch proxies from a single URL with timeout."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=8)
        if response.status_code == 200:
            proxies = response.text.replace('\r', '').split('\n')
            # Limit results per source
            return proxies[:PROXIES_PER_SOURCE]
    except Exception as e:
        pass
    return []

def check_and_save_proxy(proxy):
    """Test proxy connectivity and save if working."""
    global live_count, stop_testing
    
    # Stop early if we've reached target
    if stop_testing or live_count >= TARGET_PROXIES:
        return
    
    proxy_dict = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }
    
    try:
        response = requests.get(
            TEST_URL, 
            proxies=proxy_dict, 
            timeout=TIMEOUT,
            allow_redirects=False
        )
        
        # Check if proxy is working (httpbin returns 200 with JSON)
        if response.status_code == 200:
            print(f"✓ [{live_count + 1}] {proxy}")
            with file_lock:
                if live_count < TARGET_PROXIES:
                    with open(OUTPUT_FILE, "a", encoding="utf-8") as file:
                        file.write(f"{proxy}\n")
                        file.flush()
                    live_count += 1
                    
                    # Stop if we've reached target
                    if live_count >= TARGET_PROXIES:
                        stop_testing = True
    except:
        pass

def main():
    global stop_testing
    
    if sys.platform.startswith('win'):
        import asyncio
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    print_banner()
    start_time = time.time()
    unique_proxies = set()
    
    # ============ PHASE 1: SCRAPING ============
    print("=" * 77)
    print(" PHASE 1: FETCHING PROXIES FROM SOURCES ".center(77, "="))
    print("=" * 77)
    print(f"[*] Fetching from {len(URLS)} active sources...")
    print(f"[*] Limit: {PROXIES_PER_SOURCE} proxies per source\n")
    
    scrape_start = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS_SCRAPE) as executor:
        results = executor.map(fetch_proxies_from_url, URLS)
        for result in results:
            for proxy in result:
                proxy = proxy.strip()
                # Validate proxy format
                if (":" in proxy and 
                    len(proxy) >= 7 and 
                    not proxy.startswith("#") and 
                    "<" not in proxy and
                    proxy.count(":") == 1):
                    unique_proxies.add(proxy)

    scrape_time = time.time() - scrape_start
    
    if not unique_proxies:
        print("[!] ERROR: No proxies extracted. Check network connection.")
        return

    print(f"[✓] Extracted {len(unique_proxies)} unique proxies in {scrape_time:.1f}s\n")
    
    # Clear output file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write("")

    # ============ PHASE 2: VERIFICATION ============
    print("=" * 77)
    print(" PHASE 2: LIVE VERIFICATION ".center(77, "="))
    print("=" * 77)
    print(f"[*] Testing proxies with {MAX_WORKERS_CHECK} parallel threads")
    print(f"[*] Target: {TARGET_PROXIES} working proxies")
    print(f"[*] Timeout: {TIMEOUT}s per proxy\n")

    test_start = time.time()
    
    # Test proxies in batches to avoid overwhelming
    proxy_list = list(unique_proxies)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS_CHECK) as executor:
        executor.map(check_and_save_proxy, proxy_list)

    test_time = time.time() - test_start
    total_time = time.time() - start_time

    # ============ SUMMARY ============
    print("\n" + "=" * 77)
    print(" PROCESS SUMMARY ".center(77, "="))
    print("=" * 77)
    print(f"[*] Total Candidates Extracted  : {len(unique_proxies)}")
    print(f"[*] Total Verified Live Proxies : {live_count}")
    print(f"[*] Scraping Time               : {scrape_time:.2f}s")
    print(f"[*] Testing Time                : {test_time:.2f}s")
    print(f"[*] Total Time                  : {total_time:.2f}s")
    print(f"[*] Output File                 : {OUTPUT_FILE}")
    print(f"[*] Success Rate                : {(live_count/len(unique_proxies)*100):.1f}%" if unique_proxies else "[*] Success Rate                : 0%")
    print("=" * 77)
    print("[✓] Proxy fetch completed successfully!")
    print("[*] Next update in 3 hours...")

if __name__ == "__main__":
    main()
