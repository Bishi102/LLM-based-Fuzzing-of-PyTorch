from dotenv import load_dotenv
from openai import OpenAI
import os
import torch
import tokenizers
from transformers import AutoModelForCausalLM, AutoTokenizer

# tokenizer version requirement
tokenizers_version = tuple(int(n) for n in tokenizers.__version__.split('.'))
if tokenizers_version < (0, 12, 1):
    print("warning: Your tokenizers version looks old and you will likely have formatting issues. We recommend installing tokenizers >= 0.12.1")

# set BIG_MODEL to True to use the 6.7B parameter model, otherwise 1.3B model will be used as default
BIG_MODEL = False
# use a GPU
CUDA = True
# print intermediate outputs of infilling
VERBOSE = False

if BIG_MODEL:
    model_name = "facebook/incoder-6B"
    # the arguments added below will load a half precision version of the model,
    # which requires less RAM than loading the full float32 version.  this 
    # should fit in ~16GB of RAM
    # NOTE: half precision should *not* be used if you plan to fine-tune the
    # model. You'll need full precision and a lot of GPU memory. We have not
    # tested fine-tuning in `transformers` (the model was trained in fairseq)
    if CUDA:
        kwargs = dict(
            revision="float16", 
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
        )
    else:
        kwargs = dict(
            low_cpu_mem_usage=True,
        )
else:
    model_name = "facebook/incoder-1B"
    kwargs = {}

print("loading model")
model = AutoModelForCausalLM.from_pretrained(model_name, **kwargs)
print("loading tokenizer")
tokenizer = AutoTokenizer.from_pretrained(model_name)
print("loading complete")

if CUDA:
    # if you plan to fine-tune the model, you should not use half precision.
    model = model.half().cuda()

# signals the start of a document
BOS = "<|endoftext|>"
# signals the end of a generated infill
EOM = "<|endofmask|>"

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(
    api_key=openai_api_key
)

# mutates a given program
def mutate():
    return

