from setuptools import setup, find_packages

install_requires = ['pandas', 'requests']

setup(
    name='biomart_jr',
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
