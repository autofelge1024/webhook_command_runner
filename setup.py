#!/usr/bin/env python3


from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
	name="webhook_command_runner",
	version="1.0.0",
	url="https://github.com/autofelge1024/webhook_command_runner",
	license="MIT",
	author="autofelge1024",
	author_email="mail@autofelge1024.de",
	description="A simple and small webserver to react to webhook-calls by running commands."
				"For simplicity, webhook-urls and scripts are configured in a configfile.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: POSIX",
	],
	packages=["webhook_command_runner"],
	entry_points={"console_scripts": ["webhook-command-runner = webhook_command_runner.webserver:main"]},
	python_requires=">=3.4",  # todo: check
)