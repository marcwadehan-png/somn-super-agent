"""
Somn 包入口 - 支持 python -m smart_office_assistant.src 调用
"""

try:
    from smart_office_assistant.somn_cli import main
except ImportError:
    try:
        from somn_cli import main
    except ImportError:
        import sys
        print("Error: somn_cli not found. Run from project root or install package.")
        sys.exit(1)

if __name__ == "__main__":
    main()
