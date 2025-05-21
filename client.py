from mcp.client import MCPClient

client = MCPClient(
    "http://localhost:6277"
)  # Actualizado al puerto correcto del servidor
result = client.tool(
    "agregar_usuario_mcp",
    nombre="Maria Lopez",
    email="maria@example.com",
    password="secreto456",
)
print(result)
