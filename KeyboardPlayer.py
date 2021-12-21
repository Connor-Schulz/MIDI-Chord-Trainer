import pygame
import pygame.midi as midi


class KeyBoardController:
    def __init__(self, device_number, midi_instrument_sound_number):
        self.pedal_state = 0
        self.sustained_notes = []
        self.pressed_keys = []
        self.midi_input = None
        self.midi_output = None
        self.setup_midi(device_number, midi_instrument_sound_number)

    def setup_midi(self, device_number, midi_instrument_sound_number):
        midi.init()

        try:
            self.midi_input = midi.Input(device_number)
        except pygame.midi.MidiException:

            print(
                'ERROR: Could not connect to midi input device with id "{0}"'.format(
                    device_number
                )
            )
            exit(-1)

        try:
            self.midi_output = midi.Output(0)
        except (pygame.midi.MidiException):
            print("ERROR: Could not connect to given output device")
            exit(-1)

        self.midi_output.set_instrument(midi_instrument_sound_number - 1)

    def closeHandler(self):
        print("closing streams...")
        self.midi_output.close()
        self.midi_input.close()
        print("success")

        midi.quit()

    def handle_note(self, midi_data):
        if self.check_pedal(midi_data) != -1:
            self.remove_unneeded_notes()
            return

        if midi_data.velocity > 0:
            self.midi_output.note_on(midi_data.note_number, midi_data.velocity)
            self.pressed_keys.append(midi_data.note_number)
            self.sustained_notes.append(midi_data.note_number)

        else:
            try:
                self.pressed_keys.remove(midi_data.note_number)
            except ValueError:
                pass

        self.remove_unneeded_notes()

    def check_pedal(self, midi_data):
        if midi_data.in_device == 176:
            if midi_data.velocity > 0:
                self.pedal_state = 1
                return 1
            else:
                self.pedal_state = 0
                return 0
        return -1

    def remove_unneeded_notes(self):
        if self.pedal_state == 0:
            sustained_notes_copy = self.sustained_notes.copy()
            for note in sustained_notes_copy:
                if note not in self.pressed_keys:
                    try:
                        self.sustained_notes.remove(note)
                        self.midi_output.note_off(note)
                    except ValueError:
                        pass

    def remove_all(self):
        for note in self.sustained_notes:
            try:
                self.midi_output.note_off(note)
            except ValueError:
                pass
        self.sustained_notes = []
        self.pressed_keys = []


def newController(device_number, midi_instrument_sound_number):
    return KeyBoardController(device_number, midi_instrument_sound_number)
