import os
import random
import pygame
from colorama import Fore
from pygame.locals import *
import api
from mutagen.mp3 import MP3

# Music Folder
folder_path = "track/"
# Played music history
history = []

# Colors
black = (0, 0, 0)
white = (255, 255, 255)


def main():
    # Init
    pygame.init()

    # Font
    font = pygame.font.Font("static/font/myfont.ttf", 48)
    font_btn = pygame.font.Font("static/font/ZCOOLKuaiLe-Regular.ttf", size=15)

    # Static Configuration
    screen_width = 500
    screen_height = 250
    surface = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Live Control')
    icon = pygame.image.load('control.png')
    pygame.display.set_icon(icon)
    surface.fill(black)

    running = True

    print(Fore.CYAN + "-----Radio Station Control Interface------")
    while running:
        # Application Window:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Get all mp3 files in the music folder
        song_list = [file for file in os.listdir(folder_path) if file.endswith(".mp3")]

        # Get all songs that had not played in the last 50 songs
        unplayed_songs = [song for song in song_list if song not in history[-50:]]

        # If there are no unplayed song
        if not unplayed_songs:
            print(Fore.RED + "All available songs have been played in the last 50 rounds.")
            running = False
            break

        # Randomly select a song from the unplayed list
        selected_song = random.choice(unplayed_songs)
        history.append(selected_song)
        selected_song_path = os.path.join(folder_path, selected_song)

        artist = selected_song.split(' - ')[0].removeprefix(' ')
        title = ''.join(selected_song.split(' - ')[1::]).removeprefix(' ').removesuffix('.mp3')

        print(Fore.YELLOW + "Playing:", Fore.RESET + selected_song)
        print(Fore.YELLOW + "Title:", Fore.RESET + title)
        print(Fore.YELLOW + "Artist:", Fore.RESET + artist)
        print(Fore.CYAN + '------------------------------------------' + Fore.RESET)
        try:
            api.change(title=title, artist=artist)
        except Exception as e:
            print(Fore.RED + "Error changing title artist:", str(e).replace('\n', ' ') + Fore.RESET)
            pass

        # Init music player
        # output_device = None  # Put your device here (can be listed using the print_output_devices.py)
        # pygame.mixer.init(output_device)  # The output device is set to the device
        pygame.mixer.init()  # The output device is the current selected device
        pygame.mixer.music.load(selected_song_path)

        # Play music
        pygame.mixer.music.play()

        audio_length = MP3(selected_song_path).info.length
        audio_min = str(f"{int(audio_length // 60):02}")
        audio_sec = str(f"{round(audio_length % 60):02}")

        playing = True
        previous_sec = -1
        # If music is playing or paused (still on current song)
        while pygame.mixer.music.get_busy() or playing is False:
            # Process current timestamp
            current_seconds = pygame.mixer.music.get_pos() / 1000
            current_min = current_seconds // 60
            current_sec = current_seconds % 60
            if current_sec == 60:
                current_min += 1
                current_sec = 0
            current_min = str(f"{int(current_min):02}")
            current_sec = str(f"{round(current_sec):02}")
            current_timestamp = ''.join((current_min + ':' + current_sec, ' / ', audio_min + ':' + audio_sec))

            # Update page timestamp
            if int(current_seconds) >= int(previous_sec) + 1:
                try:
                    api.change(title=title, artist=artist)
                    api.timestamp(current_timestamp)
                except Exception as e:
                    print(Fore.RED + "Error when changing timestamp: " + str(e).replace('\n', ' ') + Fore.RESET)
                    pass
            previous_sec = current_seconds

            # Update UI
            surface.fill(black)

            # Render Title
            title_text = font.render(str(title), True, white)
            text_width, text_height = title_text.get_size()
            x = (screen_width - text_width) // 2
            y = 25
            surface.blit(title_text, (x, y))

            # Render Artist
            artist_text = font.render(str(artist), True, white)
            text_width, text_height = artist_text.get_size()
            x = (screen_width - text_width) // 2
            y = 100
            surface.blit(artist_text, (x, y))

            # Mouse Pointer position for button interaction
            mouse = pygame.mouse.get_pos()

            # Center Button (Play/Stop)
            x = (screen_width - 100) // 2
            y = 175
            # Pointer detection
            if 200 <= mouse[0] <= 300 and 165 <= mouse[1] <= 205:
                pygame.draw.rect(surface, (128, 128, 128), [x, y - 10, 100, 40])
            else:
                pygame.draw.rect(surface, white, [x, y - 10, 100, 40])
            if playing:
                play_stop_text = font_btn.render("Stop", True, black)
            else:
                play_stop_text = font_btn.render("Play", True, black)
            text_width, text_height = play_stop_text.get_size()
            x = (screen_width - text_width) // 2  # Adjust x to center to fit text
            surface.blit(play_stop_text, (x, y))

            # Left timestamp
            # Render
            timestamp_text = font_btn.render(current_timestamp, True, white)
            text_width, text_height = timestamp_text.get_size()
            x = (screen_width - text_width) // 2 - 125  # Adjust x to center to fit text
            y = 175
            surface.blit(timestamp_text, (x, y))

            # Right button (Next)
            x = (screen_width - 100) // 2 + 125
            y = 175
            # Mouse pointer interaction
            if 200 + 125 <= mouse[0] <= 300 + 125 and 165 <= mouse[1] <= 205:
                pygame.draw.rect(surface, (128, 128, 128), [x, y - 10, 100, 40])
            else:
                pygame.draw.rect(surface, white, [x, y - 10, 100, 40])
            next_text = font_btn.render("Next", True, black)
            text_width, text_height = next_text.get_size()
            x = (screen_width - text_width) // 2 + 125  # Adjust x to center to fit text
            surface.blit(next_text, (x, y))

            # Render whole screen
            pygame.display.flip()

            # Button Interactions (Key Pressed)
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Pressed play/stop button
                    if 200 <= mouse[0] <= 300 and 165 <= mouse[1] <= 205:
                        if playing:
                            pygame.mixer.music.pause()
                            playing = False
                        else:
                            pygame.mixer.music.unpause()
                            playing = True
                    # Pressed next button
                    if 200 + 125 <= mouse[0] <= 300 + 125 and 165 <= mouse[1] <= 205:
                        pygame.mixer.music.pause()
                        playing = True


if __name__ == "__main__":
    main()
