import json
import os
from collections import Counter

def load_json_data(file_path):
    """加载JSON文件并返回数据"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def calculate_utterance_statistics(data):
    """
    计算utterance的长度统计信息。
    
    参数:
    - data: 包含待分析文本的数据字典。
    
    返回:
    - 一个包含最大长度、最小长度和平均长度的字典。
    """
    utterance_lengths = [len(item["utterance"]) for item in data["data"]]
    max_length = max(utterance_lengths)
    min_length = min(utterance_lengths)
    avg_length = sum(utterance_lengths) / len(utterance_lengths)
    
    return {
        "max_length": max_length,
        "min_length": min_length,
        "avg_length": avg_length
    }

def save_results_to_json(output_path, results):
    """将统计结果保存为JSON文件"""
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Datas")
    data_sets = "Stackoverflow".strip()

    input_file_path = os.path.join(base_path, data_sets, "eval", f"{data_sets.lower()}_merge_output.json")
    output_file_path = os.path.join(base_path, data_sets, "eval", f"{data_sets.lower()}_utterance_base.json")

    try:
        data = load_json_data(input_file_path)

        # 计算并打印utterance长度统计信息
        stats = calculate_utterance_statistics(data)
        
        save_results_to_json(output_file_path, stats)
        
        print(f"Utterance统计结果已保存至 {output_file_path}")
        print("Utterance 长度统计：")
        print(f"  最大值: {stats['max_length']}")
        print(f"  最小值: {stats['min_length']}")
        print(f"  平均值: {stats['avg_length']:.2f}")
    except FileNotFoundError:
        print("错误：文件未找到，请检查路径是否正确！")
    except KeyError:
        print("错误：数据格式不正确，缺少 'data' 或 'utterance' 字段！")
    except Exception as e:
        print(f"发生未知错误：{e}")