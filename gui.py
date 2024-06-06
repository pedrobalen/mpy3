import tkinter as tk
from tkinter import filedialog, messagebox
from pytube import YouTube
from moviepy.editor import *
import os

def download_video(url, output_path):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        output_file = stream.download(output_path)
        return output_file
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download video: {e}")
        return None

def convert_to_mp3(video_path, output_path):
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        base, ext = os.path.splitext(video_path)
        mp3_path = os.path.join(output_path, os.path.basename(base) + '.mp3')
        audio.write_audiofile(mp3_path)
        audio.close()
        video.close()
        return mp3_path
    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert video to MP3: {e}")
        return None

def start_download():
    url = url_entry.get()
    output_path = filedialog.askdirectory()
    
    if not url:
        messagebox.showwarning("Input Error", "Please enter a YouTube URL")
        return

    if not output_path:
        messagebox.showwarning("Input Error", "Please select an output folder")
        return

    video_path = download_video(url, output_path)
    if video_path:
        mp3_path = convert_to_mp3(video_path, output_path)
        if mp3_path:
            messagebox.showinfo("Success", f"MP3 saved to: {mp3_path}")
        os.remove(video_path)

root = tk.Tk()
root.title("YouTube MP3 Downloader")

tk.Label(root, text="YouTube URL:").grid(row=0, column=0, padx=10, pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

download_button = tk.Button(root, text="Download MP3", command=start_download)
download_button.grid(row=1, column=0, columnspan=2, pady=20)

root.mainloop()
