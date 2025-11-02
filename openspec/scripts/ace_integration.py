import sys
from pathlib import Path

# 添加 scripts 目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from datetime import datetime
import json
import os

# 导入 ACE 框架
try:
    from ace import LiteLLMClient, Generator, Reflector, Curator, Playbook
    ACE_AVAILABLE = True
except ImportError:
    ACE_AVAILABLE = False
    print("⚠️  ACE 框架未安装，将使用模拟模式")
    print("   安装: pip install ace-framework")

def learn_decision(context: dict) -> str:
    """使用 ACE 框架生成结构化的技术决策文档"""
    
    if not ACE_AVAILABLE:
        return generate_mock_decision(context)
    
    try:
        # 设置 API key（从环境变量读取）
        api_key = os.environ.get('ANTHROPIC_API_KEY') or os.environ.get('OPENAI_API_KEY')
        if not api_key:
            print("⚠️  未设置 API key，使用模拟模式")
            return generate_mock_decision(context)
        
        # 初始化 LLM 客户端
        # 优先使用 Claude，回退到 GPT
        if os.environ.get('ANTHROPIC_API_KEY'):
            model = "claude-sonnet-4"
        else:
            model = "gpt-4o-mini"
        
        client = LiteLLMClient(model=model)
        
        # 初始化 ACE 组件
        generator = Generator(client)
        reflector = Reflector(client)
        curator = Curator(client)
        playbook = get_playbook()
        
        # 构建问题和上下文
        question = f"分析技术决策：{context['change_id']}"
        full_context = f"""
## 变更背景
{context['why']}

## 考虑的方案
{context['alternatives']}

## 决策理由
{context['decision']}

## 影响的规范
{', '.join(context['affected_specs'])}
"""
        
        # 1. Generator 生成分析
        print("   🎯 Generator 正在分析决策...")
        generator_result = generator.generate(
            question=question,
            context=full_context,
            playbook=playbook
        )
        
        # 2. Reflector 提取洞察
        print("   🔍 Reflector 正在提取洞察...")
        reflection = reflector.reflect(
            question=question,
            generator_output=generator_result,
            environment_result=None,  # 技术决策没有执行反馈
            playbook=playbook
        )
        
        # 3. Curator 生成结构化文档
        print("   📝 Curator 正在生成结构化文档...")
        
        # 从 reflection 中提取信息，生成我们需要的格式
        structured_doc = format_decision_document(
            context=context,
            reflection=reflection
        )
        
        # 4. 更新 Playbook（可选）
        try:
            deltas = curator.curate(
                question=question,
                reflection=reflection,
                playbook=playbook
            )
            
            # 合并 deltas 到 playbook
            if deltas and hasattr(playbook, 'merge_deltas'):
                playbook.merge_deltas(deltas)
                
                # 保存更新后的 playbook
                playbook_path = Path("openspec/knowledge/playbook.json")
                if hasattr(playbook, 'save'):
                    playbook.save(str(playbook_path))
                elif hasattr(playbook, 'to_dict'):
                    import json
                    with open(playbook_path, 'w', encoding='utf-8') as f:
                        json.dump(playbook.to_dict(), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"   ⚠️  Playbook 更新失败（不影响文档生成）: {e}")
        
        return structured_doc
    
    except Exception as e:
        print(f"⚠️  ACE 生成失败，使用模拟模式: {e}")
        import traceback
        traceback.print_exc()
        return generate_mock_decision(context)

def format_decision_document(context: dict, reflection) -> str:
    """将 ACE reflection 格式化为我们的决策文档格式"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 提取 reflection 中的关键洞察
    key_insight = ""
    if hasattr(reflection, 'key_insight'):
        key_insight = reflection.key_insight
    elif isinstance(reflection, dict):
        key_insight = reflection.get('key_insight', '')
    elif hasattr(reflection, '__dict__'):
        key_insight = str(reflection)
    
    return f"""---
type: technical-decision
date: {today}
related_change: {context['change_id']}
related_spec: {context['affected_specs']}
helpful: 0
harmful: 0
tags: [decision, ace-generated]
---

# 技术决策：{context['change_id']}

## 背景与问题
{context['why']}

## 考虑的方案
{context['alternatives']}

## 最终决策
{context['decision']}

## ACE 分析洞察
{key_insight}

## 影响的规范
{', '.join(context['affected_specs'])}

## 接受的代价
待后续回顾时补充

## 相关资源
- 变更 ID: {context['change_id']}
- 分析时间: {today}
"""

def generate_mock_decision(context: dict) -> str:
    """生成模拟的决策文档（当 ACE 不可用时）"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    return f"""---
type: technical-decision
date: {today}
related_change: {context['change_id']}
related_spec: {context['affected_specs']}
helpful: 0
harmful: 0
tags: [decision, mock]
---

# 技术决策：{context['change_id']}

## 背景与问题
{context['why']}

## 考虑的方案
{context['alternatives']}

## 最终决策
{context['decision']}

## 接受的代价
待补充

## 相关资源
- 变更 ID: {context['change_id']}

*注：此文档由模拟模式生成。安装 ace-framework 并设置 API key 以启用真正的 ACE 分析。*
"""

def learn_error_solution(context: dict) -> str:
    """从错误和解决方案中生成学习文档"""
    if not ACE_AVAILABLE:
        return generate_mock_error_solution(context)
    
    # 实现类似 learn_decision 的逻辑
    # 为了简洁，这里先使用 mock
    return generate_mock_error_solution(context)

def generate_mock_error_solution(context: dict) -> str:
    """生成模拟的错误解决方案文档"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    return f"""---
type: error-solution
date: {today}
related_change: {context['change_id']}
severity: medium
resolved: true
helpful: 0
harmful: 0
tags: [error, fix, mock]
---

# 错误解决方案：{context['change_id']}

## 症状
{context.get('error', '错误信息')}

## 解决方案
已通过 commit {context.get('solution_commit', 'unknown')} 修复

## 代码变更
```
{context.get('solution_diff', '无代码变更')[:500]}
```

*注：此文档由模拟模式生成。*
"""

def learn_code_pattern(context: dict) -> str:
    """从 commit 提取代码模式"""
    if not ACE_AVAILABLE:
        return generate_mock_code_pattern(context)
    
    return generate_mock_code_pattern(context)

def generate_mock_code_pattern(context: dict) -> str:
    """生成模拟的代码模式文档"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    return f"""---
type: code-pattern
date: {today}
related_change: {context['change_id']}
pattern_type: {context.get('patterns', ['general'])[0]}
helpful: 0
harmful: 0
tags: [pattern, mock]
---

# 代码模式：{context.get('commit_message', 'Unknown')}

## 检测到的模式
{', '.join(context.get('patterns', []))}

## 代码变更
```
{context.get('diff', '无代码变更')[:500]}
```

*注：此文档由模拟模式生成。*
"""

def learn_system_knowledge(context: dict) -> str:
    """从归档变更提取系统级知识"""
    if not ACE_AVAILABLE:
        return generate_mock_system_knowledge(context)
    
    return generate_mock_system_knowledge(context)

def generate_mock_system_knowledge(context: dict) -> str:
    """生成模拟的系统知识文档"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    return f"""---
type: system-knowledge
date: {today}
related_change: {context['change_id']}
category: 架构理解
helpful: 0
harmful: 0
tags: [system, knowledge, mock]
---

# 系统洞察：{context['change_id']}

## 概述
完成了 {context['change_id']} 的开发和归档

## 关键学习点
- 相关决策: {len(context.get('decisions', []))} 个
- 相关错误: {len(context.get('errors', []))} 个
- 相关模式: {len(context.get('patterns', []))} 个

## Spec 变更
{json.dumps(context.get('specs_changes', {}), ensure_ascii=False, indent=2)}

*注：此文档由模拟模式生成。*
"""

def get_playbook():
    """获取或创建项目的 Playbook"""
    playbook_path = Path("openspec/knowledge/playbook.json")
    
    if not ACE_AVAILABLE:
        return None
    
    try:
        # 尝试加载现有 playbook
        if playbook_path.exists() and playbook_path.stat().st_size > 0:
            # ACE Playbook 的加载方法
            if hasattr(Playbook, 'from_file'):
                return Playbook.from_file(str(playbook_path))
            elif hasattr(Playbook, 'from_dict'):
                with open(playbook_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return Playbook.from_dict(data)
        
        # 创建新的 Playbook
        playbook = Playbook()
        
        # 保存空的 playbook
        playbook_path.parent.mkdir(parents=True, exist_ok=True)
        if hasattr(playbook, 'save'):
            playbook.save(str(playbook_path))
        elif hasattr(playbook, 'to_dict'):
            with open(playbook_path, 'w', encoding='utf-8') as f:
                json.dump(playbook.to_dict(), f, ensure_ascii=False, indent=2)
        
        return playbook
    
    except Exception as e:
        print(f"⚠️  Playbook 操作失败: {e}")
        # 返回新的 Playbook 实例
        try:
            return Playbook()
        except:
            return None