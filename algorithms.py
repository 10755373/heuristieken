import helpers as hp

#  algorithms for filling based on volume
def fill_cargo_volume(solution):
    rockets = solution.rockets
    cargolist = solution.cargolist
    cargo_in_rockets = solution.cargo_in_rockets
    hp.fill_cargo_volume_based(rockets, cargolist, cargo_in_rockets)


#  algorithms for filling based on mass
def fill_cargo_mass(solution):
    rockets = solution.rockets
    cargolist = solution.cargolist
    cargo_in_rockets = solution.cargo_in_rockets
    hp.fill_cargo_mass_based(rockets, cargolist, cargo_in_rockets)


# algorithms for filling based on density-ratio
def sim_an_hill_climber_spacex(solution):

    rockets = solution.rockets
    cargolist = solution.cargolist
    cargo_in_rockets = solution.cargo_in_rockets

    hp.fill_cargo_density_with_error_corrected(rockets, cargolist, cargo_in_rockets)
    hp.switchitems_rockets_fill(rockets, cargolist, cargo_in_rockets, hp.fill_cargo_density_with_error_corrected)

    possibility = 1
    while(possibility == 1):
        possibility = hp.switchitems_rocket_and_list_fill(rockets, cargolist, cargo_in_rockets, hp.fill_cargo_single_rocket_density_with_error)


def sim_an_solo_spacex(solution):
    rockets = solution.rockets
    cargolist = solution.cargolist
    cargo_in_rockets = solution.cargo_in_rockets
    hp.fill_cargo_density_with_error(rockets, cargolist, cargo_in_rockets)


def random_fill(solution):
    rockets = solution.rockets
    cargolist = solution.cargolist
    cargo_in_rockets = solution.cargo_in_rockets
    hp.fill_cargo_random(rockets, cargolist, cargo_in_rockets)


def random_fill_hill_climber(solution):
    rockets = solution.rockets
    cargolist = solution.cargolist
    cargo_in_rockets = solution.cargo_in_rockets
    hp.fill_cargo_random(rockets, cargolist, cargo_in_rockets)
    hp.switchitems_rockets_fill(rockets, cargolist, cargo_in_rockets, hp.fill_cargo_random)

    possibility = 1
    while(possibility == 1):
        possibility = hp.switchitems_rocket_and_list_fill(rockets, cargolist, cargo_in_rockets, hp.fill_cargo_random)


#  algorithms for cost optimisation
def sim_an_cost(solution, T_begin, iter_no):
    T = T_begin
    rockets = solution.rockets
    for i in range(iter_no):
        hp.cost_opitimization_probability_depended(rockets, T)
        T = hp.update_temperature(T)

def hill_climber_cost(solution):
    rockets = solution.rockets
    hp.cost_opitimization_hill_climber(rockets)

def greedy_cost(solution):
    rockets = solution.rockets
    hp.cost_opitimization_greedy(rockets)
