from services.parsers.node_parser import parse_package_json
from services.parsers.python_parser import parse_requirements
from services.parsers.java_parser import parse_pom_xml
from services.parsers.php_parser import parse_composer_json
from services.parsers.ruby_parser import parse_gemfile
from services.parsers.kotlin_parser import parse_build_gradle

def detect_ecosystem(file_path, file):
  if file_path.endswith('requirements.txt'):
    return parse_requirements(file)
  elif file_path.endswith('pom.xml'):
    return parse_pom_xml(file)
  elif file_path.endswith('package.json'):
    return parse_package_json(file)
  elif file_path.endswith('composer.json'):
    return parse_composer_json(file)
  elif file_path.endswith('gemfile'):
    return parse_gemfile(file)
  elif file_path.endswith('build.gradle'):
    return parse_build_gradle(file)
  else:
    return 'Unknown'