CONTENT = content/ancients.json
DIST = dist/index.html
TESTS = tests/test_mobile.py

.PHONY: all content build test clean

all: content build test

content:
	python3 tools/extract_content.py
	python3 tools/check_content.py

build: $(CONTENT) build.py $(wildcard templates/*)
	python3 build.py

test: $(DIST)
	python3 $(TESTS)

clean:
	rm -f $(DIST)