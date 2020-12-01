# This currently assumes a 16-bit, 44100Hz .wav file

import os
import math
from waveTools import *
import config

# TODO: Clarify that floating point rounding errors are fine

#########################
# FUNCTIONS TO COMPLETE #
#########################

def makeSofter(channel):
    '''
    '''
    # TODO: Write me

def chipmunk(channel):
    '''
    '''
    # TODO: Write me

def removeVocals(leftChannel, rightChannel):
    '''
    '''
    # TODO: Write me

def reverse(channel):
    '''
    '''
    # TODO: Write me

def twoSampleDelay(channel, oneSampleBack, twoSampleBack):
    '''
    '''
    # TODO: Write me

def ohYeah(channel, prevSample):
    '''
    '''
    # TODO: Write me

def crescendo(channel, startVolume, endVolume):
    '''
    '''
    # TODO: Write me


############
# OPTIONAL #
############

def custom(channel):
    '''
    Placeholder.
    '''
    # OPTIONAL: Write your own effect!
    return []

################################
# STARTER CODE - DO NOT MODIFY #
################################

def processEffect(frames, effect, source, prevTwoFrames, fadeStartPoint):
    '''
    Given some frames and an effect to apply, applies that affect to the
    given source audio. Also needs to know the last two frames from the
    previous chunk so that effects which use previous frames can work
    smoothly, and the fade start point so that crescendo can be applied
    smoothly across multiple chunks.
    '''
    newPrevTwoFrames = [
        (frames[0][-1], frames[1][-1]),
        (frames[0][-2], frames[1][-2])
    ]
    fadeEndPoint = fadeStartPoint # not elegant but oh well...

    if effect == "makeSofter":
        lc = makeSofter(frames[0])
        rc = makeSofter(frames[1])
        target_length = len(frames[0])
        processedFrames = lc, rc
    elif effect == "removeVocals":
        processedChannel = removeVocals(frames[0], frames[1])
        processedFrames = [processedChannel, processedChannel]
        target_length = len(frames[0])
    elif effect == "chipmunk":
        lc = chipmunk(frames[0])
        rc = chipmunk(frames[1])
        target_length = math.ceil(len(frames[0]) / 2)
        processedFrames = lc, rc
    elif effect == "reverse":
        lc = reverse(frames[0])
        rc = reverse(frames[1])
        target_length = len(frames[0])
        processedFrames = lc, rc
    elif effect == "ohYeah":
        lc = ohYeah(frames[0], prevTwoFrames[0][0])
        rc = ohYeah(frames[1], prevTwoFrames[0][1])
        target_length = len(frames[0]) * 2
        processedFrames = lc, rc
    elif effect == "twoSampleDelay":
        processedFrames = []
        lc = twoSampleDelay(frames[0], prevTwoFrames[0][0], prevTwoFrames[1][0])
        rc = twoSampleDelay(frames[1], prevTwoFrames[0][1], prevTwoFrames[1][1])
        processedFrames = lc, rc
        prevTwoFrames = newPrevTwoFrames
        target_length = len(frames[0])
    elif effect == "crescendo":
        totalFadeTime = source.getnframes()
        # For certain duration: <time> * config.SAMPLE_RATE
        fadeEndPoint = len(frames[0])/(totalFadeTime) + fadeStartPoint
        if fadeEndPoint <= 1:
            lc = crescendo(frames[0], fadeStartPoint, fadeEndPoint)
            rc = crescendo(frames[1], fadeStartPoint, fadeEndPoint)
            processedFrames = lc, rc
        else:
            processedFrames = frames
        target_length = len(frames[0])
    elif effect == "custom":
        lc = custom(frames[0])
        rc = custom(frames[1])
        target_length = None
        processedFrames = lc, rc
    else:
        raise ValueError(
            "You have entered the name of an effect that is invalid.  " +
            "Please check your spelling."
        )
    # Error checking
    if any(frame > 1.0 or frame < -1.0 for frame in processedFrames):
        raise ValueError(
            "Your effect returned a sample value that was too"
          + "large (> 1.0) or too small (< -1.0)."
        )
    if (
        target_length != None
    and len(processedFrames[0]) != target_length
    ):
        raise ValueError(
            (
                "Your effect returned a list of {} samples, when it"
              + "should have returned {} samples."
            ).format(
                len(processedFrames[0]),
                target_length
            )
        )
    return processedFrames, newPrevTwoFrames, fadeEndPoint


def processFile(sourcePath, destinationPath, effect):
    '''
    Loads data from the fie at the given source path, applies the given
    affect, and saves a processed file at the given destination path.
    Also, if the `simpleaudio` module is available, this will play the
    processed audio directly using the system's speakers; if not, it
    prints out a message indicating that `simpleaudio` could be
    installed.
    '''
    source, numFrames = openWaveFile(sourcePath)
    destination = openDestinationFile(destinationPath, source)
    wavedata = b""

    # necessary for "reverse"
    frameRange = range(0, numFrames, config.FRAME_CHUNK_SIZE)
    if effect == "reverse":
        frameRange = reversed(frameRange)

    # necessary for "crescendo"
    fadeStartPoint = 0 # need to keep track

    # necessary for "twoSampleDelay" and "ohYeah"
    prevTwoFrames = [(0, 0), (0, 0)]
    # [(lc: n - 1), (rc: n - 1), (lc: n - 2, rc: n - 2)]

    # process each FRAME_CHUNK_SIZE window of data in the wave file
    for framePointer in frameRange:
        # Get config.FRAME_CHUNK_SIZE frames from wave file
        # Last window will be <= FRAME_CHUNK_SIZE
        frames, numOfSamples = getFrames(source, framePointer)
        if numOfSamples == 0 and numFrames != framePointer + numOfSamples:
            print(
                "Warning: Your .wav file appears to be corrupted! Are"
              + " you sure your download was completed without errors?"
            )
            print(
                (
                    "Your .wav file says it contains {} frames, but we"
                    " only found {}."
                ).format(numFrames, framePointer + numOfSamples)
            )
        splitFrames = separateChannels(frames, config.NUM_CHANNELS)

        # Get process effect on window
        data = processEffect(
            splitFrames,
            effect,
            source,
            prevTwoFrames,
            fadeStartPoint
        )
        processedFrames, newPrevTwoFrames, newStartPoint = data

        # Reconstruct window into list of interleaved samples
        outputFrames = reconstructFrames(processedFrames)

        # Write data
        fmt = "<" + "h" * len(outputFrames) # generally the same as numOfSamples
        coded = struct.pack(fmt, *outputFrames) # * is the unpacking operator
        destination.writeframes(coded)
        if simpleaudio is not None:
            wavedata += coded

        # Update data for twoSampleDelay and crescendo
        prevTwoFrames, fadeStartPoint = newPrevTwoFrames, newStartPoint

    destination.close()
    source.close()

    if simpleaudio is None:
        print(
            "Note: if you install the `simpleaudio` package via the"
          + " 'Manage packages' option in the 'Tools' menu, the"
          + " the processed result will be played directly in Python."
        )
    else:
        print("Playing the result directly using `simpleaudio`...")
        wo = simpleaudio.WaveObject(
            wavedata,
            config.NUM_CHANNELS,
            config.SAMPLE_WIDTH,
            config.SAMPLE_RATE
        )
        wo.play().wait_done()


###############################################
# TESTING CODE - COMMENT AND UNCOMMENT THINGS #
###############################################

def test():
    """
    Standard testing function: gets run when the file is
    run, but not when it's being graded.
    """
    # Soundfile sources and destinations
    soundsdir = os.path.join(os.getcwd(), "sounds")
    pokerSourcePath = os.path.join(soundsdir, "poker.wav");
    pokerDestinationPath = os.path.join(soundsdir, "poker_proc.wav");
    helloSourcePath = os.path.join(soundsdir, "hello.wav");
    helloDestinationPath = os.path.join(soundsdir, "hello_proc.wav");
    prayerSourcePath = os.path.join(soundsdir, "prayer.wav");
    prayerDestinationPath = os.path.join(soundsdir, "prayer_proc.wav");
    distanceSourcePath = os.path.join(soundsdir, "distance.wav");
    distanceDestinationPath = os.path.join(soundsdir, "distance_proc.wav");

    print("Start testing...")

    # Test makeSofter
    # print(makeSofter([0, -0.2, 0.4, -0.6]))
    # print(makeSofter([]))
    # print(makeSofter([0.1, -0.4]))
    # processFile(pokerSourcePath, pokerDestinationPath, "makeSofter")
    # processFile(distanceSourcePath, distanceDestinationPath, "makeSofter")

    # Test chipmunk
    # print(chipmunk([0, -0.2, 0.4, -0.6]))
    # print(chipmunk([-0.3, 0.2, 0.1]))
    # print(chipmunk([]))
    # processFile(prayerSourcePath, prayerDestinationPath, "chipmunk")
    # processFile(helloSourcePath, helloDestinationPath, "chipmunk")

    # Test removeVocals
    # print(removeVocals([0.1, 0.5, -0.2, 0.3], [-0.1, -0.6, 0.3, 0.1]))
    # print(removeVocals([0.7, 0.2], [0.3, -0.4]))
    # print(removeVocals([], []))
    # processFile(distanceSourcePath, distanceDestinationPath, "removeVocals")
    # processFile(pokerSourcePath, pokerDestinationPath, "removeVocals")

    # Test reverse
    # print(reverse([0.1, -0.2, 0.5, 0.2]))
    # print(reverse([0.1, -0.9, 0.3]))
    # print(reverse([]))
    # processFile(pokerSourcePath, pokerDestinationPath, "reverse")
    # processFile(prayerSourcePath, prayerDestinationPath, "reverse")

    # Test twoSampleDelay
    # print(twoSampleDelay([0.1, -0.2, 0.5, 0.6], -0.7, -0.9))
    # print(twoSampleDelay([0.1, 0.6, -0.2, 0.25, 0.3], -0.5, 0))
    # print(twoSampleDelay([], 0.1, 0.2))
    # processFile(prayerSourcePath, prayerDestinationPath, "twoSampleDelay")
    # processFile(pokerSourcePath, pokerDestinationPath, "twoSampleDelay")

    # Test ohYeah
    # print(ohYeah([0.5, -0.1, 0.4], -0.1))
    # print(ohYeah([0.1], 0.1))
    # print(ohYeah([], -0.9))
    # processFile(helloSourcePath, helloDestinationPath, "ohYeah")
    # processFile(pokerSourcePath, pokerDestinationPath, "ohYeah")

    # Test crescendo
    # print(crescendo([1.0, 1.0, 1.0], 0.2, 0.8))
    # print(crescendo([0.9, 0.4, 0.6, 0.2], 0, 1))
    # print(crescendo([], 0, 1))
    # processFile(helloSourcePath, helloDestinationPath, "crescendo")
    # processFile(prayerSourcePath, prayerDestinationPath, "crescendo")

    # Test custom
    # processFile(pokerSourcePath, pokerDestinationPath, "custom")
    # processFile(helloSourcePath, helloDestinationPath, "custom")

    print("...end testing.")

if __name__ == '__main__':
    test()
