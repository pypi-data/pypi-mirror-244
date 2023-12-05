from setuptools import setup, find_packages

setup(
    name='mousie_mover',
    version='2.0.0',
    author='Owen Kelly',
    author_email='okelly4408@gmail.com',
    description='Moves cursor in all sorts of pattterns and durations',
    packages=find_packages(),
    install_requires=["argparse", "pyautogui", "screeninfo"],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)