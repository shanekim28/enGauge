
## Originality/Creativity
While our idea stems from qualitative text analysis, which is a topic on machine learning and natural language processing that’s been researched and studied by many individuals,  the **parsing of a forum channel is unique**. Qualitative text analysis has generally been based on sources such as news articles, classical novels, and movie scripts, but analyzing real-time forum-based discussion platforms such as Piazza, Slack, and Discord is a novel one. The **ability to determine whether a user’s post’s content is considered a question, answer, or neither** is appended with a creative method to **track user engagement via the content itself, replies to questions, and reactions to those responses**.


## Technical Complexity
Determining what makes a question was a difficult process. Since the English language is so dynamic, there are many different forms a sentence can take. Thankfully, using pre-trained models from the Stanford Core NLP library, we were able to break up sentences into their constituent clauses and classify them based on what clauses they contained. Our solution consisted of 5 major parts interacting with each other: 
- an Angular web application
- a backend RESTful API service built on Flask with 6 endpoint
- a Discord bot made with the unofficial Discord Python wrapper
- a Java-based NLP server
- a CockroachDB cloud database 

The bot sends specific message data to the NLP server which returns whether the message is a question: 
- message content
- message ID
- the Discord user ID of the message author
- whether the message refers to another message
- how many unique users reacted to the message
- the timestamp the message was created at

A user is given points to a question based on the quality of the question, which is currently determined by the amount of words in the question.

Then, the backend tracks answers to that question. A message is deemed an answer to a question if the message has a reference to the question (such as when a user directly replies to the message) **or** to a tag of the ID of the user who asked the question. The answerer is then awarded points based on the speed and relevance of their answer, utilizing logarithmic equations to emphasize a diminishing return of points if an answerer takes too long to respond. An answerer receives almost no points after an hour of the posting of a question. 

Finally, scores are updated on the leaderboard based on the simplicity of directly importing the style of the primary SQL table located in the CockroachDB database, with this update occurring every few seconds.



## Adherence to Theme
Judging engagement in a remote environment compared to an in-person one is distinct and difficult to analyze. In an in-person environment, it is simpler for a teacher or professor to detect which students are actively participating by observing each student’s body language, eye contact, willingness to collaborate with classmates, and other touch points by simply searching around the classroom. 

However, the lack of face-to-face interaction in the remote learning environment creates a barrier towards engagement analysis: unique indicators such as body language and physical behavior vanishes due to the asynchronous nature, and it’s unclear to figure out how frequent students are participating in the material without the professor constantly searching the forum platform. The integration of our Discord scraper bot with natural language processing allows for tangible touch points in the remote environment: each student in a certain Discord server gains points based on if a student asks questions, answers other questions, and the reaction of the asker of the question to the response. 

This feedback loop is emphasized in a real-time discussion-based application like Discord, where interaction between students and instructors is more likely than on a Zoom lecture, for example, due to the subconscious safety of being behind a screen. This feedback loop allows for an instructor to feasibly analyze the effectiveness of remote learning based on the distribution of points over the entire class: the more points a student has, the more engaged they are. 



## Practical Implementation
We designed the Discord bot’s to be as accessible as possible, relying on an underscore key character to denote a command.  The bot relies on only a few simple commands, such as __scan_ in order to look through messages and scan for questions, answers, and participation, __register_ to track a certain user’s points, and __leaderboard_ to view the **overall top 3 most engaged students**.  The __leaderboard_ command also includes a link to a simple but stylish front-end web application that displays the participation points for each participant on the Discord channel as well as a leaderboard with an **easy to read GUI**. The understanding of the key metrics is simple: the **more points a student has, the more engaged they are**, and that level of accessibility makes this project a user-friendly one.



## What's next for enGauge
We might expand the idea of participation chatbots and apply them to other mediums such as Piazza and Slack, which are used to a great extent during our current remote learning environment.  We might also consider expanding our point participation system to Zoom and employ audio and textual machine learning parsing algorithms in order to obtain participation information that can help professors improve their teaching strategies and hold students more accountable in remote learning.
