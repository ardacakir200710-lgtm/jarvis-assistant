import os
import urllib.request
import urllib.parse
import re
import webbrowser

# Güvenlik Sınırı: Sadece Jarvis klasörünün içinde işlem yapılabilir
SAFE_DIRECTORY = os.path.abspath(os.path.dirname(__file__))

def _is_safe_path(target_path: str) -> bool:
    """Verilen dosya yolunun güvenli dizin içinde olup olmadığını kontrol eder."""
    # Mutlak (absolute) yolu hesapla
    abs_target = os.path.abspath(os.path.join(SAFE_DIRECTORY, target_path))
    # Hedef yolun güvenli dizinle başlayıp başlamadığını doğrula
    return os.path.commonpath([SAFE_DIRECTORY, abs_target]) == SAFE_DIRECTORY

def open_application(app_name: str) -> str:
    """Belirtilen uygulamayı veya oyunu bilgisayarda açar."""
    app_name = app_name.lower()
    apps = {
        "vs code": "code",
        "vscode": "code",
        "cs2": "start steam://rungameid/730",
        "counter strike": "start steam://rungameid/730",
        "squad": "start steam://rungameid/393380",
        "browser": "start msedge",
        "notepad": "notepad"
    }
    
    command = apps.get(app_name)
    if command:
        try:
            os.system(command)
            return f"Successfully opened {app_name}."
        except Exception as e:
            return f"Error opening {app_name}: {str(e)}"
    else:
        return f"I don't know the system path for {app_name}."

def play_music(song_name: str) -> str:
    """YouTube üzerinde arama yapar ve ilk çıkan şarkıyı tarayıcıda otomatik başlatır."""
    try:
        query_string = urllib.parse.urlencode({"search_query": song_name})
        html_content = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'watch\?v=(\S{11})', html_content.read().decode())
        
        if search_results:
            video_url = "https://www.youtube.com/watch?v=" + search_results[0]
            webbrowser.open(video_url)
            return f"Successfully playing {song_name} on YouTube."
        else:
            return f"Could not find {song_name} on YouTube."
    except Exception as e:
        return f"Error trying to play music: {str(e)}"

# --- GÜVENLİK KORUMALI DOSYA ARAÇLARI ---

def read_code_file(file_path: str) -> str:
    """Güvenli dizin dışına çıkmadan belirtilen dosya içeriğini okur."""
    if not _is_safe_path(file_path):
        return "Security Error: Access denied. You cannot read files outside the Jarvis project directory."
    
    try:
        abs_path = os.path.abspath(os.path.join(SAFE_DIRECTORY, file_path))
        if not os.path.exists(abs_path):
            return f"Error: File '{file_path}' does not exist."
        with open(abs_path, "r", encoding="utf-8") as f:
            content = f.read()
        return f"File content of {file_path}:\n{content}"
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_code_file(file_path: str, code_content: str) -> str:
    """Güvenli dizin dışına çıkmadan belirtilen dosyaya kod yazar/günceller."""
    if not _is_safe_path(file_path):
        return "Security Error: Access denied. You cannot write files outside the Jarvis project directory."
    
    try:
        abs_path = os.path.abspath(os.path.join(SAFE_DIRECTORY, file_path))
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(code_content)
        return f"Successfully updated and saved code to {file_path}."
    except Exception as e:
        return f"Error writing to file: {str(e)}"