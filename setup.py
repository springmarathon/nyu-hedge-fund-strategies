from setuptools import setup 
  
setup(
    name='quant-strategies', 
    version='0.1', 
    author='Eileen Zhang', 
    author_email='Eileen.Wei.Zhang@gmail.com', 
    packages=['common', 'optimization', 'sharadar'], 
    install_requires=[ 
        'numpy', 
        'pandas', 
    ], 
)