from pathlib import Path
from urllib.request import urlopen

URL = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat"
OUT = Path(__file__).resolve().parent / "airports.dat"

print("OpenFlights airports.dat downloader")
print("Source:", URL)
print("Target:", OUT)

try:
    with urlopen(URL, timeout=30) as response, OUT.open("wb") as target:
        target.write(response.read())
except Exception as exc:
    print("Download failed:", exc)
    print("Manual download: open https://openflights.org/data and download airports.dat")
    raise SystemExit(1)

print(f"Downloaded {OUT.stat().st_size:,} bytes to {OUT}")
