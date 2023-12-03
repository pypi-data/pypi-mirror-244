<div align="center">
<h1>AudioFusion</h1>
Python music editor
</div>

<i>A package that allows to edit your music file however you want with effects like slowed reverb and 8d.</i>

<h2>Installation:</h2>

```bash
>>> python3 -m pip install AudioFusion
```

<h2>Usage:</h2>

```python
>>> from AudioFusion import Fusion


>>> # Load your music file
>>> music = Fusion.loadSound("/path/to/your/music.mp3")

>>> # Add effects
>>> music = Fusion.effect8D(music)
>>> music = Fusion.effectSlowed(music)

>>> # Reverb effect is a special case. Its highly suggest to add reverb in very end and mention it while saving music file otherwise you will face errors...
>>> music = Fusion.effectReverb(music)

>>> # Save your edited music file
>>> Fusion.saveSound(music, "finalMusic", ifReverb=True)


```
<p>More effects and method will be added soon</p>
<p>PR in github repository are always welcome.</p>

<h2>Detailed Usage:</h2>

```python
>>> from AudioFusion import Fusion


>>> # Load your music file
>>> music = Fusion.loadSound("/path/to/your/music.mp3")

>>> # Add effects
>>> music = Fusion.effect8D(
        music,
        panBoundary = 100,  # Perctange of dist from center that audio source can go
        jumpPercentage = 5,  # Percentage of dist b/w L-R to jump at a time
        timeLtoR = 10000,  # Time taken for audio source to move from left to right in ms
        volumeMultiplier = 6  # Max volume DB increase at edges
)

>>> music = Fusion.effectSlowed(music, speedMultiplier: float = 0.92 ): # Slowdown audio, 1.0 means original speed, 0.5 half speed etc

>>> # Reverb effect is a special case. Its highly suggest to add reverb in very end and mention it while saving music file otherwise you will face errors...
>>> music = Fusion.effectReverb(
        music,
        roomSize = 0.8, 
        damping = 1,
        width = 0.5,
        wetLevel = 0.3,
        dryLevel = 0.8,
        outputFile = "tempWavFileForReverb.wav"
    )

>>> # Save your edited music file
>>> Fusion.saveSound(music, "finalMusic", ifReverb=True)


```