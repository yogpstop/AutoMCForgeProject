import os,sys,shutil,zipfile,time, copy
from ConfigParser import SafeConfigParser
_path_ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def isbinary(file):##text file contains only HT,LF,CR and basic characters
    f = open(file,"rb")
    for b in f.read():
        value = ord(b)
        if value < 9:
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
    cr = re.compile("[^0-9]")
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
        if dir.startswith("."):
            continue
        if not os.path.isdir(os.path.join(_path_,dir)):
            continue
        if not os.path.isfile(os.path.join(_path_,dir,"build.cfg")):
            continue
        dirs.append(dir)
    i = 0
    while(i<len(dirs)):
        print str(i)+" "+dirs[i]
        i+=1
    while True:
        num = raw_input("select target project: ")
        if num.isdigit():
            if int(num)<len(dirs):
                return dirs[int(num)]
def install():
    import urllib
    import re
    from xml.etree.ElementTree import ElementTree, Element
    forge_zip = os.path.join(_path_,"forge.zip")
    print "> Start forge install"###############################################################################################
    fl = urllib.urlopen("http://files.minecraftforge.net/").read().decode().splitlines()
    regax = re.compile("http://files.minecraftforge.net/minecraftforge/minecraftforge-src-([^-]*)-([^-]*).zip")
    builds = {}
    for build in fl:
        m = regax.search(build)
        if m:
            if cmp_version("4.0.0.188",m.group(2)) > 0:
                continue
            if not builds.has_key(m.group(1)):
                builds[m.group(1)] = {}
            builds[m.group(1)][m.group(2)]=m.group(0)
    ############################################################################################################################
    for m in sorted(builds.keys(), cmp=cmp_version):
        print m
    while True:
        mcversion = raw_input("select Minecraft version: ")
        if builds.has_key(mcversion):
            break
    ############################################################################################################################
    for build in sorted(builds[mcversion].keys(), cmp=cmp_version):
        print build
    done = False
    while True:
        bnum = raw_input("select Forge build: ")
        for build in builds[mcversion].keys():
            if build==bnum or build.split(".")[-1]==bnum:
                urllib.urlretrieve(builds[mcversion][build],forge_zip)
                done = True
                break
        if done:
            break
    print "> Extracting forge"##################################################################################################
    zf = zipfile.ZipFile(forge_zip,"r")
    zf.extractall(_path_)
    zf.close()
    ############################################################################################################################
    forge_dir = os.path.join(_path_,"forge")
    fml_dir = os.path.join(forge_dir,"fml")
    mcp_dir = os.path.join(_path_,".api","Forge"+mcversion+"-"+build)
    if os.path.isdir(mcp_dir):
        shutil.rmtree(mcp_dir)
    sys.path.append(fml_dir)
    sys.path.append(forge_dir)
    import forge,fml
    print "> Forge ModLoader Setup Start"
    try:
        fml.download_mcp(fml_dir=fml_dir,mcp_dir=mcp_dir)
    except Exception:
        pass
    fml.setup_mcp(fml_dir=fml_dir, mcp_dir=mcp_dir)
    os.chdir(mcp_dir)
    config = SafeConfigParser()
    conffile = os.path.join(mcp_dir,"conf","mcp.cfg")
    config.read(conffile)
    src_dir = os.path.join(mcp_dir,config.get("DEFAULT","DirSrc"))
    if not os.path.isdir(os.path.join(os.environ["HOME"],".minecraft")):
        os.symlink(os.path.join(mcp_dir,config.get("DEFAULT","DirJars")),os.path.join(os.environ["HOME"],".minecraft"))
        symblink=True
    else:
        symlink=False
    try:
        fml.setup_fml(fml_dir=fml_dir, mcp_dir=mcp_dir)
    except Exception:
        fml.decompile_minecraft(fml_dir=fml_dir,mcp_dir=mcp_dir)
    fml.apply_fml_patches(fml_dir=fml_dir, mcp_dir=mcp_dir, src_dir=src_dir)
    fml.finish_setup_fml(fml_dir=fml_dir, mcp_dir=mcp_dir)
    print "> Forge ModLoader Setup End"
    sys.path.append(mcp_dir)
    from runtime.mcp import updatenames_side,updatemd5_side
    from runtime.commands import Commands,CLIENT,SERVER
    print "> Minecraft Forge Setup Start"
    cmd = Commands()
    print "> Applying forge patches"
    forge.apply_forge_patches(fml_dir=fml_dir, mcp_dir=mcp_dir, forge_dir=forge_dir, src_dir=src_dir)
    if os.path.isdir(os.path.join(mcp_dir,os.path.normpath(config.get("OUTPUT","srcclient")))):
        updatenames_side(cmd,CLIENT)
        updatemd5_side(cmd,CLIENT)
    if os.path.isdir(os.path.join(mcp_dir,os.path.normpath(config.get("OUTPUT","srcserver")))):
        updatenames_side(cmd,SERVER)
        updatemd5_side(cmd,SERVER)
    fml.reset_logger()
    print "> Minecraft Forge Setup Finished"
    shutil.rmtree(forge_dir)
    os.remove(forge_zip)
    if symblink:
        os.remove(os.path.join(os.environ["HOME"],".minecraft"))
    print "> Editing eclipse workspace"#########################################################################################
    #----------Initialize Directories
    mcploc = "$%7BWORKSPACE_LOC%7D/.api/Forge"+mcversion+"-"+build
    basedir = os.path.join(mcp_dir,config.get("DEFAULT","DirEclipse"))
    dbg=os.path.join(basedir,".metadata",".plugins","org.eclipse.debug.core",".launches")
    #----------.project Fixes
    tree = ElementTree()
    pj=os.path.join(basedir,"Minecraft",".project")
    tree.parse(pj)
    linkedResources = tree.find("linkedResources")
    common_src_dir = os.path.join(src_dir,"common")+os.sep
    common_src_dir_exist = os.path.isdir(common_src_dir)
    for link in linkedResources.findall("link")[:]:
        name = link.findtext("name")
        if name == "src" or name == "common":
            linkedResources.remove(link)
    for vari in tree.find("variableList").findall("variable"):
        if vari.findtext("name") == "MCP_LOC":
            vari.find("value").text = mcploc
            break
    tree.find("name").text = "@PROJECT_NAME@"
    tree.write(pj)
    #---------.classpath Fixes
    tree = ElementTree()
    cp=os.path.join(basedir,"Minecraft",".classpath")
    tree.parse(cp)
    for cpe in tree.getroot().findall("classpathentry")[:]:
        path = cpe.get("path")
        if path == "src" or path == "common":
            tree.getroot().remove(cpe)
    tree.getroot().insert(0,Element("classpathentry",
        {"kind":"lib","path":"lib/deobfMC.jar","sourcepath":"lib/deobfMC-src.jar"}))
    tree.write(cp)
    #----------Client.launch Fixes
    tree = ElementTree()
    tree.parse(os.path.join(dbg,"Client.launch"))
    for cache in tree.getroot().findall("listAttribute"):
        if cache.get("key") == "org.eclipse.debug.core.MAPPED_RESOURCE_PATHS":
            for cache2 in cache.findall("listEntry"):
                if cache2.get("value").endswith(".java"):
                    cache2.set("value","/@PROJECT_NAME@/lib/deobfMC.jar")
            break
    for cache in tree.getroot().findall("stringAttribute"):
        if cache.get("key") == "org.eclipse.jdt.launching.PROJECT_ATTR":
            cache.set("value","@PROJECT_NAME@")
        if cache.get("key") == "org.eclipse.jdt.launching.WORKING_DIRECTORY":
            cache.set("value","${workspace_loc:@PROJECT_NAME@/jars}")
    tree.write(os.path.join(dbg,"Client.launch"))
    #----------Server.launch Fixes
    tree = ElementTree()
    tree.parse(os.path.join(dbg,"Server.launch"))
    for cache in tree.getroot().findall("listAttribute"):
        if cache.get("key") == "org.eclipse.debug.core.MAPPED_RESOURCE_PATHS":
            for cache2 in cache.findall("listEntry"):
                if cache2.get("value").endswith(".java"):
                    cache2.set("value","/@PROJECT_NAME@/lib/deobfMC.jar")
            break
    for cache in tree.getroot().findall("stringAttribute"):
        if cache.get("key") == "org.eclipse.jdt.launching.PROJECT_ATTR":
            cache.set("value","@PROJECT_NAME@")
        if cache.get("key") == "org.eclipse.jdt.launching.WORKING_DIRECTORY":
            cache.set("value","${workspace_loc:@PROJECT_NAME@/jars}")
    tree.write(os.path.join(dbg,"Server.launch"))
    print "> Creating minecraft libraries"######################################################################################
    lib_dir = os.path.join(mcp_dir,config.get("DEFAULT","DirLib"))
    cl_bin_dir = os.path.join(mcp_dir,os.path.normpath(config.get("RECOMPILE","binclient")))+os.sep
    cl_src_dir = os.path.join(mcp_dir,os.path.normpath(config.get("OUTPUT","srcclient")))+os.sep
    zip = zipfile.ZipFile(os.path.join(lib_dir,"deobfMC.jar"),"w",zipfile.ZIP_DEFLATED)
    for dpath,dnames,fnames in os.walk(cl_bin_dir):
        for fname in fnames:
            p = os.path.join(dpath,fname)
            zip.write(p,p.replace(cl_bin_dir,""))
    for dpath,dnames,fnames in os.walk(cl_src_dir):
        for fname in fnames:
            if fname.endswith(".java"):
                continue
            p = os.path.join(dpath,fname)
            zip.write(p,p.replace(cl_src_dir,""))
    if common_src_dir_exist:
        for dpath,dnames,fnames in os.walk(common_src_dir):
            for fname in fnames:
                if fname.endswith(".java"):
                    continue
                p = os.path.join(dpath,fname)
                zip.write(p,p.replace(common_src_dir,""))
    zip.close()
    zip = zipfile.ZipFile(os.path.join(lib_dir,"deobfMC-src.jar"),"w",zipfile.ZIP_DEFLATED)
    for dpath,dnames,fnames in os.walk(cl_src_dir):
        for fname in fnames:
            p = os.path.join(dpath,fname)
            zip.write(p,p.replace(cl_src_dir,""))
    if common_src_dir_exist:
        for dpath,dnames,fnames in os.walk(common_src_dir):
            for fname in fnames:
                p = os.path.join(dpath,fname)
                zip.write(p,p.replace(common_src_dir,""))
    zip.close()
    print "> Editing config file"###############################################################################################
    config.set("OUTPUT","TestClient","dummy")
    confobj = open(conffile,"wb")
    config.write(confobj)
    confobj.close()
    return mcversion
def get_versions():
    versions = []
    for dir in os.listdir(os.path.join(_path_,".api")):
        if not dir.startswith("Forge"):
            continue
        versions.append(dir.replace("Forge",""))
    if len(versions)==0:
        versions.append(install())
    versions = sorted(versions, cmp=cmp_version)
    return versions
def get_newest():
    return get_versions()[-1]
def i_eclipse(dir,version=""):
    from xml.etree.ElementTree import ElementTree,Element
    todir = os.path.join(_path_,dir)
    cf = os.path.join(todir,"build.cfg")
    if not os.path.isfile(cf):
        print dir+" doesn't have build.cfg. Create it!"
        return
    if not version in get_versions():
        print "> Minecraft version is invalid. Change to newest"
        version = get_newest()
    print "> Copying eclipse project files to "+dir
    #-----build.cfg Fixes
    config = SafeConfigParser()
    config.read(cf)
    config.set("pj","mcv",version)
    cff = open(cf,"w")
    config.write(cff)
    cff.close()
    #-----InitializeDirectories
    fromdir = os.path.join(_path_,".api","Forge"+version,"eclipse")
    l_fromdir = os.path.join(fromdir,".metadata",".plugins","org.eclipse.debug.core",".launches")
    l_todir = os.path.join(_path_,".metadata",".plugins","org.eclipse.debug.core",".launches")
    if not os.path.isdir(targetDir):
        os.makedirs(targetDir)
    #-----.classpath File
    tree = ElementTree()
    tree.parse(os.path.join(fromdir,"Minecraft",".classpath"))
    for src in config.get("pj","src").split(":"):
        if src.endswith("/"):
            tree.getroot().append(Element("classpathentry",{"kind":"src","path":src[:-1]}))
        else:
            point = src.rfind("/")
            if point == -1:
                bsrc = ""
                nsrc = src
            else:
                bsrc = src[:point]
                nsrc = src[point+1:]+"/"
            tree.getroot().append(Element("classpathentry",{"kind":"src","path":bsrc,"including":nsrc}))
    if config.has_option("pj","api"):
        for api in config.get("pj","api").split(":"):
            tree.getroot().append(Element("classpathentry",
                {"kind":"lib","path":"lib/"+api+".jar","sourcepath":"lib/"+api+"-src.jar"}))
    tree.write(os.path.join(todir,".classpath"))
    #-----.project File
    inputfile = open(os.path.join(fromdir,"Minecraft",".project"),"rb")
    filedata = inputfile.read()
    inputfile.close()
    outputfile = open(os.path.join(todir,".project"),"wb")
    outputfile.write(filedata.replace("@PROJECT_NAME@",dir))
    outputfile.close()
    #-----ClientBootFile
    inputfile = open(os.path.join(l_fromdir,"Client.launch"),"rb")
    filedata = inputfile.read()
    inputfile.close()
    outputfile = open(os.path.join(l_todir,dir+"Client.launch"),"wb")
    outputfile.write(filedata.replace("@PROJECT_NAME@",dir))
    outputfile.close()
    #-----ServerBootFile
    inputfile = open(os.path.join(l_fromdir,"Server.launch"),"rb")
    filedata = inputfile.read()
    inputfile.close()
    outputfile = open(os.path.join(l_todir,dir+"Server.launch"),"wb")
    outputfile.write(filedata.replace("@PROJECT_NAME@",dir))
    outputfile.close()
def i_select(version=None,all=False):
    if version == None:
        version = get_newest()
    if not version in get_versions():
        print "> Minecraft version is invalid. Change to newest"
        version = get_newest()
    for dir in os.listdir(_path_):
        if dir.startswith("."):
            continue
        if not os.path.isdir(os.path.join(_path_,dir)):
            continue
        if not os.path.isfile(os.path.join(_path_,dir,"build.cfg")):
            continue
        if all:
            i_eclipse(dir,version)
        else:
            while True:
                ret = raw_input(dir+" is MinecraftForge project[y/n]?")
                if ret[0] == "y" or ret[0] == "Y":
                    i_eclipse(dir,version)
                    break
                if ret[0] == "n" or ret[0] == "N":
                    break
def build(pname):
    starttime = time.time()
    pj_dir = os.path.join(_path_,pname)
    cf = os.path.join(pj_dir,"build.cfg")
    if not os.path.isfile(cf):
        print dir+" doesn't have build.cfg. Create it!"
        return
    config = SafeConfigParser()
    config.read(cf)
    fversion = ""
    if config.has_option("pj","mcv"):
        fversion = config.get("pj","mcv")
    if not fversion in get_versions():
        print "> Minecraft version is invalid. Change to newest"
        fversion = get_newest()
    mcp_dir = os.path.join(_path_,".api","Forge"+fversion)
    mcp_cfg_file = os.path.join(mcp_dir,"conf","mcp.cfg")
    mcp_cfg = SafeConfigParser()
    mcp_cfg.read(mcp_cfg_file)
    src_dir = os.path.join(mcp_dir,mcp_cfg.get("DEFAULT","DirSrc"))
    _temp_ = os.path.join(mcp_dir,os.path.normpath(mcp_cfg.get("OUTPUT","SrcClient")))+os.sep
    if os.path.isdir(os.path.join(src_dir,"common")):
        src_dir = os.path.join(src_dir,"common")+os.sep
        cl_src_dir = _temp_
    else:
        src_dir = _temp_
    bin_dir = os.path.join(mcp_dir,os.path.normpath(mcp_cfg.get("RECOMPILE","BinClient")))+os.sep
    reobf_dir = os.path.join(mcp_dir,os.path.normpath(mcp_cfg.get("REOBF","ReobfDirClient")))+os.sep
    lib_dir = os.path.join(mcp_dir,mcp_cfg.get("DEFAULT","DirLib"))
    sys.path.insert(0,os.path.join(mcp_dir,mcp_cfg.get("DEFAULT","DirRuntime")))

    mversion = config.get("pj","version")
    if config.has_option("pj","out"):
        out = config.get("pj","out").replace("/",os.sep)
    else:
        out = os.path.join("dist",fversion.replace("-",os.sep),pname+"-"+mversion+".zip")
    exfile = os.path.join(pj_dir,out)
    exdir = os.path.dirname(exfile)
    if not os.path.isdir(exdir):
        os.makedirs(exdir)
    srces = []
    reses = []
    apies = []
    repes = {}
    repes["@VERSION@"]=mversion
    repes["@MCVERSION@"]=fversion.split("-")[0]
    repes["@FORGEVERSION@"]=fversion.split("-")[1]
    repes["@FORGEBUILD@"]=fversion.split(".")[-1]
    os.chdir(mcp_dir)
    if not os.path.isdir(os.path.join(os.environ["HOME"],".minecraft")):
        os.symlink(os.path.join(mcp_dir,mcp_cfg.get("DEFAULT","DirJars")),os.path.join(os.environ["HOME"],".minecraft"))
        symblink=True
    else:
        symblink=False
    import commands,mcp
    cmd = commands.Commands()
    for dir in config.get("pj","src").replace("/",os.sep).split(":"):
        ndir = os.path.abspath(os.path.join(pj_dir,os.path.dirname(dir)))+os.sep
        dir = os.path.abspath(os.path.join(pj_dir,dir))
        cache = []
        res_cache = []
        for fpath, dnames, fnames in os.walk(dir):
            for fname in fnames:
                if fname.endswith(".java"):
                    cache.append(os.path.join(fpath,fname).replace(ndir,""))
                else:
                    res_cache.append(os.path.join(fpath,fname).replace(ndir,""))
        if len(cache) > 0:
            tap = (ndir,cache)
            srces.append(tap)
        if len(res_cache) > 0:
            tap = (ndir,res_cache)
            reses.append(tap)
    if config.has_option("pj","res"):
        for dir in config.get("pj","res").replace("/",os.sep).split(":"):
            ndir = os.path.abspath(os.path.join(pj_dir,os.path.dirname(dir)))+os.sep
            dir = os.path.abspath(os.path.join(pj_dir,dir))
            cache = []
            for fpath, dnames, fnames in os.walk(dir):
                for fname in fnames:
                    cache.append(os.path.join(fpath,fname).replace(ndir,""))
            tap = (ndir,cache)
            reses.append(tap)
    if config.has_option("pj","api"):
        for name in config.get("pj","api").replace("/",os.sep).split(":"):
            apies.append(name)
    if config.has_option("pj","rep"):
        for rep in config.get("pj","rep").split("|"):
            bef,aft=rep.split("=")
            repes[bef] = aft
    srg = False
    if config.has_option("pj","srg"):
        srg = config.getboolean("pj","srg")
    cmd.logger.info("> Cleaning directories")###################################################################################
    for path,dnames,fnames in os.walk(src_dir):
        for fname in fnames:
            os.remove(os.path.join(path,fname))
    try:
        for path,dnames,fnames in os.walk(cl_src_dir):
            for fname in fnames:
                os.remove(os.path.join(path,fname))
    except NameError:
        pass
    dummyjava = open(os.path.join(src_dir,"dummy.java"),"wb")
    dummyjava.write("public class dummy{}")
    dummyjava.close()
    cmd.cleanbindirs(commands.CLIENT)
    cmd.logger.info("> Recompiling")############################################################################################
    cmd.recompile(commands.CLIENT)
    cmd.logger.info("> Extracting forge binaries")##############################################################################
    deobfjar = zipfile.ZipFile(os.path.join(lib_dir,"deobfMC.jar"),"r")
    for f in deobfjar.namelist():
        cache = os.path.join(bin_dir,f)
        if not os.path.exists(cache):
            if f.endswith("/"):
                os.mkdir(cache)
            else:
                if f.endswith(".class"):
                    deobfjar.extract(f,bin_dir)
    deobfjar.close()
    if len(apies) > 0:##########################################################################################################
        cmd.logger.info("> Extracting api binaries")
        for api in apies:
            zf = zipfile.ZipFile(os.path.join(lib_dir,api+".jar"),"r")
            for f in zf.namelist():
                cache = os.path.join(bin_dir,f)
                if not os.path.exists(cache):
                    if f.endswith("/"):
                        os.mkdir(cache)
                    else:
                        if f.endswith(".class"):
                            zf.extract(f,bin_dir)
            zf.close()
    cmd.logger.info("> Generating md5s")########################################################################################
    cmd.gathermd5s(commands.CLIENT)
    cmd.logger.info("> Copying Mod sources")####################################################################################
    for base, list in srces:
        for src in list[:]:
            tofile = os.path.join(src_dir,src)
            fromfile = os.path.join(base,src)
            todir = os.path.dirname(tofile)
            if not os.path.isdir(todir):
                os.makedirs(todir)
            if isbinary(fromfile):
                shutil.copy2(fromfile,tofile)
            else:
                inputfile = open(fromfile,"rb")
                filedata = inputfile.read()
                inputfile.close()
                for repfrom,repto in repes.items():
                    filedata = filedata.replace(repfrom,repto)
                outputfile = open(tofile,"wb")
                outputfile.write(filedata)
                outputfile.close()
    cmd.logger.info("> Recompiling")############################################################################################
    cmd.recompile(commands.CLIENT)
    cmd.logger.info("> Creating Retroguard config files")#######################################################################
    if srg:
        cmd.createreobfsrg()
        cmd.creatergcfg(reobf=True, srg_names=True)
    else:
        cmd.creatergcfg(reobf=True)
    cmd.logger.info("> Reobfuscating")##########################################################################################
    if srg:
        mcp.reobfuscate_side(cmd,commands.CLIENT,srg_names=True)
    else:
        mcp.reobfuscate_side(cmd,commands.CLIENT)
    cmd.logger.info("> Creating output ZipFile")################################################################################
    output = zipfile.ZipFile(exfile,"w",zipfile.ZIP_DEFLATED)
    for base,dnames,fnames in os.walk(reobf_dir):
        for fname in fnames:
            cache = os.path.join(base,fname)
            output.write(cache,cache.replace(reobf_dir,""))
    for base,list in reses:
        for res in list:
            cache = os.path.join(base,res)
            if isbinary(cache):
                output.write(cache,res)
            else:
                inputfile = open(cache,"rb")
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
    if config.has_option("pj","capif"):
        name = config.get("pj","capif")
        cmd.logger.info("> Cleaning bin directory")#############################################################################
        cmd.cleanbindirs(commands.CLIENT)
        cmd.logger.info("> Recompiling")########################################################################################
        cmd.recompile(commands.CLIENT)
        cmd.logger.info("> Creating libraries")#################################################################################
        lzip = zipfile.ZipFile(os.path.join(lib_dir,name+".jar"),"w",zipfile.ZIP_DEFLATED)
        for dpath,dnames,fnames in os.walk(bin_dir):
            for fname in fnames:
                p = os.path.join(dpath,fname)
                if not p==os.path.abspath(os.path.join(bin_dir,"dummy.class")):
                    lzip.write(p,p.replace(bin_dir,""))
        for base,list in reses:
            for res in list:
                cache = os.path.join(base,res)
                if isbinary(cache):
                    lzip.write(cache,res)
                else:
                    inputfile = open(cache,"rb")
                    filedata = inputfile.read()
                    inputfile.close()
                    for repfrom,repto in repes.items():
                        filedata = filedata.replace(repfrom,repto)
                    st = os.stat(cache)
                    zinfo = zipfile.ZipInfo(res, time.localtime(st.st_mtime)[0:6])
                    zinfo.external_attr = (st[0] & 0xFFFF) << 16L
                    zinfo.compress_type = lzip.compression
                    zinfo.flag_bits = 0x00
                    lzip.writestr(zinfo,filedata)
        lzip.close()
        lzip = zipfile.ZipFile(os.path.join(lib_dir,name+"-src.jar"),"w",zipfile.ZIP_DEFLATED)
        for dpath,dnames,fnames in os.walk(src_dir):
            for fname in fnames:
                p = os.path.join(dpath,fname)
                if not p==os.path.abspath(os.path.join(src_dir,"dummy.java")):
                    lzip.write(p,p.replace(src_dir,""))
        lzip.close()
    if symblink:
        os.remove(os.path.join(os.environ["HOME"],".minecraft"))
    cmd.logger.info("- All Done in %.2f seconds", time.time() - starttime)
    import logging
    logger = logging.getLogger()
    while len(logger.handlers) > 0:
        logger.removeHandler(logger.handlers[0])
def main(cur=None):
    if cur == None:
        cur = get_newest()
    while True:
        print "0. exit"
        print "1. build project (an project chosen by user) *current minecraft version is ignored"
        print "2. update eclipse project file (all projects)"
        print "3. update eclipse project file (some projects chosen by user)"
        print "4. update eclipse project file (an project chosen by user)"
        print "5. install new minecraft forge"
        print "6. change minecraft version"
        print "current minecraft version : "+cur
        input = raw_input(">")
        if input=="0":
            return
        elif input=="1":
            build(select_one())
        elif input=="2":
            i_select(cur,True)
        elif input=="3":
            i_select(cur)
        elif input=="4":
            i_eclipse(select_one(),cur)
        elif input=="5":
            cur = install()
        elif input=="6":
            while True:
                for v in get_versions():
                    print v
                input = raw_input("select new minecraft version: ")
                for version in get_versions():
                    if version==input or version.split(".")[-1]==input:
                        cur = version
                        done = True
                        break
                if done:
                    break
if __name__ == "__main__":
    main()