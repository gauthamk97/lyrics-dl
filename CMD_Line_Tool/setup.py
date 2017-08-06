from setuptools import setup

setup(
    name="getlyrics",
    version="1.0",
    py_module=["getlyrics"],
    install_requires=["Click"],
    entry_points='''
        [console_scripts]
        getlyrics=main:maingl
    '''
)
