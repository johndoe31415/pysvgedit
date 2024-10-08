import setuptools

with open("README.md") as f:
	long_description = f.read()

setuptools.setup(
	name = "pysvgedit",
	packages = setuptools.find_packages(),
	version = "0.0.6rc0",
	license = "gpl-3.0",
	description = "Native Python library to create and edit SVG documents",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	author = "Johannes Bauer",
	author_email = "joe@johannes-bauer.com",
	url = "https://github.com/johndoe31415/pysvgedit",
	download_url = "https://github.com/johndoe31415/pysvgedit/archive/v0.0.6rc0.tar.gz",
	keywords = [ "svg" ],
	install_requires = [
	],
	entry_points = {
		"console_scripts": [
			"svgmakorender = pysvgedit.apps.MakoRendererApp:MakoRendererApp.main",
			"svganimationrender = pysvgedit.apps.AnimationRendererApp:AnimationRendererApp.main",
			"svgvalidate = pysvgedit.apps.ValidatorApp:ValidatorApp.main",
		]
	},
	include_package_data = False,
	classifiers = [
		"Development Status :: 4 - Beta",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3 :: Only",
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"Programming Language :: Python :: 3.10",
	],
)
