from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, VideoUnavailable, NoTranscriptFound
import re,os,random
import requests
from colorama import Fore,init
init(autoreset=True)

def get_video_title(video_id):
    try:
        # Fetch video page to get title
        response = requests.get(f'https://www.youtube.com/watch?v={video_id}')
        title_match = re.search(r'<title>(.*?) - YouTube</title>', response.text)
        if title_match:
            return title_match.group(1)
    except Exception as e:
        print("Error fetching video title:", e)
    return "YouTube_Transcript"

def save_transcript(video_url):
    # Extract video ID from URL
    video_id = video_url.split("v=")[-1]

    try:
        # Check available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Try to fetch Hindi transcript if available, otherwise default to any available language
        if 'or' in [t.language_code for t in transcript_list]:
            transcript = transcript_list.find_transcript(['or'])
            print("Odia transcript found.✅")

        elif 'hi' in [t.language_code for t in transcript_list]:
            transcript = transcript_list.find_transcript(['hi'])
            print("Hindi transcript found.✅")
        else:
            transcript = transcript_list.find_transcript(['en', 'en-US'])  # Try English if Hindi is unavailable
            print("Using English or default available transcript.✅")
        
        # Retrieve and join transcript text
        transcript_text = "\n".join([entry['text'] for entry in transcript.fetch()])
        
        # Fetch and sanitize video title for saving
        video_title = get_video_title(video_id)
        sanitized_title = re.sub(r'[\\/*?:"<>|]', "", video_title)
        
        try:
            if os.name == 'nt':    
                # Ensure "Transcripts" folder exists
                folder_path = "Transcripts"
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                
                # Save transcript to a text file in the "Transcripts" folder
                file_path = os.path.join(folder_path, f"{sanitized_title}.txt")
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(transcript_text)
                
                save_message = f"Transcript saved as '{file_path}'"
                print(Fore.GREEN + save_message)
        except:
            # Ensure "Transcripts" folder exists
                folder_path = "//sdcard//Download//Transcripts"
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                
                # Save transcript to a text file in the "Transcripts" folder
                file_path = os.path.join(folder_path, f"{sanitized_title}.txt")
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(transcript_text)
                
                save_message = f"Transcript saved as '{file_path}'"
                print(Fore.GREEN + save_message)

    except TranscriptsDisabled:
        print(Fore.YELLOW+"Transcripts are disabled for this video.")
    except VideoUnavailable:
        print(Fore.RED+"Video is unavailable.")
    except NoTranscriptFound:
        print(Fore.RED+"No transcript found for this video.")
    except Exception as e:
        print(Fore.RED+"An error occurred:", e)

def banner():
    banner = [Fore.CYAN+'''
╭╮╱╱╭┳━━━━╮╭━━━━╮╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╭╮╱╭━━━╮╱╱╱╱╱╱╱╱╱╱╭╮╱╱╱╱╱╱╱╱╭╮
┃╰╮╭╯┃╭╮╭╮┃┃╭╮╭╮┃╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╭╯╰╮╰╮╭╮┃╱╱╱╱╱╱╱╱╱╱┃┃╱╱╱╱╱╱╱╱┃┃
╰╮╰╯╭┻╯┃┃╰╯╰╯┃┃┣┻┳━━┳━╮╭━━┳━━┳━┳┳━┻╮╭╯╱┃┃┃┣━━┳╮╭╮╭┳━╮┃┃╭━━┳━━┳━╯┣━━┳━╮
╱╰╮╭╯╱╱┃┃╱╱╱╱┃┃┃╭┫╭╮┃╭╮┫━━┫╭━┫╭╋┫╭╮┃┃╱╱┃┃┃┃╭╮┃╰╯╰╯┃╭╮┫┃┃╭╮┃╭╮┃╭╮┃┃━┫╭╯
╱╱┃┃╱╱╱┃┃╱╱╱╱┃┃┃┃┃╭╮┃┃┃┣━━┃╰━┫┃┃┃╰╯┃╰╮╭╯╰╯┃╰╯┣╮╭╮╭┫┃┃┃╰┫╰╯┃╭╮┃╰╯┃┃━┫┃
╱╱╰╯╱╱╱╰╯╱╱╱╱╰╯╰╯╰╯╰┻╯╰┻━━┻━━┻╯╰┫╭━┻━╯╰━━━┻━━╯╰╯╰╯╰╯╰┻━┻━━┻╯╰┻━━┻━━┻╯
╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱┃┃
╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╰╯
------------------------------------------------------------------------
Author - Rajkishor Patra
Github - imraj569
------------------------------------------------------------------------               
              ''',Fore.GREEN+'''
╭━┳┳━━╮╭━━╮╱╱╱╱╱╱╭━╮╱╱╱╭╮╱╭╮╱╭━━╮╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╭╮
╰╮┃┣╮╭╯╰╮╭╋┳━╮╭━┳┫━╋━┳┳╋╋━┫╰╮╰╮╮┣━┳┳┳┳━┳┳╮╭━┳━╮╭╯┣━┳┳╮
╭┻╮┃┃┃╱╱┃┃╭┫╋╰┫┃┃┣━┃━┫╭┫┃╋┃╭┫╭┻╯┃╋┃┃┃┃┃┃┃╰┫╋┃╋╰┫╋┃┻┫╭╯
╰━━╯╰╯╱╱╰┻╯╰━━┻┻━┻━┻━┻╯╰┫╭┻━╯╰━━┻━┻━━┻┻━┻━┻━┻━━┻━┻━┻╯
╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╰╯
--------------------------------------------------------------
Author - Rajkishor Patra
Github - imraj569
--------------------------------------------------------------
'''
              ]
    print(random.choice(banner))

if __name__ == "__main__":
    os.system("cls")
    banner()
    video_url = input(Fore.CYAN+"Enter the YouTube video URL: ")
    save_transcript(video_url)
