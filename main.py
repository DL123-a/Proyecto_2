from recommendation import recommend_users_with_reason

usuario = "aaron"

recomendaciones = recommend_users_with_reason(usuario)

print(f"\nRecomendaciones para @{usuario}\n")

for r in recomendaciones:

    print(
        f"@{r['usuario']} | "
        f"Intereses en común: {r['intereses_comunes']} | "
        f"Amigos en común: {r['amigos_en_comun']}"
    )