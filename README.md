# 古诗词 TXT 生成器

为 M5 PaperS3 电子书固件设计的古诗词 TXT 文件生成工具。
目前仅针对梦西游啊游大佬的固件进行了测试，其他固件请自行测试。

感谢梦西游啊游大佬提供的固件：[edcbook](https://edcbook.cn/)

## 数据来源

本项目使用 [chinese-poetry](https://github.com/chinese-poetry/chinese-poetry) 开源诗词库作为数据源。

- 📚 最全中华古诗词数据库，包含唐诗、宋词、元曲等
- 📖 数据格式规范，JSON 结构清晰
- 🔄 通过 Git Submodule 方式引入，方便更新

感谢 [chinese-poetry](https://github.com/chinese-poetry/chinese-poetry) 项目的贡献者们！

## 功能特性

✅ **智能排版**: 可自定义每页行数和每行字符数
✅ **自动分页**: 短诗一页一首，长诗自动分页
✅ **装饰美化**: 支持边框、分隔线等装饰元素
✅ **目录嵌套**: 按分类生成嵌套目录结构，便于快速定位
✅ **批量处理**: 自动读取所有诗词 JSON 文件
✅ **长度筛选**: 可设置诗词长度范围

## 项目结构

```
poetry-txt-generator/
├── config.json              # 配置文件
├── requirements.txt         # Python 依赖
├── README.md               # 本文档
├── src/                    # 源代码
│   ├── main.py            # 主程序入口
│   ├── config/
│   │   └── settings.py    # 配置管理
│   ├── parser/
│   │   └── json_parser.py # JSON 解析器
│   ├── formatter/
│   │   └── page_formatter.py      # 页面格式化
│   └── generator/
│       ├── txt_generator.py       # TXT 生成器
│       └── catalog_builder.py     # 目录构建器
└── data/
    └── output/            # 生成的 TXT 文件输出目录
```

## 配置说明

编辑 `config.json` 文件自定义生成参数：

```json
{
    "page_lines": 14,                       // 每页行数
    "page_columns": 13,                     // 每行字符数
    "poem_length_range": {
        "min": 5,                            // 最小诗词长度（字符数）
        "max": 1000                          // 最大诗词长度
    },
    "input_directory": "./data/input",      // 诗词 JSON 根目录（见下方配置示例）
    "output_directory": "./data/output",    // 输出目录
    "enable_decoration": true,              // 是否启用装饰（边框）
    "enable_catalog": true,                 // 是否生成总目录
    "title_separator": "・",                // 标题分隔符
    "poems_per_file": 20                    // 每个文件包含的诗词数量
}
```

### 数据源配置

根据你的使用场景，选择以下配置方式之一：

#### 方式 1：直接使用 Submodule 数据（推荐）

```json
{
  "input_directory": "./data/chinese-poetry/全唐诗"
}
```

优点：无需复制数据，节省磁盘空间，可随时更新

#### 方式 2：使用自定义数据目录

```json
{
  "input_directory": "./data/input"
}
```

然后手动从 `data/chinese-poetry/` 复制所需数据到 `data/input/`
根据需要建立分类目录，目录名为中文，将对应的诗词json数据复制到对应的分类目录中，input目录内容示例：

```text
output/
├── 唐诗三百首/
│   └── 唐诗三百首.json
└── 宋词三百首/
    └── 宋词三百首.json
```

**可用的数据目录：**

- `./data/chinese-poetry/全唐诗`
- `./data/chinese-poetry/宋词`
- `./data/chinese-poetry/元曲`
- `./data/chinese-poetry/诗经`
- `./data/chinese-poetry/蒙学`
- 更多见 `data/chinese-poetry/` 目录

**注意1** 由于中文间隔号"·"不是全角显示，有点儿强迫症，所以使用了日文中的"・"字符当做间隔号，需要使用字体转换工具，添加自定义字符：0x30FB，否则间隔号将显示为口
**注意2** 当前版本未测试直接使用data/chinese-poetry中的某个全量数据目录，由于内容较多，全量生成策略还未考虑成熟，建议手动复制少量数据进行生成

## 使用方法

### 1. 克隆项目并初始化 Submodule

```bash
# 克隆项目
git clone https://github.com/jszsj/poetry-txt-generator-m5papers3.git
cd poetry-txt-generator-m5papers3

# 初始化并更新 submodule（下载诗词数据库）
git submodule update --init --recursive
```

**注意：** chinese-poetry 数据库较大（约 237 MB），初次下载需要一些时间。

### 2. 创建配置文件

```bash
# 从示例文件复制配置
cp config.json.example config.json

# 或在 Windows PowerShell 中
copy config.json.example config.json
```

然后根据需求编辑 `config.json`。

### 3. 配置参数

根据你的需求编辑 `config.json`：

1. **调整显示参数**：根据你的屏幕/字体大小设置 `page_lines` 和 `page_columns`
2. **选择数据源**：设置 `input_directory`（参考上方"数据源配置"）
3. **其他选项**：装饰开关、诗词长度范围等

### 4. 运行程序

```bash
python main.py
```

### 4. 查看输出

生成的文件位于 `./data/output/` 目录：

```text
output/
├── 00_总目录.txt           # 全部诗词总目录
├── 唐诗三百首/
│   ├── 00_目录.txt        # 分类目录
│   ├── 0001_静夜思.txt
│   ├── 0002_春晓.txt
│   └── ...
├── 宋词/
│   ├── 00_目录.txt
│   ├── 0001_水调歌头.txt
│   └── ...
└── ...
```

## 目录结构设计

### 层级 1：分类目录

按诗词来源分类（蒙学、唐诗、宋词、元曲等），每个分类一个文件夹。

### 层级 2：分类索引

每个分类文件夹内有 `00_目录.txt`，列出该分类下所有诗词。

### 层级 3：诗词文件

每首诗词独立的 TXT 文件，文件名格式：`序号_诗词名.txt`

### 总目录

`00_总目录.txt` 提供全局概览，显示所有分类和诗词数量。

## 排版特性

### 1. 智能标题居中

诗词标题和作者名自动居中对齐

### 2. 自动换行

长句子按每行字符数自动换行，保持美观

### 3. 装饰边框

```text
╔　　　登鸛雀樓　　　　╗
╠　　　「王之渙」　　　╣
　　　　　　　　　　　　　
　　　　　　　　　　　　　
　　　　　　　　　　　　　
　　　　　　　　　　　　　
白日依山盡，黃河入海流。
欲窮千里目，更上一層樓。
　　　　　　　　　　　　　
　　　　　　　　　　　　　
　　　　　　　　　　　　　
　　　　　　　　　　　　　
　　　　　　　　　　　　　
╚　▶涼州詞二首・一　　╝
```

### 4. 多页诗词

长诗自动分页，每页顶部显示页码：

```
[第1/3页]
```

## 快速定位技巧

在paper s3中：

1. **按朝代查找**: 进入对应分类目录（唐诗三百首、宋词等）
2. **按序号浏览**: 文件名带序号，方便按顺序阅读
3. **查看索引**: 打开分类的 `00_目录.txt` 快速了解包含内容
4. **总目录**: 查看 `00_总目录.txt` 了解全部收录内容

## 常见问题

### Q: 如何调整页面大小？

A: 修改 `config.json` 中的 `page_lines` 和 `page_columns` 参数。

### Q: 如何只生成特定长度的诗词？

A: 调整 `poem_length_range` 的 `min` 和 `max` 值。

### Q: 是否可以关闭装饰边框？

A: 将 `enable_decoration` 设为 `false`。

### Q: 生成的文件中文乱码？

A: 确保 ESP32 支持 UTF-8 编码。所有生成的文件使用 UTF-8 编码。

### Q: 如何更新诗词数据？

A: 进入 submodule 目录更新：

```bash
cd data/chinese-poetry
git pull origin master
```

## 许可证

MIT

诗词数据来自 [chinese-poetry](https://github.com/chinese-poetry/chinese-poetry) 项目，遵循其开源许可证。

## 更新日志

### v0.1.0 (2026-01-07)

- ✅ 初始版本
- ✅ 支持批量 JSON 解析
- ✅ 智能分页和排版
- ✅ 装饰边框
- ✅ 嵌套目录结构
- ✅ 完整配置系统
