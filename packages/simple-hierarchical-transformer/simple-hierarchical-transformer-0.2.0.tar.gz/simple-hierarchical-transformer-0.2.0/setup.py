from setuptools import setup, find_packages

setup(
  name = 'simple-hierarchical-transformer',
  packages = find_packages(exclude=[]),
  version = '0.2.0',
  license='MIT',
  description = 'Simple Hierarchical Transformer',
  author = 'Phil Wang',
  author_email = 'lucidrains@gmail.com',
  long_description_content_type = 'text/markdown',
  url = 'https://github.com/lucidrains/simple-hierarchical-transformer',
  keywords = [
    'artificial intelligence',
    'deep learning',
    'transformers',
    'attention mechanism',
    'hierarchical'
  ],
  install_requires=[
    'accelerate',
    'einops>=0.7.0',
    'local-attention',
    'torch>=2.0'
  ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)
