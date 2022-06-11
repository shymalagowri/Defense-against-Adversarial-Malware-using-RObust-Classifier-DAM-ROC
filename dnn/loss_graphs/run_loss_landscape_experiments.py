# coding=utf-8
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from os import system
from utils.utils import load_parameters, set_parameter
import shutil
import time


if __name__ == "__main__":
    trained_experiment_model = sys.argv[1]

    original_parameters_filepath = "figure_generation_parameters.ini"
    exp_time = time.strftime("%m_%d_%Hh_%Mm", time.localtime())

    new_params_directory = "experiment_parameters"
    if not os.path.exists(new_params_directory):
        os.mkdir(new_params_directory)
    new_params_name = "loss_landscape_parameters_{exp}_{time}.ini".format(
        exp=trained_experiment_model, time=exp_time)

    new_params_filepath = os.path.join(new_params_directory, new_params_name)
    shutil.copy(original_parameters_filepath, new_params_filepath)
    new_params = load_parameters(new_params_filepath)

    trained_model_directory = "../helper_files"

    model_filepath_base_string = os.path.join(trained_model_directory, "[training_{train_meth}_evasion_{train_meth}]_{exp_name}-model.pt")

    train_methods = ['natural', 'dfgsm_k', 'rfgsm_k', 'grosse', 'topkr']
    evasion_methods = ['rfgsm_k', 'dfgsm_k', 'grosse', 'topkr']

    set_parameter(new_params_filepath, "general", "generate_histogram", "False")

    for train_method in train_methods:
        model_filepath = model_filepath_base_string.format(train_meth=train_method, exp_name=trained_experiment_model)

        set_parameter(new_params_filepath, "general", "training_method", train_method)
        set_parameter(new_params_filepath, "general", "model_weights_path", model_filepath)

        for evasion_method in evasion_methods:
            set_parameter(new_params_filepath, "general", "evasion_method", evasion_method)
            start_time = time.time()
            # source activate nn_mal;
            system("python generate_loss_figures.py {params} {time}".format(
                params=new_params_filepath, time=exp_time))
            print("Time to run loss landscape train/evasion pair:", time.time() - start_time)
