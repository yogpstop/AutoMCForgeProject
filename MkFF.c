#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
const char buildxml1[] = "<project name=\"";
const char buildxml2[] = "\" default=\"main\">\n"
		"	<property name=\"mod.version\" value=\"";
const char buildxml3[] = "\" />\n"
		"\n"
		"	<property name=\"mc.version\" value=\"";
const char buildxml4[] = "\" />\n"
		"	<property name=\"forge.version\" value=\"";
const char buildxml5[] =
		"\" />\n"
				"	<property name=\"src.dir\" value=\"src\" />\n"
				"	<property name=\"res.dir\" value=\"res\" />\n"
				"	<property name=\"jar.dir\" value=\"dist\" />\n"
				"	<property name=\"mcp.dir\" value=\"../.api/mcp-${mc.version}-${forge.version}\" />\n"
				"	<property name=\"reobf.dir\" value=\"${mcp.dir}/reobf/minecraft\" />\n"
				"	<property name=\"mcpsrc.dir\" value=\"${mcp.dir}/src/minecraft\" />\n"
				"	<property name=\"mcpsrc.dir.concrete\" value=\"${mcpsrc.dir}/org/yogpstop\" />\n"
				"	<property name=\"jar.path\" value=\"${jar.dir}/${mc.version}/${ant.project.name}-${mod.version}.jar\" />\n"
				"\n"
				"	<target name=\"clean\">\n"
				"		<delete dir=\"${mcpsrc.dir.concrete}\" />\n"
				"	</target>\n"
				"\n"
				"	<target name=\"copysource\" depends=\"clean\">\n"
				"		<copy todir=\"${mcpsrc.dir}\">\n"
				"			<fileset dir=\"${src.dir}\" />\n"
				"			<filterset>\n"
				"				<filter token=\"VERSION\" value=\"${mod.version}\" />\n"
				"			</filterset>\n"
				"		</copy>\n"
				"	</target>\n"
				"\n"
				"	<target name=\"compile\" depends=\"copysource\">\n"
				"\n"
				"		<exec dir=\"${mcp.dir}\" executable=\"cmd\" osfamily=\"windows\">\n"
				"			<arg line=\"/c recompile.bat\" />\n"
				"		</exec>\n"
				"		<exec dir=\"${mcp.dir}\" executable=\"sh\" osfamily=\"unix\">\n"
				"			<arg value=\"recompile.sh\" />\n"
				"		</exec>\n"
				"		<exec dir=\"${mcp.dir}\" executable=\"cmd\" osfamily=\"windows\">\n"
				"			<arg line=\"/c reobfuscate.bat\" />\n"
				"		</exec>\n"
				"		<exec dir=\"${mcp.dir}\" executable=\"sh\" osfamily=\"unix\">\n"
				"			<arg value=\"reobfuscate.sh\" />\n"
				"		</exec>\n"
				"	</target>\n"
				"\n"
				"	<target name=\"package\" depends=\"compile\">\n"
				"		<jar destfile=\"${jar.path}\">\n"
				"			<fileset dir=\"${reobf.dir}\" />\n"
				"			<fileset dir=\"${res.dir}\" />\n";
const char buildxml6[] = "\n"
		"		</jar>\n"
		"		<antcall target=\"clean\" />\n"
		"	</target>\n"
		"\n"
		"	<target name=\"main\" depends=\"package\" />\n"
		"</project>\n";
const char gitignore[] = "/dist\n/bin\n.*";
const char modvstr[] = "mod.version\" value=\"";
const char manifestSt[] = "<manifest";
const char manifestEnd[] = "</manifest>";
const char cp[] = "<classpathentry kind=\"src\" path=\"src\"/>";
const char proj11[] = ".linkedResourceslink.name";
const char proj12[] = "src";
const char proj21[] = ".variableList.variable.name";
const char proj22[] = "MCP_LOC";
const char proj23[] = ".variableList.variable.value";
char* getModv(const char* buildxml) {
	register const char* search = modvstr;
	do {
		if (*buildxml == *search) {
			while (1)
				if (*++buildxml != *++search)
					break;
			if (*search == '\0')
				break;
			search = modvstr;
		}
	} while (*++buildxml);
	register int pos = 0;
	while (*++buildxml != '"')
		pos++;
	char* modv = malloc(pos + 1);
	modv += pos;
	*modv = '\0';
	for (buildxml--; *buildxml != '"'; buildxml--)
		*--modv = *buildxml;
	return modv;
}
char* getManifest(const char* buildxml) {
	register const char* search = manifestSt;
	do {
		if (*buildxml == *search) {
			while (1)
				if (*++buildxml != *++search)
					break;
			if (*search == '\0')
				break;
			search = manifestSt;
		}
	} while (*++buildxml);
	if (*buildxml == '\0')
		return "";
	register int pos = 9;
	search = manifestEnd;
	do {
		pos++;
		if (*buildxml == *search) {
			while (1) {
				pos++;
				if (*++buildxml != *++search)
					break;
			}
			if (*search == '\0')
				break;
			search = manifestEnd;
		}
	} while (*++buildxml);
	char* manifest = malloc(pos + 1);
	manifest += pos;
	*manifest = '\0';
	for (buildxml--, pos--; pos > 0; pos--)
		*--manifest = *buildxml--;
	return manifest;
}
int main(void) {
	register char *cpa, *cpa2;
	register const char *cpb, *cpb2;
	register int i, j;
	register char cc;
	FILE *fp;

	char mcv[16] = { }, forgev[64] = { };

	ina: fputs("Type MinecraftVersion less than 15 characters>", stdout);
	cpa = mcv;
	i = 0;
	fflush(stdin);
	while ((cc = getc(stdin))) {
		if (i > 0 && (cc == 0x08 || cc == 0x7f)) {
			*--cpa = '\0';
			i--;
			continue;
		}
		if (cc < 0x20 || i > 15)
			break;
		*cpa++ = cc;
		i++;
	}
	if (i == 0 || i > 15) {
		for (i = 0; i < 16; i++)
			mcv[i] = '\0';
		goto ina;
	}
	inb: fputs("Type MinecraftForgeVersion less than 63 characters>", stdout);
	cpa = forgev;
	i = 0;
	fflush(stdin);
	while ((cc = getc(stdin))) {
		if (i > 0 && (cc == 0x08 || cc == 0x7f)) {
			*--cpa = '\0';
			i--;
			continue;
		}
		if (cc < 0x20 || i > 63)
			break;
		*cpa++ = cc;
		i++;
	}
	if (i == 0 || i > 63) {
		for (i = 0; i < 64; i++)
			forgev[i] = '\0';
		goto inb;
	}
	char sfn[40 + strlen(mcv) + strlen(forgev)];
	cpa = sfn;
	*cpa++ = '.';
	*cpa++ = 'a';
	*cpa++ = 'p';
	*cpa++ = 'i';
	*cpa++ = '/';
	*cpa++ = 'm';
	*cpa++ = 'c';
	*cpa++ = 'p';
	*cpa++ = '-';
	for (cpb = mcv; *cpb; cpb++, cpa++)
		*cpa = *cpb;
	*cpa++ = '-';
	for (cpb = forgev; *cpb; cpb++, cpa++)
		*cpa = *cpb;
	*cpa++ = '/';
	*cpa++ = 'e';
	*cpa++ = 'c';
	*cpa++ = 'l';
	*cpa++ = 'i';
	*cpa++ = 'p';
	*cpa++ = 's';
	*cpa++ = 'e';
	*cpa++ = '/';
	*cpa++ = 'M';
	*cpa++ = 'i';
	*cpa++ = 'n';
	*cpa++ = 'e';
	*cpa++ = 'c';
	*cpa++ = 'r';
	*cpa++ = 'a';
	*cpa++ = 'f';
	*cpa++ = 't';
	char* const targetp = cpa;
	*cpa++ = '/';
	*cpa++ = '.';
	*cpa++ = 'c';
	*cpa++ = 'l';
	*cpa++ = 'a';
	*cpa++ = 's';
	*cpa++ = 's';
	*cpa++ = 'p';
	*cpa++ = 'a';
	*cpa++ = 't';
	*cpa++ = 'h';
	*cpa = '\0';
	fp = fopen(sfn, "r");
	if (fp == NULL ) {
		printf("%s is not found. check version and directories.", sfn);
		return EXIT_FAILURE;
	}
	fseek(fp, 0, SEEK_END);
	char* const classpath = malloc(ftell(fp) + 44);
	fseek(fp, 0, SEEK_SET);
	cpb = cp;
	cpa = classpath;
	while ((cc = fgetc(fp)) != -1) {
		*cpa++ = cc;
		if (cc == *cpb) {
			while ((cc = fgetc(fp)) != -1) {
				*cpa++ = cc;
				if (cc != *++cpb)
					break;
			}
			if (*cpb == '\0') {
				*cpa++ = '\t';
				*cpa++ = '<';
				*cpa++ = 'c';
				*cpa++ = 'l';
				*cpa++ = 'a';
				*cpa++ = 's';
				*cpa++ = 's';
				*cpa++ = 'p';
				*cpa++ = 'a';
				*cpa++ = 't';
				*cpa++ = 'h';
				*cpa++ = 'e';
				*cpa++ = 'n';
				*cpa++ = 't';
				*cpa++ = 'r';
				*cpa++ = 'y';
				*cpa++ = ' ';
				*cpa++ = 'k';
				*cpa++ = 'i';
				*cpa++ = 'n';
				*cpa++ = 'd';
				*cpa++ = '=';
				*cpa++ = '"';
				*cpa++ = 's';
				*cpa++ = 'r';
				*cpa++ = 'c';
				*cpa++ = '"';
				*cpa++ = ' ';
				*cpa++ = 'p';
				*cpa++ = 'a';
				*cpa++ = 't';
				*cpa++ = 'h';
				*cpa++ = '=';
				*cpa++ = '"';
				*cpa++ = 'm';
				*cpa++ = 'c';
				*cpa++ = 's';
				*cpa++ = 'r';
				*cpa++ = 'c';
				*cpa++ = '"';
				*cpa++ = '/';
				*cpa++ = '>';
				*cpa++ = '\n';
				break;
			}
			cpb = cp;
		}
	}
	while ((cc = fgetc(fp)) != -1)
		*cpa++ = cc;
	*cpa = '\0';
	fclose(fp);
	cpa = targetp;
	*cpa++ = '/';
	*cpa++ = '.';
	*cpa++ = 'p';
	*cpa++ = 'r';
	*cpa++ = 'o';
	*cpa++ = 'j';
	*cpa++ = 'e';
	*cpa++ = 'c';
	*cpa++ = 't';
	*cpa = '\0';
	fp = fopen(sfn, "r");
	char project1[96] = { };
	fseek(fp, 0, SEEK_END);
	char* const project2 = malloc(ftell(fp));
	fseek(fp, 0, SEEK_SET);
	char class[128] = { };
	cpa = project1;
	cpa2 = class;
	while ((cc = fgetc(fp)) != -1) {
		*cpa++ = cc;
		if (cc == '?') {
			cc = fgetc(fp);
			*cpa++ = cc;
			if (cc == '>')
				break;
		}
	}
	while ((cc = fgetc(fp)) != -1) {
		*cpa++ = cc;
		if (cc == '>')
			break;
	}
	while ((cc = fgetc(fp)) != -1) {
		*cpa++ = cc;
		if (cc == '<') {
			cc = fgetc(fp);
			*cpa++ = cc;
			if (cc != 'n')
				continue;
			cc = fgetc(fp);
			*cpa++ = cc;
			if (cc != 'a')
				continue;
			cc = fgetc(fp);
			*cpa++ = cc;
			if (cc != 'm')
				continue;
			cc = fgetc(fp);
			*cpa++ = cc;
			if (cc != 'e')
				continue;
			cc = fgetc(fp);
			*cpa++ = cc;
			if (cc != '>')
				continue;
			cpa = project2;
			break;
		}
	}
	while ((cc = fgetc(fp)) != -1) {
		if (cc == '<')
			break;
	}
	*cpa++ = cc;
	while ((cc = fgetc(fp)) != -1) {
		*cpa++ = cc;
		if (cc == '<') {
			cc = fgetc(fp);
			*cpa++ = cc;
			if (cc == '/') {
				while (*cpa2 != '.')
					*cpa2-- = '\0';
				*cpa2 = '\0';
			} else {
				*cpa2++ = '.';
				*cpa2++ = cc;
				while ((cc = fgetc(fp)) != '>') {
					*cpa++ = cc;
					*cpa2++ = cc;
				}
				*cpa++ = cc;
				cpb = proj11;
				cpb2 = class;
				while (*cpb++ == *cpb2++ && *cpb != '\0')
					;
				if (*cpb == '\0') {
					cc = fgetc(fp);
					*cpa++ = cc;
					if (cc != 's')
						continue;
					cc = fgetc(fp);
					*cpa++ = cc;
					if (cc != 'r')
						continue;
					cc = fgetc(fp);
					*cpa++ = cc;
					if (cc != 'c')
						continue;
					cc = fgetc(fp);
					*cpa++ = cc;
					if (cc != '<')
						continue;
					while (*--cpa != '>')
						;
					cpa++;
					*cpa++ = 'm';
					*cpa++ = 'c';
					*cpa++ = 's';
					*cpa++ = 'r';
					*cpa++ = 'c';
					*cpa++ = '<';
					break;
				}
			}
		}
	}
	while ((cc = fgetc(fp)) != -1) {
		*cpa++ = cc;
		if (cc == '<') {
			cc = fgetc(fp);
			*cpa++ = cc;
			if (cc == '/') {
				while (*cpa2 != '.')
					*cpa2-- = '\0';
				*cpa2 = '\0';
			} else {
				*cpa2++ = '.';
				*cpa2++ = cc;
				while ((cc = fgetc(fp)) != '>') {
					*cpa++ = cc;
					*cpa2++ = cc;
				}
				*cpa++ = cc;
				cpb = proj21;
				cpb2 = class;
				while (*cpb++ == *cpb2++ && *cpb != '\0')
					;
				if (*cpb == '\0') {
					cc = fgetc(fp);
					*cpa++ = cc;
					if (cc != 'M')
						continue;
					cc = fgetc(fp);
					*cpa++ = cc;
					if (cc != 'C')
						continue;
					cc = fgetc(fp);
					*cpa++ = cc;
					if (cc != 'P')
						continue;
					cc = fgetc(fp);
					*cpa++ = cc;
					if (cc != '_')
						continue;
					cc = fgetc(fp);
					*cpa++ = cc;
					if (cc != 'L')
						continue;
					cc = fgetc(fp);
					*cpa++ = cc;
					if (cc != 'O')
						continue;
					cc = fgetc(fp);
					*cpa++ = cc;
					if (cc != 'C')
						continue;
					cc = fgetc(fp);
					*cpa++ = cc;
					if (cc != '<')
						continue;
					break;
				}
			}
		}
	}
	while ((cc = fgetc(fp)) != -1) {
		*cpa++ = cc;
		if (cc == '<') {
			cc = fgetc(fp);
			*cpa++ = cc;
			if (cc == '/') {
				while (*cpa2 != '.')
					*cpa2-- = '\0';
				*cpa2 = '\0';
			} else {
				*cpa2++ = '.';
				*cpa2++ = cc;
				while ((cc = fgetc(fp)) != '>') {
					*cpa++ = cc;
					*cpa2++ = cc;
				}
				*cpa++ = cc;
				cpb = proj23;
				cpb2 = class;
				while (*cpb++ == *cpb2++ && *cpb != '\0')
					;
				if (*cpb == '\0') {
					*cpa++ = '$';
					*cpa++ = '%';
					*cpa++ = '7';
					*cpa++ = 'B';
					*cpa++ = 'W';
					*cpa++ = 'O';
					*cpa++ = 'R';
					*cpa++ = 'K';
					*cpa++ = 'S';
					*cpa++ = 'P';
					*cpa++ = 'A';
					*cpa++ = 'C';
					*cpa++ = 'E';
					*cpa++ = '_';
					*cpa++ = 'L';
					*cpa++ = 'O';
					*cpa++ = 'C';
					*cpa++ = '%';
					*cpa++ = '7';
					*cpa++ = 'D';
					*cpa++ = '/';
					*cpa++ = '.';
					*cpa++ = 'a';
					*cpa++ = 'p';
					*cpa++ = 'i';
					*cpa++ = '/';
					*cpa++ = 'm';
					*cpa++ = 'c';
					*cpa++ = 'p';
					*cpa++ = '-';
					for (cpb = mcv; *cpb; cpb++, cpa++)
						*cpa = *cpb;
					*cpa++ = '-';
					for (cpb = forgev; *cpb; cpb++, cpa++)
						*cpa = *cpb;
					while ((cc = fgetc(fp)) != '<')
						;
					*cpa++ = cc;
					break;
				}
			}
		}
	}
	while ((cc = fgetc(fp)) != -1)
		*cpa++ = cc;
	*cpa = '\0';
	fclose(fp);
	DIR *dp = opendir("./");
	struct dirent *dir;
	char *modv, *manifest;
	struct stat s;
	while ((dir = readdir(dp))) {
		stat(dir->d_name, &s);
		if (!(s.st_mode & S_IFDIR) || dir->d_name[0] == '.')
			continue;
		j = strlen(dir->d_name);
		char fn[j + 12];
		for (cpb = dir->d_name, cpa = fn; *cpb; cpb++, cpa++)
			*cpa = *cpb;
		*cpa++ = '/';
		*cpa++ = 'b';
		*cpa++ = 'u';
		*cpa++ = 'i';
		*cpa++ = 'l';
		*cpa++ = 'd';
		*cpa++ = '.';
		*cpa++ = 'x';
		*cpa++ = 'm';
		*cpa++ = 'l';
		*cpa = '\0';
		fp = fopen(fn, "r");
		if (fp == NULL ) {
			modv = "1.0.0";
			manifest = "";
		} else {
			fseek(fp, 0, SEEK_END);
			char* const buildxml = malloc(ftell(fp) + 1);
			fseek(fp, 0, SEEK_SET);
			cpa = buildxml;
			while ((cc = fgetc(fp)) != -1)
				*cpa++ = cc;
			*cpa = '\0';
			modv = getModv(buildxml);
			manifest = getManifest(buildxml);
			fclose(fp);
			free(buildxml);
		}
		fp = fopen(fn, "w");
		fputs(buildxml1, fp);
		fputs(dir->d_name, fp);
		fputs(buildxml2, fp);
		fputs(modv, fp);
		fputs(buildxml3, fp);
		fputs(mcv, fp);
		fputs(buildxml4, fp);
		fputs(forgev, fp);
		fputs(buildxml5, fp);
		fputs(manifest, fp);
		fputs(buildxml6, fp);
		fclose(fp);
		cpa = &fn[j];
		*cpa++ = '/';
		*cpa++ = '.';
		*cpa++ = 'g';
		*cpa++ = 'i';
		*cpa++ = 't';
		*cpa++ = 'i';
		*cpa++ = 'g';
		*cpa++ = 'n';
		*cpa++ = 'o';
		*cpa++ = 'r';
		*cpa++ = 'e';
		*cpa = '\0';
		fp = fopen(fn, "w");
		fputs(gitignore, fp);
		fclose(fp);
		cpa = &fn[j];
		*cpa++ = '/';
		*cpa++ = '.';
		*cpa++ = 'c';
		*cpa++ = 'l';
		*cpa++ = 'a';
		*cpa++ = 's';
		*cpa++ = 's';
		*cpa++ = 'p';
		*cpa++ = 'a';
		*cpa++ = 't';
		*cpa++ = 'h';
		*cpa = '\0';
		fp = fopen(fn, "w");
		fputs(classpath, fp);
		fclose(fp);
		cpa = &fn[j];
		*cpa++ = '/';
		*cpa++ = '.';
		*cpa++ = 'p';
		*cpa++ = 'r';
		*cpa++ = 'o';
		*cpa++ = 'j';
		*cpa++ = 'e';
		*cpa++ = 'c';
		*cpa++ = 't';
		*cpa = '\0';
		fp = fopen(fn, "w");
		fputs(project1, fp);
		fputs(dir->d_name, fp);
		fputs(project2, fp);
		fclose(fp);
	}
	free(classpath);
	free(project2);
	return 0;
}
