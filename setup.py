from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

with open("requirements.txt") as f:
    required = [
        l.strip()
        for l in f.read().splitlines()
        if l.strip() and not l.strip().startswith("#")
    ]

setup_args = dict(
    name="imgseg02561",
    version="0.0.1",
    packages=find_packages(),
    author="Søren Winkel Holm",
    author_email="s183911@dtu.dk",
    install_requires=required,
    description="Image segmentation",
    long_description_content_type="text/markdown",
    long_description=readme,
)

if __name__ == "__main__":
    setup(**setup_args)
