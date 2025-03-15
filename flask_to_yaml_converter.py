import ast
import yaml


input_file = 'main.py'

output_file = 'archivo.yaml'


with open(input_file, 'r', encoding='utf-8') as f:
    source_code = f.read()


parsed_code = ast.parse(source_code)

routes = []


for node in ast.walk(parsed_code):
    if isinstance(node, ast.FunctionDef):
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call) and hasattr(decorator.func, 'attr') and decorator.func.attr == 'route':
                route_path = decorator.args[0].s if decorator.args else ''
                methods = []
                for kw in decorator.keywords:
                    if kw.arg == 'methods' and isinstance(kw.value, ast.List):
                        methods = [el.s for el in kw.value.elts]
                routes.append({
                    'path': route_path,
                    'methods': methods or ['GET'],
                    'handler': node.name
                })


with open(output_file, 'w', encoding='utf-8') as f:
    yaml.dump({'routes': routes}, f, allow_unicode=True)

print(f'Rutas exportadas a {output_file} con éxito!')