import requests
import os
import subprocess
import time
import argparse

#url_list = ["http://www.google.com","http://www.microsoft.com"]
ping_list = ["8.8.8.8"]
timeout = 5
compteur = 0

def change_connection():
    with open("/home/witch_one.txt","r") as file:
        for line in file:
            if str(line) == "1\n":
                print("entree dans le if")
                file.close()
                #os.system("ip link set eno1 down")
                os.system("/usr/sbin/dhclient -r")
                time.sleep(5)
                os.system("ip link set eno1 down")
                time.sleep(5)
                os.system("ip link set enp3s0 up")
                time.sleep(5)
                os.system("/usr/sbin/dhclient")
                time.sleep(5)
                os.system("ip link set eno1 down")
                os.system("ip addr del 192.168.31.100/24 dev eno1")
                os.system("ip route add 0/0 via 192.168.1.254 dev enp3s0")
                os.remove("/home/witch_one.txt")
                os.system("echo 2 > /home/witch_one.txt")
                #os.remove("/etc/resolv.conf")
                #os.system("echo nameserver 8.8.8.8 > /etc/resolv.conf")
                exit()
            else:
                print("entree dans le else")
                file.close()
                os.system("/usr/sbin/dhclient -r")
                time.sleep(5)
                os.system("ip link set enp3s0 down")
                time.sleep(5)
                os.system("ip link set eno1 up")
                time.sleep(5)
                os.system("/usr/sbin/dhclient")
                time.sleep(5)
                os.system("ip link set enp3s0 down")
                os.system("ip addr del 192.168.1.16/24 dev enp3s0")
                os.remove("/home/witch_one.txt")
                os.system("echo 1 > /home/witch_one.txt")
                #os.remove("/etc/resolv.conf")
                #os.system("echo nameserver 8.8.8.8 > /etc/resolv.conf")
                exit()

def scan_ping(ping_list,compteur):
    compteur = compteur + 1
    for url in ping_list:
        output = subprocess.Popen(["ping", "-c", "1", url], stdout=subprocess.PIPE).communicate()[0]
        if "1 received" in output.decode("utf-8"):
            print("tu as internet")
            exit()
        else:
            print("pas internet essai numero ",compteur)
            if compteur == 3:
                print("changing connextion")
                change_connection()
            time.sleep(5) 
            scan_ping(ping_list,compteur)	
          #  change_connection()

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--change", help="changing interfaces", default=False, action="store_true")
args = parser.parse_args()
if args.change != False:
        change_connection()
        
with open("/home/witch_one.txt","r") as file:
    for line in file:
        if str(line) == "1\n":
            os.system("ip link set enp3s0 down")
            os.system("ip addr del 192.168.1.16/24 dev enp3s0")
        else:
            os.system("ip link set eno1 down")
            os.system("ip addr del 192.168.31.100/24 dev eno1")
            os.system("ip route add 0/0 via 192.168.1.254 dev enp3s0")
file.close()

scan_ping(ping_list,compteur)
#change_connection()
