
# GoFile Uploader (Python Script)

import os
import requests
os.system("pip install colorama tqdm requests_toolbelt")
from tqdm.notebook import tqdm
from colorama import Fore, Style
from IPython.display import clear_output
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor

def upload_file(file_path, api_token, folder_id=""):
    response = requests.get("https://api.gofile.io/servers").json()
    server = response["data"]["servers"][0]["name"]
    upload_url = f"https://{server}.gofile.io/contents/uploadfile"
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    print(f"⚡ {Fore.GERRN} Uploading Prosesing:...{Style.RESET_ALL}")

    with open(file_path, "rb") as file, tqdm(total=file_size, unit="B", unit_scale=True, bar_format='{rate_fmt}{postfix} {l_bar}{bar} {n_fmt}/{total_fmt} : {remaining}', colour='green') as progress_bar:
        encoder = MultipartEncoder(fields={"file": (file_name, file), "folderId": folder_id})
        monitor = MultipartEncoderMonitor(encoder, lambda m: progress_bar.update(m.bytes_read - progress_bar.n))
        headers = {"Authorization": f"Bearer {api_token}", "Content-Type": monitor.content_type}
        response = requests.post(upload_url, headers=headers, data=monitor)
        clear_output()

    if response.ok:
        data = response.json().get("data", {})
        Print(f"✅ {Fore.GERRN} Uploading Completed...{Style.RESET_ALL}")
        print("\n╭───────────────────────────────────────────╮")
        print(f"│ {Fore.YELLOW}File:{Style.RESET_ALL} {data.get('name', 'Unknown')}")
        print(f"│ {Fore.YELLOW}Download page:{Style.RESET_ALL} {data.get('downloadPage', 'N/A')}")
        print("╰───────────────────────────────────────────╯")
    else:
        print("\nUpload failed!", response.text)
