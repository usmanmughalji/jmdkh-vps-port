import re
import binascii
from base64 import b64decode
from requests import Session

# Rename re.findall to re_findall
from re import findall as re_findall

from bot.helper.ext_utils.exceptions import DirectDownloadLinkException

CRYPT = "" # Crypt cookie

def re_findall(pattern: str, string: str) -> list:
    try:
        return re.findall(pattern, string)
    except:
        return []

def gdtot_bypass(url: str) -> str:
    """ Gdtot google drive link generator
    By https://github.com/xcscxr """

    if CRYPT is None:
        raise DirectDownloadLinkException("ERROR: CRYPT cookie not provided")

    match = re_findall(r'https?://(.+)\.gdtot\.(.+)\/\S+\/\S+', url)[0]

    with Session() as client:
        client.cookies.update({'crypt': CRYPT})
        client.get(url)
        res = client.get(f"https://{match[0]}.gdtot.{match[1]}/dld?id={url.split('/')[-1]}")
    matches = re_findall('gd=(.*?)&', res.text)
    try:
        # Check if the length of the string is a multiple of 4
        missing_padding = len(matches[0]) % 4
        if missing_padding != 0:
            # Add padding characters until the length is a multiple of 4
            matches[0] += '=' * (4 - missing_padding)
        decoded_id = b64decode(matches[0]).decode('utf-8')
    except binascii.Error:
        raise DirectDownloadLinkException("ERROR: Invalid Base64-encoded string")
    except:
        raise DirectDownloadLinkException("ERROR: Try in your browser, mostly file not found or user limit exceeded!")
    return f'https://drive.google.com/open?id={decoded_id}'
