import json
import sys
import os

def main():
    if len(sys.argv) < 2:
        print("Usage: python summarize_results.py <path> [<path> ...]")
        print("  <path> can be a .json file or a directory containing .json files")
        sys.exit(1)

    json_files = []
    for arg in sys.argv[1:]:
        if os.path.isdir(arg):
            for f in sorted(os.listdir(arg)):
                if f.endswith('.json'):
                    json_files.append(os.path.join(arg, f))
        elif os.path.isfile(arg) and arg.endswith('.json'):
            json_files.append(arg)

    if not json_files:
        print("No JSON files found.")
        sys.exit(1)

    rows = []

    for filepath in sorted(json_files):
        with open(filepath) as f:
            data = json.load(f)

        runner_name = data.get('runner', 'Unknown')

        for task_key, task_data in data.get('results', {}).items():
            averages = task_data.get('averages', {})
            avg_units_won = averages.get('units_won_total', 0)
            game_count = task_data.get('full', {}).get('game_count', 0)

            rows.append((avg_units_won, task_key, runner_name, game_count))

    rows.sort(key=lambda x: x[0], reverse=True)

    print(f"\n{'Rank':<5} {'Avg Units Won':<17} {'Hands':<8} {'Source':<45} {'Task'}")
    print(f"{'====':<5} {'=============':<17} {'=====':<8} {'======':<45} {'===='}")
    for i, (avg, task_key, source, hands) in enumerate(rows, 1):
        print(f"{i:<5} {avg:<17.6f} {hands:<8} {source:<45} {task_key}")

    print(f"\nTotal tasks: {len(rows)}")
    print(f"Total JSON files: {len(json_files)}")


if __name__ == "__main__":
    main()
