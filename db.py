from neo4j import GraphDatabase
       
URI = "bolt://127.0.0.1:7687"
USER = "neo4j"
PASSWORD = "proyecto2basesdedatos" 

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))


def run_query(query, params=None):
    with driver.session() as session:
        return list(session.run(query, params or {}))


# -------------------------
# FUNCIONES PARA CREAR DATOS
# -------------------------

def create_user(name,username):
    query = "CREATE (:Usuario {name: $name, username: $username})"
    run_query(query, {"name": name, "username": username})
    
def delete_user(username):
    query = "MATCH (u:Usuario {username: $username}) DETACH DELETE u"
    run_query(query, {"username": username})


def create_interest(name):
    query = "CREATE (:Interes {name: $name})"
    run_query(query, {"name": name})


def add_interest(user, interes):
    query = """
    MATCH (u:Usuario {username: $user}), (i:Interes {name: $interes})
    CREATE (u)-[:TIENE_INTERES]->(i)
    """
    run_query(query, {"user": user, "interes": interes})


def follow(user1, user2):
    query = """
    MATCH (a:Usuario {username: $u1}), (b:Usuario {username: $u2})
    CREATE (a)-[:SIGUE]->(b)
    """
    run_query(query, {"u1": user1, "u2": user2})

def get_interests():
    query = """
    MATCH (i:Interes)
    RETURN i.name AS name
    ORDER BY i.name
    """

    result = run_query(query)

    return [record["name"] for record in result]

#   VERIFICACIONES

def user_exists(username):
    query = """
    MATCH (u:Usuario {username: $username})
    RETURN COUNT(u) > 0 AS exists
    """

    result = run_query(query, {
        "username": username
    })

    return result[0]["exists"]

def interest_exists(interest_name):
    query = """
    MATCH (i:Interes {name: $interest_name})
    RETURN COUNT(i) > 0 AS exists
    """

    result = run_query(query, {
        "interest_name": interest_name
    })

    return result[0]["exists"]

def already_follows(user1, user2):
    query = """
    MATCH (u1:Usuario {username: $user1})-[r:SIGUE]->(u2:Usuario {username: $user2})
    RETURN COUNT(r) > 0 AS exists
    """

    result = run_query(query, {
        "user1": user1,
        "user2": user2
    })

    return result[0]["exists"]

def already_has_interest(username, interest):
    query = """
    MATCH (u:Usuario {username: $username})-[r:TIENE_INTERES]->(i:Interes {name: $interest})
    RETURN COUNT(r) > 0 AS exists
    """

    result = run_query(query, {
        "username": username,
        "interest": interest
    })

    return result[0]["exists"]
# -------------------------
# LIMPIAR BASE DE DATOS
# -------------------------

def clear_db():
    run_query("MATCH (n) DETACH DELETE n")