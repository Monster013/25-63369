import os
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

#############
# MKTORRENT #
#############

def generate_output_file(file_or_directory):
    base_name = os.path.basename(file_or_directory.rstrip('/'))
    base_name_without_extension = os.path.splitext(base_name)[0]
    return f"{base_name_without_extension}.torrent"

# Calculate piece
def calculate_piece_size(file_or_directory):
    file_size = os.path.getsize(file_or_directory)

    if file_size < 350 * 2**20:  # less than 350MiB
        return 18  # 256 KiB
    elif file_size < 512 * 2**20:  # 350MiB to 512MiB
        return 18  # 256 KiB
    elif file_size < 1 * 2**30:  # 512MiB to 1.0GiB
        return 19  # 512 KiB
    elif file_size < 2 * 2**30:  # 1.0GiB to 2.0GiB
        return 20  # 1 MiB
    elif file_size < 4 * 2**30:  # 2.0GiB to 4.0GiB
        return 21  # 2 MiB
    elif file_size < 8 * 2**30:  # 4.0GiB to 8.0GiB
        return 22  # 4 MiB
    elif file_size < 16 * 2**30:  # 8.0GiB to 16.0GiB
        return 23  # 8 MiB
    elif file_size < 50 * 2**30:  # 16.0GiB to 50.0GiB
        return 24  # 16 MiB
    else:  # 50.0GiB and up
        return 25  # 32 MiB

def get_piece_size(file_or_directory, custom_piece_size):
    if custom_piece_size == 0:
        return calculate_piece_size(file_or_directory)
    else:
        return custom_piece_size

########################
# Screenshots & Upload #
########################


def generate_screenshots_and_upload(video_path, start_time, interval_minutes, num_screenshots, output_directory, api_key, quality=1):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    image_urls = []
    interval_seconds = interval_minutes * 60

    for i in range(num_screenshots):
        timestamp = start_time + i * interval_seconds
        hours, remainder = divmod(timestamp, 3600)
        minutes, seconds = divmod(remainder, 60)
        timestamp_str = f"{hours:02}:{minutes:02}:{seconds:02}"  # Format as HH:MM:SS
        output_path = os.path.join(output_directory, f"screenshot_{i+1}.png")

        command = (
            f'ffmpeg -ss {timestamp_str} -i "{video_path}" '
            f'-vframes 1 -q:v {quality} "{output_path}"'
        )
        result = os.system(command)

        if result != 0:
            print(f"Error generating screenshot at {timestamp_str}.")
            continue

        try:
            with open(output_path, "rb") as file:
                img_base64 = base64.b64encode(file.read()).decode('utf-8')

            payload = {"key": api_key, "image": img_base64}
            response = requests.post("https://api.imgbb.com/1/upload", data=payload)

            if response.status_code == 200:
                image_url = response.json()["data"]["url"]
                image_urls.append(image_url)
            else:
                print(f"Error uploading image: {response.json()['error']['message']}")
        except Exception as e:
            print(f"Error uploading screenshot_{i+1}.png: {e}")

    return image_urls

def generate_bbcode(image_urls, screenshot_links):
    bbcode_list = [f"[img]{url}[/img]" for url in image_urls]

    with open(screenshot_links, "w") as file:
        file.write("\n\n".join(bbcode_list))

def display_first_screenshot(output_directory):
    first_screenshot_path = os.path.join(output_directory, "screenshot_1.png")
    if os.path.exists(first_screenshot_path):
        Image.open(first_screenshot_path).show()
        
        
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
    mediainfo = mediainfo.replace('General', '[quote]\n[b][color=green]General[/color][/b]\n[font=Courier New]')
    mediainfo = mediainfo.replace('Video Track', '[/font]\n\n[b][color=blue]Video Track[/color][/b]\n[font=Courier New]')
    mediainfo = mediainfo.replace('Audio Tracks#', '[/font]\n\n[b][color=Orange]Audio Tracks[/color][/b][font=Courier New]', 1)
    mediainfo = mediainfo.replace('Subtitles#', '[/font]\n\n[b][color=Teal]Subtitles[/color][/b]\n[font=Courier New]')
    filtered_lines = [line for line in mediainfo.splitlines() if not line.startswith("Audio Tracks#")]
    filtered_lines = [line for line in mediainfo.splitlines() if not line.startswith("Subtitles#")]
    mediainfo = '\n'.join(filtered_lines)
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
