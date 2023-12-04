from setuptools import setup, find_packages

setup(
    name =                      'known',
    version =                   '0.0.14',
    url =                       'https://github.com/Nelson-iitp/known',
    author =                    'Nelson.S',
    author_email =              'mail.nelsonsharma@gmail.com',
    description =               'Module :: known',
    packages =                  find_packages(include=['known', 'known.*']),
    classifiers=                ['License :: OSI Approved :: MIT License'],
    package_dir =               { '' : 'module'},
    install_requires =          [],
    include_package_data =      True
)   