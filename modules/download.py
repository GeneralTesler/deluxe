import shutil, os, uuid, json, time
import magic
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from modules.extract import MinDoc

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class ExtensionException(Exception):
    pass


def getextfrommime(buf):
    """get extension from mime type"""
    mime = magic.Magic(mime=True)
    mf = mime.from_buffer(buf)

    # http://filext.com/faq/office_mime_types.php
    if mf == "application/msword":
        return "doc"
    elif (
        mf == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        return "docx"
    elif mf == "application/vnd.ms-excel":
        return "xls"
    elif mf == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        return "xlsx"
    elif mf == "application/vnd.ms-powerpoint":
        return "ppt"
    elif (
        mf
        == "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    ):
        return "pptx"
    elif mf == "application/pdf":
        return "pdf"
    # magic will sometimes return this mime typee. its not associated with any particular office doc type
    # at some point, i will investigate a fix for this - until then, the extractor can guess
    elif mf == "application/vnd.ms-office":
        return "office"
    else:
        raise ExtensionException


def downloadlist(urls, outdir):
    """downloads a list of URLs to a specified directory
       performs a HEAD request beforehand to check for dead links
       uses magic to get the mime type (dont want to rely on extension in url)"""

    absp = os.path.abspath(outdir)

    ua = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }

    docs = []
    dltargets = []

    for url in urls:
        try:
            r = requests.head(url, headers=ua, allow_redirects=True, verify=False)
            if str(r.status_code)[:1] != "5" and str(r.status_code)[:1] != "4":
                dltargets.append(url)
        except:
            pass

    # TODO: add a status bar?
    if len(dltargets) > 0:
        if not os.path.isdir(absp):
            os.makedirs(absp)
        for url in dltargets:
            ofp = absp + "/" + str(uuid.uuid4())
            ext = ""

            r = requests.get(
                url, headers=ua, stream=True, allow_redirects=True, verify=False
            )
            try:
                ext = getextfrommime(r.content)
            except ExtensionException:
                pass

            with open(ofp, "wb") as f:
                for chunk in r.iter_content(chunk_size=128):
                    f.write(chunk)

            docs.append(MinDoc(url, ext, ofp).retjson())

    manf = absp + "/" + "manifest.json"
    manjson = {
        "files": docs,
        "meta": {
            "total": len(docs),
            "directory": absp,
            "manifest": manf,
            "timestamp": int(time.time()),
        },
    }
    with open(manf, "w") as f:
        f.write(json.dumps(manjson, indent=4, sort_keys=True))

    # return manf
