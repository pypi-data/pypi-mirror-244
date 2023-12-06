from pathlib import Path
from setuptools import setup





setup(
    name='robocraft',
    version='1.1.3',
    description='Pythonization of ComputerCraft Minecraft mod. Write Python instead Lua!',
    author='Artem Robocodovich',
    author_email='garo109696@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Games/Entertainment',
    ],
    keywords='computercraft minecraft',
    package_data={'robocraft': ['back.lua']},
    install_requires=['aiohttp == 3.8.5', 'greenlet'],
    entry_points={
        'console_scripts': ['robocraft = robocraft.server:main'],
    },
)
