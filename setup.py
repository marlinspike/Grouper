import setuptools

requirements = [
    'PTable==0.9.2',
    'Click>=7.0',
    'prettytable>=7'
]

setuptools.setup(
    name="azure-nsg-easy-management",
    version="0.90",
    packages=setuptools.find_packages(),
    install_requires=requirements,

    package_data={
        '': ['*.txt', '*.rst']
    },

    # metadata to display on PyPI
    author="Reuben Cleetus",
    author_email="reuben@cleet.us",
    description="Azure NSG Rules easily managed via a CSV File, which Gruoper than exports as complete ARM templates that you can place into Source Control and use directly.",
    license="MIT",
    keywords="Azure, NSG, Rules, Management"

)