all:
	rm -f output.exe
	gcc -s -O2 -Wall -o output.exe main.c