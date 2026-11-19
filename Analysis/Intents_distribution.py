import json
import os
import sys
from collections import Counter
import matplotlib.pyplot as plt

class DatasetAnalyzer:
    def __init__(self, json_file_path, excluded_classes=None):
        """
        初始化类实例，加载 JSON 数据。
        :param json_file_path: JSON 文件路径
        :param excluded_classes: 需要排除的类别列表（可选）
        """
        self.json_file_path = json_file_path
        self.excluded_classes = excluded_classes if excluded_classes else []
        self.data_list = self.load_json_data()

    def load_json_data(self):
        """
        从 JSON 文件中加载数据。
        :return: 数据列表
        """
        with open(self.json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["data"]

    def calculate_class_counts(self, exclude=False):
        """
        统计类别分布。可以选择是否排除指定类别。
        :param exclude: 是否排除指定类别
        :return: 类别分布（Counter 对象）
        """
        # 提取所有 "intent" 的值，并根据参数决定是否排除指定类别
        names = [
            item["intent"]
            for item in self.data_list
            if not exclude or item["intent"] not in self.excluded_classes
        ]
        return Counter(names)

    def calculate_gini_index(self):
        """
        计算基尼指数和类别分布（排除指定类别）。
        :return: 基尼指数、类别分布、总样本数
        """
        # 计算类别分布（排除指定类别）
        class_counts = self.calculate_class_counts(exclude=True)
        total_samples = sum(class_counts.values())
        
        # 如果没有有效样本，则返回默认值
        if total_samples == 0:
            return 0.0, class_counts, 0
        
        # 计算每个类别的比例
        proportions = [count / total_samples for count in class_counts.values()]
        
        # 计算基尼指数
        gini_index = 1 - sum(p**2 for p in proportions)
        return gini_index, class_counts, total_samples

    def calculate_imbalance_ratio(self, class_counts):
        """
        计算类别不平衡度（Imbalance Ratio）。
        :param class_counts: 类别分布（Counter 对象）
        :return: 不平衡度
        """
        max_count = max(class_counts.values()) if class_counts else 0
        min_count = min(class_counts.values()) if class_counts else 0
        imbalance_ratio = max_count / min_count if min_count > 0 else float('inf')
        return imbalance_ratio

    def plot_class_distribution(self, class_counts):
        """
        可视化类别分布（不进行排除）。
        :param class_counts: 类别分布（Counter 对象）
        """
        labels = list(class_counts.keys())
        values = list(class_counts.values())
        
        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color='skyblue')
        plt.title("Class Distribution")
        plt.xlabel("Class (Intent)")
        plt.ylabel("Number of Samples")
        plt.xticks(rotation=45)
        plt.show()

    def save_class_distribution_plot(self, class_counts, output_image_path):
        """
        保存类别分布的可视化图为图片文件（不进行排除）。
        :param class_counts: 类别分布（Counter 对象）
        :param output_image_path: 输出图片文件路径
        """
        labels = list(class_counts.keys())
        values = list(class_counts.values())
        
        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color='skyblue')
        plt.title("Class Distribution")
        plt.xlabel("Class (Name)")
        plt.ylabel("Number of Samples")
        plt.xticks(rotation=45)
        
        plt.savefig(output_image_path, bbox_inches='tight')  # 确保标签不被裁剪
        plt.close()  # 关闭图形，避免内存泄漏
    def save_results_to_json(self, results, output_file_path):
        """
        将分析结果保存到 JSON 文件中。
        :param results: 分析结果字典
        :param output_file_path: 输出 JSON 文件路径
        """
        with open(output_file_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
    def analyze(self, output_file_path=None, output_image_path=None):
        """
        主分析方法：计算基尼指数、类别分布、类别不平衡度，并可视化。
        如果提供了 output_file_path，则保存结果到 JSON 文件。
        如果提供了 output_image_path，则保存可视化图为图片文件。
        """
        # 计算基尼指数和类别分布（排除指定类别）
        gini_index, filtered_class_counts, total_samples = self.calculate_gini_index()
        
        # 计算类别不平衡度
        imbalance_ratio = self.calculate_imbalance_ratio(filtered_class_counts)
        
        # 获取完整的类别分布（不进行排除）
        full_class_counts = self.calculate_class_counts(exclude=False)
        
        # 计算类别比例（基于排除后的类别分布）
        class_proportions = {key: value / total_samples for key, value in filtered_class_counts.items()}
        
        names = [
            item["intent"]
            for item in self.data_list]
        # 构造结果字典
        results = {
            "total_samples": sum(Counter(names).values()),
            "class_distribution": dict(full_class_counts),  # 使用完整类别分布
            "gini_index": gini_index,
            "imbalance_ratio": imbalance_ratio,
            "class_proportions": class_proportions
        }
        
        # 输出统计结果
        print("Analysis Results:")
        print(json.dumps(results, indent=4, ensure_ascii=False))
        
        # 如果指定了输出文件路径，则保存结果到 JSON 文件
        if output_file_path:
            self.save_results_to_json(results, output_file_path)
            print(f"Results saved to {output_file_path}")
        
        # 可视化类别分布（使用完整类别分布）
        self.plot_class_distribution(full_class_counts)
        
        # 如果指定了输出图片路径，则保存可视化图为图片文件（使用完整类别分布）
        if output_image_path:
            self.save_class_distribution_plot(full_class_counts, output_image_path)
            print(f"Visualization saved to {output_image_path}")


# 如果直接运行脚本，则调用主分析方法
if __name__ == '__main__':
    # 基准路径
    base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Datas")
    # 提取的字符串
    dataset_name = "Stackoverflow"
    # 评估路径
    eval_path = "eval"
    # 构建完整的基准路径
    full_base_path = os.path.join(base_path, dataset_name, eval_path)
    # 替换为你的 JSON 文件路径
    json_file_path = os.path.join(full_base_path, f"{dataset_name}_merge_output.json")
    
    # 定义需要排除的类别
    # excluded_classes = ["Unknown"]
    excluded_classes = [""]
    
    # 创建类实例并进行分析
    analyzer = DatasetAnalyzer(json_file_path, excluded_classes=excluded_classes)
    
    # 指定输出 JSON 文件路径
    output_file_path = os.path.join(full_base_path, f"{dataset_name}_analysis_results.json")

    # 指定输出图片文件路径
    output_image_path = os.path.join(full_base_path, f"{dataset_name}_class_distribution.png")

    # 进行分析并将结果保存到 JSON 文件和图片文件
    analyzer.analyze(output_file_path=output_file_path, output_image_path=output_image_path)