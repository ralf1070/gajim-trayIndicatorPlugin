PLUGIN      := tray_indicator
DATA_HOME   ?= $(or $(XDG_DATA_HOME),$(HOME)/.local/share)
PLUGINS_DIR ?= $(DATA_HOME)/gajim/plugins
DEST        := $(PLUGINS_DIR)/$(PLUGIN)
VERSION     := $(shell python3 -I -c 'import json; print(json.load(open("$(PLUGIN)/plugin-manifest.json"))["version"])')
ZIP         := $(PLUGIN)_$(VERSION).zip

.PHONY: all install uninstall dist clean

all: dist

install:
	rm -rf "$(DEST)"
	mkdir -p "$(DEST)"
	cp $(PLUGIN)/*.py $(PLUGIN)/plugin-manifest.json "$(DEST)/"
	@echo "Installed to $(DEST) - restart Gajim to load it"

uninstall:
	rm -rf "$(DEST)"

dist: $(ZIP)

$(ZIP): $(wildcard $(PLUGIN)/*.py) $(PLUGIN)/plugin-manifest.json
	rm -f "$@"
	zip -r "$@" $(PLUGIN) -x '*/__pycache__/*'

clean:
	rm -f $(PLUGIN)_*.zip
	rm -rf $(PLUGIN)/__pycache__
