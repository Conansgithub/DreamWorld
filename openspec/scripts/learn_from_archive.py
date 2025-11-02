"""
从归档的变更中提取系统级洞察，更新 CLAUDE.md
"""
from pathlib import Path
import yaml

def learn_from_archive(change_id: str):
    """分析完整的变更，提取系统级知识"""
    
    archive_dir = Path(f".openspec/archive/{change_id}")
    
    # 1. 收集变更的所有信息
    context = {
        "change_id": change_id,
        "proposal": (archive_dir / "proposal.md").read_text(),
        "specs_changes": collect_spec_changes(archive_dir / "specs"),
        "decisions": collect_related_decisions(change_id),
        "errors": collect_related_errors(change_id),
        "patterns": collect_related_patterns(change_id)
    }
    
    # 2. ACE 学习：生成系统级洞察
    from ace_integration import learn_system_knowledge
    system_insight = learn_system_knowledge(context)
    
    # 3. 保存到 system-knowledge/
    insight_file = Path(f".openspec/knowledge/system-knowledge/{change_id}.md")
    insight_file.parent.mkdir(parents=True, exist_ok=True)
    insight_file.write_text(system_insight)
    
    # 4. 提取高价值见解到 CLAUDE.md
    high_value_insights = extract_high_value_insights(system_insight)
    update_claude_md(high_value_insights)
    
    # 5. 更新 Playbook
    update_playbook_from_insights(system_insight)
    
    print(f"✅ 自动学习：从 {change_id} 提取了系统级洞察并更新了 CLAUDE.md")

def collect_spec_changes(specs_dir: Path) -> dict:
    """收集 spec 的变更"""
    changes = {"added": [], "modified": [], "removed": []}
    
    for spec_file in specs_dir.rglob("spec.md"):
        content = spec_file.read_text()
        
        # 解析 ADDED/MODIFIED/REMOVED 标记
        for line in content.split('\n'):
            if '**Status**: ADDED' in line:
                changes["added"].append(extract_component_name(line))
            elif '**Status**: MODIFIED' in line:
                changes["modified"].append(extract_component_name(line))
            # REMOVED 通常在 proposal 中标记
    
    return changes

def collect_related_decisions(change_id: str) -> list[dict]:
    """收集与此变更相关的所有决策"""
    decisions = []
    decisions_dir = Path(".openspec/knowledge/decisions")
    
    for decision_file in decisions_dir.glob(f"*{change_id}*.md"):
        content = decision_file.read_text()
        metadata = extract_yaml_frontmatter(content)
        decisions.append({
            "file": decision_file.name,
            "metadata": metadata,
            "content": content
        })
    
    return decisions

def update_claude_md(insights: list[str]):
    """更新 CLAUDE.md，保持最重要的 20 条见解"""
    claude_md = Path(".openspec/knowledge/CLAUDE.md")
    current_content = claude_md.read_text() if claude_md.exists() else ""
    
    # 解析现有见解
    existing_insights = parse_claude_md_insights(current_content)
    
    # 合并新见解
    all_insights = existing_insights + insights
    
    # 按重要性排序（基于 helpful 计数）
    all_insights.sort(key=lambda x: x['helpful'], reverse=True)
    
    # 保留前 20 条
    top_insights = all_insights[:20]
    
    # 重新生成 CLAUDE.md
    new_content = generate_claude_md(top_insights)
    claude_md.write_text(new_content)

def generate_claude_md(insights: list[dict]) -> str:
    """生成 CLAUDE.md 内容"""
    sections = {
        "架构理解": [],
        "关键决策": [],
        "常见陷阱": [],
        "最佳实践": []
    }
    
    # 将见解分类到不同 section
    for insight in insights:
        category = insight['category']
        sections[category].append(insight)
    
    # 生成 markdown
    content = """# 项目全局上下文

本文档自动维护项目最重要的 20 条见解。
Claude Code 将始终加载此文件。

"""
    
    for section, items in sections.items():
        if items:
            content += f"\n## {section}\n\n"
            for item in items:
                content += f"### {item['title']}\n"
                content += f"{item['summary']}\n"
                content += f"*来源: {item['source']} | 有用次数: {item['helpful']}*\n\n"
    
    return content

def extract_component_name(line: str) -> str:
    """从标记行提取组件名"""
    pass

def extract_yaml_frontmatter(content: str) -> dict:
    """解析 YAML frontmatter"""
    import yaml
    # 实现解析逻辑
    pass

def collect_related_errors(change_id: str) -> list[dict]:
    """收集相关错误"""
    pass

def collect_related_patterns(change_id: str) -> list[dict]:
    """收集相关模式"""
    pass

def extract_high_value_insights(system_insight: str) -> list[dict]:
    """从系统洞察中提取高价值见解"""
    pass

def parse_claude_md_insights(content: str) -> list[dict]:
    """解析 CLAUDE.md 中的现有见解"""
    pass

def update_playbook_from_insights(system_insight: str):
    """从洞察更新 Playbook"""
    pass