# -*- coding: utf-8 -*-
import json
import os

class JsonParser:
    """解析JSON诗词文件，支持批量读取和分类"""

    def __init__(self, poetry_root_dir):
        """初始化
        Args:
            poetry_root_dir: 诗词JSON文件的根目录
        """
        self.poetry_root_dir = poetry_root_dir
        self.poems_by_category = {}

    # 标题分隔符配置（类变量）
    TITLE_SEPARATOR = '・'  # 标题中的分隔符，可配置

    @staticmethod
    def _normalize_title_spaces(text):
        """将标题中的空格转换为分隔符，连续空格合并为一个分隔符
        Args:
            text: 待处理标题文本
        Returns:
            str: 转换后的文本
        """
        if not text:
            return text
        import re
        # 将一个或多个连续空格（半角或全角）替换为一个分隔符
        text = re.sub(r'[\s　]+', JsonParser.TITLE_SEPARATOR, text)
        return text

    @staticmethod
    def _normalize_spaces(text):
        """将英文空格转换为全角空格，确保排版整齐
        Args:
            text: 待处理文本
        Returns:
            str: 转换后的文本
        """
        if not text:
            return text
        # 将半角空格转换为全角空格
        return text.replace(' ', '　')

    def is_chinese_directory(self, dirname):
        """判断是否为中文目录（诗词分类目录）"""
        for char in dirname:
            if '\u4e00' <= char <= '\u9fff':
                return True
        return False

    def load_all_poems(self, min_length=0, max_length=float('inf')):
        """加载所有诗词JSON文件
        Args:
            min_length: 最小诗词长度
            max_length: 最大诗词长度
        Returns:
            dict: {分类名: [诗词列表]}
        """
        for item in os.listdir(self.poetry_root_dir):
            item_path = os.path.join(self.poetry_root_dir, item)

            # 只处理中文目录
            if not os.path.isdir(item_path) or not self.is_chinese_directory(item):
                continue

            category_name = item
            self.poems_by_category[category_name] = []

            # 遍历目录中的JSON文件
            for filename in os.listdir(item_path):
                if not filename.endswith('.json'):
                    continue

                file_path = os.path.join(item_path, filename)
                try:
                    poems = self._parse_json_file(file_path, min_length, max_length)
                    self.poems_by_category[category_name].extend(poems)
                except Exception as e:
                    print(f"警告: 读取 {file_path} 失败: {e}")

        return self.poems_by_category

    def _parse_json_file(self, file_path, min_length, max_length):
        """解析单个JSON文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        poems = []

        # 处理不同的JSON格式
        if isinstance(data, list):
            # 格式：[{title: ..., paragraphs: [...]}, ...]
            for item in data:
                poem = self._extract_poem_info(item)
                if poem and min_length <= poem['length'] <= max_length:
                    poems.append(poem)
        elif isinstance(data, dict):
            # 格式：{title: ..., paragraphs: [...]}
            poem = self._extract_poem_info(data)
            if poem and min_length <= poem['length'] <= max_length:
                poems.append(poem)

        return poems

    def _extract_poem_info(self, data):
        """提取诗词信息"""
        title = data.get('title', '无题')
        author = data.get('author', '佚名')
        paragraphs = data.get('paragraphs', [])

        if not paragraphs:
            return None

        # 标题：将空格转换为分隔符・（连续空格合并）
        title = self._normalize_title_spaces(title)
        # 作者：将空格转换为全角空格
        author = self._normalize_spaces(author)

        # 将诗句中的英文空格转换为全角空格
        paragraphs = [self._normalize_spaces(para) for para in paragraphs]

        # 计算诗词总长度
        content = ''.join(paragraphs)
        length = len(content)

        return {
            'title': title,
            'author': author,
            'paragraphs': paragraphs,
            'content': content,
            'length': length
        }
