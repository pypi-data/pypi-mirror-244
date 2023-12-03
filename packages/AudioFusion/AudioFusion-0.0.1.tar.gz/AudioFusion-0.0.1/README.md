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
>>> music = Music.loadSound("/path/to/your/music.mp3")

>>> # Add effects
>>> music = Music.effect8D(music)
>>> music = Music.effectSlowed(music)

>>> # Reverb effect is a special case. Its highly suggest to add reverb in very end and mention it while saving music file otherwise you will face errors...
>>> music = Music.effectReverb(music)

>>> # Save your edited music file
>>> Music.saveSound(music, "finalMusic.mp3", ifReverb=True)


```
<p>More effects and method will be added soon</p>
<p>PR in github repository are always welcome.</p>