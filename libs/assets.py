from . import debug
from libs import modutil
import inspect
import os
import random


assetsPath = os.path.join(modutil.absolutePath, "assets")
tempPath = os.path.join(modutil.absolutePath, "temp")
assetDirs = []

debug.log("Loading assets...")

for asset in os.listdir(assetsPath):
    if os.path.isfile(os.path.join(assetsPath, asset)):
        debug.log(f"File '{asset}' was found on top of assets/, please create a subfolder for it.")
    else:
        assetDirs.append(asset)


def get(asset):
    """
    Gets the filename of an specified asset, None if it doesn't exist.
    :param asset: The name of the asset to search for.
    :return: The filename of the specified asset.
    """

    packagename = os.path.splitext(os.path.basename(inspect.stack()[1].filename))[0]
    if os.path.exists(os.path.join(assetsPath, packagename)):
        assetpathinpackage = os.path.join(assetsPath, packagename, asset)
        if os.path.exists(assetpathinpackage):
            return assetpathinpackage
        else:
            return getfrombasepath(asset)
    else:
        return getfrombasepath(asset)


def getfrombasepath(asset):
    """
        Gets the filename of an specified asset only in the base assets/ folder, None if it doesn't exist.
        For internal use only, use get() instead.
        :param asset: The name of the asset to search for.
        :return: The filename of the specified asset.
    """

    path = os.path.join(assetsPath, asset)
    if os.path.exists(path):
        return path
    else:
        debug.log("Trying to get asset '"+asset+"', which doesn't exist")
        return None

def gettemppath():
    """
        Obtains a temporal filepath.
    """

    return os.path.join(tempPath, "%032x" % random.getrandbits(128))
