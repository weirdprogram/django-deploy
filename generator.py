from typing import Text, Optional
import yaml


def generate(#project_name: Text,
             # static_folder: Text,
             # template_folder: Text,
             python_version: Text,
             # dbtype: Text
             ) -> Text:
    write_docker_file(python_version)
    write_nginx_docker_file()
    return "Finish"


def write_docker_file(python_version: Text):
    try:
        print("Please look at https://hub.docker.io for more information about python image version")
        print("Writing Dockerfile...")
        print("Please Wait..")
        strings = 'FROM python:%s \n' \
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

    



def generate_conf_nginx():
    pass