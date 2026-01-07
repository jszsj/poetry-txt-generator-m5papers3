# -*- coding: utf-8 -*-
import os

class TxtGenerator:
    """TXT文件生成器"""

    def __init__(self, settings, formatter):
        self.settings = settings
        self.formatter = formatter
        self.file_mapping = {}  # {分类: {诗词title: 文件名}}

    def generate_all(self, poems_by_category):
        """生成所有TXT文件
        Args:
            poems_by_category: {分类名: [诗词列表]}
        Returns:
            dict: 文件映射表
        """
        output_dir = self.settings.output_dir
        output_dir = os.path.abspath(output_dir)

        # 如果output_dir是文件，先删除
        if os.path.exists(output_dir) and os.path.isfile(output_dir):
            os.remove(output_dir)

        os.makedirs(output_dir, exist_ok=True)

        total_poems = sum(len(poems) for poems in poems_by_category.values())
        processed = 0

        print(f"\n开始生成TXT文件，共 {len(poems_by_category)} 个分类，{total_poems} 首诗词")
        print("=" * 60)

        for category, poems in sorted(poems_by_category.items()):
            if not poems:
                continue

            print(f"\n处理分类: {category} ({len(poems)}首)")

            # 为每个分类创建子目录
            category_dir = os.path.join(output_dir, category)
            os.makedirs(category_dir, exist_ok=True)

            self.file_mapping[category] = {}

            # 根据配置决定生成方式
            poems_per_file = self.settings.poems_per_file

            if poems_per_file == 1:
                # 一首诗一个文件（原有逻辑）
                for idx, poem in enumerate(poems, 1):
                    try:
                        self._generate_poem_file(poem, category, category_dir, idx)
                        self.file_mapping[category][poem['title']] = f"{idx:04d}_{poem['title']}.txt"
                        processed += 1

                        if processed % 10 == 0:
                            print(f"  已处理: {processed}/{total_poems}")

                    except Exception as e:
                        print(f"  警告: 生成《{poem['title']}》失败: {e}")
            else:
                # 多首诗合并到一个文件
                for batch_start in range(0, len(poems), poems_per_file):
                    batch_poems = poems[batch_start:batch_start + poems_per_file]
                    batch_idx = batch_start // poems_per_file + 1

                    try:
                        filename = self._generate_batch_file(batch_poems, category, category_dir, batch_idx, batch_start + 1)
                        # 记录批次中每首诗的文件映射
                        for poem in batch_poems:
                            self.file_mapping[category][poem['title']] = filename
                        processed += len(batch_poems)

                        if processed % 10 == 0:
                            print(f"  已处理: {processed}/{total_poems}")

                    except Exception as e:
                        print(f"  警告: 生成批次 {batch_idx} 失败: {e}")

            # 生成分类索引文件
            self._generate_category_index(category, poems, category_dir)

        print(f"\n=" * 60)
        print(f"生成完成！共处理 {processed} 首诗词")
        print(f"输出目录: {os.path.abspath(output_dir)}")

        return self.file_mapping

    def _generate_poem_file(self, poem, category, category_dir, index):
        """生成单首诗词的TXT文件"""
        # 计算子目录范围（每100个文件一个子目录）
        start_idx = ((index - 1) // 100) * 100 + 1
        end_idx = start_idx + 99
        subdir_name = f"{start_idx:03d}-{end_idx:03d}"
        subdir_path = os.path.join(category_dir, subdir_name)
        os.makedirs(subdir_path, exist_ok=True)

        # 格式化诗词内容
        pages = self.formatter.format_poem(poem)

        # 安全的文件名
        safe_title = self._safe_filename(poem['title'])
        filename = f"{index:04d}_{safe_title}.txt"
        filepath = os.path.join(subdir_path, filename)

        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            for page_idx, page in enumerate(pages, 1):
                f.write(page)
                if page_idx < len(pages):
                    f.write("\n")  # 添加换行符让下一页从新行开始

    def _generate_batch_file(self, poems, category, category_dir, batch_idx, start_poem_idx):
        """生成包含多首诗词的批次文件
        Args:
            poems: 诗词列表（该批次的所有诗）
            category: 分类名
            category_dir: 分类目录
            batch_idx: 批次编号
            start_poem_idx: 起始诗词编号
        Returns:
            str: 文件名
        """
        # 计算子目录范围
        start_idx = ((start_poem_idx - 1) // 100) * 100 + 1
        end_idx = start_idx + 99
        subdir_name = f"{start_idx:03d}-{end_idx:03d}"
        subdir_path = os.path.join(category_dir, subdir_name)
        os.makedirs(subdir_path, exist_ok=True)

        # 生成文件名：起止序号
        end_poem_idx = start_poem_idx + len(poems) - 1
        filename = f"{start_poem_idx:04d}-{end_poem_idx:04d}_合集.txt"
        filepath = os.path.join(subdir_path, filename)

        # 格式化所有诗词
        with open(filepath, 'w', encoding='utf-8') as f:
            for idx, poem in enumerate(poems):
                # 获取下一首诗的信息（如果有）
                next_poem = poems[idx + 1] if idx < len(poems) - 1 else None

                # 格式化当前诗词
                pages = self.formatter.format_poem(poem, next_poem)

                # 写入所有页面
                for page_idx, page in enumerate(pages, 1):
                    f.write(page)
                    if page_idx < len(pages):
                        f.write("\n")

                # 如果不是最后一首诗，添加一个换行分隔
                if idx < len(poems) - 1:
                    f.write("\n")

        return filename

    def _to_fullwidth_number(self, num):
        """将数字转换为全角数字"""
        halfwidth = '0123456789'
        fullwidth = '０１２３４５６７８９'
        trans = str.maketrans(halfwidth, fullwidth)
        return str(num).translate(trans)

    def _generate_category_index(self, category, poems, category_dir):
        """生成分类索引文件（按子目录拆分）"""
        # 按照100个一组分割诗词列表
        total_poems = len(poems)
        poems_per_file = self.settings.poems_per_file
        page_width = self.settings.chars_per_line
        page_lines = self.settings.lines_per_page

        for start_idx in range(0, total_poems, 100):
            end_idx = min(start_idx + 100, total_poems)
            batch_poems = poems[start_idx:end_idx]

            # 子目录范围
            range_start = start_idx + 1
            range_end = end_idx

            # 目录文件名
            index_file = os.path.join(category_dir, f'目录{range_start:03d}-{range_end:03d}.txt')

            lines = []

            # 顶部边框
            if self.settings.enable_decoration:
                lines.append('╔' + '　' * (page_width - 2) + '╗')
                # 分类名居中
                category_text = f'【{category}】'
                text_len = len(category_text)
                if text_len < page_width - 2:
                    left_pad = (page_width - 2 - text_len) // 2
                    lines.append('╠' + '　' * left_pad + category_text + '　' * (page_width - 2 - text_len - left_pad) + '╣')
                else:
                    lines.append('╠' + category_text[:page_width-2] + '╣')

                # 范围信息 - 使用全角数字和波浪号
                range_text = f'第{self._to_fullwidth_number(range_start)}～{self._to_fullwidth_number(range_end)}首'
                text_len = len(range_text)
                if text_len < page_width - 2:
                    left_pad = (page_width - 2 - text_len) // 2
                    lines.append('╠' + '　' * left_pad + range_text + '　' * (page_width - 2 - text_len - left_pad) + '╣')
                lines.append('╚' + '　' * (page_width - 2) + '╝')
            else:
                lines.append('═' * page_width)
                lines.append(f"{category} ({range_start}～{range_end})".center(page_width, '　'))
                lines.append('═' * page_width)

            if poems_per_file == 1:
                # 一首一文件模式 - 标题和作者分行显示
                for idx, poem in enumerate(batch_poems, start_idx + 1):
                    title = poem['title']
                    author = poem['author']
                    # 格式：全角序号・标题
                    #      「作者」
                    num_str = self._to_fullwidth_number(f"{idx:03d}")
                    title_line = f"{num_str}・{title}"
                    author_line = f"　　「{author}」"
                    lines.append(title_line)
                    lines.append(author_line)
            else:
                # 多首合并模式 - 按文件分组
                for file_start in range(0, len(batch_poems), poems_per_file):
                    file_poems = batch_poems[file_start:file_start + poems_per_file]
                    global_start = start_idx + file_start + 1
                    global_end = global_start + len(file_poems) - 1

                    # 文件标题 - 使用全角数字和波浪号
                    file_line = f"━{self._to_fullwidth_number(f'{global_start:04d}')}～{self._to_fullwidth_number(f'{global_end:04d}')}━"
                    lines.append(file_line[:page_width])

                    # 列出文件中的诗词 - 标题和作者分行显示
                    for idx, poem in enumerate(file_poems):
                        poem_idx = global_start + idx
                        title = poem['title']
                        author = poem['author']
                        # 全角序号和标题
                        num_str = self._to_fullwidth_number(f"{poem_idx:03d}")
                        title_line = f"{num_str}・{title}"
                        author_line = f"　　「{author}」"
                        lines.append(title_line)
                        lines.append(author_line)

            with open(index_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))

    def _safe_filename(self, filename):
        """生成安全的文件名"""
        # 替换不安全字符
        unsafe_chars = '<>:"/\\|?*'
        for char in unsafe_chars:
            filename = filename.replace(char, '_')
        # 限制长度
        if len(filename) > 50:
            filename = filename[:50]
        return filename
