from setuptools import setup, find_packages

install_requires = ['future', 'pandas', 'requests', 'requests_cache']

setup(
    name='pybiomart',
    version='0.0.1',
    url='',
    author='Julian de Ruiter',
    author_email='julianderuiter@gmail.com',
    description='',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    extras_require={},
    zip_safe=True,
    classifiers=[],
    install_requires=install_requires
)
