"""
测试 ACE 集成
"""
import sys
from pathlib import Path

# 添加 scripts 目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

import shutil
import subprocess

def test_proposal_learning():
    """测试 Proposal 阶段学习"""
    print("🧪 测试 Proposal 学习...")
    
    # 创建测试 proposal
    test_change = Path("openspec/changes/test-decision")
    test_change.mkdir(parents=True, exist_ok=True)
    
    # 写入 proposal.md
    (test_change / "proposal.md").write_text("""
## Why
测试技术决策提取

## What Changes
- 添加测试功能
""")
    
    # 写入 design.md
    (test_change / "design.md").write_text("""
## Alternatives Considered

### 方案 1: 简单方案
优点：快速
缺点：功能有限

### 方案 2: 复杂方案
优点：功能强大
缺点：开发慢

## Decision Rationale
选择方案 1，因为现阶段速度更重要
""")
    
    # 运行学习
    from learn_from_proposal import extract_decision_from_proposal
    
    try:
        extract_decision_from_proposal(test_change)
        
        # 验证结果
        decisions_dir = Path("openspec/knowledge/decisions")
        if decisions_dir.exists():
            decision_files = list(decisions_dir.glob("*test-decision.md"))
            
            if decision_files:
                print("✅ Proposal 学习测试通过")
                print(f"   生成文件: {decision_files[0]}")
            else:
                print("❌ Proposal 学习测试失败：未找到生成的决策文件")
        else:
            print("❌ Proposal 学习测试失败：decisions 目录不存在")
    
    except Exception as e:
        print(f"❌ Proposal 学习测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 清理
        if test_change.exists():
            shutil.rmtree(test_change)

def test_chromadb_indexing():
    """测试 ChromaDB 索引"""
    print("🧪 测试 ChromaDB 索引...")
    
    try:
        import chromadb
        
        client = chromadb.PersistentClient(path="./openspec/knowledge/chroma_db")
        
        # 尝试获取或创建集合
        collection = client.get_or_create_collection("test_collection")
        
        # 添加测试文档
        collection.add(
            documents=["这是一个测试文档"],
            metadatas=[{"type": "test", "date": "2025-11-02"}],
            ids=["test-001"]
        )
        
        # 查询
        results = collection.query(
            query_texts=["测试"],
            n_results=1
        )
        
        if results['documents'][0]:
            print("✅ ChromaDB 索引测试通过")
        else:
            print("❌ ChromaDB 索引测试失败")
        
        # 清理
        client.delete_collection("test_collection")
    
    except Exception as e:
        print(f"❌ ChromaDB 索引测试失败: {e}")
        import traceback
        traceback.print_exc()

def test_mcp_server():
    """测试 MCP 服务器"""
    print("🧪 测试 MCP 服务器...")
    
    # 跳过 MCP 服务器测试（需要 mcp 库）
    print("⏭️  MCP 服务器测试已跳过（需要先安装 mcp 库）")

if __name__ == "__main__":
    print("🚀 开始集成测试...\n")
    
    test_proposal_learning()
    print()
    test_chromadb_indexing()
    print()
    test_mcp_server()
    
    print("\n✅ 集成测试完成")