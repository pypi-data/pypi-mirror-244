import platform
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Build extras_requires based on platform
def build_additional_requires():
    py_version = platform.python_version()[0:3].replace('.', "")
    if platform.system() == "Linux" and platform.machine() == "x86_64":
        additional_requires=[
            f"speexdsp_ns @ https://github.com/dscripka/openWakeWord/releases/download/v0.1.1/speexdsp_ns-0.1.2-cp{py_version}-cp{py_version}-linux_x86_64.whl",
        ]
    elif platform.system() == "Linux" and platform.machine() == "aarch64":
        additional_requires=[
            f"speexdsp_ns @ https://github.com/dscripka/openWakeWord/releases/download/v0.1.1/speexdsp_ns-0.1.2-cp{py_version}-cp{py_version}-linux_aarch64.whl",
        ],
    elif platform.system() == "Windows" and platform.machine() == "x86_64":
        additional_requires=[
            'PyAudioWPatch'
        ]
    else:
        additional_requires = []

    return additional_requires

setuptools.setup(
    name="openwakeword-compact",
    version="0.5.0",
    install_requires=[
        'onnxruntime>=1.10.0,<2',
        'tflite-runtime>=2.8.0,<3; platform_system == "Linux"',
        'tqdm>=4.0,<5.0',
        'requests>=2.0,<3',
    ],
    extras_require={
        'test': [
            'pytest>=7.2.0,<8',
            'pytest-cov>=2.10.1,<3',
            'pytest-flake8>=1.1.1,<2',
            'flake8>=4.0,<4.1',
            'pytest-mypy>=0.10.0,<1',
            'types-requests',
            'types-PyYAML',
            'mock>=5.1,<6',
            'types-mock>=5.1,<6',
            'types-requests>=2.0,<3'
        ],
    },
    author="David Scripka, Siran Shen",
    description="A compact version of the open source framework 'openwakeword' by David Scripka",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/siranshen/openWakeWord-Compact",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache 2.0 License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires=">=3.7",
)