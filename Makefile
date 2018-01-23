lambdazip:
	sudo rm -rf ./lambda/build
	mkdir ./lambda/build
	sudo pip install soundcloud -t ./lambda/build
	sudo pip install flask -t ./lambda/build
	cp lambda/skill.py ./lambda/build/skill.py
	cp lambda/ssml_builder.py ./lambda/build/ssml_builder.py
	cp lambda/queue_manager.py ./lambda/build/queue_manager.py
	cp lambda/flask_ask/flask_ask ./lambda/build/flask_ask -r
	sudo pip install -r ./lambda/flask_ask/requirements.txt -t ./lambda/build
	cd ./lambda/build
	zip skill . -r
	mv skill.zip ../skill.zip
	cd ../..

lambdaupdate:
	cp lambda/skill.py ./lambda/build/skill.py
	cp lambda/ssml_builder.py ./lambda/build/ssml_builder.py
	cp lambda/queue_manager.py ./lambda/build/queue_manager.py
	cd ./lambda/build
	zip skill . -r
	