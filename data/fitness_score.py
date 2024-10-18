import ast

class DataflowGraph:
    def __init__(self):
        self.dependencies = {}

    def add_dependency(self, target, source):
        if target not in self.dependencies:
            self.dependencies[target] = []
        if source is not None:
            self.dependencies[target].append(source)

    def calculate_depth(self):
        visited = set()
        depth_cache = {}

        def dfs(node):
            if node in depth_cache:
                return depth_cache[node]
            visited.add(node)
            max_depth = 1
            if node in self.dependencies:
                for neighbor in self.dependencies[node]:
                    max_depth = max(max_depth, 1 + dfs(neighbor))
            depth_cache[node] = max_depth
            return max_depth

        max_depth = 0
        for node in self.dependencies:
            if node not in visited:
                max_depth = max(max_depth, dfs(node))

        return max_depth

# Function to build the dataflow graph and calculate its depth
def calculate_dataflow_depth(program_code):
    tree = ast.parse(program_code)
    graph = DataflowGraph()
    current_values = {}

    class DataflowVisitor(ast.NodeVisitor):
        def visit_Assign(self, node):
            targets = node.targets
            value = node.value

            if isinstance(value, ast.Name):
                for target in targets:
                    if isinstance(target, ast.Name):
                        graph.add_dependency(target.id, value.id)
                        current_values[target.id] = value.id

            elif isinstance(value, ast.BinOp):
                if isinstance(value.left, ast.Name) and isinstance(value.right, ast.Name):
                    for target in targets:
                        if isinstance(target, ast.Name):
                            graph.add_dependency(target.id, value.left.id)
                            graph.add_dependency(target.id, value.right.id)
                            current_values[target.id] = value

            elif isinstance(value, ast.Call):
                for arg in value.args:
                    if isinstance(arg, ast.Name):
                        for target in targets:
                            if isinstance(target, ast.Name):
                                graph.add_dependency(target.id, arg.id)
                                current_values[target.id] = value

            else:
                for target in targets:
                    if isinstance(target, ast.Name):
                        graph.add_dependency(target.id, None)
                        current_values[target.id] = value

            self.generic_visit(node)

    visitor = DataflowVisitor()
    visitor.visit(tree)
    return graph.calculate_depth()


