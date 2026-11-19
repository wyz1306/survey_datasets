import json
import os
from collections import Counter

def read_json_file(filename):
    """读取JSON文件并返回数据"""
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def merge_data(batch_data):
    """合并批次数据并返回合并后的数据和意图列表"""
    merged_data = []
    intents = []
    for data in batch_data:
        merged_data.extend(data['data'])
        intents.extend([intent['intent'] for intent in data['data']])
    return merged_data, intents

def update_statistics(stats, merged_data, intents):
    """更新统计信息"""
    stats['utterance_number'] += len(merged_data)
    stats['intents_number'] = len(set(intents))
    stats['intents_count'].update(intents)

def write_to_output_file(outfile, merged_data, stats):
    """将数据写入输出文件"""
    output = {
        "data": merged_data,
        "utterancenumber": stats['utterance_number'],
        "intentsnumber": stats['intents_number'],
        "intents": list(stats['intents_count'])
    }
    json.dump(output, outfile, indent=4, ensure_ascii=False)

def merge_json_files(filelist, batchsize, outputfile):
    """合并JSON文件"""
    # 初始化统计信息
    stats = {
        'utterance_number': 0,
        'intents_number': 0,
        'intents_count': Counter()
    }

    # 检查输出文件的目录是否存在，如果不存在则创建
    outputdir = os.path.dirname(outputfile)
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    # 分批次处理文件
    with open(outputfile, 'w', encoding='utf-8') as outfile:
        for i in range(0, len(filelist), batchsize):
            batch_files = filelist[i:i + batchsize]
            batch_data = []

            # 读取批次中的每个文件
            for filename in batch_files:
                try:
                    data = read_json_file(filename)
                    batch_data.append(data)
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    print(f"Error reading {filename}: {e}")

            # 合并批次数据
            merged_data, intents = merge_data(batch_data)

            # 更新统计信息
            update_statistics(stats, merged_data, intents)

            # 清空批次数据，释放内存
            batch_data = []

        # 写入最终合并的数据和统计信息
        write_to_output_file(outfile, merged_data, stats)

if __name__ == '__main__':
    # Run from anywhere: paths are resolved against the repository root.
    # The batched outputs written by the per-dataset loader are merged into a
    # single file named <dataset>_merge_output.json (lower case), which is what
    # the scripts under Analysis/ read. Datasets that ship separate train and
    # test splits list both files in `filelist`.
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    eval_dir = os.path.join(root, 'Datas', 'Stackoverflow', 'eval')
    filelist = [os.path.join(eval_dir, 'output_data.json')]
    batchsize = 20
    outputfile = os.path.join(eval_dir, 'stackoverflow_merge_output.json')

    merge_json_files(filelist, batchsize, outputfile)
