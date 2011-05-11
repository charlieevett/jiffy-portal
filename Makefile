test:
	@echo 'Running all tests...'
	@nosetests -w tests

run:
	@python main.py

coverage: coverage_html/index.html
	open coverage_html/index.html

.coverage: portal/*.py portal/templates/*.html
	nosetests --with-coverage --cover-package=portal -w tests

coverage_html/index.html: .coverage
	coverage html --d coverage_html --include=portal/*

submodule_update:
	@echo 'Updating submodules...'
	@git submodule init
	@git submodule update
	@mkdir -p lib

update_werkzeug: submodule_update
	@echo 'Updating Werkzeug...'
	@cp -r deps/werkzeug/werkzeug lib/

update_jinja2: submodule_update
	@echo 'Updating Jinja2...'
	@cp -r deps/jinja2/jinja2 lib/

update_flask: submodule_update
	@echo 'Updating Flask...'
	@cp -r deps/flask/flask lib/

update_wtforms: submodule_update
	@echo 'Updating wtforms...'
	@cp -r deps/wtforms/wtforms lib/

update_pymongo: submodule_update
	@echo 'Updating pymongo...'
	@cp -r deps/pymongo/pymongo lib/
	@cp -r deps/pymongo/bson lib/
	@cp -r deps/pymongo/gridfs lib/

update_mongoalchemy: submodule_update
	@echo 'Updating mongoalchemy...'
	@cp -r deps/pymongo/pymongo lib/

libs: update_werkzeug update_jinja2 update_flask update_wtforms update_pymongo

bootstrap: libs
	@echo 'Creating the settings.py file...'
	@python mk_settings.py
	@echo 'Done.'

build: bootstrap

nose:
	@echo 'Installing nose if needed...'
	@python -c 'import nose' 2>/dev/null || pip install nose

clean:
	@echo 'Cleaning...'
	@find . -name "*.pyc" -exec rm -f {} \;
	@echo 'Done.'
