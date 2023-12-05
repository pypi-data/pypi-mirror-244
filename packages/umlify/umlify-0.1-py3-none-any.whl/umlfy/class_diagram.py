import ast
import os

class ClassVisitor(ast.NodeVisitor):
    def __init__(self):
        self.classes = {}
        self.dependencies = {}
    
    def visit_Assign(self, node):
        # Verifica se a atribuição é uma instância de classe
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
            class_name = node.value.func.id
            if class_name in self.classes:
                current_class = self.current_class
                if current_class not in self.dependencies:
                    self.dependencies[current_class] = set()
                self.dependencies[current_class].add(class_name)
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node):
        if node.name == '__init__':
            for arg in node.args.args:
                if arg.arg != 'self' and hasattr(arg, 'annotation') and isinstance(arg.annotation, ast.Name):
                    dependency_type = arg.annotation.id
                    if self.current_class not in self.dependencies:
                        self.dependencies[self.current_class] = set()
                    self.dependencies[self.current_class].add(dependency_type)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.current_class = node.name
        methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef) and not n.name.startswith('_')]
        self.classes[node.name] = methods
        self.generic_visit(node)

def analyze_file(file_path):
    with open(file_path, 'r') as file:
        node = ast.parse(file.read())
        visitor = ClassVisitor()
        visitor.visit(node)
        return visitor.classes, visitor.dependencies

def analyze_directory(directory_path):
    classes_in_directory = {}
    dependencies_in_directory = {}
    for file in os.listdir(directory_path):
        if file.endswith('.py'):
            classes, dependencies = analyze_file(os.path.join(directory_path, file))
            classes_in_directory.update(classes)
            dependencies_in_directory.update(dependencies)
    return classes_in_directory, dependencies_in_directory


def generate_uml(classes, dependencies, packages):
    uml_str = "@startuml ClassDiagram\n"
    
    # Adicionando classes aos pacotes
    for package_name, package_classes in packages.items():
        uml_str += f"package \"{package_name}\" {{\n"
        for class_name in package_classes:
            uml_str += f"    class {class_name} {{\n"
            for method in classes.get(class_name, []):
                uml_str += f"      +{method}()\n"
            uml_str += "    }\n"
        uml_str += "}\n"

    # Adicionando relações
    for class_name, deps in dependencies.items():
        for dep in deps:
            uml_str += f"{class_name} --> {dep}\n"

    uml_str += "@enduml"
    return uml_str


def generate_class_diagram(app_path, package_names, file_path):
    classes_info = {}
    dependencies_info = {}
    packages = {}

    for package_name in package_names:
        package_path = os.path.join(app_path, package_name)
        if os.path.isdir(package_path):
            package_classes, package_dependencies = analyze_directory(package_path)
        elif os.path.isfile(f"{package_path}.py"):
            package_classes, package_dependencies = analyze_file(f"{package_path}.py") 
        else:
            continue 

        packages[package_name.capitalize()] = package_classes
        classes_info.update(package_classes)
        dependencies_info.update(package_dependencies)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    uml_string = generate_uml(classes_info, dependencies_info, packages)

    with open(file_path, 'w') as file:
        file.write(uml_string)

    return True