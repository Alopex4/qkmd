import setuptools

with open("README.md", 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='qkmd',
    version='0.1',
    author="alopex cheung",
    author_email="alopex4@163.com",
    description="Quick markdown what you need, just via a link.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Alopex4/qkmd",
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Linux",
    ],
    install_requires=[
        'requests',
        'pyquery',
        'pygments',
    ],
    entry_points={'console_scripts': [
        'qkmd = qkmd.qkmd:command_runner',
    ]},
)
