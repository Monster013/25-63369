import os
import math
import json
import base64
import requests
import shutil
from PIL import Image
from IPython.display import display, HTML, clear_output

def install_torrents_tools():
    if not shutil.which('mktorrent'):
        os.system('sudo apt-get install mktorrent mediainfo')
        os.system('sudo add-apt-repository ppa:ubuntuhandbook1/ffmpeg7')
        os.system('sudo apt-get install ffmpeg')
        os.system('pip install bencode.py')
        os.system("pip install ffmpeg-python")

#############
# MKTORRENT #
#############

def generate_output_file(file_or_directory):
    base_name = os.path.basename(file_or_directory.rstrip('/'))
    base_name_without_extension = os.path.splitext(base_name)[0]
    return f"{base_name_without_extension}.torrent"

# Calculate piece
def get_piece_size(path):
    """Returns the recommended -p value for a file or directory based on its total size."""
    if os.path.isfile(path):
        file_size = os.path.getsize(path)
    elif os.path.isdir(path):
        file_size = sum(os.path.getsize(os.path.join(dirpath, f)) for dirpath, _, files in os.walk(path) for f in files)
    else:
        raise ValueError("Invalid path: Must be a file or directory")

    if file_size < 350 * 2**20:   # < 350MiB
        return 18  # 256 KiB
    elif file_size < 512 * 2**20:  # 350MiB – 512MiB
        return 18  # 256 KiB
    elif file_size < 1 * 2**30:    # 512MiB – 1.0GiB
        return 19  # 512 KiB
    elif file_size < 2 * 2**30:    # 1.0GiB – 2.0GiB
        return 20  # 1 MiB
    elif file_size < 4 * 2**30:    # 2.0GiB – 4.0GiB
        return 21  # 2 MiB
    elif file_size < 8 * 2**30:    # 4.0GiB – 8.0GiB
        return 22  # 4 MiB
    elif file_size < 16 * 2**30:   # 8.0GiB – 16.0GiB
        return 23  # 8 MiB
    elif file_size < 32 * 2**30:   # 16.0GiB – 32.0GiB
        return 24  # 16 MiB
    elif file_size < 64 * 2**30:   # 32.0GiB – 64.0GiB
        return 25  # 32 MiB
    else:                          # 64.0GiB and up
        return 26  # 64 MiB

def edit_torrent(torrent_file, output_folder="Torrents/", flags=None):
    import bencode

    os.makedirs(output_folder, exist_ok=True)

    trackers = {
        "Bwtorrents": ("https://bwtorrents.tv/announce.php", "[BWT]_"),
        "HDtorrents": ("https://hdts-announce.ru/announce.php", "[HDT]_"),
        "OnlyEncodes": ("https://onlyencodes.cc/announce/25c4d087ead462cc1524152730249534", "[OE]_"),
        "ReelFlix": ("https://reelflix.xyz/announce/16e8052671bd10f90bfd97c19ffe8f68", "[RF]_"),
        "FearNoPeer": ("https://fearnopeer.com/announce/057e9e010fd881a81a3145179c15b6f3", "[FNP]_"),
        "Avistaz": ("https://tracker.avistaz.to/announce", "[AVZ]_"),
        "TorrentLeech": ("https://tracker.torrentleech.org/a/290c045dd374d7946f6fe12b82cb0590", "[TL]_"),
        "Upload.LX": ("https://upload.cx/announce/348dd8411ba6ede76c4fa29ce84f6e00", "[ULCX]_")
    }

    flags = flags or {k: True for k in trackers}  # Enable all if not provided

    with open(torrent_file, "rb") as f:
        torrent_data = {k.encode() if isinstance(k, str) else k: v for k, v in bencode.bdecode(f.read()).items()}

    base_filename = os.path.splitext(os.path.basename(torrent_file))[0]

    for tracker, (announce_url, prefix) in trackers.items():
        if flags.get(tracker, False):
            modified_torrent = torrent_data.copy()
            modified_torrent.update({b"announce": announce_url.encode(), b"created by": b"qBittorrent v5.0.3"})

            with open(os.path.join(output_folder, f"{prefix}{base_filename}.torrent"), "wb") as f:
                f.write(bencode.bencode(modified_torrent))

            print(f"Saved: {prefix}{base_filename}.torrent")



########################
# Screenshots & Upload #
########################


def generate_screenshots(video_path, num_screenshots, output_directory, quality=2):
    os.makedirs(output_directory, exist_ok=True)
   
    import ffmpeg
    
    # Probe video file to get duration
    image_urls = []
    probe = ffmpeg.probe(video_path)
    duration = float(probe['format']['duration'])
    adjusted_duration = math.floor(duration) - 500
    timestamps = [adjusted_duration / num_screenshots * i for i in range(1, num_screenshots + 1)]

    # Generate screenshots
    for i, timestamp in enumerate(timestamps, start=1):
        output_path = os.path.join(output_directory, f"screenshot_{i:02d}.png")
        result = os.system(f'ffmpeg -ss {timestamp} -i "{video_path}" -vframes 1 -q:v {quality} "{output_path}"')
        if result != 0:
            print(f"Error generating screenshot at {timestamp}.")
            continue

def upload_images(image_host="Imageride"):
    # API details
    API_KEYS = {
        "Freeimage": "6d207e02198a847aa98d0a2a901485a5",
        "Imgbb": "c516a4478af7178c2a972e33726debde",
        "Imageride": "chv_hPz_d469c413d03d3553409d2a7df490b9ac49d601069149d36619969c325dcda1069935a016a2ba54d050fedeec5f8800f0020d5c2c884f928edce2934f1ca7f5b4",
        "Lookmyimg": "chv_rqe_5b7662f6a29425eca2007889d08da9383cb9ec8e29fa856575dd8b71149ec01d993f78c7e8aa15c74857e7e2637c884029bcb9ec3593c214ef373f06db5415f6",
        "Onlyimg": "chv_8mI2_4a9a14480a0bd73524e87f7598cc7ce6e71202cd357a54a9720c23cd0eaba8cc53032bc547819bc65281d3fd2f833b55522af4c2dabd57c94043f44fdbee0a3c",
        "PTScreen": "pts_tDpg_43c54de7c9b2055d161ece8b3e109aa2018814815696749fc66c83d901e6f4973d2a27f80b0cfb0d03a6d2ca1646c5490a0958bd5dda1cc1600ecb8fc86b5d6c"
    }

    API_URLS = {
        "Freeimage": "https://freeimage.host/api/1/upload",
        "Imgbb": "https://api.imgbb.com/1/upload",
        "Imageride": "https://www.imageride.net/api/1/upload",
        "Lookmyimg": "https://lookmyimg.com/api/1/upload",
        "Onlyimg": "https://imgoe.download/api/1/upload",
        "PTScreen": "https://ptscreens.com/api/1/upload"
    }

    # Validate API choice
    if image_host not in API_URLS:
        print(f"Invalid API choice! Defaulting to Imageride.")
        image_host = "Imageride"

    api_url = API_URLS[image_host]
    api_key = API_KEYS[image_host]

    # Folder paths
    folder = "/content/screenshots"
    output_folder = "/content/screenshots/uploaddata"
    os.makedirs(output_folder, exist_ok=True)
    files = sorted(f for f in os.listdir(folder) if f.lower().endswith((".png", ".jpg")))

    upload_results = []
    bbc_full, bbc_medium, bbc_thumb = [], [], []

    for img in files:
        output_path = os.path.join(folder, img)
        with open(output_path, "rb") as file:
            img_base64 = base64.b64encode(file.read()).decode('utf-8')

        payload = {"key": api_key, "image": img_base64}
        response = requests.post(api_url, data=payload)

        img_response = response.json()  # Get JSON response
        upload_results.append({img: img_response})  # Store response with image name

        # Extract URLs from response
        url_full = img_response.get('data', {}).get('url', '')
        url_viewer = img_response.get('data', {}).get('url_viewer', '')
        url_medium = img_response.get('data', {}).get('medium', {}).get('url', '')
        url_thumb = img_response.get('data', {}).get('thumb', {}).get('url', '')

        # Generate BBCodes
        if url_full and url_viewer:
            bbc_full.append(f"[url={url_viewer}][img]{url_full}[/img][/url]")
        if url_medium and url_viewer:
            bbc_medium.append(f"[url={url_viewer}][img]{url_medium}[/img][/url]")
        if url_thumb and url_viewer:
            bbc_thumb.append(f"[url={url_viewer}][img]{url_thumb}[/img][/url]")

        print(f"{img} → {img_response}")  # Print full JSON response

    # Save all responses to a JSON file
    json_output_path = os.path.join(output_folder, "upload_responses.json")
    with open(json_output_path, "w") as json_file:
        json.dump(upload_results, json_file, indent=4)

    print(f"\nAll responses saved to {json_output_path}")

    # Save BBCode to text files
    with open(os.path.join(output_folder, "bbcode_full.txt"), 'w') as f_full, \
         open(os.path.join(output_folder, "bbcode_medium.txt"), 'w') as f_medium, \
         open(os.path.join(output_folder, "bbcode_thumb.txt"), 'w') as f_thumb:
        f_full.write("\n\n".join(bbc_full))
        f_medium.write("\n".join(bbc_medium))
        f_thumb.write("\n".join(bbc_thumb))

    print(f"BBCode files saved in {output_folder}")        
        
###########################
# Screenshot & Media INFO #
###########################

def generate_smbbcode(screenshot_links, media_info):
    # Read screenshot links BBCode
    with open(screenshot_links, 'r') as screenshot_links_file:
        screenshot_bbcode = screenshot_links_file.read()

    # Read and process media info
    with open(media_info, "r") as media_info_file:
        lines = media_info_file.readlines()

    # Copy file name from the second line and remove the first three lines
    file_name = lines[1].strip() if len(lines) > 1 else "Unknown File"
    del lines[:3]

    # Format media info content
    mediainfo = ''.join(lines)
    mediainfo = mediainfo.replace('★ General ★', '[quote]\n[b][color=green]★ General ★[/color][/b]\n[font=Courier New]')
    mediainfo = mediainfo.replace('★ Video Track ★', '[/font]\n\n[b][color=blue]★ Video Track ★[/color][/b]\n[font=Courier New]')
    mediainfo = mediainfo.replace('★ Audio Track ★', '[/font]\n\n[b][color=Orange]★ Audio Track ★[/color][/b]\n[font=Courier New]', 1)
    mediainfo = mediainfo.replace('★ Subtitle ★', '[/font]\n\n[b][color=Teal]★ Subtitle ★[/color][/b]\n[font=Courier New]')
    mediainfo += '[/font][/quote]'

    return file_name, screenshot_bbcode, mediainfo
    

def generate_output_txtfile(video_file):
    base_name = os.path.basename(video_file.rstrip('/'))
    base_name_without_extension = os.path.splitext(base_name)[0]
    return f"{base_name_without_extension}_Torrent_Description.V2.txt"
    
###########################
# Loading Animation Setup #
###########################

def loadingAN(name="loading"):
      if name == "loading":
          return display(HTML('<style>.lds-ring {   display: inline-block;   position: relative;   width: 34px;   height: 34px; } .lds-ring div {   box-sizing: border-box;   display: block;   position: absolute;   width: 34px;   height: 34px;   margin: 4px;   border: 5px solid #cef;   border-radius: 50%;   animation: lds-ring 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;   border-color: #cef transparent transparent transparent; } .lds-ring div:nth-child(1) {   animation-delay: -0.45s; } .lds-ring div:nth-child(2) {   animation-delay: -0.3s; } .lds-ring div:nth-child(3) {   animation-delay: -0.15s; } @keyframes lds-ring {   0% {     transform: rotate(0deg);   }   100% {     transform: rotate(360deg);   } }</style><div class="lds-ring"><div></div><div></div><div></div><div></div></div>'))
      elif name == "loadingv2":
          return display(HTML('''<style>.lds-hourglass {  display: inline-block;  position: relative;  width: 34px;  height: 34px;}.lds-hourglass:after {  content: " ";  display: block;  border-radius: 50%;  width: 34px;  height: 34px;  margin: 0px;  box-sizing: border-box;  border: 20px solid #dfc;  border-color: #dfc transparent #dfc transparent;  animation: lds-hourglass 1.2s infinite;}@keyframes lds-hourglass {  0% {    transform: rotate(0);    animation-timing-function: cubic-bezier(0.55, 0.055, 0.675, 0.19);  }  50% {    transform: rotate(900deg);    animation-timing-function: cubic-bezier(0.215, 0.61, 0.355, 1);  }  100% {    transform: rotate(1800deg);  }}</style><div class="lds-hourglass"></div>'''))

def textAN(TEXT, ty='text'):
      if ty == 'text':
            return display(HTML('''<style>@import url(https://fonts.googleapis.com/css?family=Raleway:400,700,900,400italic,700italic,900italic);#wrapper {   font: 17px 'Raleway', sans-serif;animation: text-shadow 1.5s ease-in-out infinite;    margin-left: auto;    margin-right: auto;    }#container {    display: flex;    flex-direction: column;    float: left;     }@keyframes text-shadow { 0% 20% {          transform: translateY(-0.1em);        text-shadow:             0 0.1em 0 #0c2ffb,             0 0.1em 0 #2cfcfd,             0 -0.1em 0 #fb203b,             0 -0.1em 0 #fefc4b;    }    40% {          transform: translateY(0.1em);        text-shadow:             0 -0.1em 0 #0c2ffb,             0 -0.1em 0 #2cfcfd,             0 0.1em 0 #fb203b,             0 0.1em 0 #fefc4b;    }       60% {        transform: translateY(-0.1em);        text-shadow:             0 0.1em 0 #0c2ffb,             0 0.1em 0 #2cfcfd,             0 -0.1em 0 #fb203b,             0 -0.1em 0 #fefc4b;    }   }@media (prefers-reduced-motion: reduce) {    * {      animation: none !important;      transition: none !important;    }}</style><div id="wrapper"><div id="container">'''+TEXT+'''</div></div>'''))
      elif ty == 'textv2':
            textcover = str(len(TEXT)*0.55)
            return display(HTML('''<style>@import url(https://fonts.googleapis.com/css?family=Anonymous+Pro);.line-1{font-family: 'Anonymous Pro', monospace;    position: relative;   border-right: 1px solid;    font-size: 15px;   white-space: nowrap;    overflow: hidden;    }.anim-typewriter{  animation: typewriter 0.4s steps(44) 0.2s 1 normal both,             blinkTextCursor 600ms steps(44) infinite normal;}@keyframes typewriter{  from{width: 0;}  to{width: '''+textcover+'''em;}}@keyframes blinkTextCursor{  from{border-right:2px;}  to{border-right-color: transparent;}}</style><div class="line-1 anim-typewriter">'''+TEXT+'''</div>'''))
                      

##########
#THE END #
##########
