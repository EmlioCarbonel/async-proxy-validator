```python
import asyncio
import aiohttp
import time
import json

# ================= Configuration =================
INPUT_FILE = 'proxies.txt'
OUTPUT_FILE = 'valid_proxies.json'
TEST_URL = 'http://httpbin.org/ip'
TIMEOUT_SECONDS = 5
CONCURRENCY_LIMIT = 50
# ===============================================

async def test_proxy(proxy, session, semaphore):
    async with semaphore:
        start_time = time.time()
        try:
            async with session.get(TEST_URL, proxy=proxy, timeout=TIMEOUT_SECONDS) as response:
                if response.status == 200:
                    data = await response.json()
                    latency = round((time.time() - start_time) * 1000)
                    print(f"[✅ SUCCESS] {proxy} | Latency: {latency}ms | Returned IP: {data.get('origin')}")
                    return {"proxy": proxy, "latency_ms": latency}
        except Exception:
            print(f"[❌ FAILED] {proxy} | Timeout or Connection Refused")
            return None

async def main():
    with open(INPUT_FILE, 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]

    print(f"Loaded {len(proxies)} proxies for testing. Starting async validation...\n")
    
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
    timeout = aiohttp.ClientTimeout(total=TIMEOUT_SECONDS)
    
    valid_proxies = []
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [test_proxy(proxy, session, semaphore) for proxy in proxies]
        results = await asyncio.gather(*tasks)
        
        for res in results:
            if res:
                valid_proxies.append(res)
                
    # Sort by latency
    valid_proxies = sorted(valid_proxies, key=lambda x: x['latency_ms'])
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(valid_proxies, f, indent=4)
        
    print(f"\n🎉 Validation complete! {len(valid_proxies)} working proxies saved to {OUTPUT_FILE}.")

if __name__ == '__main__':
    # Ensure proxies.txt exists
    import os
    if not os.path.exists(INPUT_FILE):
        with open(INPUT_FILE, 'w') as f:
            f.write("http://127.0.0.1:8080\n") # Example
        print(f"Created example {INPUT_FILE}. Please add your proxies and run again.")
    else:
        # Run async loop
        asyncio.run(main())
