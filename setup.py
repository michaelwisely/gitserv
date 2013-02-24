from setuptools import setup, find_packages

setup(name="gitserv",
      version="1.0",
      # url='http://github.com/michaelwisely/git-server',
      license='BSD',
      description="A Twisted Conch SSH server for git access",
      author='Michael Wisely',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      install_requires=['setuptools',
                        'Twisted',
                        'pycrypto',
                        'pyasn1',
                        'dulwich>=0.8.6',
                        'jsonschema',
                        'requests',
                        ],
      entry_points={
        'console_scripts': ['gitserv = gitserv.main:run'],
        },
      )
