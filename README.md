# IdentifyCountry
Given an address, identify which country is this address in. 

## Description
This problem can be viewed as a classification problem: the input is a string that might (or might not) be an address, the output is one (or more) of the 195 countries there are currently in the world. Let's not get political here regarding the country name and stuff. 

Define the set **C = {195_Countries} U {Not_An_Address}**, The set **S = {All_Possible_String}**. For simplified cases, say each address is representing at most one country. If we want to model the more generic cases, like identifying string "Shanghai -> New York" to "USA and China", then we simply extend the definition of country from set **C** to **C^n**. But for the explanation, let's not complicate things here for now. Then in "reality", there should be a probability function **P: S x C -> R+**. For example, (I made up the number): 

    P ("USA" | "New York, USA") = 1
    P ("USA" | "Georgia") = 0.5 and P ("Georgia" | "Georgia") = 0.5
    P ("Not_An_Address" | "See you in hell") = 1

Where does this probability comes from? Mostly from common sense: for example, if the string is "London", it's more likely that this string means the city London in UK, but there are several streets in UK, Canada and the US that is named "London street". According to common sense, it's almost certain that when the person fill his address as "London" without country name, he means "London, UK", else he would have clarified. Another way people use to decide the probability is the context. For example, if we are gathering this address information from someone's github page, we know that he is a programmer, then there are way more programmers in the US than the country Gorgia. Then when he filled in the address "Gorgia" witout contry name, one could argue that it's more likely that he means Gorgia in the US. 



There are four possible scenarios that might occure: 
1. The input address is clearly mapping to no country, like "See you in hell" is clearly not  valid address.
2. The input address is clearly mapping to a single country, like "New York, USA" is clearly in the US.
3. The input address might be mapped to several countries, like "Georgia" might be the country or a state in the US.
