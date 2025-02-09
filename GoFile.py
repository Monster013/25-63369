
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

#####################
# GoFile Downloader #
#####################

def gofile_downloader(gofile_url, downloader):
    
    if not shutil.which("aria2c"):
        os.system("apt-get install -y aria2")

    content_id = gofile_url.split("/")[-1]
    user_agent = os.getenv("GF_USERAGENT", "Mozilla/5.0")
    headers = {
        "User-Agent": user_agent,
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "*/*",
        "Connection": "keep-alive",
    }

    # Step 1: Check for existing token
    token = os.getenv("GOFILE_TOKEN")

    if not token:
        print("Creating a new account...")

        create_account_response = post("https://api.gofile.io/accounts", headers=headers).json()

        if create_account_response.get("status") != "ok":
            print("Account creation failed!", file=sys.stderr)
            sys.exit(1)

        token = create_account_response["data"]["token"]
        print(f"New Access Token: {token}\n")

    else:
        print(f"Using existing token: {token}\n")

    # Step 2: Fetch Content Info
    url = f"https://api.gofile.io/contents/{content_id}?wt=4fd6sg89d7s6&cache=true&sortField=createTime&sortDirection=1"
    headers["Authorization"] = f"Bearer {token}"

    response = get(url, headers=headers)
    
    try:
        response_json = response.json()
        if response_json.get("status") != "ok":
            print(f"Failed to get a link from {url}\n")
            return

        data = response_json["data"]

        download_links = []

        # Folder Links
        if data["type"] == "folder" and "children" in data:
            for child_id, child in data["children"].items():
                filename = child["name"]
                file_link = child["link"]
                print(f"File Name: {filename}")
                print(f"Direct URL: {file_link}\n")
                download_links.append(file_link)
        else:
            filename = data["name"]
            file_link = data["link"]
            print(f"File Name: {filename}")
            print(f"Direct URL: {file_link}")
            download_links.append(file_link)
        
        return download_links
    
    except Exception as e:
        print(f"Error parsing API response: {e}")
        print(f"Raw Response: {response.text}")
        
