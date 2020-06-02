import os

def buildFiles(changed_files, builddir, compiler):
	buildstr = compiler + " -c"
	for item in changed_files:
		buildstr = buildstr + " " + item

	print(buildstr)
	os.system(buildstr)

def linkFiles(builddir, compiler, libs, output):
	linkstr = compiler + " -o " + output
	for item in libs:
		linkstr = linkstr + " " + item

	for item in os.listdir(builddir):
		if item[-2:] == ".o":
			linkstr = linkstr + " " + builddir + item

	print(linkstr)
	os.system(linkstr)