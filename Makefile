.PHONY: list sim data clean-generated

VAR ?= variants/srad/ours_192lane

list:
	@find variants -maxdepth 2 -name Makefile -print

data:
	$(MAKE) -C $(VAR) data

sim:
	$(MAKE) -C $(VAR) sim

clean-generated:
	powershell -ExecutionPolicy Bypass -File scripts/clean-generated.ps1
