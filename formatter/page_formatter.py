# -*- coding: utf-8 -*-

class PageFormatter:
    """诗词页面格式化器，支持智能分页和装饰"""

    def __init__(self, settings):
        self.settings = settings
        self.lines_per_page = settings.lines_per_page
        # chars_per_line 直接表示每行字符数（全部为中文/全角字符）
        self.chars_per_line = settings.chars_per_line

    def _to_fullwidth_number(self, num):
        """将数字转换为全角数字"""
        halfwidth = '0123456789'
        fullwidth = '０１２３４５６７８９'
        trans = str.maketrans(halfwidth, fullwidth)
        return str(num).translate(trans)

    def format_poem(self, poem, next_poem=None):
        """格式化单首诗词
        Args:
            poem: 当前诗词
            next_poem: 下一首诗词（可选）
        Returns:
            list: 页面列表，每个页面是字符串
        """
        pages = []

        # 构建诗词标题区
        header_lines = self._build_header(poem)

        # 构建诗词内容区
        content_lines = self._build_content(poem)

        # 合并并分页
        all_lines = header_lines + content_lines
        pages = self._split_into_pages(all_lines, poem, next_poem)

        return pages

    def _build_header(self, poem):
        """构建诗词标题区"""
        lines = []

        # 标题和作者不再单独占行，将在装饰行中显示
        # 这里返回空列表，标题和作者会在_finalize_page中添加到装饰行

        return lines

    def _build_content(self, poem):
        """构建诗词内容"""
        all_lines = []

        for i, paragraph in enumerate(poem['paragraphs']):
            # 处理每一段，自动换行
            para_lines = self._wrap_text(paragraph)
            all_lines.extend(para_lines)

        # 移除末尾多余空行
        while all_lines and all_lines[-1] == '':
            all_lines.pop()

        # 找出最长的行
        max_len = max(len(line) for line in all_lines) if all_lines else 0

        # 计算最长行的居中位置（向左偏）
        if max_len < self.chars_per_line:
            left_padding = (self.chars_per_line - max_len) // 2
        else:
            left_padding = 0

        # 所有行都从相同位置开始（左对齐），实现最长句居中，短句与长句左对齐
        centered_lines = []
        for line in all_lines:
            centered_line = '　' * left_padding + line
            centered_lines.append(centered_line)

        return centered_lines

    def _wrap_text(self, text):
        """文本自动换行，支持逗号分隔的长句子智能分行"""
        lines = []

        # 首先按逗号分割，将较长的段落拆分成小句
        parts = text.split('，')
        current_line = ''

        for i, part in enumerate(parts):
            if not part:
                continue

            # 如果不是最后一部分，添加回逗号
            part_with_comma = part + '，' if i < len(parts) - 1 else part

            # 计算添加此部分后的长度
            potential_line = current_line + part_with_comma

            # 如果当前行为空，直接添加（即使超长也要添加）
            if not current_line:
                current_line = part_with_comma
            # 如果加上这部分会超长，先输出当前行，再开始新行
            elif len(potential_line) > self.chars_per_line:
                lines.append(current_line)
                current_line = part_with_comma
            # 否则继续追加到当前行
            else:
                current_line = potential_line

        # 处理最后一行
        if current_line:
            lines.append(current_line)

        return lines if lines else ['']

    def _split_into_pages(self, lines, poem, next_poem=None):
        """将行列表分割成页面"""
        pages = []
        current_page_lines = []
        page_num = 1
        all_page_contents = []  # 临时存储所有页面内容

        for line in lines:
            current_page_lines.append(line)

            if len(current_page_lines) >= self.lines_per_page - 3:  # 为顶部2行和底部1行装饰行预留空间
                # 页面已满，保存当前页内容
                all_page_contents.append((current_page_lines[:], page_num))
                current_page_lines = []
                page_num += 1

        # 处理最后一页
        if current_page_lines:
            all_page_contents.append((current_page_lines[:], page_num))

        # 现在我们知道总页数了，生成所有页面
        total_pages = len(all_page_contents)
        for content_lines, page_num in all_page_contents:
            is_last_page = (page_num == total_pages)
            page_content = self._finalize_page(content_lines, poem, page_num, total_pages, is_last_page, next_poem)
            pages.append(page_content)

        return pages

    def _finalize_page(self, lines, poem, page_num, total_pages, is_last_page, next_poem=None):
        """完成页面，填充空行和装饰边框"""
        result_lines = []

        # 添加顶部装饰行（带标题）
        if self.settings.enable_decoration:
            title = poem['title']  # 不加书名号
            result_lines.append(self._make_border('top', title))
            # 添加作者行（使用「」括号）
            author = f"「{poem['author']}」"
            result_lines.append(self._make_separator(author))

        # 计算剩余可用行数（总行数 - 顶部2行 - 底部1行）
        available_lines = self.lines_per_page - 3 if self.settings.enable_decoration else self.lines_per_page
        content_lines_count = len(lines)

        # 计算上下空行数，实现垂直居中（向上偏）
        if content_lines_count < available_lines:
            empty_lines_needed = available_lines - content_lines_count
            top_padding = empty_lines_needed // 2  # 向上偏：上方空行较少
            bottom_padding = empty_lines_needed - top_padding
        else:
            top_padding = 0
            bottom_padding = 0

        # 添加上方空行
        for _ in range(top_padding):
            result_lines.append(self._make_empty_line())

        # 添加内容行
        result_lines.extend(lines)

        # 添加下方空行
        for _ in range(bottom_padding):
            result_lines.append(self._make_empty_line())

        # 添加底部装饰行（带分页信息或下一首标题）
        if self.settings.enable_decoration:
            # 如果只有1页且有下一首诗，显示下一首标题
            if total_pages == 1 and next_poem:
                next_title = next_poem['title']
                # 计算可用空间（chars_per_line - 2个边框字符）
                available_width = self.chars_per_line - 2

                # 使用简洁的提示符 "▶" 节省空间
                prefix = '▶'
                prefix_len = len(prefix)

                # 如果标题太长，智能截断并加省略号
                if prefix_len + len(next_title) > available_width:
                    max_title_len = available_width - prefix_len - 1  # 留一个字符给可能的省略号
                    if max_title_len > 0:
                        next_title = next_title[:max_title_len] + '…'

                next_info = prefix + next_title
                result_lines.append(self._make_border('bottom', next_info))
            else:
                # 否则显示页码
                page_info = f'第{self._to_fullwidth_number(page_num)}／{self._to_fullwidth_number(total_pages)}页'
                result_lines.append(self._make_border('bottom', page_info))

        return '\n'.join(result_lines)

    def _center_text(self, text):
        """文本居中"""
        text_len = self._display_width(text)
        if text_len >= self.display_width:
            return text[:self.chars_per_line]

        padding = (self.display_width - text_len) // 2
        return '　' * padding + text

    def _pad_line(self, text):
        """不填充行，直接返回原文本"""
        return text

    def _display_width(self, text):
        """计算显示宽度（全部为中文/全角字符，直接返回字符数）"""
        return len(text)

    def _make_border(self, position='top', info_text=''):
        """生成边框，仅在四角显示制表符，中间可显示信息"""
        if self.settings.border_style == 'double':
            if position == 'top':
                corner_left = '╔'
                corner_right = '╗'
            else:
                corner_left = '╚'
                corner_right = '╝'
        elif self.settings.border_style == 'single':
            if position == 'top':
                corner_left = '┌'
                corner_right = '┐'
            else:
                corner_left = '└'
                corner_right = '┘'
        else:
            corner_left = '+'
            corner_right = '+'

        # 总字符数 = chars_per_line
        # 左角(1) + 中间内容 + 右角(1) = chars_per_line
        # 中间内容字符数 = chars_per_line - 2

        middle_chars = self.chars_per_line - 2

        if info_text:
            # 显示信息文本（居中）
            info_len = len(info_text)
            if info_len <= middle_chars:
                left_padding = (middle_chars - info_len) // 2
                right_padding = middle_chars - info_len - left_padding
                middle = '　' * left_padding + info_text + '　' * right_padding
            else:
                # 信息太长，截断
                middle = info_text[:middle_chars]
        else:
            # 使用全角空格填充
            middle = '　' * middle_chars

        return corner_left + middle + corner_right

    def _make_separator(self, info_text=''):
        """生成分隔线，只显示四角，可选显示居中文本"""
        if self.settings.border_style == 'double':
            corner_left = '╠'
            corner_right = '╣'
        elif self.settings.border_style == 'single':
            corner_left = '├'
            corner_right = '┤'
        else:
            corner_left = '+'
            corner_right = '+'

        middle_chars = self.chars_per_line - 2

        if info_text:
            # 显示居中文本（向左偏）
            info_len = len(info_text)
            if info_len <= middle_chars:
                left_padding = (middle_chars - info_len) // 2
                right_padding = middle_chars - info_len - left_padding
                middle = '　' * left_padding + info_text + '　' * right_padding
            else:
                # 信息太长，截断
                middle = info_text[:middle_chars]
        else:
            # 中间使用全角空格填充
            middle = '　' * middle_chars

        return corner_left + middle + corner_right

    def _make_empty_line(self):
        """生成空行（使用全角空格）"""
        return '　' * self.chars_per_line
