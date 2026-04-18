import pygame
import os

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()

        # Файл тұрған папканың нақты жолын алу
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Файлдардың жолын анықтау
        self.playlist = [
            os.path.join(base_dir, "uide.mp3"),
            os.path.join(base_dir, "qustar.mp3")
        ]
        
        # ТЕКСЕРУ: Бағдарлама қай жерден файл іздеп жатыр?
        print("Бағдарлама мына папкадан іздеп жатыр:", base_dir)
        print("Файлдардың толық жолы:", self.playlist)

        self.current_index = 0
        self.is_playing = False

    def play(self):
        file_path = self.playlist[self.current_index]
        
        # Файл бар ма, жоқ па? Соны тексереміз
        if os.path.exists(file_path):
            print("Файл табылды:", file_path)
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            self.is_playing = True
        else:
            print("ҚАТЕЛІК: Файл табылмады:", file_path)
    
    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next(self):
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play()

    def prev(self):
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play()

    def get_current_track(self):
        return os.path.basename(self.playlist[self.current_index])
    
    def get_position(self):
        pos = pygame.mixer.music.get_pos()
        return pos // 1000