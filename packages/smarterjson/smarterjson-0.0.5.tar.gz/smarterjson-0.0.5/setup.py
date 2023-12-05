from setuptools import setup, find_packages

long_description = ""

setup(
    name='smarterjson',
    version='0.0.5',
    description='A smart json tools',
    long_description = long_description,
    url='https://github.com/0x22f1a6543a0/custom-json',
    author='Zhang Jiaqi',
    author_email='2953911716@qq.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='TODO',
    install_requires = [
      "TODO",
    ],
    packages=find_packages(),
    include_package_data=True,
)
