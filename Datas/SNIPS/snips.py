import pandas as pd
import json
#数据来源https://github.com/OpenGPTX/illuminer
# 文件路径
test_file_path = "./data/test.tsv"  # 输入的 TSV 文件路径
train_file_path = "./data/train.tsv"  # 输入的 TSV 文件路径
test_json_file = "./eval/test_data.json"  # 输出的 JSON 文件路径
train_json_file = "./eval/train_data.json"  # 输出的 JSON 文件路径

# 定义一个函数来处理 TSV 文件并生成 JSON
def process_tsv_to_json(tsv_path, output_path):
    # 使用 Pandas 读取 TSV 文件
    df = pd.read_csv(tsv_path, sep='\t')

    # 初始化结果容器
    data_list = []
    unique_intents = set()

    # 遍历数据并构造 JSON 数据结构
    for _, row in df.iterrows():
        utterance = row["text"].strip()  # 提取用户输入的语句
        intent = row["intent"].strip()  # 提取意图标签

        # 如果 domain 列为空，则根据 intent 推断 domain
        # domain = row["domain"].strip() if row["domain"].strip() else infer_domain_from_intent(intent)

        record = {
            "utterance": utterance,
            "intent": intent,
            "domain": "person voice assistance"
        }

        data_list.append(record)
        unique_intents.add(intent)

    # 构造最终的 JSON 结构
    result = {
        "data": data_list,
        "utterance_number": len(data_list),
        "intents_number": len(unique_intents),
        "intents": sorted(list(unique_intents))
    }

    # 写入 JSON 文件
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    print(f"处理完成，结果已保存到 {output_path} 中。")

# 辅助函数：根据 intent 推断 domain
def infer_domain_from_intent(intent):
    # 简单推断逻辑（可根据实际需求扩展）
    if intent.startswith("Play") or intent.startswith("AddTo"):
        return "music"
    elif intent.startswith("Rate"):
        return "books"
    else:
        return "general"

# 调用函数处理文件
process_tsv_to_json(test_file_path, test_json_file)
process_tsv_to_json(train_file_path, train_json_file)
