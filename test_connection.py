#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Photoshop MCP Server 连接测试脚本.

运行此脚本以验证 Photoshop MCP Server 是否正确安装并可连接到 Photoshop。

使用方法:
    python test_connection.py
    python test_connection.py --verbose
"""

import sys
import argparse
import io

# 设置标准输出编码为 UTF-8
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def print_header(title: str) -> None:
    """打印标题头."""
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)


def print_result(name: str, success: bool, detail: str = "") -> None:
    """打印测试结果."""
    status = "[OK] " if success else "[FAIL]"
    print(f"  {name}: {status}")
    if detail:
        print(f"    -> {detail}")


def test_module_import() -> tuple[bool, str]:
    """测试模块导入."""
    try:
        from photoshop_mcp_server.server import create_server
        from photoshop_mcp_server.app import __version__
        return True, f"版本 {__version__}"
    except ImportError as e:
        return False, str(e)


def test_server_creation() -> tuple[bool, str]:
    """测试服务器创建."""
    try:
        from photoshop_mcp_server.server import create_server
        server = create_server()
        return True, "FastMCP 服务器创建成功"
    except Exception as e:
        return False, str(e)


def test_photoshop_connection() -> tuple[bool, str]:
    """测试 Photoshop 连接."""
    try:
        from photoshop_mcp_server.ps_adapter.application import PhotoshopApp
        ps = PhotoshopApp()
        version = ps.get_version()
        return True, f"Photoshop 版本: {version}"
    except Exception as e:
        return False, f"请确保 Photoshop 已启动 ({e})"


def test_active_document() -> tuple[bool, str]:
    """测试获取活动文档."""
    try:
        from photoshop_mcp_server.ps_adapter.application import PhotoshopApp
        ps = PhotoshopApp()
        doc = ps.get_active_document()
        if doc:
            return True, f"活动文档: {doc.name}"
        return True, "无活动文档（正常）"
    except Exception as e:
        return False, str(e)


def test_registered_tools(verbose: bool = False) -> tuple[bool, list[str]]:
    """测试已注册的工具."""
    try:
        from photoshop_mcp_server.registry import register_all_tools
        from mcp.server.fastmcp import FastMCP

        server = FastMCP("test")
        registered = register_all_tools(server)

        tools = []
        for module_name, tool_names in registered.items():
            tools.extend(tool_names)

        return True, tools
    except Exception as e:
        return False, [str(e)]


def main():
    """运行所有测试."""
    parser = argparse.ArgumentParser(description="测试 Photoshop MCP Server 连接")
    parser.add_argument("-v", "--verbose", action="store_true", help="显示详细信息")
    args = parser.parse_args()

    print("\n[Photoshop MCP Server 连接测试]")
    print("-" * 50)

    all_passed = True

    # 测试 1: 模块导入
    print_header("1. 模块导入测试")
    success, detail = test_module_import()
    print_result("模块导入", success, detail)
    all_passed = all_passed and success

    # 测试 2: 服务器创建
    print_header("2. 服务器创建测试")
    success, detail = test_server_creation()
    print_result("服务器创建", success, detail)
    all_passed = all_passed and success

    # 测试 3: Photoshop 连接
    print_header("3. Photoshop 连接测试")
    success, detail = test_photoshop_connection()
    print_result("Photoshop 连接", success, detail)
    all_passed = all_passed and success

    # 测试 4: 活动文档
    print_header("4. 活动文档测试")
    success, detail = test_active_document()
    print_result("获取活动文档", success, detail)
    all_passed = all_passed and success

    # 测试 5: 已注册工具
    print_header("5. 已注册工具测试")
    success, tools = test_registered_tools(args.verbose)
    print_result("工具注册", success, f"共 {len(tools)} 个工具")
    if args.verbose or success:
        for tool in tools:
            print(f"    - {tool}")

    # 总结
    print_header("测试总结")
    if all_passed:
        print("  [OK] 所有测试通过! MCP 服务器已准备就绪。")
        print("\n  启动服务器命令:")
        print("    photoshop-mcp-server")
        print("\n  或配置到 MCP 客户端:")
        print('    {"command": "photoshop-mcp-server", "args": []}')
    else:
        print("  [FAIL] 部分测试失败，请检查上述错误信息。")
        print("\n  常见问题:")
        print("    1. 确保已安装依赖: pip install -e .")
        print("    2. 确保 Photoshop 已启动")
        print("    3. 确保运行在 Windows 系统上")
    print()

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
