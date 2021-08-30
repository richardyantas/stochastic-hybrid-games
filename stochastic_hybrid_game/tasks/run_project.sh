# export PYTHONPATH=.
# python ./stochastic_hybrid_game/src/run_experiment.py

# cd build && cmake .. && make

# python stochastic_hybrid_game/src/models/SWH.py  # to generate perturbations

python stochastic_hybrid_game/src/run_experiment.py --controller=MPC.Greedy
python stochastic_hybrid_game/src/run_experiment.py --controller=MPC.Uppaal

# python stochastic_hybrid_game/src/viz/visualizer.py