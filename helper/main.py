import os
import re
import sys
import subprocess
from datetime import datetime

# 杂志配置信息
MAGZINES = {
    "ny": {
        "id": "ny",
        "name": "The New Yorker Magazine",
        "recipe": "The New Yorker Magazine",
        "folder": "the_new_yorker",
        "date_regex": r"magazine/\K\d{4}/\d{2}/\d{2}", # 从日志提取
    },
    "te": {
        "id": "te",
        "name": "The Economist",
        "recipe": "The Economist",
        "folder": "the_economist",
        "date_regex": r"images/\K(\d{8})", # 从日志提取
    },
    "tm": {
        "id": "tm",
        "name": "TIME Magazine",
        "recipe": "TIME Magazine",
        "folder": "time_magzine",
        "date_regex": r"TIM\K(\d{6})", # 从日志提取
    }
}

BOOKS_DIR = "converted_ebooks"

def extract_date_from_output(output, mag_id):
    config = MAGZINES[mag_id]
    regex = config.get("date_regex")
    if not regex:
        return None
    
    # 查找匹配项
    # Note: re doesn't support \K, so we adapt
    if mag_id == "ny":
        match = re.search(r"magazine/(\d{4})/(\d{2})/(\d{2})", output)
        if match:
            return "".join(match.groups())
    elif mag_id == "te":
        match = re.search(r"images/(\d{8})", output)
        if match:
            return match.group(1)
    elif mag_id == "tm":
        match = re.search(r"TIM(\d{6})", output)
        if match:
            return f"20{match.group(1)}"
            
    return None

def extract_date_from_file(filename):
    # 通用的文件名日期提取: [Month DD, YYYY] 或 [Month DD]
    match = re.search(r"\[([A-Za-z]+)\s(\d{1,2})(?:st|nd|rd|th)?(?:,\s(\d{4}))?\]", filename)
    if match:
        month_str, day, year = match.groups()
        try:
            month = datetime.strptime(month_str[:3], "%b").month
        except:
            return None
        
        if not year:
            year = datetime.now().year
            
        return f"{year}{int(month):02d}{int(day):02d}"
    return None

def run_command(args):
    print(f"Running: {' '.join(args)}")
    # 改用 Popen 实现流式输出日志，防止长时间卡顿
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    full_output = []
    if process.stdout:
        for line in process.stdout:
            print(line, end="") # 实时流式输出
            full_output.append(line)
    process.wait()
    return "".join(full_output), process.returncode

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <mag_id>")
        sys.exit(1)

    mag_id = sys.argv[1]
    if mag_id not in MAGZINES:
        print(f"Unknown magazine: {mag_id}")
        sys.exit(1)

    config = MAGZINES[mag_id]
    recipe = config["recipe"]
    
    if not os.path.exists(BOOKS_DIR):
        os.makedirs(BOOKS_DIR)

    # 1. 运行转换
    print(f"--- Fetching {config['name']} ---")
    raw_epub = "temp_output.epub"
    convert_output, code = run_command(["ebook-convert", f"{recipe}.recipe", raw_epub])
    
    if code != 0 or not os.path.exists(raw_epub):
        print("Conversion failed.")
        sys.exit(1)

    # 2. 确定日期
    date_str = extract_date_from_output(convert_output, mag_id)
    if not date_str:
        # 尝试从文件名/元数据提取
        date_str = extract_date_from_file(raw_epub)
    
    if not date_str:
        # 最后兜底使用当前日期
        date_str = datetime.now().strftime("%Y%m%d")
        print(f"Warning: Could not extract date, using current: {date_str}")
    
    print(f"Publication Date: {date_str}")

    # 3. 重命名与目录组织
    base_name = f"{date_str} - {config['name']}"
    target_dir = os.path.join(BOOKS_DIR, date_str)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    final_epub = os.path.join(target_dir, f"{base_name}.epub")
    final_pdf = os.path.join(target_dir, f"{base_name}.pdf")
    cover_jpg = os.path.join(target_dir, "cover.jpg")

    os.rename(raw_epub, final_epub)

    # 4. 提取封面
    run_command(["ebook-meta", final_epub, f"--get-cover={cover_jpg}"])

    # 5. 转换为 PDF
    print(f"Converting to PDF...")
    run_command(["ebook-convert", final_epub, final_pdf])

    # 6. 设置环境变量给 GitHub Actions
    if "GITHUB_ENV" in os.environ:
        with open(os.environ["GITHUB_ENV"], "a") as f:
            f.write(f"DATE={date_str}\n")
            f.write(f"MAG_FOLDER={config['folder']}\n")
            f.write(f"MAG_NAME={config['name']}\n")

    print(f"Success! Files saved in {target_dir}")

if __name__ == "__main__":
    main()
