import os
import sys
import shutil
import zipfile
_path_ = os.path.dirname(os.path.abspath(__file__))
def isbinary(file):
    f = open(file,'rb')
    for b in f.read():
        value = ord(b)
        if value < 10:
            return True
        if 10 < value and value < 13:
            return True
        if 13 < value and value < 32:
            return True
        if value == 127:
            return True
    f.close()
    return False
def cmp_version(a,b):
    if a == None:
        return 1
    if b == None:
        return -1
    import re
    cr = re.compile('[^0-9]')
    sa = cr.split(a)
    salen = len(sa)
    sb = cr.split(b)
    sblen = len(sb)
    blen = salen
    if blen < sblen:
        blen = sblen
    i = 0
    while True:
        if i >= salen:
            if not (i >= sblen):
                return -int(sb[i])
            return 0
        if i >= sblen:
            return int(sa[i])
        resu = int(sa[i]) - int(sb[i])
        if not (resu == 0):
            return resu
        i+=1
def install():
    import urllib
    import re
    from xml.etree.ElementTree import ElementTree, Element
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
    for m in sorted(builds.keys(), cmp=cmp_version):
        print m
    while True:
        mcversion = raw_input('select Minecraft version: ')
        if builds.has_key(mcversion):
            break
    for build in sorted(builds[mcversion],key=lambda x:x[0], cmp=cmp_version):
        print build[0]," released on ",build[1]
    done = False
    while True:
        bnum = raw_input('select Forge build: ')
        for build in builds[mcversion]:
            if build[0]==bnum:
                urllib.urlretrieve(build[2],'forge.zip')
                done = True
                break
        if done:
            break
    zf = zipfile.ZipFile('forge.zip','r')
    zf.extractall()
    zf.close()
    sys.path.append(os.path.join(_path_,'forge'))
    import install
    mcpf = os.path.join(_path_,'.api','Forge'+mcversion)
    if os.path.isdir(mcpf):
        shutil.rmtree(mcpf)
    install.main(mcpf)
    os.chdir(_path_)
    shutil.rmtree('forge')
    os.remove('forge.zip')
    mcploc = "$%7BWORKSPACE_LOC%7D/.api/Forge"+mcversion
    tree = ElementTree()
    basedir = os.path.join(mcpf,'eclipse','Minecraft')
    pj=os.path.join(basedir,".project")
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
    cp=os.path.join(basedir,".classpath")
    tree.parse(cp)
    for cpe in tree.getroot().getiterator("classpathentry"):
        if cpe.get("path") == "src":
            tree.getroot().remove(cpe)
            break
    tree.getroot().insert(0,Element("classpathentry",{"kind":"lib","path":"lib/deobfMC.jar","sourcepath":"lib/deobfMC-src.jar"}))
    tree.write(cp)
    zip = zipfile.ZipFile(os.path.join(mcpf,"lib","deobfMC.jar"),"w",zipfile.ZIP_DEFLATED)
    dir = os.path.join(mcpf,"bin","minecraft")+os.sep
    for dpath,dnames,fnames in os.walk(dir):
        for fname in fnames:
            p = os.path.join(dpath,fname)
            zip.write(p,p.replace(dir,""))
    zip.close()
    zip = zipfile.ZipFile(os.path.join(mcpf,"lib","deobfMC-src.jar"),"w",zipfile.ZIP_DEFLATED)
    dir = os.path.join(mcpf,"src","minecraft")+os.sep
    for dpath,dnames,fnames in os.walk(dir):
        for fname in fnames:
            p = os.path.join(dpath,fname)
            zip.write(p,p.replace(dir,""))
    zip.close()
    return mcversion
def get_newest():
    versions = []
    for dir in os.listdir(os.path.join(_path_,'.api')):
        if not dir.startswith('Forge'):
            continue
        versions.append(dir.replace('Forge',''))
    if len(versions)==0:
        versions.append(install())
    versions = sorted(versions, cmp=cmp_version,reverse=True)
    return versions[0]
def i_eclipse(dir,version=None):
    if version == None:
        version = get_newest()
    fromdir = os.path.join(_path_,'.api','Forge'+version,"eclipse","Minecraft")
    todir = os.path.join(_path_,dir)
    shutil.copy2(os.path.join(fromdir,'.classpath'),os.path.join(todir,'.classpath'))
    inputfile = open(os.path.join(fromdir,'.project'),'rb')
    filedata = inputfile.read()
    inputfile.close()
    filedata = filedata.replace('@PROJECT_NAME@',dir)
    outputfile = open(os.path.join(todir,'.project'),'wb')
    outputfile.write(filedata)
    outputfile.close()
def i_all(version=None):
    if version == None:
        version = get_newest()
    for dir in os.listdir(_path_):
        if dir.startswith('.'):
            continue
        if not os.path.isdir(os.path.join(_path_,dir)):
            continue
        while True:
            ret = raw_input(dir+' is MinecraftForge project?')
            if ret[0] == 'y' or ret[0] == 'Y':
                i_eclipse(dir,version)
                break;
            if ret[0] == 'n' or ret[0] == 'N':
                break;
class build:
    def __init__(self, mversion, fversion=get_newest(), out=None):
        if out == None:
            out = os.path.join('dist',fversion,os.path.basename(os.getcwd())+'-'+mversion+'.zip')
        self.zip = os.path.abspath(out)
        exdir = os.path.dirname(self.zip)
        if not os.path.isdir(exdir):
            os.makedirs(exdir)
        self.mcpdir = os.path.join(_path_,'.api','Forge'+fversion)
        self.srces = []
        self.reses = []
        self.apies = []
        self.repes = {}
        self.repes['@VERSION@']=mversion
    def src(self, dir):
        ndir = os.path.abspath(os.path.dirname(dir))+os.sep
        dir = os.path.abspath(dir)
        cache = []
        for fpath, dnames, fnames in os.walk(dir):
            for fname in fnames:
                cache.append(os.path.join(fpath,fname).replace(ndir,''))
            for dname in dnames:
                cache.append(os.path.join(fpath,dname).replace(ndir,''))
        tap = (ndir,cache)
        self.srces.append(tap)
    def res(self, dir):
        ndir = os.path.abspath(os.path.dirname(dir))+os.sep
        dir = os.path.abspath(dir)
        cache = []
        for fpath, dnames, fnames in os.walk(dir):
            for fname in fnames:
                cache.append(os.path.join(fpath,fname).replace(ndir,''))
            for dname in dnames:
                cache.append(os.path.join(fpath,dname).replace(ndir,''))
        tap = (ndir,cache)
        self.reses.append(tap)
    def api(self, path):
        self.apies.append(os.path.join(_path_,'.api',path))
    def rep(self, bef, aft):
        self.repes[bef] = aft
    def process(self):
        import time
        deles = []
        sys.path.insert(0,os.path.join(self.mcpdir,'runtime'))
        os.chdir(self.mcpdir)
        import recompile, reobfuscate, updatemd5
        srcdir = os.path.join(self.mcpdir,'src','minecraft')
        for api in self.apies:
            zf = zipfile.ZipFile(api,'r')
            for f in zf.namelist():
                cache = os.path.join(srcdir,f)
                if not os.path.exists(cache):
                    deles.append(cache)
                    if f.endwith('/'):
                        os.mkdir(cache)
                    else:
                        zf.extract(f,srcdir)
            zf.close()
        sys.argv.append('--force')
        updatemd5.main()
        sys.argv.remove('--force')
        for base, list in self.srces:
            for src in list[:]:
                tofile = os.path.join(srcdir,src)
                fromfile = os.path.join(base,src)
                todir = os.path.dirname(tofile)
                if not os.path.isdir(todir):
                    cache = todir
                    while True:
                        if os.path.isdir(os.path.dirname(cache)):
                            break
                        cache = os.path.dirname(cache)
                    deles.append(cache)
                if os.path.exists(tofile):
                    list.remove(src)
                elif os.path.isdir(fromfile):
                    os.mkdir(tofile)
                elif isbinary(fromfile):
                    shutil.copy2(fromfile,tofile)
                else:
                    inputfile = open(fromfile,'rb')
                    filedata = inputfile.read()
                    inputfile.close()
                    for repfrom,repto in self.repes.items():
                        filedata = filedata.replace(repfrom,repto)
                    outputfile = open(tofile,'wb')
                    outputfile.write(filedata)
                    outputfile.close()
        try:
            recompile.main()
        except SystemExit:
            pass
        reobfuscate.main()
        for base,list in self.srces:
            for src in list:
                cache = os.path.join(srcdir,src)
                if os.path.isdir(cache):
                    shutil.rmtree(cache)
                elif os.path.isfile(cache):
                    os.remove(cache)
        for delf in deles:
            if os.path.isdir(delf):
                shutil.rmtree(delf)
            elif os.path.isfile(delf):
                os.remove(delf)
        output = zipfile.ZipFile(self.zip,'w',zipfile.ZIP_DEFLATED)
        reobfdir = os.path.join(self.mcpdir,'reobf','minecraft')+os.sep
        for base,dnames,fnames in os.walk(reobfdir):
            for dname in dnames:
                cache = os.path.join(base,dname)
                output.write(cache,cache.replace(reobfdir,''))
            for fname in fnames:
                cache = os.path.join(base,fname)
                output.write(cache,cache.replace(reobfdir,''))
        for base,list in self.reses:
            for res in list:
                cache = os.path.join(base,res)
                if os.path.isdir(cache):
                    output.write(cache,res)
                elif isbinary(cache):
                    output.write(cache,res)
                else:
                    inputfile = open(cache,'rb')
                    filedata = inputfile.read()
                    inputfile.close()
                    for repfrom,repto in self.repes.items():
                        filedata = filedata.replace(repfrom,repto)
                    st = os.stat(cache)
                    zinfo = zipfile.ZipInfo(res, time.localtime(st.st_mtime)[0:6])
                    zinfo.external_attr = (st[0] & 0xFFFF) << 16L
                    zinfo.compress_type = output.compression
                    zinfo.flag_bits = 0x00
                    output.writestr(zinfo,filedata)
        output.close()
if __name__ == '__main__':
    i_all(install())