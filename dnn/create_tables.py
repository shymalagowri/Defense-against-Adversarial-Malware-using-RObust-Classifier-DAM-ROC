import json
import os
import pandas as pd

if __name__ == "__main__":
    if not os.path.exists("output/tables"):
        os.mkdir("output/tables")

    train_methods = ['natural', 'dfgsm_k', 'rfgsm_k', 'topkr', 'grosse']
    evasion_methods = ['natural', 'dfgsm_k', 'rfgsm_k', 'topkr', 'grosse']

    metric = [["robustness_ratio", "RR_sensitivity"], ["evasion_rate", "evasion_rate_fnr"], ["evasion", "Ev_F1"], ["evasion", "Ev_accuracy"]]

    for x in metric:
        table = []
        for train_method in train_methods:
            row = []
            for evasion_method in evasion_methods:
                filename = f"[training_{train_method}_evasion_{evasion_method}]_run_experiments.json"
                with open("output/metrics/derived_results/" + filename, "r") as result_file:
                    metrics = json.load(result_file)
                row.append(metrics[x[0]][x[1]])
            table.append(row)
        table_df = pd.DataFrame(table)
        table_df.columns = evasion_methods
        table_df.index = train_methods
        print()
        print(x[1])
        print(table_df)
        table_df.to_csv("output/tables/" + x[1] + "_table.csv")
