# LittleAntispoof

This project has been developed for the Multimodal Interaction course at Sapienza University of Rome (2021-22).

LittleAntispoof is a multimodal **face liveness detection** module that can be used in the context of face anti-spoofing.

The system uses a **challenge-response** interaction style, composed of gaze verification, emotion verification, speech verification, and eye blinking check.

Specifically, recognition attempts that must be checked for liveness, will pass though the following phases, in a random order:

* **Gaze** challenge: the user is asked to look towards a certain direction, randomly chosen.
* **Emotion** challenge: the user is asked to provide an emotion-distorted face expression (e.g. happy face), randomly chosen.
* **Speech** challenge: the user is asked to pronounce a randomly chosen phrase.

During challenges, the user's **eye blinking rate** is also checked, in order to determine whether it is within a configured one.

