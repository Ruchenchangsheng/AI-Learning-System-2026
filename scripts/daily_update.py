#!/usr/bin/env python3
"""
AI学习管理系统 - 每日更新脚本
功能：更新学习进度、生成报告、同步GitHub
"""

import json
import os
import sys
from datetime import datetime, timedelta
import subprocess
from pathlib import Path

class LearningSystemUpdater:
    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        self.config_path = self.base_path / "config"
        self.progress_path = self.base_path / "progress"
        self.scripts_path = self.base_path / "scripts"
        
        # 加载配置
        self.load_configs()
        
    def load_configs(self):
        """加载配置文件"""
        try:
            with open(self.config_path / "learning_plan.json", "r", encoding="utf-8") as f:
                self.learning_plan = json.load(f)
            
            with open(self.config_path / "daily_checklist.json", "r", encoding="utf-8") as f:
                self.checklist = json.load(f)
                
        except FileNotFoundError as e:
            print(f"配置文件未找到: {e}")
            sys.exit(1)
    
    def get_today_info(self):
        """获取今日信息"""
        today = datetime.now()
        return {
            "date": today.strftime("%Y-%m-%d"),
            "day_of_week": today.strftime("%A"),
            "week_number": today.isocalendar()[1],
            "day_number": (today - datetime(2026, 3, 29)).days + 1
        }
    
    def create_daily_log(self):
        """创建或更新今日日志"""
        today_info = self.get_today_info()
        log_file = self.progress_path / "daily_logs" / f"{today_info['date']}.md"
        
        # 如果日志文件已存在，读取现有内容
        if log_file.exists():
            print(f"今日日志已存在: {log_file}")
            with open(log_file, "r", encoding="utf-8") as f:
                content = f.read()
            return content
        else:
            # 创建新日志文件
            print(f"创建今日日志: {log_file}")
            return self.generate_daily_log(today_info, log_file)
    
    def generate_daily_log(self, today_info, log_file):
        """生成每日日志内容"""
        # 这里可以调用模板生成日志
        # 简化版：复制模板文件
        template_file = self.progress_path / "daily_logs" / "template.md"
        
        if template_file.exists():
            with open(template_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 替换模板变量
            content = content.replace("{date}", today_info["date"])
            content = content.replace("{day_number}", str(today_info["day_number"]))
            content = content.replace("{day_of_week}", today_info["day_of_week"])
            
            # 保存文件
            with open(log_file, "w", encoding="utf-8") as f:
                f.write(content)
            
            return content
        else:
            # 创建简单日志
            content = f"""# {today_info['date']} 学习日志
            
## 今日计划
- [ ] 学习Python基础
            
## 学习内容
            
## 完成情况
            
## 明日计划"""
            
            with open(log_file, "w", encoding="utf-8") as f:
                f.write(content)
            
            return content
    
    def update_progress_stats(self):
        """更新学习统计"""
        stats_file = self.progress_path / "learning_stats.json"
        
        if stats_file.exists():
            with open(stats_file, "r", encoding="utf-8") as f:
                stats = json.load(f)
        else:
            stats = {
                "total_days": 0,
                "completed_days": 0,
                "total_study_hours": 0,
                "average_daily_hours": 0,
                "projects_completed": 0,
                "last_updated": ""
            }
        
        # 更新统计
        today_info = self.get_today_info()
        stats["total_days"] = today_info["day_number"]
        stats["last_updated"] = today_info["date"]
        
        # 保存更新
        with open(stats_file, "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        
        return stats
    
    def sync_with_github(self, commit_message=None):
        """同步到GitHub"""
        if commit_message is None:
            today_info = self.get_today_info()
            commit_message = f"每日更新: {today_info['date']} - 第{today_info['day_number']}天"
        
        try:
            # 切换到仓库目录
            original_dir = os.getcwd()
            os.chdir(self.base_path)
            
            # Git操作
            commands = [
                ["git", "add", "."],
                ["git", "commit", "-m", commit_message],
                ["git", "push", "origin", "main"]
            ]
            
            for cmd in commands:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"Git命令失败: {' '.join(cmd)}")
                    print(f"错误: {result.stderr}")
                    return False
            
            print("✅ GitHub同步成功")
            return True
            
        except Exception as e:
            print(f"GitHub同步失败: {e}")
            return False
            
        finally:
            os.chdir(original_dir)
    
    def generate_daily_report(self):
        """生成每日报告"""
        today_info = self.get_today_info()
        report = {
            "date": today_info["date"],
            "day_number": today_info["day_number"],
            "system_status": "运行正常",
            "tasks_for_today": self.get_todays_tasks(),
            "reminders": self.get_daily_reminders(),
            "progress_summary": self.get_progress_summary()
        }
        
        # 保存报告
        report_file = self.progress_path / "daily_reports" / f"{today_info['date']}.json"
        report_file.parent.mkdir(exist_ok=True)
        
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return report
    
    def get_todays_tasks(self):
        """获取今日任务"""
        # 根据学习计划生成今日任务
        # 简化版：返回固定任务
        return [
            "Python基础学习",
            "完成练习题",
            "更新学习日志",
            "GitHub同步"
        ]
    
    def get_daily_reminders(self):
        """获取每日提醒"""
        return [
            "08:00 - 开始学习",
            "12:00 - 午休",
            "14:00 - 下午学习",
            "20:00 - 晚上学习",
            "22:00 - 总结与提交"
        ]
    
    def get_progress_summary(self):
        """获取进度摘要"""
        today_info = self.get_today_info()
        return {
            "days_completed": today_info["day_number"] - 1,
            "days_remaining": 93 - today_info["day_number"],
            "completion_percentage": round((today_info["day_number"] / 93) * 100, 1),
            "current_phase": "第1阶段 - 基础速成",
            "next_milestone": "完成Python基础"
        }
    
    def run_daily_update(self):
        """执行每日更新"""
        print("=" * 50)
        print("🤖 AI学习管理系统 - 每日更新")
        print("=" * 50)
        
        # 1. 获取今日信息
        today_info = self.get_today_info()
        print(f"📅 日期: {today_info['date']} (第{today_info['day_number']}天)")
        
        # 2. 更新日志
        print("\n📝 更新学习日志...")
        log_content = self.create_daily_log()
        print("✅ 日志更新完成")
        
        # 3. 更新统计
        print("\n📊 更新学习统计...")
        stats = self.update_progress_stats()
        print(f"✅ 统计更新完成: 第{stats['total_days']}天")
        
        # 4. 生成报告
        print("\n📋 生成每日报告...")
        report = self.generate_daily_report()
        print("✅ 报告生成完成")
        
        # 5. GitHub同步
        print("\n🌐 同步到GitHub...")
        sync_success = self.sync_with_github()
        
        if sync_success:
            print("🎉 每日更新完成！")
        else:
            print("⚠️ 更新完成，但GitHub同步失败")
        
        return {
            "success": sync_success,
            "date": today_info["date"],
            "day_number": today_info["day_number"],
            "log_updated": True,
            "stats_updated": True,
            "report_generated": True,
            "github_synced": sync_success
        }

def main():
    """主函数"""
    # 检查是否在正确目录
    if not Path("config").exists():
        print("❌ 请在AI学习管理系统根目录运行此脚本")
        print("   或指定正确的路径: python daily_update.py /path/to/system")
        sys.exit(1)
    
    # 创建更新器实例
    updater = LearningSystemUpdater()
    
    # 执行更新
    result = updater.run_daily_update()
    
    # 输出结果
    print("\n" + "=" * 50)
    print("📈 更新结果摘要")
    print("=" * 50)
    for key, value in result.items():
        if key != "success":
            print(f"{key}: {value}")
    
    if result["success"]:
        print("\n🎯 今日任务完成！继续加油！")
    else:
        print("\n⚠️ 部分任务失败，请检查错误信息")

if __name__ == "__main__":
    main()