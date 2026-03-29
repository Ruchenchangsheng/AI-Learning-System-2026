#!/usr/bin/env python3
"""
AI学习管理系统 - JSON转Excel工具
功能：将学习计划、每日任务等JSON文件转换为Excel表格
"""

import json
import pandas as pd
import os
from datetime import datetime
from pathlib import Path

class LearningJsonToExcel:
    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        self.config_path = self.base_path / "config"
        self.output_path = self.base_path / "excel_reports"
        
        # 创建输出目录
        self.output_path.mkdir(exist_ok=True)
    
    def convert_learning_plan_to_excel(self):
        """将学习计划JSON转换为Excel"""
        input_file = self.config_path / "learning_plan.json"
        output_file = self.output_path / "学习计划总览.xlsx"
        
        if not input_file.exists():
            print(f"❌ 学习计划文件不存在: {input_file}")
            return False
        
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 创建Excel写入器
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                # 1. 总体目标表
                if 'overall_goal' in data:
                    overall_df = pd.DataFrame([data['overall_goal']])
                    overall_df.to_excel(writer, sheet_name='总体目标', index=False)
                
                # 2. 学习阶段表
                if 'learning_phases' in data:
                    phases_data = []
                    for phase in data['learning_phases']:
                        phase_info = {
                            '阶段名称': phase.get('name', ''),
                            '时间范围': phase.get('time_range', ''),
                            '持续时间': phase.get('duration', ''),
                            '主要目标': phase.get('main_goals', ''),
                            '关键成果': phase.get('key_outcomes', ''),
                            '优先级': phase.get('priority', '')
                        }
                        phases_data.append(phase_info)
                    
                    phases_df = pd.DataFrame(phases_data)
                    phases_df.to_excel(writer, sheet_name='学习阶段', index=False)
                
                # 3. 每日安排表
                if 'daily_schedule' in data:
                    schedule_data = []
                    for time_slot in data['daily_schedule']:
                        slot_info = {
                            '时间段': time_slot.get('time', ''),
                            '活动': time_slot.get('activity', ''),
                            '时长': time_slot.get('duration', ''),
                            '地点': time_slot.get('location', ''),
                            '工具': time_slot.get('tools', '')
                        }
                        schedule_data.append(slot_info)
                    
                    schedule_df = pd.DataFrame(schedule_data)
                    schedule_df.to_excel(writer, sheet_name='每日安排', index=False)
                
                # 4. 里程碑表
                if 'milestones' in data:
                    milestones_data = []
                    for milestone in data['milestones']:
                        milestone_info = {
                            '里程碑': milestone.get('name', ''),
                            '目标日期': milestone.get('target_date', ''),
                            '完成标准': milestone.get('completion_criteria', ''),
                            '重要性': milestone.get('importance', ''),
                            '状态': milestone.get('status', '未开始')
                        }
                        milestones_data.append(milestone_info)
                    
                    milestones_df = pd.DataFrame(milestones_data)
                    milestones_df.to_excel(writer, sheet_name='里程碑', index=False)
                
                # 5. 资源列表
                if 'resources' in data:
                    resources_data = []
                    for resource in data['resources']:
                        resource_info = {
                            '资源类型': resource.get('type', ''),
                            '名称': resource.get('name', ''),
                            '链接': resource.get('url', ''),
                            '描述': resource.get('description', ''),
                            '推荐程度': resource.get('recommendation_level', '')
                        }
                        resources_data.append(resource_info)
                    
                    resources_df = pd.DataFrame(resources_data)
                    resources_df.to_excel(writer, sheet_name='学习资源', index=False)
            
            print(f"✅ 学习计划已转换为Excel: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ 转换失败: {e}")
            return False
    
    def convert_daily_checklist_to_excel(self):
        """将每日任务模板JSON转换为Excel"""
        input_file = self.config_path / "daily_checklist.json"
        output_file = self.output_path / "每日任务模板.xlsx"
        
        if not input_file.exists():
            print(f"❌ 每日任务文件不存在: {input_file}")
            return False
        
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                # 1. 每日模板表
                if 'daily_template' in data:
                    template_data = []
                    template = data['daily_template']
                    
                    # 基本信息
                    base_info = {
                        '项目': '基本信息',
                        '值': json.dumps({
                            '日期': template.get('date', ''),
                            '星期': template.get('day_of_week', ''),
                            '阶段': template.get('phase', ''),
                            '周数': template.get('week_number', 0),
                            '天数': template.get('day_number', 0)
                        }, ensure_ascii=False)
                    }
                    template_data.append(base_info)
                    
                    # 上午任务
                    morning = template.get('morning_session', {})
                    morning_info = {
                        '项目': '上午任务',
                        '值': json.dumps({
                            '时间': morning.get('time', ''),
                            '任务': morning.get('tasks', []),
                            '完成': morning.get('completed', False),
                            '备注': morning.get('notes', '')
                        }, ensure_ascii=False)
                    }
                    template_data.append(morning_info)
                    
                    # 下午任务
                    afternoon = template.get('afternoon_session', {})
                    afternoon_info = {
                        '项目': '下午任务',
                        '值': json.dumps({
                            '时间': afternoon.get('time', ''),
                            '任务': afternoon.get('tasks', []),
                            '完成': afternoon.get('completed', False),
                            '备注': afternoon.get('notes', '')
                        }, ensure_ascii=False)
                    }
                    template_data.append(afternoon_info)
                    
                    # 晚上任务
                    evening = template.get('evening_session', {})
                    evening_info = {
                        '项目': '晚上任务',
                        '值': json.dumps({
                            '时间': evening.get('time', ''),
                            '任务': evening.get('tasks', []),
                            '完成': evening.get('completed', False),
                            '备注': evening.get('notes', '')
                        }, ensure_ascii=False)
                    }
                    template_data.append(evening_info)
                    
                    template_df = pd.DataFrame(template_data)
                    template_df.to_excel(writer, sheet_name='每日模板', index=False)
                
                # 2. 第1阶段任务表
                if 'phase1_tasks' in data:
                    tasks_data = []
                    phase1 = data['phase1_tasks']
                    
                    for week_num, week_data in phase1.items():
                        for day_key, day_data in week_data.items():
                            task_info = {
                                '周': week_num,
                                '天': day_key,
                                '日期': day_data.get('date', ''),
                                '重点': day_data.get('focus', ''),
                                '上午任务': '\n'.join(day_data.get('morning_tasks', [])),
                                '下午任务': '\n'.join(day_data.get('afternoon_tasks', [])),
                                '晚上任务': '\n'.join(day_data.get('evening_tasks', []))
                            }
                            tasks_data.append(task_info)
                    
                    tasks_df = pd.DataFrame(tasks_data)
                    tasks_df.to_excel(writer, sheet_name='第1阶段任务', index=False)
                
                # 3. 检查清单类别表
                if 'checklist_categories' in data:
                    categories_data = []
                    categories = data['checklist_categories']
                    
                    for category_name, items in categories.items():
                        for i, item in enumerate(items, 1):
                            category_info = {
                                '类别': category_name,
                                '序号': i,
                                '检查项': item
                            }
                            categories_data.append(category_info)
                    
                    categories_df = pd.DataFrame(categories_data)
                    categories_df.to_excel(writer, sheet_name='检查清单', index=False)
                
                # 4. 完成指标表
                if 'completion_metrics' in data:
                    metrics_data = []
                    metrics = data['completion_metrics']
                    
                    for metric_name, levels in metrics.items():
                        for level_name, description in levels.items():
                            metric_info = {
                                '指标类型': metric_name,
                                '等级': level_name,
                                '描述': description
                            }
                            metrics_data.append(metric_info)
                    
                    metrics_df = pd.DataFrame(metrics_data)
                    metrics_df.to_excel(writer, sheet_name='完成指标', index=False)
                
                # 5. 每日问题表
                if 'daily_questions' in data:
                    questions_data = []
                    questions = data['daily_questions']
                    
                    for time_period, q_list in questions.items():
                        for i, question in enumerate(q_list, 1):
                            question_info = {
                                '时间段': time_period,
                                '序号': i,
                                '问题': question
                            }
                            questions_data.append(question_info)
                    
                    questions_df = pd.DataFrame(questions_data)
                    questions_df.to_excel(writer, sheet_name='每日问题', index=False)
            
            print(f"✅ 每日任务模板已转换为Excel: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ 转换失败: {e}")
            return False
    
    def convert_learning_stats_to_excel(self):
        """将学习统计JSON转换为Excel"""
        input_file = self.base_path / "progress" / "learning_stats.json"
        output_file = self.output_path / "学习统计.xlsx"
        
        if not input_file.exists():
            print(f"❌ 学习统计文件不存在: {input_file}")
            return False
        
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                # 1. 当前进度表
                if 'current_progress' in data:
                    progress_data = []
                    progress = data['current_progress']
                    
                    for key, value in progress.items():
                        progress_data.append({
                            '指标': key,
                            '值': str(value)
                        })
                    
                    progress_df = pd.DataFrame(progress_data)
                    progress_df.to_excel(writer, sheet_name='当前进度', index=False)
                
                # 2. 学习统计表
                if 'learning_statistics' in data:
                    stats_data = []
                    stats = data['learning_statistics']
                    
                    for key, value in stats.items():
                        stats_data.append({
                            '统计项': key,
                            '数值': value
                        })
                    
                    stats_df = pd.DataFrame(stats_data)
                    stats_df.to_excel(writer, sheet_name='学习统计', index=False)
                
                # 3. 知识掌握表
                if 'knowledge_mastery' in data:
                    knowledge_data = []
                    knowledge = data['knowledge_mastery']
                    
                    for subject, info in knowledge.items():
                        knowledge_data.append({
                            '学科': subject,
                            '掌握程度': info.get('level', 0),
                            '已学主题': ', '.join(info.get('topics_covered', [])),
                            '最后练习': info.get('last_practiced', '')
                        })
                    
                    knowledge_df = pd.DataFrame(knowledge_data)
                    knowledge_df.to_excel(writer, sheet_name='知识掌握', index=False)
                
                # 4. 性能指标表
                if 'performance_metrics' in data:
                    performance_data = []
                    metrics = data['performance_metrics']
                    
                    for key, value in metrics.items():
                        performance_data.append({
                            '指标': key,
                            '得分': value
                        })
                    
                    performance_df = pd.DataFrame(performance_data)
                    performance_df.to_excel(writer, sheet_name='性能指标', index=False)
                
                # 5. 下一个里程碑表
                if 'next_milestones' in data:
                    milestones_data = []
                    milestones = data['next_milestones']
                    
                    for milestone in milestones:
                        milestones_data.append({
                            '里程碑': milestone.get('milestone', ''),
                            '目标日期': milestone.get('target_date', ''),
                            '优先级': milestone.get('priority', ''),
                            '状态': '待完成'
                        })
                    
                    milestones_df = pd.DataFrame(milestones_data)
                    milestones_df.to_excel(writer, sheet_name='下一个里程碑', index=False)
            
            print(f"✅ 学习统计已转换为Excel: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ 转换失败: {e}")
            return False
    
    def create_daily_excel_report(self, date=None):
        """创建每日Excel报告"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        input_file = self.base_path / "progress" / "daily_logs" / f"{date}.md"
        output_file = self.output_path / f"每日报告_{date}.xlsx"
        
        if not input_file.exists():
            print(f"❌ 每日日志文件不存在: {input_file}")
            return False
        
        try:
            # 读取Markdown文件
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析Markdown表格（简化版）
            # 这里可以添加更复杂的Markdown解析逻辑
            
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                # 创建基本信息表
                info_data = [{
                    '项目': '日期',
                    '值': date
                }, {
                    '项目': '文件路径',
                    '值': str(input_file)
                }, {
                    '项目': '生成时间',
                    '值': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }]
                
                info_df = pd.DataFrame(info_data)
                info_df.to_excel(writer, sheet_name='基本信息', index=False)
                
                # 创建内容预览表
                preview_data = [{
                    '类型': '原始内容',
                    '内容': content[:1000] + '...' if len(content) > 1000 else content
                }]
                
                preview_df = pd.DataFrame(preview_data)
                preview_df.to_excel(writer, sheet_name='内容预览', index=False)
            
            print(f"✅ 每日报告已创建: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ 创建报告失败: {e}")
            return False
    
    def convert_all_to_excel(self):
        """转换所有JSON文件为Excel"""
        print("=" * 50)
        print("📊 AI学习管理系统 - JSON转Excel工具")
        print("=" * 50)
        
        results = []
        
        # 1. 转换学习计划
        print("\n1. 🔄 转换学习计划...")
        result1 = self.convert_learning_plan_to_excel()
        results.append(("学习计划", result1))
        
        # 2. 转换每日任务模板
        print("\n2. 🔄 转换每日任务模板...")
        result2 = self.convert_daily_checklist_to_excel()
        results.append(("每日任务模板", result2))
        
        # 3. 转换学习统计
        print("\n3. 🔄 转换学习统计...")
        result3 = self.convert_learning_stats_to_excel()
        results.append(("学习统计", result3))
        
        # 4. 创建今日报告
        print("\n4. 🔄 创建今日报告...")
        result4 = self.create_daily_excel_report()
        results.append(("今日报告", result4))
        
        # 输出结果汇总
        print("\n" + "=" * 50)
        print("📈 转换结果汇总")
        print("=" * 50)
        
        success_count = 0
        for name, success in results:
            status = "✅ 成功" if success else "❌ 失败"
            print(f"{name}: {status}")
            if success:
                success_count += 1
        
        print(f"\n🎯 完成度: {success_count}/{len(results)}")
        
        if success_count > 0:
            print(f"\n📁 Excel文件保存在: {self.output_path}")
            print("📋 生成的文件:")
            for file in self.output_path.glob("*.xlsx"):
                print(f"  - {file.name}")
        
        return success_count == len(results)

def main():
    """主函数"""
    import sys
    
    # 检查是否在正确目录
    if not Path("config").exists():
        print("❌ 请在AI学习管理系统根目录运行此脚本")
        print("   或指定正确的路径: python json_to_excel.py /path/to/system")
        sys.exit(1)
    
    # 创建转换器实例
    converter = LearningJsonToExcel()
    
    # 执行转换
    success = converter.convert_all_to_excel()
    
    if success:
        print("\n🎉 所有JSON文件已成功转换为Excel！")
        print("📊 现在可以用Excel查看和管理学习数据了！")
    else:
        print("\n⚠️ 部分文件转换失败，请检查错误信息")
    
    # 提供使用建议
    print("\n" + "=" * 50)
    print("💡 使用建议")
    print("=" * 50)
    print("1. 每日运行: python scripts/json_to_excel.py")
    print("2. 查看Excel: 打开 excel_reports/ 目录中的文件")
    print("3. 自定义: 修改脚本以适应特定需求")
    print("4. 自动化: 添加到每日更新脚本中")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())

