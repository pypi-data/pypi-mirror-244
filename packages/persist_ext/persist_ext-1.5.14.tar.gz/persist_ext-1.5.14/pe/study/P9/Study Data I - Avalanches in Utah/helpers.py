import pandas as pd

def load_task_output(task_id, subtask_id):
    return pd.read_csv(f"./output_datasets/df_task_{task_id}{subtask_id}.csv")

def save_dataset(df, task_id, subtask_id):
    df.to_csv(f"./output_datasets/df_task_{task_id}{subtask_id}.csv", index=False)