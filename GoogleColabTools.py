
import os
import shutil
import subprocess

def install_rtorrent(name="rutorrent"):
    if name == "flood":
        # Install rTorrent with Flood WEB UI
        if not shutil.which('rtorrent'):
            os.system('apt-get install rtorrent screen mediainfo -y')
            os.system('wget "" -O "/root/.rtorrent.rc"')
            subprocess.Popen(['screen', '-d', '-m', '-fa', '-S', 'rtorrent', 'rtorrent'])

    elif name == "rutorrent":
        # Install rTorrent with ruTorrent WEB UI
        if not shutil.which('rtorrent'):
            os.system('apt-get update')
            os.system('apt-get install -y rtorrent mediainfo sox screen php php-fpm php-json php-curl php-xml apache2 libapache2-mod-php')
            os.system('pip install cloudscraper')
            os.system('wget "" -O "/root/.rtorrent.rc"')
            subprocess.Popen(['screen', '-d', '-m', '-fa', '-S', 'rtorrent', 'rtorrent'])

    
os.path.isfile("/content/v4.3.8.tar.gz") and os.remove("/content/v4.3.8.tar.gz")
os.path.isdir("/content/ruTorrent-4.3.8") and shutil.rmtree("/content/ruTorrent-4.3.8")
