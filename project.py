"""
FINAL PROJECT
Name(s): [REDACTED]
PID(s):  [REDACTED]
Sources: Lecture slides
"""

import numpy as np
import os
from PIL import Image
import wave
import struct
import matplotlib.pyplot as plt

NUM_CHANNELS = 3


# --------------------------------------------------------------------------- #

# YOU SHOULD NOT MODIFY THESE TWO METHODS

def img_read_helper(path):
    """
    Creates an RGBImage object from the given image file
    """
    # Open the image in RGB
    img = Image.open(path).convert("RGB")
    # Convert to numpy array and then to a list
    matrix = np.array(img).tolist()
    # Use student's code to create an RGBImage object
    return RGBImage(matrix)


def img_save_helper(path, image):
    """
    Saves the given RGBImage instance to the given path
    """
    # Convert list to numpy array
    img_array = np.array(image.get_pixels())
    # Convert numpy array to PIL Image object
    img = Image.fromarray(img_array.astype(np.uint8))
    # Save the image object to path
    img.save(path)


# --------------------------------------------------------------------------- #

# Part 1: RGB Image #
class RGBImage:
    """
    Represents an image in RGB format
    """

    def __init__(self, pixels):
        """
        Initializes a new RGBImage object

        # Test with non-rectangular list
        >>> pixels = [
        ...              [[255, 255, 255], [255, 255, 255]],
        ...              [[255, 255, 255]]
        ...          ]
        >>> RGBImage(pixels)
        Traceback (most recent call last):
        ...
        TypeError

        # Test instance variables
        >>> pixels = [
        ...              [[255, 255, 255], [0, 0, 0]]
        ...          ]
        >>> img = RGBImage(pixels)
        >>> img.pixels
        [[[255, 255, 255], [0, 0, 0]]]
        >>> img.num_rows
        1
        >>> img.num_cols
        2
        """
        # YOUR CODE GOES HERE #
        # Raise exceptions here
        if (not isinstance(pixels, list) or len(pixels) == 0 or any(not\
            isinstance(row, list) or len(row) == 0 for row in pixels) or \
            any(len(row) != len(pixels[0]) for row in pixels) or any(not\
            isinstance(pixel, list) or len(pixel) != 3 for row in pixels for\
            pixel in row)):
            raise TypeError()

        if any(not all(isinstance(value, int) and 0 <= value <= 255 for value\
            in pixel) for row in pixels for pixel in row):
            raise ValueError()
        self.pixels = pixels
        self.num_rows = len(pixels)
        self.num_cols = len(pixels[0])

    def size(self):
        """
        Returns the size of the image in (rows, cols) format

        # Make sure to complete __init__ first
        >>> pixels = [
        ...              [[255, 255, 255], [0, 0, 0]]
        ...          ]
        >>> img = RGBImage(pixels)
        >>> img.size()
        (1, 2)
        """
        # YOUR CODE GOES HERE #
        return (self.num_rows, self.num_cols)

    def get_pixels(self):
        """
        Returns a copy of the image pixel array

        # Make sure to complete __init__ first
        >>> pixels = [
        ...              [[255, 255, 255], [0, 0, 0]]
        ...          ]
        >>> img = RGBImage(pixels)
        >>> img_pixels = img.get_pixels()

        # Check if this is a deep copy
        >>> img_pixels                               # Check the values
        [[[255, 255, 255], [0, 0, 0]]]
        >>> id(pixels) != id(img_pixels)             # Check outer list
        True
        >>> id(pixels[0]) != id(img_pixels[0])       # Check row
        True
        >>> id(pixels[0][0]) != id(img_pixels[0][0]) # Check pixel
        True
        """
        # YOUR CODE GOES HERE #
        return [[pixel[:] for pixel in row] for row in self.pixels]

    def copy(self):
        """
        Returns a copy of this RGBImage object

        # Make sure to complete __init__ first
        >>> pixels = [
        ...              [[255, 255, 255], [0, 0, 0]]
        ...          ]
        >>> img = RGBImage(pixels)
        >>> img_copy = img.copy()

        # Check that this is a new instance
        >>> id(img_copy) != id(img)
        True
        """
        # YOUR CODE GOES HERE #
        return RGBImage(self.get_pixels())

    def get_pixel(self, row, col):
        """
        Returns the (R, G, B) value at the given position

        # Make sure to complete __init__ first
        >>> pixels = [
        ...              [[255, 255, 255], [0, 0, 0]]
        ...          ]
        >>> img = RGBImage(pixels)

        # Test with an invalid index
        >>> img.get_pixel(1, 0)
        Traceback (most recent call last):
        ...
        ValueError

        # Run and check the returned value
        >>> img.get_pixel(0, 0)
        (255, 255, 255)
        """
        # YOUR CODE GOES HERE #
        if not isinstance(row, int) or not isinstance(col, int):
            raise TypeError()
        if row < 0 or row >= self.num_rows or col < 0 or col >= \
            self.num_cols:
            raise ValueError()

        return tuple(self.pixels[row][col])

    def set_pixel(self, row, col, new_color):
        """
        Sets the (R, G, B) value at the given position

        # Make sure to complete __init__ first
        >>> pixels = [
        ...              [[255, 255, 255], [0, 0, 0]]
        ...          ]
        >>> img = RGBImage(pixels)

        # Test with an invalid new_color tuple
        >>> img.set_pixel(0, 0, (256, 0, 0))
        Traceback (most recent call last):
        ...
        ValueError

        # Check that the R/G/B value with negative is unchanged
        >>> img.set_pixel(0, 0, (-1, 0, 0))
        >>> img.pixels
        [[[255, 0, 0], [0, 0, 0]]]
        """
        # YOUR CODE GOES HERE #
        if not isinstance(row, int) or not isinstance(col, int):
            raise TypeError()
        if row < 0 or row >= self.num_rows or col < 0 or col >= self.num_cols:
            raise ValueError()
        if (not isinstance(new_color, tuple) or len(new_color) != 3 or not\
            all(isinstance(value, int) for value in new_color)):
            raise TypeError()
        if any(value > 255 for value in new_color):
            raise ValueError()

        for i in range(3):
            if new_color[i] >= 0:
                self.pixels[row][col][i] = new_color[i]

# Part 2: Image Processing Template Methods #
class ImageProcessingTemplate:
    """
    Contains assorted image processing methods
    Intended to be used as a parent class
    """

    def __init__(self):
        """
        Creates a new ImageProcessingTemplate object

        # Check that the cost was assigned
        >>> img_proc = ImageProcessingTemplate()
        >>> img_proc.cost
        0
        """
        # YOUR CODE GOES HERE #
        self.cost = 0

    def get_cost(self):
        """
        Returns the current total incurred cost

        # Check that the cost value is returned
        >>> img_proc = ImageProcessingTemplate()
        >>> img_proc.cost = 50 # Manually modify cost
        >>> img_proc.get_cost()
        50
        """
        # YOUR CODE GOES HERE #
        return self.cost

    def negate(self, image):
        """
        Returns a negated copy of the given image

        # Check if this is returning a new RGBImage instance
        >>> img_proc = ImageProcessingTemplate()
        >>> pixels = [
        ...              [[255, 255, 255], [0, 0, 0]]
        ...          ]
        >>> img = RGBImage(pixels)
        >>> img_negate = img_proc.negate(img)
        >>> id(img) != id(img_negate) # Check for new RGBImage instance
        True

        # The following is a description of how this test works
        # 1 Create a processor
        # 2/3 Read in the input and expected output
        # 4 Modify the input
        # 5 Compare the modified and expected
        # 6 Write the output to file
        # You can view the output in the img/out/ directory
        >>> img_proc = ImageProcessingTemplate()                            # 1
        >>> img = img_read_helper('img/test_image_32x32.png')                 # 2
        >>> img_exp = img_read_helper('img/exp/test_image_32x32_negate.png')  # 3
        >>> img_negate = img_proc.negate(img)                               # 4
        >>> img_negate.pixels == img_exp.pixels # Check negate output       # 5
        True
        >>> img_save_helper('img/out/test_image_32x32_negate.png', img_negate)# 6
        """
        # YOUR CODE GOES HERE #
        return RGBImage([[[255 - r, 255 - g, 255 - b] for r, g, b in row] for\
            row in image.pixels])

    def grayscale(self, image):
        """
        Returns a grayscale copy of the given image

        # See negate for info on this test
        # You can view the output in the img/out/ directory
        >>> img_proc = ImageProcessingTemplate()
        >>> img = img_read_helper('img/test_image_32x32.png')
        >>> img_exp = img_read_helper('img/exp/test_image_32x32_gray.png')
        >>> img_gray = img_proc.grayscale(img)
        >>> img_gray.pixels == img_exp.pixels # Check grayscale output
        True
        >>> img_save_helper('img/out/test_image_32x32_gray.png', img_gray)
        """
        # YOUR CODE GOES HERE #
        return RGBImage([[[avg := (r + b + g) // 3] * 3 for r, g, b, in row]\
         for row in image.pixels])

    def rotate_180(self, image):
        """
        Returns a rotated version of the given image

        # See negate for info on this test
        # You can view the output in the img/out/ directory
        >>> img_proc = ImageProcessingTemplate()
        >>> img = img_read_helper('img/test_image_32x32.png')
        >>> img_exp = img_read_helper('img/exp/test_image_32x32_rotate.png')
        >>> img_rotate = img_proc.rotate_180(img)
        >>> img_rotate.pixels == img_exp.pixels # Check rotate_180 output
        True
        >>> img_save_helper('img/out/test_image_32x32_rotate.png', img_rotate)
        """
        # YOUR CODE GOES HERE #
        return RGBImage([row[::-1] for row in image.pixels[::-1]])

    def get_average_brightness(self, image):
        """
        Returns the average brightness for the given image

        >>> img_proc = ImageProcessingTemplate()
        >>> img = img_read_helper('img/test_image_32x32.png')
        >>> img_proc.get_average_brightness(img)
        86
        """
        # YOUR CODE GOES HERE #
        total_bright = sum((r + b + g) // 3 for row in image.pixels for r, g, \
            b in row)
        return total_bright // (len(image.pixels) * len(image.pixels[0]))

    def adjust_brightness(self, image, intensity):
        """
        Returns a new image with adjusted brightness level

        >>> img_proc = ImageProcessingTemplate()
        >>> img = img_read_helper('img/test_image_32x32.png')
        >>> img_exp = img_read_helper('img/exp/test_image_32x32_adjusted.png')
        >>> img_adjust = img_proc.adjust_brightness(img, 1.2)
        >>> img_adjust.pixels == img_exp.pixels # Check adjust_brightness
        True
        >>> img_save_helper('img/out/test_image_32x32_adjusted.png', img_adjust)
        """
        # YOUR CODE GOES HERE #
        if not isinstance(intensity, float):
            raise TpeError()
        def adjust_channel(value):
            return min(255, max(0, int(value * intensity)))
        return RGBImage([[[adjust_channel(r), adjust_channel(g), \
            adjust_channel(b)] for r, g, b in row] for row in image.pixels])


# Part 3: Standard Image Processing Methods #
class StandardImageProcessing(ImageProcessingTemplate):
    """
    Represents a standard tier of an image processor
    """

    def __init__(self):
        """
        Creates a new StandardImageProcessing object

        # Check that the cost was assigned
        >>> img_proc = StandardImageProcessing()
        >>> img_proc.cost
        0
        """
        # YOUR CODE GOES HERE #
        self.cost = 0
        self.free_calls = 0

    def apply_cost(self, cost):
        if self.free_calls > 0:
            self.free_calls -= 1
        else:
            self.cost += cost

    def negate(self, image):
        """
        Returns a negated copy of the given image

        # Check the expected cost
        >>> img_proc = StandardImageProcessing()
        >>> img_in = img_read_helper('img/square_32x32.png')
        >>> negated = img_proc.negate(img_in)
        >>> img_proc.get_cost()
        5

        # Check that negate works the same as in the parent class
        >>> img_proc = StandardImageProcessing()
        >>> img = img_read_helper('img/test_image_32x32.png')
        >>> img_exp = img_read_helper('img/exp/test_image_32x32_negate.png')
        >>> img_negate = img_proc.negate(img)
        >>> img_negate.pixels == img_exp.pixels # Check negate output
        True
        """
        # YOUR CODE GOES HERE #
        self.apply_cost(5)
        return super().negate(image)


    def grayscale(self, image):
        """
        Returns a grayscale copy of the given image

        """
        # YOUR CODE GOES HERE #
        self.apply_cost(6)
        return super().grayscale(image)

    def rotate_180(self, image):
        """
        Returns a rotated version of the given image
        """
        # YOUR CODE GOES HERE #
        self.apply_cost(10)
        return super().rotate_180(image)

    def adjust_brightness(self, image, intensity):
        """
        Returns a new image with adjusted brightness level
        """
        # YOUR CODE GOES HERE #
        self.apply_cost(1)
        return super().adjust_brightness(image)

    def redeem_coupon(self, amount):
        """
        Makes the given number of methods calls free

        # Check that the cost does not change for a call to negate
        # when a coupon is redeemed
        >>> img_proc = StandardImageProcessing()
        >>> img = img_read_helper('img/test_image_32x32.png')
        >>> img_proc.redeem_coupon(1)
        >>> img = img_proc.rotate_180(img)
        >>> img_proc.get_cost()
        0
        """
        # YOUR CODE GOES HERE #
        if not isinstance(amount, int):
            raise TypeError('Amount must be an integer')
        if amount <= 0:
            raise ValueError('Amount must be a positive integer')
        self.free_calls += amount


# Part 4: Premium Image Processing Methods #
class PremiumImageProcessing(ImageProcessingTemplate):
    """
    Represents a paid tier of an image processor
    """

    def __init__(self):
        """
        Creates a new PremiumImageProcessing object

        # Check the expected cost
        >>> img_proc = PremiumImageProcessing()
        >>> img_proc.get_cost()
        50
        """
        # YOUR CODE GOES HERE #
        self.cost = 50

    def pixelate(self, image, block_dim):
        """
        Returns a pixelated version of the image, where block_dim is the size of 
        the square blocks.

        >>> img_proc = PremiumImageProcessing()
        >>> img = img_read_helper('img/test_image_32x32.png')
        >>> img_pixelate = img_proc.pixelate(img, 4)
        >>> img_exp = img_read_helper('img/exp/test_image_32x32_pixelate.png')
        >>> img_exp.pixels == img_pixelate.pixels # Check pixelate output
        True
        >>> img_save_helper('img/out/test_image_32x32_pixelate.png', img_pixelate)
        """
        # YOUR CODE GOES HERE #
        height, width = len(image.pixels), len(image.pixels[0])
        new_pixels = [[pixel[:] for pixel in row] for row in image.pixels]

        for i in range(0, height, block_dim):
            for j in range(0, width, block_dim):
                block = []
                for x in range(i, min(i + block_dim, height)):
                    for y in range(j, min(j + block_dim, width)):
                        block.append(image.pixels[x][y])

                avg_color = np.mean(block, axis = 0).astype(int).tolist()

                for x in range(i, min(i + block_dim, height)):
                    for y in range(j, min(j + block_dim, width)):
                        new_pixels[x][y] = avg_color
        return RGBImage(new_pixels)

    def edge_highlight(self, image):
        """
        Returns a new image with the edges highlighted

        >>> img_proc = PremiumImageProcessing()
        >>> img = img_read_helper('img/test_image_32x32.png')
        >>> img_edge = img_proc.edge_highlight(img)
        >>> img_exp = img_read_helper('img/exp/test_image_32x32_edge.png')
        >>> img_exp.pixels == img_edge.pixels # Check edge_highlight output
        True
        >>> img_save_helper('img/out/test_image_32x32_edge.png', img_edge)
        """
        # YOUR CODE GOES HERE #
        height, width = len(image.pixels), len(image.pixels[0])

        grayscale_pixels = [[sum(pixel) // 3 for pixel in row] for row in\
        image.pixels]

        kernel = [
            [-1, -1, -1],
            [-1, 8, -1],
            [-1, -1, -1]
        ]

        new_pixels = [[0] * width for i in range(height)]

        for i in range(height):
            for j in range(width):
                masked_value = 0
                for ki in range(-1, 2):
                    for kj in range(-1, 2):
                        ni, nj = i + ki, j + kj
                        if 0 <= ni < height and 0 <= nj < width:
                            masked_value += grayscale_pixels[ni][nj] * \
                            kernel[ki +1][kj +1]
                masked_value = max(0, min(255, masked_value))
                new_pixels[i][j] = [masked_value] * 3
        return RGBImage(new_pixels)


# --------------------------------------------------------------------------- #

# YOU SHOULD NOT MODIFY THESE THREE METHODS

def audio_read_helper(path, visualize=False):
    """
    Creates an AudioWave object from the given WAV file
    """
    with wave.open(path, "rb") as wav_file:
        num_frames = wav_file.getnframes()  # Total number of frames
        num_channels = wav_file.getnchannels()  # Number of channels (1 for mono, 2 for stereo)
        sample_width = wav_file.getsampwidth()  # Number of bytes per sample (e.g., 2 for 16-bit)
        
        # Read the frames as bytes
        raw_bytes = wav_file.readframes(num_frames)
        
        # Determine the format string for struct.unpack()
        fmt = f"{num_frames * num_channels}{'h' if sample_width == 2 else 'B'}"
        
        # Convert bytes to a list of integers
        audio_data = list(struct.unpack(fmt, raw_bytes))

    return AudioWave(audio_data)


def audio_save_helper(path, audio, sample_rate = 44100):
    """
    Saves the given AudioWave instance to the given path as a WAV file
    """
    sample_rate = 44100  # 44.1 kHz standard sample rate
    num_channels = 1  # Mono
    sample_width = 2  # 16-bit PCM

    # Convert list to bytes
    byte_data = struct.pack(f"{len(audio.wave)}h", *audio.wave)
    with wave.open(path, "wb") as wav_file:
        wav_file.setnchannels(num_channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(byte_data)


def audio_visualizer(path, start=0, end=5):
    """
    Visualizes the given WAV file
    x-axis: time (sec)
    y-axis: wave amplitude
    ---
    Parameters: 
        path (str): path to the WAV file
        start (int): start timestamp in seconds, default 0
        end (int): end timestamp in seconds, default 5
    """
    with wave.open(path, "rb") as wav_file:
        sample_freq = wav_file.getframerate()  # Sample rate
        n_samples = wav_file.getnframes()  # Total number of samples
        duration = n_samples/sample_freq # Duration of audio, in seconds

        if any([type(param) != int for param in [start, end]]):
            raise TypeError("start and end should be integers.")
        if (start < 0) or (start > duration) or (end < 0) or (end > duration) or start >= end:
            raise ValueError(f"Invalid timestamp: start and end should be between 0 and {int(duration)}, and start < end.")
        
        num_frames = wav_file.getnframes()  # Total number of frames
        num_channels = wav_file.getnchannels()  # Number of channels (1 for mono, 2 for stereo)
        sample_width = wav_file.getsampwidth()  # Number of bytes per sample (e.g., 2 for 16-bit)
        
        # Extract audio wave as list
        raw_bytes = wav_file.readframes(num_frames)
        fmt = f"{num_frames * num_channels}{'h' if sample_width == 2 else 'B'}"
        audio_data = list(struct.unpack(fmt, raw_bytes))

        # Plot the audio wave
        time = np.linspace(start, end, num=(end - start)*sample_freq)
        audio_data = audio_data[start*sample_freq:end*sample_freq]
        plt.figure(figsize=(15, 5))
        plt.ylim([-32768, 32767])
        plt.plot(time, audio_data)
        plt.title(f'Audio Plot of {path} from {start}s to {end}s')
        plt.ylabel('sound wave')
        plt.xlabel('time (s)')
        plt.xlim(start, end)
        plt.show()


# --------------------------------------------------------------------------- #

# Part 5: Multimedia Processing
class AudioWave():
    """
        Represents audio through a 1-dimensional array of amplitudes
    """
    def __init__(self, amplitudes):
        self.wave = amplitudes

class PremiumPlusMultimediaProcessing(PremiumImageProcessing):
    """
        Represents the paid tier of multimedia processing
    """
    def __init__(self):
        """
        Creates a new PremiumPlusMultimediaProcessing object

        # Check the expected cost
        >>> multi_proc = PremiumPlusMultimediaProcessing()
        >>> multi_proc.get_cost()
        75
        """
        # YOUR CODE GOES HERE #
        self.cost = 75
    
    def reverse_song(self, audio):
        """
        Reverses the audio of the song.

        >>> multi_proc = PremiumPlusMultimediaProcessing()
        >>> audio = audio_read_helper('audio/one_summers_day.wav')
        >>> audio_reversed = multi_proc.reverse_song(audio)
        >>> audio_exp = audio_read_helper('audio/exp/one_summers_day_reversed.wav')
        >>> audio_exp.wave == audio_reversed.wave # Check reverse_song output
        True
        >>> audio_save_helper('audio/out/one_summers_day_reversed.wav', audio_reversed)
        """
        # YOUR CODE GOES HERE #
        if not isinstance(audio, AudioWave):
            raise TypeError()

        return AudioWave([audio.wave[i] for i in range(len(audio.wave) - 1, -1, -1)])
    
    def slow_down(self, audio, factor):
        """
        Slows down the song by a certain factor.

        >>> multi_proc = PremiumPlusMultimediaProcessing()
        >>> audio = audio_read_helper('audio/one_summers_day.wav')
        >>> audio_slow = multi_proc.slow_down(audio, 2)
        >>> audio_exp = audio_read_helper('audio/exp/one_summers_day_slow.wav')
        >>> audio_exp.wave == audio_slow.wave # Check slow_down output
        True
        >>> audio_save_helper('audio/out/one_summers_day_slow.wav', audio_slow)
        """
        # YOUR CODE GOES HERE #
        if not isinstance(audio, AudioWave) or not isinstance(factor, int) or factor < 1:
            raise TypeError()
            
        new_wave = [sample for sample in audio.wave for _ in range(factor)]
            
        return AudioWave(new_wave)
    
    def speed_up(self, audio, factor):
        """
        Speeds up the song by a certain factor.

        >>> multi_proc = PremiumPlusMultimediaProcessing()
        >>> audio = audio_read_helper('audio/one_summers_day.wav')
        >>> audio_sped_up = multi_proc.speed_up(audio, 2)
        >>> audio_exp = audio_read_helper('audio/exp/one_summers_day_sped_up.wav')
        >>> audio_exp.wave == audio_sped_up.wave # Check speed_up output
        True
        >>> audio_save_helper('audio/out/one_summers_day_sped_up.wav', audio_sped_up)
        """
        # YOUR CODE GOES HERE #
        if not isinstance(audio, AudioWave) or not isinstance(factor, int) or factor < 1:
            raise TypeError()
        
        new_wave = [audio.wave[i] for i in range(0, len(audio.wave), factor)]
        
        return AudioWave(new_wave)

    def reverb(self, audio):
        """
        Adds a reverb/echo effect to the song.

        >>> multi_proc = PremiumPlusMultimediaProcessing()
        >>> audio = audio_read_helper('audio/one_summers_day.wav')
        >>> audio_reverb = multi_proc.reverb(audio)
        >>> audio_exp = audio_read_helper('audio/exp/one_summers_day_reverb.wav')
        >>> audio_exp.wave == audio_reverb.wave # Check reverb output
        True
        >>> audio_save_helper('audio/out/one_summers_day_reverb.wav', audio_reverb)
        """
        # YOUR CODE GOES HERE #
        if not isinstance(audio, AudioWave):
            raise TypeError()

        filter_weights = [1.0, 0.8, 0.6, 0.4, 0.2]
        new_wave = [round(sum(audio.wave[i - j] * filter_weights[j] for j in range(len(filter_weights)) if i - j >= 0)) 
                    for i in range(len(audio.wave))]

        new_wave = [max(min(sample, 32767), -32768) for sample in new_wave]

        return AudioWave(new_wave)
        
    def clip_song(self, audio, start, end):
        """
        Clips a song based on a specified start and end.
        
        >>> multi_proc = PremiumPlusMultimediaProcessing()
        >>> audio = audio_read_helper('audio/one_summers_day.wav')
        >>> audio_clipped = multi_proc.clip_song(audio, 30, 70)
        >>> audio_exp = audio_read_helper('audio/exp/one_summers_day_clipped.wav')
        >>> audio_exp.wave == audio_clipped.wave # Check clip_song output
        True
        >>> audio_save_helper('audio/out/one_summers_day_clipped.wav', audio_clipped)
        """
        # YOUR CODE GOES HERE 
        if not isinstance(audio, AudioWave):
            raise TypeError()
        if not isinstance(start, int) or not isinstance(end, int):
            raise TypeError()
        if not (0 <= start <= 100) or not (0 <= end <= 100):
            raise ValueError()
        s, e = (len(audio.wave) * start) // 100, (len(audio.wave) * end) // 100 +1
        return AudioWave(audio.wave[s:e])




# Part 6: Image KNN Classifier #
class ImageKNNClassifier:
    """
    Represents a simple KNNClassifier
    """

    def __init__(self, k_neighbors):
        """
        Creates a new KNN classifier object
        """
        # YOUR CODE GOES HERE #
        self.k_neighbors = k_neighbors

    def fit(self, data):
        """
        Stores the given set of data and labels for later
        """
        # YOUR CODE GOES HERE #
        if len(data) < self.k_neighbors:
            raise ValueError()
        self.data = data
        
    def distance(self, image1, image2):
        """
        Returns the distance between the given images

        >>> img1 = img_read_helper('img/steve.png')
        >>> img2 = img_read_helper('img/knn_test_img.png')
        >>> knn = ImageKNNClassifier(3)
        >>> knn.distance(img1, img2)
        15946.312896716909
        """
        # YOUR CODE GOES HERE #
        if not isinstance(image1, RGBImage) or not isinstance(image2, RGBImage):
            raise TypeError("Both inputs must be instances of RGBImage.")

        if image1.size != image2.size:
            raise ValueError("Images must have the same dimensions.")

        squared_diff = (image1.pixels - image2.pixels) ** 2

        sum_squared_diff = squared_diff.sum()

        euclidean_distance = sum_squared_diff ** (1 / 2)

        return euclidean_distance


    def vote(self, candidates):
        """
        Returns the most frequent label in the given list

        >>> knn = ImageKNNClassifier(3)
        >>> knn.vote(['label1', 'label2', 'label2', 'label2', 'label1'])
        'label2'
        """
        # YOUR CODE GOES HERE #



    def predict(self, image):
        """
        Predicts the label of the given image using the labels of
        the K closest neighbors to this image

        The test for this method is located in the knn_tests method below
        """
        # YOUR CODE GOES HERE #
        


def knn_tests(test_img_path):
    """
    Function to run knn tests

    >>> knn_tests('img/knn_test_img.png')
    'nighttime'
    """
    # Read all of the sub-folder names in the knn_data folder
    # These will be treated as labels
    path = 'knn_data'
    data = []
    for label in os.listdir(path):
        label_path = os.path.join(path, label)
        # Ignore non-folder items
        if not os.path.isdir(label_path):
            continue
        # Read in each image in the sub-folder
        for img_file in os.listdir(label_path):
            train_img_path = os.path.join(label_path, img_file)
            img = img_read_helper(train_img_path)
            # Add the image object and the label to the dataset
            data.append((img, label))

    # Create a KNN-classifier using the dataset
    knn = ImageKNNClassifier(5)

    # Train the classifier by providing the dataset
    knn.fit(data)

    # Create an RGBImage object of the tested image
    test_img = img_read_helper(test_img_path)

    # Return the KNN's prediction
    predicted_label = knn.predict(test_img)
    return predicted_label
