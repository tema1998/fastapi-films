from setuptools import setup

setup(
    name='fastapi-films',
    version='0.0.1',
    author='tema1998',
    author_email='artemvol1998@gmail.com',
    description='FastAPI app',
    install_requires=[
        'fastapi==0.110.0',
        'uvicorn==0.28.0',
        'SQLAlchemy==2.0.28',
        'pytest==8.1.1',
        'requests==2.31.0',
        'pydantic==2.6.4',
        'alembic==1.13.1',
        'asyncpg==0.29.0',
        'envparse==0.2.0',
        'psycopg2==2.9.9',
    ],
    scripts=['app/main.py', 'scripts/create_db.py']
)
