import os
import shutil
data_dir = r'G:/My Drive/ranking_instytutow/data_manual_completion/institutions'
target_dir = r'G:/My Drive/ranking_instytutow/data/articles/manual_download'

moved = []
empty = []
for dir in os.listdir(data_dir):
    print(dir)
    