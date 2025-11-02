from mcp import Server, Tool
import chromadb
from pathlib import Path

app = Server("openspec-knowledge")

# 初始化 ChromaDB 客户端
chroma_client = chromadb.PersistentClient(path="./.openspec/knowledge/chroma_db")

@app.tool()
def search_decisions(query: str, top_k: int = 3) -> list[dict]:
    """搜索相关的技术决策
    
    当你需要了解"为什么这样设计"时使用此工具。
    
    Args:
        query: 搜索查询，如 "为什么选择 JWT"
        top_k: 返回结果数量
    """
    collection = chroma_client.get_collection("decisions")
    results = collection.query(query_texts=[query], n_results=top_k)
    
    formatted = []
    for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
        formatted.append({
            "title": metadata['title'],
            "date": metadata['date'],
            "related_spec": metadata['related_spec'],
            "summary": doc[:300] + "...",
            "full_path": metadata['file_path'],
            "helpful": metadata.get('helpful', 0)
        })
    
    return formatted

@app.tool()
def search_errors(query: str, top_k: int = 3) -> list[dict]:
    """搜索过往遇到的错误和解决方案
    
    当你遇到问题或错误时，先用此工具搜索是否之前遇到过。
    
    Args:
        query: 错误描述或症状，如 "JWT 验证慢"
        top_k: 返回结果数量
    """
    collection = chroma_client.get_collection("error_solutions")
    results = collection.query(query_texts=[query], n_results=top_k)
    
    formatted = []
    for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
        formatted.append({
            "title": metadata['title'],
            "severity": metadata['severity'],
            "resolved": metadata['resolved'],
            "solution_summary": extract_solution_summary(doc),
            "full_path": metadata['file_path'],
            "helpful": metadata.get('helpful', 0)
        })
    
    return formatted

@app.tool()
def search_patterns(query: str, top_k: int = 5) -> list[dict]:
    """搜索相关的代码模式和最佳实践
    
    当你需要实现某个功能时，用此工具查找过往的实现模式。
    
    Args:
        query: 功能描述，如 "错误处理" 或 "缓存"
        top_k: 返回结果数量
    """
    collection = chroma_client.get_collection("code_patterns")
    results = collection.query(query_texts=[query], n_results=top_k)
    
    formatted = []
    for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
        # 提取代码示例
        code_example = extract_code_block(doc)
        
        formatted.append({
            "title": metadata['title'],
            "pattern_type": metadata['pattern_type'],
            "when_to_use": metadata['when_to_use'],
            "code_example": code_example,
            "full_path": metadata['file_path'],
            "helpful": metadata.get('helpful', 0)
        })
    
    return formatted

@app.tool()
def get_spec_context(spec_path: str) -> dict:
    """获取特定 spec 的完整上下文
    
    返回 spec 的内容以及相关的决策、错误、模式。
    
    Args:
        spec_path: spec 文件路径，如 "specs/auth/spec.md"
    """
    # 读取 spec
    spec_file = Path(spec_path)
    if not spec_file.exists():
        return {"error": f"Spec not found: {spec_path}"}
    
    spec_content = spec_file.read_text()
    
    # 查找相关的决策
    related_decisions = search_by_spec(spec_path, "decisions")
    
    # 查找相关的错误
    related_errors = search_by_spec(spec_path, "error_solutions")
    
    # 查找相关的模式
    related_patterns = search_by_spec(spec_path, "code_patterns")
    
    return {
        "spec_content": spec_content,
        "related_decisions": related_decisions,
        "related_errors": related_errors,
        "related_patterns": related_patterns
    }

@app.tool()
def mark_helpful(knowledge_file: str):
    """标记某个知识文件为"有用"
    
    当你使用了某个决策/错误/模式并发现它有帮助时，调用此工具。
    这会增加该知识的 helpful 计数，帮助系统学习什么是高质量的知识。
    
    Args:
        knowledge_file: 知识文件路径
    """
    file_path = Path(knowledge_file)
    content = file_path.read_text()
    
    # 解析 YAML frontmatter
    metadata = extract_yaml_frontmatter(content)
    metadata['helpful'] = metadata.get('helpful', 0) + 1
    
    # 更新文件
    new_content = replace_yaml_frontmatter(content, metadata)
    file_path.write_text(new_content)
    
    # 更新 ChromaDB 中的元数据
    update_chromadb_metadata(knowledge_file, metadata)
    
    return {"success": True, "new_helpful_count": metadata['helpful']}

@app.tool()
def mark_harmful(knowledge_file: str, reason: str):
    """标记某个知识文件为"有害/误导"
    
    当你发现某个决策/错误/模式的信息不准确或误导时，调用此工具。
    
    Args:
        knowledge_file: 知识文件路径
        reason: 为什么有害的说明
    """
    file_path = Path(knowledge_file)
    content = file_path.read_text()
    
    metadata = extract_yaml_frontmatter(content)
    metadata['harmful'] = metadata.get('harmful', 0) + 1
    
    # 添加反馈 section
    feedback = f"\n\n## ⚠️ 反馈 ({datetime.now().strftime('%Y-%m-%d')})\n\n{reason}\n"
    new_content = replace_yaml_frontmatter(content, metadata) + feedback
    file_path.write_text(new_content)
    
    update_chromadb_metadata(knowledge_file, metadata)
    
    return {"success": True, "new_harmful_count": metadata['harmful']}

@app.resource("claude-md")
def get_claude_md() -> str:
    """获取项目全局上下文 (CLAUDE.md)
    
    这个文件始终在你的上下文中，无需调用此工具。
    """
    return Path(".openspec/knowledge/CLAUDE.md").read_text()

def search_by_spec(spec_path: str, collection_name: str, top_k: int = 5) -> list[dict]:
    """根据 spec 路径搜索相关知识"""
    collection = chroma_client.get_collection(collection_name)
    
    # 使用 metadata 过滤
    results = collection.query(
        query_texts=[spec_path],
        n_results=top_k,
        where={"related_spec": {"$contains": spec_path}}
    )
    
    return format_results(results)

def extract_solution_summary(doc: str) -> str:
    """提取解决方案摘要"""
    pass

def extract_code_block(doc: str) -> str:
    """提取代码块"""
    pass

def extract_yaml_frontmatter(content: str) -> dict:
    """解析 YAML frontmatter"""
    pass

def replace_yaml_frontmatter(content: str, metadata: dict) -> str:
    """替换 YAML frontmatter"""
    pass

def update_chromadb_metadata(knowledge_file: str, metadata: dict):
    """更新 ChromaDB 元数据"""
    pass

def format_results(results) -> list[dict]:
    """格式化搜索结果"""
    pass

if __name__ == "__main__":
    app.run()