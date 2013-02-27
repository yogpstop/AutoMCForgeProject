all:
	rm -f MkFF.exe
	gcc-3 -mno-cygwin -O2 -Wall -fmessage-length=0 -o MkFF.exe MkFF.c