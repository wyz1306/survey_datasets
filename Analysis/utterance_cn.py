import json
import os
import torch
from ltp import LTP
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from itertools import islice

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

def init_ltp():
    # 初始化LTP模型
    ltp = LTP(pretrained_model_name_or_path="../LTP/")  # 确保路径正确
    if torch.cuda.is_available():
        # 设置CUDA可见性，确保不同进程不会争夺相同的GPU资源
        os.environ["CUDA_VISIBLE_DEVICES"] = str(os.getpid() % torch.cuda.device_count())
        ltp.to("cuda:0")
    return ltp

def process_batch(batch, ltp):
    """
    处理一批数据，进行句法分析和统计。
    
    参数:
    - batch: 包含多个字典的列表，每个字典都有一个"utterance"键，其值为需要处理的句子。
    - ltp: 已初始化的LTP实例。
    
    返回:
    - 一个字典，包含句子长度分布、词性分布和依存关系分布。
    """
    sentence_lengths = []
    pos_counter = Counter()
    dep_counter = Counter()

    # 使用pipeline方法代替单独调用segment, pos, dep等方法
    output = ltp.pipeline(
        [item.get("utterance", "").strip() for item in batch if item.get("utterance", "").strip()],
        tasks=["cws", "pos", "dep"]
    )

    # 对于每一条utterance的分词、词性和依存关系结果
    for utterance_seg, utterance_pos, utterance_dep in zip(output.cws, output.pos, output.dep):
        # 记录句子长度
        sentence_lengths.append(len(utterance_seg))
        
        # 统计词性分布
        for word_pos in utterance_pos:
            pos_counter[word_pos] += 1
        
        # 检查并处理依存关系
        for dep in utterance_dep:
            if len(dep) >= 3:  # 确保至少有三个元素
                _, _, dep_relation = dep[:3]  # 只取前三个元素
                dep_counter[dep_relation] += 1
            else:
                print(f"Unexpected dependency structure detected: {dep}")
    
    return {
        "sentence_length_distribution": Counter(sentence_lengths),
        "pos_distribution": pos_counter,
        "dependency_distribution": dep_counter
    }
def process_batch_with_ltp(batch):
    ltp_instance = init_ltp()
    return process_batch(batch, ltp_instance)
# def replace_pos_keys_with_descriptions(pos_distribution):
#     """
#     将结果中词性分布的键改换成描述。
    
#     参数:
#     - pos_distribution: 一个Counter对象，包含词性分布的统计信息。
    
#     返回:
#     - 一个新的Counter对象，其中原来的词性标签被替换成了相应的描述。
#     """
#     # 定义词性标签到描述的映射
#     pos_to_description = {
#         'a': 'adjective', 'ni': 'organization name',
#         'b': 'other noun-modifier ', 'nl': 'location noun',
#         'c': 'conjunction', 'ns': 'geographical name ',
#         'd': 'adverb', 'nt': 'temporal noun ',
#         'e': 'exclamation', 'nz': 'other proper noun' ,
#         'g': 'morpheme', 'o': 'onomatopoeia',
#         'h': 'prefix', 'p': 'preposition',
#         'i': 'idiom', 'q': 'quantity',
#         'j': 'abbreviation', 'r': 'pronoun',
#         'k': 'suffix', 'u': 'auxiliary',
#         'm': 'number', 'v': 'verb',
#         'n': 'general noun', 'wp': 'punctuation',
#         'nd': 'direction noun', 'ws': 'foreign words',
#         'nh': 'person name', 'x': 'non-lexeme',
#         'z': 'descriptive words'
#     }

#     # 创建一个新的Counter对象用于存储转换后的数据
#     converted_distribution = Counter()

#     # 遍历原始的词性分布并进行转换
#     for pos_tag, count in pos_distribution.items():
#         if pos_tag in pos_to_description:
#             description = pos_to_description[pos_tag]
#             converted_distribution[description] += count
#         else:
#             # 如果没有找到对应的描述，则保留原标签
#             converted_distribution[pos_tag] += count

#     return converted_distribution

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

    # # 在每个子进程中重新初始化LTP实例
    # process_batch_with_ltp(batch=batched)

    batches = [data["data"][i:i + batch_size] for i in range(0, len(data["data"]), batch_size)]
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(process_batch_with_ltp, batches)
        
        for result in results:
            total_sentence_lengths.update(result["sentence_length_distribution"])
            total_pos_counter.update(result["pos_distribution"])
            total_dep_counter.update(result["dependency_distribution"])
    
    # total_pos_counter=replace_pos_keys_with_descriptions(total_pos_counter)
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
    data_sets = "Banking".strip()

    input_file_path = os.path.join(base_path, data_sets, "eval", f"{data_sets.lower()}_merge_output.json")
    output_file_path = os.path.join(base_path, data_sets, "eval", f"{data_sets.lower()}_combined_result.json")

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