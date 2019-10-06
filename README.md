# Deluxe - Metadata Search and Extract

Deluxe searches for PDF and Office documents for a target domain, downloads them, then extracts the authorship metadata from them. Alternatively, it can scrape a URL for document links, download them, then extract the authorship metadata from them. 

After performing the initial search or scrape, the tool produces a manifest file in the output directory. This manifest contains information about each files downloaded as well as some meta information about the documents. After performing extraction, a copy of the document is made an updated with the authorship information. See the [section](#manifest-files-structure) below for structure. 

Deluxe is the spiritual successor to [Metasearch](https://github.com/GeneralTesler/metasearch2), a tool I developed a while ago when I was first learning Python.

*Note: this is still a somewhat beta release and requires some additional testing. If you have any feedback, please open an issue.*

## Install

```
pip install -r requirements
```

*note: virtualenv recommended*

## Usage

**Search**

```
usage: deluxe search [-h] -d DOMAIN [-n NUMRES] -o SEARCHOUT

optional arguments:
  -h, --help    show this help message and exit
  -d DOMAIN     target domain
  -n NUMRES     approx. number of search results to retrieve (per extension)
  -o SEARCHOUT  output directory for files
```

Notes

- The -n argument specifies the number of results to stop at (default 50). This is only an approximate number


**Scrape**

```
usage: deluxe scrape [-h] -u URL -o SCRAPEOUT

optional arguments:
  -h, --help    show this help message and exit
  -u URL        page to scrape
  -o SCRAPEOUT  output directory for files
```

**Extract**

```
usage: deluxe extract [-h] -m MAN -o EXTOUT [-p]

optional arguments:
  -h, --help   show this help message and exit
  -m MAN       manifest file location
  -o EXTOUT    output file name
  -p, --print  print list of results to terminal (de-duped across all files)
```

## Manifest Files Structure

**Pre-extract**

```
{
  "files": [
    {
      "filetype": "string",     //extension (e.g. pdf, docx)
      "path": "string",         //path on disk to file
      "url": "string"           //url for file
    },
    ...
  ],
  "meta": {
    "directory": "string",      //directory where file was downloaded to
    "manifest": "string",       //name of manifest file (including path)
    "timestamp": int,           //timestamp when manifest was made
    "total": int                //total number of documents downloaded
} 
```

**Post-extract**

```
{
  "files": [
    {
      "filetype": "string",     //extension (e.g. pdf, docx)
      "names" : list            //de-duped (per file) list of names extracted (e.g. author)
      "path": "string",         //path on disk to file
      "url": "string"           //url for file
    },
    ...
  ],
  "meta": {
    "directory": "string",      //directory where file was downloaded to
    "manifest": "string",       //name of manifest file (including path)
    "timestamp": int,           //timestamp when manifest was made (gets updated)
    "total": int                //total number of documents downloaded
} 
```

## To-dos

- 

## Changelog

- 10/6/2019 - testing not using Exiftool
- 8/18/2018 - Initial release