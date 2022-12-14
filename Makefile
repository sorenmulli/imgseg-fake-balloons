install:
	pip install --editable . --upgrade 

data:
	python imgseg02561/extract_dataset.py dataset --name v1 --N 1000

cleandata:
	rm -r dataset/**/*.png

train:
	python imgseg02561/train.py training --name resnet50
