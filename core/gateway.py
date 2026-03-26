# core/gateway.py
"""
网关层 - 系统的入口，负责接收请求和路由
"""
import time
import uuid
from typing import Dict, Any, Optional, Callable

class Gateway:
    """
    网关层
    职责：
    1. 接收用户请求
    2. 身份认证（简化版）
    3. 创建/管理会话
    4. 路由到智能体
    5. 返回响应
    """
    
    def __init__(self):
        self.agent = None
        self.sessions = {}  # 会话存储
        self.request_count = 0
        
        print("[网关层] 初始化完成")
    
    def register_agent(self, agent):
        """
        注册智能体
        
        参数:
            agent: 智能体实例
        """
        self.agent = agent
        print(f"[网关层] 智能体已注册: {agent.name}")
    
    def _get_or_create_session(self, session_id: Optional[str] = None) -> str:
        """
        获取或创建会话ID
        
        参数:
            session_id: 可选的现有会话ID
            
        返回:
            有效的会话ID
        """
        if session_id and session_id in self.sessions:
            # 更新最后活动时间
            self.sessions[session_id]["last_active"] = time.time()
            return session_id
        
        # 创建新会话
        new_session_id = session_id or f"session_{uuid.uuid4().hex[:8]}"
        self.sessions[new_session_id] = {
            "created_at": time.time(),
            "last_active": time.time(),
            "request_count": 0
        }
        print(f"[网关层] 创建新会话: {new_session_id}")
        return new_session_id
    
    def _authenticate(self, auth_token: Optional[str] = None) -> bool:
        """
        简化的身份认证
        
        参数:
            auth_token: 认证令牌
            
        返回:
            是否认证通过
        """
        # 简化版：总是返回True，实际项目可扩展
        return True
    
    def handle_request(self, 
                      user_input: str, 
                      session_id: Optional[str] = None,
                      auth_token: Optional[str] = None) -> Dict[str, Any]:
        """
        处理用户请求的主方法
        
        参数:
            user_input: 用户输入
            session_id: 会话ID
            auth_token: 认证令牌
            
        返回:
            处理结果
        """
        self.request_count += 1
        request_id = f"req_{self.request_count:04d}"
        
        print(f"\n{'='*50}")
        print(f"[网关层] 收到请求 [{request_id}]")
        print(f"[网关层] 用户输入: '{user_input}'")
        print(f"[网关层] 会话ID: {session_id}")
        
        # 1. 身份认证
        if not self._authenticate(auth_token):
            return {
                "status": "error",
                "error": "认证失败",
                "request_id": request_id
            }
        
        # 2. 获取/创建会话
        valid_session_id = self._get_or_create_session(session_id)
        
        # 3. 记录请求
        self.sessions[valid_session_id]["request_count"] += 1
        
        # 4. 调用智能体处理
        start_time = time.time()
        
        if not self.agent:
            return {
                "status": "error",
                "error": "智能体未注册",
                "request_id": request_id
            }
        
        # 简单的输入解析（实际应用可让LLM做）
        # 这里实现一个简单的规则解析
        parsed = self._parse_input(user_input)
        
        result = self.agent.process(
            command=parsed["command"],
            params=parsed["params"],
            session_id=valid_session_id
        )
        
        elapsed = time.time() - start_time
        
        # 5. 记录响应
        print(f"[网关层] 处理完成，耗时: {elapsed:.2f}秒")
        print(f'[网关层] 响应: {result.get("output", "")[:50]}...')
        
        # 6. 返回结果
        return {
            "status": "success",
            "request_id": request_id,
            "session_id": valid_session_id,
            "processing_time": elapsed,
            **result  # 合并智能体的返回结果
        }
    
    def _parse_input(self, user_input: str) -> Dict[str, Any]:
        """
        简化的输入解析器
        
        参数:
            user_input: 原始用户输入
            
        返回:
            解析后的命令和参数
        """
        user_input = user_input.strip()
        
        # 问候命令
        if "你好" in user_input or "hello" in user_input.lower():
            # 提取可能的名字
            parts = user_input.split()
            name = parts[-1] if len(parts) > 1 and parts[-1] not in ["你好", "hello"] else None
            
            return {
                "command": "greet",
                "params": {"name": name} if name else {}
            }
        
        # 记住用户命令
        elif "记住" in user_input:
            name = user_input.replace("记住", "").strip()
            return {
                "command": "greet",
                "params": {"name": name, "remember_me": True}
            }
        
        # 文件操作命令（扩展示例）
        elif "保存" in user_input and "文件" in user_input:
            content = user_input.replace("保存到文件", "").replace("保存文件", "").strip()
            return {
                "command": "file",
                "params": {"action": "save", "content": content}
            }
        
        # 未知命令
        else:
            return {
                "command": "unknown",
                "params": {"text": user_input}
            }
    
    def get_stats(self) -> Dict[str, Any]:
        """获取网关统计信息"""
        return {
            "total_requests": self.request_count,
            "active_sessions": len(self.sessions),
            "sessions": {
                sid: {
                    "age": time.time() - data["created_at"],
                    "requests": data["request_count"]
                }
                for sid, data in self.sessions.items()
            }
        }