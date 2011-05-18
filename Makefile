MONGOD_DB_PATH=/tmp/mongod_db

test:
	@echo 'Running all tests...'
	@nosetests -w tests

run:
	@python main.py --debug

run_mongod:
	@mkdir -p $(MONGOD_DB_PATH)
	@mongod --dbpath $(MONGOD_DB_PATH)

coverage:
	nosetests --with-coverage --cover-package=portal -w tests
	coverage html --d coverage_html --include=portal/*
	open coverage_html/index.html

submodule_update:
	@echo 'Updating submodules...'
	@git submodule init
	@git submodule update
	@mkdir -p lib

copy_libs: submodule_update
	@echo 'Updating Flask...'
	@cp -r deps/flask/flask lib/
	@echo 'Updating Werkzeug...'
	@cp -r deps/werkzeug/werkzeug lib/
	@echo 'Updating Jinja2...'
	@cp -r deps/jinja2/jinja2 lib/

	@echo 'Updating wtforms...'
	@cp -r deps/wtforms/wtforms lib/

	@echo 'Updating pymongo...'
	@cp -r deps/pymongo/pymongo lib/
	@cp -r deps/pymongo/bson lib/
	@cp -r deps/pymongo/gridfs lib/

	@echo 'Updating mongoalchemy...'
	@cp -r deps/mongoalchemy/mongoalchemy lib/
	@cp -r deps/flask-mongoalchemy/flaskext lib/

	@echo 'Updating beanstalkc...'
	@cp -r deps/beanstalkc/beanstalkc.py lib/


libs: copy_libs

bootstrap: libs
	@echo 'Creating the settings.py file...'
	@python mk_settings.py
	@echo 'Done.'

build: bootstrap

clean:
	@echo 'Cleaning...'
	@find . -name "*.pyc" -exec rm -f {} \;
	@echo 'Done.'
