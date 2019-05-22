import numpy as np
import pandas as pd
import math
import random
from rocket import Rocket
from item import Item
from sys import argv


def cost_opitimization_greedy(rockets):
    for i in range(40):
        # cross check between all rockets
        cost_reduction_max = 0
        for rocket_i in rockets:
            for rocket_j in rockets:
                # only for different rockets
                if (rocket_i != rocket_j):
                    # cross check for all items in seperate rockets
                    for item_i in rocket_i.items:
                        for item_j in rocket_j.items:
                            # call for cost_difference function
                            cost_difference = cost_difference(rocket_i, rocket_j, item_i, item_j)
                            # calculate reduction current switch
                            cost_reduction = - (cost_difference)
                            # track switch for highest payoff
                            if cost_reduction > cost_reduction_max:
                                cost_reduction_max = cost_reduction
                                item_to_change_1 = item_i
                                rocket_item_1 = rocket_i
                                item_to_change_2 = item_j
                                rocket_item_2 = rocket_j
                            # change back
                            rocket_i.interchange_items(item_j, item_i)
                            rocket_j.interchange_items(item_i, item_j)
        # make the best switch possible
        if cost_reduction_max > 0:
            rocket_item_1.interchange_items(item_to_change_1, item_to_change_2)
            rocket_item_2.interchange_items(item_to_change_2, item_to_change_1)


def cost_opitimization_hill_climber(rockets):
    # cross check between all rockets
    for rocket_i in rockets:
        for rocket_j in rockets:
            # only for different rockets
            if (rocket_i != rocket_j):
                # cross check for all items in seperate rockets
                for item_i in rocket_i.items:
                    for item_j in rocket_j.items:
                        # call for cost_difference function
                        cost_difference = cost_difference(rocket_i, rocket_j, item_i, item_j)
                        # change reduced the cost
                        if cost_difference < 0:
                            # break out of rocket.items loops after item is filled
                            break
                        # switch back items if it did not lead to item filled
                        else:
                            # change back
                            rocket_i.interchange_items(item_j, item_i)
                            rocket_j.interchange_items(item_i, item_j)


def cost_opitimization_probability_depended(rockets, T):
    # cross check between all rockets
    for rocket_i in rockets:
        for rocket_j in rockets:
            # only for different rockets
            if (rocket_i != rocket_j):
                # cross check for all items in seperate rockets
                for item_i in rocket_i.items:
                    for item_j in rocket_j.items:
                        cost_difference = cost_difference(rocket_i, rocket_j, item_i, item_j)
                        # change reduced the cost
                        if cost_difference < 0:
                            # break out of rocket.items loops after item is filled
                            break
                        # switch back items if it did not lead to item filled
                        else:
                            probability =  math.exp(-cost_difference/T)
                            # generate random number
                            random_number = random.random()
                            if (probability > random_number):
                                break
                            else:
                                # change back
                                rocket_i.interchange_items(item_j, item_i)
                                rocket_j.interchange_items(item_i, item_j)


def cost_difference(rocket_i, rocket_j, item_i, item_j):
    # if items can switch, do so, and check if item from unfilled list fits in as result
    if (rocket_j.filled_weight - item_j.mass + item_i.mass <= rocket_j.payload_mass) and (rocket_j.filled_volume - item_j.volume + item_i.volume <= rocket_j.payload_volume) and (rocket_i.filled_weight + item_j.mass - item_i.mass <= rocket_i.payload_mass) and (rocket_i.filled_volume + item_j.volume - item_i.volume <= rocket_i.payload_volume) and (item_i != item_j):
        # calculate cost before change
        cost_before = cost(rockets)
        # interchange items between the rockets
        rocket_i.interchange_items(item_i, item_j)
        rocket_j.interchange_items(item_j, item_i)
        # calculate cost after change
        cost_after = cost(rockets)
        cost_difference = cost_after - cost_before
        return cost_difference
    else
        return 0


def update_temperature(T):
    T = T * 0.95
    return T


def fill_cargo_density_with_error(rockets, cargolist, cargo_in_rockets):

    filled = 0
    for i in range(3):
        for rocket in rockets:
            if (rocket.payload_volume - rocket.filled_volume != 0):
                rocket.average_density = (rocket.payload_mass - rocket.filled_weight)/(rocket.payload_volume - rocket.filled_volume)
            else:
                rocket.average_density = 0

        for i in np.arange(0, 2, 0.1):
        # increase range for search iteratively
            items_loaded = []
            for item in cargolist:
                for rocket in rockets:
                    # calculate shift in density
                    density_difference = rocket.average_density - rocket.initial_average_density
                    # set upper and lower bound for range of densities
                    if density_difference == 0:
                        rocket_density_upper = (rocket.average_density + rocket.average_density*i)
                        rocket_density_lower = (rocket.average_density - rocket.average_density*i)
                    # in case of a positive number
                    if density_difference > 0:
                        # print('yes')
                        rocket_density_upper = (rocket.average_density + rocket.average_density*i + density_difference*i)
                        rocket_density_lower = (rocket.average_density - rocket.average_density*i + density_difference*i)
                    # in case of a negative number
                    if density_difference < 0:
                        # print('yes')
                        rocket_density_upper = (rocket.average_density + rocket.average_density*i - density_difference*i)
                        rocket_density_lower = (rocket.average_density - rocket.average_density*i - density_difference*i)
                    # if items are within density range and fit the rocket, load in rocket
                    if(item.density <= rocket_density_upper and item.density >= rocket_density_lower) and (rocket.filled_weight + item.mass <= rocket.payload_mass) and (rocket.filled_volume + item.volume <= rocket.payload_volume) and (item not in cargo_in_rockets):
                        filled += 1
                        rocket.load_item_error(item)
                        cargo_in_rockets.append(item)
                        items_loaded.append(item)
            # remove items in cargolist if loaded
            for item in items_loaded:
                cargolist.remove(item)
    # return amount of items filled in current session
    return filled


def fill_cargo_density_with_error_corrected(rockets, cargolist, cargo_in_rockets):

    filled = 0
    for i in range(3):
        for rocket in rockets:
            if (rocket.payload_volume - rocket.filled_volume != 0):
                rocket.initial_average_density = (rocket.payload_mass - rocket.filled_weight)/(rocket.payload_volume - rocket.filled_volume)
            else:
                rocket.initial_average_density = 0

        for i in np.arange(0, 2, 0.1):
        # increase range for search iteratively
            items_loaded = []
            for item in cargolist:
                for rocket in rockets:
                    # calculate shift in density
                    density_difference = rocket.average_density - rocket.initial_average_density
                    # set upper and lower bound for range of densities
                    if density_difference == 0:
                        rocket_density_upper = (rocket.initial_average_density + rocket.initial_average_density*i)
                        rocket_density_lower = (rocket.initial_average_density - rocket.initial_average_density*i)
                    # in case of a positive number
                    if density_difference > 0:
                        rocket_density_upper = (rocket.initial_average_density + rocket.initial_average_density*i + density_difference*i)
                        rocket_density_lower = (rocket.initial_average_density - rocket. initial_average_density*i + density_difference*i)
                    # in case of a negative number
                    if density_difference < 0:
                        rocket_density_upper = (rocket.initial_average_density + rocket.initial_average_density*i - density_difference*i)
                        rocket_density_lower = (rocket.initial_average_density - rocket. initial_average_density*i - density_difference*i)
                    # if items are within density range and fit the rocket, load in rocket
                    if(item.density <= rocket_density_upper and item.density >= rocket_density_lower) and (rocket.filled_weight + item.mass <= rocket.payload_mass) and (rocket.filled_volume + item.volume <= rocket.payload_volume) and (item not in cargo_in_rockets):
                        filled += 1
                        rocket.load_item_error(item)
                        cargo_in_rockets.append(item)
                        items_loaded.append(item)
            # remove items in cargolist if loaded
            for item in items_loaded:
                cargolist.remove(item)

    # return amount of items filled in current session
    return filled


def fill_cargo_random(rockets, cargolist, cargo_in_rockets):
    filled = 0
    items_loaded = []
    for item in cargolist:
        for rocket in rockets:
            # if items are within density range and fit the rocket, load in rocket
            if(rocket.filled_weight + item.mass <= rocket.payload_mass) and (rocket.filled_volume + item.volume <= rocket.payload_volume) and (item not in cargo_in_rockets):
                filled += 1
                rocket.load_item(item)
                cargo_in_rockets.append(item)
                items_loaded.append(item)
    # remove items in cargolist if loaded
    for item in items_loaded:
        cargolist.remove(item)
    # return amount of items filled in current session
    return filled


# def fill_cargo_volume_based(rockets, cargolist, cargo_in_rockets):
#     filled = 0
#     items_loaded = []
#     for rocket in rockets:
#         rocket_list = []
#         rocket_list.append(rocket)
#         sorted_rockets = sorted(rocket_list, key=lambda rocket: rocket.payload_volume)
#         for cargo in cargolist:
#             sorted_cargo = sorted(cargolist, key=lambda item: item.volume)
#             for rocket in sorted_rockets:
#                 for cargo in sorted_cargo:
#                     if (rocket.filled_weight + item.mass <= rocket.payload_mass) and (rocket.filled_volume + item.volume <= rocket.payload_volume) and (item not in cargo_in_rockets):
#                         filled += 1
#                         rocket.load_item(item)
#                         cargo_in_rockets.append(item)
#                         items_loaded.append(item)
#         for item in items_loaded:
#             sorted_cargo.remove(item)
#     return filled
#
#
# def fill_cargo_mass_based(rockets, cargolist, cargo_in_rockets):
#     filled = 0
#     items_loaded = []
#     for rocket in rockets:
#         rocket_list = []
#         rocket_list.append(rocket)
#         sorted_rockets = sorted(rocket_list, key=lambda rocket: rocket.mass_ratio)
#         for cargo in cargolist:
#             sorted_cargo = sorted(cargolist, key=lambda item: item.mass)
#             for rocket in sorted_rockets:
#                 for cargo in sorted_cargo:
#                     if (rocket.filled_weight + item.mass <= rocket.payload_mass) and (rocket.filled_volume + item.volume <= rocket.payload_volume) and (item not in cargo_in_rockets):
#                         filled += 1
#                         rocket.load_item(item)
#                         cargo_in_rockets.append(item)
#                         items_loaded.append(item)
#         for item in items_loaded:
#             sorted_cargo.remove(item)
#     return filled


def fill_cargo_single_rocket_density_with_error(rocket, cargolist, cargo_in_rockets):
    filled = 0

    for i in range(3):

        if (rocket.payload_volume - rocket.filled_volume != 0):
            rocket.initial_average_density = (rocket.payload_mass - rocket.filled_weight)/(rocket.payload_volume - rocket.filled_volume)
        else:
            rocket.initial_average_density = 0
        # increase range for search iteratively
        for i in np.arange(0, 1.5, 0.1):
            # keep track of loaded items
            items_loaded = []
            for item in cargolist:
                # calculate the density difference
                density_difference = rocket.average_density - rocket.initial_average_density
                # set upper and lower bound for range of densities
                if density_difference == 0:
                    rocket_density_upper = (rocket.initial_average_density + rocket.initial_average_density*i)
                    rocket_density_lower = (rocket.initial_average_density - rocket.initial_average_density*i)
                # in case of a positive number
                if density_difference > 0:
                    rocket_density_upper = (rocket.initial_average_density + rocket.initial_average_density*i + density_difference*i)
                    rocket_density_lower = (rocket.initial_average_density - rocket. initial_average_density*i + density_difference*i)
                # in case of a negative number
                if density_difference < 0:
                    rocket_density_upper = (rocket.initial_average_density + rocket.initial_average_density*i - density_difference*i)
                    rocket_density_lower = (rocket.initial_average_density - rocket. initial_average_density*i - density_difference*i)
                # if items are within density range and fit the rocket, load in rocket
                if(item.density <= rocket_density_upper and item.density >= rocket_density_lower) and (rocket.filled_weight + item.mass <= rocket.payload_mass) and (rocket.filled_volume + item.volume <= rocket.payload_volume) and (item not in cargo_in_rockets):
                    rocket.load_item(item)
                    cargo_in_rockets.append(item)
                    filled += 1
                    items_loaded.append(item)
            # remove items in cargolist if loaded
            for item in items_loaded:
                cargolist.remove(item)
    # return amount of items filled in current session
    return filled


# shifts items between rocket in order to make space and try to fit items after each shift.
def switchitems_rockets_fill(rockets, cargolist, cargo_in_rockets, fill_function):
    # cross check between all rockets
    for rocket_i in rockets:
        for rocket_j in rockets:
            # only for different rockets
            if (rocket_i != rocket_j):
                # cross check for all items in seperate rockets
                for item_i in rocket_i.items:
                    for item_j in rocket_j.items:
                        # if items can switch, do so, and check if item from unfilled list fits in as result
                        if (rocket_j.filled_weight - item_j.mass + item_i.mass <= rocket_j.payload_mass) and (rocket_j.filled_volume - item_j.volume + item_i.volume <= rocket_j.payload_volume) and (rocket_i.filled_weight + item_j.mass - item_i.mass <= rocket_i.payload_mass) and (rocket_i.filled_volume + item_j.volume - item_i.volume <= rocket_i.payload_volume) and (item_i != item_j):
                            # interchange items between the rockets
                            rocket_i.interchange_items(item_i, item_j)
                            rocket_j.interchange_items(item_j, item_i)
                            # try to fit more items
                            filled = fill_function(rockets, cargolist, cargo_in_rockets)
                            if filled > 0:
                                # break out of loop after item is filled
                                break
                            # switch back items if it did not lead to item filled
                            else:
                                rocket_i.interchange_items(item_j, item_i)
                                rocket_j.interchange_items(item_i, item_j)


def interchange_item_list(list, item_1, item_2):
    for i in range(len(list)):
        if list[i] == item_1:
            list[i] = item_2


def switchitems_rocket_and_list_fill(rockets, cargolist, cargo_in_rockets, fill_function):
    for item_list in cargolist:
        for rocket in rockets:
            for item_rocket in rocket.items:
                # check is item in rocket can be swapped with item from cargo_unfilled
                if (rocket.filled_weight - item_rocket.mass + item_list.mass <= rocket.payload_mass) and (rocket.filled_volume - item_rocket.volume + item_list.volume <= rocket.payload_volume) and (item_list != item_rocket):
                    # switch items between rocket and list
                    rocket.interchange_items(item_rocket, item_list)
                    interchange_item_list(cargolist, item_list, item_rocket)
                    # try to fill item
                    filled = fill_function(rocket, cargolist, cargo_in_rockets)
                    if (filled) > 0:
                        return 1
                    # if switch did not result in filled item, switch back
                    else:
                        rocket.interchange_items(item_list, item_rocket)
                        interchange_item_list(cargolist, item_rocket, item_list)
    return 0


def cost(rockets):
    total_cost = 0
    for rocket in rockets:
        Fuel_grams = (rocket.mass + rocket.filled_weight)*(rocket.fuel_to_weight)/(1 - rocket.fuel_to_weight)
        cost_rocket = (rocket.base_cost * (10**6)) + round(1000 * Fuel_grams)
        total_cost += cost_rocket
    return total_cost
