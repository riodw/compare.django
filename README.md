New Clone:

```
uv venv
```

## Activate Env
```
source .venv/bin/activate
python manage.py runserver
```

Check python version
```
python --version
```
Should be "Python 3.14.2"

Install packages
```
uv sync
```


## Run Server
```
python manage.py runserver
```

## Setup Databse

### Migrate
```
python manage.py migrate
```

### Create superuser
```
python manage.py createsuperuser
```

## Populate Dummy Data
```
python manage.py populate_dummy_data
```
