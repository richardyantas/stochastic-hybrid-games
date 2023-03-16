
help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

conda-update:
	conda env update --prune -f environment.yml
	echo "!!!RUN RIGHT NOW:\nconda activate ucsp-solar"

pip-tools:
	python -m pip install pip-tools
	pip-compile requirements/prod.in && pip-compile requirements/dev.in
	pip-sync requirements/prod.txt requirements/dev.txt

run:
	python stochastic_hybrid_game/src/run_experiment.py --controller=MPC.Uppaal
test:
	pytest -q sthocastic_hybrid_game/src/dataProcessing_test.py
lint:
	tasks/lint.sh


# .PHONY: test
# test: 
# 		pytest -q sthocastic_hybrid_game/src/dataProcessing_test.py
# all:
# 		echo "all :)"


# python stochastic_hybrid_game/src/models/SWH.py  # set perturbations
# # previously set pattern.json in mpc.py
# python stochastic_hybrid_game/src/run_experiment.py --controller=MPC.Greedy #--perturbations=
# python stochastic_hybrid_game/src/run_experiment.py --controller=MPC.Uppaal
# python stochastic_hybrid_game/src/viz/visualizer.py

# stochastic_hybrid_game