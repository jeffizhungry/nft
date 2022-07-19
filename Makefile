clean:
	rm -rf ./images

images:
	python3 generate_images.py

metadata:
	python3 generate_metadata.py