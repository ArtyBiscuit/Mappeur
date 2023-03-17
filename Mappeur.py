try:
    import time
    import requests
except ImportError as err:
    print(err)

def prCyan(skk):
    print("\033[96m {}\033[00m" .format(skk))
def prYellow(skk):
    print("\033[93m {}\033[00m" .format(skk))

def heder():
    prCyan(" __  __                              _ ")
    prCyan("|  \/  |__ _ _ __ _ __  ___ _  _ _ _| |")
    prCyan("| |\/| / _` | '_ \ '_ \/ -_) || | '_|_|")
    prCyan("|_|  |_\__,_| .__/ .__/\___|\_,_|_| (_)")
    prCyan("            |_|  |_|                   ")

def get(url):
    r = requests.get(url)
    if r.status_code == 200:
        print ("\033[A                                                                                    \033[A")
        prCyan('(' + str(r.status_code) + ')' + ' ' + url)
    elif r.status_code == 429:
        print ("\033[A                                                                                    \033[A")
        prYellow('(' + str(r.status_code) + ')' + ' ' + url)
    elif r.status_code == 404:
        print ("\033[A                                                                                    \033[A")
        print("Try:", url, end="")


def get_word_file(default):
    wst = default
    while True:
        wst = str(input("Wordlist: "))
        print()
        if wst == "":
            print("Wordlist not set.")
            time.sleep(2)
            while True:
                print ("\033[A                                                                                    \033[A")
                rep = input("Use default ?. (y/n): ")
                if rep == 'y':
                    wst = default
                    break
                elif rep == 'n':
                    break
        if wst != "":
          break
    return wst

def main():
    heder()
    default_wordlst = "Wordlist/wordlst"
    url = str(input("URL: "))
    timeToSleep = float(input("TTS (default 2s): "))
    wst = get_word_file(default_wordlst)
    f = open(wst, "r")
    lines = f.readlines()
    f.close()
    for path in lines:
        time.sleep(timeToSleep)
        get(url + path)

if __name__ == "__main__":
    main()
