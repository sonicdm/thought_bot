from thought_bot.game import start_game


def run_bot():
    print("Welcome to the Thought Bot.\n"
          "###########################\n")

    host_name = "Your thoughts"
    player_name = None
    while not player_name:
        player_name = raw_input("What is your name?:")
    start_game(player_name, host_name)


if __name__ == "__main__":
    run_bot()
    raw_input('Press Enter to Exit')
