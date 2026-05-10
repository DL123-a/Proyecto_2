from db import *
from recommendation import recommend_users_with_reason


def load_sample_data():
    clear_db()

    create_user("Alice")
    create_user("Bob")
    create_user("Charlie")

    create_interest("Gaming")
    create_interest("Arte")

    add_interest("Alice", "Gaming")
    add_interest("Bob", "Gaming")
    add_interest("Charlie", "Arte")

    follow("Alice", "Bob")


if __name__ == "__main__":
    load_sample_data()

    recomendaciones = recommend_users_with_reason("Alice")

    print("Recomendaciones para Alice:\n")
    for r in recomendaciones:
        print(f"{r['usuario']} | Intereses en común: {r['intereses_comunes']} | Amigos en común: {r['amigos_en_comun']}")