import pandas as pd
import json
import pyarrow.parquet as pq
# 数据来源https://huggingface.co/datasets/DeepPavlov/banking77/tree/main
# 文件路径
test_path = "./data/test-00000-of-00001.parquet"
train_path = "./data/train-00000-of-00001.parquet"
intents_path = "./intents/intents-00000-of-00001.parquet"

# 输出文件路径
test_output_file = "./eval/test_output.json"
train_output_file = "./eval/train_output.json"

# 定义一个函数来处理每个 chunk
def process_and_write(input_path, intents_df, output_file, chunk_size=1000):
    # 初始化结果容器
    utterance_count = 0
    unique_intents = set()
    # 打开输出文件，准备逐块写入
    with open(output_file, "w", encoding="utf-8") as f:
        f.write('{\n"data": [\n')  # JSON 数组的开头
        first_chunk = True  # 标记是否是第一个 chunk

        # 使用 pyarrow.ParquetFile 读取 parquet 文件
        parquet_file = pq.ParquetFile(input_path)
        for batch in parquet_file.iter_batches(batch_size=chunk_size):
            # 将当前批次转换为 Pandas DataFrame
            chunk = batch.to_pandas()

            # 确保数据类型一致
            chunk['label'] = chunk['label'].astype(int)
            intents_df['id'] = intents_df['id'].astype(int)

            # 合并当前 chunk 和 intents_df
            merged_chunk = pd.merge(chunk, intents_df, left_on='label', right_on='id', how='inner')

            for i,(_,row) in enumerate(merged_chunk.iterrows()):
                record={
                    "utterance": row['utterance'],
                    "intent": row['name'],
                    "domain": "bank"
                }
                # 更新统计信息
                utterance_count += 1
                unique_intents.add(row['name'])
                # 写入 JSON 数据
                if not first_chunk or i > 0:
                    f.write(",\n")
                else:
                    first_chunk = False

                json.dump(record, f, ensure_ascii=False)

        # 写入 JSON 数组的结尾
        f.write("\n],\n")

        # 写入统计信息
        f.write(f'"utterance_number": {utterance_count},\n')
        f.write(f'"intents_number": {len(unique_intents)},\n')
        f.write('"intents": ' + json.dumps(sorted(list(unique_intents)), ensure_ascii=False) + "\n}")

    print(f"处理完成，结果已保存到 {output_file} 中。")

# 读取 intents 数据
intents_df = pd.read_parquet(intents_path)
intents_df['id'] = intents_df['id'].astype(int)

# 处理 test 和 train 数据
process_and_write(test_path, intents_df, test_output_file)
process_and_write(train_path, intents_df, train_output_file)

print("处理完成，结果已保存到 JSON 文件中。")
