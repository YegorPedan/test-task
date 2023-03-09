class Song:
    def __init__(self, duration):
        self.duration = duration

class Playlist:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current_node = None
        self.current_duration_left = 0
        self.playing = False
    
    def play(self):
        if not self.playing:
            self.playing = True
            if not self.current_node:
                self.current_node = self.head
            self.current_duration_left = self.current_node.value.duration
            print(f"Сейчас играет: {self.current_node.value}")
    
    def pause(self):
        self.playing = False
        print("Пауза.")
    
    def add_song(self, duration):
        new_song = Song(duration)
        if not self.head:
            self.head = DoublyLinkedListNode(new_song)
            self.tail = self.head
        else:
            new_node = DoublyLinkedListNode(new_song)
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        print(f"Песня добавлена: {new_song}")
    
    def next_song(self):
        if not self.current_node:
            self.current_node = self.head
        elif self.current_node.next:
            self.current_node = self.current_node.next
        else:
            self.current_node = self.head
        self.current_duration_left = self.current_node.value.duration
        print(f"Сейчас играет: {self.current_node.value}")
    
    def prev_song(self):
        if not self.current_node:
            self.current_node = self.tail
        elif self.current_node.prev:
            self.current_node = self.current_node.prev
        else:
            self.current_node = self.tail
        self.current_duration_left = self.current_node.value.duration
        print(f"Сейчас играет: {self.current_node.value}")
    
    def tick(self):
        if self.playing and self.current_duration_left > 0:
            self.current_duration_left -= 1
        elif self.playing and self.current_duration_left == 0:
            self.next_song()
        else:
            pass

class DoublyLinkedListNode:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None
