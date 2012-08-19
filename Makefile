STATIC_ROOT=apps/promise/static

compile_less:
	lessc ${STATIC_ROOT}/less/main.less > ${STATIC_ROOT}/css/main.css

watch:
	echo "Watching less files..."
	watchr -e "watch('less/.*\.less') { system 'make compile_less' }"

setup_local:
	gem install watchr
	npm install less -g
	pip install -r conf/requirements-local.txt

reset_local_database:
	mysql -uroot -e"DROP DATABASE promise_local; CREATE DATABASE promise_local;"
	python manage.py syncdb
	python manage.py generate_profiles_and_promises

.PHONY: watch
