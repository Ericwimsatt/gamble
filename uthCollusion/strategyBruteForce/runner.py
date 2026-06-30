import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from strategies import *
from run_simulation import run_simulation

class Runner:
    def __init__(self, name):
        self.name = name
        self.tasks = []
        self.results = {}
        self.results_summaries = {}

    def add_task(self, **task):
        self.tasks.append(task)

    def run_tasks(self):
        print("Running tasks, total tasks: {}".format(len(self.tasks)))
        with ThreadPoolExecutor(max_workers=len(self.tasks)) as executor:
            future_to_meta = {}
            for task in self.tasks:
                name = f"{task.get('player_hand', '')} // {task['strategy_name']} // {task.get('deads_pattern_name', '')}"
                future = executor.submit(run_simulation, task['pre_flop_strategy'], task['post_flop_strategy'], task['river_strategy'], task.get('dead_card_maker', None), num_hands=task['hands'], player_hand_maker=task.get('player_hand_maker', None))
                future_to_meta[future] = (name, task['hands'])
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
        for name in sorted(self.results_summaries, key=lambda n: self.results_summaries[n], reverse=True):
            print(f"{name}: Average Units Won: {self.results_summaries[name]}")

        self._write_results()

    def _write_results(self):
        if not self.results:
            return
        hands = next(iter(self.results.values())).stats['game_count']
        safe_name = self.name.replace(" ", "_").replace("/", "_").replace("\\", "_")
        out_dir = os.path.join("uthCollusion", "strategyBruteForce", "raw_outs")
        os.makedirs(out_dir, exist_ok=True)
        filepath = os.path.join(out_dir, f"{safe_name}_{hands}.json")
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
    runner = Runner("Base")
    runner.add_task(strategy_name="Base Strat", deads_pattern_name="None", pre_flop_strategy=base_strategies['pre_flop'], post_flop_strategy=base_strategies['post_flop'], river_strategy=base_strategies['river'], dead_card_maker=None, hands=100000)
    runner.run_tasks()
    # Strat comparison when low pair is made
    num_hands = 10000

    low_pair_runner = Runner("Low Pair Dead Card Strategies")
    low_pair_runner.add_task(strategy_name="No Bet when low pair", deads_pattern_name="Always low pair", pre_flop_strategy=pass_if_dead_pair, post_flop_strategy=base_strategies['post_flop'], river_strategy=base_strategies['river'], dead_card_maker=dead_cards_matching_player_low(1), hands=num_hands)
    low_pair_runner.add_task(strategy_name="No Bet when low pair unless both high", deads_pattern_name="Always low pair", pre_flop_strategy=pass_if_dead_pair_unless_ace_queen, post_flop_strategy=base_strategies['post_flop'], river_strategy=base_strategies['river'], dead_card_maker=dead_cards_matching_player_low(1), hands=num_hands)
    low_pair_runner.add_task(strategy_name="No Bet when low pair unless pocket pair", deads_pattern_name="Always low pair", pre_flop_strategy=pass_if_dead_pair_unless_pocket_pair, post_flop_strategy=base_strategies['post_flop'], river_strategy=base_strategies['river'], dead_card_maker=dead_cards_matching_player_low(1), hands=num_hands)
    low_pair_runner.add_task(strategy_name="No Bet when low pair unless pocket pair of eights", deads_pattern_name="Always low pair", pre_flop_strategy=pass_if_dead_pair_unless_eights_pocket_pair, post_flop_strategy=base_strategies['post_flop'], river_strategy=base_strategies['river'], dead_card_maker=dead_cards_matching_player_low(1), hands=num_hands)
    low_pair_runner.add_task(strategy_name="No Bet when low pair unless face pocket pair", deads_pattern_name="Always low pair", pre_flop_strategy=pass_if_dead_pair_unless_face_pocket_pair, post_flop_strategy=base_strategies['post_flop'], river_strategy=base_strategies['river'], dead_card_maker=dead_cards_matching_player_low(1), hands=num_hands)
    print(low_pair_runner.tasks)
    low_pair_runner.run_tasks()


