
##########################
# GoFile (Python Script) #
##########################

import os
import sys
import shutil
import requests
from requests import post, get
os.system("pip install colorama tqdm requests_toolbelt")
from tqdm.notebook import tqdm
from colorama import Fore, Style
from IPython.display import clear_output
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor

###################
# GoFile Uploader #
###################

def upload_file(file_path, api_token, folder_id=""):
    response = requests.get("https://api.gofile.io/servers").json()
    server = response["data"]["servers"][0]["name"]
    upload_url = f"https://{server}.gofile.io/contents/uploadfile"
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    print(f"⚡ {Fore.GREEN} Uploading Prosesing:...{Style.RESET_ALL}\n")

    with open(file_path, "rb") as file, tqdm(total=file_size, unit="B", unit_scale=True, bar_format='{rate_fmt}{postfix} {l_bar}{bar} {n_fmt}/{total_fmt} : {remaining}', colour='green') as progress_bar:
        encoder = MultipartEncoder(fields={"file": (file_name, file), "folderId": folder_id})
        monitor = MultipartEncoderMonitor(encoder, lambda m: progress_bar.update(m.bytes_read - progress_bar.n))
        headers = {"Authorization": f"Bearer {api_token}", "Content-Type": monitor.content_type}
        response = requests.post(upload_url, headers=headers, data=monitor)
        clear_output()

    if response.ok:
        data = response.json().get("data", {})
        print(f"✅ {Fore.GREEN} Uploading Completed...{Style.RESET_ALL}")
        print("\n╭───────────────────────────────────────────╮")
        print(f"│ {Fore.YELLOW}File:{Style.RESET_ALL} {data.get('name', 'Unknown')}")
        print(f"│ {Fore.YELLOW}Download page:{Style.RESET_ALL} {data.get('downloadPage', 'N/A')}")
        print("╰───────────────────────────────────────────╯")
    else:
        print("\nUpload failed!", response.text)
 
if __name__ == "__main__":
    file_path = input("Enter the file path: ").strip()
    api_token = "LO9CGYusEwxJvle1Hz4tfrOHgGcnTfIu"  # Replace with your API token
    folder_id = ""  # Optional: Set folder ID
    
    if os.path.exists(file_path):
        upload_file(file_path, api_token, folder_id)
    else:
        print("Error: File not found!")
