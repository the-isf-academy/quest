Dialogue
========

Many narrative games involve dialogue in which characters talk with one another. Dialogue provides a 
convenient way of structuring back-and-forth talk in which the player's choice of response leads to 
the interlocutor saying something else. Back and forth until the end of the conversation.

Dialogue relies on a data structure of lists and dicts recording what gets said, possible responses, 
and what happens when each response is given. That data structure looks like this::

    {
        "START": {
            "content": [
                "Hello", 
                "Have we met?"
            ],
            "options": {
                "You don't remember?": "FRIENDS",
                "I think not": "STRANGERS"
            }
        },
        "FRIENDS": {
            "content": [
                "Oh, of course.",
                "I didn't recognize you with that wig.
            ],
            "options": {
                "Do you like it? It's new.": "WIG",
                "I doubt that.": "ANGRY",
            }
        },
        ...
    }
    
Writing dialogue this way can get tedious. Instead, you can write dialogue in a simplified dialect of the 
Ink language and use :py:meth:`Dialogue.from_ink`. Here is the Ink code for the Grandma's Soup example game.
It should be pretty self-explanatory::

    === START ===
    Oh hello there, my dear. It's so nice to see you. I knew you were coming today
    so I decided to make your favorite soup. 
    
    Before I can make it though, I need to forage some vegetables from the island. 
    My legs are not as strong as they used to be. Do you think you could help me?
    
    + Of course, grandma! -> HELP
    + Meh, I was gonna play fortnite -> BADBOY
    
    === HELP ===
    Oh you are such a dear. 
    
    + What do you need? -> VEGGIES
    
    === BADBOY ===
    You are a very bad boy. 
    
    + Sorry, I'll help. -> VEGGIES
    
    === VEGGIES ===
    I just need a few things. I need carrots and potatoes and 
    tomatos. 
    
    Oh, and can't forget a mushroom!
    
    + OK -> END

    === CARROTS ===
    Oh, these are lovely carrots. But I still need more vegetables. 
    
    + OK -> END
    
    === TOMATOS ===
    Oh, these are such ripe tomatos. But I still need more vegetables. 
    
    + OK -> END
    
    === POTATOES ===
    Oh, these are very spuddy potatoes. But I still need more vegetables. 
    
    + OK -> END
    
    === MUSHROOM ===
    Oh, what a beautiful mushroom. It reminds me of my girlhood. But I still need 
    more vegetables. 
    
    + OK -> END
    
    === SOUP ===
    Ah, now we have everything we need for some delicious soup! why don't you go 
    explore the island and I'll call you when it is ready?
    
    + OK -> END



    

.. automodule:: quest.dialogue
   :members:

