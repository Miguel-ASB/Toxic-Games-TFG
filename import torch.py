import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(f"using device: {device}")

devNum = torch.cuda.current_device()

print(f"device number: {devNum}")

devName = torch.cuda.get_device_name(devNum)

print(f"device name: {devName}")