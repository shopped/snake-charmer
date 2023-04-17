import numpy as np
import math

noteDictionary = {}
noteFrequencies = []
def make_note_dictionary():
    global noteDictionary, noteFrequencies
    notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

    noteIndex = 0
    currentFrequency = 110
    while currentFrequency < 7040:
        noteDictionary[currentFrequency] = notes[noteIndex]
        noteIndex += 1
        if noteIndex == len(notes):
            noteIndex = 0
        currentFrequency = currentFrequency * 2**(1/12)
    noteFrequencies = list(noteDictionary.keys())

    # print(noteDictionary)
    # print(noteFrequencies)

make_note_dictionary()

def frequency_to_note(value):
    if (value < 196 or value > 3951): # only will do A3 to A7, 220 -> 3520 Hz
        return 'x'
    
    noteDiffs = list(map(lambda x: abs(value - x), noteFrequencies))
    noteIndex = np.argmin(noteDiffs)
    return noteDictionary[noteFrequencies[noteIndex]]

def round_up_to_even(f):
    return int(math.ceil(f / 2.) * 2)

def gaussian_kernel1d(sigma, truncate=2.0):
    sigma = float(sigma)
    sigma2 = sigma * sigma
    # make the radius of the filter equal to truncate standard deviations
    radius = int(truncate * sigma + 0.5)
    exponent_range = np.arange(1)

    x = np.arange(-radius, radius+1)
    phi_x = np.exp(-0.5 / sigma2 * x ** 2)
    phi_x = phi_x / phi_x.sum()
    return phi_x

def get_smoothing_filter(FFT_window_size_ms, filter_length_ms, verbose = 0):
    buffer_length = round_up_to_even(filter_length_ms / FFT_window_size_ms)+1
    filter_sigma = buffer_length / 3  #How quickly the smoothing influence drops over the buffer length
    filter_weights = gaussian_kernel1d(filter_sigma)[:,np.newaxis]

    max_index = np.argmax(filter_weights)
    filter_weights = filter_weights[:max_index+1]
    filter_weights = filter_weights / np.mean(filter_weights)

    if verbose:
        min_fraction = 100*np.min(filter_weights)/np.max(filter_weights)
        print('\nApplying temporal smoothing to the FFT features...')
        print("Smoothing buffer contains %d FFT windows (sigma: %.3f) --> min_contribution: %.3f%%" %(buffer_length, filter_sigma, min_fraction))
        print("Filter weights:")
        for i, w in enumerate(filter_weights):
            print("%02d: %.3f" %(len(filter_weights)-i, w))

    return filter_weights

class numpy_data_buffer:
    """
    A fast, circular FIFO buffer in numpy with minimal memory interactions by using an array of index pointers
    """

    def __init__(self, n_windows, samples_per_window, dtype = np.float32, start_value = 0, data_dimensions = 1):
        self.n_windows = n_windows
        self.data_dimensions = data_dimensions
        self.samples_per_window = samples_per_window
        self.data = start_value * np.ones((self.n_windows, self.samples_per_window), dtype = dtype)

        if self.data_dimensions == 1:
            self.total_samples = self.n_windows * self.samples_per_window
        else:
            self.total_samples = self.n_windows

        self.elements_in_buffer = 0
        self.overwrite_index = 0

        self.indices = np.arange(self.n_windows, dtype=np.int32)
        self.last_window_id = np.max(self.indices)
        self.index_order = np.argsort(self.indices)

    def append_data(self, data_window):
        self.data[self.overwrite_index, :] = data_window

        self.last_window_id += 1
        self.indices[self.overwrite_index] = self.last_window_id
        self.index_order = np.argsort(self.indices)

        self.overwrite_index += 1
        self.overwrite_index = self.overwrite_index % self.n_windows

        self.elements_in_buffer += 1
        self.elements_in_buffer = min(self.n_windows, self.elements_in_buffer)

    def get_most_recent(self, window_size):
        ordered_dataframe = self.data[self.index_order]
        if self.data_dimensions == 1:
            ordered_dataframe = np.hstack(ordered_dataframe)
        return ordered_dataframe[self.total_samples - window_size:]

    def get_buffer_data(self):
        return self.data[:self.elements_in_buffer]