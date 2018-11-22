#! /usr/bin/python3

#Permission is hereby granted, free of charge, to any person
#obtaining a copy of this software and associated documentation files
#(the "Software"), to deal in the Software without restriction,
#including without limitation the rights to use, copy, modify, merge,
#publish, distribute, sublicense, and/or sell copies of the Software,
#and to permit persons to whom the Software is furnished to do so,
#subject to the following conditions:
#
#The above copyright notice and this permission notice shall be
#included in all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
#BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
#ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
#CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import pandas as pd
import sys
import collections

def readCsvToDictsAppend(result,filename,keyname):
    reader = pd.read_csv(filename, encoding = "ISO-8859-1")
    readerDict = reader.to_dict('records')
    for rowDict in readerDict:
        key = rowDict[keyname]
        if key in result:
            sys.exit("fatal error, the file: "+filename+" has double key: "+key)
        result[key] = rowDict
    return result

def readCsvToDicts(filename,keyname):
    result = {}
    return readCsvToDictsAppend(result,filename,keyname)

def fatal(errorMsg):
    print(errorMsg)
    exit(1)
    
if len(sys.argv) < 2:
    print('Must be called like: \n'+sys.argv[0]+' ENTITIES_CSV_FILE')
    exit(1)

entitiesCsvFilename = sys.argv[1]
    
entities = readCsvToDicts(entitiesCsvFilename,"item")
for i in range (2,len(sys.argv)):
    readCsvToDictsAppend(entities,sys.argv[i],"item")
keys = readCsvToDicts("csv/keys.csv","name")
key_texts = readCsvToDicts("csv/key_text.csv","key")
notes = readCsvToDicts("csv/note.csv","name")
note_texts = collections.OrderedDict()
readCsvToDictsAppend(note_texts, "csv/note_text.csv", "key")
spawnflags = readCsvToDicts("csv/spawnflags.csv","item")
spawnflag_texts = readCsvToDicts("csv/spawnflag_text.csv","key")

def printKeys(item_name):
    for item in sorted(key_texts):
        if item_name in keys.keys():
            keyLine = keys[item_name]
            if item in keyLine.keys():
                hasKey = keyLine[item]
                #The hasKey == hasKey us used to check for NaN. Blank fields are NaNs in Pandas
                if (hasKey and hasKey == hasKey):
                    defaultText = ""
                    basename = item
                    basekey = key_texts[item]["basekey"]
                    if (isTrue(basekey)):
                        basename = basekey
                    name = basename
                    fullname = key_texts[item]["fullname"]
                    if (isinstance(fullname, str) and len(fullname)>0):
                        name = fullname
                    try:
                        defaultTextActual = keyLine[item+"_default"]
                        if key_texts[item]["type"] == "integer":
                            defaultText = " Default: "+str(int(defaultTextActual))+"."
                        else:
                            defaultText = " Default: "+str(defaultTextActual)+"."
                    except:
                        defaultText = ""
                    text = key_texts[item]["text"]
                    if (text and text == text):
                        print("\""+basename+"\" : "+str(key_texts[item]["text"])+defaultText)
                    else:
                        print("\""+basename+"\" : No text"+defaultText)

def printNotes(item_name):
    for item in note_texts.keys():
        if (item_name in notes.keys()):
            keyLine = notes[item_name]
            if item in sorted(keyLine.keys()):
                hasKey = keyLine[item]
                if (hasKey and hasKey == hasKey):
                    print(str(note_texts[item]["text"]))
                    

def isTrue(some_value):
    # True is represented by the string "true". Note that pandas uses NaN for blank strings
    if (isinstance(some_value, str) and len(some_value)>0):
        return True
    return False
    
for item in sorted(entities):
    row = entities[item]
    print(row["quaked"])
    if isinstance(row["model"],str):
        model = row["model"]
        print("--------- MODEL FOR RADIANT ONLY - DO NOT SET THIS AS A KEY --------")
        print("model=\""+model+"\"")
    if isinstance(row["description"],str):
        print(row["description"])
    print("--------- KEYS --------")
    printKeys(item)
    print("--------- NOTES --------")
    printNotes(item)
    print("*/")
    