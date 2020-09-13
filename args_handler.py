import argparse
from generator import generate
parser = argparse.ArgumentParser()

parser.add_argument("-p", "--project_folder", help="Root Folder of your Django Project")
parser.add_argument("-s", "--static_folder", help="Static Folder of your Django Project")
parser.add_argument("-db", "--database_project", help="Database of your Django Project")
parser.add_argument("-py", "--python_image_version", help="See https://hub.docker.com/_/python for python image")
options = parser.parse_args()
# print(options.project_folder)
generate(project_name=options.project_folder,
         static_folder=options.static_folder,
         python_version=options.python_image_version,
         database=options.database_project)
