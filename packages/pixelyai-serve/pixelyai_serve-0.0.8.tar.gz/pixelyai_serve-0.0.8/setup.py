from setuptools import setup, find_packages

setup(
    name='pixelyai_serve',
    version='0.0.8',
    author='Erfan Zare Chavoshi',
    author_email='erfanzare82@eyahoo.com',
    description='serve utilises of pixelyai in jax and torch',
    url='https://github.com/erfanzar/EasyDeL',
    packages=find_packages('lib/python'),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='machine learning, deep learning, pytorch, jax, flax',
    install_requires=[
        # "EasyDel>=0.0.35",
        "pydantic_core==2.10.1"
    ],
    python_requires='>=3.8',
    package_dir={'': 'lib/python'},
    password='PixelyAIServeJAXTORCH'
)
