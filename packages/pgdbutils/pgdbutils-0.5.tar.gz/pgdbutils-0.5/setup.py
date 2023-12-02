from setuptools import setup, find_packages

setup(
    name='pgdbutils',
    version='0.5',
    packages=find_packages(),
    install_requires=[
        'psycopg2'
    ],
    long_description_content_type='text/x-rst', 
    long_description=open('readme.rst').read(),
    license='MIT',
    author='Technical Heist',
    author_email='contact@technicalheist.com',
    url='https://github.com/technicalheist/pgdbutils.git',
    keywords=['PostgreSQL', 'database', 'CRUD', 'utility'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
