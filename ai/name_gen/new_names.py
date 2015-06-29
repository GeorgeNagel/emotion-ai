from ai.name_gen.arthurian.new_names import \
    generate_names as fantasy_generate_names


def generate_name(gender, type="fantasy"):
    if type == "fantasy":
        # Create new names based on Arthurian names
        return fantasy_generate_names(gender, 1)[0]
    elif type == "arthurian":
        pass
    elif type == "old_welsh":
        pass
