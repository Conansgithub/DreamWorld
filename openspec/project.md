# Project Context

## Purpose
DreamWorld 是一个多服务游戏平台，使用 .NET 8.0 构建后端服务，采用微服务架构。

## Tech Stack
- Backend: .NET 8.0 (ASP.NET Core Web API)
- Frontend: 计划中的 Web 客户端
- Database: 待定
- Containerization: Docker
- AI Assisted Development: OpenSpec + ACE 框架

## Project Conventions

### Code Style
- 使用 C# 最新语言特性
- 启用 Nullable Reference Types
- 遵循 RESTful API 设计原则

### Architecture Patterns
- 微服务设计：核心 API 和实时服务器分离
- API 优先开发：集成 Swagger/OpenAPI
- 容器优先：内置 Docker 支持

### Learning System (NEW)
本项目使用 ACE 框架自动学习开发经验：
- 技术决策自动记录在 `openspec/knowledge/decisions/`
- 错误和解决方案记录在 `openspec/knowledge/lessons/errors/`
- 代码模式记录在 `openspec/knowledge/lessons/patterns/`
- 顶级见解维护在 `openspec/knowledge/CLAUDE.md`

### Git Workflow
- 主分支：main
- 功能分支：feature/xxx
- 使用 OpenSpec 进行变更管理

## Domain Context
游戏平台领域，需要处理实时通信、用户管理、游戏状态等。

## Important Constraints
- 早期开发阶段
- 性能和安全性优先
- 保持代码简洁

## External Dependencies
- Swagger/OpenAPI (Swashbuckle.AspNetCore v6.6.2)