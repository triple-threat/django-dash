STATIC_ROOT=apps/promise/static

compile_less:
	lessc ${STATIC_ROOT}/less/main.less > ${STATIC_ROOT}/css/main.css

watch:
	echo "Watching less files..."
	watchr -e "watch('less/.*\.less') { system 'make compile_less' }"

pip_install_local:
	pip install -r conf/requirements-local.txt

setup_local: pip_install_local
	gem install watchr
	npm install less -g

reset_local_database:
	mysql -uroot -p -e"DROP DATABASE promise_local; CREATE DATABASE promise_local;"
	python manage.py syncdb
	python manage.py generate_profiles_and_promises

run: pip_install_local reset_local_database
	python manage.py runserver

.PHONY: watch
