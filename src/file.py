import sqlite3
import os

def getChangedFiles(files=None, builddir=None, exts=None):
	changed_files = []
	database_files = {}

	# cache found, only compile changed files #
	if os.path.isfile(builddir + "build.db"):
		database = sqlite3.connect(builddir + "build.db")
		cursor = database.cursor()

		# get files from database #
		cursor.execute("SELECT * FROM files;")
		dbreturn = cursor.fetchall()
		for item in dbreturn:
			database_files[item[0]] = item

		for item in files:
			dirItems = getItemDir(item, exts)

			# directory object found #
			if len(dirItems) > 0:
				for file in dirItems:
					dbreturn = [database_files[file]]

					# new file found #
					if len(dbreturn) == 0:
						database.execute("INSERT INTO files values ('" + file + "', '" + str(os.stat(file).st_mtime) + "');")
						print("new file '" + file + "'")
						changed_files.insert(len(changed_files), file)

					# check when last edited #
					else:
						last_c_time = dbreturn[0][1]
						curr_c_time = str(os.stat(file).st_mtime)

						if last_c_time != curr_c_time:
							changed_files.insert(len(changed_files), dbreturn[0][0])
							cursor.execute("UPDATE files SET date = '" + curr_c_time + "' WHERE file = '" + file + "';")
						else:
							print("skipped '" + file + "'")
			
			# normal file object #
			else:
				dbreturn = [database_files[item]]

				# new file found #
				if len(dbreturn) == 0:
					print("new file " + item)
					cursor.execute("INSERT INTO files values ('" + item + "', '" + str(os.stat(item).st_mtime) + "');")
					changed_files.insert(len(changed_files), item)

				# check if file has been changed #
				else:
					last_c_time = dbreturn[0][1]
					curr_c_time = str(os.stat(item).st_mtime)

					if last_c_time != curr_c_time:
						changed_files.insert(len(changed_files), dbreturn[0][0])
						cursor.execute("UPDATE files SET date = '" + curr_c_time + "' WHERE file = '" + item + "';")
					else:
						print("skipped '" + item + "'")

	# no cache found, compile everything #
	else:
		database = sqlite3.connect(builddir + "build.db")
		database.execute("CREATE TABLE files (file TEXT, date TEXT);")
		database.commit()

		for item in files:
			# if marked as directory #
			dirItems = getItemDir(item, exts)
			if len(dirItems) > 0:
				for file in dirItems:
					database.execute("INSERT INTO files values ('" + file + "', '" + str(os.stat(file).st_mtime) + "');")
					print("new file '" + file + "'")
					changed_files.insert(len(changed_files), file)

			# single file #
			else:
				database.execute("INSERT INTO files values ('" + item + "', '" + str(os.stat(item).st_mtime) + "');")
				print("new file '" + item + "'")
				changed_files.insert(len(changed_files), item)

	database.commit()
	database.close()

	return changed_files

def getItemDir(item, exts):
	returnList = []
	if item[:3] == "%d " or item[:3] == "%D ":
		for file in os.listdir(item[3:]):
			filesplit = file[3:].split(".")

			# check if file should be compiled #
			if filesplit[len(filesplit) - 1] in exts:
				returnList.insert(len(returnList), item[3:] + file)

	return returnList