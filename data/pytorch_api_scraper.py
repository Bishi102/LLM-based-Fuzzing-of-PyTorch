import torch
import inspect
import importlib
import sys

# List of prefixes to exclude
excluded_prefixes = []
def traversedir(module, pref='', level=0):
    """Traverse the module and return the full names of all functions and classes."""
    for attr in dir(module):
        if attr[0] == '_':
            continue
        if attr not in sys.modules:
            fullname = f'{pref}.{attr}'
            if any(fullname.startswith(excluded) for excluded in excluded_prefixes):
                continue 
            try:
                importlib.import_module(fullname)
                for submodule in traversedir(getattr(module, attr), pref=fullname, level=level+1):
                    yield submodule
            except Exception as e:
                continue
            yield fullname

def get_clean_signature(obj):
    """Retrieve the function signature, keeping default values but removing type annotations."""
    try:
        sig = inspect.signature(obj)
        params = []
        for name, param in sig.parameters.items():
            if param.default is param.empty:
                param_str = name  # No default value
            else:
                param_str = f"{name}={param.default!r}"  # Include the default value

            if param.kind in [param.VAR_POSITIONAL, param.VAR_KEYWORD]:
                param_str = f"*{param_str}" if param.kind == param.VAR_POSITIONAL else f"**{param_str}"

            params.append(param_str)
        
        return f"({', '.join(params)})"
    except (ValueError, TypeError):
        return None

def main():
    with open('pytorch_api_signatures.txt', 'w') as file:
        for fullname in traversedir(torch, pref='torch'):
            try:
                obj = eval(fullname)
                if callable(obj):
                    signature = get_clean_signature(obj)
                    if signature:
                        file.write(f'{fullname}{signature}\n')
            except Exception as e:
                continue

if __name__ == "__main__":
    main()