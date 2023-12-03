try:
    from .jax_module import PixelyAIServeJax
except ModuleNotFoundError:
    print("Couldn't import JAXServe")

try:
    from .torch_module import PixelyAIServeTorch
except ModuleNotFoundError:
    print("Couldn't import TorchServe")
