import json
import random
import time

# Global dictionary to track the player's state
player = {
    "name": "",
    "hp": 100,
    "max_hp": 100,
    "attack": 20,
    "gold": 0,
    "inventory": ["Health Potion"],
}


def print_slow(text, delay=0.03):
    """Prints text directly to prevent terminal buffer freezing."""
    print(text)


def load_game():
    """Loads save data from a JSON file if it exists."""
    global player
    try:
        with open("savegame.json", "r") as file:
            player = json.load(file)
            print_slow("\n[+] Save file found! Character data loaded.")
    except FileNotFoundError:
        print_slow("\n[*] No save file found. Starting a new adventure!")


def save_game():
    """Saves the current player state to a JSON file."""
    try:
        with open("savegame.json", "w") as file:
            json.dump(player, file, indent=4)
            print_slow("\n[✓] Game successfully saved to 'savegame.json'!")
    except Exception as e:
        print(f"Error saving game: {e}")


def show_stats():
    """Displays player stats and inventory."""
    print("\n" + "=" * 30)
    print(f" HERO: {player['name']}")
    print(f" Health (HP): {player['hp']}/{player['max_hp']}")
    print(f" Attack: {player['attack']}")
    print(f" Gold: {player['gold']} coins")
    print(f" Inventory: {', '.join(player['inventory'])}")
    print("=" * 30)


def use_potion():
    """Consumes a Health Potion from the player's inventory."""
    if "Health Potion" in player["inventory"]:
        player["inventory"].remove("Health Potion")
        heal_amount = 35
        player["hp"] = min(player["max_hp"], player["hp"] + heal_amount)
        print_slow(f"\n[+] You drank a potion! Restored {heal_amount} HP. Current HP: {player['hp']}")
    else:
        print_slow("\n[!] You don't have any Health Potions in your inventory!")


def battle():
    """Interactive battle loop against a random monster."""
    monsters = [
        {"name": "Goblin", "hp": 40, "attack": 10, "gold": 15},
        {"name": "Orc Warrior", "hp": 70, "attack": 18, "gold": 35},
        {"name": "Shadow Knight", "hp": 110, "attack": 25, "gold": 70},
    ]

    monster = random.choice(monsters)
    monster_hp = monster["hp"]

    print_slow(f"\n[!] A fierce {monster['name']} appeared! (HP: {monster_hp}, Attack: {monster['attack']})")

    while monster_hp > 0 and player["hp"] > 0:
        print(f"\nYour HP: {player['hp']} | {monster['name']} HP: {monster_hp}")
        print("1. Attack")
        print("2. Use Health Potion")
        print("3. Run away")

        choice = input("Choose an action (1-3): ").strip()

        if choice == "1":
            # Player attack with critical hit chance
            damage = random.randint(player["attack"] - 5, player["attack"] + 5)
            is_critical = random.random() < 0.2  # 20% critical hit chance

            if is_critical:
                damage *= 2
                print_slow(f"💥 CRITICAL HIT! You dealt {damage} damage!")
            else:
                print_slow(f"⚔️ You attacked the {monster['name']} and dealt {damage} damage.")

            monster_hp -= damage

            # Monster counter-attack if still alive
            if monster_hp > 0:
                monster_damage = random.randint(monster["attack"] - 3, monster["attack"] + 3)
                player["hp"] -= monster_damage
                print_slow(f"👹 The {monster['name']} attacked back and dealt {monster_damage} damage!")

        elif choice == "2":
            use_potion()

        elif choice == "3":
            if random.random() < 0.5:
                print_slow("\n🏃 You successfully escaped from the battle!")
                return
            else:
                print_slow("\n[!] Failed to escape! The monster strikes you from behind!")
                player["hp"] -= monster["attack"]

        else:
            print_slow("Invalid choice! You waste time and the monster takes advantage!")

    # Battle outcome check
    if player["hp"] <= 0:
        print_slow("\n☠️ You were defeated in battle... GAME OVER!")
    else:
        print_slow(f"\n🎉 You defeated the {monster['name']}!")
        player["gold"] += monster["gold"]
        print_slow(f"[+] You found {monster['gold']} gold coins!")

        # Chance to drop a health potion after victory
        if random.random() < 0.4:
            player["inventory"].append("Health Potion")
            print_slow("[+] You also looted a Health Potion!")


def explore():
    """Exploration handler with random dungeon events."""
    print_slow("\n🔍 Exploring the depths of the dungeon...")
    time.sleep(0.5)

    event = random.choice(["battle", "treasure", "empty"])

    if event == "battle":
        battle()
    elif event == "treasure":
        found_gold = random.randint(10, 30)
        player["gold"] += found_gold
        print_slow(f"\n💰 You found an abandoned chest containing {found_gold} gold coins!")
    else:
        print_slow("\n...The room is empty and quiet. Nothing happens.")


def main():
    print_slow("=== WELCOME TO THE DUNGEON OF SHADOW ===")
    
    load_game()

    if not player["name"]:
        player["name"] = input("\nEnter your hero's name: ").strip()
        if not player["name"]:
            player["name"] = "Hero"

    while player["hp"] > 0:
        print("\n--- MAIN MENU ---")
        print("1. Explore Dungeon (Battle / Treasure)")
        print("2. View Stats & Inventory")
        print("3. Use Health Potion")
        print("4. Save Game")
        print("5. Quit Game")

        choice = input("Choose an action (1-5): ").strip()

        if choice == "1":
            explore()
        elif choice == "2":
            show_stats()
        elif choice == "3":
            use_potion()
        elif choice == "4":
            save_game()
        elif choice == "5":
            save_game()
            print_slow("\nYou left the adventure. See you next time!")
            break
        else:
            print_slow("Invalid choice!")


if __name__ == "__main__":
    main()

