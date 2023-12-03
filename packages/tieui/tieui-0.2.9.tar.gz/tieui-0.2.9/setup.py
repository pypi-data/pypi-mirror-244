from setuptools import setup, find_packages

setup(
    name='tieui',
    version='0.2.9',
    packages=find_packages(),
    install_requires=[
        'flask_cors',
        'flask_socketio',
        'flask',
        'json',
        'os',
        'signal',
        'openai',
        'gunicorn',
        'eventlet',
        'stripe',
        'sendgrid',
        'websocket-client',
        're',
        'tempfile',
    ],
    author='TieUi',
    author_email='info@tieUi.com',
    description='Tie Ui package for local development',
    url='https://tieui.app',
)