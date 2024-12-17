import unittest
import json
import os
from unittest.mock import patch, mock_open, MagicMock
from hw2 import get_dependencies, build_plantuml_graph

class TestDependencyGraph(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='{"dependencies": {"express": "^4.17.1", "axios": "^0.21.1"}}')
    def test_get_dependencies(self, mock_file):
        dependencies = get_dependencies("express")
        self.assertIn("axios", dependencies)
        self.assertNotIn("nonexistent-package", dependencies)

    @patch('hw2.get_dependencies')
    def test_build_plantuml_graph(self, mock_get_dependencies):
        mock_get_dependencies.side_effect = lambda pkg: {
            "express": ["axios"],
            "axios": [],
        }.get(pkg, [])

        uml_code = build_plantuml_graph("express")
        expected_code = (
            '@startuml\n'
            'package "express" {\n'
            '  [express] --> [axios]\n'
            '}\n@enduml'
        )
        self.assertEqual(uml_code.strip(), expected_code.strip())

    @patch('hw2.subprocess.run')
    @patch('builtins.open', new_callable=mock_open)
    def test_visualize_plantuml(self, mock_file, mock_subprocess):
        from hw2 import visualize_plantuml

        plantuml_code = '@startuml\npackage "Test" {}\n@enduml'
        visualize_plantuml(plantuml_code, 'path/to/plantuml.jar')

        # Проверяем, что файл был открыт для записи
        mock_file.assert_called_once_with('output.puml', 'w')
        
        # Проверяем, что subprocess.run был вызван с правильными аргументами
        mock_subprocess.assert_called_once_with(['java', '-jar', 'path/to/plantuml.jar', 'output.puml'])

if __name__ == '__main__':
    unittest.main()
