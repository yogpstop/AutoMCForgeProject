import os,sys,shutil,zipfile,time,logging,ConfigParser
_path_ = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger()
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
def select_one():
    dirs=[]
    for dir in os.listdir(_path_):
        if dir.startswith('.'):
            continue
        if not os.path.isdir(os.path.join(_path_,dir)):
            continue
        if not os.path.isfile(os.path.join(_path_,dir,'build.cfg')):
            continue
        dirs.append(dir)
    i = 0
    while(i<len(dirs)):
        print str(i)+' '+dirs[i]
        i+=1
    while True:
        num = raw_input('select target project: ')
        if num.isdigit():
            if int(num)<len(dirs):
                return dirs[int(num)]
def install():
    import urllib
    import re
    from xml.etree.ElementTree import ElementTree, Element
    print '> Start forge install'###############################################################################################
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
    ############################################################################################################################
    for m in sorted(builds.keys(), cmp=cmp_version):
        print m
    while True:
        mcversion = raw_input('select Minecraft version: ')
        if builds.has_key(mcversion):
            break
    ############################################################################################################################
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
    print '> Extracting forge'##################################################################################################
    zf = zipfile.ZipFile('forge.zip','r')
    zf.extractall()
    zf.close()
    ############################################################################################################################
    sys.path.append(os.path.join(_path_,'forge'))
    import install
    mcpf = os.path.join(_path_,'.api','Forge'+mcversion)
    if os.path.isdir(mcpf):
        shutil.rmtree(mcpf)
    install.main(mcpf)##########################################################################################################
    os.chdir(_path_)
    shutil.rmtree('forge')
    os.remove('forge.zip')
    print '> Editing eclipse workspace'#########################################################################################
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
    tree.getroot().insert(0,Element("classpathentry",
        {"kind":"lib","path":"lib/deobfMC.jar","sourcepath":"lib/deobfMC-src.jar"}))
    tree.write(cp)
    print '> Creating minecraft libraries'######################################################################################
    zip = zipfile.ZipFile(os.path.join(mcpf,"lib","deobfMC.jar"),"w",zipfile.ZIP_DEFLATED)
    bindir = os.path.join(mcpf,"bin","minecraft")+os.sep
    for dpath,dnames,fnames in os.walk(bindir):
        for fname in fnames:
            p = os.path.join(dpath,fname)
            zip.write(p,p.replace(bindir,""))
    zip.close()
    zip = zipfile.ZipFile(os.path.join(mcpf,"lib","deobfMC-src.jar"),"w",zipfile.ZIP_DEFLATED)
    srcdir = os.path.join(mcpf,"src","minecraft")+os.sep
    for dpath,dnames,fnames in os.walk(srcdir):
        for fname in fnames:
            p = os.path.join(dpath,fname)
            zip.write(p,p.replace(srcdir,""))
    zip.close()
    print '> Editing config file'###############################################################################################
    config = ConfigParser.SafeConfigParser()
    conffile = os.path.join(mcpf,'conf','mcp.cfg')
    config.read(conffile)
    config.set('OUTPUT','TestClient','dummy')
    confobj = open(conffile,'wb')
    config.write(confobj)
    confobj.close()
    print '> Creating dummy java file'##########################################################################################
    dummyjava = open(os.path.join(srcdir,'dummy.java'),'wb')
    dummyjava.write('public class dummy{}')
    dummyjava.close()
    return mcversion
def get_versions():
    versions = []
    for dir in os.listdir(os.path.join(_path_,'.api')):
        if not dir.startswith('Forge'):
            continue
        versions.append(dir.replace('Forge',''))
    if len(versions)==0:
        versions.append(install())
    versions = sorted(versions, cmp=cmp_version)
    return versions
def get_newest():
    return get_versions()[-1]
def i_eclipse(dir,version=None):
    from xml.etree.ElementTree import ElementTree,Element
    todir = os.path.join(_path_,dir)
    cf = os.path.join(todir,'build.cfg')
    if not os.path.isfile(cf):
        print dir+" doesn't have build.cfg. Create it!"
        return
    if version == None:
        version = get_newest()
    if not version in get_versions():
        print '> Minecraft version is invalid. Change to newest'
        version = get_newest()
    print '> Copying eclipse project files to '+dir
    config = ConfigParser.SafeConfigParser()
    config.read(cf)
    config.set('pj','mcv',version)
    cff = open(cf,'w')
    config.write(cff)
    cff.close()
    fromdir = os.path.join(_path_,'.api','Forge'+version,"eclipse","Minecraft")
    tree = ElementTree()
    tree.parse(os.path.join(fromdir,'.classpath'))
    for src in config.get('pj','src').split(':'):
        if src.endswith('/'):
            tree.getroot().append(Element("classpathentry",{"kind":"src","path":src[:-1]}))
        else:
            src = src.split('/')
            if len(src)==1:
                src = src[0]
            else:
                src = '/'.join(src[:-1])
            if src=='':
                src='.'
            tree.getroot().append(Element("classpathentry",{"kind":"src","path":src}))
    if config.has_option('pj','api'):
        for api in config.get('pj','api').split(':'):
            tree.getroot().append(Element('classpathentry',
                {'kind':'lib','path':'lib/'+api+'.jar','sourcepath':'lib/'+api+'-src.jar'}))
    tree.write(os.path.join(todir,'.classpath'))
    inputfile = open(os.path.join(fromdir,'.project'),'rb')
    filedata = inputfile.read()
    inputfile.close()
    filedata = filedata.replace('@PROJECT_NAME@',dir)
    outputfile = open(os.path.join(todir,'.project'),'wb')
    outputfile.write(filedata)
    outputfile.close()
def i_select(version=None,all=False):
    if version == None:
        version = get_newest()
    if not version in get_versions():
        print '> Minecraft version is invalid. Change to newest'
        version = get_newest()
    for dir in os.listdir(_path_):
        if dir.startswith('.'):
            continue
        if not os.path.isdir(os.path.join(_path_,dir)):
            continue
        if not os.path.isfile(os.path.join(_path_,dir,'build.cfg')):
            continue
        if all:
            i_eclipse(dir,version)
        else:
            while True:
                ret = raw_input(dir+' is MinecraftForge project[y/n]?')
                if ret[0] == 'y' or ret[0] == 'Y':
                    i_eclipse(dir,version)
                    break
                if ret[0] == 'n' or ret[0] == 'N':
                    break
def build(pname):
    starttime = time.time()
    pdir = os.path.join(_path_,pname)
    cf = os.path.join(pdir,'build.cfg')
    if not os.path.isfile(cf):
        print dir+" doesn't have build.cfg. Create it!"
        return
    config = ConfigParser.SafeConfigParser()
    config.read(cf)
    mversion = config.get('pj','version')
    fversion = ''
    if config.has_option('pj','mcv'):
        fversion = config.get('pj','mcv')
    if not fversion in get_versions():
        print '> Minecraft version is invalid. Change to newest'
        fversion = get_newest()
    if config.has_option('pj','out'):
        out = config.get('pj','out').replace('/',os.sep)
    else:
        out = os.path.join('dist',fversion,pname+'-'+mversion+'.zip')
    exfile = os.path.join(pdir,out)
    exdir = os.path.dirname(exfile)
    if not os.path.isdir(exdir):
        os.makedirs(exdir)
    mcpdir = os.path.join(_path_,'.api','Forge'+fversion)
    srces = []
    reses = []
    apies = []
    repes = {}
    repes['@VERSION@']=fversion
    srcdir = os.path.join(mcpdir,'src','minecraft')+os.sep
    bindir = os.path.join(mcpdir,'bin','minecraft')+os.sep
    reobfdir = os.path.join(mcpdir,'reobf','minecraft')+os.sep
    apidir = os.path.join(mcpdir,'lib')
    sys.path.insert(0,os.path.join(mcpdir,'runtime'))
    os.chdir(mcpdir)
    import commands,mcp
    cmd = commands.Commands()
    for dir in config.get('pj','src').replace('/',os.sep).split(':'):
        ndir = os.path.abspath(os.path.join(pdir,os.path.dirname(dir)))+os.sep
        dir = os.path.abspath(os.path.join(pdir,dir))
        cache = []
        for fpath, dnames, fnames in os.walk(dir):
            for fname in fnames:
                cache.append(os.path.join(fpath,fname).replace(ndir,''))
        tap = (ndir,cache)
        srces.append(tap)
    if config.has_option('pj','res'):
        for dir in config.get('pj','res').replace('/',os.sep).split(':'):
            ndir = os.path.abspath(os.path.join(pdir,os.path.dirname(dir)))+os.sep
            dir = os.path.abspath(os.path.join(pdir,dir))
            cache = []
            for fpath, dnames, fnames in os.walk(dir):
                for fname in fnames:
                    cache.append(os.path.join(fpath,fname).replace(ndir,''))
            tap = (ndir,cache)
            reses.append(tap)
    if config.has_option('pj','api'):
        for name in config.get('pj','api').replace('/',os.sep).split(':'):
            apies.append(name)
    if config.has_option('pj','rep'):
        for rep in config.get('pj','rep').split('|'):
            bef,aft=rep.split('=')
            repes[bef] = aft
    cmd.logger.info('> Cleaning directories')###################################################################################
    for path,dnames,fnames in os.walk(srcdir):
        for fname in fnames:
            os.remove(os.path.join(path,fname))
    dummyjava = open(os.path.join(srcdir,'dummy.java'),'wb')
    dummyjava.write('public class dummy{}')
    dummyjava.close()
    cmd.cleanbindirs(commands.CLIENT)
    cmd.logger.info('> Recompiling')############################################################################################
    cmd.recompile(commands.CLIENT)
    cmd.logger.info('> Extracting forge binaries')##############################################################################
    deobfjar = zipfile.ZipFile(os.path.join(apidir,'deobfMC.jar'),'r')
    for f in deobfjar.namelist():
        cache = os.path.join(bindir,f)
        if not os.path.exists(cache):
            if f.endswith('/'):
                os.mkdir(cache)
            else:
                deobfjar.extract(f,bindir)
    deobfjar.close()
    if len(apies) > 0:##########################################################################################################
        cmd.logger.info('> Extracting api binaries')
        for api in apies:
            zf = zipfile.ZipFile(os.path.join(apidir,api+'.jar'),'r')
            for f in zf.namelist():
                cache = os.path.join(bindir,f)
                if not os.path.exists(cache):
                    if f.endswith('/'):
                        os.mkdir(cache)
                    else:
                        zf.extract(f,bindir)
            zf.close()
    cmd.logger.info('> Generating md5s')########################################################################################
    cmd.gathermd5s(commands.CLIENT)
    cmd.logger.info('> Copying Mod sources')####################################################################################
    for base, list in srces:
        for src in list[:]:
            tofile = os.path.join(srcdir,src)
            fromfile = os.path.join(base,src)
            todir = os.path.dirname(tofile)
            if not os.path.isdir(todir):
                os.makedirs(todir)
            if isbinary(fromfile):
                shutil.copy2(fromfile,tofile)
            else:
                inputfile = open(fromfile,'rb')
                filedata = inputfile.read()
                inputfile.close()
                for repfrom,repto in repes.items():
                    filedata = filedata.replace(repfrom,repto)
                outputfile = open(tofile,'wb')
                outputfile.write(filedata)
                outputfile.close()
    cmd.logger.info('> Recompiling')############################################################################################
    cmd.recompile(commands.CLIENT)
    cmd.logger.info('> Creating Retroguard config files')#######################################################################
    cmd.creatergcfg(reobf=True)
    cmd.logger.info('> Reobfuscating')##########################################################################################
    mcp.reobfuscate_side(cmd,commands.CLIENT)
    cmd.logger.info('> Creating output ZipFile')################################################################################
    output = zipfile.ZipFile(exfile,'w',zipfile.ZIP_DEFLATED)
    for base,dnames,fnames in os.walk(reobfdir):
        for fname in fnames:
            cache = os.path.join(base,fname)
            output.write(cache,cache.replace(reobfdir,''))
    for base,list in reses:
        for res in list:
            cache = os.path.join(base,res)
            if isbinary(cache):
                output.write(cache,res)
            else:
                inputfile = open(cache,'rb')
                filedata = inputfile.read()
                inputfile.close()
                for repfrom,repto in repes.items():
                    filedata = filedata.replace(repfrom,repto)
                st = os.stat(cache)
                zinfo = zipfile.ZipInfo(res, time.localtime(st.st_mtime)[0:6])
                zinfo.external_attr = (st[0] & 0xFFFF) << 16L
                zinfo.compress_type = output.compression
                zinfo.flag_bits = 0x00
                output.writestr(zinfo,filedata)
    output.close()
    if config.has_option('pj','capif'):
        name = config.get('pj','capif')
        cmd.logger.info('> Cleaning bin directory')#############################################################################
        cmd.cleanbindirs(commands.CLIENT)
        cmd.logger.info('> Recompiling')########################################################################################
        cmd.recompile(commands.CLIENT)
        cmd.logger.info('> Creating libraries')#################################################################################
        lzip = zipfile.ZipFile(os.path.join(apidir,name+".jar"),"w",zipfile.ZIP_DEFLATED)
        for dpath,dnames,fnames in os.walk(bindir):
            for fname in fnames:
                p = os.path.join(dpath,fname)
                if not p==os.path.abspath(os.path.join(bindir,'dummy.class')):
                    lzip.write(p,p.replace(bindir,""))
        lzip.close()
        lzip = zipfile.ZipFile(os.path.join(apidir,name+"-src.jar"),"w",zipfile.ZIP_DEFLATED)
        for dpath,dnames,fnames in os.walk(srcdir):
            for fname in fnames:
                p = os.path.join(dpath,fname)
                if not p==os.path.abspath(os.path.join(srcdir,'dummy.java')):
                    lzip.write(p,p.replace(srcdir,""))
        lzip.close()
    cmd.logger.info('- All Done in %.2f seconds', time.time() - starttime)
    while len(logger.handlers) > 0:
        logger.removeHandler(logger.handlers[0])
def main(cur=None):
    if cur == None:
        cur = get_newest()
    while True:
        print '0. exit'
        print '1. build project (an project chosen by user) *current minecraft version is unavailable'
        print '2. update eclipse project file (all projects)'
        print '3. update eclipse project file (some projects chosen by user)'
        print '4. update eclipse project file (an project chosen by user)'
        print '5. install new minecraft forge'
        print '6. change minecraft version'
        print 'current minecraft version : '+cur
        input = raw_input('>')
        if input=='0':
            return
        elif input=='1':
            build(select_one())
        elif input=='2':
            i_select(cur,True)
        elif input=='3':
            i_select(cur)
        elif input=='4':
            i_eclipse(select_one())
        elif input=='5':
            cur = install()
        elif input=='6':
            while True:
                for v in get_versions():
                    print v
                input = raw_input('select new minecraft version: ')
                if input in get_versions():
                    cur = input
                    break
if __name__ == '__main__':
    main()