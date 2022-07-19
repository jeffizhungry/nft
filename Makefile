clean:
	rm -rf ./images

images:
	python3 generate_images.py

.PHONY: metadata
metadata:
	python3 generate_metadata.py