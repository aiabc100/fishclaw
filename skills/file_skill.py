# skills/file_skill.py
"""
文件操作技能 - 展示如何扩展技能
"""
import os
from datetime import datetime
from typing import Dict, Any

class FileSkill:
    """文件操作技能"""
    
    def __init__(self):
        self.name = "file"
        self.description = "文件读写操作"
        self.version = "1.0.0"
        self.memory = None
        
        print(f"[技能] 初始化: {self.name}")
    
    def set_memory(self, memory):
        self.memory = memory
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行文件操作
        
        参数格式:
            - action: 操作类型 (save/read/list)
            - content: 要保存的内容 (save时)
            - filename: 文件名 (可选)
        """
        try:
            action = params.get('action')
            
            if action == 'save':
                return self._save_file(params)
            elif action == 'read':
                return self._read_file(params)
            elif action == 'list':
                return self._list_files()
            else:
                return {
                    "status": "error",
                    "output": f"不支持的操作: {action}"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "output": f"文件操作失败: {str(e)}"
            }
    
    def _save_file(self, params: Dict) -> Dict:
        """保存文件"""
        content = params.get('content', '')
        
        if not content:
            return {
                "status": "error",
                "output": "没有提供要保存的内容"
            }
        
        # 创建保存目录
        save_dir = "./output"
        os.makedirs(save_dir, exist_ok=True)
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = params.get('filename', f"note_{timestamp}.txt")
        filepath = os.path.join(save_dir, filename)
        
        # 保存文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 记录到记忆
        if self.memory:
            self.memory.set_preference('last_saved_file', filepath)
        
        return {
            "status": "success",
            "output": f"文件已保存: {filepath}",
            "filepath": filepath,
            "size": len(content)
        }
    
    def _read_file(self, params: Dict) -> Dict:
        """读取文件"""
        filename = params.get('filename')
        
        if not filename:
            return {
                "status": "error",
                "output": "请指定要读取的文件名"
            }
        
        if not os.path.exists(filename):
            return {
                "status": "error",
                "output": f"文件不存在: {filename}"
            }
        
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            "status": "success",
            "output": f"文件内容:\n{content[:200]}...",
            "content": content,
            "size": len(content)
        }
    
    def _list_files(self) -> Dict:
        """列出文件"""
        save_dir = "./output"
        if not os.path.exists(save_dir):
            return {
                "status": "success",
                "output": "输出目录不存在",
                "files": []
            }
        
        files = os.listdir(save_dir)
        file_list = "\n".join([f"  - {f}" for f in files])
        
        return {
            "status": "success",
            "output": f"输出目录中的文件:\n{file_list}",
            "files": files
        }
    
    def get_skill_info(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "parameters": {
                "action": {
                    "type": "string",
                    "description": "操作类型: save/read/list",
                    "required": True
                },
                "content": {
                    "type": "string",
                    "description": "要保存的内容",
                    "required": False
                },
                "filename": {
                    "type": "string",
                    "description": "文件名",
                    "required": False
                }
            }
        }

def create_skill():
    return FileSkill()