import app
import sys
from src import preprocess as pre
from src import comment_database as cdb

###############################################################################
#               The run for the comment-extractor application              #
###############################################################################

length = len(sys.argv)

if length == 0:
  print('usage: run.py <command> <filename or repository')
  exit(0)

if length == 2 and sys.argv[1] in ('-h', '--help'):
  print('usage: \n run.py <command> <filename or repository')
  print('To get comments from directory: \n python3 run.py -d <root directory>')
  print('To get comments from repositories: \n python3 run.py -repo <repository link> <branch name> <depth>')

elif length >= 3:
    command1 = sys.argv[1]
    directory = sys.argv[2]
    if command1 == '-d':
      app.get_comment_from_path_using_all_languages(directory, './')
    elif command1 == '-repo':
      if length < 4:
        Exception("Not enough arguments")
      else:
        repo = sys.argv[2]
        branch = sys.argv[3]
        app.get_comment_from_repo_using_all_languages(repo , branch, './')
    elif command1 == "-process":
      leng = len(sys.argv)
      for i in range(2, leng):
        print("processing file: " + sys.argv[i])
        process = pre(sys.argv[i])
        process.create_new_processed_file()
    elif command1 == "-duplicate":
      leng = len(sys.argv)
      duplicated_files = []
      for i in range(2, len(sys.argv)):
        comment_db = cdb(sys.argv[i])
        comment_db.remove_duplicates_in_database()
        comment_db.export_table_to_csv()
    elif command1 == '-auto':
      leng = len(sys.argv)
      duplicated_files = []
      for i in range(2, len(sys.argv)):
        comment_db = cdb(sys.argv[i])
        comment_db.remove_duplicates_in_database()
        duplicated_files.append( comment_db.export_table_to_csv() )

      for each_file in duplicated_files:
        process = pre("./" + each_file)
        process.create_new_processed_file()

    elif command1 == "-comment":
      process = pre()
      stuff_to_process = {'line': sys.argv[2]}
      print(process.process_comment(stuff_to_process))


# app.get_comment_from_repo_using_all_languages("https://github.com/k9mail/k-9.git", "main", "./commentfiles/")
