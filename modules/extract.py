import exiftool
import json, time
import tempfile, shutil
from zipfile import ZipFile

class MinDoc():
    def __init__(self,url,ftype,diskpath):
        self.url = url
        self.ftype = ftype
        self.diskpath = diskpath
    
    def retjson(self):
        propjson = {
            "url":self.url,
            "filetype":self.ftype,
            "path":self.diskpath   
        }
        return propjson

class StarDoc(MinDoc):
    def __init__(self,url,ftype,diskpath):
        MinDoc.__init__(self,url,ftype,diskpath)
        self.producer = None
        self.author = None
        self.creator = None

    def __getitem__(self,item):
        return getattr(self,item)
    
    def __setitem__(self,obj,key,item):
        '''need to pass metadata and key separately to avoid trying to read the value of a non-existent key'''
        try:
            setattr(self,item,obj[key])
        except:
            pass

    def prepcsv(self):
        '''remove commas from metadata properties'''
        self.creator = self.creator.encode('ascii','ignore').replace(',','') if self.creator is not None and type(self.creator) is not int else self.creator
        self.producer = self.producer.encode('ascii','ignore').replace(',','') if self.producer is not None and type(self.producer) is not int else self.producer
        self.author = self.author.encode('ascii','ignore').replace(',','') if self.author is not None and type(self.author) is not int else self.author

    def guessextract(self,et):
        '''try to extract metadata from an unknown office doc using both extraction methods'''
        self.stdextract(et)
        if self.author is None and self.creator is None and self.producer is None:
            self.tmpfextract(et)

    def tmpfextract(self,et):
        '''extract metadata from newer office formats (which are archived XML files)'''
        tempdir = tempfile.mkdtemp()
        with ZipFile(self.diskpath,'r') as z:
            z.extractall(tempdir)
        md = et.get_metadata(tempdir+'/docProps/core.xml')
        shutil.rmtree(tempdir)

        self.__setitem__(md,'XMP:CorePropertiesCreator','creator')

    def stdextract(self,et):
        '''extraction for normally supported extensions (e.g. PDF & older office formats)'''
        md = et.get_metadata(self.diskpath)

        if self.ftype in ['doc','xls','ppt','office']:
            self.__setitem__(md,'FlashPix:Author','author')
        elif self.ftype == 'pdf':
            self.__setitem__(md,'PDF:Author','author')
            self.__setitem__(md,'PDF:Producer','producer')
            self.__setitem__(md,'PDF:Creator','creator')

    def extractmetadata(self,et):
        '''extract metadata based on file type
           commas are stripped'''
        if self.ftype in ['docx','xlsx','pptx']:
            self.tmpfextract(et)
        elif self.ftype == 'office':
            self.guessextract(et)
        else:
            self.stdextract(et)

def processmanifest(manf,ofp):
    '''takes in manifest and produces new manifest with metadata'''
    with open(manf, 'r') as f:
        manstr = f.read()
    manf = json.loads(manstr)
    with exiftool.ExifTool() as et:
        for df in manf['files']:
            docu = StarDoc(df['url'],df['filetype'],df['path'])
            docu.extractmetadata(et)
            docu.prepcsv()
            df['producer'] = docu.producer
            df['creator'] = docu.creator
            df['author'] = docu.author
    manf['meta']['timestamp'] = int(time.time())
    with open(ofp,'w') as f:
        f.write(json.dumps(manf,indent=4,sort_keys=True))
    return manf

def pprintmanifest(manj):
    print 'Producer,Creator,Author,URL'
    for df in manj['files']:
        print '%s,%s,%s,%s' % (df['producer'],df['creator'],df['author'],df['url'])
