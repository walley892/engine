from setuptools import setup

setup(
    name='engine',
    version='0.1.0',    
    description='A example Python package',
    author='Stephen Hudson',
    author_email='',
    license='BSD 2-clause',
    packages=['engine', 'engine.rendering'],
    package_data={'': ['rendering/font_textures/font.json', 'rendering/font_textures/font.png']},
    install_requires=[],

    classifiers=['Programming Language :: Python :: 3.5'],
)
