import pandas as pd
import json
#数据来源https://fb.me/covid_mcid_dataset

# 文件路径
test_file_path = "./covid_release/en/test.tsv"  # 输入的 TSV 文件路径
train_file_path = "./covid_release/en/train.tsv"  # 输入的 TSV 文件路径
eval_file_path = "./covid_release/en/eval.tsv"  # 输入的 TSV 文件路径

test_output_json = "./eval/test_output_data.json"  # 输出的 JSON 文件路径
train_output_json = "./eval/train_output_data.json"  # 输出的 JSON 文件路径
eval_output_json = "./eval/eval_output_data.json"  # 输出的 JSON 文件路径

# 定义一个函数来处理 TSV 文件并批量写入 JSON 文件
def read_tsv_to_json_batched(tsv_file, output_file, chunk_size=1000):
    # 初始化统计信息
    utterance_count = 0
    unique_intents = set()

    # 打开输出文件，准备逐块写入
    with open(output_file, "w", encoding="utf-8") as f:
        f.write('{\n"data": [\n')  # JSON 数组的开头
        first_chunk = True  # 标记是否是第一个 chunk

        # 使用 Pandas 分块读取 TSV 文件
        reader = pd.read_csv(tsv_file, sep='\t', header=None, names=["utterance", "intent"], chunksize=chunk_size)
        for chunk in reader:
            # 遍历当前批次的数据
            for i, (_, row) in enumerate(chunk.iterrows()):
                utterance = row["utterance"].strip()  # 去除多余空格
                intent = row["intent"].split(":")[1].rstrip()  # 提取 intent 名称（去掉前缀 "intent:"）

                record = {
                    "utterance": utterance,
                    "intent": intent,
                    "domain": "medicine"
                }

                # 更新统计信息
                utterance_count += 1
                unique_intents.add(intent)

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
read_tsv_to_json_batched(test_file_path, test_output_json)
read_tsv_to_json_batched(train_file_path, train_output_json)
read_tsv_to_json_batched(eval_file_path, eval_output_json)

