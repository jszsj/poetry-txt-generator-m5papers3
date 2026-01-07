# 配置示例说明

## 数据源选择

### 方式 1: 直接使用 Submodule 数据（推荐）

无需复制数据，直接配置路径：

```json
{
    "input_directory": "./data/chinese-poetry/全唐诗"
}
```

**可用的数据源：**
- `./data/chinese-poetry/全唐诗` - 完整唐诗（约 42,863 首）
- `./data/chinese-poetry/宋词` - 宋词全集（约 21,050 首）
- `./data/chinese-poetry/元曲` - 元曲集
- `./data/chinese-poetry/诗经` - 诗经
- `./data/chinese-poetry/蒙学` - 三字经、百家姓等
- 更多见 `data/chinese-poetry/` 目录

### 方式 2: 使用自定义数据目录

1. 手动从 `data/chinese-poetry/` 复制所需数据到 `data/input/`
2. 配置文件设置：
```json
{
    "input_directory": "./data/input"
}
```

---

## 示例 1: M5 PaperS3 (960×540) - 当前配置
适合：M5 PaperS3 电子书固件，合集模式

## 示例 1: M5 PaperS3 (960×540) - 当前配置
适合：M5 PaperS3 电子书固件，合集模式

```json
{
    "page_lines": 14,
    "page_columns": 13,
    "poem_length_range": {
        "min": 5,
        "max": 1000
    },
    "input_directory": "./data/chinese-poetry/全唐诗",
    "output_directory": "./data/output",
    "enable_decoration": true,
    "enable_catalog": true,
    "title_separator": "・",
    "poems_per_file": 20
}
```

## 示例 2: 小屏幕电子书 (2.9寸 e-ink)
适合：分辨率 296×128，每行约15个汉字，单诗单文件

```json
{
    "page_lines": 12,
    "page_columns": 15,
    "poem_length_range": {
        "min": 10,
        "max": 500
    },
    "input_directory": "./data/chinese-poetry/宋词",
    "output_directory": "./data/output",
    "enable_decoration": true,
    "enable_catalog": true,
    "title_separator": "・",
    "poems_per_file": 1
}
```

## 示例 3: 中等屏幕 (4.2寸 e-ink) - 推荐
适合：分辨率 400×300，每行约20个汉字

```json
{
    "page_lines": 20,
    "page_columns": 30,
    "poem_length_range": {
        "min": 5,
        "max": 1000
    },
    "input_directory": "./data/chinese-poetry/诗经",
    "output_directory": "./data/output",
    "enable_decoration": true,
    "enable_catalog": true,
    "title_separator": "・",
    "poems_per_file": 10
}
```

## 示例 4: 大屏幕 (7.5寸 e-ink)
适合：分辨率 800×480，每行约35个汉字

```json
{
    "page_lines": 30,
    "page_columns": 40,
    "poem_length_range": {
        "min": 5,
        "max": 2000
    },
    "input_directory": "./data/chinese-poetry/元曲",
    "output_directory": "./data/output",
    "enable_decoration": true,
    "enable_catalog": true,
    "title_separator": "・",
    "poems_per_file": 1
}
```

## 示例 5: 简约模式（无边框装饰）
适合：追求简洁的用户

```json
{
    "page_lines": 20,
    "page_columns": 30,
    "poem_length_range": {
        "min": 5,
        "max": 1000
    },
    "input_directory": "./data/chinese-poetry/蒙学",
    "output_directory": "./data/output",
    "enable_decoration": false,
    "enable_catalog": true,
    "title_separator": "・",
    "poems_per_file": 1
}
```

## 示例 6: 只生成短诗（绝句、五言、七言）
适合：只想看短诗

```json
{
    "page_lines": 20,
    "page_columns": 30,
    "poem_length_range": {
        "min": 10,
        "max": 100
    },
    "input_directory": "./data/input",
    "output_directory": "./data/output",
    "enable_decoration": true,
    "enable_catalog": true,
    "title_separator": "・",
    "poems_per_file": 1
}
```
注意：此配置需要手动从 `data/chinese-poetry/` 复制数据到 `data/input/`

## 参数说明

### page_lines (每页行数)
- 建议范围：10-40
- 过小会导致频繁翻页
- 过大可能超出屏幕显示范围

### page_columns (每行字符数)
- 建议范围：20-50
- 注意：中文字符通常占2个显示宽度
- 实际显示宽度 ≈ page_columns / 2 个汉字

### poem_length_range (诗词长度范围)
- min: 最小字符数，过滤掉过短的内容
- max: 最大字符数，过滤掉过长的内容
- 绝句约20-40字
- 律诗约50-70字
- 词约50-200字
- 长诗可达1000字以上

### enable_decoration (启用装饰)
- true: 显示边框、分隔线
- false: 纯文本输出

### enable_catalog (启用目录)
- true: 生成总目录文件
- false: 不生成总目录
