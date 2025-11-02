"""
从 proposal 中自动提取技术决策
"""
import yaml
from pathlib import Path
from datetime import datetime
from ace_integration import learn_decision

def extract_decision_from_proposal(change_dir: Path):
    """从 proposal 和 design 文件中提取技术决策"""
    
    proposal = (change_dir / "proposal.md").read_text()
    design = (change_dir / "design.md").read_text() if (change_dir / "design.md").exists() else ""
    
    # 解析 proposal 的 Why 部分
    why_section = extract_section(proposal, "## Why")
    
    # 解析 design 的 Alternatives / Decision 部分
    alternatives = extract_section(design, "## Alternatives Considered")
    decision_rationale = extract_section(design, "## Decision Rationale")
    
    # 如果有足够的决策信息，触发学习
    if decision_rationale or alternatives:
        context = {
            "change_id": change_dir.name,
            "why": why_section,
            "alternatives": alternatives,
            "decision": decision_rationale,
            "affected_specs": list_affected_specs(change_dir / "specs")
        }
        
        # ACE 学习：生成结构化的决策记录
        decision_doc = learn_decision(context)
        
        # 存储到 knowledge/decisions/
        decision_file = Path(f".openspec/knowledge/decisions/{datetime.now().strftime('%Y-%m-%d')}-{change_dir.name}.md")
        decision_file.write_text(decision_doc)
        
        # 向量化并索引到 ChromaDB
        index_to_chromadb(decision_doc, collection="decisions")
        
        print(f"✅ 自动学习：从 {change_dir.name} 提取了技术决策")
    else:
        print(f"ℹ️  {change_dir.name} 没有足够的决策信息，跳过学习")

def extract_section(markdown: str, heading: str) -> str:
    """提取 markdown 中特定 section 的内容"""
    lines = markdown.split('\n')
    section_lines = []
    in_section = False
    
    for line in lines:
        if line.startswith(heading):
            in_section = True
            continue
        elif in_section and line.startswith('##'):
            break
        elif in_section:
            section_lines.append(line)
    
    return '\n'.join(section_lines).strip()

def list_affected_specs(specs_dir: Path) -> list[str]:
    """列出受影响的 spec 文件"""
    if not specs_dir.exists():
        return []
    
    affected = []
    for spec_file in specs_dir.rglob("spec.md"):
        # 读取 spec，找出 ADDED/MODIFIED/REMOVED 标记
        content = spec_file.read_text()
        if any(marker in content for marker in ["ADDED", "MODIFIED", "REMOVED"]):
            # 计算相对于 specs/ 根目录的路径
            relative = spec_file.relative_to(specs_dir.parent)
            affected.append(str(relative))
    
    return affected