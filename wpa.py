import requests
import os
import subprocess
import time

#url_list = ["http://www.google.com","http://www.microsoft.com"]
ping_list = ["8.8.8.8","1.1.1.1"]
timeout = 5

def change_connection():
    with open("witch_one.txt","r") as file:
        for line in file:
            if str(line) == "1\n":
                print("entree dans le if")
                file.close()
                #os.system("ip link set eno1 down")
                os.system("dhclient -r")
                time.sleep(5)
                os.system("ip link set eno1 down")
                time.sleep(5)
                os.system("ip link set enp3s0 up")
                time.sleep(5)
                os.system("dhclient")
                time.sleep(5)
                os.system("ip link set eno1 down")
                os.system("ip addr del 192.168.31.100/24 dev eno1")
                os.system("ip route add 0/0 via 192.168.1.254 dev enp3s0")
                os.remove("witch_one.txt")
                os.system("echo 2 > witch_one.txt")
                #os.remove("/etc/resolv.conf")
                #os.system("echo nameserver 8.8.8.8 > /etc/resolv.conf")
                exit()
            else:
                print("entree dans le else")
                file.close()
                os.system("dhclient -r")
                time.sleep(5)
                os.system("ip link set enp3s0 down")
                time.sleep(5)
                os.system("ip link set eno1 up")
                time.sleep(5)
                os.system("dhclient")
                time.sleep(5)
                os.system("ip link set enp3s0 down")
                os.system("ip addr del 192.168.1.16/24 dev enp3s0")
                os.remove("witch_one.txt")
                os.system("echo 1 > witch_one.txt")
                #os.remove("/etc/resolv.conf")
                #os.system("echo nameserver 8.8.8.8 > /etc/resolv.conf")
                exit()

def scan_ping(ping_list):
    for url in ping_list:
        output = subprocess.Popen(["ping", "-c", "3", url], stdout=subprocess.PIPE).communicate()[0]
        if "3 received" in output.decode("utf-8"):
            print("tu as internet")
            exit()
        else:
            change_connection()

scan_ping(ping_list)
#change_connection()
