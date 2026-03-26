# skills/greeting_skill.py
"""
问候技能 - 展示技能的基本结构和记忆交互
"""
import datetime
from typing import Dict, Any

class GreetingSkill:
    """问候技能"""
    
    def __init__(self):
        self.name = "greeting"
        self.description = "根据时间和用户偏好返回个性化问候"
        self.version = "1.0.0"
        self.memory = None  # 会在执行前由Agent注入
        
        print(f"[技能] 初始化: {self.name}")
    
    def set_memory(self, memory):
        """注入记忆对象"""
        self.memory = memory
    
    def _get_time_based_greeting(self) -> str:
        """根据当前时间返回问候语"""
        hour = datetime.datetime.now().hour
        
        if 5 <= hour < 12:
            return "早上好"
        elif 12 <= hour < 14:
            return "中午好"
        elif 14 <= hour < 18:
            return "下午好"
        else:
            return "晚上好"
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行问候技能
        
        参数格式:
            - name: 用户名 (可选)
            - remember_me: 是否记住用户 (可选)
        """
        try:
            # 1. 从参数或记忆中获取用户名
            user_name = params.get('name')
            
            # 如果没有提供名字，尝试从记忆读取
            if not user_name and self.memory:
                user_name = self.memory.get_preference('user_name')
            
            # 如果还没有，使用默认值
            if not user_name:
                user_name = '朋友'
            
            # 2. 获取时间问候
            time_greeting = self._get_time_based_greeting()
            
            # 3. 如果需要记住用户
            memory_note = ""
            if params.get('remember_me', False) and self.memory:
                self.memory.set_preference('user_name', user_name)
                memory_note = "（已将您记住）"
            
            # 4. 获取问候风格偏好
            style = '友好'  # 默认风格
            if self.memory:
                style = self.memory.get_preference('greeting_style', '友好')
            
            # 5. 根据风格生成问候
            if style == '正式':
                greeting = f"{time_greeting}，{user_name}先生/女士。很高兴为您服务。{memory_note}"
            else:
                greeting = f"{time_greeting}呀，{user_name}！今天过得怎么样？{memory_note}"
            
            # 6. 返回结果
            return {
                "status": "success",
                "output": greeting,
                "metadata": {
                    "skill": self.name,
                    "time": datetime.datetime.now().isoformat(),
                    "user": user_name,
                    "remembered": params.get('remember_me', False)
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "output": f"生成问候时出错: {str(e)}"
            }
    
    def get_skill_info(self) -> Dict[str, Any]:
        """返回技能信息"""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "parameters": {
                "name": {
                    "type": "string",
                    "description": "用户名称",
                    "required": False
                },
                "remember_me": {
                    "type": "boolean",
                    "description": "是否记住用户",
                    "required": False
                }
            }
        }

# 技能工厂函数 - Agent通过这个创建技能实例
def create_skill():
    return GreetingSkill()