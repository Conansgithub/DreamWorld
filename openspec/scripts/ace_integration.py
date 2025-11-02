from ace import Generator, Reflector, Curator, Playbook, LiteLLMClient
from pathlib import Path

def learn_error_solution(context: dict) -> str:
    """从错误和解决方案中生成学习文档"""

def learn_code_pattern(context: dict) -> str:
    """从 commit 提取代码模式"""

def learn_system_knowledge(context: dict) -> str:
    """从归档变更提取系统级知识"""

def learn_decision(context: dict) -> str:
    """使用 ACE 框架生成结构化的技术决策文档"""
    
    client = LiteLLMClient(model="claude-sonnet-4")
    generator = Generator(client)
    reflector = Reflector(client)
    
    # 1. Generator 生成决策分析
    analysis = generator.generate(
        question=f"分析这个技术决策的理由和权衡",
        context=f"""
变更ID: {context['change_id']}
为什么: {context['why']}
考虑的替代方案: {context['alternatives']}
决策理由: {context['decision']}
影响的规范: {', '.join(context['affected_specs'])}
""",
        playbook=get_playbook()
    )
    
    # 2. Reflector 提取结构化信息
    structured = reflector.reflect(
        generator_output=analysis,
        prompt="""
从上面的分析中提取以下结构化信息，输出为 YAML + Markdown 格式：
```yaml
---
type: technical-decision
date: YYYY-MM-DD
related_spec: [spec 路径列表]
related_change: archive/YYYY-MM-DD-xxx/
tags: [相关标签]
---
```

然后包含以下 Markdown sections：
# 技术决策：[简洁标题]

## 背景与问题
[描述要解决的问题和约束条件]

## 考虑的方案
[列出每个方案的优缺点]

## 最终决策
[说明选择了什么方案及其理由]

## 接受的代价
[列出这个决策的缺点和我们愿意接受的理由]

## 相关资源
[链接到相关文档、讨论等]
"""
    )
    
    return structured

def get_playbook() -> Playbook:
    """获取或创建项目的 Playbook"""
    playbook_path = Path(".openspec/knowledge/playbook.json")
    if playbook_path.exists():
        return Playbook.load(playbook_path)
    else:
        # 初始化新 playbook
        playbook = Playbook()
        playbook.add_rule("技术决策模板", """
技术决策文档应该包含：
1. 明确的问题陈述
2. 至少 2 个考虑的替代方案
3. 每个方案的优缺点分析
4. 选择理由（技术、业务、团队能力等）
5. 接受的代价和缓解措施
6. 如果有条件，包含"验证结果"（几个月后的回顾）
""")
        return playbook