import torch

cuda = torch.cuda.is_available()

if not cuda:
    raise Exception("CUDA not available!")