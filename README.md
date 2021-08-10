# Flask Conference API

## API Documentation
https://documenter.getpostman.com/view/3760039/Tzz4QJvb

## Setup
Setup Python virtualenviroment and install requirements
```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```
Connect Databse via .env file. Please refer .env.example

Run Database Migrations
```
python migrate.py db migrate
python migrate.py db upgrade
```
Run the application
```
python run.py
```

## Running Automated Tests
```
pytest --disable-pytest-warnings
```
## Successful Test Result Sample
<img src="https://res.cloudinary.com/vannucherum/image/upload/v1628600404/github/result.png">