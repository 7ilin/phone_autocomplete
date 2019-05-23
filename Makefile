install:
		pip install -r requirements.txt

install_db:
		python phone_autocomplete.py install_db

test:
		pytest
