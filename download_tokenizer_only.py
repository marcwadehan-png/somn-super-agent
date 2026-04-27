"""
下载正确的Gemma4 tokenizer到本地目录
"""
import os
import sys

# 目标目录
target_dir = r"d:\AI\somn\models\gemma4-local-b"
os.makedirs(target_dir, exist_ok=True)

from huggingface_hub import snapshot_download

model_id = "google/gemma-4-2b-it"

print(f"正在下载 tokenizer 文件...")
local_path = snapshot_download(
    repo_id=model_id,
    allow_patterns=["tokenizer.json", "tokenizer_config.json"],
    local_dir=target_dir,
    local_dir_use_symlinks=False
)
print(f"下载完成: {local_path}")
