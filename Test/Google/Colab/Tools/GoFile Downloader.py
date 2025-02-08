
# GoFile Downloader__

import os
import sys
import shutil
from requests import post, get

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

        # Step 3: Download Files 
        if download_links:
            print("Starting downloads using {downloader}...\n")
            for file_link in download_links:
                if downloader == "Aria2c":
                    !aria2c -c -x 16 --header='cookie: accountToken={token}' '{file_link}'
                elif downloader == "WGet":
                    !wget -c --header="cookie: accountToken={token}" "{file_link}"
                elif downloader == "Curl":
                    !curl -C - -H "cookie: accountToken={token}" -O "{file_link}"
                
    except Exception as e:
        print(f"Error parsing API response: {e}")
        print(f"Raw Response: {response.text}")
