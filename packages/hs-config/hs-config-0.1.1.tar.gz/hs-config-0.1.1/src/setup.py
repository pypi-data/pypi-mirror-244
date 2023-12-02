from setuptools import setup

setup(
    name='hs-config',
    version='0.1.1',
    packages=[
        "pydantic[dotenv]>=2.5.1",
        "pydantic-settings>=2.1.0",
    ],
    package_dir={'': 'src'},
    url='https://github.com/x-haose/hs-config',
    license='MIT',
    author='昊色居士',
    author_email='xhrtxh@gmail.com',
    description='基于pydantic的python项目通用配置库'
)
