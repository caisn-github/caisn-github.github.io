import pandas as pd

def record(csv_file_path:str,results:dict)->None:
    # 将 DataFrame 写入 CSV 文件
    df = pd.DataFrame.from_dict(results, orient='index').transpose()
    df.to_csv(csv_file_path, index=False)