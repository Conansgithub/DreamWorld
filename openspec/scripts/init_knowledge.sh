#!/bin/bash
# 初始化 ACE 知识库结构

echo "🚀 初始化 OpenSpec 知识库..."

# 创建目录结构
mkdir -p openspec/knowledge/{decisions,lessons/{errors,patterns,antipatterns},system-knowledge,chroma_db}

# 初始化 CLAUDE.md（如果不存在）
if [ ! -f "openspec/knowledge/CLAUDE.md" ]; then
  cat > openspec/knowledge/CLAUDE.md << 'EOF'
# 项目全局上下文

本文档自动维护项目最重要的见解。
Claude Code 将始终加载此文件。

## 架构理解

（自动填充）

## 关键决策

（自动填充）

## 常见陷阱

（自动填充）

## 最佳实践

（自动填充）
EOF
fi

# 初始化 playbook.json
if [ ! -s "openspec/knowledge/playbook.json" ]; then
  cat > openspec/knowledge/playbook.json << 'EOF'
{
  "rules": [],
  "templates": {
    "technical-decision": {
      "required_sections": ["背景与问题", "考虑的方案", "最终决策", "接受的代价"],
      "quality_criteria": ["至少 2 个替代方案", "明确的选择理由"]
    },
    "error-solution": {
      "required_sections": ["症状", "根本原因", "解决方案", "预防措施"],
      "quality_criteria": ["清晰的复现步骤", "具体的解决代码"]
    },
    "code-pattern": {
      "required_sections": ["问题", "模式代码", "何时使用", "权衡"],
      "quality_criteria": ["完整的代码示例", "清晰的适用场景"]
    }
  },
  "metadata": {
    "version": "1.0",
    "last_updated": "2025-11-02"
  }
}
EOF
fi

# 安装 Python 依赖
echo "📦 安装 Python 依赖..."
pip install chromadb sentence-transformers watchdog pyyaml

# 下载嵌入模型
echo "📥 下载嵌入模型..."
python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('nomic-ai/nomic-embed-text-v1')"

echo "✅ 知识库初始化完成！"
echo ""
echo "下一步："
echo "1. 运行: chmod +x openspec/scripts/openspec-with-learning"
echo "2. 添加别名: alias openspec-learn='./openspec/scripts/openspec-with-learning'"
echo "3. 使用: openspec-learn proposal <change-id>"