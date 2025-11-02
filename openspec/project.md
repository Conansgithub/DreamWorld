# 项目上下文

## 目的
DreamWorld是一个由AI担任专业"地下城主"(DM)的在线TRPG平台。玩家在"主神空间"进行社交准备，然后通过独一无二的"种子ID"，组队进入由AI动态主持的、规则严谨的回合制"轮回世界"，体验可分享、可攻略的传奇冒险，并追寻由AI即时创造的、拥有专属故事的"神赐装备"。

## 技术栈
- **管理后端**: .NET 8.0 (ASP.NET Core Web API)
- **游戏服务**: Go (Gin框架)
- **管理前端**: React 18+ (TypeScript)
- **游戏前端**: Vue 3 (Composition API, TypeScript)
- **容器化**: Docker (Linux目标)
- **API文档**: Swagger/OpenAPI (后端), OpenAPI规范 (游戏服务)
- **实时通信**: WebSocket (Go实现)
- **规范管理**: OpenSpec框架
- **开发工具**: Visual Studio (C#), VS Code (Go/React/Vue), GoLand

## 项目约定

### 代码风格
- **C#代码**: 遵循Microsoft C#编码约定
  - 类名：PascalCase (例：`WeatherForecastController`)
  - 方法名：PascalCase (例：`GetWeatherForecast`)
  - 变量名：camelCase (例：`_logger`)
  - 常量：PascalCase (例：`Summaries`)
  - 文件组织：按功能模块组织，控制器放在Controllers文件夹
  - 启用特性：Nullable引用类型、隐式using语句

- **Go代码**: 遵循Go官方代码规范
  - 包名：小写，简短，有意义
  - 函数名：驼峰命名，导出函数首字母大写
  - 变量名：驼峰命名，简短明确
  - 常量：大写，下划线分隔
  - 文件组织：按功能分包，handler、model、service分离

- **React代码**: 遵循React和TypeScript最佳实践
  - 组件名：PascalCase
  - 文件名：PascalCase (.tsx)
  - 变量/函数：camelCase
  - 常量：UPPER_SNAKE_CASE
  - 使用函数组件和Hooks

- **Vue代码**: 遵循Vue 3官方风格指南
  - 组件名：PascalCase (多单词)
  - 文件名：kebab-case
  - 变量/函数：camelCase
  - 常量：UPPER_SNAKE_CASE
  - 使用Composition API和<script setup>

### 架构模式
- **微服务架构**:
  - C# 核心API (`core-api`): 处理**核心游戏逻辑**（AI交互、规则裁定、数据库持久化）、用户管理、内容管理。**它是游戏的大脑。**
  - Go 实时服务 (`realtime-api`): **只处理实时通信**（WebSocket消息广播、频道管理）。**它是游戏的神经网络，不处理复杂逻辑。**
  - 前端应用分离: 管理端(React)和游戏端(Vue)

- **分层架构**:
  - .NET: 控制器层、服务层、数据访问层
  - Go: Handler层、Service层、Repository层
  - React: 组件层、状态管理(Redux/Zustand)、API服务层
  - Vue: 组件层、状态管理(Pinia)、API服务层

- **通信模式**:
  - RESTful API: 管理端与后端通信，服务间HTTP通信
  - WebSocket: 游戏端与实时服务通信
  - 服务间通信: 初期使用HTTP/REST，性能瓶颈时考虑gRPC

- **容器化部署**: Docker容器化，支持多环境部署
- **API版本控制**: 语义化版本控制策略

### 测试策略
- **C#测试**:
  - 单元测试: xUnit覆盖核心业务逻辑
  - 集成测试: WebApplicationFactory测试API端点
  - 测试覆盖率: 目标80%以上

- **Go测试**:
  - 单元测试: 标准testing包
  - 基准测试: testing/benchmark
  - 集成测试: testify或testcontainers

- **前端测试**:
  - React: Jest + React Testing Library
  - Vue: Vitest + Vue Test Utils
  - E2E测试: Playwright或Cypress

- **API测试**:
  - REST API: Postman/Newman自动化测试
  - WebSocket: 自定义测试脚本
  - 性能测试: Artillery或k6

### Git工作流
- **分支策略**: GitHub Flow (单一main分支，feature分支开发)
- **提交约定**: 使用约定式提交格式
  - feat: 新功能
  - fix: 错误修复
  - docs: 文档更新
  - style: 代码格式调整
  - refactor: 重构
  - test: 测试相关
- **代码审查**: 所有PR必须经过代码审查
- **分支保护**: main分支需要PR和审查

## 领域上下文
DreamWorld项目专注于AI驱动的在线TRPG平台，核心是"AI Dungeon Master"概念：

### 核心游戏循环
- **准备阶段 @ 主神空间**: 安全的中央社交枢纽，角色成长、装备整理、种子分享、队伍组建
- **冒险阶段 @ 轮回世界**: AI DM主持的回合制TRPG体验，动态叙事、规则仲裁、神赐装备获取

### 核心概念
- **主神空间 (Hub World)**: 程序驱动的安全社交枢纽，角色管理、装备整理、排行榜、种子分享、队伍组建
- **轮回世界 (Mission World)**: AI驱动的回合制副本，基于种子ID生成，支持分享和重复挑战
- **神赐装备 (AI-Generated Loot)**: AI根据剧情、怪物主题和玩家表现即时创造的独特故事装备
- **地下城主 (Dungeon Master)**: AI核心身份，负责动态叙事、规则裁定、NPC扮演、伏笔埋设
- **种子系统**: 每个轮回世界的唯一标识，支持分享、攻略、速通挑战

### 技术需求
- **回合制战斗系统**: 严格的TRPG规则引擎，技能检定、豁免检定、战术规划
- **AI叙事引擎**: 动态生成对话、事件分支、剧情发展，记忆玩家行为影响
- **实时同步**: 多玩家回合制状态同步，行动队列管理
- **内容生成**: AI驱动的装备、怪物、场景程序化生成

## 重要约束
- **性能要求**: 支持1000+并发用户，回合制响应时间<500ms，实时通信延迟<100ms
- **游戏公平性**: 严格的TRPG规则引擎，确保掷骰和数值计算的透明性和公平性
- **AI响应质量**: AI DM响应时间<2秒，保持叙事连贯性和逻辑一致性
- **种子确定性**: 相同种子ID必须生成相同的基础世界结构，确保可攻略性
- **安全要求**: 用户数据加密，API访问控制，防止作弊和外挂
- **可扩展性**: 水平扩展支持，微服务独立部署
- **兼容性**: 支持现代浏览器，移动端响应式设计
- **数据保护**: 遵循GDPR等数据保护法规

## 外部依赖
- **数据库**:
  - 管理数据: PostgreSQL (用户、角色、装备、种子元数据)
  - 游戏数据: Redis (实时回合状态、会话、行动队列) + MongoDB (冒险历史、AI叙事日志)
  - 内容数据: PostgreSQL (种子模板、怪物库、装备基础数据)

- **缓存**: Redis集群 (会话、实时数据、排行榜)

- **消息队列**:
  - 初期: 暂不引入，使用HTTP直接通信
  - 后期: 性能瓶颈时考虑RabbitMQ或Apache Kafka

- **CDN**: CloudFlare或AWS CloudFront (静态资源)

- **监控**:
  - APM: Datadog或New Relic
  - 日志: ELK Stack (Elasticsearch, Logstash, Kibana)
  - 指标: Prometheus + Grafana

- **认证**:
  - JWT + OAuth2.0
  - 身份提供商: Auth0或自建IdentityServer

- **存储**:
  - 文件存储: AWS S3或MinIO
  - 资源分发: CDN加速
