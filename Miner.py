from libs.Requester import Requester
import importlib as importer
import libs.logo as logo
from colorama import *
from hashlib import *
from random import *
import string
import random
import os

def fancy_hashrate(value):
    units = ["H/s", "kH/s", "MH/s", "GH/s", "TH/s", "PH/s", "EH/s"]
    magnitude = 0
    while value >= 1000 and magnitude < len(units) - 1:
        value /= 1000.0
        magnitude += 1
    return f"{value:.2f} {units[magnitude]}"


def random_string(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

rqster = Requester(False)
base = os.path.dirname(__file__)
init()

miner_name = "UltraDUCO Miner"
version = "1.0"
os_name = os.name
use_miner = "default"

if os_name == "nt":
    os.system("title "+miner_name)
elif os_name == "posix":
    os.system('printf "\033]0;' + miner_name + '\007"')

logo.print_logo()

print(Fore.YELLOW + "[>] Welcome to UltraDUCO Miner ! An Unofficial Ultimate DUCO Miners for PC !" + Style.RESET_ALL)
username = None
mining_key = None
while True:
    username = input(Fore.BLUE + "[ᕲ] Username : " + Style.RESET_ALL)
    if username != None and username != "":
        break
    else:
        print(Fore.RED + "[ERROR] No valid Input" + Style.RESET_ALL)

mining_key = input(Fore.BLUE + "[⚷] Mining Key (If you have) : " + Style.RESET_ALL)
print()
if input(Fore.BLUE + "[⛯] Do you want to use the default miner or Choose one from the Add-ons Folder ? ([D]efault/[A]dd-on) : " + Style.RESET_ALL).lower() == "a":
    list_ = os.listdir(os.path.join(base,"Addons"))
    if len(list_) == 0:
        print(Fore.RED + "[ERROR] No Add-on Found, Switching to default miner." + Style.RESET_ALL)
    else:
        print(Fore.CYAN + "[i] Searching for Add-ons ..." + Style.RESET_ALL)
        validate_addon = []
        for addon in list_:
            if addon.endswith(".py"):
                try:
                    temp = importer.import_module(f"Addons.{addon[:-3]}")
                    diff = 500
                    r2 = random_string(10)
                    r1 = randint(100,410)
                    hashed = sha1(f"{str(r2)}{str(r1)}".encode("ascii")).hexdigest()
                    test = temp.Mine(hashed,r2,diff)

                    if test[0] == r1:
                        validate_addon.append([addon,test[1]])
                except Exception as e:
                    pass

        if len(validate_addon) == 0:
            print(Fore.RED + "[ERROR] No Valid Add-on Found, Switching to default miner." + Style.RESET_ALL)
        else:
            print()
            print(Fore.YELLOW + f"[>] {len(validate_addon)} Add-ons Found ! Choose one by entering the Index of the item : " + Style.RESET_ALL)
            i = 0
            for a in validate_addon:
                print(Fore.MAGENTA + f"[{i}]    " + a[0][:-3] + "    " + fancy_hashrate(a[1]) + Style.RESET_ALL)
                i = i + 1

            choose = None
            while True:
                choose = input(Fore.BLUE + f"[?] Choose [0-{i-1}] : " + Style.RESET_ALL)
                if choose != None and choose != "":
                    try:
                        choose = int(choose)
                        if int(choose)>=0 and int(choose)<=i-1:
                            use_miner = "custoM" + validate_addon[choose][0]
                            break
                        else:
                            print(Fore.RED + "[ERROR] No valid Input" + Style.RESET_ALL)
                    except Exception as e:
                        print(Fore.RED + "[ERROR] No valid Input" + Style.RESET_ALL)
                else:
                    
                    print(Fore.RED + "[ERROR] No valid Input" + Style.RESET_ALL)
            

print()
print(Fore.CYAN + "[i] Connecting to the Nearest Pool ..." + Style.RESET_ALL)

status = rqster.FastConnection()
if status:
    print(Fore.GREEN + "[√] Connected Successfully !" + Style.RESET_ALL)
else:
    print(Fore.RED + "[ERROR] Pool unreachable, Exiting. " + Style.RESET_ALL)
    exit()
print()
details_pool = rqster.GetPoolData()
print(f"""{Fore.CYAN}[i] Pool Details :
- Pool Name : {details_pool['name']}
- Pool Version : {details_pool['version']}
- Pool IP : {details_pool['ip']}
- Pool Port : {details_pool['port']}
- Pool Region : {details_pool['region']}""" + Style.RESET_ALL)
print()
print(Fore.CYAN + f"[i] Miner will be used : {'Default' if use_miner == 'default' else use_miner.replace('custoM','',1)[:-3]}" + Style.RESET_ALL)

dif = None
while True:
    dif = input(Fore.BLUE + "[⛯] Choose a difficulity of the JOBS ? ([LOW]/[MEDIUM]/[HIGH]) : " + Style.RESET_ALL)
    if dif == "LOW" or dif == "MEDIUM" or dif == "HIGH":
        break
    else:
        print(Fore.RED + "[ERROR] No valid Input" + Style.RESET_ALL)
        
print("\n")
print(Fore.YELLOW + f"[⛏] Starting the Miner ..." + Style.RESET_ALL)
miner = None
if use_miner == "default":
    miner = importer.import_module(f"libs.sha1")
else:
    miner = importer.import_module(f"Addons.{use_miner.replace('custoM','',1)[:-3]}")

while True:
    j = rqster.RequestJOB(username,mining_key,dif)
    r =  miner.Mine(j[1],j[0],j[2])
    name_ = " - " + use_miner.replace('custoM','',1)[:-3]
    r0 = rqster.ValidationJOBResults(r[0],r[1],f"{miner_name} V{version}{'' if use_miner == 'default' else name_ }")
    
    if r0 == "GOOD":
        print(Fore.GREEN + "[ᕲ][" + str(r[2]) + "] Share accepted " + str(r[0]) + "      " + fancy_hashrate(r[1]) + Style.RESET_ALL)
    elif r0 == "BAD":
        print(Fore.RED + "[ᕲ][" + str(r[2]) + "] Share rejected " + str(r[0]) + "      " + fancy_hashrate(r[1]) + Style.RESET_ALL)
    elif r0 == "INVU":
        print(Fore.RED + "[ERROR] Invalid credentials, Please retry again." + Style.RESET_ALL)
        while True:
            username = input(Fore.BLUE + "[ᕲ] Username : " + Style.RESET_ALL)
            if username != None and username != "":
                break
            else:
                print(Fore.RED + "[ERROR] No valid Input" + Style.RESET_ALL)


