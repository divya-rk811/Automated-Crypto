import requests
import time
import sys

class CryptoMonitor:
    def __init__(self, coin_id='bitcoin', currency='usd'):
        self.url = f"https://api.coingecko.com/api/v3/simple/price"
        self.params = {'ids': coin_id, 'vs_currencies': currency}
        self.coin_id = coin_id

    def fetch_price(self):
        try:
            response = requests.get(self.url, params=self.params)
            response.raise_for_status()
            data = response.json()
            return data[self.coin_id]['usd']
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def start_monitoring(self, threshold, interval=60):
        print(f"--- Monitoring {self.coin_id.upper()} (Alert at ${threshold}) ---")
        try:
            while True:
                price = self.fetch_price()
                if price:
                    status = "🚨 ALERT!" if price <= threshold else "✅ Stable"
                    print(f"[{time.strftime('%H:%M:%S')}] {price} USD | {status}")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user.")

if __name__ == "__main__":
    # Example: Alert me if Bitcoin drops below 60,000
    monitor = CryptoMonitor(coin_id='bitcoin')
    monitor.start_monitoring(threshold=60000)
