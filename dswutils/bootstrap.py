import requests
import platform
import zipfile
import os
from tqdm import tqdm

def bdownload(url, fname):
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))
    with open(fname, 'wb') as file, tqdm(
            desc=fname,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)


def wipe():
    plt = platform.system()

    if   plt == "Windows":
        print("Your system is Windows")
    elif plt == "Linux":
        home = os.path.expanduser("~")
        os.system("rm -rf " + home + "/.sapphire/chainstate")
        os.system("rm -rf " + home + "/.sapphire/blocks")
        with zipfile.ZipFile("bootstrap.zip", "r") as zip_ref:
            zip_ref.extractall(home + "/.sapphire/")
        os.remove("bootstrap.zip")
    elif plt == "Darwin":
        print("Your system is MacOS")
    else:
        print("Unidentified system")


bdownload("https://explorer.decenomy.net/bootstraps/SAPP/bootstrap.zip", "bootstrap.zip")

wipe()

