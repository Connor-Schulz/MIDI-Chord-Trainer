import pygame
import pygame.midi as midi
from KeyboardPlayer import newController
from draw import new_surface
from random import randint
from random import choice


class note:
    def __init__(self, in_device, note_number, velocity, channel, timestamp):
        self.in_device = in_device
        self.note_number = note_number
        self.velocity = velocity
        self.channel = channel
        self.timestamp = timestamp


class chord:
    def __init__(self, name, notes):
        self.name = name
        self.notes = notes


class scale:
    def __init__(self, name, notes):
        self.name = name
        self.notes = notes
        self.note_amount = len(notes)


class Scales:
    def __init__(self):
        self.MAJOR = scale([" Major"], [0, 2, 4, 5, 7, 9, 11])
        self.MINOR_NAT = scale([" Natural Minor"], [0, 2, 3, 5, 7, 8, 10])
        self.MINOR_HAR = scale([" Harmonic Minor"], [0, 2, 3, 5, 7, 8, 11])

    def getList(self):
        return [self.MAJOR, self.MINOR_NAT, self.MINOR_HAR]


class Chords:
    def __init__(self):
        self.MAJOR = chord(["", "Maj", "M", "!"], [0, 4, 7])
        self.MINOR = chord(["m"], [0, 3, 7])
        self.AUGMENTED = chord(["aug"], [0, 4, 8])
        self.DIMINISHED = chord(["dim"], [0, 3, 6])
        self.SUS2 = chord(["sus2"], [0, 2, 7])
        self.SUS4 = chord(["sus4"], [0, 5, 7])
        self.MAJ7 = chord(["M^7^", "Ma^7^", "maj^7^"], [0, 4, 7, 11])
        self.MIN7 = chord(["m^7^", "min^7^"], [0, 3, 7, 10])
        self.DOM7 = chord(["^7^"], [0, 4, 7, 10])
        self.HALFDIM = chord(["min7@^5^", "&"], [0, 3, 6, 10])
        self.DIM7 = chord(["dim^7^"], [0, 3, 6, 9])
        self.AUG7 = chord(["aug^7^"], [0, 4, 8, 10])

    def getList(self):
        return [
            self.MAJOR,
            self.MINOR,
            self.AUGMENTED,
            self.DIMINISHED,
            self.SUS2,
            self.SUS4,
            self.MAJ7,
            self.MIN7,
            self.DOM7,
            self.HALFDIM,
            self.DIM7,
            self.AUG7,
        ]


def solution_generator(type):
    if type == 1:
        answer_type = Chords()
    elif type == 2:
        answer_type = Scales()

    key = randint(0, 11)
    answer = choice(answer_type.getList())

    for i in range(len(answer.notes)):
        answer.notes[i] += key
        answer.notes[i] %= 12

    answer.name = number_to_note(answer.notes[0]) + choice(answer.name)

    return answer


def check_answer(key_array, answer):

    key_array_new = sorted(key_array).copy()

    for i in range(len(key_array_new)):
        key_array_new[i] = key_array_new[i] % 12

    if (
        list(set(answer)) == list(set(key_array_new))
        and answer[0] == key_array_new[0] % 12
    ):
        return True
    else:
        return False


def check_scale(key_array, answer):

    key_array_new = sorted(key_array).copy()

    for i in range(len(key_array_new)):
        key_array_new[i] = key_array_new[i] % 12

    if (
        list(set(answer)) == list(set(key_array_new))
        and answer[0] == key_array_new[0] % 12
    ):
        return True
    else:
        return False


def key_randomize(answer_chord, keyboardHandler, window):

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("paused")
                    pause_screen(window, keyboardHandler)
        if keyboardHandler.midi_input.poll() is True:
            data = read_midi_input(keyboardHandler.midi_input)
            keyboardHandler.handle_note(data)
            if check_answer(keyboardHandler.pressed_keys, answer_chord.notes) is True:
                return 1


def pause_screen(window, keyboardHandler):
    window.draw_pause_screen()
    keyboardHandler.remove_all()

    while 1:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    window.undraw_pause_screen()
                    keyboardHandler.midi_input.read(1024)
                    return 1


def scale_game(answer_scale, keyboardHandler):
    starting_note = None
    highest_note = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

        if keyboardHandler.midi_input.poll() is True:
            data = read_midi_input(keyboardHandler.midi_input)
            keyboardHandler.handle_note(data)
            if (
                starting_note is None
                and data.note_number % 12 == answer_scale.notes[0]
                and data.in_device != 176
            ):
                starting_note = data.note_number
            if (
                highest_note is None or data.note_number > highest_note
            ) and data.in_device != 176:
                highest_note = data.note_number
            if (
                data.note_number == starting_note
                and highest_note % 12 == answer_scale.notes[0]
                and highest_note > starting_note
            ):
                print("Correct")
                return 1


def create_window():

    (width, height) = (1000, 500)
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("MIDI GAME")
    draw_surface = new_surface(window)
    return draw_surface


def run_game(window):
    keyboardHandler = newController(1, 1)
    game_event = 1
    game_type = 1

    while game_event > 0:
        window.window.fill((255, 255, 255))

        answer = solution_generator(game_type)

        window.write_on_window(answer.name)
        if game_type == 1:
            game_event = key_randomize(answer, keyboardHandler, window)
        elif game_type == 2:
            game_event = scale_game(answer, keyboardHandler)

    keyboardHandler.closeHandler()


def print_devices():
    for n in range(midi.get_count()):
        print(n, midi.get_device_info(n))


def number_to_note(number):

    notes_list = [
        ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"],
        ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"],
    ]

    notes = notes_list[randint(0, 1)]
    return notes[number % 12]


# reads a midi object from the input stream
def read_midi_input(input_device):
    event = input_device.read(1)[0]

    in_device = event[0][0]
    note_number = event[0][1]
    velocity = event[0][2]
    channel = event[0][3]
    timestamp = event[1]

    data = note(in_device, note_number, velocity, channel, timestamp)

    return data


def main():
    # initialize pygame modules
    pygame.init()

    # run game
    window = create_window()
    run_game(window)

    pygame.display.quit()
    pygame.quit()


main()
