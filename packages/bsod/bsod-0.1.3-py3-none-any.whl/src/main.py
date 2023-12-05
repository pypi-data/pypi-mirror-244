from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from utils import play_audio, blocK_keyboard, show_error
import threading

def main():
    thread1 = threading.Thread(target=play_audio, args=["assets/audio.mp3",])
    thread2 = threading.Thread(target=show_error)

    blocK_keyboard()
    
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

if __name__ == "__main__":
    main()