# core/agent.py
"""
智能体层 - 核心决策单元
"""
import importlib.util
import os
import yaml
from typing import Dict, Any, List, Optional
from .memory import Memory

class Agent:
    """
    智能体
    职责：
    1. 加载和管理技能
    2. 接收网关的命令
    3. 调用合适的技能执行
    4. 与记忆层交互
    """
    
    def __init__(self, config_file: str):
        """
        初始化智能体
        
        参数:
            config_file: 配置文件路径
        """
        self.name = "FishClaw"
        self.description = "一个可扩展的AI智能体"
        self.skills = {}
        self.memory = None
        
        # 加载配置
        self.config = self._load_config(config_file)
        
        # 初始化记忆层
        memory_config = self.config.get("memory", {})
        self.memory = Memory(memory_config.get("path", "./memory"))
        
        # 加载技能
        self._load_skills()
        
        print(f"[智能体层] 初始化完成: {self.name}")
        print(f"[智能体层] 已加载 {len(self.skills)} 个技能: {list(self.skills.keys())}")
    
    def _load_config(self, config_file: str) -> Dict:
        """加载YAML配置文件"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            print(f"[智能体层] 配置文件 {config_file} 不存在，使用默认配置")
            return {"skills": []}
    
    def _load_skills(self):
        """加载所有启用的技能"""
        skills_config = self.config.get("skills", [])
        
        for skill_config in skills_config:
            if not skill_config.get("enabled", True):
                continue
            
            try:
                # 动态导入技能模块
                skill_path = skill_config["path"]
                skill_name = skill_config["name"]
                
                # 检查文件是否存在
                if not os.path.exists(skill_path):
                    print(f"[智能体层] 警告: 技能文件不存在 {skill_path}")
                    continue
                
                # 动态加载模块
                spec = importlib.util.spec_from_file_location(skill_name, skill_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # 创建技能实例（要求模块有create_skill函数）
                if hasattr(module, 'create_skill'):
                    skill = module.create_skill()
                    self.skills[skill_name] = skill
                    print(f"[智能体层] 加载技能: {skill_name} - {skill.description}")
                else:
                    print(f"[智能体层] 警告: 技能 {skill_name} 没有 create_skill 函数")
                    
            except Exception as e:
                print(f"[智能体层] 错误: 加载技能 {skill_config.get('name')} 失败: {e}")
    
    def process(self, command: str, params: Dict, session_id: str) -> Dict[str, Any]:
        """
        处理来自网关的命令
        
        参数:
            command: 命令名称
            params: 命令参数
            session_id: 会话ID
            
        返回:
            处理结果
        """
        print(f"[智能体层] 处理命令: {command}")
        print(f"[智能体层] 参数: {params}")
        print(f"[智能体层] 会话: {session_id}")
        
        # 1. 查询会话记忆
        session_data = self.memory.get_session(session_id)
        print(f"[智能体层] 会话历史: {len(session_data.get('history', []))} 条记录")
        
        # 2. 根据命令调用相应的技能
        if command == "greet":
            result = self._execute_skill("greeting", params, session_id)
        elif command == "file":
            result = self._execute_skill("file", params, session_id)
        elif command == "unknown":
            result = {
                "status": "error",
                "output": f"抱歉，我不理解 '{params.get('text', '')}'，请换个说法试试"
            }
        else:
            result = {
                "status": "error",
                "output": f"未知命令: {command}"
            }
        
        # 3. 记录到对话历史
        self.memory.add_to_history(session_id, "user", str(params))
        self.memory.add_to_history(session_id, "assistant", result.get("output", ""))
        
        return result
    
    def _execute_skill(self, skill_name: str, params: Dict, session_id: str) -> Dict[str, Any]:
        """
        执行指定的技能
        
        参数:
            skill_name: 技能名称
            params: 技能参数
            session_id: 会话ID
        """
        if skill_name not in self.skills:
            return {
                "status": "error",
                "output": f"技能 {skill_name} 不存在"
            }
        
        try:
            skill = self.skills[skill_name]
            
            # 给技能传入记忆对象（如果技能需要）
            if hasattr(skill, 'set_memory'):
                skill.set_memory(self.memory)
            
            # 执行技能
            result = skill.execute(params)
            
            # 确保结果包含必要字段
            if "output" not in result:
                result["output"] = str(result.get("result", "执行完成"))
            
            return result
            
        except Exception as e:
            print(f"[智能体层] 技能执行错误: {e}")
            return {
                "status": "error",
                "output": f"执行技能时出错: {str(e)}"
            }
    
    def get_available_skills(self) -> List[Dict]:
        """获取所有可用技能的信息"""
        return [
            {
                "name": name,
                "info": skill.get_skill_info()
            }
            for name, skill in self.skills.items()
        ]