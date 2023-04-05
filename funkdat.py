import argparse
import ast
import os
from typing import List, Tuple, Optional, Set

class FunctionVisitor(ast.NodeVisitor):
    def __init__(self, function_name: str):
        self.function_name = function_name
        self.nodes = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if node.name == self.function_name:
            self.nodes.append(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        if node.name == self.function_name:
            self.nodes.append(node)
        self.generic_visit(node)

def find_function_in_file(file_path: str, function_name: str) -> Optional[ast.AST]:
    with open(file_path, "r") as file:
        content = file.read()
        try:
            tree = ast.parse(content)
            visitor = FunctionVisitor(function_name)
            visitor.visit(tree)

            if visitor.nodes:
                return visitor.nodes[0]
        except SyntaxError:
            pass

    return None

def find_related_in_file(file_path: str, function_node: ast.AST, related: Set[str]) -> List[Tuple[str, ast.AST]]:
    related_nodes = []
    with open(file_path, "r") as file:
        content = file.read()
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if node.name in related:
                        related_nodes.append((file_path, node))
                        related.remove(node.name)
        except SyntaxError:
            pass

    return related_nodes

def walk_and_find_function(repo_path: str, function_name: str, filename: Optional[str]) -> Tuple[str, ast.AST]:
    if filename:
        function_node = find_function_in_file(filename, function_name)
        if function_node:
            return filename, function_node
        else:
            return None, None

    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                function_node = find_function_in_file(file_path, function_name)
                if function_node:
                    return file_path, function_node

    return None, None

def find_related(repo_path: str, file_path: str, function_name: str) -> List[Tuple[str, ast.AST]]:
    with open(file_path, "r") as file:
        content = file.read()
        tree = ast.parse(content)
        function_node = None

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function_name:
                function_node = node
                break

        if function_node is None:
            return []

        related = set()
        for node in ast.walk(function_node):
            if isinstance(node, ast.Name):
                related.add(node.id)

        related_nodes = []
        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    nodes = find_related_in_file(file_path, function_node, related)
                    related_nodes.extend(nodes)

                    if not related:
                        break

    return related_nodes

def main():
    parser = argparse.ArgumentParser(description="Find function and related code in a repo")
    parser.add_argument("--repo", required=True, help="Path to the repository")
    parser.add_argument("--function", required=True, help="Function name to find")
    parser.add_argument("--filename", help="Optional filename to start the search")
    parser.add_argument("--debug", action='store_true', help="Enable debug mode to show extra output")

    args = parser.parse_args()

    repo_path = args.repo
    function_name = args.function
    filename = args.filename
    debug = args.debug

    if filename is not None:
        filename = os.path.join(repo_path, filename)

    file_path, function_node = walk_and_find_function(repo_path, function_name, filename)

    if function_node is None:
        print(f"Function '{function_name}' not found.")
        return

    print(f"Function '{function_name}' found in file: {file_path}")

    related_nodes = find_related(repo_path, file_path, function_name)

    output_file = f"{function_name}_output.py"
    with open(output_file, 'w') as f:
        f.write(ast.unparse(function_node))
        f.write("\n")

        for node_file_path, node in related_nodes:
            if debug:
                print(f"Node from file {node_file_path}:")
                print(ast.unparse(node))
                print("-" * 80)
            
            f.write(ast.unparse(node))
            f.write("\n")

    print(f"Output written to: {output_file}")

if __name__ == "__main__":
    main()
