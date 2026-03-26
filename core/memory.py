# core/memory.py
"""
记忆层 - 负责短期会话记忆和长期用户偏好
"""
import os
import json
from typing import Dict, Any, Optional
from datetime import datetime

class Memory:
    """
    记忆管理器
    职责：
    1. 短期记忆：按会话ID存储对话历史
    2. 长期记忆：存储用户偏好，跨会话持久化
    """
    
    def __init__(self, memory_path: str = "./memory"):
        """
        初始化记忆管理器
        
        参数:
            memory_path: 记忆文件存储路径
        """
        self.memory_path = memory_path
        self.short_term = {}  # 短期记忆（内存缓存）
        self.long_term = {}   # 长期记忆（会持久化）
        
        # 创建记忆目录
        os.makedirs(memory_path, exist_ok=True)
        os.makedirs(os.path.join(memory_path, "sessions"), exist_ok=True)
        
        # 加载长期记忆
        self._load_long_term_memory()
        
        print(f"[记忆层] 初始化完成，存储路径: {memory_path}")
    
    def _load_long_term_memory(self):
        """加载长期记忆文件"""
        long_term_file = os.path.join(self.memory_path, "long_term.json")
        if os.path.exists(long_term_file):
            try:
                with open(long_term_file, 'r', encoding='utf-8') as f:
                    self.long_term = json.load(f)
                print(f"[记忆层] 加载长期记忆: {len(self.long_term)} 条记录")
            except:
                self.long_term = {}
    
    def _save_long_term_memory(self):
        """保存长期记忆到文件"""
        long_term_file = os.path.join(self.memory_path, "long_term.json")
        with open(long_term_file, 'w', encoding='utf-8') as f:
            json.dump(self.long_term, f, ensure_ascii=False, indent=2)
    
    def get_session(self, session_id: str) -> Dict[str, Any]:
        """
        获取会话的短期记忆
        
        参数:
            session_id: 会话ID
            
        返回:
            会话记忆字典
        """
        # 先查内存缓存
        if session_id in self.short_term:
            return self.short_term[session_id]
        
        # 再查磁盘文件
        session_file = os.path.join(self.memory_path, "sessions", f"{session_id}.json")
        if os.path.exists(session_file):
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                    self.short_term[session_id] = session_data
                    return session_data
            except:
                pass
        
        # 返回空会话
        return {"history": [], "created_at": datetime.now().isoformat()}
    
    def save_session(self, session_id: str, data: Dict[str, Any]):
        """
        保存会话记忆
        
        参数:
            session_id: 会话ID
            data: 要保存的数据
        """
        # 更新内存缓存
        self.short_term[session_id] = data
        
        # 保存到磁盘
        session_file = os.path.join(self.memory_path, "sessions", f"{session_id}.json")
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """
        获取用户长期偏好
        
        参数:
            key: 偏好键名
            default: 默认值
        """
        return self.long_term.get(key, default)
    
    def set_preference(self, key: str, value: Any):
        """
        设置用户长期偏好
        
        参数:
            key: 偏好键名
            value: 偏好值
        """
        self.long_term[key] = value
        self._save_long_term_memory()
        print(f"[记忆层] 长期记忆已更新: {key}={value}")
    
    def add_to_history(self, session_id: str, role: str, content: str):
        """
        添加一条对话历史
        
        参数:
            session_id: 会话ID
            role: 角色 (user/assistant)
            content: 内容
        """
        session = self.get_session(session_id)
        if "history" not in session:
            session["history"] = []
        
        session["history"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # 保持历史记录在合理范围内
        if len(session["history"]) > 50:
            session["history"] = session["history"][-50:]
        
        self.save_session(session_id, session)