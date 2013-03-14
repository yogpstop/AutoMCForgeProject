#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <sys/stat.h>
const char gitignore[] = "/dist\n/bin\n.*";
const char cp[] = "<classpath>";
const char proj11[] = ".linkedResources.link.name";
const char proj12[] = "src";
const char proj21[] = ".variableList.variable.name";
const char proj22[] = "MCP_LOC";
const char proj23[] = ".variableList.variable.value";
int main(void) {
	register char *cpa, *cpa2;
	register const char *cpb, *cpb2;
	register int i, j;
	register char cc;
	FILE *fp;
	char *classpath, *project2;
	struct dirent *dir;
	struct stat s;
	char mcv[16] = { }, layer[128] = { }, project1[96] = { };
	// char[] sfn, fn

	/* get minecraft version */
	ina: fputs("Type MinecraftVersion less than 15 characters>", stdout);
	cpa = mcv;
	i = 0;
	fflush(stdin);
	while ((cc = getc(stdin)))
	{
		if (i > 0 && (cc == 0x08 || cc == 0x7f))
		{
			*--cpa = 0;
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
			mcv[i] = 0;
		goto ina;
	}
	j = i;
	/* find forge folder and open .classpath */
	char sfn[40 + i + j];
	cpa = sfn;
	*cpa++ = '.';
	*cpa++ = 'a';
	*cpa++ = 'p';
	*cpa++ = 'i';
	*cpa++ = '/';
	*cpa++ = 'M';
	*cpa++ = 'C';
	*cpa++ = 'P';
	for (cpb = mcv; *cpb; cpb++, cpa++)
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
	cpa2 = cpa;
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
	*cpa = 0;
	fp = fopen(sfn, "rb");
	if (fp == NULL ) {
		printf("%s is not found. check version and directories.", sfn);
		return EXIT_FAILURE;
	}
	/* read classpath with add entry */
	fseek(fp, 0, SEEK_END);
	classpath = malloc(ftell(fp) + 44);
	fseek(fp, 0, SEEK_SET);
	cpb = cp;
	cpa = classpath;
	while ((cc = fgetc(fp)) != EOF) {
		*cpa++ = cc;
		if (cc == *cpb) {
			while ((cc = fgetc(fp)) != EOF) {
				*cpa++ = cc;
				if (cc != *++cpb)
					break;
			}
			if (*cpb == 0) {
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
	while ((cc = fgetc(fp)) != EOF)
		*cpa++ = cc;
	*cpa = 0;
	fclose(fp);
	/* open .project and read that with some fix. */
	cpa = cpa2;
	*cpa++ = '/';
	*cpa++ = '.';
	*cpa++ = 'p';
	*cpa++ = 'r';
	*cpa++ = 'o';
	*cpa++ = 'j';
	*cpa++ = 'e';
	*cpa++ = 'c';
	*cpa++ = 't';
	*cpa = 0;
	fp = fopen(sfn, "rb");
	fseek(fp, 0, SEEK_END);
	project2 = malloc(ftell(fp));
	fseek(fp, 0, SEEK_SET);
	cpa = project1;
	cpa2 = layer;
	while ((cc = fgetc(fp)) != EOF) {
		*cpa++ = cc;
		if (cc == '?') {
			cc = fgetc(fp);
			*cpa++ = cc;
			if (cc == '>')
				break;
		}
	}
	while ((cc = fgetc(fp)) != EOF) {
		*cpa++ = cc;
		if (cc == '>')
			break;
	}
	while ((cc = fgetc(fp)) != EOF) {
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
			*cpa = 0;
			cpa = project2;
			break;
		}
	}
	while ((cc = fgetc(fp)) != EOF) {
		if (cc == '<')
			break;
	}
	*cpa++ = cc;
	while ((cc = fgetc(fp)) != EOF) {
		*cpa++ = cc;
		if (cc == '<') {
			cc = fgetc(fp);
			*cpa++ = cc;
			if (cc == '/') {
				while (*cpa2 != '.' && cpa2 > layer)
					cpa2--;
				*cpa2 = 0;
			} else {
				*cpa2++ = '.';
				*cpa2++ = cc;
				while ((cc = fgetc(fp)) != '>') {
					*cpa++ = cc;
					*cpa2++ = cc;
				}
				*cpa2 = 0;
				*cpa++ = cc;
				cpb = proj11;
				cpb2 = layer;
				while (*cpb++ == *cpb2++ && *cpb != 0)
					;
				if (*cpb == 0) {
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
	while (*cpa2 != '.' && cpa2 > layer)
		cpa2--;
	*cpa2 = 0;
	while ((cc = fgetc(fp)) != EOF) {
		*cpa++ = cc;
		if (cc == '<') {
			cc = fgetc(fp);
			*cpa++ = cc;
			if (cc == '/') {
				while (*cpa2 != '.' && cpa2 > layer)
					cpa2--;
				*cpa2 = 0;
			} else {
				*cpa2++ = '.';
				*cpa2++ = cc;
				while ((cc = fgetc(fp)) != '>') {
					*cpa++ = cc;
					*cpa2++ = cc;
				}
				*cpa2 = 0;
				*cpa++ = cc;
				cpb = proj21;
				cpb2 = layer;
				while (*cpb++ == *cpb2++ && *cpb != 0)
					;
				if (*cpb == 0) {
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
	while (*cpa2 != '.' && cpa2 > layer)
		cpa2--;
	*cpa2 = 0;
	while ((cc = fgetc(fp)) != EOF) {
		*cpa++ = cc;
		if (cc == '<') {
			cc = fgetc(fp);
			*cpa++ = cc;
			if (cc == '/') {
				while (*cpa2 != '.' && cpa2 > layer)
					cpa2--;
				*cpa2 = 0;
			} else {
				*cpa2++ = '.';
				*cpa2++ = cc;
				while ((cc = fgetc(fp)) != '>') {
					*cpa++ = cc;
					*cpa2++ = cc;
				}
				*cpa2 = 0;
				*cpa++ = cc;
				cpb = proj23;
				cpb2 = layer;
				while (*cpb++ == *cpb2++ && *cpb != 0)
					;
				if (*cpb == 0) {
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
					*cpa++ = 'M';
					*cpa++ = 'C';
					*cpa++ = 'P';
					for (cpb = mcv; *cpb; cpb++, cpa++)
						*cpa = *cpb;
					while ((cc = fgetc(fp)) != '<')
						;
					*cpa++ = cc;
					break;
				}
			}
		}
	}
	while ((cc = fgetc(fp)) != EOF)
		*cpa++ = cc;
	*cpa = 0;
	fclose(fp);
	/* get projects and write files. */
	DIR *dp = opendir("./");
	while ((dir = readdir(dp))) {
		stat(dir->d_name, &s);
		if (!(s.st_mode & S_IFDIR) || dir->d_name[0] == '.')
			continue;
		inb: fputs("query ", stdout);
		fputs(dir->d_name, stdout);
		fputs("?(y/n)", stdout);
		fflush(stdin);
		cc = getc(stdin);
		if (cc == 'n')
			continue;
		if (cc != 'y')
			goto inb;
		for (j = 0; dir->d_name[j] != 0; j++)
			;
		char fn[j + 12];
		for (cpb = dir->d_name, cpa = fn; *cpb; cpb++, cpa++)
			*cpa = *cpb;
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
		*cpa = 0;
		fp = fopen(fn, "wb");
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
		*cpa = 0;
		fp = fopen(fn, "wb");
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
		*cpa = 0;
		fp = fopen(fn, "wb");
		fputs(project1, fp);
		fputs(dir->d_name, fp);
		fputs(project2, fp);
		fclose(fp);
	}
	free(classpath);
	free(project2);
	return EXIT_SUCCESS;
}
