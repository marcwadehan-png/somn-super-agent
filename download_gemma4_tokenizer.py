"""
下载正确的Gemma4 tokenizer
"""
import os
import sys

# 安装必要的包
os.system(f'"{sys.executable}" -m pip install huggingface_hub -q')

from huggingface_hub import snapshot_download

model_id = "google/gemma-4-2b-it"

print(f"正在从HuggingFace下载Gemma4 tokenizer...")
print(f"模型: {model_id}")

try:
    # 只下载tokenizer相关文件
    local_dir = snapshot_download(
        repo_id=model_id,
        allow_patterns=[
            "tokenizer.json",
            "tokenizer_config.json",
            "*.vocab",
            "spiece.model",
            "tokenizer.model",
        ],
        local_dir=None,
        local_dir_use_symlinks=False
    )
    print(f"下载完成！目录: {local_dir}")
except Exception as e:
    print(f"下载失败: {e}")
    print("\n尝试备用方案...")

    # 备用：从google/gemma-3-4b-it 下载（如果上述失败）
    backup_model_id = "google/gemma-3-4b-it"
    try:
        local_dir = snapshot_download(
            repo_id=backup_model_id,
            allow_patterns=[
                "tokenizer.json",
                "tokenizer_config.json",
            ],
            local_dir_use_symlinks=False
        )
        print(f"备用下载完成！目录: {local_dir}")
    except Exception as e2:
        print(f"备用也失败: {e2}")
