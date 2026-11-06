import os
import time
import ollama
from voice import JarvisVoice
from ear import JarvisEar
from memory import JarvisMemory
from tools import open_application, play_music, read_code_file, write_code_file
import keyboard

jarvis_tools = [
    {
        'type': 'function',
        'function': {
            'name': 'open_application',
            'description': 'Opens an application or game on the computer (e.g., VS Code, CS2, Notepad).',
            'parameters': {
                'type': 'object',
                'properties': {
                    'app_name': {'type': 'string', 'description': 'The name of the application to open'}
                },
                'required': ['app_name']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'play_music',
            'description': 'Searches and plays a specific song, music, or video on YouTube.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'song_name': {'type': 'string', 'description': 'The name of the song or artist to play'}
                },
                'required': ['song_name']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'read_code_file',
            'description': 'Reads the content of a specified code file path within the project directory.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'file_path': {'type': 'string', 'description': 'The path of the file to read'}
                },
                'required': ['file_path']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'write_code_file',
            'description': 'Writes or updates code content to a specified file path within the project directory.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'file_path': {'type': 'string', 'description': 'The path of the file to write/update'},
                    'code_content': {'type': 'string', 'description': 'The complete code content to write into the file'}
                },
                'required': ['file_path', 'code_content']
            }
        }
    }
]

def main():
    db_path = "jarvis_memory.db"
    if not os.path.exists(db_path):
        print(f"[System Warning] Database '{db_path}' not found. Creating a new one.")

    try:
        jarvis_audio = JarvisVoice()
        jarvis_ear = JarvisEar()
        jarvis_memory = JarvisMemory(db_path=db_path)
    except Exception as e:
        print(f"[Critical Error] Failed to initialize core modules: {e}")
        return
    
    jarvis_audio.speak("Systems, memory, and hybrid input modules are fully online, Arda.")
    print("\n=========================================================")
    print(" [SYSTEM READY] How would you like to communicate?")
    print("   -> Hold 'RIGHT CTRL' key to speak (Voice Mode)")
    print("   -> Press 'TAB' key to type (Text Mode)")
    print("   -> Press 'ESC' while Jarvis is speaking to interrupt")
    print("=========================================================\n")
    
    while True:
        try:
            user_input = ""
            
            if keyboard.is_pressed('right ctrl'):
                user_input = jarvis_ear.listen_ptt(hotkey='right ctrl')
            
            elif keyboard.is_pressed('tab'):
                while keyboard.is_pressed('tab'):
                    time.sleep(0.01)
                
                user_input = input("\n[Terminal] Type your message and press Enter: ")
                
            else:
                time.sleep(0.05)
                continue

            if not user_input or len(user_input.strip()) < 2:
                continue
                
            print(f"\nArda: {user_input}")

            if any(word in user_input.lower() for word in ['shut down', 'exit', 'goodbye', 'quit', 'stop']):
                jarvis_audio.speak("Shutting down systems. Goodbye, Arda.")
                break

            jarvis_memory.save_message("user", user_input)

            coding_keywords = ["code", "script", "c++", "c", "python", "function", "debug", "memory leak", "file", "error", "bug", "refactor"]
            has_coding_intent = any(keyword in user_input.lower() for keyword in coding_keywords)
            dynamic_temp = 0.1 if has_coding_intent else 0.3
            print(f"[System] Mode: {'Coding' if has_coding_intent else 'Standard'} | Temperature: {dynamic_temp}")

            print("[System] Jarvis is thinking...")
            recent_context = jarvis_memory.get_recent_context(limit=6)
            
            response = ollama.chat(
                model='jarvis', 
                messages=recent_context,
                options={'temperature': dynamic_temp},
                tools=jarvis_tools
            )

            jarvis_reply = ""

            if response['message'].get('tool_calls'):
                for tool in response['message']['tool_calls']:
                    function_name = tool['function']['name']
                    arguments = tool['function']['arguments']
                    result_msg = ""

                    try:
                        if function_name == 'open_application':
                            result_msg = open_application(arguments.get('app_name', ''))
                        elif function_name == 'play_music':
                            result_msg = play_music(arguments.get('song_name', ''))
                        elif function_name == 'read_code_file':
                            result_msg = read_code_file(arguments.get('file_path', ''))
                        elif function_name == 'write_code_file':
                            result_msg = write_code_file(arguments.get('file_path', ''), arguments.get('code_content', ''))
                        else:
                            result_msg = "Error: Unknown tool called."
                    except Exception as tool_err:
                        result_msg = f"Error executing tool: {str(tool_err)}"
                    
                    recent_context.append(response['message'])
                    recent_context.append({'role': 'tool', 'content': result_msg})
                    
                    final_response = ollama.chat(model='jarvis', messages=recent_context)
                    jarvis_reply = final_response['message']['content']
            else:
                jarvis_reply = response['message']['content']

            jarvis_memory.save_message("assistant", jarvis_reply)
            
            # EKSİK OLAN SATIR EKLENDİ: Artık ne cevap verdiğini ekranda görebileceksin
            print(f"Jarvis: {jarvis_reply}")
            
            jarvis_audio.speak(jarvis_reply)
            print("\n" + "-"*50 + "\n")

        except Exception as loop_err:
            print(f"[Runtime Error] {loop_err}")
            continue

if __name__ == "__main__":
    main()