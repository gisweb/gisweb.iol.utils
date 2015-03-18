from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='iol.gisweb.utils',
      version=version,
      description="Utilities for Iol Application",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='plone iol',
      author='Marco Carbone',
      author_email='marco.carbone@gmx.com',
      url='https://github.com/gisweb/iol.gisweb.utils.git',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['iol', 'iol.gisweb'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.api',
          'Products.CMFPlomino',
          'gisweb.iol',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
