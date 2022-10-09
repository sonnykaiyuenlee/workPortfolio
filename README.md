# Equity Model



## Getting started
1. Create a virtual environment (`python -m venv env`)
2. Activate environment (`source env/bin/activate` on Mac/Linux)
3. Install requirements (`pip install -r requirements.txt`)
4. `cd` into backend directory
5. Make migrations (`python manage.py makemigrations --settings=backend.settings.base`)
6. Start Django app (`python manage.py runserver --settings=backend.settings.base`)


## Development notes
Make sure you're always leaving legible comments on your code and writing tests for
it. (`python manage.py test re_model --settings=backend.settings.base`)
