import sqlite3
import os

def getChangedFiles(files=None, builddir=None):
	changed_files = []

	# cache found, only compile changed files #
	if os.path.isfile(builddir + "build.db"):
		database = sqlite3.connect(builddir + "build.db")
		cursor = database.cursor()

		for item in files:
			cursor.execute("SELECT * FROM files WHERE file ='" + item + "'")
			dbreturn = cursor.fetchall()

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
			database.execute("INSERT INTO files values ('" + item + "', '" + str(os.stat(item).st_mtime) + "');")

			print("new file '" + item + "'")

			changed_files.insert(len(changed_files), item)

	database.commit()
	database.close()

	return changed_files