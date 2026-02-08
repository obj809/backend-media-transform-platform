# commands.md

## venv

python3 -m venv venv

source venv/bin/activate

pip freeze > requirements.txt

pip install -r requirements.txt

## run server

./venv/bin/python -m uvicorn app.main:app --reload

## test endpoints

python scripts/test_endpoints.py

## run tests

pytest -v