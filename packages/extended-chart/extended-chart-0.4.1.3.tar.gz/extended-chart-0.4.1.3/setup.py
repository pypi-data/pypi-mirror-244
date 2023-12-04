from setuptools import setup

setup(name='extended-chart',
      version='0.4.1.3',
      description='wrapper for lightweight-charts-python for trading strategy discovery',
      url='https://github.com/karunkrishna/poc_lightweight_charts',
      author='Karun Krishna',
      author_email='karun.krishna@gmail.com',
      license='MIT',
      packages=['extended_chart', 'extended_chart.utils'],
      install_requires=['lightweight-charts==1.0.18.7'],
      zip_safe=False
      )
