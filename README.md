# M-PATH
An Empathic Embodied Conversational Agent

This repository includes the empathic dialogue management system for an embodied conversational agent, which is created at iVizLab, in Simon Fraser University by Ozge Nilay Yalcin.
You can find details about this project at :

http://www.sfu.ca/~oyalcin/project/empathy/ 

https://ivizlab.org/research/ai-affective-virtual-human/

To cite the project and code:

Yalçın, Ö. N., & DiPaola, S. (2019, August). M-path: a conversational system for the empathic virtual agent. In Biologically Inspired Cognitive Architectures Meeting (pp. 597-607). Springer, Cham.

Yalçın, Ö. N. (in press) Empathy Framework for Embodied Conversational Agents. Cognitive Systems Research.

```
@InProceedings{10.1007/978-3-030-25719-4_78,
author="Yal{\c{c}}{\i}n, {\"O}zge Nilay
and DiPaola, Steve",
editor="Samsonovich, Alexei V. ",
title="M-Path: A Conversational System for the Empathic Virtual Agent",
booktitle="Biologically Inspired Cognitive Architectures 2019",
year="2020",
publisher="Springer International Publishing",
address="Cham",
pages="597--607",
abstract="M-Path is an embodied conversational agent developed to achieve natural interaction using empathic behaviors. This paper is aimed to describe the details of the conversational management system within the M-Path framework that manages dialogue interaction with an emotional awareness. Our conversational system is equipped with a goal-directed narrative structure that adapts to the emotional reactions of the user using empathy mechanisms. We further show the implementation and a preliminary evaluation of our system in a consultation scenario, where our agent uses text-based dialogue interaction to conduct surveys.",
isbn="978-3-030-25719-4"
}
```

## Getting Started
The project is written on Python and works on Python >= 3.6

This project uses Smartbody character animation system as a character animation platform in Windows. Download Smartbody from: http://smartbody.ict.usc.edu/

A version of this project that uses Unity instead of Smartbody is under development at iVizLab, Simon Fraser University.

You will also need ActiveMQ running in your computer. Follow instructions from : https://activemq.apache.org/getting-started
You might want to run the broker as a service in Windows that automatically runs at start-up, for ease of use.

## Installing

We recommend creating a virtual environment with Python >= 3.6, clone the project and use requirements.txt to prepare your environment.

```
pip install -r requirements.txt
```

## Download the Models
All of the models used in M-PATH are included in the github except the fine-tuned language categorization model for surveys, which should be downloaded to:
https://github.com/onyalcin/M-PATH/tree/master/dialogue_system/dialogue/utils

using following linK:
https://researchdata.sfu.ca/islandora/object/islandora%3A10713

## Running M-Path
1. Start Smartbody and make sure ActiveMQ is running
2. Load Character using one of the files in https://github.com/onyalcin/M-PATH/tree/master/Smartbody_files, the config files currently uses Matt. Wait until you see the character in Smartbody.
3. Run TTSRelay within Smartbody
4. In your virtualenv, run:
```
python -m dialogue_system
```
5. Use push-to-talk to speak with the avatar or type to start written conversation.


## Changing Configuration and Dialogue Structure
In this version, M-PATH is configured to conduct a part of the California Depression Questionnaire, with some flexibility on dialogue-turn taking. The surveys that can be used and the Q&A functionality of the agent can be extended by changing the dataset folders. More information about this process will soon be provided.


