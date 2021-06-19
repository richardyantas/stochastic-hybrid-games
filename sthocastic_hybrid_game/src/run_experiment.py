
import multiprocessing
import argparse
import importlib
from sthocastic_hybrid_game.src.controllers import UPPAAL, MPC
from sthocastic_hybrid_game.src.viz import viz2


def _import_class(module_and_clas_name: str) -> type:
    """Import class from a module, e.g. 'sthocastics_hybrid_game.controllers.UPPAAL'"""
    module_name, class_name = module_and_clas_name.rsplit(".", 1)
    module = importlib.import_module(module_name)
    class_ = getattr(module, class_name)
    return class_


def _setup_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--data_class", type=str, default="SOLAR")
    parser.add_argument("--model_class", type=str, default="SWH")
    parser.add_argument("--controller_class", type=str, default="MPC")
    temp_args, _ = parser.parse_known_args()
    data_class = _import_class(
        f"sthocastic_hybrid_game.src.data.{temp_args.data_class}")
    model_class = _import_class(
        f"sthocastic_hybrid_game.src.models.{temp_args.model_class}")
    controller_class = _import_class(
        f"sthocastic_hybrid_game.src.controllers.{temp_args.controller_class}")
    data_group = parser.add_argument_group("Data Args")
    data_class.add_to_argparse(data_group)
    model_group = parser.add_argument_group("Model Args")
    model_class.add_to_argparse(model_group)
    controller_group = parser.add_argument_group("Controller Args")
    controller_class.add_to_argparse(controller_group)
    return parser


def main():
    parser = _setup_parser()
    args = parser.parse_args()
    data_class = _import_class(
        f"sthocastic_hybrid_game.src.data.{args.data_class}")
    model_class = _import_class(
        f"sthocastic_hybrid_game.src.models.{args.model_class}")
    controller_class = _import_class(
        f"sthocastic_hybrid_game.src.controllers.{args.controller_class}")
    data = data_class(args)
    model = model_class(data_config=data.config(),
                        disturbs=data.loader_data(), args=args)
    controller = controller_class(
        data_config=data.config(), disturbs=data.loader_data(), model=model, args=args)

    state_times = [0]
    tau = controller.get_tau()
    nrSteps = controller.get_nrSteps()
    life_time = data.config()["life_time"]
    state = model.get_initial_state()
    states = [state]
    control_times = []
    u_actions = model.get_uncontrollable_actions()
    # in minutes k=3, d boundary over R [n + e, m + e]
    for i in range(0, life_time):
        if i % (tau) == 0:
            if i + nrSteps*tau >= life_time:  # regresar el tamanio del ultimo patron IMPORTANTE !!!
                break
            controllable_mode = controller.control(state, i)
            control_times.append(i)
        state = model.update(controllable_mode, u_actions[i], state, i)
        state_times.append(i)
        states.append(list(state))
    print("Simulation completed!")
    print("Plotting ..")
    c_actions = controller.get_controllable_actions()
    u_actions = u_actions[0:len(state_times)]
    viz2(states, c_actions, u_actions,
         data.config(), data.loader_data(), control_times, state_times)
    return


if __name__ == '__main__':
    main()
