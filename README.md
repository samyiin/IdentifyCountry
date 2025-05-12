# IdentifyCountry
Given an address, identify which country is this address in. 

## Problem Description
This problem can be viewed as a classification problem: the input is a string that might (or might not) be an address, the output is one (or more) of the 195 countries there are currently in the world. Let's not get political here regarding the country name and stuff. 

Define the set **C = {195_Countries} U {Not_An_Address}**, The set **S = {All_Possible_String}**. For simplified cases, say each address is representing at most one country. If we want to model the more generic cases, like identifying string "Shanghai -> New York" to "USA and China", then we simply extend the definition of country from set **C** to **C^n**. But for the explanation, let's not complicate things here for now. Then in "reality", there should be a probability function **P: S x C -> R+**. For example, (I made up the number): 

    P (country="USA" | string="New York, USA") = 1 and P (country=Other_Country | string="New York, USA") = 0
    P (country="USA" | string="Georgia") = 0.5 and P (country="Georgia" | string="Georgia") = 0.5
    P (country="Not_An_Address" | string="See you in hell") = 1

Where does this probability comes from? Mostly from common sense: for example, if the string is "London", it's more likely that this string means the city London in UK, but there are several streets in UK, Canada and the US that is named "London street". According to common sense, it's almost certain that when the person fill his address as "London" without country name, he means "London, UK", else he would have clarified. Another way people use to decide the probability is the context. For example, if we are gathering this address information from someone's github page, we know that he is a programmer, then there are way more programmers in the US than the country Gorgia. So if he filled in the address "Gorgia" witout contry name, one could argue that it's more likely that he means the state Gorgia in the US. Other common examples are "Cambridge". 

It is possible that the input string is too ambiguous so that it can map to a lot of possible countries (including Not_An_Address), in that case we define it as *Ambiguous*. Something like this:

    "Ambiguous": Select threshold a, such that for all country, P(country | string) < a
But these are all theories, in reality, we don't have the P function and the a threshold. So below are how we approach this problem. 

## Our Goal
We want the classifier to have this two nice properties:
1. If the address is ambiguous, then return Ambiguous without classifying.
2. If the address is not ambiguous, it is clearly an address in a country or clearly not an actual address, the classifier should classify with good accuracy.

Try to visualize this on an axis with one end being all the countries, the other end being Not_An_Address, the middle part is Ambiguous. 

Technically, we can also define it this way:
1. If the address is ambiguous, then return Ambiguous without classifying.
2. If the address is clearly not an address, then return Not_An_Address without classifying.
3. If the address is clearly an address in a country, then classify the country correctly.

There are other ways to define, for example just add Ambiguous as one option and we just want a accurate classifier. But the definition of probability function above are most intuitive to me, so whatever....


## Methods
### Geopy
We start by uing *Geopy*, This is basically a powerful tool that given a string, it will return the possible countries. 

    https://geopy.readthedocs.io/en/stable/
But it doesnot give us the nice properties we want:
1. If there are at least one possible match, then Geopy will always return the results. We migitate this by setting a rule: if there are more than 3 possible matches in the results of Geopy, then we will label this location as "Ambiguous".
2. When the address is not ambiguous, sometimes the accuracy of Geopy is not ideal. Most common confusion pair (in context of a confusion matrix) is when the address is clarly Not_An_Address, like "Earth", Geopy still returns a location becuase somewhere there is a place name with "Earth" in it. But the other direction is not a problem: for most of the address string that is clearly in an actual Country, Geopy can usually find the country.
3. It cannot resolve the case of multiple countries like "Shanghai - New York"
### LLM
We can simply pass the answer to LLMs like Chatgpt, and ask if they know the address. Compare to Geopy, this approach have more "common sense"; it wouldn't mistake "Earth" as an actual address. On the other hand, Geopy is cheaper (free with 1 request per second), and it works better when then address is just a street name. 
A little update on 2025.05.12: We can use fucntion calling api of OpenAI now to make sure the output country is exacly the same spelling, capitalization and stuff. 

### Hybrid Approach
What we did eventually, is we first pass address to Geopy, and for those Geopy cannot identify, we pass it to LLM. This is the most economic way. 

What is the best way? 

## Method Evaluation
Based on our definition, "Ambiguous" is a binary classification, so we will evaluate it using TN/FN. And then the rest of the classification is essentially a multi-class classification, so we will evaluate it using accuracy. 

You can see why we don't use the split-into-3 definition, becasue the evaluation will be TN/FN for both binary classification of "Ambiguous" and "Not_An_Address"... Not to mention that Not_An_Address is a natural compliment of country classification, and Ambiguous is not. 
