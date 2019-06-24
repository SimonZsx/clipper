# Image Query App

<br/>

## Overview
This application accepts  a audio file as initial input and generate sentiment analysis and subject information of the input.  The model representation:

<br/>

## Container Information
This application consists for five containers.

#### Container1: speech recognition. 
Input: audio file `(.wav)`; Output: `String`

#### Container2: tokenizor
Input: image file  `String`; Output: `String` 

#### Container3: sentiment analyzer
Input: String; Output: `String`, return true if it is positive, false otherwise

#### Container4: subject analyzer
Input: `String`; Output: `String`

<br/>




