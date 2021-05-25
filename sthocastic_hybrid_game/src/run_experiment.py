
import multiprocessing
import argparse
import importlib
from sthocastic_hybrid_game.src.controllers import UPPAAL, MPC


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
        data_config=data.config(), model=model, args=args)
    t = 0
    dt = 60
    num_tau = controller.get_tau()
    for i in range(0, data.config()["life_time"]):
        if i >= (data.config()["life_time"] - len(controller.get_pat())*num_tau):
            break
        if i % (num_tau) == 0:
            pat = controller.control(int(i/num_tau))
        t = t + dt

    print("completed!")
    return


if __name__ == '__main__':
    main()
