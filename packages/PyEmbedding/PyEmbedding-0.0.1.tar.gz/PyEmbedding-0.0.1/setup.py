from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Effortlessly transform data into meaningful vector representations in Python.'
LONG_DESCRIPTION = """PyEmbedding is a versatile Python package designed to streamline the implementation and utilization of embedding techniques in various applications. Whether you're working with natural language processing, computer vision, or any domain that involves transforming data into meaningful vector representations, PyEmbedding provides a user-friendly interface and a robust set of tools."""

# Setting up
setup(
        name="PyEmbedding", 
        version=VERSION,
        author="Kyle Ng",
        author_email="<pyembedding@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], 
        
        keywords=['python', 'embedding'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
            'Natural Language :: English',
        ]
)