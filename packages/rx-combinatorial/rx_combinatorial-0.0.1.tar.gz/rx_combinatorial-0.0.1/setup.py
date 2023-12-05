from setuptools import setup, find_packages

import glob

setup(
    name            = 'rx_combinatorial',
    version         = '0.0.1',
    description     = 'Project used to calculate combinatorial background shapes',
    long_description= '',
    scripts         = [
        'scripts/cb_job', 
        'scripts/cb_submit', 
        'scripts/get_scales', 
        'scripts/get_cb_data',
        'scripts/plot_uncertainties', 
        'scripts/plot_data'],
    package_dir     = {'' : 'src'},
    install_requires= open('requirements.txt').read()
)

