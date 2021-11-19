import pandas as pd
import os


def timecode_stamp(csv_file, out_dir = None, font_path = 'fonts/arial.ttf', font_factor=25, overwrite = False, open_dir = True):

    # supported containers
    video_ext = ('.mp4', '.mov') 

    # check font factor
    if not font_factor > 0:
        font_factor = 10 # default value

    # extract dataframe from csv file
    df = pd.read_csv(csv_file)
    # get df length
    df_len = len(df['File Name'])

    # batch encode videos
    for i in range(df_len):

        # Read filepath and filename, check validity
        filepath = df.iloc[i]['File Path']
        filename = df.iloc[i]['File Name']
        video_in = os.path.join(filepath, filename)
        if not os.path.isfile(video_in):
            print(f"{video_in} not valid >> Skip file")
            continue
        
        # Read timecode and framerate
        timecode = df.iloc[i]['Audio TC'].replace(':', '\:')
        framerate = df.iloc[i]['Framerate']

        # if Rotation column in csv file and rotation agnle supported
        rotation = ""
        if 'Rotation' in df:
            angle = int(df.iloc[i]['Rotation'])
            rotation_arg = {90: 'transpose=1, ', -90: 'transpose=2, ', 180: 'transpose=2,transpose=2, '} # arguments for the ffmpeg rotation
            if angle in rotation_arg.keys():
                rotation = rotation_arg[angle]

        if os.path.isfile(video_in) and video_in[-4:].lower() in video_ext:
            
            # if output dir invalid
            if not out_dir or not os.path.isdir(out_dir):
                out_dir = os.path.join(os.path.dirname(csv_file), "out_tc")
                os.mkdir(out_dir)
            
            # define video out
            video_out = os.path.join(out_dir, filename)

            # skip file if already in output folder and overwrite is set to False
            if os.path.isfile(video_out) and not overwrite:
                print("{} already in output folder - Skipped. Delete file or set overwrite parameter to True".format(filename))
                continue
            
            print(50*'#') # log separator
            print(filename, timecode, framerate, rotation)
            print(50*'#') # log separator
        
            if filename.endswith('obs.mp4'):
                # Keep left channel
                command = "ffmpeg -i {input} -map 0 -map -0:a:0 -filter_complex \"{rot}drawtext=fontfile={font}: fontsize=(h/{size}): text={take_name}: timecode='{tc}': r={fps}: \ x=(w-tw)/2: y=h-(lh): fontcolor=white: box=1: boxcolor=0x00000000@1\" -y {output}".format(input=video_in, output=video_out, tc=timecode, fps=framerate, rot=rotation, font=font_path, size = font_factor, take_name=filename[:-4]+'  Tc/')
            else:
                # Remove all audio
                command = "ffmpeg -i {input} -filter_complex \"{rot}drawtext=fontfile={font}: fontsize=(h/{size}): text={take_name}: timecode='{tc}': r={fps}: \ x=(w-tw)/2: y=h-(lh): fontcolor=white: box=1: boxcolor=0x00000000@1\" -an -y {output}".format(input=video_in, output=video_out, tc=timecode, fps=framerate, rot=rotation, font=font_path, size = font_factor, take_name=filename[:-4]+'  Tc/')
            
            print(command)
            os.system(command)

        else:
            print("{} not found >> skipped".format(video_in))

    # opens out directory
    if open_dir:
        os.startfile(out_dir)


if __name__ == "__main__":

    # define video directory and csv file paths
    csv_file = r"C:\Users\artist\Desktop\TEST\tc.csv"

    timecode_stamp(csv_file, font_factor = 45, overwrite=False)