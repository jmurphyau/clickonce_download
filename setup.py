try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def get_requirements(filename):
    with open(filename) as file:
        return file.readlines()

def main():
    setup(
        name='clickonce_download',
        author='jmurphyau',
        description='Downloads files referenced from a click once .application file',
        url='https://github.com/jmurphyau/clickonce_download',
        version='1.0.0',
        python_requires='>=3.7.0',
        install_requires=get_requirements('requirements.txt'),
        scripts=['clickonce_download.py'],
    )

if __name__ == "__main__":
    main()
