# Python-second-project
Notes Telegram bot @my_notes22_bot
This Notes bot helps keeping record of your notes. you can:
    1. add a note using /add then the note in the same message.
    2. delete a note using /delete then its number in the same message.
    3. change a note using /edit then the number of the note in the same message.
    4. see your notes using /show.
    5. delete all your notes using /stopservice
  it also has /start and /help commands.

about the code:
first we have data_base = {} which is a dictionary that would be used to store the notes.
global waiting_reply is an integer that would be used to indicate if a function needed further action done after the command but in a separate message. when it's zero, it means no further action is required.
now about the functions:
@dp.message_handler(): It's a simple commands handler, it can be used to filter commands
After every handler with the specified command, we define a function that handles this command accordingly, which are:
1. process_start_command(message: types.Message): a function that takes a message object as a parameter, it only sends a welcome message and refers to the help command for bot's info.
2. process_help_command(message: types.Message): in case a help command was sent it only sends a message with the available commands and how to use them.
3. process_show_command(message: types.Message): in case the user doesn't have notes, it sends a message informing them, othe wise it creates a string text, each line in it is first a number from 1 to notes number, then the note then a new line using "\n"
4. process_add_command(msg: types.Message): if the user sent the command with no extra letters, it asks them to send the note in the same message, if it was sent after the command, it adds it to the list of notes after creating a key with an empty list for the user if they were not registered yet.
5. process_delete_command(msg: types.Message): first it checks if the user has anynotes, if not it sends them a message informing them of that, if they only wrote the command without any numbers it also informs them to put the number after the command, if the number isn't valid it informs them, if everything is in place  the note is deleted and a message is sent.
6. process_stop_command(msg: types.Message): this function deletes the whole record of notes but not by itself, after making sure the user is in the data_base it sends the user a message asking him to confirm the choice and changes waiting_reply to -1, if the user types the confirmation message, the without_command function deletes the user record completely.
7. process_edit_command(msg: types.Message): if the user has no notes, isn't in the database or sent the command without the number the functions sends a message to inform them, if they sent a number bigger than the number of their notes or some unvalid number the function also informs them. if everything was in order, the function changes the value of waiting_reply to the number of the note that they want to change.
8. process_without_command(msg: types.Message): 

