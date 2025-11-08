# Auto Mailing Bot

## Overview

Auto Mailing Bot is a Telegram automation tool that sends messages on behalf of user Telegram accounts to selected groups. It helps users maintain visibility in Telegram communities, particularly useful for professionals in the logistics industry who want to stay noticed and receive more offers.

## Features

1. Automatic message sending on behalf of user accounts.
2. Ability to add multiple Telegram accounts and groups.
3. User authentication via username and password.
4. Configurable message intervals and durations.
5. Support for sending multiple messages in parallel.
6. Message history tracking and management.

## How It Works

1. Create an account or sign in to an existing one.
2. Start mailing through the bot interface and configure parameters such as intervals, durations, and message content.
3. Add your Telegram accounts using phone verification.
4. Add your target groups to the bot.
5. Select which accounts and groups to use for mailing.
6. Press **Start** to begin sending messages.
7. Sent or in-progress messages will appear in the message history section.
8. The system supports parallel message delivery to reduce the risk of account blocking.

## Internal Functionality

1. The bot records new messages in a normalized database, allowing users to interact with them efficiently.
2. A scheduled service (in development) will fetch recently added messages from the database.
3. The scheduler creates message delivery tasks stored in the database.
4. A message broker and background workers process these tasks asynchronously and reliably.

## Target Users

1. Individuals who need to send bulk text messages to selected Telegram groups.
2. Logistics professionals seeking better visibility to attract more business opportunities.

## Additional Information

1. Development is temporarily paused due to time constraints.
2. Approximately 50% of the bot's functionality has been completed.
