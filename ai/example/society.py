"""Create agents and relationships."""
import random

from ai.core.agent import Agent, GENDERS
from ai.core.personality import combine_personalities
from ai.name_gen.new_names import generate_name


# Random variation of child from parents personalities
CHILD_PERSONALITY_VARIATION = 0.1

SEED_GENERATION_SIZE = 10
NUMBER_OF_GENERATIONS = 3
CHILDREN_PER_PARENTS = range(1, 6)


def create_society(seed_generation_size=SEED_GENERATION_SIZE,
                   number_of_generations=NUMBER_OF_GENERATIONS,
                   children_per_parents=CHILDREN_PER_PARENTS):
    agents = []

    # Create the seed generation
    first_generation = []
    while len(first_generation) < SEED_GENERATION_SIZE - 1:
        # Create seed generation agent
        agent = Agent.create_random_agent()
        first_generation.append(agent)

    generations = [first_generation]
    generations_created = 1
    while generations_created < NUMBER_OF_GENERATIONS:
        # Create a generation based on the previous generation
        generation = create_generation(
            generations[generations_created - 1], CHILDREN_PER_PARENTS
        )
        generations.append(generation)
        generations_created += 1

    for generation in generations:
        agents.extend(generation)
    return agents


def create_generation(previous_generation, children_per_parents):
    """children_per_parents - A list of possible number of children."""
    next_generation = []
    # Pair off parents
    males = [agent for agent in previous_generation if agent.gender == GENDERS.MALE]  # noqa
    females = [agent for agent in previous_generation if agent.gender == GENDERS.FEMALE]  # noqa
    couples = zip(males, females)
    for couple in couples:
        for birth in range(random.choice(children_per_parents)):
            child_gender = random.choice([GENDERS.MALE, GENDERS.FEMALE])
            child = create_child(couple[0], couple[1], child_gender)
            next_generation.append(child)
    return next_generation


def create_child(agent_1, agent_2, child_gender):
    """Create a new agent and relationships simulating childbirth."""
    if agent_1.gender == agent_2.gender:
        raise ValueError("Mating not possible.")

    # Create a new agent based on the personalities of the parents
    p1 = agent_1.personality
    p2 = agent_2.personality

    p3 = combine_personalities(p1, p2, CHILD_PERSONALITY_VARIATION)
    child = Agent.from_personality(p3)
    child.set_parents(agent_1, agent_2)
    child.name = generate_name(child_gender)
    child.gender = child_gender

    agent_1.add_child(child)
    agent_2.add_child(child)
    print "%s and %s have a child child: %s" % (
        agent_1.name, agent_2.name, child.name)
    return child
