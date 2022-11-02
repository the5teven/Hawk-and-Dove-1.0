# Hawk-and-Dove-1.0
This code runs a visual simulation of the Hawk-Dove Game (a famous model in the field of evolutionary game theory). There are some tweaks to the original model though to make this one more realistic.  Game perimeters can be set by the user.

<img src="Image/gif.gif" width="650" />

My Rules(This is a lot so feel free to not read this): 
1. There is a set amount of food.
2. Hawks and Doves will go out and look for food once a day.
3. Hawks and Doves will pick food at random.
4. If one or more doves choose the same peace of food they will all split it evenly.
5. If one or more hawks choose the same peace of food they will fight over it. Ultimately, they will end up splitting the food evenly but, lose a set portion of the food as a penalty for fighting.
6. If one or more doves and one or more hawks choose the same food the hawks will steal a majority of the food for themselves. If there are more than one doves they will split their portion among themselves evenly. If there is more than one Hawk, the hawks will fight over their portion, ultimately splitting their portion evenly among themselves, but lose a set portion of the food as a penalty for fighting.
7. If a Hawk or Dove chooses a piece of food and no one else chooses it they will get all the food.
8. At the end of the day if a Hawk or Dove does not have a set amount of food it will die.
9. At the end of the day if a Hawk or Dove has a set amount of food over there food they need to live they will reproduce and make new Hawks or Doves equal to (the food they have - food needed to live) food needed to live, basically making babies with all the extra food they have.
10. Food resets every day.

Rules Basically: Doves are nice and Hocks are assholes that fight.
