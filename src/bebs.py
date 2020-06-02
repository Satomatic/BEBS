import linecache
import sqlite3
import sys
import os

# files passed from bmake #
makefile = None
execute = None
output = "a.out"
force = False
error = False
compiler = "g++"

# check args #
i = 0
for x in range(len(sys.argv)):
	if x == 0:
		continue

	if x > i:
		if sys.argv[x] == "-f":
			force = True

		elif sys.argv[x] == "-o":
			if len(sys.argv) > x + 1:
				output = sys.argv[x + 1]
				i = x + 1
			else:
				print("[BEBS] ! '-o' Please specify output file")
				error = True

		elif sys.argv[x] == "-x":
			if len(sys.argv) > x + 1:
				execute = sys.argv[x + 1]
				i = x + 1
			else:
				print("[BEBS] ! '-x' Please specify execute command")
				error = True

		else:
			makefile = sys.argv[x]

# search for file #
if makefile == None:
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
if makefile == None:
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
		print("[BEBS] ! Please sepcify '" + item + "'")
		error = True

if error == True:
	sys.exit(1)

if force == True:
	print("'-f' force full recompile")

	for item in os.listdir(builddir):
		os.remove(builddir + item)

# check build location #
if not os.path.isdir(builddir):
	print("[BEBS] ! `builddir` does not exist '" + builddir + "'")
	sys.exit(1)

# collect project files #
print("Collecting files ...")
changed_files = []

# only build changed files #
if os.path.isfile(builddir + "build.db"):
	database = sqlite3.connect(builddir + "build.db")
	cursor = database.cursor()

	for item in files:
		cursor.execute("SELECT * FROM files WHERE file ='" + item + "'")
		dbreturn = cursor.fetchall()

		# new file found in bmake list #
		if len(dbreturn) == 0:
			print("new file " + item)
			cursor.execute("INSERT INTO files values ('" + item + "', '" + str(os.stat(item).st_mtime) + "');")
			changed_files.insert(len(changed_files), item)
		else:
			last_c_time = dbreturn[0][1]
			curr_c_time = str(os.stat(item).st_mtime)

			if last_c_time != curr_c_time:
				changed_files.insert(len(changed_files), dbreturn[0][0])
				cursor.execute("UPDATE files SET date = '" + curr_c_time + "' WHERE file = '" + item + "';")
			else:
				print("skipped '" + item + "'")

	database.commit()
	database.close()

# no cache found, build all files #
else:
	database = sqlite3.connect(builddir + "build.db")
	database.execute("CREATE TABLE files (file TEXT, date TEXT);")
	database.commit()

	for item in files:
		database.execute("INSERT INTO files values ('" + item + "', '" + str(os.stat(item).st_mtime) + "');")

		print("new file '" + item + "'")

		changed_files.insert(len(changed_files), item)
	
	database.commit()
	database.close()

# check for any changes #
if len(changed_files) == 0:
	print("\nno changes found\n")
	sys.exit(1)

# compile file to objects #
buildstr = compiler + " -c"
for item in changed_files:
	buildstr = buildstr + " " + item

print("\nbuilding files ...")
print(buildstr)
os.system(buildstr)

# move objects to build directory #
print("\nmoving into build ...")
os.system("mv *.o " + builddir)

# link files #
linkstr = compiler + " -o " + output
for item in libs:
	linkstr = linkstr + " " + item

for item in os.listdir(builddir):
	if item[-2:] == ".o":
		linkstr = linkstr + " " + builddir + item

print("linking files ...")
os.system(linkstr)

print(linkstr)

print("\nBuild done > " + output)

# execute final command #
if (execute != None):
	os.system(execute)
	print("execute >> " + execute)