# Copyright (C) 2012,2013 yogpstop
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the
# GNU Lesser General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.

import os, sys, shutil, zipfile, time, copy, re, urllib, logging, subprocess, argparse
from ConfigParser import SafeConfigParser
from xml.etree.ElementTree import ElementTree, Element
from xml.etree.ElementTree import tostring as TreeToStr
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
	cr = re.compile("[^0-9]")
	sa = cr.split(a)
	salen = len(sa)
	sb = cr.split(b)
	sblen = len(sb)
	i = 0
	while True:
		if i >= salen:
			if not (i >= sblen):
				return -1-int(sb[i])
			return 0
		if i >= sblen:
			return 1+int(sa[i])
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
				print "> Downloading MinecraftForge"
				urllib.urlretrieve(builds[mcversion][build],forge_zip)
				done = True
				break
		if done:
			break
	print "> Extracting MinecraftForge"#########################################################################################
	zf = zipfile.ZipFile(forge_zip,"r")
	zf.extractall(_path_)
	zf.close()
	os.remove(forge_zip)
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
		fml.download_mcp(fml_dir=fml_dir, mcp_dir=mcp_dir)
	except Exception:
		pass
	try:
		fml.setup_mcp(fml_dir=fml_dir, mcp_dir=mcp_dir, gen_conf=False)
	except Exception:
		fml.setup_mcp(fml_dir=fml_dir, mcp_dir=mcp_dir, dont_gen_conf=True)
	try:
		fml.setup_fml(fml_dir=fml_dir, mcp_dir=mcp_dir)
	except Exception:
		fml.decompile_minecraft(fml_dir=fml_dir, mcp_dir=mcp_dir)
	src_dir = os.path.join(mcp_dir,"src")
	fml.apply_fml_patches(fml_dir=fml_dir, mcp_dir=mcp_dir, src_dir=src_dir)
	fml.finish_setup_fml(fml_dir=fml_dir, mcp_dir=mcp_dir)
	print "> Forge ModLoader Setup End"
	print "> Minecraft Forge Setup Start"
	print "> Applying forge patches"
	forge.apply_forge_patches(fml_dir=fml_dir, mcp_dir=mcp_dir, forge_dir=forge_dir, src_dir=src_dir)
	config = SafeConfigParser()
	conffile = os.path.join(mcp_dir,"conf","mcp.cfg")
	conffilep = open(conffile, "rb")
	config.readfp(conffilep)
	conffilep.close()
	sys.path.append(mcp_dir)
	os.chdir(mcp_dir)
	from runtime.mcp import updatenames_side,updatemd5_side,recompile_side
	from runtime.commands import Commands,CLIENT,SERVER
	cmd = Commands()
	if os.path.isdir(os.path.join(mcp_dir,os.path.normpath(config.get("OUTPUT","srcclient")))):
		updatenames_side(cmd,CLIENT)
		updatemd5_side(cmd,CLIENT)
		recompile_side(cmd,CLIENT)
	if os.path.isdir(os.path.join(mcp_dir,os.path.normpath(config.get("OUTPUT","srcserver")))):
		updatenames_side(cmd,SERVER)
		updatemd5_side(cmd,SERVER)
		recompile_side(cmd,SERVER)
	fml.reset_logger()
	print "> Minecraft Forge Setup Finished"
	shutil.rmtree(forge_dir)
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
	common_src_dir = os.path.join(src_dir,"common")
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
	outputfile = open(cp,"wb")
	outputfile.write(TreeToStr(tree.getroot()).replace("Minecraft/","@PROJECT_NAME@/"))
	outputfile.close()
	#----------Client.launch Fixes
	tree = ElementTree()
	tree.parse(os.path.join(dbg,"Client.launch"))
	for cache in tree.getroot().findall("listAttribute"):
		if cache.get("key") == "org.eclipse.debug.core.MAPPED_RESOURCE_PATHS":
			for cache2 in cache.findall("listEntry"):
				if cache2.get("value").endswith(".java"):
					cache2.set("value","/@PROJECT_NAME@/lib/deobfMC.jar")
				if cache2.get("value").startswith("/Minecraft/"):
					cache2.set("value",cache2.get("value").replace("/Minecraft/","/@PROJECT_NAME@/",1))
			break
	for cache in tree.getroot().findall("stringAttribute"):
		if cache.get("key") == "org.eclipse.jdt.launching.PROJECT_ATTR":
			cache.set("value","@PROJECT_NAME@")
		if cache.get("key") == "org.eclipse.jdt.launching.WORKING_DIRECTORY":
			cache.set("value","${workspace_loc:@PROJECT_NAME@/jars}")
		if cache.get("key") == "org.eclipse.jdt.launching.VM_ARGUMENTS":
			cache.set("value",cache.get("value")+" -Dfml.ignoreInvalidMinecraftCertificates=true")
	tree.write(os.path.join(dbg,"Client.launch"))
	#----------Server.launch Fixes
	tree = ElementTree()
	tree.parse(os.path.join(dbg,"Server.launch"))
	for cache in tree.getroot().findall("listAttribute"):
		if cache.get("key") == "org.eclipse.debug.core.MAPPED_RESOURCE_PATHS":
			for cache2 in cache.findall("listEntry"):
				if cache2.get("value").endswith(".java"):
					cache2.set("value","/@PROJECT_NAME@/lib/deobfMC.jar")
				if cache2.get("value").startswith("/Minecraft/"):
					cache2.set("value",cache2.get("value").replace("/Minecraft/","/@PROJECT_NAME@/",1))
			break
	for cache in tree.getroot().findall("stringAttribute"):
		if cache.get("key") == "org.eclipse.jdt.launching.PROJECT_ATTR":
			cache.set("value","@PROJECT_NAME@")
		if cache.get("key") == "org.eclipse.jdt.launching.WORKING_DIRECTORY":
			cache.set("value","${workspace_loc:@PROJECT_NAME@/jars}")
	tree.write(os.path.join(dbg,"Server.launch"))
	print "> Creating minecraft libraries"######################################################################################
	lib_dir = os.path.join(mcp_dir,config.get("DEFAULT","DirLib"))
	cl_bin_dir = os.path.join(mcp_dir,os.path.normpath(config.get("RECOMPILE","binclient")))
	cl_src_dir = os.path.join(mcp_dir,os.path.normpath(config.get("OUTPUT","srcclient")))
	cdir = os.path.join(os.path.join(lib_dir,"deobfMC"))
	cdirs = os.path.join(os.path.join(lib_dir,"deobfMC-src"))
	shutil.rmtree(cdir,True)
	shutil.rmtree(cdirs,True)
	for dpath,dnames,fnames in os.walk(cl_bin_dir):
		for fname in fnames:
			p = os.path.join(dpath,fname)
			zp = os.path.join(cdir,os.path.relpath(p,cl_bin_dir))
			dzp = os.path.dirname(zp)
			if not os.path.isdir(dzp):
				os.makedirs(dzp)
			shutil.copy2(p,zp)
	for dpath,dnames,fnames in os.walk(cl_src_dir):
		for fname in fnames:
			p = os.path.join(dpath,fname)
			zp = os.path.join(cdirs,os.path.relpath(p,cl_src_dir))
			dzp = os.path.dirname(zp)
			if not os.path.isdir(dzp):
				os.makedirs(dzp)
			shutil.copy2(p,zp)
			if fname.endswith(".java"):
				continue
			zp = os.path.join(cdir,os.path.relpath(p,cl_src_dir))
			dzp = os.path.dirname(zp)
			if not os.path.isdir(dzp):
				os.makedirs(dzp)
			shutil.copy2(p,zp)
	if common_src_dir_exist:
		for dpath,dnames,fnames in os.walk(common_src_dir):
			for fname in fnames:
				p = os.path.join(dpath,fname)
				zp = os.path.join(cdirs,os.path.relpath(p,common_src_dir))
				dzp = os.path.dirname(zp)
				if not os.path.isdir(dzp):
					os.makedirs(dzp)
				shutil.copy2(p,zp)
				if fname.endswith(".java"):
					continue
				zp = os.path.join(cdir,os.path.relpath(p,common_src_dir))
				dzp = os.path.dirname(zp)
				if not os.path.isdir(dzp):
					os.makedirs(dzp)
				shutil.copy2(p,zp)
	subprocess.check_call(["jar","cf",os.path.join(lib_dir,"deobfMC.jar"),"-C",cdir,"."])
	subprocess.check_call(["jar","cf",os.path.join(lib_dir,"deobfMC-src.jar"),"-C",cdirs,"."])
	shutil.rmtree(cdir)
	shutil.rmtree(cdirs)
	print "> Editing config file"###############################################################################################
	config.set("OUTPUT","TestClient","dummy")
	confobj = open(conffile,"wb")
	config.write(confobj)
	confobj.close()
	return mcversion+"-"+build
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
	cff = open(cf,"rb")
	config.readfp(cff)
	cff.close()
	config.set("pj","mcv",version)
	cff = open(cf,"wb")
	config.write(cff)
	cff.close()
	#-----InitializeDirectories
	fromdir = os.path.join(_path_,".api","Forge"+version,"eclipse")
	l_fromdir = os.path.join(fromdir,".metadata",".plugins","org.eclipse.debug.core",".launches")
	l_todir = os.path.join(_path_,".metadata",".plugins","org.eclipse.debug.core",".launches")
	if not os.path.isdir(l_todir):
		os.makedirs(l_todir)
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
			done = False
			for entry in tree.getroot().findall("classpathentry"):
				if entry.get("kind") == "src" and entry.get("path") == bsrc:
					entry.set("including",entry.get("including")+"|"+nsrc)
					done = True
			if not done:
				tree.getroot().append(Element("classpathentry",{"kind":"src","path":bsrc,"including":nsrc}))
	if config.has_option("pj","res"):
		for src in config.get("pj","res").split(":"):
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
				done = False
				for entry in tree.getroot().findall("classpathentry"):
					if entry.get("kind") == "src" and entry.get("path") == bsrc:
						entry.set("including",entry.get("including")+"|"+nsrc)
						done = True
				if not done:
					tree.getroot().append(Element("classpathentry",{"kind":"src","path":bsrc,"including":nsrc}))
	if config.has_option("pj","api"):
		for api in config.get("pj","api").split(":"):
			tree.getroot().append(Element("classpathentry",
				{"kind":"lib","path":"lib/"+api+".jar","sourcepath":"lib/"+api+"-src.jar"}))
	outputfile = open(os.path.join(todir,".classpath"),"wb")
	outputfile.write(TreeToStr(tree.getroot()).replace("@PROJECT_NAME@",dir))
	outputfile.close()
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
	pj_cfg_f = os.path.join(pj_dir,"build.cfg")
	if not os.path.isfile(pj_cfg_f):
		print dir+" doesn't have build.cfg. Create it!"
		return
	pj_cfg = SafeConfigParser()
	pj_cfg_fp = open(pj_cfg_f, "rb")
	pj_cfg.readfp(pj_cfg_fp)
	pj_cfg_fp.close()
	if pj_cfg.has_option("pj","mcv"):
		forge_v = pj_cfg.get("pj","mcv")
	else:
		forge_v = ""
	if not forge_v in get_versions():
		print "> Minecraft version is invalid. Change to newest"
		forge_v = get_newest()
	mcp_dir = os.path.join(_path_,".api","Forge"+forge_v)
	mcp_cfg_f = os.path.join(mcp_dir,"conf","mcp.cfg")
	mcp_cfg = SafeConfigParser()
	mcp_cfg_fp = open(mcp_cfg_f, "rb")
	mcp_cfg.readfp(mcp_cfg_fp)
	mcp_cfg_fp.close()
	mcp_src_dir = os.path.join(mcp_dir,mcp_cfg.get("DEFAULT","DirSrc"))
	_temp_ = os.path.join(mcp_dir,os.path.normpath(mcp_cfg.get("OUTPUT","SrcClient")))
	if os.path.isdir(os.path.join(mcp_src_dir,"common")):
		mcp_src_dir = os.path.join(mcp_src_dir,"common")
		mcp_cl_src_dir = _temp_
	else:
		mcp_src_dir = _temp_
	mcp_bin_dir = os.path.join(mcp_dir,os.path.normpath(mcp_cfg.get("RECOMPILE","BinClient")))
	mcp_reobf_dir = os.path.join(mcp_dir,os.path.normpath(mcp_cfg.get("REOBF","ReobfDirClient")))
	mcp_lib_dir = os.path.join(mcp_dir,mcp_cfg.get("DEFAULT","DirLib"))
	mod_v = pj_cfg.get("pj","version")
	# Output File
	if pj_cfg.has_option("pj","out"):
		pj_out_f = os.path.join(pj_dir,pj_cfg.get("pj","out").replace("/",os.sep))
	else:
		pj_out_f = os.path.join(pj_dir,"dist",forge_v.replace("-",os.sep),pname+"-"+forge_v.split("-")[0]+"-"+mod_v+".zip")
	pj_out_dir = os.path.dirname(pj_out_f)
	if not os.path.isdir(pj_out_dir):
		os.makedirs(pj_out_dir)
	srces = []
	reses = []
	apies = []
	repes = {}
	repes["@VERSION@"]=mod_v
	repes["@MCVERSION@"]=forge_v.split("-")[0]
	repes["@MC_VERSION@"]=forge_v.split("-")[0]
	repes["@FORGEVERSION@"]=forge_v.split("-")[1]
	repes["@FORGE_VERSION@"]=forge_v.split("-")[1]
	repes["@FORGEBUILD@"]=forge_v.split(".")[-1]
	repes["@FORGE_BUILD@"]=forge_v.split(".")[-1]
	os.chdir(mcp_dir)
	sys.path.append(mcp_dir)
	from runtime.mcp import reobfuscate_side
	from runtime.commands import Commands,CLIENT,SERVER
	cmd = Commands()
	for dir in pj_cfg.get("pj","src").replace("/",os.sep).split(":"):
		ndir = os.path.abspath(os.path.join(pj_dir,os.path.dirname(dir)))
		dir = os.path.abspath(os.path.join(pj_dir,dir))
		cache = []
		res_cache = []
		for fpath, dnames, fnames in os.walk(dir):
			for fname in fnames:
				if fname.endswith(".java"):
					cache.append(os.path.relpath(os.path.join(fpath,fname),ndir))
				else:
					res_cache.append(os.path.relpath(os.path.join(fpath,fname),ndir))
		if len(cache) > 0:
			tap = (ndir,cache)
			srces.append(tap)
		if len(res_cache) > 0:
			tap = (ndir,res_cache)
			reses.append(tap)
	if pj_cfg.has_option("pj","res"):
		for dir in pj_cfg.get("pj","res").replace("/",os.sep).split(":"):
			ndir = os.path.abspath(os.path.join(pj_dir,os.path.dirname(dir)))
			dir = os.path.abspath(os.path.join(pj_dir,dir))
			cache = []
			if os.path.isfile(dir):
				cache.append(os.path.relpath(dir,ndir))
			elif os.path.isdir(dir):
				for fpath, dnames, fnames in os.walk(dir):
					for fname in fnames:
						cache.append(os.path.relpath(os.path.join(fpath,fname),ndir))
			tap = (ndir,cache)
			reses.append(tap)
	if pj_cfg.has_option("pj","api"):
		for name in pj_cfg.get("pj","api").replace("/",os.sep).split(":"):
			apies.append(name)
	if pj_cfg.has_option("pj","rep"):
		for rep in pj_cfg.get("pj","rep").split("|"):
			bef,aft=rep.split("=")
			repes[bef] = aft
	for repfrom,repto in repes.items():
		pj_out_f = pj_out_f.replace(repfrom,repto)
	srg = False
	if pj_cfg.has_option("pj","srg"):
		srg = pj_cfg.getboolean("pj","srg")
	cmd.logger.info("> Cleaning directories")###################################################################################
	for path,dnames,fnames in os.walk(mcp_src_dir):
		for fname in fnames:
			os.remove(os.path.join(path,fname))
	try:
		for path,dnames,fnames in os.walk(mcp_cl_src_dir):
			for fname in fnames:
				os.remove(os.path.join(path,fname))
	except NameError:
		pass
	dummyjava = open(os.path.join(mcp_src_dir,"dummy.java"),"wb")
	dummyjava.write("class dummy{}")
	dummyjava.close()
	cmd.cleanbindirs(CLIENT)
	cmd.logger.info("> Recompiling")############################################################################################
	cmd.recompile(CLIENT)
	cmd.logger.info("> Extracting forge binaries")##############################################################################
	deobfjar = zipfile.ZipFile(os.path.join(mcp_lib_dir,"deobfMC.jar"),"r")
	for file in deobfjar.namelist():
		cache = os.path.join(mcp_bin_dir,file)
		if not os.path.exists(cache):
			if file.endswith("/"):
				os.mkdir(cache)
			else:
				if file.endswith(".class"):
					deobfjar.extract(file,mcp_bin_dir)
	deobfjar.close()
	if len(apies) > 0:##########################################################################################################
		cmd.logger.info("> Extracting api binaries")
		for api in apies:
			zf = zipfile.ZipFile(os.path.join(mcp_lib_dir,api+".jar"),"r")
			for file in zf.namelist():
				cache = os.path.join(mcp_bin_dir,file)
				if not os.path.exists(cache):
					if file.endswith(".class"):
						todir = os.path.dirname(os.path.join(mcp_bin_dir,file))
						if not os.path.exists(todir):
							os.makedirs(todir)
						zf.extract(file,mcp_bin_dir)
			zf.close()
	cmd.logger.info("> Generating md5s")########################################################################################
	cmd.gathermd5s(CLIENT)
	cmd.logger.info("> Copying Mod sources")####################################################################################
	for base, list in srces:
		for src in list:
			tofile = os.path.join(mcp_src_dir,src)
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
	cmd.recompile(CLIENT)
	cmd.logger.info("> Creating Retroguard config files")#######################################################################
	if srg:
		try:
			cmd.createreobfsrg()
			cmd.creatergcfg(reobf=True, srg_names=True)
		except Exception:
			srg=False; 
	if not srg:
		cmd.creatergcfg(reobf=True)
	cmd.logger.info("> Reobfuscating")##########################################################################################
	if srg:
		reobfuscate_side(cmd,CLIENT,srg_names=True)
	else:
		reobfuscate_side(cmd,CLIENT)
	cmd.logger.info("> Creating output ZipFile")################################################################################
	cdir = pj_out_f+".c"
	shutil.rmtree(cdir,True)
	os.makedirs(cdir)
	for base,dnames,fnames in os.walk(mcp_reobf_dir):
		for fname in fnames:
			p = os.path.join(base,fname)
			zp = os.path.join(cdir,os.path.relpath(p,mcp_reobf_dir))
			dzp = os.path.dirname(zp)
			if not os.path.isdir(dzp):
				os.makedirs(dzp)
			shutil.copy2(p,zp)
	for base,list in reses:
		for res in list:
			p = os.path.join(base,res)
			zp = os.path.join(cdir,res)
			dzp = os.path.dirname(zp)
			if not os.path.isdir(dzp):
				os.makedirs(dzp)
			shutil.copy2(p,zp)
			if not isbinary(p):
				fobj = open(zp,"rb")
				filedata = fobj.read()
				fobj.close()
				for repfrom,repto in repes.items():
					filedata = filedata.replace(repfrom,repto)
				fobj = open(zp,"wb")
				fobj.write(filedata)
				fobj.close()
	call = ["jar"]
	if pj_cfg.has_option("pj","man"):
		inputfile = open(os.path.join(pj_dir, pj_cfg.get("pj","man").replace("/",os.sep)),"rb")
		tofile = pj_out_f+".man"
		filedata = inputfile.read()
		inputfile.close()
		for repfrom,repto in repes.items():
			filedata = filedata.replace(repfrom,repto)
		outputfile = open(tofile,"wb")
		outputfile.write(filedata)
		outputfile.close()
		call.extend(["cmf",tofile])
	else:
		call.extend(["cf"])
	call.extend([pj_out_f,"-C",cdir,"."])
	subprocess.check_call(call)
	shutil.rmtree(cdir)
	if pj_cfg.has_option("pj","man"):
		os.remove(tofile)
	if pj_cfg.has_option("pj","capif"):
		api_lib_f = pj_cfg.get("pj","capif")
		cmd.logger.info("> Cleaning bin directory")#############################################################################
		cmd.cleanbindirs(CLIENT)
		cmd.logger.info("> Recompiling")########################################################################################
		cmd.recompile(CLIENT)
		cmd.logger.info("> Creating libraries")#################################################################################
		cdir = os.path.join(mcp_lib_dir,api_lib_f)
		shutil.rmtree(cdir,True)
		os.makedirs(cdir)
		for dpath,dnames,fnames in os.walk(mcp_bin_dir):
			for fname in fnames:
				p = os.path.join(dpath,fname)
				if not p==os.path.abspath(os.path.join(mcp_bin_dir,"dummy.class")):
					zp = os.path.join(cdir,os.path.relpath(p,mcp_bin_dir))
					dzp = os.path.dirname(zp)
					if not os.path.isdir(dzp):
						os.makedirs(dzp)
					shutil.copy2(p,zp)
		for base,list in reses:
			for res in list:
				p = os.path.join(base,res)
				zp = os.path.join(cdir,res)
				dzp = os.path.dirname(zp)
				if not os.path.isdir(dzp):
					os.makedirs(dzp)
				shutil.copy2(p,zp)
				if not isbinary(p):
					fobj = open(zp,"rb")
					filedata = fobj.read()
					fobj.close()
					for repfrom,repto in repes.items():
						filedata = filedata.replace(repfrom,repto)
					fobj = open(zp,"wb")
					fobj.write(filedata)
					fobj.close()
		subprocess.check_call(["jar","cf",cdir+".jar","-C",cdir,"."])
		shutil.rmtree(cdir)
		os.makedirs(cdir)
		for dpath,dnames,fnames in os.walk(mcp_src_dir):
			for fname in fnames:
				p = os.path.join(dpath,fname)
				if not p==os.path.abspath(os.path.join(mcp_src_dir,"dummy.java")):
					zp = os.path.join(cdir,os.path.relpath(p,mcp_src_dir))
					dzp = os.path.dirname(zp)
					if not os.path.isdir(dzp):
						os.makedirs(dzp)
					shutil.copy2(p,zp)
		subprocess.check_call(["jar","cf",cdir+"-src.jar","-C",cdir,"."])
		shutil.rmtree(cdir)
	cmd.logger.info("- All Done in %.2f seconds", time.time() - starttime)
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
	parser = argparse.ArgumentParser(description="Auto MinecraftForge Project Assembler and Builder")
	parser.add_argument("-b", "--build",metavar="ProjectName", help="Build selected project")
	args = parser.parse_args()
	if args.build is None:
		main()
	else:
		build(args.build)
