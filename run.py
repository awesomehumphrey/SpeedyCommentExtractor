import app
import sys

###############################################################################
#               The driver for the comment-extractor application              #
###############################################################################

length = len(sys.argv)

if length == 0:
  print('usage: driver.py <command> <filename or repository')
  exit(0)

if length == 2 and sys.argv[1] in ('-h', '--help'):
  print('usage: \n driver.py <command> <filename or repository')
  print('To get comments from directory: \n python3 driver.py -d <root directory>')
  print('To get comments from repositories: \n python3 driver.py -repo <repository link> <branch name> <depth>')

elif length == 3:
    command1 = sys.argv[1]
    directory = sys.argv[2]
    if command1 == '-d':
        app.get_comment_from_path_using_all_languages(directory, './')


# app.get_comment_from_repo_using_all_languages("https://github.com/k9mail/k-9.git", "main", "./commentfiles/")
