import unittest

from generator import write_docker_compose 
import yaml

class TestWriteDockerCompose(unittest.TestCase):
    def test_defaultparameter(self):
        str_docker_compose = write_docker_compose()
        docker_compose = yaml.safe_load(str_docker_compose)
        self.assertIs(type(docker_compose), dict)

if __name__ == '__main__':
    unittest.main()