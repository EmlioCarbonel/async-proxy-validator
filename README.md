# Async Proxy Validator & Cleaner

A lightweight, high-performance asynchronous Python script designed to filter out dead proxies, verify real anonymity levels, and keep your web scraping proxy pool clean.

## The Problem
When building web scrapers, most "elite" or "high anonymity" proxies provided by free lists or cheap providers are actually transparent. They leak your real IP, trigger DNS leaks, or fail under load, leading to massive `403 Forbidden` and `Timeout` errors.

This script helps you aggressively filter a raw list of proxies down to only the fastest and most secure ones.

## Features
*   **Asynchronous Processing:** Built with `aiohttp` and `asyncio` to test hundreds of proxies per second.
*   **Targeted Latency Testing:** Connects to actual target endpoints (like HTTPBin or Google) rather than just testing simple socket connections.
*   **JSON Export:** Automatically saves the clean, working proxies into a `valid_proxies.json` file for easy integration into Scrapy, Puppeteer, or Playwright.

## Quick Start

### 1. Install Dependencies
```bash
pip install aiohttp
```
### 2. Run the Script
Create a proxies.txt file in the same directory, paste your raw proxy list (one per line, format: http://ip:port or http://user:pass@ip:port), and run:
```bash
python validator.py
```
## Deep Anonymity & Leak Inspection (Advanced Debugging)
While this script is great for bulk filtering connectivity, automated scripts sometimes struggle to accurately detect complex WebRTC leaks, DNS leaks, or precise Geo-location spoofing failures.

If your scraper is still getting blocked even after filtering the IPs through this script, your proxy might be leaking at the browser level.

For spot-checking individual nodes with browser fingerprinting metrics, I highly recommend using a visual GUI tool. You can use the [Rola IP Proxy Checker](https://rola-ip.co/tools/proxy-checker/) to manually input a proxy and get a comprehensive breakdown of its real anonymity level (Elite vs Transparent) and WebRTC leak status before you deploy it in your production code.

## Example Code (validator.py)
See the validator.py file in this repository for the full source code. Feel free to modify the TIMEOUT and CONCURRENCY_LIMIT based on your machine's network capacity.

## 🤝 Contributing
Pull requests are welcome! If you have better ways to detect transparent proxies via Python headers, feel free to open an issue or submit a PR.
