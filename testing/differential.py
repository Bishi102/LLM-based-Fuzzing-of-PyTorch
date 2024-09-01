import torch

def run_on_device(snippet: str, device: torch.device):
    env = {}
    modded_snippet = snippet.replace('torch.device("cuda")', f'torch.device("{device.type}")')
    print(modded_snippet)
    try:
        exec(modded_snippet, env)
        if 'output_tensor' in env:
            output_tensor = env['output_tensor']
            print(f"Output Tensor: {output_tensor}")
            return output_tensor
        else:
            print("No 'output_tensor' found in the snippet output.")
            return False
    except Exception as e:
        print(f"Error using {device.type}: {e}")
        return None

def test_snippet(snippet: str):
    cpu_output = run_on_device(snippet, torch.device('cpu'))
    if torch.cuda.is_available():
        gpu_output = run_on_device(snippet, torch.device('cuda'))
        if cpu_output is not None and gpu_output is not None:
            if torch.allclose(cpu_output, gpu_output.cpu(), atol=1e-6):
                print("Outputs are close enough on CPU and GPU")
            else:
                print("Outputs differ between CPU and GPU")
        else:
            print("Failed to run on GPU")
    else:
        print("CUDA is not available")

