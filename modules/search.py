from googlesearch import search

def extensionsearch(target,num):
    extensions = ['docx','pptx','pdf','xlsx', 'doc', 'ppt', 'xls']
    res = []
    for ext in extensions:
        query = 'filetype:%s site:%s' % (ext,target)
        for url in search(query, stop=num):
            e = url.split('.')[-1]
            #if e in extensions:	
            res.append(url)
    return res
