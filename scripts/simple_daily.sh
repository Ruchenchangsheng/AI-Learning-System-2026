#!/bin/bash
# AI学习管理系统 - 简易每日脚本
# 爸爸每天运行这个脚本即可完成所有操作

echo "🤖 AI学习管理系统 - 每日助手"
echo "=============================="

# 获取今日日期
TODAY=$(date '+%Y-%m-%d')
echo "📅 今天是: $TODAY"

# 1. 拉取最新更新
echo ""
echo "1. 🔄 拉取GitHub最新更新..."
git pull origin main
if [ $? -eq 0 ]; then
    echo "   ✅ 拉取成功"
else
    echo "   ⚠️ 拉取失败，请检查网络或Git配置"
fi

# 2. 显示今日学习计划
echo ""
echo "2. 📋 今日学习计划:"
if [ -f "progress/daily_logs/$TODAY.md" ]; then
    echo "   ✅ 今日日志存在: progress/daily_logs/$TODAY.md"
    echo ""
    echo "   今日任务摘要:"
    grep -A5 "## 📅 今日计划表" "progress/daily_logs/$TODAY.md" | head -10
else
    echo "   ⚠️ 今日日志不存在，请创建或联系小爪"
fi

# 3. 显示学习统计
echo ""
echo "3. 📊 学习统计:"
if [ -f "progress/learning_stats.json" ]; then
    CURRENT_DAY=$(grep -o '"current_day": [0-9]*' progress/learning_stats.json | grep -o '[0-9]*')
    TOTAL_DAYS=$(grep -o '"total_days": [0-9]*' progress/learning_stats.json | grep -o '[0-9]*')
    PERCENTAGE=$(echo "scale=1; $CURRENT_DAY * 100 / $TOTAL_DAYS" | bc)
    echo "   第 $CURRENT_DAY 天 / 共 $TOTAL_DAYS 天"
    echo "   完成度: $PERCENTAGE%"
else
    echo "   ⚠️ 学习统计文件不存在"
fi

# 4. 提醒事项
echo ""
echo "4. ⏰ 今日提醒:"
echo "   08:00-12:00 - 上午学习 (Python基础)"
echo "   14:00-18:00 - 下午学习 (数据类型与控制流)"
echo "   20:00-21:00 - 晚上学习 (项目实践)"
echo "   21:00-21:30 - 模拟面试 (小爪提问)"
echo "   22:00-22:30 - 总结提交 (GitHub推送)"

# 5. 操作指南
echo ""
echo "5. 🎯 今日操作:"
echo "   📝 学习时记录进度到: progress/daily_logs/$TODAY.md"
echo "   💻 写代码练习Python基础"
echo "   ❓ 遇到问题随时QQ问小爪"
echo "   📤 晚上运行: ./scripts/daily_update.py"

# 6. 小爪的鼓励
echo ""
echo "6. 🐾 小爪的鼓励:"
echo "   今天是第 $CURRENT_DAY 天，坚持就是胜利！"
echo "   记住：完成比完美重要，先写出能运行的程序！"
echo "   小爪会全程陪伴，随时为你提供支持！"

echo ""
echo "=============================="
echo "🚀 现在开始今天的学习吧！"
echo "💪 加油，爸爸！"