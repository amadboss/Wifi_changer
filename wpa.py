import requests
import os
import subprocess
import time

url_list = ["http://www.google.com","http://www.microsoft.com"]
ping_list = ["8.8.8.8","1.1.1.1"]
timeout = 5

def change_wifi():
    with open("witch_one.txt","r") as file:
        for line in file:
            if line == "1":
                file.close()
                os.system("systemctl stop wpa_supplicant")
                time.sleep(5)
                os.system("wpa_supplicant -B -D nl80211 -1 <L'INTERFACE> -c /etc/wpa-supplicant/wpa2.conf")
                time.sleep(5)
                os.remove("witch_one.txt")
                os.system("echo 2 > witch_one.txt")
            else:
                file.close()
                os.system("systemctl stop wpa_supplicant")
                time.sleep(5)
                os.system("wpa_supplicant -B -D nl80211 -1 <L'INTERFACE> -c /etc/wpa-supplicant/wpa1.conf")
                time.sleep(5)
                os.remove("witch_one.txt")
                os.system("echo 1 > witch_one.txt")

def scan_ping(ping_list):
    for url in ping_list:
      output = subprocess.Popen(
                ["ping", "-c", "3", url], stdout=subprocess.PIPE).communicate()[0]
            if "3 received" in output.decode("utf-8"):
                exit()
            else:
                change_wifi()

#scan_ping(ping_list)


for url in url_list:
    try:
        request = requests.get(url, timeout=timeout)
        #print("connected to",url)
        exit()
    except (requests.ConnectionError, requests.Timeout) as exception:
        scan_ping(ping_list)
        #print("No internet connection.")

