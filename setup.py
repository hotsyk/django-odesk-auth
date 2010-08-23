from distutils.core import setup

version = __import__('odesk_auth').get_version()


setup(name='django-odesk-auth',
      version=version,
      description='',
      long_description='',
      author='oDesk',
      author_email='python@odesk.com',
      packages = ['odesk_auth',],
      install_requires = ['python-odesk', ],
      classifiers=['Development Status :: 1 - Alpha',
                   'Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: Utilities'],)