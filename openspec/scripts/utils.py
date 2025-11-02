"""
通用工具函数
"""
import yaml
import re
from pathlib import Path
from typing import Optional, Dict, Any

def extract_yaml_frontmatter(content: str) -> Dict[str, Any]:
    """解析 YAML frontmatter"""
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(pattern, content, re.DOTALL)
    
    if match:
        yaml_content = match.group(1)
        return yaml.safe_load(yaml_content)
    return {}

def replace_yaml_frontmatter(content: str, metadata: Dict[str, Any]) -> str:
    """替换 YAML frontmatter"""
    yaml_str = yaml.dump(metadata, allow_unicode=True, default_flow_style=False)
    
    # 移除旧的 frontmatter
    pattern = r'^---\s*\n.*?\n---\s*\n'
    content_without_frontmatter = re.sub(pattern, '', content, count=1, flags=re.DOTALL)
    
    # 添加新的 frontmatter
    return f"---\n{yaml_str}---\n{content_without_frontmatter}"

def extract_section(markdown: str, heading: str) -> str:
    """提取 markdown 中特定 section 的内容"""
    lines = markdown.split('\n')
    section_lines = []
    in_section = False
    heading_level = len(heading.split()[0])  # 计算 # 数量
    
    for line in lines:
        if line.strip().startswith(heading):
            in_section = True
            continue
        elif in_section and line.startswith('#' * heading_level + ' '):
            # 遇到同级或更高级标题，停止
            break
        elif in_section:
            section_lines.append(line)
    
    return '\n'.join(section_lines).strip()

def extract_code_block(doc: str, language: str = None) -> str:
    """提取代码块"""
    if language:
        pattern = rf'```{language}\n(.*?)```'
    else:
        pattern = r'```(?:\w+)?\n(.*?)```'
    
    matches = re.findall(pattern, doc, re.DOTALL)
    return matches[0] if matches else ""

def slugify(text: str) -> str:
    """转换为 URL 友好的 slug"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text[:50]  # 限制长度

def ensure_dir(path: Path):
    """确保目录存在"""
    path.mkdir(parents=True, exist_ok=True)