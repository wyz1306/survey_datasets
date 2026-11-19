import json
import os
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from itertools import islice

# 加载spaCy的英语模型
import spacy

nlp = spacy.load("en_core_web_lg")


def load_json_data(file_path):
    """加载JSON文件并返回数据"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def batched(iterable, batch_size):
    """将可迭代对象分批处理"""
    it = iter(iterable)
    while True:
        batch = list(islice(it, batch_size))
        if not batch:
            break
        yield batch


def process_batch(batch):
    """
    使用spaCy处理一批数据，进行句法分析和统计。
    
    参数:
    - batch: 包含多个字典的列表，每个字典都有一个"utterance"键，其值为需要处理的句子。
    
    返回:
    - 一个字典，包含句子长度分布、词性分布和依存关系分布。
    """
    sentence_lengths = []
    pos_counter = Counter()
    dep_counter = Counter()

    # 对每条utterance进行spaCy处理
    for item in batch:
        doc = nlp(item.get("utterance", "").strip())
        sentence_lengths.append(len(doc))

        # 统计词性分布
        for token in doc:
            pos_counter[token.pos_] += 1

        # 统计依存关系
        for token in doc:
            dep_counter[token.dep_] += 1

    return {
        "sentence_length_distribution": Counter(sentence_lengths),
        "pos_distribution": pos_counter,
        "dependency_distribution": dep_counter
    }


def analyze_syntax_parallel(data, batch_size=1000, max_workers=4):
    """
    并行分析数据集中的句法结构。
    
    参数:
    - data: 包含待分析文本的数据字典。
    - batch_size: 每个批次的大小。
    - max_workers: 最大并发工作线程数。
    
    返回:
    - 一个包含句子长度分布、词性分布和依存关系分布的字典。
    """
    total_sentence_lengths = Counter()
    total_pos_counter = Counter()
    total_dep_counter = Counter()

    batches = [data["data"][i:i + batch_size] for i in range(0, len(data["data"]), batch_size)]

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(process_batch, batches)

        for result in results:
            total_sentence_lengths.update(result["sentence_length_distribution"])
            total_pos_counter.update(result["pos_distribution"])
            total_dep_counter.update(result["dependency_distribution"])

    return {
        "sentence_length_distribution": dict(total_sentence_lengths),
        "pos_distribution": dict(total_pos_counter),
        "dependency_distribution": dict(total_dep_counter)
    }


def save_results_to_json(output_path, results):
    """将统计结果保存为JSON文件"""
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Datas")
    data_sets = "Stackoverflow".strip()

    input_file_path = os.path.join(base_path, data_sets, "eval", f"{data_sets.lower()}_merge_output.json")
    output_file_path = os.path.join(base_path, data_sets, "eval", f"{data_sets.lower()}_utterance_multi.json")

    try:
        data = load_json_data(input_file_path)

        # 计算 utterance 长度统计信息
        utterance_lengths = [len(item["utterance"]) for item in data["data"]]
        max_length = max(utterance_lengths)
        min_length = min(utterance_lengths)
        avg_length = sum(utterance_lengths) / len(utterance_lengths)

        syntax_stats = analyze_syntax_parallel(data, batch_size=1000, max_workers=4)

        results = {
            "utterance_stats": {
                "max_length": max_length,
                "min_length": min_length,
                "avg_length": avg_length
            },
            "syntax_stats": syntax_stats
        }

        save_results_to_json(output_file_path, results)

        print(f"统计结果已保存至 {output_file_path}")
        print("Utterance 长度统计：")
        print(f"  最大值: {max_length}")
        print(f"  最小值: {min_length}")
        print(f"  平均值: {avg_length:.2f}")
        print("句法结构统计：")
        print(f"  句子长度分布: {syntax_stats['sentence_length_distribution']}")
        print(f"  词性分布: {syntax_stats['pos_distribution']}")
        print(f"  依存关系统计: {syntax_stats['dependency_distribution']}")
    except FileNotFoundError:
        print("错误：文件未找到，请检查路径是否正确！")
    except KeyError:
        print("错误：数据格式不正确，缺少 'data' 或 'utterance' 字段！")
    except Exception as e:
        print(f"发生未知错误：{e}")