from neo4j import GraphDatabase

URI = "neo4j://127.0.0.1:7687"
USER = "neo4j"
PASSWORD = "proyecto2basesdedatos" 

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))


def run_query(query, params=None):
    with driver.session() as session:
        return list(session.run(query, params or {}))


# -------------------------
# FUNCIONES PARA CREAR DATOS
# -------------------------

def create_user(name):
    query = "CREATE (:Usuario {name: $name})"
    run_query(query, {"name": name})


def create_interest(name):
    query = "CREATE (:Interes {name: $name})"
    run_query(query, {"name": name})


def add_interest(user, interest):
    query = """
    MATCH (u:Usuario {name: $user}), (i:Interes {name: $interest})
    CREATE (u)-[:TIENE_INTERES]->(i)
    """
    run_query(query, {"user": user, "interest": interest})


def follow(user1, user2):
    query = """
    MATCH (a:Usuario {name: $u1}), (b:Usuario {name: $u2})
    CREATE (a)-[:SIGUE]->(b)
    """
    run_query(query, {"u1": user1, "u2": user2})


# -------------------------
# LIMPIAR BASE DE DATOS
# -------------------------

def clear_db():
    run_query("MATCH (n) DETACH DELETE n")