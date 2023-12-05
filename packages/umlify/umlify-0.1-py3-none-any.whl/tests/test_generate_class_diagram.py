import os
from umlfy.class_diagram import generate_class_diagram

def test_generate_class_diagram():
    test_app_path = '/home/adeline/Projetos/UMLfy/tests/_test_app'
    test_package_names = ["services", "repositories"]
    test_file_path = '/home/adeline/Projetos/UMLfy/tests/output/test_diagram.puml'

    result = generate_class_diagram(test_app_path, test_package_names, test_file_path)
    
    assert result is True
    assert os.path.exists(test_file_path)

    with open(test_file_path, 'r') as file:
        uml_content = file.read()

    assert "@startuml ClassDiagram" in uml_content
    assert "package \"Services\"" in uml_content or "package \"Repositories\"" in uml_content
