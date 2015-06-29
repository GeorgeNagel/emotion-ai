import random

from ai.core.agent import Agent


def wait_for_input():
    _ = raw_input()  # noqa


def joust(player_1, player_2):
    # Jousting phase
    player_1_mounted = True
    player_2_mounted = True
    while player_1_mounted and player_2_mounted:
        player_1_mounted, player_2_mounted = joust_pass(player_1, player_2)
    # Ground fighting phase
    player_1_health = 5
    player_2_health = 5
    player_1_advantage = int(player_1_mounted)
    player_2_advantage = int(player_2_mounted)
    if player_1_advantage > player_2_advantage:
        advantage = 'p1'
    elif player_2_advantage > player_1_advantage:
        advantage = 'p2'
    else:
        advantage = 'neither'
    wait_for_input()
    print "%s and %s pull their swords out and prepare for hand combat." % (
        player_1.name, player_2.name)
    while (player_1_health > 0) and (player_2_health > 0):
        player_1_advantage, player_1_health, \
            player_2_advantage, player_2_health = sword_fight(
                player_1, player_1_advantage,
                player_1_health, player_2,
                player_2_advantage, player_2_health)
    if (player_1_health <= 0) and (player_2_health <= 0):
        print "%s and %s lie bloodied on the ground." % (
            player_1.name, player_2.name)
    elif player_1_health <= 0:
        print "%s lies bloodied on the ground." % player_1.name
    elif player_2_health <= 0:
        print "%s lies bloodied on the ground." % player_2.name
    player_1_alive = (player_1_health > 0)
    player_2_alive = (player_2_health > 0)
    return (advantage, player_1_alive, player_2_alive)


def joust_pass(player_1, player_2):
    print "%s and %s gallop towards each other at high speed." % (
        player_1.name, player_2.name
    )
    wait_for_input()
    player_1_mounted = True
    player_2_mounted = True
    dice_roll = random.choice(range(10))
    if dice_roll < 5:
        # Nothing happens
        print "Both hits miss. They turn around and line up for another pass."
    elif dice_roll < 7:
        # Player 1 knocked off
        print "%s is hit square in the chest and is thrown to the ground." % (
            player_1.name)
        player_1_mounted = False
    elif dice_roll < 9:
        # Player 2 knocked off
        print "%s is knocked straight on and is thrown to the ground." % (
            player_2.name)
        player_2_mounted = False
    else:
        # Both knocked off
        print "%s and %s collide and are both thrown to the ground." % (
            player_1.name, player_2.name
        )
        player_1_mounted = False
        player_2_mounted = False
    return (player_1_mounted, player_2_mounted)


def sword_fight(p1, p1_advantage, p1_health, p2, p2_advantage, p2_health):
    if p1_advantage > p2_advantage:
        print "%s takes the high ground." % p1.name
    elif p2_advantage > p1_advantage:
        print "%s takes the high ground." % p2.name
    wait_for_input()
    p1_advantage, p2_health, p2_advantage = sword_attack(
        p1, p1_advantage, p2, p2_health, p2_advantage)
    wait_for_input()
    p2_advantage, p1_health, p1_advantage = sword_attack(
        p2, p2_advantage, p1, p1_health, p1_advantage)
    return (p1_advantage, p1_health, p2_advantage, p2_health)


def sword_attack(attacker, attacker_advantage,
                 defender, defender_health, defender_advantage):
    dice_size = max((10 + attacker_advantage - defender_advantage), 1)
    dice_roll = random.choice(range(dice_size))
    # 1-2 defender gains an advantage
    # 3-4 defender blocks
    # 5-6 attacker gains an advantage
    # 7-8 attacker wounds 1
    # 9 attacker wounds 2
    print "%s slashes at %s." % (attacker.name, defender.name)
    if dice_roll < 3:
        print "%s parries into better position." % defender.name
        defender_advantage = defender_advantage + 1
    elif dice_roll < 5:
        print "%s blocks the attack." % defender.name
    elif dice_roll < 7:
        print "%s blocks the attack and %s presses forward." % (
            defender.name, attacker.name)
        attacker_advantage = attacker_advantage + 1
    elif dice_roll < 9:
        print "%s makes contact and %s shows blood." % (
            attacker.name, defender.name)
        attacker_advantage = attacker_advantage + 1
        defender_health = defender_health - 1
    else:
        print "%s wounds %s deeply." % (attacker.name, defender.name)
        attacker_advantage = attacker_advantage + 1
        defender_health = defender_health - 2
    attacker_advantage = max(attacker_advantage, 2)
    defender_advantage = max(defender_advantage, 2)
    return (attacker_advantage, defender_health, defender_advantage)


if __name__ == "__main__":
    runs = 1
    while runs > 0:
        runs = runs - 1
        p1 = Agent.create_random_agent()
        p2 = Agent.create_random_agent()
        advantage, p1alive, p2alive = joust(p1, p2)
