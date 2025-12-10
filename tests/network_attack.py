import urllib.request
import urllib.error

try:
    urllib.request.urlopen("http://google.com", timeout=3)
    print("Network access success (FAILURE)")
except Exception as e:
    print(f"Network access blocked (SUCCESS): {e}")
