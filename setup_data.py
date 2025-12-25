import os
import requests
import sys

# Correct raw URLs for NSL-KDD
urls = {
    "KDDTrain+.txt": "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain%2B.txt",
    "KDDTest+.txt": "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTest%2B.txt"
}

# Ensure we save in the absolute correct path
base_dir = os.path.dirname(os.path.abspath(__file__))
save_dir = os.path.join(base_dir, "data", "raw")
os.makedirs(save_dir, exist_ok=True)

print(f" Saving files to: {save_dir}")
print(" Downloading dataset... (This should take > 10 seconds)")

for filename, url in urls.items():
    print(f"\n   Attempting to download {filename}...")
    try:
        response = requests.get(url, stream=True)
        # Check if the URL actually exists (throws error if 404)
        response.raise_for_status()
        
        file_path = os.path.join(save_dir, filename)
        
        # Write file and show progress
        with open(file_path, "wb") as f:
            total_size = 0
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                total_size += len(chunk)
        
        # Check if file is empty
        if total_size < 1000:
            print(f"ERROR: {filename} is too small ({total_size} bytes). Download failed.")
        else:
            print(f"Success! {filename} downloaded ({total_size / 1024 / 1024:.2f} MB)")
            
    except Exception as e:
        print(f"CRITICAL ERROR: Could not download {filename}.")
        print(f"   Reason: {e}")

print("\n------------------------------------------------")
print("Check your folder now: sentinel-nids-ml/data/raw/")