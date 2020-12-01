# Audio Toolkit

By Andrew Davis 
Additions by Peter Mawhorter

Inspired by http://nifty.stanford.edu/2012/zingaro-stereo-sound-processing/

## General Overview

This task involves writing several functions that will process
audio files with digital effects.  Our program will
work only on .wav audio files.  Most of the information in
a .wav audio file is simply a list of numbers that represent
the audio signals of songs, speech, or noise.  Yes, the
audio you listen to on your computer is stored as a list of
numbers!

Most audio files, including .wav files, have two lists of
numbers, one for the left speaker and one for the right.
These two lists are called **channels** and the numbers in
each list are called **samples**.  We will design most of our
audio effects to work on a single channel and the starter
code will handle processing both channels.

All written code should be done in the file `audioToolkit.py`.
Do not modify any of the starter code or the python files
`config.py` or `waveTools.py`.

We will also need some real .wav files to process.  The starter
code contains a folder called "sounds" which contains four
audio excerpts from the following songs:

1. "Poker Face" by Lady Gaga
1. "Hello" by Adele
1. "I Say A Little Prayer" by Aretha Franklin
1. "The Distance" by Cake

### `processFile`

The function `processFile` is called to process
one of the four audio files from above with one of
the audio effects you will write.  **You do not need
to write `processFile`.  It has already been written
for you**.  Your task is to write the effects.  The
function `processFile` takes a minimum of 
three arguments:

1. The filepath to the audio file to process
2. The filepath to the location to write the new audio file
3. The name of the function that will process the audio as a
string

The starter code under `main` provides function calls to
`processFile` to apply effects to the above songs. 
Uncomment any call to try your effect! The 
starter code under `main` handles the creation of filepaths 
for each of the four songs to pass to `processFile`.
The variables for those paths are listed below:

+ `pokerSourcePath`: The source path to "Poker Face"
+ `pokerDestinationPath`: The destination path to "Poker Face"
+ `helloSourcePath`: The source path to "Hello"
+ `helloDestinationPath`: The destination path to "Hello"
+ `prayerSourcePath`: The source path to "I Say A Little Prayer"
+ `prayerDestinationPath`: The destination path to "I Say A Little Prayer"
+ `distanceSourcePath`: The source path to "The Distance"
+ `distanceDestinationPath`: The destination path to the "The Distance"

By default, the output
files are in the same folder as the input files but with the
suffix "_proc" attached to the end of the file name to distinguish
the processed files from the originals.  However, if you would 
like to try these effects on a different
audio file, then you will need to determine the filepaths 
yourself.  Look at the starter code for a template.

Each audio effect is written as a function whose name will
be passed as a string to `processFile`.  Below is an example
of a call to `processFile` that will make the volume of
the song "Poker Face" by Lady Gaga softer and place the new file
in the sounds folder under the name "poker_proc.wav".

```python
processFile(pokerSourcePath, pokerDestinationPath, "makeSofter")
```

## Audio Effects to Write

As a general rule, **all effect functions must return a new list**.
Do not modify the original channel or samples in place.

Due to the representation of floating point numbers in computers,
certain mathematical calculations will lead to very tiny errors.
These tiny errors are okay.  **DO NOT ROUND YOUR ANSWERS**.  If your
answers differ ever so slightly from our output below, then your
answer is almost certainly correct.

### Audio Effect 1: `makeSofter`

The function `makeSofter` is designed to make your audio file
softer.  `makeSofter` takes a channel (i.e., a list
of numbers) and should return a new list where each value has
been multiplied by a factor of 0.1. In general, the numbers
representing audio (i.e., samples) should lie in the range of
-1 to 1.  Audio files are perceived as louder the closer those
samples get to -1 and 1.  Therefore, multiplying all values by
0.1 will narrow the range of the samples, making the audio 
softer. 

Example usage:

```python
>>> makeSofter([0, -0.2, 0.4, -0.6])
[0.0, -0.020000000000000004, 0.04000000000000001, -0.06]

>>> makeSofter([])
[]

>>> makeSofter([0.1, -0.4])
[0.010000000000000002, -0.04000000000000001]
```
Notice how some of the answers have very small errors when attempting
to multiply by 0.1.  Again that is okay.  

Below is an example 
of calling `processFile` on "Poker Face" with `makeSofter`. 

```python
processFile(pokerSourcePath, pokerDestinationPath, "makeSofter")
```

Go to the sounds folder in your starter code and open up 
"poker_proc.wav" to hear the result!

### Audio Effect 2: `chipmunk`

The function `chipmunk` is designed to make everything sound
like it was made by Alvin and the Chipmunks!  Technically, 
all the pitches and frequency of the sound become higher.
When applied to the human voice, it gives a chipmunk-like
effect.  `chipmunk` takes just a channel
and returns a channel of half the length.  `chipmunk` works
by only retaining the samples from even indices.  The other
samples are discarded.

Example usage:

```python
>>> chipmunk([0, -0.2, 0.4, -0.6])
[0, 0.4]

>>> chipmunk([-0.3, 0.2, 0.1])
[-0.3, 0.1]

>>> chipmunk([])
[]
```

Below is an example of 
calling `processFile` on "Hello" using the chipmunk effect.

```python
processFile(helloSourcePath, helloDestinationPath, "chipmunk")
``` 

### Audio Effect 3: `removeVocals`

The function `removeVocals` is designed to remove the vocal
track from a song.  The algorithm is crude and simple but 
only works for
certain songs when the vocal track is evenly split between 
the left channel and the 
right channel.  Therefore, we can subtract one channel
from the other and the remaining result should be the rest
of the song.  Therefore, `removeVocals` requires two channels
as arguments: the left and the right channel.  `removeVocals`
will return a single channel.  

To illustrate the algorithm, let's take two channels as
an example: a left channel of [0.1, 0.5, -0.2, 0.3] and
a right channel of [-0.1, -0.6, 0.3, 0.1].  To remove the
vocals subtract all the values from the right channel from
the corresponding values of the left channel. That should
yield a result of [0.2, 1.1, -0.5, 0.2].  You'll notice
that with the right combination of numbers it is possible
for the subtraction to produce a result outside of our
preferred range of -1 to 1.  The final step to the 
algorithm is to divide all the results by two.  Therefore,
the final result should be [0.1, 0.55, -0.25, 0.1]

You can assume that the length of the left channel and
right channel are the same length.

Example Usage:

```python
>>> removeVocals([0.1, 0.5, -0.2, 0.3], [-0.1, -0.6, 0.3, 0.1])
[0.1, 0.55, -0.25, 0.09999999999999999]

>>> removeVocals([0.7, 0.2], [0.3, -0.4])
[0.19999999999999998, 0.30000000000000004]

>>> removeVocals([], [])
[]
```

Below is an example of calling
`processFile` on "The Distance" using the vocal removal effect.

```python
processFile(distanceSourcePath, distanceDestinationPath, "removeVocals")
``` 

As a final note about this effect, it works decently well on the
Cake example but poorly on the others.  Even so with the Cake
example, you can hear that some of the other instrumentation
is degraded, meaning that those instruments were relatively
evenly split between the left and right channels.  It is
incredibly difficult to devise such an algorithm that works
universally.  

### Audio Effect 4: `reverse`

The function `reverse` takes a channel and reverses the 
order of the samples.  `reverse` should return a new
channel.  This is an old audio technique that can be used
to create swells.  It has also been used in some contexts to
create hidden messages that can be revealed only when the
listener plays the audio backwards.  Check out this Wikipedia
article on [Backmasking](https://en.wikipedia.org/wiki/Backmasking).

For this function, you cannot use the `reversed` function or the method
`.reverse()`.  In any other context, you should use either of these
tools.  It is usually inadvisable to try and write something that
has already been written for you.  However, for pedagogical purposes,
implementing `reverse` is great practice for working with loops and
the `range` function.

Example Usage:

```python
>>> reverse([0.1, -0.2, 0.5, 0.2])
[0.2, 0.5, -0.2, 0.1]

>>> reverse([0.1, -0.9, 0.3])
[0.3, -0.9, 0.1]

>>> reverse([])
[]
```

Below is an example of calling `processFile`
on "I Say A Little Prayer" using the reverse effect.

```python
processFile(prayerSourcePath, prayerDestinationPath, "reverse")
``` 

### Audio Effect 5: `twoSampleDelay`

The function `twoSampleDelay` creates an underwater effect by 
removing the higher pitches in the audio file.  In technical
terms, this is called a Lowpass Filter.  A filter is a 
processing technique that removes parts of an audio signal.
Filtering is a common technique in lots of data processing 
especially for images and video.

`twoSampleDelay` works by adding together the original channel
and the original channel shifted by two indices to the right.
For example, suppose we had a channel of `[0.1, 0.4, -0.1, 0.3]`.  
A shifted version of that channel would be `[?, ?, 0.1, 0.4]`. 
We can see that the original 0.1 has now moved two indices to the
right as well as the sample 0.4.  Notice how -0.1 and 0.3 ``fall 
off" and are no longer retained when we shift. We want to keep 
the shifted version to be the same length.  

We also have a question about how to fill the two spots on
the left of the shifted version, notated right now with
question marks.  Those will be filled
by arguments passed to `twoSampleDelay`.  The parameter
`twoSampleBack` will be used for index 0
and `oneSampleBack` will be used for index 1.  Suppose
then that `twoSampleBack` had a value of -0.9 and 
`oneSampleBack` had a value of -0.7.  Then if 
channel `[0.1, 0.4, -0.1, 0.3]` is shifted, we would
get `[-0.9, -0.7, 0.1, 0.4]`. 

The final step to the algorithm is to add the original
and shifted version together and divide by two. When
we add, we add at each index as shown below to produce
a new list.

<pre>
   |  0.1 |  0.4 | -0.1 | 0.3 |
 + | -0.9 | -0.7 |  0.1 | 0.4 |
-----------------------------
   | -0.8 | -0.3 |  0.0 | 0.7 |
</pre>

Then we divide each sample by two.  In this example, that would
give us a final result of `[-0.4, -0.15, 0, 0.35]`.  

**twoSampleDelay should work with lists of size zero to two
as well!**

Some hints:
+ The algorithm for `twoSampleBack` can be a little complicated.
Make you understand how the shifted version is generated before
you start writing your code.
+ The above algorithm can be implemented exactly
as described above using several for-loops.  As an extra goal,
use exactly one for-loop.  Think about updating the parameters
`oneSampleBack` and `twoSampleBack` as you progress through
the loop to accomplish the same task.  Reducing the number
of loops in your program can pay big dividends in terms of
efficiency, especially for large files like audio files. 

Example Usage:

```python
>>> twoSampleDelay([0.1, -0.2, 0.5, 0.6], -0.7, -0.9)
[-0.4, -0.44999999999999996, 0.3, 0.19999999999999998]

>>> twoSampleDelay([0.1, 0.6, -0.2, 0.25, 0.3], -0.5, 0)
[0.05, 0.04999999999999999, -0.05, 0.425, 0.04999999999999999]

>>> twoSampleDelay([], 0.1, 0.2)
[]
```

Below is
an example of calling `processFile` using "Poker
Face" with the two-sample delay:

```
processFile(pokerSourcePath, pokerDestinationPath, "twoSampleDelay")
```

### Audio Effect 6: `ohYeah`

The function `ohYeah` will be used to drop the pitch, 
similar to how `chipmunk` raised the pitch.
There is no particular named associated with this effect but
a famous example comes from the song "Oh Yeah" by Yello
popularized in Ferris Bueller's Day Off.  You can listen
[here](https://www.youtube.com/watch?v=Ya1ySdk9Oao).

`ohYeah` works by adding a new sample in between each sample.
The value of the new sample is always halfway between the
original samples.  For example, suppose we had a channel
of `[0.1, 0.4]`.  The value between those samples is 0.25
as it is equidistant from 0.1 and 0.4.  `ohYeah` also adds
a new sample at the front which is between the argument
`prevSample` and the sample at the 0th index.  

For example, if we call `ohYeah` with the channel 
`[0.1, -0.3]` and a previous sample of 0.6 as in
`ohYeah([0.1, -0.3], 0.6)`, then the call should
return `[0.35, 0.1, -0.1, -0.3]`.  The value 0.35 comes
from the halfway point between 0.6 and 0.1.  The value
0.1 is from the original signal.  The value -0.1 is
the halfway point between 0.1 and -0.3.  And finally,
the value -0.3 comes from the original sample.  Notice
that `ohYeah` will always retain the original samples
but double the length by adding samples in between the
originals and attaching a new one to the front.  

This process of generating new sample points between
others is called **interpolation** and is used often
for many audio effects.

Example Usage:

```python
>>> ohYeah([0.5, -0.1, 0.4], -0.1)
[0.19999999999999998, 0.5, 0.2, -0.1, 0.15, 0.4]

>>> ohYeah([0.1], 0.1)
[0.1, 0.1]

>>> ohYeah([], -0.9)
[]
```

Below is
an example of calling `processFile` on "Hello" using
the "Oh Yeah" effect.

```python
processFile(helloSourcePath, helloDestinationPath, "ohYeah")
```

### Audio Effect 7: `crescendo`

The function `crescendo` creates a fade-in on the audio 
track for the duration of the song length.  The simplest 
way to produce a fade-in is to generate
a list of samples that incrementally grow from some start
point up to but not including some end point, 
very similarly to the `range` function.  

For example, suppose we want to generate 4 samples that
grow from 0.2 up to 0.4.  Such a list of samples would
be `[0.2, 0.25, 0.3, 0.35]`.  Note how we do not include
0.4 but do include 0.2.  Also notice that the rate of
increase is always the same (i.e., 0.05) even between
0.35 and 0.4.  

To create a fade-in, then, we multiply our increasing 
samples by the original samples at each index and
return a new list.  For example, suppose our original
samples are `[0.2, -0.4, 0.6, 0.1]` and we want fade-in
from 0.2 to 0.4, then we would multiply each index as
follows:

<pre>
   | 0.2  | -0.4  | 0.6  | 0.1   |
 * | 0.2  |  0.25 | 0.3  | 0.35  |
----------------------------------
   | 0.04 | -0.1  | 0.18 | 0.035 |
</pre>

The final result is `[0.04, -0.1, 0.18, 0.035]`.  The 
length of the increasing samples should always match
the length of the original samples.

The function `crescendo` takes three arguments: `channel`,
`startVolume`, and `endVolume`.  It should return a channel
of the same length.  `startVolume` represents the starting
point of the ramping samples and `endVolume` represents
the ending point of the ramping samples. `startVolume` and `endVolume`
are values between 0 and 1 that represent what fraction of the song's
overall volume should be achieved with 1 being full volume. 

Example Usage:

```python
>>> crescendo([1.0, 1.0, 1.0], 0.2, 0.8)
[0.2, 0.4, 0.6000000000000001]

>>> crescendo([0.9, 0.4, 0.6, 0.2], 0, 1)
[0.0, 0.1, 0.3, 0.15000000000000002]

>>> crescendo([], 0, 1)
[]
```

Below is an example of calling
`processFile` on "The Distance" with a crescendo:

```python
processFile(distanceSourcePath, distanceDestinationPath, "crescendo")
```

### For Fun: Custom Audio Effect

The function `custom` is a function to allow you to explore your own
audio effect.  **It is not graded nor required for this assignment.**  But it
can be interesting to see how manipulation of samples produces
interesting audio effects.  Remember though to keep your range of numbers
between -1 and 1. Otherwise you could damage your speakers or your ears!

Do not add any parameters to `custom` otherwise it will not work with the
starter code. 

To process an audio file using your custom effect, make sure to call
`processFile` with the third argument as `"custom"`.  For example,

```python
processFile(pokerSourcePath, pokerDestinationPath, "custom")
```

Show us all the fun ways you can experiment with music!
