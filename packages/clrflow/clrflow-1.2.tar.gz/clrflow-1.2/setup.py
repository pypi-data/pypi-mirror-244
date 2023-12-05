from distutils.core import setup
setup(
  name = 'clrflow',
  packages = ['clrflow'],
  version = '1.2',
  license='MIT',
  description = 'A text formatting module with additional beauty functions and compact tools.',
  author = 'rver',                   
  author_email = 'rverflow@gmail.com',      
  url = 'https://github.com/rver38/clrflow/',   
  download_url = 'https://github.com/rver38/clrflow/archive/refs/tags/v1.2.tar.gz',    
  keywords = ['color','gradient','text','strings','formatting','ansi','format'],   
  install_requires=["numpy"],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
  ],
)
