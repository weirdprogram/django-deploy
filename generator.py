from pathlib import Path
from typing import Text
from jinja2 import Environment, FileSystemLoader
import yaml
import jinja2

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


def write_docker_compose(version: int = 3, 
                        nginx_dockerfile: Text = 'nginx.Dockerfile',
                        nginx_ports: list = ['0.0.0.0:443:443'],
                        nginx_volume: list = ['./static:/var/www/static'],
                        nginx_network_alias: list = ['acmecorp.com']
                    ):
    docker_compose = {}

    docker_compose['version'] = version
    docker_compose['services'] = {}
    docker_compose['services']['nginx'] = {
        'build': {
            'context': '.',
            'dockerfile': nginx_dockerfile
        },
        'ports': nginx_ports,
        'networks':{
            'default':{
                'aliases': nginx_network_alias
            }
        },
        'depends_on':['web']
    }
    return yaml.dump(docker_compose, default_flow_style=False)

    
def generate_conf_nginx(project_name: Text,
                        static_folder: Text) -> Text:
    if static_folder is None:
        static_folder = "static"
    cur_dir = os.getcwd()
    folder_loader_nginx = FileSystemLoader('templates/conf/nginx/conf.d/')
    folder_loader_mount = FileSystemLoader('templates/config/nginx/')
    env_nginx = Environment(loader=folder_loader_nginx)
    env_mount = Environment(loader=folder_loader_mount)
    template_nginx = env_nginx.get_template('nginx.conf')
    template_mount = env_mount.get_template('default.conf')
    Path(cur_dir + '/conf/nginx/conf.d').mkdir(parents=True, exist_ok=True)
    Path(cur_dir + '/config/nginx').mkdir(parents=True, exist_ok=True)
    outpout_strings_nginx = template_nginx.render(project_name=project_name,
                                                  static_folder=static_folder)
    project_conf = open("conf/nginx/conf.d/"+project_name+".conf", "w")
    project_conf.write(outpout_strings_nginx)
    output_strings_mounting = template_mount.render(project_name=project_name,
                                                    static_folder=static_folder)
    nginx_default = open("config/nginx/"+"default.conf", "w")
    nginx_default.write(output_strings_mounting)
    message = "Success Created Nginx Configuration"
    return message
  
  
def generate_conf_nginx():
    pass
