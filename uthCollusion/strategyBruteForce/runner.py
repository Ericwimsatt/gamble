import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from strategies import *
from run_simulation import run_simulation

# type task = tuple[str, str, callable, callable, callable, callable | None, int]

class Runner:
    def __init__(self, name):
        self.name = name
        self.tasks = []
        self.results = {}
        self.results_summaries = {}

    def add_task(self, task):
        self.tasks.append(task)
    
    def run_tasks(self):
        with ThreadPoolExecutor(max_workers=len(self.tasks)) as executor:
            future_to_meta = {}
            for task in self.tasks:
                strategy_name, deads_pattern_name, pre_flop_strategy, post_flop_strategy, river_strategy, dead_card_maker, hands = task
                name = f"{strategy_name} // {deads_pattern_name}"
                future = executor.submit(run_simulation, pre_flop_strategy, post_flop_strategy, river_strategy, dead_card_maker, hands=hands)
                future_to_meta[future] = (name, hands)
                print(f"Submitted task: {name}")

            for future in as_completed(future_to_meta):
                name, hands = future_to_meta[future]
                result = future.result()
                print(f"Task {name} completed. Simulations: {hands}, \nAverages: {result.average_str()}")
                self.results[name] = result
                self.results_summaries[name] = result.average_units_won()

        print("All tasks completed")
        for name in self.results.keys():
            print(f"{name}: Average Units Won: {self.results_summaries[name]}\n full results: \n{self.results[name].average_str()}")
        
        print("Summarized stats:")
        for name in self.results.keys():
            print(f"{name}: Average Units Won: {self.results_summaries[name]}")

        self._write_results()

    def _write_results(self):
        if not self.results:
            return
        hands = next(iter(self.results.values())).stats['game_count']
        safe_name = self.name.replace(" ", "_").replace("/", "_").replace("\\", "_")
        os.makedirs("raw_outs", exist_ok=True)
        filepath = os.path.join("raw_outs", f"{safe_name}_{hands}.json")
        output = {
            "runner": self.name,
            "hands": hands,
            "results": {}
        }
        for name, result in self.results.items():
            gc = result.stats['game_count']
            output["results"][name] = {
                "full": result.stats.copy(),
                "averages": {k: v / gc for k, v in result.stats.items()} if gc > 0 else {}
            }
        with open(filepath, "w") as f:
            json.dump(output, f, indent=2)
        print(f"Results written to {filepath}")

if __name__ == "__main__":
    num_hands = 100
    runner = Runner("Base")
    runner.add_task(("Base Strat", "None", base_strategies['pre_flop'], base_strategies['post_flop'], base_strategies['river'], None, num_hands))
    runner.run_tasks()
    # Strat comparison when low pair is made
    low_pair_runner = Runner("Low Pair Dead Card Strategies")
    low_pair_runner.add_task(("No Bet when low pair", "Always low pair", pass_if_dead_pair, base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_low(1), num_hands))
    low_pair_runner.add_task(("No Bet when low pair unless both high", "Always low pair", pass_if_dead_pair_unless_ace_queen, base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_low(1), num_hands))
    low_pair_runner.add_task(("No Bet when low pair unless pocket pair", "Always low pair", pass_if_dead_pair_unless_pocket_pair, base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_low(1), num_hands))
    low_pair_runner.add_task(("No Bet when low pair unless pocket pair of eights", "Always low pair", pass_if_dead_pair_unless_eights_pocket_pair, base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_low(1), num_hands))
    low_pair_runner.add_task(("No Bet when low pair unless face pocket pair", "Always low pair", pass_if_dead_pair_unless_face_pocket_pair, base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_low(1), num_hands))
    print(low_pair_runner.tasks)
    runner.run_tasks()


