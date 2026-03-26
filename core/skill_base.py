# core/skill_base.py
"""
技能基类 - 所有技能都必须继承这个类
"""
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseSkill(ABC):
    """技能抽象基类"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """技能名称"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """技能描述"""
        pass
    
    @abstractmethod
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行技能的核心方法
        
        参数:
            params: 技能参数字典
            
        返回:
            包含执行结果的字典，必须包含status字段
        """
        pass
    
    def get_skill_info(self) -> Dict[str, Any]:
        """获取技能信息（可被子类重写）"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {}  # 可定义参数规范
        }