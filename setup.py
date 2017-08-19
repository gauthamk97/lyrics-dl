from setuptools import setup
with open("README.rst", "rb") as f:
    long_descr = f.read().decode('utf-8')

setup(
    name="lyrics-dl",
    version="1.0.3",
    description='A tool to obtain the lyrics to your favorite songs',
    author='Gautham Kumar',
    author_email='kgautham1997@gmail.com',
    url='https://github.com/gauthamk97/getlyrics',
    long_description=long_descr,
    license='MIT',
    packages=["getlyrics"],
    install_requires=["Click"],
    entry_points= {
        "console_scripts" : ['lyrics-dl=getlyrics.__main__:maingl']
    }
)
