from setuptools import Extension, setup

ext = Extension(
    name='bgra',
    sources=['bgra.c'],
    py_limited_api=True,
    define_macros=[
        ("Py_LIMITED_API", 0x030B0000),
    ],
)

setup(
    name='bgra',
    version='0.1.0',
    ext_modules=[ext],
)
