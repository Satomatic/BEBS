import os

def buildFiles(compiler, args, changed_files, buildpath, template):
	build_str = template
	
	args_string = ""
	for item in args:
		args_string = args_string + item + " "
	args_string = args_string[:-1]

	file_string = ""
	for item in changed_files:
		file_string = file_string + item + " "

	build_str = build_str.replace("{compiler}", compiler)
	build_str = build_str.replace("{args}", args_string)
	build_str = build_str.replace("{files}", file_string)

	print(build_str)
	os.system(build_str)

def linkFiles(linker, args, output, builddir, libs, template):
	link_str = template

	args_string = ""
	file_string = ""
	lib_string = ""

	# build arg string #
	if len(args) > 0:
		for item in args:
			args_string = args_string + item + " "
		args_string = args_string[:-1]

	# output string #
	output_string = "-o " + output

	# file string #
	for item in os.listdir(builddir):
		if item[-2:] == ".o":
			file_string = file_string + builddir + item + " "
	file_string = file_string[:-1]

	# lib string
	for item in libs:
		lib_string = lib_string + item + " "
	lib_string = lib_string[:-1]

	link_str = link_str.replace("{linker}", linker)
	link_str = link_str.replace("{args}", args_string)
	link_str = link_str.replace("{output}", output_string)
	link_str = link_str.replace("{files}", file_string)
	link_str = link_str.replace("{libs}", lib_string)

	print(link_str)
	os.system(link_str)

def executeCommand(execute):
	if execute != None:
		os.system(execute)