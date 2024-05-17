RISK Bot
Aidan O’Connor (ao274), Alexander Lawless (ajl429)
Reinforcement Learning, Heuristic Algorithms
RISK

Project Description:
At the beginning of the semester, our goal was to build an AI model for the strategy game, RISK. We felt that RISK is a difficult game with a lot of moving parts, so building an intelligent AI to play the game would be a good challenge. We knew that RISK is a relatively complicated game and making a functioning version of the game is not the point of this project, so we planned to use internet resources to help build the game. We wanted to incorporate two aspects of AI into our project, heuristic algorithms and reinforcement learning. We felt that it was important to build two different types of AI’s using totally different approaches, and see how they stacked up against each other. The heuristic model would take in the current state of a RISK game, anywhere from placing your first troop to the end of the game, and would make a decision based on that state. We felt that this was an important first step in getting to an AI that can be strategic and win games. We knew that building a heuristic model that can actually win in this game would be difficult due to all the different elements of RISK strategy, so we didn’t set high performance expectations. The reinforcement learning model would build off of the heuristic model and learn from mistakes it made in prior games. We planned to keep track of the following metrics: win rate, number of turns to win, territory control percentage, ratio of troops lost to troops gained, and human evaluation. We would then use these parameters and have our model learn from its mistakes to update the values in hopes for better performance. We wanted our model to be able to beat other bots, and stand a chance of winning against a real human. 

In terms of what we actually did, we stayed pretty true to the original goals of the project that we set at the start of the semester. We spent the majority of the first part of the semester browsing for repositories we could use to make a RISK game, and researching AI techniques and how to implement them. We ended up finding some useful resources, including a repository with a well-functioning RISK game and a GUI. We also found good research on strategy in the game and some good resources on building basic AI for game development. We then proceeded with the construction of our heuristic model. We wanted to have a few baseline models that we would have our heuristic play against to see if it is improving. We made a model that does absolutely nothing, a model that makes random choices on what it does, and an attacking model that always chooses to attack if it can. The goal was to develop our heuristic such that it can beat all three of these models decisively. At first, we developed a complicated heuristic model that simulated all possible actions. It would simulate each action and return possible future game states, along with the probabilities that those game states would occur. It would then evaluate those potential future game states, and give each one a score based on game strategy. After it had all those scores, it would take the highest score and choose to do the action that led to that score. We ended up having approximately 300 lines of code with many different scores that contributed to the final weight choice. However, it wasn’t performing that well. It would tie with the model that does nothing and lose to the random choice model. We ultimately realized that we were overdoing it a bit. The model would give scores for all these different strategic elements of the game, and would choose the action that gave the highest average score for all the different elements. But RISK is complicated and can’t use a universal strategy for all turns of the game. It ended up basically doing nothing but stacking troops in a few territories and attacking if an enemy got close. It was not aggressive at all and its strategy seemed pretty random, since it had no memory of its strategy from the move before. Instead of trying to complicate the model even further, we decided to redo it with a more intuitive approach. We decided to have different strategies for different turn types. So one by one, we added basic strategy logic for the different turn types of the game. As we added more logic to our model, it slowly began to perform better and better against all three, which we’ll get into later in the evaluation. We finished development of the heuristic with a satisfying win rate and proceeded to the reinforcement learning element of the project. 

We built off of our heuristic model to develop our reinforcement learning model, since the heuristic performed pretty well even against a human. We took certain elements of our heuristic’s logic like its capacity for performing certain actions, and made them into adjustable weighted parameters. For example, we added parameters for the heuristic’s propensity to add fortify more troops to a region, select territories on the same continent, attack, and other similar actions. This was a contrast from our initial intention of using win rate, number of turns to win, territory control percentage, ratio of troops lost to troops gained, and human evaluation. As time went on and we learned more about the game and strategy, we realized that it would be better to use the other weighted parameters to improve performance. We adjusted our heuristic to have these parameters and configured so the model learns from its mistakes and adjusts the parameters accordingly. It worked well and improved our model’s performance. 

The key aspects of AI that were central to our project were heuristic models and reinforcement learning, as we intended at the beginning of the project. Neither of us had extensive experience in either of these areas, so we looked at it as a fun learning opportunity. We did extensive research into heuristics and how to build a good one. We did overdo it on our first implementation and combined all our resources into something that was a little bit too complicated to actually perform. But we learned from this and ended up designing something a little more simple, but could scale much easier to encompass more logic. We are proud of the end product of our heuristic and feel that we have learned a lot on the subject. The second element of AI that we incorporated into the project was reinforcement learning. Something we both had mild exposure to from machine learning courses but had never really implemented into a large and practical system like this. So it took some trial and error to get the learning working. At first, we only had one or two parameters that the model would learn from and there wasn’t any quantifiable improvement. But as we added more parameters and ran the model more and more, the parameters got fine tuned to a point where it was beating our base heuristic. The goal when we set out on this project was to incorporate these two elements of AI into our project and we feel that this was accomplished. We both have learned a lot about these two elements of artificial intelligence and we feel that it will be useful as we start our careers in the coming months. 

Evaluation:
We evaluated our model in a variety of ways. The question that we most wanted answered was how our model performed against our baseline models. So we had to develop a way to definitively view performance in a way that gave us some numerical data. Whenever we made any changes, we would first run it in the GUI version of the game and play against it to see how it performed and if there were any bugs. Once we were sure that there were no bugs and the changes we made worked as intended, we proceeded to our second step of evaluation. We have a function that allows for two or more AI’s to play against each other for a set amount of games. It would log the state of the game at each turn, and tell us the end winner. At first, we played ten games between AI’s to get an idea for the performance. However, 10 seemed to be too few sometimes to get a true idea of which player was performing better, so we bumped that number up to 100. We would play 100 games and determine how well our model was performing. Finally, we would play against the model ourselves and see if it could beat us. 

As mentioned before, our heuristic model was scrapped and remade because it was not performing well against our baseline models. We started tracking performance once we started with our second iteration of the heuristic. The first turn style that we put in logic for was the assignment of territories at the beginning of the game. We didn’t expect significant performance from this, since it only affects the strategy before the game actually starts. In our ten game simulation against the AI that does nothing, it tied each time, as seen below. This match log can be found in the logs directory of the project with the name “20240517-1537_Do Nothing_Heuristic”


Then we added in pre placement logic, which we also didn’t expect much from because this is only the portion of the game where you assign troops after assigning territories, with no additional strategy. This proved to be true, as the heuristic won one game, and the other 9 were a tie. You can view the log of this match in the logs directory with the name “20240517-1545_Do Nothing_Heuristic”

Then we added in placement logic, which is how the player places troops at the beginning of a turn. We assumed it might enhance performance but not by that much since there still was no aggression in the model, which is required to win games. The model did not perform that well, ending in a tie all five games again. You can see this log at “20240517-1601_Do Nothing_Heuristic”

Now it was time for the model to be aggressive, so we added in attack logic. We expected a significant performance increase here because a model that attacks should beat a model that does nothing. This came true and our model won 10 times. You can view the log at “20240517-1603_Do Nothing_Heuristic”

Now that our model definitively beat the do_nothing model, we put it against random and attacker to see how it performed. We weren’t sure what to expect, but we hoped it would beat random decisively. Heuristic won 10 times against random and 7 times against the attacker. Those logs can be seen at “20240517-1607_Heuristic_Random” and “20240517-1610_Attacker_Heuristic”.


We then added in logic for the occupation turn after winning an attack. This forced the conquered territory to have all the troops from the conqueror go to it, encouraging more aggressiveness. We expected a moderate performance increase here. We also decided to have 100 game matches at this point to get a more definitive idea of model performance. Encouragingly, our model won 90 times. The log can be viewed at “20240517-1612_Attacker_Heuristic”

Finally, we added fortification logic. This is only one move after an entire turn that is not all that important, so we didn’t expect much to change. This was confirmed with the model winning 85.5 games, so a slight performance decrease that can be attributed to randomness. This log can be viewed at “20240517-1622_Attacker_Heuristic”

Overall, we think that we were successful in the implementation of our heuristic model. We set out originally with the goal of definitively beating our baseline models, which we did. All three we beat with a high level of certainty. We also wanted it to be competitive with a human, which it definitely is. I encourage anyone to try and beat this model, it is not trivial and I would even consider it a little challenging. We are proud of this fact and view the heuristic as a definite success. 



Reinforcement Learning:
After developing an outline for a heuristic algorithm that we were satisfied with, we decided to add weights to choose between different actions as the AI plays the game. With weights implemented in different parts of the heuristic’s decision-making process, we would be able to customize and “learn” the right balance between these decisions through reinforcement learning. 

In order to do this, we had to redesign a significant portion of the code for both the heuristic algorithm and the primary game script. By adding a separate json file to store the weights configuration, we were able to write a script to dynamically change these weights based on how the model was performing in previous matches. The script: reinforcement_learning.py, executes a command to run 100 games between our heuristic algorithm and another comparative ai. It uses the log files generated from those games to determine which algorithm won, and populates all of this data into a q table. The script then uses this information to data the config file, altering the weights based on whether or not the model won the previous games. 

Some examples of weights we implemented were based on strategies that we were familiar with from playing the game in real life. For example, we knew that there is some advantage to claiming contiguous territories at the start of the game, so we added the “weight_continent” variable so that the heuristic could weigh the benefits of using this strategy. Other weights we added include “weight_troops”, “weight_agression”, “weight_spread”, et cetera. We noticed improvements in the model’s performance from an initial arbitrary low value at first to the more finely tuned weights after a few runs of this script. Our heuristic algorithm was now “learning” how to balance different decisions effectively.

Here is an example of a default weight configuration we would start off with, each weight having a very low value. That configuration showed a decisive victory over the Attacker ai, as seen below (88-12). We found that almost always when the heuristic algorithm did not beat the attacker algorithm, these games almost always resulted in a tie. (logs/log_1715980001.txt)


Provided here is an example of how the weights changed after a few iterations of the reinforcement learning script. Accompanying this change in weights was an increase in the heuristic model’s success (logs/log_1715980064.txt). The heuristic algorithm jumped to a 91% win rate against the attacker AI after just a few rounds of “learning”. While we continued seeing success the more we trained our model, we did observe a plateau in the bot’s effectiveness in around the mid-90% range. 

 









While we enjoyed the challenge of incorporating aspects of reinforcement learning into our project, we ultimately do not think it had the impact we were hoping for. Improvement in the model’s performance was not all that significant as the weights were updated, and we also observed that most of the weights just approached 1.0 the more we ran the reinforcement learning script. We have identified a few issues that likely caused these challenges, the largest of which was the type and implementation of weights in the heuristic’s decision-making process. Despite our efforts to vary the model’s habits from the initial heuristic logic, the model just tended to more or less revert to those habits after a few rounds of “learning”. Perhaps this could have been alleviated had we initially designed our scripts with this in mind, but we believe that there is still merit to this method of incorporating weights into the heuristic. Ultimately, we accomplished our goals of creating a heuristic model that beat a basic “attacker” AI, as well as finding ways to “teach” this heuristic model how to perform better by implementing reinforcement learning. 
Sources:

Resource we used to develop a strategy:
https://web.mit.edu/sp.268/www/risk.pdf

Main game rules that we used to help build the game and logic:
https://www.hasbro.com/common/instruct/risk.pdf

Main Repository we used for game logic and the GUI:
https://github.com/cjarchibald/RISK-AI

Resource we used to develop initial heuristic model:
https://theresamigler.com/wp-content/uploads/2020/03/2048.pdf

Resource for reinforcement learning in games:
https://medium.com/@www.seymour/training-an-ai-to-play-a-game-using-deep-reinforcement-learning-b63534cfdecd

Repository with RISK game and an AI:
Github: Arsanuos/RiskGameWithAI

Resource for building a RISK AI:
Martin Sonesson: Creating an AI for Risk board game
