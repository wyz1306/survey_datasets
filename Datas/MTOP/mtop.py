import pandas as pd
import json
import pyarrow.parquet as pq
#数据来源https://huggingface.co/datasets/mteb/mtop_intent/tree/main

# 文件路径
test_path = "./data/test_en-00000-of-00001-32bc89f7a6f05de1.parquet"
train_path = "./data/train_en-00000-of-00001-fc176d2de42e5a89.parquet"
validation_path = "./data/eval_en-00000-of-00001-c4d91b50c54960f7.parquet"

# 输出文件路径
test_output_file = "./eval/test_output.json"
train_output_file = "./eval/train_output.json"
validation_output_file = "./eval/validation_output.json"

# 定义一个函数来处理 Parquet 文件并批量写入 JSON 文件
def process_parquet_to_json(input_path, output_file, chunk_size=1000):
    # 初始化统计信息
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

            # 去重重复列
            chunk = chunk.loc[:, ~chunk.columns.duplicated()]

            # 处理 slot 列中的缺失值
            chunk['slot'] = chunk['slot'].fillna("None")

            # 遍历当前批次的数据
            for i, (_, row) in enumerate(chunk.iterrows()):
                _intent = row["intent"].split(":")[1].rstrip()
                record = {
                    "utterance": row['utterance'],
                    "intent": _intent,
                    "domain": row['domain']
                }

                # 更新统计信息
                utterance_count += 1
                unique_intents.add(_intent)

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

# 调用函数处理文件
process_parquet_to_json(test_path, test_output_file)
process_parquet_to_json(train_path, train_output_file)
process_parquet_to_json(validation_path, validation_output_file)
