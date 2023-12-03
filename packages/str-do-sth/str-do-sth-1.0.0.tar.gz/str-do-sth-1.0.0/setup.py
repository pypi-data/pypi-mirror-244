import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="str-do-sth",
  version="1.0.0",
  author="Cuber_AHZ",
  author_email="2119244804@qq.com",
  description="it can take STR to INT,FLOAT,BOOL,LIST",
  long_description=long_description,
  long_description_content_type="text/markdown",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)
