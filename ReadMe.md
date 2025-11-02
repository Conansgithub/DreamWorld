# OpenSpec + ACE 知识库

本目录包含项目的自动学习知识库。

## 目录结构
```
knowledge/
├── CLAUDE.md                 # 项目全局上下文（始终在 Claude 上下文中）
├── playbook.json            # ACE Playbook 状态
├── decisions/               # 技术决策记录
├── lessons/                 # 实现经验
│   ├── errors/             # 错误和解决方案
│   ├── patterns/           # 代码模式
│   └── antipatterns/       # 应避免的做法
├── system-knowledge/        # 系统级理解
└── chroma_db/              # 向量数据库
```

## 如何使用

### 自动学习
系统在以下时机自动学习：
- **Proposal 创建后**：提取技术决策
- **Apply 实现中**：捕获错误和模式
- **Archive 归档后**：提取系统洞察

### 手动查询
使用 Claude Code 的 MCP 工具：
```
@openspec-knowledge:search_decisions "为什么选择 XXX"
@openspec-knowledge:search_errors "XXX 错误"
@openspec-knowledge:search_patterns "XXX 实现"
```

### 反馈机制
标记知识质量：
```
@openspec-knowledge:mark_helpful "knowledge/decisions/xxx.md"
@openspec-knowledge:mark_harmful "knowledge/decisions/xxx.md" "原因"
```

## 维护

- **每周**：检查 helpful/harmful 比率，修剪低质量知识
- **每月**：更新 CLAUDE.md，确保顶级见解最新
- **每季度**：归档 12 个月前的知识