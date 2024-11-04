
import os
import re
import time
import json
import shutil
import subprocess
import urllib.request
from IPython.display import HTML


####################
# Rtorrent Setup's #
####################

def install_rtorrent(name="flood"):
    if name == "flood":
        # Installing Rtorrent with Flood WEB UI
        if not shutil.which('rtorrent'):
            os.system('apt-get install rtorrent screen mediainfo -y')
            os.system('wget "" -O "/root/.rtorrent.rc"')
            subprocess.Popen(['screen', '-d', '-m', '-fa', '-S', 'rtorrent', 'rtorrent'])

    elif name == "rutorrent":
        # Installing Rtorrent with ruTorrent WEB UI
        if not shutil.which('rtorrent'):
            os.system('apt-get update')
            os.system('apt-get install -y rtorrent mediainfo sox screen php php-fpm php-json php-curl php-xml apache2 libapache2-mod-php')
            os.system('pip install cloudscraper')
            os.system('wget "https://github.com/Monster013/25-63369/raw/refs/heads/main/rtorrent.rc" -O "/root/.rtorrent.rc"')
            subprocess.Popen(['screen', '-d', '-m', '-fa', '-S', 'rtorrent', 'rtorrent'])

def install_rtorrent_unstable():
    
    # Installing Rtorrent Unstable 
    os.system("apt-get update")
    os.system("apt-get install -y build-essential pkg-config libncurses5-dev libcurl4-openssl-dev libxml2-dev")
    
    libtorrent_url = "https://github.com/rakshasa/rtorrent-archive/raw/master/libtorrent-0.14.0.tar.gz"
    urllib.request.urlretrieve(libtorrent_url, "libtorrent-0.14.0.tar.gz")
    os.system("tar -xzvf libtorrent-0.14.0.tar.gz")
    os.chdir("libtorrent-0.14.0")
    os.system("./autogen.sh && ./configure && make && make install")
    os.chdir("..")
    
    rtorrent_url = "https://github.com/rakshasa/rtorrent-archive/raw/master/rtorrent-0.10.0.tar.gz"
    urllib.request.urlretrieve(rtorrent_url, "rtorrent-0.10.0.tar.gz")
    os.system("")
    os.chdir("rtorrent-0.10.0")
    os.system("./autogen.sh && ./configure && make && make install")
    os.chdir("..")
    os.system("ldconfig")
    

################
# Ngrok  Setup #
################

def start_ngrok_http(tunnel_port, ngrok_authtoken):
    # Check if ngrok is installed
    if not shutil.which('ngrok'):
        os.system('wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz -P /content')
        os.system('tar -xvzf /content/ngrok-v3-stable-linux-amd64.tgz -C /content')
        os.system('mv /content/ngrok /usr/local/bin/')
        os.remove('/content/ngrok-v3-stable-linux-amd64.tgz')
        
    # Set ngrok authtoken
    os.system(f'ngrok config add-authtoken "{ngrok_authtoken}"')

    # Start ngrok tunnel
    os.system(f'ngrok http {tunnel_port} &')
    time.sleep(2)
    
    # Get the public URL
    tunnel_url = os.popen('curl -s http://localhost:4040/api/tunnels').read()
    url_data = json.loads(tunnel_url)
    public_url = url_data['tunnels'][0]['public_url']
    
    return public_url

def start_ngrok_tcp(tunnel_port, ngrok_authtoken):
    # Check if ngrok is installed
    if not shutil.which('ngrok'):
        os.system('wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz -P /content')
        os.system('tar -xvzf /content/ngrok-v3-stable-linux-amd64.tgz -C /content')
        os.system('mv /content/ngrok /usr/local/bin/')
        os.remove('/content/ngrok-v3-stable-linux-amd64.tgz')
        
    # Set ngrok authtoken
    os.system(f'ngrok config add-authtoken "{ngrok_authtoken}"')

    # Start ngrok tunnel
    os.system(f'ngrok tcp {tunnel_port} &')
    time.sleep(2)
    
    # Get the public URL
    tunnel_url = os.popen('curl -s http://localhost:4040/api/tunnels').read()
    url_data = json.loads(tunnel_url)
    public_url = url_data['tunnels'][0]['public_url']
    
    return public_url

#####################
# Argotunnal  Setup #
#####################

def start_cloudflared_http(tunnel_port):
    if not shutil.which('cloudflared'):
        os.system('curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb -o cloudflared.deb')
        os.system('sudo dpkg -i cloudflared.deb')
        os.remove('/content/cloudflared.deb')

    # Start the cloudflared tunnel
    subprocess.Popen(['cloudflared', 'tunnel', '--url', f'http://localhost:{tunnel_port}', '--logfile', f'/root/cloudflared.{tunnel_port}.log'])
    time.sleep(5)

    # Now find the cloudflared URL
    log_file_path = f'/root/cloudflared.{tunnel_port}.log'
    with open(log_file_path, 'r') as file:
        log_content = file.read()
        
    pattern = r'https://(.*?\.trycloudflare\.com)'
    urls = re.findall(pattern, log_content)

    if urls:
        return f'https://{urls[-1]}'
    else:
        return ' Something is worng, Please run again...'


def start_cloudflared_tcp(tunnel_port):
    if not shutil.which('cloudflared'):
        os.system('curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb -o cloudflared.deb')
        os.system('sudo dpkg -i cloudflared.deb')
        os.remove('/content/cloudflared.deb')

    # Start the cloudflared tunnel
    subprocess.Popen(['cloudflared', 'tunnel', '--url', f'tcp://localhost:{tunnel_port}', '--logfile', f'/root/cloudflared.{tunnel_port}.log'])
    time.sleep(5)

    # Now find the cloudflared URL
    log_file_path = f'/root/cloudflared.{tunnel_port}.log'
    with open(log_file_path, 'r') as file:
        log_content = file.read()
        
    pattern = r'https://(.*?\.trycloudflare\.com)'
    urls = re.findall(pattern, log_content)

    if urls:
        return f'tcp://{urls[-1]}'
    else:
        return ' Something is worng, Please run again...'
                
########################
# Button  Style  Setup #
########################

# Define your button style variables
bttxt = 'hsla(210, 50%, 85%, 1)'
btcolor = 'hsl(210, 80%, 42%)'
btshado = 'hsla(210, 40%, 52%, .4)'

# HTML button code
def get_button_html(tunnel_url):
    showUrL = tunnel_url
    showTxT = f"Access URL : {tunnel_url}"

    return f'''<style>@import url('https://fonts.googleapis.com/css?family=Source+Code+Pro:200,900');:root{{--text-color:{bttxt};--shadow-color:{btshado};--btn-color:{btcolor};--bg-color:#141218;}}*{{box-sizing:border-box;}}button{{position:relative;padding:10px 20px;border:none;background:none;cursor:pointer;font-family:"Source Code Pro";font-weight:900;font-size:100%;color:var(--text-color);background-color:var(--btn-color);box-shadow:var(--shadow-color) 2px 2px 22px;border-radius:4px;z-index:0;overflow:hidden;}}button:focus{{outline-color:transparent;box-shadow:var(--btn-color) 2px 2px 22px;}}.right::after,button::after{{content:var(--content);display:block;position:absolute;white-space:nowrap;padding:40px 40px;pointer-events:none;}}button::after{{font-weight:200;top:-30px;left:-20px;}}.right,.left{{position:absolute;width:100%;height:100%;top:0;}}.right{{left:66%;}}.left{{right:66%;}}.right::after{{top:-30px;left:calc(-66%-20px);background-color:var(--bg-color);color:transparent;transition:transform .4s ease-out;transform:translate(0,-90%)rotate(0deg);}}button:hover .right::after{{transform:translate(0,-47%)rotate(0deg);}}button .right:hover::after{{transform:translate(0,-50%)rotate(-7deg);}}button .left:hover~.right::after{{transform:translate(0,-50%)rotate(7deg);}}button::before{{content:'';pointer-events:none;opacity:.6;background:radial-gradient(circle at 20% 35%,transparent 0,transparent 2px,var(--text-color) 3px,var(--text-color) 4px,transparent 4px),radial-gradient(circle at 75% 44%,transparent 0,transparent 2px,var(--text-color) 3px,var(--text-color) 4px,transparent 4px),radial-gradient(circle at 46% 52%,transparent 0,transparent 4px,var(--text-color) 5px,var(--text-color) 6px,transparent 6px);width:100%;height:300%;top:0;left:0;position:absolute;animation:bubbles 5s linear infinite both;}}@keyframes bubbles{{from{{transform:translate();}}to{{transform:translate(0,-66.666%);}}}}</style><center><a href="{showUrL}" target="_blank"><div style="width:700px;height:80px;padding-top:15px"><button style='--content:"{showTxT}";'><div class="left"></div>{showTxT}<div class="right"></div></button></div></a></center>'''

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
          
