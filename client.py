from mcp.client import MCPClient

client = MCPClient("http://localhost:8000")  # Cambia el puerto si es necesario
result = client.tool(
    "agregar_usuario_mcp",
    nombre="Maria Lopez",
    email="maria@example.com",
    password="secreto456",
)
print(result)
