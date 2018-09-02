![alt text](https://github.com/rosevoul/media/blob/master/nater/nater-logo.png)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://github.com/rosevoul/nater/blob/master/LICENSE)

# Natural Test Routine

Nater is an open-source recommendation engine for automating a test routine using natural language processing techniques. 
It is based on the word embeddings generated from software documents in order to employ a recommender system which guides the creation of automated test scenarios and the tracing of covered requirements. 
In addition, it adopts association analysis re-ranking to improve the provided recommendations based on the user activity.

This engine addresses test engineers working with Model-Based Testing,
where building blocks can be teamed to implement an automated test. The user
can create a test scenario that will transform into a test ready to run and supports automatic requirement tracing. 

Experiments conducted in the European Space Agency’s Ground Segment test scenarios demonstrate the ability of this domain-specific tool to produce results close to human thinking and ease testing procedures.

Created by: Fei Voulivasi (rosevoul@gmail.com)<br>

### Features

* supports understanding of **specific-domain context** and semantics
* **easily tunable** to fit the needs of different domains
* provides **spell checking** functionality
* exploits information of massive volumes of **software documentation**
* reduces the time and effort taken to derive **automated tests**
* improves the **test coverage** of the software requirements



### Screenshots
<img src="https://github.com/rosevoul/media/blob/master/nater/gui-1.png" width="800" >

<img src="https://github.com/rosevoul/media/blob/master/nater/gui-2.png" width="800">


### Technical Overview

The high-level design diagram shows the main concept of the recomender system.

<img src="https://github.com/rosevoul/media/blob/master/nater/high-level-concept.png" width="600">

### Installation

Although the engine can run on other systems, it was developed and validated using:
* Ubuntu 16.04 (Xenial)
* Python 3.5.2

#### Dependencies
The required python modules can be found in the requirements.txt file.

Important modules:
* [pandas](https://pandas.pydata.org/) (data manipulation and analysis)
* [gensim](https://radimrehurek.com/gensim/) (vector space modeling and topic modeling)
* [orange3-associate](https://pypi.org/project/Orange3-Associate/) (association rules and frequent itemsets mining)
* [nltk](https://www.nltk.org/) (human language data processing)

The dependecies can be installed using the command:
`$ pip install -r requirements.txt`

Make sure that you have already installed the [pip](https://pip.pypa.io/en/stable/installing/) command line.

