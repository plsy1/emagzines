import os
import shutil
import re

def archive_magazines():
    # 获取当前目录下所有的文件夹
    # 假设脚本在 magzines 分支的根目录下运行
    items = [d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.')]
    
    for mag_folder in items:
        # 跳过一些已知的非杂志目录
        if mag_folder in ['repo_magzines', 'helper', 'converted_ebooks']:
            continue
            
        print(f"Processing magazine folder: {mag_folder}")
        
        # 获取该杂志下的所有子目录
        issue_folders = [d for d in os.listdir(mag_folder) if os.path.isdir(os.path.join(mag_folder, d))]
        
        for issue in issue_folders:
            # 检查是否为 YYYYMMDD 格式 (8位数字)
            if re.match(r'^\d{8}$', issue):
                year = issue[:4]
                year_dir = os.path.join(mag_folder, year)
                
                # 创建年份目录
                if not os.path.exists(year_dir):
                    print(f"  Creating year directory: {year_dir}")
                    os.makedirs(year_dir)
                
                # 移动目录
                src = os.path.join(mag_folder, issue)
                dst = os.path.join(year_dir, issue)
                
                print(f"  Moving {src} -> {dst}")
                try:
                    shutil.move(src, dst)
                except Exception as e:
                    print(f"  Error moving {issue}: {e}")
            else:
                print(f"  Skipping non-date folder: {issue}")

if __name__ == "__main__":
    archive_magazines()
