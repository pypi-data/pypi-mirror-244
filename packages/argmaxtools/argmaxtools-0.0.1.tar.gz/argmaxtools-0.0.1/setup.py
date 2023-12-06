from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='argmaxtools',
    version='0.0.1', # __version__,
    url='https://github.com/argmaxinc/argmaxtools',
    description="Inference. Anything. Everywhere",
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Argmax, Inc.',
    install_requires=[
        "coremltools>=7.1",
        "torch",
        "transformers",
        "huggingface-hub",
        "scikit-learn",
    ],
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
    ],
)
