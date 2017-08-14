from setuptools import setup

setup(
    name="getlyrics",
    version="1.0.1",
    description='A tool to obtain the lyrics to your favorite songs',
    author='Gautham Kumar',
    author_email='kgautham1997@gmail.com',
    url='https://github.com/gauthamk97/getlyrics',
    license='MIT',
    packages=["getlyrics"],
    install_requires=["Click"],
    entry_points= {
        "console_scripts" : ['getlyrics=getlyrics.__main__:maingl']
    }
)
