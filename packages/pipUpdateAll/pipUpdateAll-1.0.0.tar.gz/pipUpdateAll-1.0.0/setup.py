from setuptools import setup, find_packages


def read_readme():
    with open('README.md', 'r', encoding='utf-8') as file:
        return file.read()


setup(
    name='pipUpdateAll',
    version='1.0.0',
    author='SurivZ',
    author_email='franklinserrano23@email.com',
    description='Paquete para actualizar todos los paquetes instalados con \'pip\'',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/SurivZ/pip-update-all',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'update = pipUpdateAll:update',
        ],
    },
)
