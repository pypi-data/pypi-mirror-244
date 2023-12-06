from setuptools import setup

setup(
  name='webfleet_connect',
  version='0.1.0',
  description='The WEBFLEET.connect API connects software applications with the Webfleet fleet management solution. Via WEBFLEET.connect you can enhance the value of all types of business solutions, including routing and scheduling optimization, ERP, Transport Management System (TMS), supply chain planning, asset management, and much more.',
  url='https://github.com/movomx/webfleet_connect_python',
  author='movomx',
  author_email='alex.guajardo@movomx.com',
  license='MIT License',
  packages=['webfleet_connect'],
  install_requires=['requests', 'python-dotenv'],

  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Topic :: Software Development :: Libraries'
  ]
)
