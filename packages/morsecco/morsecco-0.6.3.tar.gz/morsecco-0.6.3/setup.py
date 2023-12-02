from setuptools import setup

setup(
    name='morsecco',
    version='0.6.3',    
    description='A minimalistic, but mighty programming language',
    url='https://github.com/Philipp-Sasse/morsecco',
    package_data={ '': ['help.txt'] },
    include_package_data=True,
    author='Philipp Sasse',
    author_email='Philipp.Sasse@sonnenkinder.org',
    license='BSD 2-clause',
    packages=['morsecco'],
    install_requires=[
                      ],
    entry_points={
        'console_scripts': [
            'morsecco=morsecco.morsecco:main',
        ],
    },

    classifiers=[
        'Development Status :: 3 - Alpha',
	'Environment :: Console',
	'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: OS Independent',
	'Operating System :: MacOS :: MacOS X',
	'Operating System :: POSIX :: Linux',        
	'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
	'Topic :: Software Development :: Interpreters',
    ],
)
