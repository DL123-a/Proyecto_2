from db import *
import random

gaming_users = [
    ("Alex Perez", "alex_gamer"),
    ("Daniel Ruiz", "darkplayer"),
    ("Carlos Gomez", "noobmaster"),
    ("Ana Morales", "pixel_ana"),
    ("Luis Castro", "luisXP"),
    ("Mario Flores", "marioplays"),
    ("Kevin Lopez", "kev_gaming"),
    ("Sofia Vega", "sofia_otaku"),
    ("Jorge Diaz", "prostream"),
    ("Valeria Leon", "val_gamer")
]

tech_users = [
    ("Mario Dev", "mario_dev"),
    ("Sofia Ramirez", "sofia.codes"),
    ("Luis Herrera", "ai_luis"),
    ("Andrea Castillo", "andreaTech"),
    ("Carlos Mendez", "byteCarlos"),
    ("Elena Torres", "elena_dev"),
    ("Fernando Cruz", "fernandoAI"),
    ("Patricia Soto", "pat_code"),
    ("Ricardo Silva", "ricTech"),
    ("Natalia Gomez", "nata_dev")
]

art_users = [
    ("Sofia Lopez", "sofia_art"),
    ("Maria Perez", "lens_maria"),
    ("Jose Ramirez", "draw_jose"),
    ("Andrea Luna", "andrea_sketch"),
    ("Camila Torres", "cam_design"),
    ("Lucia Morales", "lucia_photo"),
    ("Gabriel Soto", "gab_artist"),
    ("Valentina Ruiz", "val_draws"),
    ("Paula Garcia", "paula_creative"),
    ("Diego Flores", "diego_visual")
]

fitness_users = [
    ("Luis Gomez", "fit_luis"),
    ("Ana Torres", "gym_ana"),
    ("Carlos Vega", "carlosfit"),
    ("Daniela Ruiz", "dani_runner"),
    ("Miguel Castro", "miguelGym"),
    ("Patricia Lopez", "healthy_paty"),
    ("Fernando Morales", "fernando_fit"),
    ("Andrea Silva", "andrea_yoga"),
    ("Kevin Diaz", "kevinWorkout"),
    ("Valeria Perez", "val_fitlife")
]

social_users = [
    ("Ana Lopez", "ana_lifestyle"),
    ("Sofia Morales", "sofi_travel"),
    ("Carlos Ruiz", "carloscine"),
    ("Lucia Gomez", "lucia_foodie"),
    ("Diego Perez", "diego_marketing"),
    ("Camila Silva", "camilaStyle"),
    ("Miguel Torres", "miguel_vibes"),
    ("Patricia Garcia", "pat_social"),
    ("Fernando Diaz", "fernandoTrips"),
    ("Valentina Castro", "val_music")
]

interests = [
    "Gaming",
    "Anime",
    "Programacion",
    "Musica",
    "Arte",
    "Fotografia",
    "Fitness",
    "Cine",
    "Viajes",
    "Lectura",
    "Streaming",
    "Diseño",
    "Inteligencia Artificial",
    "Videojuegos",
    "Tecnologia",
    "Naturaleza",
    "Moda",
    "Cocina",
    "Deportes",
    "Marketing"
]

group_interests = {
    "gaming": [
        "Gaming",
        "Anime",
        "Streaming",
        "Videojuegos"
    ],

    "tech": [
        "Programacion",
        "Inteligencia Artificial",
        "Tecnologia",
        "Gaming"
    ],

    "art": [
        "Arte",
        "Diseño",
        "Fotografia",
        "Musica"
    ],

    "fitness": [
        "Fitness",
        "Deportes",
        "Naturaleza",
        "Viajes"
    ],

    "social": [
        "Moda",
        "Cocina",
        "Marketing",
        "Cine",
        "Musica"
    ]
}

all_users = {
    "gaming": gaming_users,
    "tech": tech_users,
    "art": art_users,
    "fitness": fitness_users,
    "social": social_users
}

def load_realistic_data():

    # limpiar base de datos
    clear_db()

    print("Base de datos limpiada")

    
    # CREAR INTERESES
    
    for interest in interests:
        create_interest(interest)

    print("Intereses creados")

   
    # CREAR USUARIOS
  
    for group in all_users:

        for name, username in all_users[group]:

            create_user(name, username)

            # obtener intereses del grupo
            possible_interests = group_interests[group]

            # asignar entre 2 y 4 intereses
            selected = random.sample(
                possible_interests,
                random.randint(2, len(possible_interests))
            )

            for interest in selected:
                add_interest(username, interest)

    print("Usuarios e intereses creados")
    
        
    # CREAR RELACIONES SIGUE
    

    # follows dentro del mismo grupo
    for group in all_users:

        usernames = [
            username
            for _, username in all_users[group]
        ]

        for user in usernames:

            # cada usuario seguirá entre 2 y 5 personas
            amount = random.randint(2, 5)

            possible_follows = [
                u for u in usernames
                if u != user
            ]

            selected_follows = random.sample(
                possible_follows,
                amount
            )

            for followed in selected_follows:

                if not already_follows(user, followed):
                    follow(user, followed)

    print("Relaciones dentro de grupos creadas")
    
      
    # CREAR RELACIONES ENTRE GRUPOS
    

    all_usernames = []

    for group in all_users:
        for _, username in all_users[group]:
            all_usernames.append(username)

    for user in all_usernames:

        # cada usuario seguirá 1 o 2 usuarios de otros grupos
        amount = random.randint(1, 2)

        possible_follows = [
            u for u in all_usernames
            if u != user and not already_follows(user, u)
        ]

        selected_follows = random.sample(
            possible_follows,
            amount
        )

        for followed in selected_follows:
            follow(user, followed)

    print("Relaciones entre grupos creadas")
    
load_realistic_data()