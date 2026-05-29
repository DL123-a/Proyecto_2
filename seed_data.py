from db import *

import csv
import random
import re

# --------------------------------
# CONFIGURACION
# --------------------------------

random.seed(42)

MALE_FILE = "male.txt"
FEMALE_FILE = "female.txt"
HOBBIES_FILE = "hobbies.csv"

MAX_USERS = 1000

MIN_SECONDARY_INTERESTS = 1
MAX_SECONDARY_INTERESTS = 2

MIN_INTERNAL_FOLLOWS = 4
MAX_INTERNAL_FOLLOWS = 8

MIN_EXTERNAL_FOLLOWS = 1
MAX_EXTERNAL_FOLLOWS = 3


# --------------------------------
# HELPERS
# --------------------------------

def generate_username(name):

    username = name.lower()

    username = re.sub(
        r'[^a-z0-9]',
        '',
        username
    )

    return username


# --------------------------------
# LEER NOMBRES
# --------------------------------

def load_names():

    names = []

    with open(
        MALE_FILE,
        encoding="utf-8"
    ) as file:

        for line in file:

            name = line.strip()

            if name:
                names.append(name)

    with open(
        FEMALE_FILE,
        encoding="utf-8"
    ) as file:

        for line in file:

            name = line.strip()

            if name:
                names.append(name)

    random.shuffle(names)

    return names[:MAX_USERS]


# --------------------------------
# LEER HOBBIES
# --------------------------------

def load_hobbies():

    hobbies = []

    with open(
        HOBBIES_FILE,
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.reader(file)

        next(reader)

        for row in reader:

            if row:

                hobbies.append(
                    row[0].strip()
                )

    return hobbies


# --------------------------------
# CREAR USUARIOS
# --------------------------------

def create_users(names):

    usernames_used = set()

    users = []

    for name in names:

        username = generate_username(name)

        original = username
        counter = 1

        while username in usernames_used:

            username = (
                f"{original}{counter}"
            )

            counter += 1

        usernames_used.add(username)

        create_user(
            name,
            username
        )

        users.append(
            (
                name,
                username
            )
        )

    return users


# --------------------------------
# CREAR INTERESES
# --------------------------------

def create_interests(hobbies):

    for hobby in hobbies:

        if not interest_exists(hobby):

            create_interest(hobby)


# --------------------------------
# CREAR COMUNIDADES
# --------------------------------

def assign_interests(users, hobbies):

    communities = {}

    for hobby in hobbies:

        communities[hobby] = []

    for _, username in users:

        primary = random.choice(
            hobbies
        )

        communities[primary].append(
            username
        )

        add_interest(
            username,
            primary
        )

        secondary_count = random.randint(
            MIN_SECONDARY_INTERESTS,
            MAX_SECONDARY_INTERESTS
        )

        secondary = random.sample(
            hobbies,
            secondary_count
        )

        for hobby in secondary:

            if hobby != primary:

                if not already_has_interest(
                    username,
                    hobby
                ):

                    add_interest(
                        username,
                        hobby
                    )

    return communities


# --------------------------------
# CREAR RELACIONES INTERNAS
# --------------------------------

def create_internal_follows(
    communities
):

    for hobby in communities:

        users = communities[hobby]

        if len(users) < 2:
            continue

        for user in users:

            amount = random.randint(
                MIN_INTERNAL_FOLLOWS,
                min(
                    MAX_INTERNAL_FOLLOWS,
                    len(users) - 1
                )
            )

            possible = [
                u
                for u in users
                if u != user
            ]

            selected = random.sample(
                possible,
                amount
            )

            for followed in selected:

                if not already_follows(
                    user,
                    followed
                ):

                    follow(
                        user,
                        followed
                    )


# --------------------------------
# CREAR RELACIONES EXTERNAS
# --------------------------------

def create_external_follows(users):

    usernames = [
        username
        for _, username in users
    ]

    for user in usernames:

        amount = random.randint(
            MIN_EXTERNAL_FOLLOWS,
            MAX_EXTERNAL_FOLLOWS
        )

        possible = [
            u
            for u in usernames
            if u != user
        ]

        selected = random.sample(
            possible,
            amount
        )

        for followed in selected:

            if not already_follows(
                user,
                followed
            ):

                follow(
                    user,
                    followed
                )


# --------------------------------
# MAIN
# --------------------------------

def load_realistic_data():

    print("Limpiando base de datos...")

    clear_db()

    hobbies = load_hobbies()

    names = load_names()

    print(
        f"{len(names)} usuarios encontrados"
    )

    print(
        f"{len(hobbies)} hobbies encontrados"
    )

    create_interests(
        hobbies
    )

    users = create_users(
        names
    )

    communities = assign_interests(
        users,
        hobbies
    )

    create_internal_follows(
        communities
    )

    create_external_follows(
        users
    )

    print(
        "Base de datos creada correctamente"
    )


if __name__ == "__main__":

    load_realistic_data()