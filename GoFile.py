
# GoFile Uploader (Python Script)

import os
import requests
os.system("pip install colorama tqdm requests_toolbelt")
from tqdm import tqdm
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
from colorama import Fore, Style

def upload_file(file_path, api_token, folder_id=""):
    response = requests.get("https://api.gofile.io/servers").json()
    server = response["data"]["servers"][0]["name"]
    upload_url = f"https://{server}.gofile.io/contents/uploadfile"
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)

    with open(file_path, "rb") as file, tqdm(total=file_size, unit="B", unit_scale=True, desc="Uploading progress") as progress_bar:
        encoder = MultipartEncoder(fields={"file": (file_name, file), "folderId": folder_id})
        monitor = MultipartEncoderMonitor(encoder, lambda m: progress_bar.update(m.bytes_read - progress_bar.n))
        headers = {"Authorization": f"Bearer {api_token}", "Content-Type": monitor.content_type}
        response = requests.post(upload_url, headers=headers, data=monitor)

    if response.ok:
        data = response.json().get("data", {})
        print("\n╭───────────────────────────────────────────╮")
        print(f"│ {Fore.YELLOW}File:{Style.RESET_ALL} {data.get('name', 'Unknown')}")
        print(f"│ {Fore.YELLOW}Download page:{Style.RESET_ALL} {data.get('downloadPage', 'N/A')} │")
        print("╰───────────────────────────────────────────╯")
    else:
        print("\nUpload failed!", response.text)
