from build import *
from file import *
import linecache
import sqlite3
import time
import sys
import os

# files passed from bmake #
makefile = None
execute = None
output = "a.out"
force = False
error = False

compiler = "g++"
linker = "g++"

pretasks = []
exts = ["cpp", "c"]
build_args = ["-c"]
link_args = []
libs = []

build_template = "{compiler} {args} {files}"
link_template = "{linker} {args} {output} {files} {libs}"

# check args #
i = 0
for x in range(len(sys.argv)):
	if x == 0:
		continue

	if x > i:
		if sys.argv[x].lower() == "-f":
			force = True

		elif sys.argv[x].lower() == "-o":
			if len(sys.argv) > x + 1:
				output = sys.argv[x + 1]
				i = x + 1
			else:
				print("[BEBS] ! '-o' Please specify output file")
				error = True

		elif sys.argv[x].lower() == "-x":
			if len(sys.argv) > x + 1:
				execute = sys.argv[x + 1]
				i = x + 1
			else:
				print("[BEBS] ! '-x' Please specify execute command")
				error = True

		else:
			makefile = sys.argv[x]

# search for file #
if not makefile:
	for item in os.listdir():
		if item == "bmake":
			makefile = item
		else:
			try:
				if "BEBS_FILE" in linecache.getline(item, 1).strip("\n"):
					makefile = item
			except:
				pass

# check for bmake file #
if makefile == None or not os.path.isfile(makefile):
	print("[BEBS] ! Couldn't find make file")
	sys.exit(1)

# read file #
file = open(makefile)
for line in file:
	line = line.strip("\n")
	exec(line)
file.close()

# check bmake file #
required = ['files', 'builddir', 'libs']

for item in required:
	if item not in locals():
		print(f"[BEBS] ! Please specify '{item}'")
		error = True

if error:
	sys.exit(1)

if force:
	print("'-f' force full recompile")

	for item in os.listdir(builddir):
		os.remove(builddir + item)

# check build location #
if not os.path.isdir(builddir):
	print(f"[BEBS] ! `builddir` does not exist '{builddir}'")
	sys.exit(1)

# collect project files #
print("Collecting files ...")
changed_files = getChangedFiles(files, builddir, exts)

# check for any changes #
if len(changed_files) == 0:
	print("\nno changes found\n")
	executeCommand(execute)
	sys.exit(1)

# execute pre-tasks #
if len(pretasks) > 0:
	print("\nexecuting pretasks ...")
	for task in pretasks:
		print(task)
		os.system(task)

# compile file to objects #
print("\nbuilding files ...")
buildFiles(compiler, build_args, changed_files, builddir, build_template)

# move objects to build directory #
print("\nmoving into build ...")
os.system("mv *.o " + builddir)

# link files #
print("linking files ...")
linkFiles(linker, link_args, output, builddir, libs, link_template)

print("\nBuild done > " + output)

# execute final command #
executeCommand(execute)
