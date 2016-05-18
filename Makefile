help:
	@echo 'Makefile for pkgen                       '
	@echo '                                         '
	@echo 'Usage:                                   '
	@echo '    make install    install as a package '

requirements:
	pip install -i http://pypi.douban.com/simple -r requirements.txt --trusted-host pypi.douban.com

install: requirements
	python setup.py install --record install.record
	@echo
	@echo "Install finished"
