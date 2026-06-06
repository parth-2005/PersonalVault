.PHONY: build-windows build-linux clean

ifeq ($(OS),Windows_NT)
PYTHON := .\venv\Scripts\python.exe
else
PYTHON := ./venv/bin/python
endif

build-windows:
	$(PYTHON) -m PyInstaller --noconfirm build_windows.spec

build-linux:
	$(PYTHON) -m PyInstaller --noconfirm build_linux.spec

clean:
	rm -rf build dist *.spec
