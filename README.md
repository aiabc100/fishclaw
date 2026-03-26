# FishClaw

一个轻量级、可扩展的 AI 智能体框架，从零开始构建，帮助理解 AI Agent 的核心架构。

## 项目简介

FishClaw 是一个教学性质的 AI 智能体框架，采用清晰的三层架构设计，展示了如何从零构建一个完整的 AI Agent 系统。项目代码简洁易懂，适合学习 AI 智能体的核心概念。

## 架构设计

```
┌─────────────────────────────────────────────────────┐
│                    用户输入                          │
└─────────────────────┬───────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────┐
│                   Gateway 网关层                     │
│  • 请求接收与路由                                    │
│  • 身份认证                                          │
│  • 会话管理                                          │
└─────────────────────┬───────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────┐
│                    Agent 智能体层                    │
│  • 技能加载与管理                                    │
│  • 命令解析与执行                                    │
│  • 决策逻辑                                          │
└─────────────────────┬───────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────┐
│                   Memory 记忆层                      │
│  • 短期记忆（会话历史）                              │
│  • 长期记忆（用户偏好）                              │
│  • 持久化存储                                        │
└─────────────────────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────┐
│                    Skills 技能层                     │
│  • GreetingSkill（问候技能）                         │
│  • FileSkill（文件操作技能）                         │
│  • 可扩展更多技能...                                 │
└─────────────────────────────────────────────────────┘
```

## 目录结构

```
fishclaw_v1/
├── core/                   # 核心模块
│   ├── __init__.py
│   ├── agent.py           # 智能体层
│   ├── gateway.py         # 网关层
│   ├── memory.py          # 记忆层
│   └── skill_base.py      # 技能基类
├── skills/                 # 技能模块
│   ├── __init__.py
│   ├── greeting_skill.py  # 问候技能
│   └── file_skill.py      # 文件操作技能
├── config.yaml            # 配置文件
├── demo.py                # 演示程序
├── requirements.txt       # 依赖列表
└── README.md              # 项目说明
```

## 快速开始

### 环境要求

- Python 3.8+
- 无需额外依赖（仅需 PyYAML）

### 安装

```bash
# 克隆项目
git clone https://github.com/yourusername/fishclaw.git
cd fishclaw

# 安装依赖
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 运行演示

```bash
python demo.py
```

### 可用命令

| 命令 | 说明 | 示例 |
|------|------|------|
| 你好 [名字] | 打个招呼 | `你好 张三` |
| 记住 [名字] | 让 AI 记住你的名字 | `记住 李四` |
| 保存到文件 [内容] | 保存内容到文件 | `保存到文件 这是一段笔记` |
| 列出文件 | 查看已保存的文件 | `列出文件` |
| 帮助 | 显示帮助信息 | `帮助` |
| 退出 | 退出程序 | `退出` |

## 核心组件

### 1. Gateway（网关层）

网关层是系统的入口，负责：
- 接收用户请求
- 身份认证（简化版）
- 创建和管理会话
- 路由到智能体
- 返回响应

### 2. Agent（智能体层）

智能体层是核心决策单元，负责：
- 加载和管理技能
- 接收网关的命令
- 调用合适的技能执行
- 与记忆层交互

### 3. Memory（记忆层）

记忆层负责数据存储，包括：
- **短期记忆**：按会话 ID 存储对话历史
- **长期记忆**：存储用户偏好，跨会话持久化

### 4. Skills（技能系统）

技能系统采用插件化设计，所有技能继承自 `BaseSkill` 基类：

```python
from core.skill_base import BaseSkill

class MySkill(BaseSkill):
    @property
    def name(self) -> str:
        return "my_skill"
    
    @property
    def description(self) -> str:
        return "我的自定义技能"
    
    def execute(self, params: dict) -> dict:
        return {
            "status": "success",
            "output": "执行成功"
        }
```

## 扩展技能

### 创建新技能

1. 在 `skills/` 目录下创建新的技能文件：

```python
# skills/my_skill.py

class MySkill:
    def __init__(self):
        self.name = "my_skill"
        self.description = "我的自定义技能"
        self.memory = None
    
    def set_memory(self, memory):
        self.memory = memory
    
    def execute(self, params):
        return {
            "status": "success",
            "output": "执行成功"
        }

def create_skill():
    return MySkill()
```

2. 在 `config.yaml` 中注册技能：

```yaml
skills:
  - name: "my_skill"
    path: "./skills/my_skill.py"
    enabled: true
    description: "我的自定义技能"
```

3. 在 `agent.py` 中添加命令处理逻辑。

## 配置说明

```yaml
# 智能体配置
agent:
  name: "FishClaw"
  description: "我的第一个OpenClaw智能体"

# 技能配置
skills:
  - name: "greeting"
    path: "./skills/greeting_skill.py"
    enabled: true

# 记忆配置
memory:
  type: "file"
  path: "./memory"
  auto_save: true
  max_history: 50

# 网关配置
gateway:
  host: "localhost"
  port: 8080
  enable_auth: false
```

## 内置技能

### GreetingSkill（问候技能）

- 根据时间返回个性化问候（早上好/中午好/下午好/晚上好）
- 支持记住用户名字
- 支持从记忆中读取用户偏好

### FileSkill（文件操作技能）

- 保存内容到文件
- 读取文件内容
- 列出已保存的文件

## 学习要点

通过这个项目，你可以学习到：

1. **分层架构设计**：如何将系统划分为清晰的层次
2. **插件化设计**：如何实现可扩展的技能系统
3. **记忆管理**：如何实现短期和长期记忆
4. **会话管理**：如何管理用户会话
5. **配置驱动**：如何使用配置文件控制系统行为

## 后续扩展方向

- [ ] 接入大语言模型（LLM）
- [ ] 添加更多技能（搜索、翻译、代码执行等）
- [ ] 实现 REST API 接口
- [ ] 添加向量数据库支持
- [ ] 实现多智能体协作
- [ ] 添加工具调用能力

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
