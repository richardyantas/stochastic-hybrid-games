
# .PHONY: test
# test: 
# 		pytest -q sthocastic_hybrid_game/src/dataProcessing_test.py
# 		pytest -q sthocastic_hybrid_game/src/dataProcessing_test.py
# all:
# 		echo "all :)"


python stochastic_hybrid_game/src/models/SWH.py  # set perturbations
# previously set pattern.json in mpc.py
python stochastic_hybrid_game/src/run_experiment.py --controller=MPC.Greedy #--perturbations=
python stochastic_hybrid_game/src/run_experiment.py --controller=MPC.Uppaal
python stochastic_hybrid_game/src/viz/visualizer.py
