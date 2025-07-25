from services.parsers.node_parser import parse_package_json
from services.parsers.python_parser import parse_requirements

def detect_ecosystem(file_path, file):
  if file_path.endswith('requirements.txt'):
    return parse_requirements(file)
  elif file_path.endswith('pom.xml'):
    return 'java'
  elif file_path.endswith('package.json'):
    return parse_package_json(file)
  elif file_path.endswith('composer.json'):
    return 'php'
  elif file_path.endswith('gemfile'):
    return 'ruby'
  elif file_path.endswith('build.gradle'):
    return 'kotlin'
  else:
    return 'Unknown'