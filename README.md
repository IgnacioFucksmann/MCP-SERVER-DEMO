# MCP Server Demo con Streamlit y Ollama

Este proyecto es una demo de un servidor MCP (Model Context Protocol) en Python, integrado con una interfaz de chat web hecha en Streamlit y un modelo de lenguaje local usando Ollama. Permite gestionar usuarios en una base de datos PostgreSQL (agregar, eliminar, modificar, consultar) tanto desde el chat como desde herramientas MCP externas.

## Características

- **Chat web** con Streamlit.
- **LLM local** usando Ollama (Llama 3 u otro modelo compatible).
- **Servidor MCP** con herramientas para CRUD de usuarios.
- **Base de datos PostgreSQL** para almacenar usuarios.
- **Integración flexible**: puedes usar solo el chat, solo el servidor MCP, o ambos.

## Requisitos

- Python 3.9+
- PostgreSQL corriendo y accesible
- [Ollama](https://ollama.com/) instalado y corriendo (para LLM local)
- Entorno virtual (recomendado)
- Las dependencias del archivo `requirements.txt`

## Instalación

1. Clona el repositorio:
   ```sh
   git clone https://github.com/tu-usuario/mcp-server-demo.git
   cd mcp-server-demo
   ```

2. Crea y activa un entorno virtual:
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # En Linux/Mac
   .venv\\Scripts\\activate   # En Windows
   ```

3. Instala las dependencias:
   ```sh
   pip install -r requirements.txt
   ```

4. Configura tu base de datos PostgreSQL y ajusta los datos de conexión en `server.py`.

5. (Opcional) Crea un archivo `.env` si usas claves de API.

## Uso

### 1. Levanta Ollama y el modelo LLM

```sh
ollama run llama3
```

### 2. Levanta el chat de Streamlit

```sh
streamlit run streamlit.py
```

Abre el navegador en [http://localhost:8501](http://localhost:8501).

### 3. (Opcional) Levanta el servidor MCP

```sh
mcp run server.py
```
o
```sh
uv run --with mcp mcp run server.py
```

## Funcionalidades del chat

- **Agregar usuario:**  
  Escribe: `agregar usuario Juan juan@mail.com clave123`
- **Eliminar usuario:**  
  Escribe: `eliminar usuario juan@mail.com`
- **Modificar usuario:**  
  Escribe: `modificar usuario juan@mail.com nombre=Juan Perez contraseña=nuevaClave`
- **Consultar usuarios:**  
  Escribe: `consultar usuarios` o `consultar usuario juan@mail.com`
- **Conversación libre:**  
  Si el mensaje no es una acción, responde la LLM local.

## Créditos

- [Streamlit](https://streamlit.io/)
- [Ollama](https://ollama.com/)
- [psycopg2](https://www.psycopg.org/)
- [Model Context Protocol (MCP)](https://modelcontext.com/)

---

¡Contribuciones y sugerencias son bienvenidas!