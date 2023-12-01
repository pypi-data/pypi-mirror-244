from qrs import __version__

from setuptools import setup

setup(
	name='qrs',
	version=__version__,
	description='Tool for Quarrel (and other word games)',
	long_description=open('README.md', 'r').read(),
	long_description_content_type='text/markdown',
	url='https://github.com/silvncr/qrs',
	author='silvncr',
	include_package_data=True,
	license='MIT',
	packages=['qrs'],
	package_data={
		'qrs': [
			'*.py',
			'*.txt',
		],
	},
	setup_requires=['pytest_runner'],
	python_requires='>=3.6',
	scripts=[],
	tests_require=['pytest'],
	entry_points={
		'console_scripts': [
			'qrs=qrs:main'
		]
	},
	zip_safe=True,
	classifiers=[
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Topic :: Games/Entertainment :: Board Games',
		'Topic :: Games/Entertainment :: Puzzle Games',
		'Topic :: Software Development :: Libraries',
		'Topic :: Software Development :: Libraries :: Python Modules',
	],
)
