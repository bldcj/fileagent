import os
import xml.etree.ElementTree as ET
from datetime import datetime
import re
import shutil
import json

from flask import Flask
from flask import request
from flask import Response
from flask import abort
from flask_cors import CORS

import file_reader

def ls(path,if_get_child,tree):
    if os.path.exists(path):
        os.chdir(path)
        dirs=os.listdir()
        manifest_path=""
        manifest_path=os.path.join(path,"fileagent_keywords.json")
        metadata={}
        if os.path.exists(manifest_path):
            with open(manifest_path,mode="r") as manifest:
                metadata=json.loads(manifest.read())
        for file in dirs:
            if os.path.isdir(file):
                child_folder=ET.SubElement(tree,"folder")
                child_folder.attrib["name"]=file
                info=os.stat(file)
                child_folder.attrib["time"]=datetime.fromtimestamp(int(info.st_mtime)).strftime("%Y-%m-%d %H:%M:%S")
                child_folder.attrib["path"]=os.path.abspath(file)
                if if_get_child==1:
                    ls(file,1,child_folder)
                    os.chdir("../")
            elif os.path.isfile(file):
                if file!="fileagent_keywords.json":
                    child_file=ET.SubElement(tree,"file")
                    child_file.attrib["name"]=file
                    info=os.stat(file)
                    child_file.attrib["time"]=datetime.fromtimestamp(int(info.st_mtime)).strftime("%Y-%m-%d %H:%M:%S")
                    child_file.attrib["size"]=str(info.st_size)
                    child_file.attrib["path"]=os.path.abspath(file)
                    if file in metadata:
                        keywords=""
                        for k in metadata[file]["keywords"]:
                            keywords=keywords+k+" "
                        keywords=keywords[0:-1]
                        child_file.attrib["keywords"]=keywords
        return tree

app=Flask(__name__)
cors=CORS(app)

@app.route("/ls")
def web_ls():
    p=request.args.get("p")
    c=int(request.args.get("c"))
    if p is None or c is None:
        abort(400)
    if os.path.exists(p):
        root=ET.Element("directory")
        root.attrib["path"]=p
        xml=bytes.decode(ET.tostring(ls(p,c,root),encoding="UTF-8"))
        response=Response(xml,status=200)
        response.headers["Content-Type"]="application/xml"
        return response
    else:
        return "No such directory."
    
@app.get("/cd")
def web_cd():
    p=request.args.get("p")
    if p:
        if os.path.exists(p):
            os.chdir(p)
            with open(os.path.join(os.path.dirname(__file__),"last_directory"),mode="w") as f:
                f.write(p)
            return os.getcwd()
        else:
            return "no such directory."
    else:
        return os.getcwd()

@app.get("/get-text")
def web_get_text():
    p=request.args.get("p")
    text=''
    if os.path.exists(p):
        if re.search("\\.doc$",p):
            text=file_reader.get_doc_text(p)
        elif re.search("\\.pdf$",p):    
            text=file_reader.get_pdf_text(p)
        elif re.search("\\.txt$",p):
            text=file_reader.get_txt_text(p)
        else:
            return "Unsupported type"
        return text
    else:
        return "No such file"
    
@app.get("/mkdir")
def web_mkdir():
    p=request.args.get("p")
    if os.path.exists(p):
        return "Existed directory."
    else:
        if os.path.exists(os.path.dirname(p)):
            os.mkdir(p)
            root=ET.Element("directory")
            root.attrib["path"]=p
            xml=bytes.decode(ET.tostring(ls(p,0,root),encoding="UTF-8"))
            response=Response(xml,status=200)
            response.headers["Content-Type"]="application/xml"
            return response
        else:
            return "No parent directory."

@app.get("/rm")
def web_rm():
    p=request.args.get("p")
    if p is None:
        abort(400)
    else:
        if os.path.exists(p):
            if os.path.isfile(p):
                os.remove(p)
            elif os.path.isdir(p): 
                shutil.rmtree(p)
            else:
                return "Unsupported path."
            return "Done."
        else:
            return "No such file or directory"
        
@app.get("/rename")
def web_rename():
    p=request.args.get("p")
    s=request.args.get("s")
    d=request.args.get("d")
    if os.path.exists(p):
        os.chdir(p)
        if os.path.exists(s):
            os.rename(s,d)
            return "Done."
        else:
            return "No such file or directory."
    else: 
        return "No such file or directory."

@app.get("/copy")
def web_copy():
    s=request.args.get("s")
    d=request.args.get("d")
    if os.path.exists(s):
        if os.path.exists(os.path.dirname(d)):
            if os.path.isfile(s):
                shutil.copy(s,d)
            elif os.path.isdir(s):
                shutil.copytree(s,d)
            else:
                return "Unsupported path."
            return "Done."
        else:
            return "Need parent directory."
    else:
        return "No such file or directory."

@app.get("/cut")
def web_cut():
    s=request.args.get("s")
    d=request.args.get("d")
    if os.path.exists(s):
        if os.path.exists(os.path.dirname(d)):
            if os.path.isfile(s):
                shutil.copy(s,d)
                os.remove(s)
            elif os.path.isdir(s):
                shutil.copytree(s,d)
                shutil.rmtree(s)
            else:
                return "Unsupported path."
            return "Done."
        else:
            return "Need parent directory."
    else:
        return "No such file or directory."

@app.get("/stat")
def web_stat():
    p=request.args.get("p")
    if os.path.exists(p):
        return json.dumps(os.stat(p))
    else:
        return "No such file or directory."

@app.route("/store-keywords",methods=["POST"])
def web_store_keywords():
    p=request.args.get("p")
    keywords=request.json.get("keywords")
    print(keywords[0])
    if os.path.exists(p) and os.path.isfile(p):
        if keywords is None:
            return "Need keywords."
        else:
            data={}
            manifest_path=os.path.join(os.path.dirname(p),"fileagent_keywords.json")
            if os.path.exists(manifest_path):
                with open(manifest_path,mode="r") as manifest:
                    data=json.loads(manifest.read())
            data[os.path.basename(p)]={"keywords":keywords}
            with open(manifest_path,mode="w") as manifest:
                data=json.dumps(data)
                manifest.write(data)
            return data
    else:
        return "No such file."

@app.route("/preferences/set",methods=["POST"])
def web_set_preferences():
    preferences=request.json.get("preferences")
    data=""
    with open(os.path.join(os.path.dirname(__file__),"preferences.json"),mode="w") as f:
        data=json.dumps(preferences)
        f.write(data)
    return data

@app.route("/preferences/get",methods=["GET"])
def web_read_preferences():
    p=os.path.join(os.path.dirname(__file__),"preferences.json")
    if os.path.exists(p):
        with open(p,mode="r") as f:
            return f.read()
    else:
        return "0"
    
@app.get("/lastdir")
def web_lastdir():
    with open(os.path.join(os.path.dirname(__file__),"last_directory"),mode="r") as f:
        return f.read()

if __name__=="__main__":
    app.run(host="0.0.0.0")

