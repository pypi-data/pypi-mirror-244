import os
from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension
# from setuptools.command.build_ext import build_ext


class CustomBuildExt(BuildExtension):
    def build_extension(self, ext):
        if ext.name == "ntt_cuda":
            self.build_lib = "src/liberate/ntt"
        else:
            self.build_lib = "src/liberate/csprng"

        os.environ["MAX_JOBS"] = str(os.cpu_count())
        super().build_extension(ext)


ext_modules = [
    CUDAExtension(
        name="randint_cuda",
        sources=[
            "src/liberate/csprng/randint.cpp",
            "src/liberate/csprng/randint_cuda_kernel.cu",
        ],
    ),
    CUDAExtension(
        name="randround_cuda",
        sources=[
            "src/liberate/csprng/randround.cpp",
            "src/liberate/csprng/randround_cuda_kernel.cu",
        ],
    ),
    CUDAExtension(
        name="discrete_gaussian_cuda",
        sources=[
            "src/liberate/csprng/discrete_gaussian.cpp",
            "src/liberate/csprng/discrete_gaussian_cuda_kernel.cu",
        ],
    ),
    CUDAExtension(
        name="chacha20_cuda",
        sources=[
            "src/liberate/csprng/chacha20.cpp",
            "src/liberate/csprng/chacha20_cuda_kernel.cu",
        ],
    ),
    CUDAExtension(
        name="ntt_cuda",
        sources=[
            "src/liberate/ntt/ntt.cpp",
            "src/liberate/ntt/ntt_cuda_kernel.cu",
        ],
    )
]

setup(name="extensions", 
      ext_modules=ext_modules,
      cmdclass={
          "build_ext": CustomBuildExt
          },
      script_args=["build_ext"] 
      ),

