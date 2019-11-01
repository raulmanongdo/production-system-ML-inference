HOME=$(pwd)

####################
## Build Commands ##
####################

build-utilities:
	cp src/utilities src/training/ -r
	cp src/utilities src/inference/ -r
build-inference: build-utilities
	rm ./build/inference -rf && \
	mkdir -p ./build && \
	cp -r ./src/inference ./build/inference && \
	pip install -r ./build/inference/requirements.txt -t ./build/inference && \
	rm ./build/inference/*.dist-info ./build/inference/__pycache__/ -rf && \
	cd ./build/inference && \
	zip -r ../inference.zip .
build: build-utilities build-inference

#########################
## Deployment Commands ##
#########################

push: build
	aws s3 cp build/training.zip s3://adss-single-lambda-terraform/source/training.zip
	aws s3 cp build/inference.zip s3://adss-single-lambda-terraform/source/inference.zip
deploy: push 
	cd tfn && terraform apply
destroy:
	cd tfn && terraform destroy

####################
## Other Commands ##
####################

tests: build-utilities
	python -m pytest test/