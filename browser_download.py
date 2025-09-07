import requests
import zipfile
import io
import os

url = "https://storage.googleapis.com/chrome-for-testing-public/140.0.7339.80/win64/chrome-win64.zip"
destino = "chrome-win64"

print("Downloading the browser for automate testing...")
response = requests.get(url, stream=True)
response.raise_for_status()

os.makedirs(destino, exist_ok=True)

print("Extracting the file...")
with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
    zip_ref.extractall(destino)

print(f"Extracted {os.path.abspath(destino)}")