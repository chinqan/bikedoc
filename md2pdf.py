#!/usr/bin/env python3
"""
Markdown 轉 PDF 工具
使用 md-to-pdf (npx) 將 Markdown 檔案轉換為精美的 PDF。
支援中文字體 (Noto Sans TC)、表格樣式、圖片嵌入。

用法：
    python md2pdf.py                          # 轉換同目錄下的 .md 檔案（僅一個時自動選取）
    python md2pdf.py 會議記錄.md              # 指定檔案
    python md2pdf.py 會議記錄.md -o output.pdf  # 指定輸出檔名
"""

import subprocess
import sys
import os
import glob
import argparse


# ── 樣式設定 ──────────────────────────────────────────────

GOOGLE_FONT_URL = "https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700&display=swap"

CSS = """
body {
    font-family: 'Noto Sans TC', sans-serif;
    font-size: 13px;
    line-height: 1.75;
    color: #222;
    max-width: 700px;
    margin: 0 auto;
}
h1 {
    text-align: center;
    font-size: 22px;
    color: #1a5276;
    border-bottom: 3px solid #2980b9;
    padding-bottom: 10px;
    margin-bottom: 24px;
}
h2 {
    font-size: 15px;
    color: #2c3e50;
    border-left: 4px solid #2980b9;
    padding-left: 10px;
    margin-top: 20px;
    margin-bottom: 8px;
}
h3 {
    font-size: 14px;
    color: #2c3e50;
    margin-top: 16px;
    margin-bottom: 6px;
}
hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 14px 0;
}
ul {
    padding-left: 22px;
    margin: 6px 0;
}
li {
    margin-bottom: 4px;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
    font-size: 12.5px;
}
th {
    background-color: #2980b9;
    color: white;
    padding: 7px 10px;
    text-align: left;
    font-weight: 600;
}
td {
    padding: 6px 10px;
    border-bottom: 1px solid #e0e0e0;
}
tr:nth-child(even) td {
    background-color: #f7f9fc;
}
blockquote {
    background: #fef9e7;
    border-left: 4px solid #f39c12;
    padding: 10px 14px;
    margin: 10px 0;
    font-size: 12.5px;
    color: #7d6608;
}
strong {
    color: #1a5276;
}
a {
    color: #2980b9;
    text-decoration: none;
    font-weight: 600;
}
a:hover {
    text-decoration: underline;
}
img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 12px auto;
    border: 1px solid #ddd;
    border-radius: 6px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
""".strip().replace("\n", "")

PDF_OPTIONS = '{"format":"A4","margin":{"top":"20mm","bottom":"20mm","left":"18mm","right":"18mm"}}'


# ── 主程式 ────────────────────────────────────────────────

def find_md_file(directory: str) -> str | None:
    """自動尋找目錄中的 .md 檔案，僅一個時自動回傳。"""
    md_files = glob.glob(os.path.join(directory, "*.md"))
    if len(md_files) == 1:
        return md_files[0]
    elif len(md_files) == 0:
        return None
    else:
        print("📂 找到多個 .md 檔案，請指定要轉換的檔案：")
        for i, f in enumerate(md_files, 1):
            print(f"   {i}. {os.path.basename(f)}")
        return None


def convert(md_path: str, output_path: str | None = None) -> bool:
    """將 Markdown 檔案轉換為 PDF。"""
    md_path = os.path.abspath(md_path)
    basedir = os.path.dirname(md_path)

    if not os.path.exists(md_path):
        print(f"❌ 找不到檔案：{md_path}")
        return False

    print(f"📄 來源：{os.path.basename(md_path)}")

    cmd = [
        "npx", "-y", "md-to-pdf", md_path,
        "--basedir", basedir,
        "--stylesheet", GOOGLE_FONT_URL,
        "--css", CSS,
        "--pdf-options", PDF_OPTIONS,
    ]

    try:
        result = subprocess.run(cmd, cwd=basedir, capture_output=True, text=True)

        # 預設輸出為同名 .pdf
        default_pdf = md_path.rsplit(".", 1)[0] + ".pdf"

        if result.returncode == 0 and os.path.exists(default_pdf):
            # 如果指定了輸出路徑，搬移檔案
            if output_path:
                output_path = os.path.abspath(output_path)
                os.rename(default_pdf, output_path)
                final_path = output_path
            else:
                final_path = default_pdf

            size_kb = os.path.getsize(final_path) / 1024
            size_str = f"{size_kb:.0f} KB" if size_kb < 1024 else f"{size_kb / 1024:.1f} MB"
            print(f"✅ PDF 生成成功！")
            print(f"📎 檔案：{final_path}")
            print(f"📦 大小：{size_str}")
            return True
        else:
            print(f"❌ 轉換失敗")
            if result.stderr:
                print(result.stderr)
            return False

    except FileNotFoundError:
        print("❌ 找不到 npx 指令，請確認已安裝 Node.js")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Markdown 轉 PDF 工具（中文友善、精美排版）"
    )
    parser.add_argument(
        "input", nargs="?", default=None,
        help="要轉換的 .md 檔案路徑（省略則自動偵測）"
    )
    parser.add_argument(
        "-o", "--output", default=None,
        help="輸出 PDF 檔案路徑（預設為同名 .pdf）"
    )
    args = parser.parse_args()

    # 決定輸入檔案
    if args.input:
        md_path = args.input
    else:
        md_path = find_md_file(os.getcwd())
        if not md_path:
            print("💡 用法：python md2pdf.py <檔案.md>")
            sys.exit(1)

    success = convert(md_path, args.output)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
