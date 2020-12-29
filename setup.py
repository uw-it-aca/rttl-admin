import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/rttl-admin>`_.
"""

# The VERSION file is created by travis-ci, based on the tag name
version_path = 'rttl_admin/VERSION'
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

url = "https://github.com/uw-it-aca/rttl-admin"
setup(
    name='RTTL Admin Application',
    version=VERSION,
    packages=['rttl_admin'],
    author="UW-IT AXDD",
    author_email="aca-it@uw.edu",
    include_package_data=True,
    install_requires=[
        'Django>=2.2.13,<3.0',
        'psycopg2<3.0',
        'uw-memcached-clients>=1.0.5,<2.0',
        'UW-Django-SAML2>=1.5.1,<2.0',
        'UW-RestClients-Core>=1.3.3,<2.0',
        'UW-RestClients-Canvas>=1.1.12,<2.0',
        'Django-SupportTools>=3.4,<4.0',
    ],
    license='Apache License, Version 2.0',
    description=('Django application for supporting UW RTTL'),
    long_description=README,
    url=url,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6'
    ],
)
