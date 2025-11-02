"""
从 proposal 中自动提取技术决策
"""
import sys
from pathlib import Path

# 添加 scripts 目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

import yaml
from datetime import datetime
from ace_integration import learn_decision
from utils import extract_yaml_frontmatter, slugify
import re

def extract_decision_from_proposal(change_dir: Path):
    """从 proposal 和 design 文件中提取技术决策"""
    
    proposal_file = change_dir / "proposal.md"
    design_file = change_dir / "design.md"
    
    if not proposal_file.exists():
        print(f"⚠️  未找到 proposal.md，跳过学习")
        return
    
    proposal = proposal_file.read_text()
    design = design_file.read_text() if design_file.exists() else ""
    
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
        try:
            decision_doc = learn_decision(context)
            
            # 确保 decisions 目录存在
            decisions_dir = Path("openspec/knowledge/decisions")
            decisions_dir.mkdir(parents=True, exist_ok=True)
            
            # 存储到 knowledge/decisions/
            decision_file = decisions_dir / f"{datetime.now().strftime('%Y-%m-%d')}-{change_dir.name}.md"
            decision_file.write_text(decision_doc)
            
            # 向量化并索引到 ChromaDB
            try:
                index_to_chromadb(decision_doc, "decisions")
            except Exception as e:
                print(f"   ⚠️  向量化索引失败（不影响文档生成）: {e}")
            
            print(f"✅ 自动学习：从 {change_dir.name} 提取了技术决策")
        
        except Exception as e:
            print(f"❌ 学习失败: {e}")
            import traceback
            traceback.print_exc()
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

def index_to_chromadb(doc: str, collection_name: str):
    """向量化并索引到 ChromaDB"""
    import chromadb
    
    client = chromadb.PersistentClient(path="./openspec/knowledge/chroma_db")
    coll = client.get_or_create_collection(collection_name)
    
    # 提取元数据
    metadata = extract_yaml_frontmatter(doc)
    
    # 生成唯一 ID
    if 'date' in metadata:
        doc_id = f"{metadata['date']}-{metadata.get('related_change', 'unknown')}"
    else:
        import hashlib
        doc_id = hashlib.md5(doc.encode()).hexdigest()[:16]
    
    # 提取标题作为元数据
    title_match = re.search(r'^# (.+)$', doc, re.MULTILINE)
    if title_match:
        metadata['title'] = title_match.group(1)
    
    # 添加文件路径
    metadata['file_path'] = f"openspec/knowledge/{collection_name}/{metadata.get('date', 'unknown')}-{slugify(metadata.get('title', 'doc'))}.md"
    
    # 添加到集合
    coll.add(
        documents=[doc],
        metadatas=[metadata],
        ids=[doc_id]
    )
    
    print(f"   已索引到 {collection_name}: {doc_id}")