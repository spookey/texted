CMD_VENV		:=	virtualenv
DIR_VENV		:=	venv
VER_PY			:=	3.7

CMD_ISORT		:=	$(DIR_VENV)/bin/isort
CMD_PIP			:=	$(DIR_VENV)/bin/pip$(VER_PY)
CMD_PYLINT		:=	$(DIR_VENV)/bin/pylint

DIR_SITE		:=	$(DIR_VENV)/lib/python$(VER_PY)/site-packages
LIB_CLICK		:=	$(DIR_SITE)/click
LIB_PILLOW		:=	$(DIR_SITE)/PIL


SCR_TEXTED		:=	texted.py


.PHONY: help
help:
	@echo "texted makefile"
	@echo "---------------"
	@echo
	@echo "requirements         install requirements"
	@echo "requirements-dev     install requirements for developing"
	@echo
	@echo "sort                 run $(CMD_ISORT) on $(SCR_TEXTED)"
	@echo "lint                 run $(CMD_PYLINT) on $(SCR_TEXTED)"

$(DIR_VENV):
	$(CMD_VENV) -p "python$(VER_PY)" "$(DIR_VENV)"

$(LIB_CLICK) $(LIB_PILLOW): $(DIR_VENV)
	$(CMD_PIP) install -r "requirements.txt"

$(CMD_ISORT) $(CMD_PYLINT): $(DIR_VENV)
	$(CMD_PIP) install -r "requirements-dev.txt"

.PHONY: requirements
requirements: $(LIB_CLICK) $(LIB_PILLOW)

.PHONY: requirements-dev
requirements-dev: $(CMD_ISORT) $(CMD_PYLINT)


define _sort
	$(CMD_ISORT) -cs -fss -m5 -y -rc $(1)
endef

.PHONY: sort
sort: $(CMD_ISORT)
	$(call _sort,"$(SCR_TEXTED)")


define PYLINT_MESSAGE_TEMPLATE
{C} {path}:{line}:{column} - {msg}
  ↪  {category} {module}.{obj} ({symbol} {msg_id})
endef
export PYLINT_MESSAGE_TEMPLATE

define _lint
	$(CMD_PYLINT) \
		--disable "C0111" \
		--msg-template="$$PYLINT_MESSAGE_TEMPLATE" \
		--output-format="colorized" \
			$(1)
endef

.PHONY: lint
lint: $(CMD_PYLINT)
	$(call _lint,"$(SCR_TEXTED)")
