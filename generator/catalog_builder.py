# -*- coding: utf-8 -*-
import os

class CatalogBuilder:
    """目录构建器，生成嵌套目录结构"""

    def __init__(self, settings):
        self.settings = settings
        self.page_width = settings.chars_per_line
        self.page_lines = settings.lines_per_page

    def _to_fullwidth_number(self, num):
        """将数字转换为全角数字"""
        halfwidth = '0123456789'
        fullwidth = '０１２３４５６７８９'
        trans = str.maketrans(halfwidth, fullwidth)
        return str(num).translate(trans)

    def _make_border(self, text=''):
        """生成适配页面宽度的边框"""
        if self.settings.enable_decoration:
            if text:
                # 居中文本
                text_len = len(text)
                if text_len + 2 <= self.page_width:
                    left_pad = (self.page_width - text_len - 2) // 2
                    right_pad = self.page_width - text_len - 2 - left_pad
                    return '╔' + '　' * left_pad + text + '　' * right_pad + '╗'
                else:
                    return '╔' + text[:self.page_width-2] + '╗'
            else:
                return '╔' + '　' * (self.page_width - 2) + '╗'
        else:
            return '═' * self.page_width

    def _make_separator(self):
        """生成分隔线"""
        if self.settings.enable_decoration:
            return '╠' + '　' * (self.page_width - 2) + '╣'
        else:
            return '─' * self.page_width

    def _make_bottom_border(self):
        """生成底部边框"""
        if self.settings.enable_decoration:
            return '╚' + '　' * (self.page_width - 2) + '╝'
        else:
            return '═' * self.page_width

    def _center_text(self, text):
        """文本居中"""
        text_len = len(text)
        if text_len >= self.page_width:
            return text[:self.page_width]
        left_pad = (self.page_width - text_len) // 2
        return '　' * left_pad + text

    def build_catalog(self, poems_by_category, file_mapping):
        """构建目录文件
        Args:
            poems_by_category: {分类名: [诗词列表]}
            file_mapping: {分类名: {诗词title: 文件名}}
        Returns:
            str: 目录内容
        """
        lines = []

        # 标题
        lines.append(self._make_border('总目录'))
        lines.append(self._center_text('【古诗词】'))
        lines.append(self._make_separator())

        # 按分类生成目录
        for idx, (category, poems) in enumerate(sorted(poems_by_category.items()), 1):
            if not poems:
                continue

            # 分类标题：全角序号・分类名「数量」
            idx_str = self._to_fullwidth_number(idx)
            count_str = self._to_fullwidth_number(len(poems))
            category_line = f"{idx_str}・{category}「{count_str}首」"
            lines.append(category_line[:self.page_width])

        lines.append(self._make_bottom_border())

        return '\n'.join(lines)

    def save_catalog(self, catalog_content, output_dir):
        """保存目录文件"""
        os.makedirs(output_dir, exist_ok=True)
        catalog_file = os.path.join(output_dir, '00_总目录.txt')

        with open(catalog_file, 'w', encoding='utf-8') as f:
            f.write(catalog_content)

        print(f"目录已生成: {catalog_file}")
        return catalog_file
