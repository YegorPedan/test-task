import threading
from time import sleep


class Song:
    def __init__(self, path: str, duration: int) -> None:
        self.path = path
        self.duration = duration


class DoublyLinkedListNode:
    def __init__(self, song: Song) -> None:
        self.song = song
        self.prev = None
        self.next = None


class Playlist:
    def __init__(self) -> None:
        self.head = None
        self.tail = None
        self.current_node = None
        self.paused = False
        self.play_thread = None

    def add_song(self, path: str, duration: int) -> None:
        new_song = Song(path, duration)
        if not self.head:
            self.head = DoublyLinkedListNode(new_song)
            self.tail = self.head
        else:
            new_node = DoublyLinkedListNode(new_song)
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        print(f"Song added {self.tail.song.path}")

    def play(self, path: str = None) -> None:
        if not self.head:
            print("Your playlist is empty")
            return

        if self.paused:
            self.paused = False
            return

        current_node = self.head
        while current_node and current_node.song.path != path:
            current_node = current_node.next

        if current_node and current_node.song.path == path:
            self.current_node = current_node
            print(f"Now playing: {current_node.song.path} for {current_node.song.duration} seconds")

            def play_song():
                remaining_time = current_node.song.duration
                while remaining_time > 0:
                    if self.paused:
                        sleep(1)
                        continue
                    sleep(1)
                    remaining_time -= 1
                self.next()

            self.play_thread = threading.Thread(target=play_song)
            self.play_thread.start()
        else:
            print("Song not found in playlist")

    def next(self) -> None:
        if self.current_node and self.current_node.next:
            self.current_node = self.current_node.next
            self.play(self.current_node.song.path)
        else:
            print("End of playlist reached")

    def prev(self) -> None:
        if self.current_node and self.current_node.prev:
            self.current_node = self.current_node.prev
            self.play(self.current_node.song.path)
        else:
            print("Beginning of playlist reached")

    def pause(self) -> None:
        """Not sure that is working correctly"""
        if self.play_thread and self.play_thread.is_alive():
            self.paused = True


if __name__ == "__main__":
    playlist = Playlist()
    playlist.add_song("first_song", 4) # create a node for first song
    playlist.add_song("second_song", 3) # create a node for second song
    playlist.add_song("third_song", 3) # create a node for third song
    playlist.play("second_song")
    playlist.prev() # use prev to play first song