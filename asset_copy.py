import sqlite3
import sys
import shutil
import os
from tqdm import tqdm

def copyAll():
    base_path = os.path.abspath(sys.argv[2])
    dest_path = os.path.abspath(sys.argv[3])
    zips_path = os.path.join(base_path, 'Data', 'Games')
    all_zips = os.listdir(zips_path)
    conn = sqlite3.connect(sys.argv[1])
    c = conn.cursor()

    rows = c.execute("""
        SELECT id
        FROM game g
    """)

    all_rows = []
    for row in rows:
        all_rows.append(row)

    for row in tqdm(all_rows):
        id = row[0]
        # Copy any zips
        files = [file for file in all_zips if file.startswith(id)]
        for file in files:
            full_path = os.path.join(zips_path, file)
            if os.path.exists(full_path):
                save_path = os.path.join(dest_path, 'Data', 'Games', file)
                dst_dir = os.path.dirname(save_path)
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                shutil.copyfile(full_path, save_path)
        # Copy any images
        try:
            logo_path = os.path.join(base_path, 'Data', 'Images', 'Logos', id[0:2], id[2:4], id + '.png')
            if os.path.exists(logo_path):
                logo_dest = os.path.join(dest_path, 'Data', 'Images', 'Logos', id[0:2], id[2:4], id + '.png')
                dst_dir = os.path.dirname(logo_dest)
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                shutil.copyfile(logo_path, logo_dest)
        except:
            pass
        try:
            ss_path = os.path.join(base_path, 'Data', 'Images', 'Screenshots', id[0:2], id[2:4], id + '.png')
            if os.path.exists(ss_path):
                ss_dest = os.path.join(dest_path, 'Data', 'Images', 'Screenshots', id[0:2], id[2:4], id + '.png')
                dst_dir = os.path.dirname(ss_dest)
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                shutil.copyfile(ss_path, ss_dest)
        except:
            pass

    

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('provide database name, root path and dest path')
    else:
        copyAll()

