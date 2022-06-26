from follow_bot import spotify
import threading
import os
from time import sleep
from colorama import Fore

lock = threading.Lock()
proxies = []
proxy_counter, counter = 0, 0
spotify_profile = str(input("Link to Profile or Playlist: "))
threads = int(input("\nThreads: "))


def load_proxies():
    if not os.path.exists("proxies.txt"):
        with open("proxies.txt", "x") as f:
            print("Created proxies.txt")
        os._exit(0)
    with open("proxies.txt", "r", encoding = "UTF-8") as f:
        for line in f.readlines():
            line = line.replace("\n", "")
            proxies.append(line)
        if not len(proxies):
            print("\nNo proxies in proxies.txt")
            os._exit(0)


print("\n[1] Proxies\n[2] Proxyless")
option = int(input("\n> "))
if option == 1:
    load_proxies()


def safe_print(arg):
    lock.acquire()
    print(arg)
    lock.release()


def thread_starter():
    global counter
    if option == 1:
        obj = spotify(spotify_profile, proxies[proxy_counter])
    else:
        obj = spotify(spotify_profile)
    result, error = obj.follow()
    if result is True:
        counter += 1
        safe_print(Fore.GREEN+"Success "+Fore.WHITE+"Followed {}".format(counter)+" times")
    else:
        safe_print(Fore.RED+f"Error: {Fore.WHITE+error}")


while True:
    if threading.active_count() <= threads:
        try:
            threading.Thread(target = thread_starter).start()
            proxy_counter += 1
        except:
            pass
        if len(proxies) <= proxy_counter:  #Loops through proxy file
            proxy_counter = 0
