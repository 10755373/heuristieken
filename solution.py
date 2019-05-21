import numpy as np
import pandas as pd
import math
import random
from rocket import Rocket
from item import Item
import algorithms as al
import copy
from matplotlib import pyplot as plt
import time

cargo_in_rockets =[]

class Solution():

    def __init__(self):
        """
        Initialize a Rocket
        """
        self.rockets = self.ReadRockets("rockets.csv")
        self.cargolist = self.ReadCargo("CargoLists/CargoList1.csv")
        self.items_count = 0
        self.cost = 0
        self.cargo_in_rockets = []


    # read in all the rockets from csv
    def ReadRockets(self, INPUT_CSV):
        rockets = []
        df = pd.read_csv(INPUT_CSV)
        for index, row in df.iterrows():
            rocket = Rocket(row["Spacecraft"], row["Nation"], row['Payload Mass (kgs)'], row['Payload Volume (m3)'],row['Mass (kgs)'], row['Base Cost($)'], row['Fuel-to-Weight'], row['Payload Mass (kgs)']/row['Payload Volume (m3)'], row['Payload Mass (kgs)']/row['Payload Volume (m3)'], [], 0, 0, row['id'])
            rockets.append(rocket)
        return rockets


    # read in the cargolist from csv
    def ReadCargo(self, INPUT_CSV):
        cargolist = []
        df = pd.read_csv(INPUT_CSV)
        for index, row in df.iterrows():
            item = Item(row['parcel_ID'], row['mass (kg)'], row['volume (m^3)'], row['mass (kg)']/row['volume (m^3)'])
            cargolist.append(item)
        return cargolist


    def count_items(self):
        self.items_count = len(self.cargo_in_rockets)
        print(self.items_count)


    def check_if_correct(self):
            total_filled_mass = 0
            total_filled_volume = 0
            total_volume_items = 0
            total_mass_items = 0
            for rocket in self.rockets:
                total_filled_mass += rocket.filled_weight
                total_filled_volume += rocket.filled_volume
                for item in rocket.items:
                    total_volume_items += item.volume
                    total_mass_items += item.mass
            print(total_filled_mass)
            print(total_mass_items)
            print(total_filled_volume)
            print(total_volume_items)


    def check_mass_volume_unused(self):
        for rocket in self.rockets:
            unused_mass = rocket.payload_mass - rocket.filled_weight
            unused_volume = rocket.payload_volume - rocket.filled_volume
            print(rocket.spacecraft)
            print(unused_mass)
            print(unused_volume)


    def cost_total(self):
        total_cost = 0
        for rocket in self.rockets:
            Fuel_grams = (rocket.mass + rocket.filled_weight)*(rocket.fuel_to_weight)/(1 - rocket.fuel_to_weight)
            print(Fuel_grams)
            cost_rocket = (rocket.base_cost * (10**6)) + round(1000 * Fuel_grams)
            total_cost += cost_rocket
        self.cost = total_cost
        print(self.cost)

    def run_programme_filling_rockets(solution):
        # keep track of chosen options
        chosen_options = []
        # introduce programme and tell user which options there are
        print("A warm welcome to the Space Freight's case from the group 'SpaceX'. You'll have to make a decision which algorithm you'ld like to run in order to fill the rockets with cargo.\n")
        print("First of all, you'll have to decide how you'ld like to fill the rockets.\n"
        "The options are:\n"
        "Option one is based on volume.\n"
        "Option two is based on mass.\n"
        "Option three is based on a density ratio.\n")
        option = input("Option: ")
        if option.isdigit():
            if option == "1":
                chosen_options.append(option)
                runs = 0
                outcomes = []
                while(runs < 15):
                    volume_based = al.fill_cargo_volume(solution)
                    outcomes.append(volume_based)
            elif option == "2":
                chosen_options.append(option)
                runs = 0
                outcomes = []
                while(runs < 15):
                    mass_based = al.fill_cargo_mass(solution)
                    outcomes.append(mass_based)
            elif option == "3":
                chosen_options.append(option)
                print("In order to fill based upon a density-ratio, you'ld have to make a decision between several algorithms.\n")
            else:
                print("Invalid command (command must be either an 1, 2 or 3). Please try again.\n")
                return 1
        else:
            print("Invalid command (command must be an integer). Please try again.\n")
            return 1
        print("There are four options to choose from:\n"
        "Option one is a rondom filler\n"
        "Option two is a random filler combined with a hill climber\n"
        "Option three is a simulated annealing\n"
        "Option four is a simulated annealing combined with a hill climber\n")
        # request for an algorithm
        print("Please choose an option by typing either one of the following numbers: 1, 2, 3 or 4\n")
        # determine ranges
        # results_sim_an_hill_climber_spacex = [0 for i in range(100)]
        # results_sim_an_solo_spacex = [0 for i in range(100)]
        # results_random_fill = [0 for i in range(100)]
        # results_random_fill_hill_climber = [0 for i in range(100)]
        # run chosen algorithm
        command = input("Option: ")
        if command.isdigit():
            if command == "1":
                chosen_options.append(command)
                results_random_fill = []
                # packages = 0
                runs = 0
                while(runs < 5):
                # solution_random_fill = copy.deepcopy(solution_sim_an_hill_climber_spacex)
                    al.random_fill(solution)
                    solution.count_items()
                    results_random_fill.append(solution.items_count)
                    # solution_random_fill = al.random_fill(self)
                    # packages = solution_random_fill.count_items()
                    # results_random_fill.append(packages)
                    runs += 1
                    # print(results_random_fill)
                return results_random_fill
            elif command == "2":
                chosen_options.append(command)
                results_random_fill_hill_climber = [0 for i in range(100)]
                runs = 0
                while(runs < 5):
                    al.random_fill_hill_climber(solution)
                    solution.count_items()
                    results_random_fill_hill_climber[solution.items_count] +=1
                    runs += 1
                return results_random_fill_hill_climber
            elif command == "3":
                chosen_options.append(command)
                results_sim_an_solo_spacex = [0 for i in range(100)]
                runs = 0
                while(runs < 5):
                    al.sim_an_solo_spacex(solution)
                    solution.count_items()
                    results_sim_an_solo_spacex[solution.items_count] += 1
                    runs += 1
                return results_sim_an_solo_spacex
            elif command == "4":
                # solution_sim_an_hill_climber_spacex = Solution()
                chosen_options.append(command)
                results_sim_an_hill_climber_spacex = [0 for i in range(100)]
                runs = 0
                while(runs < 5):
                    random.shuffle(solution.cargolist)
                    al.sim_an_hill_climber_spacex(solution)
                    solution.count_items()
                    results_sim_an_hill_climber_spacex[solution.items_count] += 1
                    # self.items_count += 1
                    # print(self.items_count)
                    runs += 1
                return results_sim_an_hill_climber_spacex
            else:
                print("Invalid command (command must be either an 1, 2, 3, or 4). Please try again.\n")
                return 1
        else:
            print("Invalid command (command must be an integer). Please try again.\n")
            return 1

    def run_programme_optimizing_costs(filling_rockets):
        # inform user about the options
        print("Alright. Now you've filled the rockets with cargo, let's run another algorithm in order to reduce the costs as much as possible.\n"
        "Once again, there are several algorithms so you've got to make another decision:\n"
        "Option one is simulated annealing\n"
        "Option two is hill climber\n"
        "Option three is greedy\n")
        # make request for an algorithm
        print("Please make a decision by typing either one of the following numbers: 1, 2 or 3\n")
        # keep track of chosen options
        chosen_options = []
        # run chosen algorithm
        command = input("Option: ")
        if command.isdigit():
            if command == "1":
                print("Please initialize a beginning temperature and the number of iterations by inserting only integers\n")
                T_begin = input("Temperature: ")
                iter_no = input("Iterations: ")
                chosen_options.append(command)
                al.sim_an_cost(filling_rockets, T_begin, iter_no)
            elif command == "2":
                chosen_options.append(command)
                al.hill_climber_cost(filling_rockets)
            elif command == "3":
                chosen_options.append(command)
                greedy_cost(filling_rockets)
            else:
                print("Invalid command (command must be either an 1, 2 or 3). Please try again.\n")
                return 1
        else:
            print("Invalid command (command must be an integer). Please try again.\n")
            return 1


if __name__ == "__main__":
    start = time.time()
    solution = Solution()
    filling_rockets = solution.run_programme_filling_rockets()
    max_filled_cargo = max(filling_rockets)
    if max_filled_cargo is not 1:
        cost_optimizing = max_filled_cargo.run_programme_optimizing_costs()
    end = time.time()
    print('Runtime = ', end - start)

    #
    # results_sim_an_hill_climber_spacex = [0 for i in range(100)]
    # results_sim_an_solo_spacex = [0 for i in range(100)]
    # results_random_fill = [0 for i in range(100)]
    # results_random_fill_hill_climber = [0 for i in range(100)]
    # runs = 0
    # while(runs < 15):
    #     solution_sim_an_hill_climber_spacex = Solution()
    #     random.shuffle(solution_sim_an_hill_climber_spacex.cargolist)
    #     # solution_sim_an_solo_spacex = copy.deepcopy(solution_sim_an_hill_climber_spacex)
    #     # solution_random_fill = copy.deepcopy(solution_sim_an_hill_climber_spacex)
    #     # solution_random_fill_hill_climber = copy.deepcopy(solution_sim_an_hill_climber_spacex)
    #
    #     al.sim_an_hill_climber_spacex(solution_sim_an_hill_climber_spacex)
    #     # al.sim_an_solo_spacex(solution_sim_an_solo_spacex)
    #     # al.random_fill(solution_random_fill)
    #     # al.random_fill_hill_climber(solution_random_fill_hill_climber)
    #     solution_sim_an_hill_climber_spacex.count_items()
    #     # solution_sim_an_solo_spacex.count_items()
    #     # solution_random_fill.count_items()
    #     # solution_random_fill_hill_climber.count_items()
    #     results_sim_an_hill_climber_spacex[solution_sim_an_hill_climber_spacex.items_count] += 1
    #     # results_sim_an_solo_spacex[solution_sim_an_solo_spacex.items_count] += 1
    #     # results_random_fill[solution_random_fill.items_count] += 1
    #     # results_random_fill_hill_climber[solution_random_fill_hill_climber.items_count] +=1
    #
    #
    #     runs += 1
    # # print(results_sim_an_hill_climber_spacex)
    # # print(results_sim_an_solo_spacex)
    # # print(results_random_fill)
    # # print(results_random_fill_hill_climber)
    #
    #
    # # data = np.random.normal(0, 20, 1000)
    #
    # # fixed bin size
    #
    # # plt.xlim([min(data)-5, max(data)+5])
    # # plt.hist(results_random_fill, bins=20)
    # # plt.axis([0, 4, 0, 100])
    #
    # # plt.title('Random Gaussian data (fixed bin size)')
    # # plt.xlabel('variable X (bin size = 5)')
    # # plt.ylabel('count')
    #
    # plt.show()



    # # solution solved by sim_an_hill_climber
    # solution_1 = Solution()
    # random.shuffle(solution_1.cargolist)
    # al.sim_an_hill_climber_spacex(solution_1)
    # solution_1_copy = copy.deepcopy(solution_1)
    # solution_1.Items_count()
    # solution_1.cost_total()
    # cost_before = solution_1.cost
    # al.sim_an_cost(solution_1, 500, 30)
    # solution_1.cost_total()
    # cost_after = solution_1.cost
    # cost_dif = cost_after - cost_before
    # print(cost_dif)
    #
    #
    # solution_1_copy.cost_total()
    # cost_before = solution_1_copy.cost
    # al.greedy_cost(solution_1_copy)
    # solution_1_copy.cost_total()
    # cost_after = solution_1_copy.cost
    # cost_dif = cost_after - cost_before
    # print(cost_dif)



        # # solution_4.check_if_correct()
