"""
Claude Agent SDK + MinerU Skill 发票解析示例
使用 Skills 功能,支持线上 PDF URL
"""
import asyncio
import os
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    # 线上 PDF URL
    pdf_url = "http://github.com/nilecui/mineru-parser/blob/main/demo.pdf"
    
    # 验证 API 密钥
    api_key = os.getenv("MINERU_API_KEY")
    if not api_key:
        print("❌ 错误: 未设置 MINERU_API_KEY 环境变量")
        print("请运行: export MINERU_API_KEY='your_api_key'")
        return
    
    # ✅ 修正后的配置
    options = ClaudeAgentOptions(
        cwd=".",
        
        # ✅ 关键:加载文件系统中的 skills
        setting_sources=["user", "project"],  # 加载用户和项目 skills
        
        # ✅ 允许必要的工具,包括 Skill
        allowed_tools=[
            "Skill",          # 必须包含以启用 Skills
            "view",
            "create_file",
            "str_replace",
        ],
        
        # 自动接受所有操作
        permission_mode="bypassPermissions",
    )
    
    print("\n" + "="*70)
    print("🚀 Claude Agent SDK + MinerU Skill 发票解析")
    print("="*70)
    print(f"📋 PDF URL: {pdf_url[:80]}...")
    print(f"🔑 API Key: {'*' * 20}{api_key[-10:]}")
    print(f"📁 工作目录: {options.cwd}")
    print(f"🔐 权限模式: {options.permission_mode}")
    print(f"📚 Skills 来源: {options.setting_sources}")
    print("="*70 + "\n")
    
    # 构建提示词 - 让 Claude 使用 mineru-parser skill
    prompt = f"""
请使用 **mineru-parser skill** 解析以下发票 PDF 并提取结构化信息。

**PDF URL:**
{pdf_url}

**提取以下发票信息:**
- 📋 **基本信息**: 发票代码、发票号码、开票日期
- 🏢 **购买方**: 名称、纳税人识别号、地址电话、开户行及账号
- 🏭 **销售方**: 名称、纳税人识别号、地址电话、开户行及账号
- 💰 **商品明细**: 名称、规格型号、单位、数量、单价、金额
- 📊 **税额信息**: 税率、税额
- 💵 **价税合计**: 大写金额、小写金额
- ✍️ **签章信息**: 收款人、复核、开票人

**输出要求:**
- 使用清晰的 Markdown 表格展示结构化数据
- 对关键金额和日期进行突出显示
- 保存解析后的完整 Markdown 到本地文件

请开始执行解析任务!
"""
    
    try:
        print("🔄 正在处理,请稍候...\n")
        print("="*70)
        message_count = 0
        
        async for message in query(prompt=prompt, options=options):
            message_count += 1
            print(f"\n📨 消息 #{message_count}")
            print("-" * 70)
            print(message)
        
        print("\n" + "="*70)
        print(f"✅ 处理完成!共收到 {message_count} 条消息")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ 错误: {type(e).__name__}")
        print(f"详情: {str(e)}")
        print("\n💡 可能的解决方案:")
        print("1. 检查 MINERU_API_KEY 环境变量是否设置正确")
        print("2. 确认 PDF URL 可以访问")
        print("3. 验证 mineru-parser skill 已安装在 .claude/skills/")
        print("4. 检查网络连接")
        import traceback
        print(f"\n堆栈信息:\n{traceback.format_exc()}")


async def test_skill_availability():
    """测试 mineru-parser skill 是否可用"""
    print("🔍 检查 mineru-parser skill 可用性...\n")
    
    options = ClaudeAgentOptions(
        cwd=".",
        setting_sources=["user", "project"],  # ✅ 加载 skills
        allowed_tools=["Skill", "view"],
        permission_mode="bypassPermissions",
    )
    
    test_prompt = """
请检查可用的 skills 并确认 mineru-parser skill 是否存在。
如果存在,请说明它的功能和使用方法。
"""
    
    try:
        async for message in query(prompt=test_prompt, options=options):
            print(message)
        print("\n✅ mineru-parser skill 检查完成!")
    except Exception as e:
        print(f"\n❌ Skill 检查失败: {e}")


if __name__ == "__main__":
    import sys
    
    # 支持命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            asyncio.run(test_skill_availability())
        elif sys.argv[1] == "--help":
            print("用法:")
            print("  python invoice_parser_skill.py          # 运行发票解析")
            print("  python invoice_parser_skill.py --test   # 测试 skill 可用性")
            print("  python invoice_parser_skill.py --help   # 显示帮助")
            print("\n环境变量:")
            print("  MINERU_API_KEY - MinerU API 密钥(必需)")
            print("\n示例:")
            print("  export MINERU_API_KEY='your_api_key'")
            print("  python invoice_parser_skill.py")
    else:
        asyncio.run(main())