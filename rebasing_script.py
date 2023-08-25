import os
import shutil
data_dir = r'G:/My Drive/ranking_instytutow/data/institutions'
target_dir = r'G:/My Drive/ranking_instytutow/data/articles/manual_download'

moved = []
empty = []
for dir in os.listdir(data_dir):
    try:
        dir_dir = os.path.join(data_dir,dir, 'papers_manual_downloaded')
        dir_tar = os.path.join(target_dir, dir)
        shutil.move(dir_dir, dir_tar)
        moved.extend(([dir]))
        
    except:
        empty.extend(([dir]))

print('udało się dla: ', moved)
print('nie dało się dla: ', empty)
    