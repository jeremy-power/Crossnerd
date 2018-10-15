import os
import logging
from db import *
from messages import *
from bot_functions import *

def define_commands():
    command_dict = {'!crossword' : enter_crossword_command,
                    '!c' : enter_crossword_command,
                    '!archive' : enter_archive_command,
                    '!a' : enter_archive_command,
                    '!both' : enter_both_command,
                    '!b' : enter_both_command,
                    '!streak' : display_streak}
    return command_dict

async def display_streak(param_array, message, client):
    discord_id = message.author.id
    streak = get_streak(discord_id)
    await streak_message(client, message, streak)


async def create_score_from_message(time, message, client, isArchive):
    try:
        time = time_to_number(str(time)) #Calls a function to convert "hh:mm:ss" to integer seconds
        score_entered = enter_score(message.author.id, message.author.display_name,time,date_scrape(), isArchive) #Attempts to actual enter the score into the database
        if score_entered == 1:
            await success_message(client, message, time)
        else:
            await score_error(client, message)
    except Exception as e:
        logging.warning(e)
        await output_error(client, message)

async def enter_crossword_command(param_array, message, client):
    time = param_array[0]
    await create_score_from_message(time, message, client, False)
    #implement validation on time here

async def enter_archive_command(param_array, message, client):
    time = param_array[0]
    #implement validation on time here
    await create_score_from_message(time, message, client, True)

async def enter_both_command(param_array, message, client):
    try:
        time = param_array[0]
        await create_score_from_message(time, message, client, False)
        time = param_array[1]
        await create_score_from_message(time, message, client, True)
    except Exception as e:
        logging.warning(e)
        await output_error(client, message)