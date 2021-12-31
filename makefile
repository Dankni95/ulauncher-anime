EXT_NAME:=com.github.dankni95.ulauncher-anime
EXT_DIR:=$(shell pwd)

deps: 
	pip install -r requirements.txt

link: 
	ln -s ${EXT_DIR} ~/.local/share/ulauncher/extensions/${EXT_NAME}

dev: 
	ulauncher --no-extensions --dev -v |& grep "ulauncher-anime"

.PHONY: deps link dev 


