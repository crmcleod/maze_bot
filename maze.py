from email import message
import discord

client = discord.Client()

maze = [
    [1, 2, 1],
    [1, 0, 1],
    [1, 1, 1],
   
]

currentDirection = "N"
currentPosition = [10, 9]
mazeStarted = False
mazeComplete = False

def move():

    global currentPosition
    global mazeComplete

    if currentDirection == 'N':
        ahead = maze[ currentPosition[0] -1 ][  currentPosition[1]    ]
        if ahead == 0:
            previousPosition = currentPosition
            currentPosition = [previousPosition[0] - 1, currentPosition[1]]
            return lookAround()
        elif ahead == 1:
            return('Way is blocked')
        elif ahead == 2:
            mazeComplete = True
            return('Congratulations you found the exit!')
    elif currentDirection == 'E':
        ahead = maze[ currentPosition[0]    ][  currentPosition[1]  +1  ]
        if ahead == 0:
            previousPosition = currentPosition
            currentPosition = [previousPosition[0], currentPosition[1] + 1]
            return lookAround()
        elif ahead == 1:
            return('Way is blocked')
        elif ahead == 2:
            mazeComplete = True
            return('Congratulations you found the exit!')
    elif currentDirection == 'W':
        ahead = maze[ currentPosition[0]    ][  currentPosition[1]  -1  ]
        if ahead == 0:
            previousPosition = currentPosition
            currentPosition = [previousPosition[0], currentPosition[1] - 1]
            return lookAround()
        elif ahead == 1:
            return('Way is blocked')
        elif ahead == 2:
            mazeComplete = True
            return('Congratulations you found the exit!')
    elif currentDirection == 'S':
        ahead = maze[ currentPosition[0] + 1][  currentPosition[1]      ]
        if ahead == 0:
            previousPosition = currentPosition
            currentPosition = [previousPosition[0] + 1, currentPosition[1]]
            return lookAround()
        elif ahead == 1:
            return('Way is blocked')
        elif ahead == 2:
            mazeComplete = True
            return('Congratulations you found the exit!')


def lookAround():
    if currentDirection == 'N':
        ahead = maze[ currentPosition[0] -1 ][  currentPosition[1]    ]
        left =  maze[ currentPosition[0]    ][  currentPosition[1] -1 ]
        right = maze[ currentPosition[0]    ][  currentPosition[1] +1 ]
        back =  maze[ currentPosition[0] +1 ][  currentPosition[1]    ]
    elif currentDirection == 'E':
        ahead = maze[ currentPosition[0]    ][  currentPosition[1]  +1  ]
        left =  maze[ currentPosition[0] -1 ][  currentPosition[1]      ]
        right = maze[ currentPosition[0] +1 ][  currentPosition[1]      ]
        back =  maze[ currentPosition[0]    ][  currentPosition[1]  -1  ]
    elif currentDirection == 'W':
        ahead = maze[ currentPosition[0]    ][  currentPosition[1]  -1  ]
        left =  maze[ currentPosition[0] +1 ][  currentPosition[1]      ]
        right = maze[ currentPosition[0] -1 ][  currentPosition[1]      ]
        back =  maze[ currentPosition[0]    ][  currentPosition[1]  +1  ]
    elif currentDirection == 'S':
        ahead = maze[ currentPosition[0] + 1][  currentPosition[1]      ]
        left =  maze[ currentPosition[0]    ][  currentPosition[1]  +1  ]
        right = maze[ currentPosition[0]    ][  currentPosition[1]  -1  ]
        back =  maze[ currentPosition[0] -1 ][  currentPosition[1]      ]

    return ('You are currently facing {currentDirection}, \n Ahead of you is {lookAhead}, \n to the left is {lookLeft}, \n to the right is {lookRight} \n and behind you is {lookBehind}'.format(
        currentDirection = currentDirection,
        lookAhead = "passable" if ahead == 0 else 'the exit' if ahead == 2 else "blocked", 
        lookLeft = "passable" if left == 0 else 'the exit' if left == 2 else "blocked", 
        lookRight = "passable" if right == 0 else 'the exit' if right == 2 else "blocked", 
        lookBehind = "passable" if back == 0 else 'the exit' if back == 2 else "blocked", 
    ))


def getCurrentDirection(turn):
    global currentDirection
    previousDirection = currentDirection
    if previousDirection == 'N':
        if turn == 'l':
            currentDirection = 'W'
        elif turn == 'r':
            currentDirection = 'E'
        elif turn == 't':
            currentDirection = 'S'
    elif previousDirection == 'E':
        if turn == 'l':
            currentDirection = 'N'
        elif turn == 'r':
            currentDirection = 'S'
        elif turn == 't':
            currentDirection = 'W'
    elif previousDirection == 'S':
        if turn == 'l':
            currentDirection = 'E'
        elif turn == 'r':
            currentDirection = 'W'
        elif turn == 't':
            currentDirection = 'N'
    elif previousDirection == 'W':
        if turn == 'l':
            currentDirection = 'S'
        elif turn == 'r':
            currentDirection = 'N'
        elif turn == 't':
            currentDirection = 'E'

async def sendMsg(msg, txt):
    await msg.channel.send(txt)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global currentDirection
    global currentPosition
    global pocketsChecked
    global mazeStarted

    messageContent = message.content.lower()

    if messageContent == 'r' or messageContent == 'l' or messageContent == 't':
        if mazeComplete == False:
            loweredLetter = messageContent
            getCurrentDirection(loweredLetter)
            await sendMsg(message, lookAround());
        elif mazeComplete == True:
            await sendMsg(message, 'You have already completed the maze, type `start over` to begin again')
    elif messageContent == 'f':
        if mazeComplete == False:
            await sendMsg(message, move())
        elif mazeComplete == True:
            await sendMsg(message, 'You have already completed the maze, type `start over` to begin again')

    if messageContent == 'start':
        if mazeStarted == True:
            await sendMsg(message, 'You have already begun, try help, commands or start over')
        elif mazeStarted == False:
            mazeStarted = True  
            await sendMsg(message, 'You find yourself at the center of a large maze, can you escape?')
            await sendMsg(message, 'To complete the maze you may use the following commands: lookaround, l for left, r for right, f for forward, t for turn 180 degrees')
            await sendMsg(message, 'l, r and t will only alter your direction, you must use f to move.')

    if messageContent == 'start over':
        currentDirection = 'N'
        currentPosition = [10, 9]
        pocketsChecked = False
        await sendMsg(message,
            'You have once again found yourself at the center of a maze \n' + 
            lookAround())

    if messageContent == 'help' or messageContent == 'commands':
        await sendMsg(message, 'To complete the maze you may use the following commands: lookaround, l for left, r for right, f for forward, t for turn 180 degrees')
        
    if messageContent == 'lookaround':
        await sendMsg(message, lookAround())


client.run(discordkey)
