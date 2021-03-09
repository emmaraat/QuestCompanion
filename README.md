# GrowTogether
## Inspiration
As we've all been experiencing lately, finding motivation and community in a pandemic, when many of our lives have moved online, can be difficult. We wanted to create a place for users working towards a common goal to encourage each other and share their progress. For example, users who want to:
- eating healthy for one month
- workout 3 times every week
- learn a new language
can join a **quest**, similar to joining a party in a video game, and be challenged to make it through the adventure.

## What it does
**QuestCompanion** bot manages creating challenges text-channels and users can navigate through the list and choose which challenge they want to join. Each challenge is created to encourage users to improve their life in a specific area in a safe virtual community for a period of time. In each challenge the bot will send an inspirational quote everyday.

**QuestCompanion** has many functionalities/commands :

- **!create [quest name]**
 available in the create-quests channel, it allows anyone to create an active quest channel

- **!delete quest channel**
  accessible for the creator of the quest and admins

- **Set a reminder**
 !remindat [YYYY-MM-DD, HH:MM the task]
 Example: !remindat 2021-02-21,14:34 make awesome discord bot

- **Reacting with a thumbs up will create a welcome message in the Quest you chose to join**

- **!image**
post a random image (limited for now)

- **!inspire me**
 post a random inspirational quote with a random color line

- **!archive quest and !unarchive quest** 
 accessible for the creator of the quest and admins

- **!who**
to receive a list of people who have joined a quest

- **!help**
 post a help message with the list of commands 

## How we built it
With love and Python! We used the Discord.py API to program the bot, and sqlite3 to manage the database.

## Challenges we ran into
It was hard to coordinate who was working on which part of the code. Additionally, because we were in different time-zones we had different moments where we were inactive.

## Accomplishments that we're proud of
The look of the bot with the embedded messages throughout creates a coherent feeling.

## What we learned
We have learned how to use the Discord.py API and use sqlite3 to manage a database that connects to the Discord bot.

## What's next for QuestCompanion
My next goals would be to add functionalities to further increase the quest-like feeling of the bot, for example:
- sending automatic reminders at a determined interval per quest channel
- allowing users to react to these reminders to confirm that they have completed a quest, which would award XP and send a confirmation/praising message
- making quest channels private for only the people who opt-in to the quest, to create a sense of privacy and community within the quest
- tracking the user progress  for every challenge 
- adding user roles for different levels based on xp, such as apprentice, adventurer, grand wizard etc.

## Tech Stack
 - Python 3.x
 - discordpy
 - API
