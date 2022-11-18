from ejemplo2_add_space.money_model import MoneyModel
import matplotlib.pyplot as plt


def basic_example_space():

    model = MoneyModel(3,8,12,0.8)  # CAMBIAR
    while model.celdas_suc != 0:
        model.step()
        print("\n")