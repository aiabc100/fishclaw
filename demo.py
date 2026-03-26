# demo.py
"""
OpenClaw 演示程序
运行这个文件可以看到完整的智能体工作流程
"""

import os
import sys
from core.gateway import Gateway
from core.agent import Agent

def print_banner():
    """打印欢迎信息"""
    banner = """
╔══════════════════════════════════════════════════════════╗
║                   FishClaw 演示                          ║
║              手搓一个AI智能体框架                         ║
╚══════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_help():
    """打印帮助信息"""
    help_text = """
 可用命令:
  - 你好 [名字]          : 打个招呼（如: 你好 张三）
  - 记住 [名字]          : 让AI记住你的名字（如: 记住李四）
  - 保存到文件 [内容]     : 保存内容到文件（如: 保存到文件 这是一段笔记）
  - 列出文件             : 查看已保存的文件
  - 帮助                 : 显示此帮助
  - 退出                 : 退出程序

 提示: AI会记住你的偏好，下次打招呼时会自动使用记住的名字
    """
    print(help_text)

def main():
    """主函数"""
    # 打印欢迎信息
    print_banner()
    
    # 确保当前目录在Python路径中
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    print("[系统] 正在启动 OpenClaw...")
    print("[系统] 创建必要的目录")
    
    # 创建必要的目录
    os.makedirs("./memory/sessions", exist_ok=True)
    os.makedirs("./output", exist_ok=True)
    os.makedirs("./skills", exist_ok=True)
    
    try:
        # 1. 初始化网关
        print("\n[系统] 1. 初始化网关层")
        gateway = Gateway()
        
        # 2. 初始化智能体
        print("\n[系统] 2. 初始化智能体层")
        agent = Agent("config.yaml")
        
        # 3. 注册智能体到网关
        print("\n[系统] 3. 注册智能体")
        gateway.register_agent(agent)
        
        # 4. 显示帮助
        print_help()
        
        # 5. 交互循环
        print("\n" + "="*50)
        print("开始对话 (输入 '退出' 结束)")
        print("="*50)
        
        session_id = None  # 第一次请求时会自动创建
        
        while True:
            try:
                # 获取用户输入
                user_input = input("\n 你: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['退出', 'exit', 'quit', 'q']:
                    print("\n 再见！")
                    break
                
                if user_input.lower() in ['帮助', 'help', '?']:
                    print_help()
                    continue
                
                # 处理请求
                result = gateway.handle_request(user_input, session_id)
                
                # 更新会话ID（如果是新会话）
                if 'session_id' in result:
                    session_id = result['session_id']
                
                # 显示响应
                if result['status'] == 'success':
                    print(f"\n AI: {result.get('output', '处理完成')}")
                    
                    # 如果有额外信息，显示出来
                    if 'metadata' in result:
                        print(f"   [元数据] {result['metadata']}")
                else:
                    print(f"\n❌ 错误: {result.get('error', '未知错误')}")
                    
            except KeyboardInterrupt:
                print("\n\n 程序被中断")
                break
            except Exception as e:
                print(f"\n❌ 运行时错误: {e}")
        
        # 6. 显示统计信息
        print("\n" + "="*50)
        print(" 会话统计")
        print("="*50)
        stats = gateway.get_stats()
        print(f"总请求数: {stats['total_requests']}")
        print(f"活跃会话: {stats['active_sessions']}")
        
        # 7. 查看记忆内容
        print("\n" + "="*50)
        print(" 记忆层内容")
        print("="*50)
        
        # 显示长期记忆
        long_term_file = "./memory/long_term.json"
        if os.path.exists(long_term_file):
            import json
            with open(long_term_file, 'r', encoding='utf-8') as f:
                long_term = json.load(f)
                if long_term:
                    print("长期记忆:")
                    for key, value in long_term.items():
                        print(f"  - {key}: {value}")
                else:
                    print("长期记忆为空")
        
        # 显示会话文件
        session_files = os.listdir("./memory/sessions")
        if session_files:
            print(f"\n会话文件 ({len(session_files)} 个):")
            for f in session_files[:5]:  # 只显示前5个
                print(f"  - {f}")
        
        print("\n✨ 演示结束！")
        
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()