# Intro

openWakeWord is an open-source wakeword library that can be used to create voice-enabled applications and interfaces.
It includes pre-trained models for common words & phrases that work well in real-world environments.

This is forked repo. See [original repo](https://github.com/dscripka/openWakeWord) for details.

# Changes in this fork

This fork prunes code related to custom model training and verification.
By avoiding importing modules related to custom models such as `sklearn`, it saves ~33MB of memory.
It proves to be useful on memory constrained devices, such as the Raspberry Pi Zero series.

# Installation

Run:
```commandline
pip install openwakeword-pruned
```
Check out other configs in the [original repo](https://github.com/dscripka/openWakeWord#installation).
