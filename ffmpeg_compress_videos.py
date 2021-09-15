import os

source_folder = r'D:\BATCH\_renders'
target_folder = r'D:\BATCH\_renders\_output'

for file in os.listdir(source_folder):
	
	filename, extension = file[:-4], file[-4:]

	if extension.lower() in {'.mp4', '.mov'}:
		
		file_in = os.path.join(source_folder, file)
		file_out = os.path.join(target_folder, filename + '.mp4')
		command = f'ffmpeg -i {file_in} -vf "crop=trunc(iw/2)*2:trunc(ih/2)*2" -vcodec libx264 -an {file_out}'
		os.system(command)
		print(f"{filename} compressed")