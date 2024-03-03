SRC = src
ROUTER = router
FILE_IO = file_io
P_n_R = place_and_route
STRUCTS = structures
UI = ui
PYCACHE = __pycache__

.PHONY: run run_win help help_win

# Linux runs
run:
	python3 ./$(SRC)/$(ROUTER)/router.py

help:
	python3 ./$(SRC)/$(ROUTER)/router.py -h

# Windows runs
run_win:
	python .\$(SRC)\$(ROUTER)\router.py

help_win:
	python .\$(SRC)\$(ROUTER)\router.py -h

# Cleanups
.PHONY: clean clean_win
# Cleanup for linux executions
clean:
	rm -rf ./$(SRC)/$(ROUTER)/$(PYCACHE)
	rm -rf ./$(SRC)/$(ROUTER)/$(FILE_IO)/$(PYCACHE)
	rm -rf ./$(SRC)/$(ROUTER)/$(P_n_R)/$(PYCACHE)
	rm -rf ./$(SRC)/$(ROUTER)/$(STRUCTS)/$(PYCACHE)
	rm -rf ./$(SRC)/$(ROUTER)/$(UI)/$(PYCACHE)

# Cleanup for windows executions
clean_win:
	rd /s /q $(SRC)\$(ROUTER)\$(PYCACHE)
	rd /s /q $(SRC)\$(ROUTER)\$(FILE_IO)\$(PYCACHE)
	rd /s /q $(SRC)\$(ROUTER)\$(P_n_R)\$(PYCACHE)
	rd /s /q $(SRC)\$(ROUTER)\$(STRUCTS)\$(PYCACHE)
	rd /s /q $(SRC)\$(ROUTER)\$(UI)\$(PYCACHE)