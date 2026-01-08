# -*- coding: utf-8 -*-
import json

class Settings:
    """项目配置管理"""

    def __init__(self):
        # 页面布局设置
        self.lines_per_page = 20  # 每页行数
        self.chars_per_line = 30  # 每行字符数

        # 诗词筛选范围
        self.min_poem_length = 5
        self.max_poem_length = 1000

        # 路径配置
        self.poetry_root_dir = '../../'  # 诗词JSON根目录
        self.output_dir = '../data/output'  # 输出目录

        # 装饰配置
        self.enable_decoration = True  # 是否启用装饰
        self.decoration_char = '═'  # 装饰字符
        self.border_style = 'double'  # 边框样式: none, single, double

        # 文本格式化配置
        self.title_separator = '・'  # 标题中的分隔符（替换空格）
        self.text_conversion = 'none'  # 简繁转换: none(不转换), s2t(简→繁), t2s(繁→简), s2tw(简→台湾), tw2s(台湾→简)

        # 文件组织配置
        self.poems_per_file = 1  # 每个文件包含的诗词数量（1=一首一文件）

        # 目录配置
        self.enable_catalog = True  # 是否生成目录
        self.catalog_nested = True  # 目录是否嵌套

    def load_from_file(self, config_file):
        """从配置文件加载设置"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # 页面布局
            self.lines_per_page = config.get('page_lines', self.lines_per_page)
            self.chars_per_line = config.get('page_columns', self.chars_per_line)

            # 诗词范围
            length_range = config.get('poem_length_range', {})
            self.min_poem_length = length_range.get('min', self.min_poem_length)
            self.max_poem_length = length_range.get('max', self.max_poem_length)

            # 路径配置
            self.poetry_root_dir = config.get('input_directory', self.poetry_root_dir)
            self.output_dir = config.get('output_directory', self.output_dir)

            # 装饰和目录
            self.enable_decoration = config.get('enable_decoration', self.enable_decoration)
            self.enable_catalog = config.get('enable_catalog', self.enable_catalog)

            # 文本格式化
            self.title_separator = config.get('title_separator', self.title_separator)
            self.text_conversion = config.get('text_conversion', self.text_conversion)

            # 文件组织
            self.poems_per_file = config.get('poems_per_file', self.poems_per_file)

            print(f"配置加载成功: 每页{self.lines_per_page}行×{self.chars_per_line}字符")
        except Exception as e:
            print(f"警告: 配置文件加载失败，使用默认配置: {e}")

    def save_to_file(self, config_file):
        """保存配置到文件"""
        config = {
            'page_lines': self.lines_per_page,
            'page_columns': self.chars_per_line,
            'poem_length_range': {
                'min': self.min_poem_length,
                'max': self.max_poem_length
            },
            'input_directory': self.poetry_root_dir,
            'output_directory': self.output_dir,
            'enable_decoration': self.enable_decoration,
            'enable_catalog': self.enable_catalog,
            'title_separator': self.title_separator,
            'text_conversion': self.text_conversion,
            'poems_per_file': self.poems_per_file
        }
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, file=f, ensure_ascii=False, indent=4)
