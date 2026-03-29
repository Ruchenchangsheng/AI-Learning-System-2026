# 📊 Excel工具使用指南

## 🎯 功能概述

本系统提供了完整的Excel处理能力，包括：

### 1. **JSON转Excel工具**
- 将学习计划、每日任务模板、学习统计等JSON文件转换为Excel表格
- 支持多工作表输出
- 自动格式化数据

### 2. **Excel自动化Skill**
- 安装的`automate-excel` skill提供丰富的Excel处理功能
- 支持读取、写入、合并、转换、验证Excel文件
- 批量处理和模板填充

### 3. **Python Excel库**
- 基于pandas和openpyxl的强大数据处理能力
- 支持CSV、JSON、XML等多种格式转换

## 🚀 快速开始

### 安装依赖
```bash
# 进入系统目录
cd AI-Learning-System-2026

# 安装Python依赖
pip install -r scripts/requirements.txt

# 或者使用系统已安装的skill
openclaw skills info automate-excel
```

### 转换JSON为Excel
```bash
# 运行转换脚本
python scripts/json_to_excel.py

# 输出文件在: excel_reports/ 目录
ls excel_reports/
```

### 使用Excel Skill
```bash
# 查看可用的Excel脚本
ls ~/.openclaw/workspace/skills/automate-excel/scripts/

# 运行示例脚本
python ~/.openclaw/workspace/skills/automate-excel/scripts/csv_to_excel.py --help
```

## 📋 生成的Excel文件

运行`json_to_excel.py`后会生成以下文件：

### 1. **学习计划总览.xlsx**
- 📄 **总体目标**：学习总体目标
- 📄 **学习阶段**：4个阶段详细计划
- 📄 **每日安排**：每日时间安排表
- 📄 **里程碑**：重要里程碑节点
- 📄 **学习资源**：推荐学习资源列表

### 2. **每日任务模板.xlsx**
- 📄 **每日模板**：每日学习模板结构
- 📄 **第1阶段任务**：第1阶段每日详细任务
- 📄 **检查清单**：各类检查项目
- 📄 **完成指标**：任务完成评估标准
- 📄 **每日问题**：每日自问问题

### 3. **学习统计.xlsx**
- 📄 **当前进度**：当前学习进度指标
- 📄 **学习统计**：学习数据统计
- 📄 **知识掌握**：各学科掌握程度
- 📄 **性能指标**：学习效率指标
- 📄 **下一个里程碑**：即将到来的里程碑

### 4. **每日报告_YYYY-MM-DD.xlsx**
- 📄 **基本信息**：报告基本信息
- 📄 **内容预览**：当日学习日志预览

## 🔧 高级用法

### 自定义转换
```python
# 自定义JSON转Excel
from scripts.json_to_excel import LearningJsonToExcel

converter = LearningJsonToExcel()
converter.convert_learning_plan_to_excel()  # 只转换学习计划
converter.create_daily_excel_report('2026-03-30')  # 指定日期
```

### 使用Excel Skill脚本
```bash
# CSV转Excel
python ~/.openclaw/workspace/skills/automate-excel/scripts/csv_to_excel.py \
  --input data/learning_stats.csv \
  --output excel_reports/学习统计.xlsx

# 合并多个Excel
python ~/.openclaw/workspace/skills/automate-excel/scripts/merge_sheets.py \
  --inputs excel_reports/*.xlsx \
  --output 合并报告.xlsx

# 筛选数据
python ~/.openclaw/workspace/skills/automate-excel/scripts/filter_excel.py \
  --input 学习统计.xlsx \
  --where "掌握程度>3" \
  --output 掌握良好.xlsx
```

### Python直接操作Excel
```python
import pandas as pd

# 读取Excel
df = pd.read_excel('excel_reports/学习计划总览.xlsx', sheet_name='学习阶段')

# 处理数据
filtered = df[df['优先级'] == 'high']

# 写入新Excel
filtered.to_excel('高优先级阶段.xlsx', index=False)

# 多工作表写入
with pd.ExcelWriter('综合报告.xlsx') as writer:
    df1.to_excel(writer, sheet_name='阶段计划')
    df2.to_excel(writer, sheet_name='每日任务')
```

## 📊 数据可视化

### 生成图表
```python
import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
df = pd.read_excel('excel_reports/学习统计.xlsx', sheet_name='知识掌握')

# 创建图表
plt.figure(figsize=(10, 6))
plt.bar(df['学科'], df['掌握程度'])
plt.title('知识掌握程度')
plt.xlabel('学科')
plt.ylabel('掌握程度')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('知识掌握图表.png')
plt.show()
```

### 数据透视表
```python
# 创建数据透视表
pivot = df.pivot_table(
    index='学科',
    values='掌握程度',
    aggfunc='mean'
)

# 保存为Excel
pivot.to_excel('知识掌握透视表.xlsx')
```

## 🔄 自动化工作流

### 每日自动转换
```bash
#!/bin/bash
# daily_excel_convert.sh

cd /path/to/AI-Learning-System-2026

# 拉取最新数据
git pull origin main

# 转换JSON为Excel
python scripts/json_to_excel.py

# 提交生成的Excel文件
git add excel_reports/
git commit -m "自动生成Excel报告 $(date '+%Y-%m-%d')"
git push origin main
```

### 添加到cron定时任务
```bash
# 每天22:30自动运行
30 22 * * * cd /path/to/AI-Learning-System-2026 && ./daily_excel_convert.sh
```

## 🛠️ 故障排除

### 常见问题

**Q: 运行脚本时提示缺少依赖**
```bash
# 安装缺失的包
pip install pandas openpyxl xlrd xlsxwriter
```

**Q: Excel文件打不开或格式错误**
```bash
# 检查文件完整性
file excel_reports/学习计划总览.xlsx

# 重新生成
rm excel_reports/*.xlsx
python scripts/json_to_excel.py
```

**Q: 中文显示乱码**
```python
# 在脚本中指定编码
df.to_excel('output.xlsx', index=False, encoding='utf-8-sig')
```

**Q: 文件太大处理慢**
```python
# 使用分块读取
chunk_size = 10000
for chunk in pd.read_excel('large_file.xlsx', chunksize=chunk_size):
    process_chunk(chunk)
```

### 调试模式
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# 现在可以看到详细的调试信息
converter = LearningJsonToExcel()
converter.convert_all_to_excel()
```

## 📈 最佳实践

### 1. **定期备份Excel文件**
```bash
# 备份到其他位置
cp excel_reports/*.xlsx ~/backups/learning_excel/
```

### 2. **版本控制Excel文件**
```bash
# 将Excel文件加入Git版本控制
git add excel_reports/*.xlsx
git commit -m "更新Excel报告"
```

### 3. **使用模板系统**
```python
# 创建自定义模板
from openpyxl import load_workbook

template = load_workbook('template.xlsx')
ws = template.active
ws['A1'] = '学习报告'
ws['A2'] = f'生成时间: {datetime.now()}'
template.save('filled_report.xlsx')
```

### 4. **数据验证**
```python
# 验证数据完整性
def validate_excel(file_path):
    df = pd.read_excel(file_path)
    
    # 检查必需列
    required_columns = ['日期', '任务', '完成度']
    missing = [col for col in required_columns if col not in df.columns]
    
    if missing:
        print(f"❌ 缺少必需列: {missing}")
        return False
    
    # 检查数据范围
    if '完成度' in df.columns:
        invalid = df[(df['完成度'] < 0) | (df['完成度'] > 100)]
        if not invalid.empty:
            print(f"⚠️ 完成度数据异常: {len(invalid)} 行")
    
    return True
```

## 🎯 使用场景

### 场景1：每日学习报告
```bash
# 每天早上查看昨日学习情况
python scripts/json_to_excel.py
open excel_reports/每日报告_$(date -d "yesterday" '+%Y-%m-%d').xlsx
```

### 场景2：周度总结
```bash
# 生成本周学习统计
python ~/.openclaw/workspace/skills/automate-excel/scripts/merge_sheets.py \
  --inputs excel_reports/每日报告_*.xlsx \
  --output 本周学习总结.xlsx
```

### 场景3：知识掌握分析
```python
# 分析知识掌握趋势
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel('excel_reports/学习统计.xlsx', sheet_name='知识掌握')

# 绘制趋势图
plt.plot(df['学科'], df['掌握程度'], marker='o')
plt.title('知识掌握趋势')
plt.savefig('知识趋势.png')
```

### 场景4：学习计划调整
```python
# 根据进度调整学习计划
df = pd.read_excel('excel_reports/学习计划总览.xlsx', sheet_name='学习阶段')

# 标记已完成阶段
df['状态'] = ['进行中', '未开始', '未开始', '未开始']
df.to_excel('更新后的学习计划.xlsx', index=False)
```

## 📞 技术支持

### 遇到问题？
1. **检查日志**：查看脚本输出的错误信息
2. **验证数据**：确保JSON文件格式正确
3. **更新依赖**：`pip install --upgrade -r scripts/requirements.txt`
4. **联系小爪**：QQ描述具体问题

### 功能建议
想要更多Excel功能？告诉小爪：
- 特定的数据可视化需求
- 自动化报表生成
- 数据导入导出优化
- 其他Excel相关功能

## 🐾 小爪的提醒

### 使用建议：
1. **定期运行**：每天运行一次`json_to_excel.py`
2. **版本控制**：将Excel文件提交到GitHub
3. **数据备份**：重要Excel文件多位置备份
4. **逐步优化**：先使用基础功能，再添加高级特性

### 安全注意：
- 🔒 不要公开分享包含个人信息的Excel文件
- 🔒 定期更新依赖包以确保安全
- 🔒 验证外部输入的Excel文件

**现在就开始使用Excel工具吧！让数据管理更直观、更高效！** 🐾