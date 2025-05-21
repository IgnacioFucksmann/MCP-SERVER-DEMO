from mcp.server.fastmcp import FastMCP
import psycopg2


def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="postgres",
        user="postgres",  # Reemplaza por tu usuario real
        password="admin",  # Reemplaza por tu contraseña real
    )


# Create an MCP server
mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool()
def agregar_usuario_mcp(nombre: str, email: str, password: str) -> str:
    """
    Agrega un usuario a la base de datos.
    """
    try:
        agregar_usuario(nombre, email, password)
        return "Usuario agregado correctamente."
    except Exception as e:
        return f"Error al agregar usuario: {e}"


@mcp.tool()
def eliminar_usuario_mcp(email: str) -> str:
    """
    Elimina un usuario de la base de datos por email.
    """
    try:
        eliminar_usuario(email)
        return "Usuario eliminado correctamente."
    except Exception as e:
        return f"Error al eliminar usuario: {e}"


@mcp.tool()
def modificar_usuario_mcp(
    email: str, nuevo_nombre: str = None, nuevo_password: str = None
) -> str:
    """
    Modifica el nombre y/o password de un usuario por email.
    """
    try:
        modificar_usuario(email, nuevo_nombre, nuevo_password)
        return "Usuario modificado correctamente."
    except Exception as e:
        return f"Error al modificar usuario: {e}"


@mcp.tool()
def consultar_usuario_mcp(email: str = None) -> str:
    """
    Consulta usuarios. Si se pasa un email, busca ese usuario; si no, lista todos.
    """
    try:
        resultados = consultar_usuario(email)
        if not resultados:
            return "No se encontraron usuarios."
        respuesta = ""
        for row in resultados:
            respuesta += f"ID: {row[0]}, Nombre: {row[1]}, Email: {row[2]}\n"
        return respuesta
    except Exception as e:
        return f"Error al consultar usuario(s): {e}"


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# Funciones auxiliares
def agregar_usuario(nombre, email, password):
    """
    Inserta un nuevo usuario en la tabla usuario.
    """
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO usuario (nombre, email, password)
                    VALUES (%s, %s, %s)
                    """,
                    (nombre, email, password),
                )
    finally:
        conn.close()


def eliminar_usuario(email):
    """
    Elimina un usuario de la tabla usuario por email.
    """
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM usuario WHERE email = %s",
                    (email,),
                )
    finally:
        conn.close()


def modificar_usuario(email, nuevo_nombre=None, nuevo_password=None):
    """
    Modifica el nombre y/o password de un usuario por email.
    """
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                if nuevo_nombre and nuevo_password:
                    cur.execute(
                        "UPDATE usuario SET nombre = %s, password = %s WHERE email = %s",
                        (nuevo_nombre, nuevo_password, email),
                    )
                elif nuevo_nombre:
                    cur.execute(
                        "UPDATE usuario SET nombre = %s WHERE email = %s",
                        (nuevo_nombre, email),
                    )
                elif nuevo_password:
                    cur.execute(
                        "UPDATE usuario SET password = %s WHERE email = %s",
                        (nuevo_password, email),
                    )
    finally:
        conn.close()


def consultar_usuario(email=None):
    """
    Consulta usuarios. Si se pasa un email, busca ese usuario; si no, lista todos.
    """
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                if email:
                    cur.execute(
                        "SELECT id, nombre, email FROM usuario WHERE email = %s",
                        (email,),
                    )
                else:
                    cur.execute("SELECT id, nombre, email FROM usuario")
                return cur.fetchall()
    finally:
        conn.close()
