# .openspec/scripts/watch_implementation.py
"""
监控实现过程，自动捕获错误和模式
"""
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import re
from pathlib import Path
from datetime import datetime
import os

class ImplementationWatcher(FileSystemEventHandler):
    def __init__(self, change_id: str):
        self.change_id = change_id
        self.recent_errors = []
    
    def on_modified(self, event):
        if event.src_path.endswith('.py') or event.src_path.endswith('.ts'):
            # 检测测试运行
            self.check_tests()
    
    def check_tests(self):
        """运行测试，捕获错误"""
        result = subprocess.run(['pytest', '-v'], capture_output=True, text=True)
        
        if result.returncode != 0:
            # 测试失败，解析错误
            error_info = self.parse_test_failure(result.stdout + result.stderr)
            
            if error_info and not self.is_duplicate_error(error_info):
                self.recent_errors.append(error_info)
                print(f"🐛 检测到错误: {error_info['summary']}")
                # 先不保存，等解决后再捕获"错误+解决方案"
    
    def on_error_resolved(self, error_info: dict):
        """错误解决后，捕获完整的"错误-解决方案"对"""
        # 获取解决问题的 commit
        solution_commit = subprocess.check_output(['git', 'log', '-1', '--format=%H']).decode().strip()
        solution_diff = subprocess.check_output(['git', 'show', solution_commit]).decode()
        
        context = {
            "change_id": self.change_id,
            "error": error_info,
            "solution_commit": solution_commit,
            "solution_diff": solution_diff
        }
        
        # ACE 学习：生成"错误-解决方案"文档
        from ace_integration import learn_error_solution
        error_doc = learn_error_solution(context)
        
        # 保存
        error_file = Path(f".openspec/knowledge/lessons/errors/{datetime.now().strftime('%Y-%m-%d')}-{error_info['slug']}.md")
        error_file.parent.mkdir(parents=True, exist_ok=True)
        error_file.write_text(error_doc)
        
        # 向量化索引
        index_to_chromadb(error_doc, collection="error_solutions")
        
        print(f"✅ 自动学习：捕获了错误解决方案 - {error_info['summary']}")

def parse_test_failure(output: str) -> dict:
    """解析测试失败信息"""
    pass

def is_duplicate_error(self, error_info: dict) -> bool:
    """检查是否重复错误"""
    pass

def index_to_chromadb(doc: str, collection: str):
    """向量化索引"""
    pass

# 启动监视器
def start_watching(change_id: str):
    event_handler = ImplementationWatcher(change_id)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    print(f"👀 开始监控 {change_id} 的实现...")