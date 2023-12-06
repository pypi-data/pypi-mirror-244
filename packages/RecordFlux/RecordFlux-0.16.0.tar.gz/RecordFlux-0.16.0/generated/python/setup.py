


from setuptools import setup, find_packages


setup(
    name='Librflxlang',
    version='0.15.1.dev30+g9ab5b4f93.d20231129',
    packages=['librflxlang'],
    package_data={
        'librflxlang':
            ['*.{}'.format(ext) for ext in ('dll', 'so', 'so.*', 'dylib')]
            + ["py.typed"],
    },
    zip_safe=False,
)
