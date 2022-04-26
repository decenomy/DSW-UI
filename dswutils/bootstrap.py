import requests
import platform
import zipfile
import os

def bdownload(url, fname):
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))
    with open(fname, 'wb') as file:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)


def wipe(coin):
    plt = platform.system()
    if  plt == "Windows":
        home = os.path.expanduser("~")
        for i in os.listdir(home + "\\AppData\\Roaming\\" + coin.capitalize() + "blocks" ):
            os.remove(os.path.join(home + "\\AppData\\Roaming\\" + coin.capitalize() + "blocks" , i))
        for i in os.listdir(home + "\\AppData\\Roaming\\" + coin.capitalize() + "chainstate" ):
            os.remove(os.path.join(home + "\\AppData\\Roaming\\" + coin.capitalize() + "chainstate" , i))
        os.rmdir(home + "\\AppData\\Roaming\\" + coin.capitalize() + "blocks" )
        os.rmdir(home + "\\AppData\\Roaming\\" + coin.capitalize() + "chainstate" )
        with zipfile.ZipFile("bootstrap.zip", "r") as zip_ref:
            zip_ref.extractall(home + "\\AppData\\Roaming\\" + coin.capitalize())
        os.remove("bootstrap.zip")
    elif plt == "Linux":
        home = os.path.expanduser("~")
        os.system("rm -rf " + home + "/." + coin + "/chainstate")
        os.system("rm -rf " + home + "/." + coin + "/blocks")
        with zipfile.ZipFile("bootstrap.zip", "r") as zip_ref:
            zip_ref.extractall(home + "/." + coin + "/")
        os.remove("bootstrap.zip")
    elif plt == "Darwin":
        print("Your system is MacOS")
    else:
        print("Unidentified system")



