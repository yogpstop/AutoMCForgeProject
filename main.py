import urllib
import re
import zipfile
import os
import sys
import shutil
from xml.etree.ElementTree import *
pydir = os.path.dirname(os.path.abspath(__file__))
fl = urllib.urlopen('http://files.minecraftforge.net/').read().decode().replace('&nbsp;',' ').replace('\n',' ')
fll = re.split('Build ',fl)
regax = re.compile('\A(.*?): (.*?) for MC: (.*?)    .*?src.*?<a[^>]*?href="(.*?)"[^>]*?>\*</a>')
builds = {}
for build in fll:
    m = regax.match(build)
    if m:
        if not builds.has_key(m.group(3)):
            builds[m.group(3)] = []
        builds[m.group(3)].append([m.group(1),m.group(2),m.group(4)])
for build in builds.items():
    print build[0]
while True:
    version = raw_input('select version: ')
    if builds.has_key(version):
        break
for build in builds[version]:
    print build[0]," released on",build[1]
done = False
while True:
    bnum = raw_input('select build: ')
    for build in builds[version]:
        if build[0]==bnum:
            urllib.urlretrieve(build[2],'forge.zip')
            done = True
            break
    if done:
        break
zf = zipfile.ZipFile('forge.zip','r')
for f in zf.namelist():
    if not f.endswith('/'):
        zf.extract(f)
zf.close()
sys.path.append(os.path.abspath('forge'))
import install
mcpf = os.path.abspath(os.path.join('.api','Forge'+version))
if os.isdir(mcpf)
    shutil.rmtree(mcpf)
install.main(mcpf)
os.chdir(pydir)
shutil.rmtree('forge')
os.remove('forge.zip')
mcploc = "$%7BWORKSPACE-LOC%7D/.api/Forge"+version
tree = ElementTree()
pj=os.path.join(mcpf,"eclipse","Minecraft",".project")
tree.parse(pj)
for link in tree.find("linkedResources").getiterator("link"):
    if link.findtext("name") == "src":
        tree.find("linkedResources").remove(link)
        break
for vari in tree.find("variableList").getiterator("variable"):
    if vari.findtext("name") == "MCP_LOC":
        vari.find("value").text = mcploc
        break
tree.find("name").text = "@PROJECT_NAME@"
tree.write(pj)
tree = ElementTree()
cp=os.path.join(mcpf,"eclipse","Minecraft",".classpath")
tree.parse(cp)
for cpe in tree.getroot().getiterator("classpathentry"):
    if cpe.get("path") == "src":
        tree.getroot().remove(cpe)
        break
tree.getroot().append(Element("classpathentry",{"kind":"lib","path":"lib/deobfMC.jar","sourcepath":"lib/deobfMC-src.jar"}))
for cpe in tree.getroot().getiterator("classpathentry"):
    if cpe.get("path") == "jars/bin/minecraft.jar":
        tree.getroot().remove(cpe)
        tree.getroot().append(cpe)
        break
tree.write(cp)
zip = zipfile.ZipFile(os.path.join(mcpf,"lib","deobfMC.jar"),"w",zipfile.ZIP_DEFLATED)
dir = os.path.join(mcpf,"bin","minecraft")
for dpath,dnames,fnames in os.walk(dir):
    for fname in fnames:
        p = os.path.join(dpath,fname)
        zip.write(p,p.replace(dir,""))
zip.close()
zip = zipfile.ZipFile(os.path.join(mcpf,"lib","deobfMC-src.jar"),"w",zipfile.ZIP_DEFLATED)
dir = os.path.join(mcpf,"src","minecraft")
for dpath,dnames,fnames in os.walk(dir):
    for fname in fnames:
        p = os.path.join(dpath,fname)
        zip.write(p,p.replace(dir,""))
zip.close()
