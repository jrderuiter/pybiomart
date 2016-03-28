from setuptools import setup, find_packages
import versioneer

install_requires = ['future', 'pandas', 'requests', 'requests_cache']

setup(
    name='pybiomart',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    url='https://github.com/jrderuiter/pybiomart',
    download_url='',
    author='Julian de Ruiter',
    author_email='julianderuiter@gmail.com',
    description='A simple pythonic interface to biomart.',
    license='MIT',
    packages=find_packages(),
    zip_safe=True,
    classifiers=['Intended Audience :: Developers',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5'],
    install_requires=install_requires,
    extras_require={}
)
