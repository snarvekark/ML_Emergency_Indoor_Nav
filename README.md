# ML_Emergency_Indoor_Nav
ML model for Indoor Navigation for Emergency Exits

This project is a Smart Navigation System for Emergency Exits. The goal of the project is to help people, helper volunteers and first responders evacuate efficiently from an indoor environmet.

There are two iOS application in this project, one for the first responders and the other for the users. 

The Backend for the project is deployed using serverless AWS Lambda service

In this project Q-Learing algorithm is used to find the shortest path for navigation. In this alogrithm reinforcement learning using rewrd matrix is used.

This repository focusses on the Machine Learning part using Q-Learning. Further the algorithm is improvised to work for any given map of a bulding and provide shortest or alternate path dynamically based on whether any certain area is safe or blocked. 

The machine learning algorithm is updated to deploy using AWS serverless Lambda function

Further the algorithm is refactored to handle mulitple paths thus reducing runtime
