# gutenbergToTei.py
#
# Reformats and renames etexts downloaded from Project Gutenberg.
#
# Software adapted from Michiel Overtoom, motoom@xs4all.nl, july 2009.
# 
# Modified by Matthew Jockers August 17, 2010 to encode result into TEI based XML
#


import os
import re
import shutil

remove = ["Produced by","End of the Project Gutenberg","End of Project Gutenberg"]

def beautify(fn, outputDir, filename):
    ''' Reads a raw Project Gutenberg etext, reformat paragraphs,
    and removes fluff.  Determines the title of the book and uses it
    as a filename to write the resulting output text. '''
    lines = [line.strip() for line in open(fn)]
    collect = False
    lookforsubtitle = False
    outlines = []
    startseen = endseen = False
    title=""
    one="<?xml version=\"1.0\" encoding=\"utf-8\"?><TEI xmlns=\"http://www.tei-c.org/ns/1.0\" version=\"5.0\"><teiHeader><fileDesc><titleStmt>"
    two = "</titleStmt><publicationStmt><publisher></publisher><pubPlace></pubPlace><availability status=\"free\"><p>Project Gutenberg</p></availability></publicationStmt><seriesStmt><title>Project Gutenberg Full-Text Database</title></seriesStmt><sourceDesc default=\"false\"><biblFull default=\"false\"><titleStmt>"
    three = "</titleStmt><extent></extent><publicationStmt><publisher></publisher><pubPlace></pubPlace><date></date></publicationStmt></biblFull></sourceDesc></fileDesc><encodingDesc><editorialDecl default=\"false\"><p>Preliminaries omitted.</p></editorialDecl></encodingDesc></teiHeader><text><body><div>"
    for line in lines:
        if line.startswith("Author: "):
        	author = line[8:]
        	authorTemp = line[8:]
        	continue
        if line.startswith("Title: "):
            title = line[7:]
            titleTemp = line[7:]
            lookforsubtitle = True
            continue
        if lookforsubtitle:
            if not line.strip():
                lookforsubtitle = False
            else:
                subtitle = line.strip()
                subtitle = subtitle.strip(".")
                title += ", " + subtitle
        if ("*** START" in line) or ("***START" in line):
            collect = startseen = True
            paragraph = ""
            continue
        if ("*** END" in line) or ("***END" in line):
            endseen = True
            break
        if not collect:
            continue
        if (titleTemp) and (authorTemp):
        	outlines.append(one)
        	outlines.append("<title>")
        	outlines.append(titleTemp)
        	outlines.append("</title>")
        	outlines.append("<author>")
        	outlines.append(authorTemp)
        	outlines.append("</author>")
        	outlines.append(two)
        	outlines.append("<title>")
        	outlines.append(titleTemp)
        	outlines.append("</title>")
        	outlines.append("<author>")
        	outlines.append(authorTemp)
        	outlines.append("</author>")
        	outlines.append(three)
        	authorTemp = False
        	titleTemp = False
        	continue
        if not line:
            paragraph = paragraph.strip()
            for term in remove:
                if paragraph.startswith(term):
                    paragraph = ""
            if paragraph:
            	paragraph = paragraph.replace("&", "&")
                outlines.append(paragraph)
                outlines.append("</p>")
            paragraph = "<p>"
        else:
            paragraph += " " + line
			
    # Compose a filename.  Replace some illegal file name characters with alternatives.
    #ofn = author + title[:150] + ".xml"
    ofn = filename
    ofn = ofn.replace("&", "")
    ofn = ofn.replace("/", "")
    ofn = ofn.replace("\"", "")
    ofn = ofn.replace(":", "")
    ofn = ofn.replace(",,", "")
    ofn = ofn.replace(" ", "")
    ofn = ofn.replace("txt", "xml")
        
    outlines.append("</div></body></text></TEI>")
    text = "\n".join(outlines)
    text = re.sub("End of the Project Gutenberg .*", "", text, re.M)
    text = re.sub("Produced by .*", "", text, re.M)
    text = re.sub("<p>\s+<\/p>", "", text)
    text = re.sub("\s+", " ", text)
    f = open(outputDir+ofn, "wt")
    f.write(text)
    f.close()

sourcepattern = re.compile(".*\.txt$")
sourceDir = "/Path/to/your/ProjectGutenberg/files/"
outputDir = "/Path/to/your/ProjectGutenberg/TEI/Output/files/"

for fn in os.listdir(sourceDir):
    if sourcepattern.match(fn):
        beautify(sourceDir+fn, outputDir, fn)
