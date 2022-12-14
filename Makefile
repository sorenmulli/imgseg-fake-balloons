install:
	pip install --editable . --upgrade 
data:
	python imgseg02561/extract_dataset.py dataset --name v1 --N 1000
make cleandata:
	rm -r dataset/**/*.png
