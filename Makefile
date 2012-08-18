compile_less:
	lessc promise/static/less/main.less > promise/static/css/main.css

watch:
	echo "Watching less files..."
	watchr -e "watch('less/.*\.less') { system 'make compile_less' }"

.PHONY: watch
