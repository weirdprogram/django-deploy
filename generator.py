from pathlib import Path
from typing import Text, Optional
import os


def generate(project_name: Text,
             static_folder: Text,
             python_version: Text,
             # dbtype: Text
             ) -> Text:
    generate_conf_nginx(project_name, static_folder)
    write_docker_file(python_version)
    write_nginx_docker_file()
    return "Finish"


def write_docker_file(python_version: Text):
    try:
        print("Please look at https://hub.docker.io for more information about python image version")
        print("Writing Dockerfile...")
        print("Please Wait..")
        strings = 'FROM python:{} \n' \
                  'COPY . /code \n' \
                  'WORKDIR /code/ \n' \
                  'RUN pip --default-timeout=1000 install --no-cache-dir -r requirements.txt\n'.format(python_version)
        docker_file = open("Dockerfile", "w")
        docker_file.write(strings)
        return print("Dockerfile Successfully Generated")
    except Exception as e:
        return print(e.args)


def write_nginx_docker_file():
    try:
        print("Writing nginx.Dockerfile")
        strings = "FROM nginx:alpine\nCOPY config/nginx/default.conf /etc/nginx/conf.d/"
        nginx_docker_file = open("nginx.Dockerfile", "w")
        nginx_docker_file.write(strings)
        return print("nginx.Dockerfile Successfully Generated")
    except Exception as e:
        return print(e.args)


def write_docker_compose():
    pass


def generate_conf_nginx(project_name: Text,
                        static_folder: Text):
    if static_folder is None:
        static_folder = "static"
    cur_dir = os.getcwd()
    Path(cur_dir + '/conf/nginx/conf.d').mkdir(parents=True, exist_ok=True)
    Path(cur_dir + '/config/nginx').mkdir(parents=True, exist_ok=True)
    strings = 'server{} \n' \
              '     listen 80; \n' \
              '     location / {} \n' \
              '         proxy_pass http://{}:8000; \n' \
              '      {} \n'\
              '\n'\
              '     location /{} {}\n' \
              '         alias /{}; # your Django projects static files - amend as required\n' \
              '     {}\n' \
              '{}\n'.format("{", "{", project_name, "}",
                            static_folder, "{", static_folder, "}",
                            "}")
    project_conf = open("conf/nginx/conf.d/"+project_name+".conf", "w")
    project_conf.write(strings)
    strings_mounting = 'server{}\n' \
                       '     listen 80;\n' \
                       '     server_name localhost;\n' \
                       '     location / {}\n' \
                       '         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n' \
                       '                   proxy_set_header X-Forwarded-Proto https;\n'\
                       '               proxy_set_header X-Real-IP $remote_addr;\n'\
                       '                   proxy_set_header Host $http_host;\n'\
                       '                   proxy_redirect off;\n'\
                       '         proxy_pass http://{}:8000;\n' \
                       '      {}\n'\
                       '\n'\
                       '     location /{} {}\n' \
                       '         alias /{}; # your Django projects static files - amend as required\n' \
                       '     {}\n' \
                       '{}\n'.format("{", "{", project_name, "}",
                                     static_folder, "{", static_folder, "}",
                                     "}")
    nginx_default = open("config/nginx/"+"default.conf", "w")
    nginx_default.write(strings_mounting)
    return print("Success created nginx configuration")

