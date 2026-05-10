from db import run_query


def recommend_users(user_name):
    query = """
    MATCH (u:Usuario {name: $user})-[:TIENE_INTERES]->(i)<-[:TIENE_INTERES]-(other)
    WHERE u <> other AND NOT (u)-[:SIGUE]->(other)
    
    OPTIONAL MATCH (u)-[:SIGUE]->(friend)-[:SIGUE]->(other)
    
    RETURN other.name AS user,
           COUNT(DISTINCT i) AS intereses_comunes,
           COUNT(DISTINCT friend) AS amigos_en_comun,
           (COUNT(DISTINCT i)*2 + COUNT(DISTINCT friend)*3) AS score
    ORDER BY score DESC
    LIMIT 5
    """
    
    result = run_query(query, {"user": user_name})
    return [record["user"] for record in result]


def recommend_users_with_reason(user_name):
    query = """
    MATCH (u:Usuario {name: $user})-[:TIENE_INTERES]->(i)<-[:TIENE_INTERES]-(other)
    WHERE u <> other AND NOT (u)-[:SIGUE]->(other)

    OPTIONAL MATCH (u)-[:SIGUE]->(friend)-[:SIGUE]->(other)

    RETURN other.name AS user,
           COUNT(DISTINCT i) AS intereses,
           COUNT(DISTINCT friend) AS amigos,
           (COUNT(DISTINCT i)*2 + COUNT(DISTINCT friend)*3) AS score
    ORDER BY score DESC
    LIMIT 5
    """

    result = run_query(query, {"user": user_name})

    return [
        {
            "usuario": r["user"],
            "intereses_comunes": r["intereses"],
            "amigos_en_comun": r["amigos"]
        }
        for r in result
    ]