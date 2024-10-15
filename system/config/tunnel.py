import os
import time
import json
import re
import shutil
import subprocess

def start_ngrok(tunnel_port, ngrock_authtoken):
    # Check if the Ngrok config exists
    if not os.path.exists('/root/.config/ngrok/ngrok.yml'):
        os.system('wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz')
        os.system('tar -xvzf ngrok-v3-stable-linux-amd64.tgz')
        os.system(f'./ngrok config add-authtoken "{ngrock_authtoken}"')
        os.remove('/content/ngrok')
        os.remove('/content/ngrok-v3-stable-linux-amd64.tgz')

    # Start Ngrok tunnel
    os.system(f'./ngrok http {tunnel_port} &')
    time.sleep(2)
    tunnel_url = os.popen('curl -s http://localhost:4040/api/tunnels').read()
    url_data = json.loads(tunnel_url)
    public_url = url_data['tunnels'][0]['public_url']
    
    return public_url

def start_cloudflared(tunnel_port):
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
        return 'No matching URL found'
        
        
# button_style.py

# Define your button style variables
bttxt = 'hsla(210, 50%, 85%, 1)'
btcolor = 'hsl(210, 80%, 42%)'
btshado = 'hsla(210, 40%, 52%, .4)'

# HTML button code
def get_button_html(tunnel_url):
    showUrL = tunnel_url
    showTxT = f"Access URL : {tunnel_url}"

    return f'''
    <style>
    @import url('https://fonts.googleapis.com/css?family=Source+Code+Pro:200,900');
    :root {{
        --text-color: {bttxt};
        --shadow-color: {btshado};
        --btn-color: {btcolor};
        --bg-color: #141218;
    }}
    * {{
        box-sizing: border-box;
    }}
    button {{
        position:relative;
        padding: 10px 20px;
        border: none;
        background: none;
        cursor: pointer;
        font-family: "Source Code Pro";
        font-weight: 900;
        font-size: 100%;
        color: var(--text-color);
        background-color: var(--btn-color);
        box-shadow: var(--shadow-color) 2px 2px 22px;
        border-radius: 4px;
        z-index: 0;
        overflow: hidden;
    }}
    button:focus {{
        outline-color: transparent;
        box-shadow: var(--btn-color) 2px 2px 22px;
    }}
    .right::after, button::after {{
        content: var(--content);
        display: block;
        position: absolute;
        white-space: nowrap;
        padding: 40px 40px;
        pointer-events:none;
    }}
    button::after{{
        font-weight: 200;
        top: -30px;
        left: -20px;
    }}
    .right, .left {{
        position: absolute;
        width: 100%;
        height: 100%;
        top: 0;
    }}
    .right {{
        left: 66%;
    }}
    .left {{
        right: 66%;
    }}
    .right::after {{
        top: -30px;
        left: calc(-66% - 20px);
        background-color: var(--bg-color);
        color:transparent;
        transition: transform .4s ease-out;
        transform: translate(0, -90%) rotate(0deg)
    }}
    button:hover .right::after {{
        transform: translate(0, -47%) rotate(0deg)
    }}
    button .right:hover::after {{
        transform: translate(0, -50%) rotate(-7deg)
    }}
    button .left:hover ~ .right::after {{
        transform: translate(0, -50%) rotate(7deg)
    }}
    /* bubbles */
    button::before {{
        content: '';
        pointer-events: none;
        opacity: .6;
        background: radial-gradient(circle at 20% 35%,  transparent 0,  transparent 2px, var(--text-color) 3px, var(--text-color) 4px, transparent 4px),
                    radial-gradient(circle at 75% 44%, transparent 0,  transparent 2px, var(--text-color) 3px, var(--text-color) 4px, transparent 4px),
                    radial-gradient(circle at 46% 52%, transparent 0, transparent 4px, var(--text-color) 5px, var(--text-color) 6px, transparent 6px);
        width: 100%;
        height: 300%;
        top: 0;
        left: 0;
        position: absolute;
        animation: bubbles 5s linear infinite both;
    }}
    @keyframes bubbles {{
        from {{ transform: translate(); }}
        to {{ transform: translate(0, -66.666%); }}
    }}
    </style>
    <center>
    <a href="{showUrL}" target="_blank">
        <div style="width: 700px; height: 80px; padding-top:15px">
            <button style='--content: "{showTxT}";'>
                <div class="left"></div>{showTxT}<div class="right"></div>
            </button>
        </div>
    </a>
    </center>
    '''
