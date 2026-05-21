import torch
import time

start = time.time()

x = torch.rand(5000, 5000, device="cuda")
y = torch.mm(x, x)

torch.cuda.synchronize()

print(time.time() - start)
