import pandas as pd
import os


def timecode_stamp(video_dir, csv_file, out_dir = None, font_path = 'font.ttf', font_factor = 25, open_dir = True):

    # supported containers
    video_ext = ('.mp4', '.mov') 
    # creates or checks output dir
    if not out_dir:
        out_dir = os.path.join(video_dir, "out_TC")
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    # check font factor
    if not font_factor > 0:
        font_factor = 25 # default value

    # list files and filepaths from video dir
    video_lst = [video for video in os.listdir(video_dir) if video[-4:].lower() in video_ext]

    # extract dataframe from csv file (File Name, Audio TC and Framerate columns mandatory)
    df = pd.read_csv(csv_file)
    df_len = len(df['File Name'])

    # batch encode videos
    for i in range(df_len):
        # get current video infos
        filename = df.iloc[i]['File Name']
        timecode = df.iloc[i]['Audio TC'].replace(':', '\:')
        framerate = df.iloc[i]['Video Framerate']
        rotation = ''
        # if Rotation column in csv file and rotation agnle supported
        if 'Rotation' in df:
            angle = int(df.iloc[i]['Rotation'])
            rotation_arg = {90: 'transpose=1, ', -90: 'transpose=2, ', 180: 'transpose=2,transpose=2, '} # arguments for the ffmpeg rotation
            if angle in rotation_arg.keys():
                rotation = rotation_arg[angle]

        print(50*'#') # output separator
        print(filename, timecode, framerate, rotation)
        
        if filename in video_lst:
            video_in = os.path.join(video_dir, filename)
            video_out = os.path.join(out_dir, filename)

            command = "ffmpeg -i {input} -filter_complex \"{rot}drawtext=fontfile={font}: fontsize=(h/{size}): timecode='{tc}': r={fps}: \ x=(w-tw)/2: y=h-(2*lh): fontcolor=white: box=1: boxcolor=0x00000000@1\" -an -y {output}".format(input=video_in, output=video_out, tc=timecode, fps=framerate, rot=rotation, font=font_path, size = font_factor)
            print(command)
            os.system(command)

        else:
            print("{} not found in directory - skipped".format(filename))

    # opens out directory
    if open_dir:
        os.startfile(out_dir)


if __name__ == "__main__":

    # define video directory and csv file paths
    video_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "medias")
    csv_file = os.path.join(video_dir, 'tc.csv')

    timecode_stamp(video_dir, csv_file)