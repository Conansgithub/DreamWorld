<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DreamWorld is a multi-service gaming platform built with .NET 8.0 backend services and planned web clients. The project is in early development stage with a clean microservices architecture foundation.

**Technology Stack:**
- Backend: .NET 8.0 (ASP.NET Core Web API) with C#
- Containerization: Docker with multi-stage builds
- API Documentation: Swagger/OpenAPI (Swashbuckle.AspNetCore v6.6.2)
- Frontend: Planned web clients (game-client, admin-client)
- Real-time: Planned real-time server

## Repository Structure

```
DreamWorld/
├── servers/                    # Backend services
│   ├── core-api/              # Main ASP.NET Core API (currently implemented)
│   └── realtime-server/       # Placeholder for real-time communication
├── web/                       # Frontend applications (placeholders)
│   ├── game-client/          # Main gaming interface
│   └── admin-client/         # Administrative interface
├── .vscode/                   # VS Code configuration
└── AGENTS.md                  # OpenSpec framework instructions
```

## Development Commands

### Core API Development
**Working Directory:** `/servers/core-api/`

#### Build & Run Commands
```bash
# Build the solution
dotnet build DreamWorldCoreApi.sln

# Run in development mode (launches Swagger UI)
dotnet run

# Watch for changes and auto-restart
dotnet watch run

# Publish for deployment
dotnet publish DreamWorldCoreApi.sln
```

#### VS Code Development
- **F5 Debugging**: Launches API and opens browser to Swagger UI automatically
- **Build Tasks**: Use Command Palette → "Tasks: Run Task" → build/publish/watch
- **Hot Reload**: Built-in with `dotnet watch run`

#### Docker Development
```bash
# Build Docker image (from servers/core-api/)
docker build -t dreamworld-core-api .

# Run container
docker run -p 8080:8080 -p 8081:8081 dreamworld-core-api
```

### Development URLs
- **HTTP API**: `http://localhost:5215`
- **HTTPS API**: `https://localhost:7230`
- **Swagger UI**: `http://localhost:5215/swagger` (available in Development mode)
- **Docker Container**: `http://localhost:8080`

## Architecture & Conventions

### Current Implementation
- **Minimal API Model**: Clean ASP.NET Core minimal hosting in `Program.cs`
- **Standard Controllers**: Traditional MVC pattern (see `WeatherForecastController.cs`)
- **Configuration Management**: .NET configuration system with environment-specific settings
- **Dependency Injection**: Standard .NET DI container
- **Nullable Reference Types**: Enabled for better null safety
- **Implicit Usings**: Enabled for cleaner code

### Project Architecture Patterns
- **Microservices Design**: Separate services for core API and real-time functionality
- **API-First Development**: Swagger/OpenAPI documentation integrated from start
- **Container-First**: Docker support built-in with multi-stage builds
- **Multi-Client Architecture**: Separate game and admin client interfaces planned

### Configuration Files
- `appsettings.json`: Base application configuration
- `appsettings.Development.json`: Development-specific settings
- `Properties/launchSettings.json`: Multiple launch profiles (HTTP, HTTPS, IIS Express, Docker)
- `.vscode/launch.json`: Debug configuration with automatic browser launch
- `.vscode/tasks.json`: Build, publish, and watch tasks

## Development Workflow

### Making Changes
1. Work in `/servers/core-api/` for backend API development
2. Use `dotnet watch run` for development with hot reload
3. Test APIs using Swagger UI or the provided `.http` file
4. Use VS Code debugger (F5) for debugging with automatic browser launch
5. Build Docker image to test containerized deployment

### Testing APIs
- **Swagger UI**: Available at `/swagger` endpoint in Development mode
- **HTTP Files**: Use `DreamWorldCoreApi.http` for API testing with VS Code
- **Browser**: APIs accessible directly via browser for GET requests

### Deployment
- **Docker**: Multi-stage builds optimized for production
- **Publish**: Use `dotnet publish` for deployment artifacts
- **User Secrets**: Configure sensitive data via .NET User Secrets

## Important Notes

### OpenSpec Framework
This project uses the OpenSpec framework for AI-assisted development. Refer to `AGENTS.md` for:
- Change proposal processes
- Specification formats and conventions
- Project structure guidelines

### Current State
- Project is in initialization stage with template weather forecast API
- Core infrastructure is in place (Docker, Swagger, VS Code integration)
- Ready for gaming-specific API development
- Frontend and real-time server directories are placeholders waiting for implementation

### Development Standards
- .NET 8.0 with latest language features
- Comprehensive Git ignore covering multiple technology stacks
- VS Code as primary development environment
- Modern async/await patterns expected
- RESTful API design principles