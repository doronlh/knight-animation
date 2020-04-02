from setuptools import setup

setup(
    name='Knight Animation',
    version='0.1',
    description='Generate animations of knight traversing a chessboard',
    url='http://github.com/doronlh/knight-animation',
    author='Doron Horwitz',
    author_email='doron@at-bay.com',
    packages=['knight_animation'],
    zip_safe=False,
    install_requires=[
        'Pillow < 7.1.0',
        'cairosvg',
        'imageio',
        'python-chess',
    ],
)
