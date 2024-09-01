import torch

def run_on_device(snippet: str, device: torch.device):
    env = {}
    modded_snippet = snippet.replace('torch.device("cuda")', f'torch.device("{device.type}")')
    seed_code = """ 
random.seed(69)
np.random.seed(69)
torch.manual_seed(69)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(69)
"""
    if "import random" not in snippet:
        modded_snippet = modded_snippet.replace("import torch", f"import torch\nimport random")
    if "import numpy as np" not in snippet:
        modded_snippet = modded_snippet.replace("import torch", f"import torch\nimport numpy as np")
    modded_snippet = modded_snippet.replace("import random", f"import random\n{seed_code}")
    print(modded_snippet)
    try:
        exec(modded_snippet, env)
        for key in env:
            if key == 'output_tensor':
                print(env[key])
                return env[key]
        print("No 'output_tensor' found in the snippet output.")
        return None
    except Exception as e:
        print(f"Error using {device.type}: {e}")
        return None

def test_snippet(snippet: str):
    cpu_output = run_on_device(snippet, torch.device('cpu'))
    if torch.cuda.is_available():
        gpu_output = run_on_device(snippet, torch.device('cuda'))
        if isinstance(cpu_output, torch.Tensor) and isinstance(gpu_output, torch.Tensor):
            if torch.allclose(cpu_output, gpu_output.cpu(), atol=1e-6):
                print("Tensors match.")
            else:
                print("Tensors do not match.")
        elif isinstance(cpu_output, bool) and isinstance(gpu_output, bool):
            if cpu_output == gpu_output:
                print("Booleans match.")
            else:
                print("Booleans do not match.")
        elif isinstance(cpu_output, (int, float)) and isinstance(gpu_output, (int, float)):
            if abs(cpu_output - gpu_output) < 1e-6:
                print("Numerical values match.")
            else:
                print("Numerical values do not match.")
        else:
            print("Unsupported output types.")
    else:
        print("CUDA is not available")

