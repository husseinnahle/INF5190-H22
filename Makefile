export FLASK_APP=index.py

run: db doc
	flask run --host=0.0.0.0

db:
	rm -f db/database.db
	sqlite3 db/database.db < db/database.sql

doc:
	raml2html doc.raml > templates/doc.html

install:
	sudo pip install -r requirements.txt

.PHONY: db