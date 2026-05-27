import streamlit as st
from typing import List
from db import *
from recommendation import recommend_users_with_reason

# ------------------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Gestor de Grafo Social",
    layout="wide"
)

st.title("Sistema de Recomendación de Usuarios")
st.write("Interfaz para administrar usuarios, intereses y relaciones del grafo.")

# ------------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------------
st.sidebar.title("Menú")

section = st.sidebar.radio(
    "Selecciona una opción",
    [
        "Agregar Usuario",
        "Eliminar Usuario",
        "Crear Interés",
        "Agregar Interés a Usuario",
        "Seguir Usuario",
        "Recomendaciones"
    ]
)


# ------------------------------------------------------------------
# AGREGAR USUARIO
# ------------------------------------------------------------------
if section == "Agregar Usuario":
    st.header("Agregar Usuario")

    with st.form("add_user_form"):
        name = st.text_input("Nombre completo")
        username = st.text_input("Nombre de usuario único")

        available_interests = get_interests()

        selected_interests = st.multiselect(
            "Selecciona intereses",
            options=available_interests
        )

        submit_add_user = st.form_submit_button("Crear Usuario")

        if submit_add_user:
            if name.strip() and username.strip():
                try:

                    if user_exists(username):
                        st.error("El nombre de usuario ya existe")

                    else:
                        create_user(name, username)

                        for interest in selected_interests:
                            add_interest(username, interest)

                        st.success(f"Usuario '{username}' creado correctamente")

                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Completa todos los campos")


# ------------------------------------------------------------------
# ELIMINAR USUARIO
# ------------------------------------------------------------------
elif section == "Eliminar Usuario":
    st.header("Eliminar Usuario")

    if "confirm_delete" not in st.session_state:
        st.session_state.confirm_delete = False

    if "user_to_delete" not in st.session_state:
        st.session_state.user_to_delete = ""

    with st.form("delete_user_form"):
        delete_username = st.text_input("Nombre de usuario único")

        submit_delete = st.form_submit_button("Eliminar Usuario")

        if submit_delete:
            if delete_username.strip():
                if user_exists(delete_username):
                    st.session_state.confirm_delete = True
                    st.session_state.user_to_delete = delete_username

                else:
                    st.error("Ese usuario no existe")
            else:
                st.warning("Ingresa un nombre de usuario")

    if st.session_state.confirm_delete:
        st.warning(
            f"¿Seguro que deseas eliminar al usuario '@{st.session_state.user_to_delete}'?"
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Confirmar eliminación"):
                try:
                    delete_user(st.session_state.user_to_delete)

                    st.success(
                        f"Usuario '@{st.session_state.user_to_delete}' eliminado"
                    )

                    st.session_state.confirm_delete = False
                    st.session_state.user_to_delete = ""

                except Exception as e:
                    st.error(f"Error: {e}")

        with col2:
            if st.button("Cancelar"):
                st.session_state.confirm_delete = False
                st.session_state.user_to_delete = ""
                st.info("Eliminación cancelada")


# ------------------------------------------------------------------
# CREAR INTERÉS
# ------------------------------------------------------------------
elif section == "Crear Interés":
    st.header("Crear Interés")

    with st.form("create_interest_form"):
        interest_name = st.text_input("Nombre del interés")

        submit_interest = st.form_submit_button("Crear Interés")

        if submit_interest:
            if interest_name.strip():
                try:
                    if interest_exists(interest_name):
                        st.warning("Ese interés ya existe")

                    else:
                        create_interest(interest_name)
                        st.success(f"Interés '{interest_name}' creado")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Ingresa un interés válido")


# ------------------------------------------------------------------
# AGREGAR INTERÉS A USUARIO
# ------------------------------------------------------------------
elif section == "Agregar Interés a Usuario":
    st.header("Agregar Interés a Usuario")

    with st.form("add_interest_user_form"):
        username_interest = st.text_input("Nombre de usuario")

        available_interests = get_interests()

        selected_interest = st.selectbox(
            "Selecciona un interés",
            options=available_interests
        )

        submit_add_interest = st.form_submit_button("Agregar Interés")

        if submit_add_interest:
            if username_interest.strip():
                try:
                    if already_has_interest(username_interest, selected_interest):
                        st.warning(
                            f"El usuario ya tiene el interés '{selected_interest}'"
                        )
                    else:
                        add_interest(username_interest, selected_interest)

                        st.success(
                            f"Interés '{selected_interest}' agregado a '{username_interest}'"
                        )

                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Ingresa un nombre de usuario")


# ------------------------------------------------------------------
# SEGUIR USUARIO
# ------------------------------------------------------------------
elif section == "Seguir Usuario":
    st.header("Seguir Usuario")

    with st.form("follow_user_form"):
        follower = st.text_input(
            "Usuario que seguirá (nombre o username)"
        )

        followed = st.text_input(
            "Usuario a seguir (nombre o username)"
        )

        submit_follow = st.form_submit_button("Seguir")

        if submit_follow:
            if follower.strip() and followed.strip():
                try:
                    if follower == followed:
                        st.warning("Un usuario no puede seguirse a sí mismo")

                    elif already_follows(follower, followed):
                        st.warning(
                            f"'{follower}' ya sigue a '{followed}'"
                        )

                    else:
                        follow(follower, followed)
                        st.success(f"'{follower}' ahora sigue a '{followed}'")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Completa todos los campos")

# ------------------------------------------------------------------
# RECOMENDACIONES
# ------------------------------------------------------------------
elif section == "Recomendaciones":

    st.header("Recomendaciones de Usuarios")

    username_recommendation = st.text_input(
        "Nombre de usuario"
    )

    amount = st.slider(
        "Cantidad de recomendaciones",
        min_value=1,
        max_value=20,
        value=5
    )

    if st.button("Generar Recomendaciones"):

        if username_recommendation.strip():

            try:

                recommendations = recommend_users_with_reason(
                    username_recommendation
                )

                if recommendations:

                    st.subheader("Usuarios recomendados")

                    for user in recommendations[:amount]:

                        with st.container(border=True):

                            st.markdown(
                                f"### @{user['usuario']}"
                            )

                            st.write(
                                f"Amigos en común: {user['amigos_en_comun']}"
                            )

                            st.write(
                                "Intereses compartidos: " +
                                ", ".join(user['intereses_lista'])
                            )

                            if st.button(
                                f"Seguir @{user['usuario']}",
                                key=user['usuario']
                            ):

                                follow(
                                    username_recommendation,
                                    user['usuario']
                                )

                                st.success(
                                    f"Ahora sigues a @{user['usuario']}"
                                )

                else:
                    st.info(
                        "No se encontraron recomendaciones para este usuario"
                    )

            except Exception as e:
                st.error(f"Error: {e}")

        else:
            st.warning("Ingresa un nombre de usuario")



# ------------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------------
st.divider()
st.caption("Interfaz desarrollada con Streamlit")
