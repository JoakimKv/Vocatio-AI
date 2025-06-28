import os
import streamlit as st
import ffmpeg
import yt_dlp

class Utils:

   def __init__(self, st_screen):
       
      self.st_screen = st_screen
      self.file_path_audio = ""
      self.file_path_video = ""

   def convert_mp4_to_wav(self, mp4_file_path):

      # Convert an MP4 file to a WAV file.

      temp_dir = "temp"

      if not os.path.exists(temp_dir):

         os.makedirs(temp_dir)

      wav_file_path = os.path.join(temp_dir, os.path.splitext(os.path.basename(mp4_file_path))[0] + ".wav")

      # Check if the file exists
      if os.path.exists(wav_file_path):
         
         # Remove the file
         os.remove(wav_file_path)
         print(f"{wav_file_path} has been deleted.")

      else:
         
         print(f"{wav_file_path} does not exist.")

      ffmpeg.input(mp4_file_path).output(wav_file_path).run()
 
      return wav_file_path

   # Saves the uploaded file to the hard drive and returns the filename.
   def save_uploaded_file(self, uploaded_file):

      file_path = os.path.join("temp", uploaded_file.name)

      with open(file_path, "wb") as f:

         f.write(uploaded_file.getbuffer())

      return file_path

   # New path_hook function for audio.
   def path_hook_audio(self, d):

      if d['status'] == 'finished':

         print("Download completed ...")
         file_path = d['filename']

         self.file_path_audio = file_path

   # New path_hook function for video.
   def path_hook_video(self, d):

      if d['status'] == 'finished':

         print("Download completed ...")
         file_path = d['filename']

         self.file_path_video = file_path

   # Updated download_youtube_audio function (for .wav format).
   def download_youtube_audio(self, url):

      try:

         ydl_opts = {
                    'format': 'bestaudio/best',  # Get the best audio-only format
                    'outtmpl': './temp/%(title)s',  # output path
                    'progress_hooks': [self.path_hook_audio],
                    'postprocessors': [{
                       'key': 'FFmpegExtractAudio',
                       'preferredcodec': 'wav',  # Convert to .wav format
                    }],
         }

         self.st_screen.write("Downloading audio from YouTube ...")

         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            
            ydl.download([url])

         self.st_screen.write("Download completed ...")
         print(self.file_path_audio)

         return self.file_path_audio + '.wav'
    
      except Exception as e:

         self.st_screen.error(f"Failed to download YouTube audio: {e}")    

         return None
      
   # Updated download_youtube_video function (for .mp4 format).
   def download_youtube_video(self, url):

      try:

         ydl_opts = {
                    'format': 'bestvideo+bestaudio/best',  # Get the best video with audio.
                    'outtmpl': './temp/%(title)s.mp4',     # Specify the output path and ensure the extension is .mp4.
                    'progress_hooks': [self.path_hook_video],
                    'merge_output_format': 'mp4',          # Ensure output is in .mp4 format.
         }

         self.st_screen.write("Downloading video from YouTube ...")

         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            
            ydl.download([url])

         self.st_screen.write("Download completed ...")
         print(self.file_path_video)

         return self.file_path_video + '.mp4'
    
      except Exception as e:

         self.st_screen.error(f"Failed to download YouTube video: {e}")    

         return None       

