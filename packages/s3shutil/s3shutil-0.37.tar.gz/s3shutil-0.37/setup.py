from distutils.core import setup

setup(
  name = 's3shutil',
  packages = ['s3shutil'],

  long_description=open('README.rst').read(),
  long_description_content_type='text/x-rst',
  version='0.37',
  license='MIT',
  description = 'Easy pythonic API to copy and sync to and from s3',
  url = 'https://github.com/andyil/s3shutil',
  download_url = 'https://github.com/andyil/s3shutil/archive/0.28.tar.gz',
  keywords = ['aws', 's3', 'cloud', 'storage', 'shutil', 'network'],
  install_requires=['boto3'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: Information Technology',
    'Intended Audience :: System Administrators',
    'Topic :: Internet',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
  ],
)
