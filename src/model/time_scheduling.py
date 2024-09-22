from tqdm import tqdm
from copy import copy
from model.knapsac import knapsack, knapsack_with_tolerance
from pandas import DataFrame
from itertools import chain
from utils import Utils as ut
from constants import network_type_map


class TimeSchedulingAlgorithm:

    @classmethod
    def find_best_scheduling(
        cls,
        data: DataFrame,
        pump_gpm: float,
        pump_type: int,
        allow_exact: bool = True,
        allow_overdosing: bool = False,
        allow_underdosing: bool = False,
    ):

        best_number_of_batches = 99999
        best_solution = None

        for solution_trial in [
            ("Constrained", 1),
            ("Relaxed-Up", 1.1),
            ("Relaxed-down", 0.9),
        ]:

            solution_type, correction_percentage = solution_trial

            pump_gpm_corrected = pump_gpm * correction_percentage

            try:
                networks_batches_solution = cls.compute_schedule_trial(
                    data, pump_gpm_corrected, pump_type
                )
            except NoSolution:
                print(
                    f"Could not find a working {solution_type} solution for pump GPM of {pump_gpm}"
                )

            current_solution_total_batches = cls.get_total_number_batches(
                networks_batches_solution
            )
            if current_solution_total_batches < best_number_of_batches:

                if solution_type == "Constrained" and allow_exact:
                    best_number_of_batches = 1 * current_solution_total_batches
                    best_solution = networks_batches_solution
                elif solution_type == "Relaxed-Up" and allow_overdosing:
                    best_number_of_batches = 1 * current_solution_total_batches
                    best_solution = networks_batches_solution

                elif solution_type == "Relaxed-down" and allow_underdosing:
                    best_number_of_batches = 1 * current_solution_total_batches
                    best_solution = networks_batches_solution

        return best_solution, best_number_of_batches

    @classmethod
    def within_any_range(cls, batch_total_gpm, pump_gpm, pump_type_):

        ##* acceptable_ranges:

        nearest_gpm, nearest_gpm_delta = -1, 99999

        pump_motor_gpm = pump_gpm / pump_type_
        # accepted_ranges = [ (pump_motor_gpm*i*0.9,pump_motor_gpm*i, pump_motor_gpm*i*1.1)  for i in range(1, pump_type+1) ]

        for range_indx in range(1, pump_type_ + 1):
            accepted_range = pump_motor_gpm * range_indx
            delta = abs(accepted_range - batch_total_gpm)
            if delta <= nearest_gpm_delta:
                nearest_gpm_delta = delta
                nearest_gpm = accepted_range

            if delta <= 0.1 * accepted_range:
                return True, nearest_gpm
        # * if reached here, then no acceptable range, return nearest one:
        return False, nearest_gpm

    @classmethod
    def correct_invalid_group(
        cls, incorrect_group, remaining_groups, optimal_gpm, pump_gpm, pump_type
    ):

        def get_group_total_gpm(group):
            flattened = list((chain.from_iterable(group.values())))
            return sum([f_[-1] for f_ in flattened]), flattened

        total_gpm, flattened = get_group_total_gpm(incorrect_group)

        ## Keep removing valves until the batch is corrected
        found_correction = False
        while total_gpm - optimal_gpm > optimal_gpm * 0.1:
            # * first, choose the item to be replaced: the one that minimizes difference:
            delta_gp = abs(optimal_gpm - total_gpm)
            # sorted_valves_by_delta_gpm = sorted(flattened, key=lambda x: abs(x[-1]-delta_gp))
            sorted_valves_by_delta_gpm = sorted(flattened, key=lambda x: x[-1])
            valve_to_replace = sorted_valves_by_delta_gpm[0]
            ##* choose the batch from the remaining groups that optimizes the performance
            remaining_groups.sort(key=lambda x: get_group_total_gpm(x)[0])
            found_correction = False
            for group_ in remaining_groups:
                current_group_gpm = get_group_total_gpm(group_)[0]
                if cls.within_any_range(
                    current_group_gpm + valve_to_replace[1], pump_gpm, pump_type
                )[0]:
                    valve_key = valve_to_replace[0].split("-")[0]
                    print(f"\n\nValue Key: {valve_to_replace[0]}\n\n ")
                    if valve_key not in group_.keys():
                        group_[valve_key] = []
                    group_[valve_key].append(valve_to_replace)
                    incorrect_group[valve_key].remove(valve_to_replace)
                    del valve_to_replace
                    found_correction = True
                    break

            if not found_correction:
                print("No possible corrections for this solution")
                break
            else:
                print("made correction to the solution for optimality")
            total_gpm, flattened = get_group_total_gpm(incorrect_group)

        remaining_groups.append(incorrect_group)
        return remaining_groups, found_correction

    @classmethod
    def check_for_further_optimizations(cls, solution_dictionary, pump_gpm, pump_type):
        has_correction = True
        while has_correction:
            for idx in range(len(solution_dictionary)):
                group = solution_dictionary[idx]
                has_correction = False

                flattened = list((chain.from_iterable(group.values())))

                total_gpm = "{:5.3f}".format(sum([f_[-1] for f_ in flattened]))

                check_flag, nearest_gpm = cls.within_any_range(
                    float(total_gpm), pump_gpm, pump_type
                )
                if check_flag:
                    print(
                        f"Batch #{idx} with GPM = {total_gpm} is valid with nearest GPM = {nearest_gpm}"
                    )
                else:
                    print(
                        f"Batch #{idx} with GPM = {total_gpm} is NOT valid with nearest GPM = {nearest_gpm}"
                    )
                    solution_dictionary.remove(group)
                    solution_dictionary, found_correction = cls.correct_invalid_group(
                        group, solution_dictionary, nearest_gpm, pump_gpm, pump_type
                    )
                    has_correction = found_correction
        return solution_dictionary

    @classmethod
    def compute_schedule_trial(cls, data: DataFrame, pump_gpm: float, pump_type: int):

        valve_type_keys = data.valve_type_key.unique().tolist()

        networks_batches = []

        for network_key in valve_type_keys:

            per_key_valves = data.loc[data["valve_type_key"] == network_key][
                ["Valve", "gpm_int", "gpm"]
            ]

            solution_dictionary = cls.distibute_valves_into_batches(
                per_key_valves, pump_gpm
            )

            ##* Try further optimization of the problem
            solution_dictionary = cls.check_for_further_optimizations(
                solution_dictionary, pump_gpm, pump_type
            )

            group_ids = []
            per_batch_gpm = []
            for id_, group in enumerate(solution_dictionary):
                group_ids.append(id_ + 1)
                flattened = list((chain.from_iterable(group.values())))
                total_gpm = "{:5.3f}".format(sum([f_[-1] for f_ in flattened]))
                per_batch_gpm.append(total_gpm)

            networks_batches.append(
                (network_key, solution_dictionary, group_ids, per_batch_gpm)
            )
        return networks_batches

    @classmethod
    def distibute_valves_into_batches(cls, valve_data: DataFrame, pump_unit_gpm: float):

        values = [1 for _ in range(len(valve_data))]
        weights = list(
            zip(valve_data["gpm_int"].tolist(), valve_data["Valve"].tolist())
        )
        weights.sort(key=lambda x: x[0])

        all_groups = []
        progress_bar = tqdm(total=len(valve_data))

        while len(weights) > 0:
            group_ = knapsack_with_tolerance(weights, values, pump_unit_gpm)

            if group_ is None or len(group_) == 0:
                raise NoSolution

            all_groups.append(copy(group_))
            progress_bar.update(len(group_))
            for element in group_:
                weights.remove(element)

        inverted_groups = []
        for _, group_ in enumerate(all_groups):
            interm_group = []
            for x in group_:
                if isinstance(
                    valve_data.loc[valve_data["Valve"] == x[-1]]["gpm"].item(), list
                ):
                    interm_group.append(
                        (
                            x[-1],
                            valve_data.loc[valve_data["Valve"] == x[-1]]["gpm"].item(),
                        )
                    )
                else:
                    interm_group.append(
                        (
                            x[-1],
                            valve_data.loc[valve_data["Valve"] == x[-1]]["gpm"].item(),
                        )
                    )
            group_ = interm_group
            names = [x[0] for x in group_]
            values = [x[1] for x in group_]
            ##* Add groups:
            groups = {k.split("-")[0]: [] for k in names}

            for valve_name, valve_gpm in zip(names, values):
                key = valve_name.split("-")[0]
                groups[key].append((valve_name, valve_gpm))
            inverted_groups.append(groups)

        return inverted_groups

    @classmethod
    def get_total_number_batches(cls, solution: list):
        
        sum_ = 0
        for s_ in solution:
            for _, _, _, batch_gpm in zip(s_[0], s_[1], s_[2], s_[3]):
                sum_ += float(batch_gpm)
        return sum_


class NoSolution(Exception):

    pass
