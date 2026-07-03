# eevn_sec_policy_templates — tooling entry points (stdlib Python only)

OUT    ?= ../rendered-policies
CONFIG ?= tools/example.conf

.PHONY: check render help

help:
	@echo "make check                     - lint template structure, IDs, cross-refs, README index"
	@echo "make render [OUT=dir] [CONFIG=file] - instantiate the set into OUT using CONFIG"

check:
	python3 tools/check_templates.py

render:
	python3 tools/render.py --out $(OUT) --config $(CONFIG) --strip-comments
