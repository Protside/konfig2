import json
import os
import click
import subprocess

def get_dependencies(package_name):
    # Определяем путь к директории node_modules
    node_modules_path = os.path.join(os.getcwd(), 'node_modules', package_name)
    
    if not os.path.exists(node_modules_path):
        return []

    dependencies = []
    # Читаем package.json для указанного пакета
    package_json_path = os.path.join(node_modules_path, 'package.json')
    
    if os.path.exists(package_json_path):
        with open(package_json_path, 'r') as f:
            package_data = json.load(f)
            # Получаем зависимости из package.json
            dependencies = package_data.get('dependencies', {}).keys()

    return list(dependencies)

def build_plantuml_graph(package_name):
    plantuml_code = f'@startuml\n'
    plantuml_code += f'package "{package_name}" {{\n'
    
    def add_dependencies(pkg, level=1):
        nonlocal plantuml_code 
        deps = get_dependencies(pkg)
        for dep in deps:
            plantuml_code += f'{"  " * level}[{pkg}] --> [{dep}]\n'
            add_dependencies(dep, level + 1)

    add_dependencies(package_name)
    
    plantuml_code += '}\n@enduml'
    return plantuml_code

def visualize_plantuml(plantuml_code, visualizer_path):
    with open('output.puml', 'w') as uml_file:
        uml_file.write(plantuml_code)
    subprocess.run(['java', '-jar', visualizer_path, 'output.puml'])


@click.command()
@click.argument('config_path')
def main(config_path):
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

    package_name = config['package_name']
    output_path = config['output_path']
    visualizer_path = config['visualizer_path']

    plantuml_graph = build_plantuml_graph(package_name)

    with open(output_path, 'w') as output_file:
        output_file.write(plantuml_graph)

    print("Сгенерированный PlantUML код:")
    print(plantuml_graph)

    visualize_plantuml(plantuml_graph, visualizer_path)

if __name__ == "__main__":
    main()
