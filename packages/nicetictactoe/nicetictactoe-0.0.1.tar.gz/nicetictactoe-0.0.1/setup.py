from setuptools import setup, find_packages

setup(
    name='nicetictactoe',
    version='0.0.1',
    license='MIT',
    author="Alex Khosrojerdi",
    author_email='alex.khosrojerdi@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/iamkhosrojerdi/nicetictactoe',
    keywords='nicetictactoe python tictactoe game',
    install_requires=[
          'pygame==2.5.2',
      ],
)