import json, time
import tempfile, shutil
from zipfile import ZipFile
import olefile
import xml.etree.ElementTree as et
from pdfrw import PdfReader

# pdfrw sometimes runs into a header check error
# when it does, the library prints an error to the terminal
# need to change the logging level to prevent this
from pdfrw.errors import log, logging

log.setLevel(logging.CRITICAL)


class MinDoc:
    def __init__(self, url, ftype, diskpath):
        self.url = url
        self.ftype = ftype
        self.diskpath = diskpath

    def retjson(self):
        return {"url": self.url, "filetype": self.ftype, "path": self.diskpath}


class StarDoc(MinDoc):
    def __init__(self, url, ftype, diskpath):
        MinDoc.__init__(self, url, ftype, diskpath)
        self.names = set()

    def conv_name_list(self):
        names_clean = set()
        for name in set(filter(None, self.names)):
            if type(name) == bytes:
                name = name.decode("utf-8", "ignore")
            if name[0] == "(":
                name = name[1:]
            if name[-1] == ")":
                name = name[:-1]
            names_clean.add(name)

        self.names = list(names_clean)

    def extract_metadata(self):
        if self.ftype in ["docx", "xlsx", "pptx"]:
            self.get_oo_metadata()
        elif self.ftype in ["doc", "xls", "ppt", "office"]:
            self.get_ole_metadata()
        elif self.ftype == "pdf":
            self.get_pdf_metadata()

        self.conv_name_list()

    def get_ole_metadata(self):
        # for doc, xls, and ppt
        with olefile.OleFileIO(self.diskpath) as ole:
            md = ole.get_metadata()
            self.names.add(md.author)

    def get_oo_metadata(self):
        # for docx, xlsx, pptx

        # TODO: move all extraction to in-memory
        tempdir = tempfile.mkdtemp()
        with ZipFile(self.diskpath, "r") as z:
            z.extractall(tempdir)

        tree = et.parse(tempdir + "/docProps/core.xml")

        for creator in tree.findall("{http://purl.org/dc/elements/1.1/}creator"):
            self.names.add(creator.text)

        for lmb in tree.findall(
            "{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}lastModifiedBy"
        ):
            self.names.add(lmb.text)

        shutil.rmtree(tempdir)

    def get_pdf_metadata(self):
        # for pdf
        try:
            pdf = PdfReader(self.diskpath)
        except ValueError:
            pass
        else:
            if "/Info" in pdf.keys():
                # library doesn't throw errors if property doesnt exist
                self.names.add(pdf.Info.Author)
                self.names.add(pdf.Info.Creator)
                self.names.add(pdf.Info.Producer)


def processmanifest(manf, ofp):
    """takes in manifest and produces new manifest with metadata"""
    with open(manf, "r") as f:
        manstr = f.read()
    manf = json.loads(manstr)
    for df in manf["files"]:
        docu = StarDoc(df["url"], df["filetype"], df["path"])
        docu.extract_metadata()
        df["names"] = docu.names
    manf["meta"]["timestamp"] = int(time.time())
    with open(ofp, "w") as f:
        f.write(json.dumps(manf, indent=4, sort_keys=True, default=str))
    return manf


def pprintmanifest(manj):
    names = []
    print("Names\n=====")

    for df in manj["files"]:
        if len(df["names"]) > 0:
            names.extend(df["names"])

    names = set(names)
    print("\n".join(names))
