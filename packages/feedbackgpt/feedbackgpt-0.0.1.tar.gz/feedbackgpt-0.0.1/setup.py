import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="feedbackgpt",
	version="0.0.1",
	author="Kunal Tangri, Noah Faro",
	description="A GPT wrapper that learns from user feedback",
	long_description=long_description,
	long_description_content_type="text/markdown",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent"
	],
	python_requires='>=3.6',
	py_modules=["feedbackgpt"],
	package_dir={'':'feedbackgpt/src'},
	install_requires=['openai', 'numpy', 'pinecone-client']
)
