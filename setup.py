import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="envText",
    version="0.0.1",
    author="Bi Huaibin",
    author_email="bi.huaibin@foxmail.com",
    description="envText for Chinese texts analysis in Environment domain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/celtics1863/envText",
    project_urls={
        "Bug Tracker": "https://github.com/celtics1863/envText/issues",
    },
    install_requires=[
        'datasets',
        'gensim',
        'tqdm',
        'numpy',
        'pytorch-crf',
        'pandas',
        'torch',
        'transformers',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    keywords='NLP,bert,Chinese,LSTM,RNN,domain text analysis',
    package_dir={"": "envText"},
    packages=setuptools.find_packages(where="envText"),
    python_requires=">=3.6",
)