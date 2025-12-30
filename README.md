# MinerU Parser

基于 Claude Agent SDK 和 MinerU Skill 的 PDF 文档解析工具，支持将 PDF 文档解析为 Markdown 格式。

## ⚠️ 重要说明

**本项目仅支持在线版本**，需要通过 URL 访问 PDF 文档，不支持本地文件上传。

## 📋 前置要求

- Python 3.7+
- `MINERU_API_KEY` 环境变量（必需）

## 🔑 配置 API 密钥

在使用本项目之前，必须先配置 MinerU API 密钥：

```bash
export MINERU_API_KEY='your_api_key_here'
```

### 获取 API 密钥

1. 访问 [MinerU 官网](https://mineru.net) 并注册/登录
2. 进入账户设置或 API 部分
3. 生成或复制您的 API 密钥

### 验证配置

运行以下命令验证 API 密钥是否已正确设置：

```bash
echo $MINERU_API_KEY
```

如果输出为空，请重新设置环境变量。

## 🚀 安装依赖

```bash
pip install claude-agent-sdk
```

## 💻 使用方法

### 基本使用

1. 确保已设置 `MINERU_API_KEY` 环境变量
2. 修改 `demo.py` 中的 PDF URL
3. 运行脚本：

```bash
python demo.py
```

### 命令行选项

```bash
# 运行发票解析
python demo.py

# 测试 skill 可用性
python demo.py --test

# 显示帮助信息
python demo.py --help
```

## 📝 示例

`demo.py` 展示了如何使用 MinerU Skill 解析发票 PDF：

- 提取发票基本信息（发票代码、发票号码、开票日期）
- 提取购买方和销售方信息
- 提取商品明细
- 提取税额和价税合计信息
- 提取签章信息

解析结果将保存到 `invoice_parsed/` 目录中。

## 🔧 配置说明

项目使用 Claude Agent SDK 的 Skills 功能，配置如下：

- **Skills 来源**: 从项目目录 `.claude/skills/` 加载
- **权限模式**: `bypassPermissions`（自动接受所有操作）
- **支持的工具**: Skill, view, create_file, str_replace

## 📚 功能特性

- ✅ 支持 PDF、DOC、DOCX、PPT、PPTX 和图片文件
- ✅ 提取文本、表格、公式和结构化内容
- ✅ 支持 OCR 和 VLM 模型
- ✅ 输出 Markdown 格式
- ✅ 自动保存解析结果

## ⚠️ 限制

- 仅支持通过 URL 访问的在线文档
- 不支持本地文件上传
- 最大文件大小：200MB
- 最大页数：600 页
- 每日配额：2000 页（高优先级）

## 🐛 故障排除

### 错误：未设置 MINERU_API_KEY

```
❌ 错误: 未设置 MINERU_API_KEY 环境变量
```

**解决方案**：
```bash
export MINERU_API_KEY='your_api_key'
```

### PDF URL 无法访问

确保 PDF URL 是公开可访问的，并且网络连接正常。

### Skill 不可用

运行测试命令检查：
```bash
python demo.py --test
```

确保 `.claude/skills/mineru-parser/` 目录存在且配置正确。

## 📄 许可证

请参考项目许可证文件。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

