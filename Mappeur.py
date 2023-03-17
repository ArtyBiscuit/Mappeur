try:
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
    #print(r.status_code)
    if r.status_code == 200:
        prCyan(url + r.status_code)
    elif r.status_code == 429:
        prYellow(url + r.status_code)


def get_word_file(default):
    wst = default
    while True:
        wst = str(input("Wordlist: "))
        if wst == "":
            print("\nWordlist not set.")
            while True:
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
    default_wordlst = "wordlst"
    url = str(input("URL: "))
    wst = get_word_file(default_wordlst)
    f = open(wst, "r")
    lines = f.readlines()
    f.close()
    for path in lines:
      #  print("Try : %s" % (url + path))
        get(url + path)

if __name__ == "__main__":
    main()
