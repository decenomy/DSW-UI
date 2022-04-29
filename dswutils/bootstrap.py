import requests
import platform
import zipfile
import os
import shutil

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
        try:
            shutil.rmtree(home + "\\AppData\\Roaming\\" + coin.capitalize() + "\\blocks" )
            shutil.rmtree(home + "\\AppData\\Roaming\\" + coin.capitalize() + "\\chainstate" )
        except:
            pass
        with zipfile.ZipFile("bootstrap.zip", "r") as zip_ref:
            zip_ref.extractall(home + "\\AppData\\Roaming\\" + coin.capitalize())
        os.remove("bootstrap.zip")
    elif plt == "Linux":
        home = os.path.expanduser("~")
        try:
            os.system("rm -rf " + home + "/." + coin + "/chainstate")
            os.system("rm -rf " + home + "/." + coin + "/blocks")
        except:
            pass
        with zipfile.ZipFile("bootstrap.zip", "r") as zip_ref:
            zip_ref.extractall(home + "/." + coin + "/")
        os.remove("bootstrap.zip")
    elif plt == "Darwin":
        print("Your system is MacOS")
    else:
        print("Unidentified system")



