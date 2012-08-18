STATIC_ROOT=apps/promise/static

compile_less:
	lessc ${STATIC_ROOT}/less/main.less > ${STATIC_ROOT}/css/main.css

watch:
	echo "Watching less files..."
	watchr -e "watch('less/.*\.less') { system 'make compile_less' }"

.PHONY: watch
