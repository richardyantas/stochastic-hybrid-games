
import multiprocessing
import argparse
import importlib
from sthocastic_hybrid_game.src.controllers import UPPAAL, MPC
from sthocastic_hybrid_game.src.viz import viz, viz2


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
                        disturbs=data.loader_data(), u_actions=data.uncontrollable_action_generation(), args=args)
    controller = controller_class(
        data_config=data.config(), disturbs=data.loader_data(), model=model, args=args)
    t = 0
    dt = 60
    times = [0]
    num_tau = controller.get_tau()
    # K = 3 (maximum size), D, thus send 3 steps more to uppal T,I
    for i in range(0, data.config()["life_time"]):
        # here is the problem !! it can be exact!!
        if i % (num_tau) == 0:
            # if (int(i/num_tau)+len(controller.get_pat()) > int(data.config()["life_time"]/num_tau)):
            #    break
            pat = controller.control(int(i/num_tau))
            times.append(i)  # here !
        t = t + dt

    print("Simulation completed!")
    print("Plotting ..")

    # one idea is to consider an aproximation error so one strategy  would be increasy the boundary over R [n + e, m + e] in python
    c_actions = controller.get_controllable_actions()
    u_actions = controller.get_uncontrollable_actions()
    c_actions.pop()
    viz2(controller.get_states(), c_actions, u_actions,
         data.config(), data.loader_data(), times)
    return


if __name__ == '__main__':
    main()
