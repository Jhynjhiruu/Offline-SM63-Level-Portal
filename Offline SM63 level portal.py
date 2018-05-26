from urllib.parse import urlencode, unquote
from urllib.request import Request, urlopen
import win32clipboard
import os
import sys
import json
print("Offline SM63 level portal v1.1.0 by Jynji")
def copyToClipboard(data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(data)
    win32clipboard.CloseClipboard()   
def getURL(length, url):
    post_fields = {"length": str(length)}
    request = Request(url, urlencode(post_fields).encode())
    return str(urlopen(request).read())[8:-16]     
while True:
    try:
        mode
    except:
        mode = str(input("This program contains a level ID finder.\nLevel IDs are used to uniquely identify forum levels.\nWould you like to open the level ID finder? (Y/N)\n")).upper()
    if mode == "Y":
        try:
            if not os.path.exists("levels.csv") or open("levels.csv").readline().rstrip("\n") != getURL("1", "http://runouw.com/levels/leveldesigner/listlevels.php"):
                with open("levels.csv", "w") as g:
                    g.write("0\n".join(getURL(2**64, "http://runouw.com/levels/leveldesigner/listlevels.php").split("0|")))
        except:
            print("runouw.com is *probably, not definitely* down. This means you will only be able to browse levels available the last time the site was up.")
            if not os.path.exists("levels.csv"):
                input("No level database backup found! Press enter to exit the program...")
                sys.exit
        h = open("levels.csv").read()
        levels = []
        [levels.append(i.split(",")) for i in h.split("\n")]
        print(len(levels), "levels loaded")
        searchData = input("What keyword would you like to search for?\n")
        searchResults = []
        for i in levels:
            for j in i:
                if searchData.upper() in j.upper():
                    searchResults.append(i)
                    break
        if searchResults:
            print(len(searchResults), "results found for", searchData + ":")
            [print("{0}: {1} by {2}".format(*i)) for i in searchResults]
            mode = "N"
        else:
            print("No results found for " + searchData + "!")
            continue
    if mode == "N":
        del mode
        while True:
            levelID = str(input("Please enter the level ID you would like to view,\nor type 'end' to return to the mode selection screen:\n"))
            url = "http://runouw.com/levels/leveldesigner/getstats.php"
            try:
                codes
            except:
                print("Loading levels from file... (this may take some time)")
                f = open("levels.csv").read()
                levels = []
                [levels.append(i.split(",")) for i in f.split("\n")]
                try:
                    codes = json.load(open("codes.json"))
                except:
                    print("No level codes backup found! Making a backup will take a long time, depending on your internet speed, so stop the program at any point - download progress will be saved.")
                    json.dump({}, open("codes.json", "w"))
                    codes = json.load(open("codes.json"))
                for i in levels:
                    j = i[0]
                    try:
                        codes[j]
                    except KeyError:
                        codes[j] = ""
                    if codes[j] == "":
                        try:
                            post_fields = {"id": str(j)}
                            request = Request(url, urlencode(post_fields).encode())
                            code = unquote(str(urlopen(request).read()).split("&")[10])[6:]
                            codes[j] = code
                            json.dump(codes, open("codes.json", "w"))
                        except:
                            input("runouw.com is *probably, not definitely* down. This means you will only be able to browse levels available the last time the site was up.")
                            if not os.path.exists("codes.json"):
                                input("No level code backup found! Press enter to exit...")
                                sys.exit
                print("Levels loaded successfully!")
            try:
                levelCode = codes[levelID]
            except KeyError:
                levelCode = ""
            levelName = "unknown"
            for i in levels:
                if i[0] == levelID:
                    levelName = i[1]
                    break
            if levelCode != "":
                print("Level found:", levelName + "!\nCopying code to clipboard...")
                copyToClipboard(levelCode)
                print("Done")
                break
            elif levelID.lower() == "end":
                break
            else:
                print("Level not found!")
    else:
        print("Invalid input!")
       
