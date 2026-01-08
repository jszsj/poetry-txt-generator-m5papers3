# -*- coding: utf-8 -*-
"""古诗词TXT生成器 - 主程序

功能：
1. 从JSON文件批量加载古诗词
2. 按配置进行智能排版和分页
3. 生成适合ESP32电子书的TXT文件
4. 创建嵌套目录结构便于快速定位
"""
import os
import sys
from config.settings import Settings
from parser.json_parser import JsonParser
from formatter.page_formatter import PageFormatter
from generator.txt_generator import TxtGenerator
from generator.catalog_builder import CatalogBuilder

def main():
    print("="*60)
    print(" "*15 + "古诗词TXT生成器")
    print("="*60)

    # 1. 加载配置
    print("\n[1/5] 加载配置...")
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    settings = Settings()

    if os.path.exists(config_path):
        settings.load_from_file(config_path)
    else:
        print(f"  警告: 配置文件不存在，使用默认配置")
        print(f"  配置: {settings.lines_per_page}行 × {settings.chars_per_line}字符/行")

    # 将配置的标题分隔符同步到JsonParser
    JsonParser.TITLE_SEPARATOR = settings.title_separator

    # 2. 解析JSON诗词文件
    print("\n[2/5] 解析JSON诗词文件...")
    poetry_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), settings.poetry_root_dir)
    )
    print(f"  诗词根目录: {poetry_root}")

    if not os.path.exists(poetry_root):
        print(f"  错误: 诗词根目录不存在: {poetry_root}")
        return

    parser = JsonParser(poetry_root, text_conversion=settings.text_conversion)
    poems_by_category = parser.load_all_poems(
        min_length=settings.min_poem_length,
        max_length=settings.max_poem_length
    )

    total_categories = len(poems_by_category)
    total_poems = sum(len(poems) for poems in poems_by_category.values())
    print(f"  加载完成: {total_categories} 个分类，共 {total_poems} 首诗词")

    if total_poems == 0:
        print("  错误: 未找到符合条件的诗词")
        return

    # 3. 初始化格式化器
    print("\n[3/5] 初始化页面格式化器...")
    formatter = PageFormatter(settings)
    print(f"  页面设置: {settings.lines_per_page}行 × {settings.chars_per_line}字符")
    print(f"  装饰模式: {'开启' if settings.enable_decoration else '关闭'}")

    # 4. 生成TXT文件
    print("\n[4/5] 生成TXT文件...")
    generator = TxtGenerator(settings, formatter)
    file_mapping = generator.generate_all(poems_by_category)

    # 5. 生成总目录
    if settings.enable_catalog:
        print("\n[5/5] 生成总目录...")
        catalog_builder = CatalogBuilder(settings)
        catalog_content = catalog_builder.build_catalog(poems_by_category, file_mapping)
        catalog_builder.save_catalog(catalog_content, settings.output_dir)
    else:
        print("\n[5/5] 跳过目录生成（配置已禁用）")

    print("\n" + "="*60)
    print("  [完成] 全部完成！")
    print("="*60)
    print(f"\n输出目录: {os.path.abspath(settings.output_dir)}")
    print("\n使用说明:")
    print("  1. 将输出目录下的所有文件复制到ESP32电子书")
    print("  2. 按分类目录浏览，每首诗词为独立文件")
    print("  3. 查看 00_总目录.txt 了解全部内容")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n\n错误: {e}")
        import traceback
        traceback.print_exc()
