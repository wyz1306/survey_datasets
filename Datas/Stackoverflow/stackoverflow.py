import json
# 数据来源https://codeload.github.com/jacoxu/StackOverflow/zip/refs/heads/master
# 文件路径
utterances_file = "./rawText/title_StackOverflow.txt"  # 第一个文件：问题列表
domains_file = "./rawText/label_StackOverflow.txt"  # 第二个文件：领域编号
mapping_file = "./rawText/intent_label.txt"  # 第三个文件：领域编号与名称的映射

output_json_file = "./eval/output_data.json"  # 输出的 JSON 文件路径

# 定义一个函数来处理文件并生成 JSON
def process_files_to_json(utterances_path, domains_path, mapping_path, output_path):
    # 读取第一个文件：问题列表
    with open(utterances_path, "r", encoding="utf-8") as f:
        utterances = [line.strip() for line in f if line.strip()]

    # 读取第二个文件：领域编号
    with open(domains_path, "r", encoding="utf-8") as f:
        domain_ids = [line.strip() for line in f if line.strip()]

    # 读取第三个文件：领域编号与名称的映射
    domain_mapping = {}
    with open(mapping_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                parts = line.strip().split()
                domain_id = parts[0]
                domain_name = parts[1]
                domain_mapping[domain_id] = domain_name

    # 检查数据长度是否一致
    if len(utterances) != len(domain_ids):
        raise ValueError("utterances 和 domain_ids 的长度不一致，请检查输入文件！")

    # 构造 JSON 数据
    data_list = []
    unique_intents = set()

    for i in range(len(utterances)):
        utterance = utterances[i]
        domain_id = domain_ids[i]

        # 获取领域名称
        domain_name = domain_mapping.get(domain_id, "Unknown")

        record = {
            "utterance": utterance,
            "intent": domain_name,
            "domain": "software"
        }

        data_list.append(record)
        unique_intents.add(domain_name)

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

# 调用函数处理文件
process_files_to_json(utterances_file, domains_file, mapping_file, output_json_file)