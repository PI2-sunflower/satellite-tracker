from setuptools import setup, find_packages


def get_requirements():
    with open('requirements.txt', 'r') as f:
        requirements = f.read().split('\n')
        return requirements


setup(
    name='tracker',
    version='0.0.1',
    description='Predicts satellites orbital parameters using TLE',
    url='https://github.com/PI2-sunflower/satellite-tracker',
    license='GPL v3.0',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*', 'notebooks*']),
    install_requires=get_requirements(),
    python_requires='>=3',
)
