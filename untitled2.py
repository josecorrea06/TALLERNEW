import sqlite3
from datetime import datetime, timedelta

# Conexión a la base de datos SQLite
conn = sqlite3.connect("clientes.db")
cursor = conn.cursor()

# ------------------ Creación de Tablas ------------------
def crear_tablas():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            contacto TEXT,
            historial_compras TEXT,
            preferencias TEXT,
            fecha_ultima_compra DATE,
            inactivo BOOLEAN DEFAULT 0
        )
    ''')
    print("Tablas creadas correctamente.")

# ------------------ Funciones CRUD ------------------
def agregar_cliente(nombre, contacto, historial_compras, preferencias):
    cursor.execute('''
        INSERT INTO clientes (nombre, contacto, historial_compras, preferencias, fecha_ultima_compra)
        VALUES (?, ?, ?, ?, ?)
    ''', (nombre, contacto, historial_compras, preferencias, datetime.now().date()))
    conn.commit()
    print("Cliente agregado correctamente.")

def actualizar_cliente(id_cliente, nombre=None, contacto=None):
    if nombre:
        cursor.execute("UPDATE clientes SET nombre = ? WHERE id = ?", (nombre, id_cliente))
    if contacto:
        cursor.execute("UPDATE clientes SET contacto = ? WHERE id = ?", (contacto, id_cliente))
    conn.commit()
    print("Cliente actualizado correctamente.")

def eliminar_cliente(id_cliente):
    cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
    conn.commit()
    print("Cliente eliminado correctamente.")

def buscar_clientes():
    cursor.execute("SELECT * FROM clientes")
    for cliente in cursor.fetchall():
        print(cliente)

# ------------------ Triggers Simulados ------------------
def verificar_clientes_inactivos():
    fecha_limite = datetime.now().date() - timedelta(days=365)  # 1 año sin compras
    cursor.execute("UPDATE clientes SET inactivo = 1 WHERE fecha_ultima_compra <= ?", (fecha_limite,))
    conn.commit()
    print("Clientes inactivos actualizados.")

def alertar_patrones_compra():
    cursor.execute("SELECT * FROM clientes WHERE historial_compras LIKE '%repetido%'")
    print("Clientes con patrones de compra inusuales:")
    for cliente in cursor.fetchall():
        print(cliente)

# ------------------ Eventos Programados ------------------
def generar_reporte_clientes():
    print("Generando reporte de clientes y ventas...")
    cursor.execute("SELECT nombre, historial_compras FROM clientes")
    for reporte in cursor.fetchall():
        print(reporte)

def limpieza_anual():
    print("Realizando limpieza anual de registros obsoletos...")
    cursor.execute("DELETE FROM clientes WHERE inactivo = 1")
    conn.commit()
    print("Registros obsoletos eliminados.")

# ------------------ Ejecución del Sistema ------------------
if __name__ == "__main__":
    crear_tablas()

    # Ejemplo de uso
    agregar_cliente("Juan Perez", "juan@example.com", "Compra repetida de producto A", "Preferencia: Electrónicos")
    agregar_cliente("Maria Lopez", "maria@example.com", "Compra única", "Preferencia: Ropa")

    print("\n--- Clientes Registrados ---")
    buscar_clientes()

    print("\n--- Verificación de Clientes Inactivos ---")
    verificar_clientes_inactivos()

    print("\n--- Alertas de Patrones de Compra ---")
    alertar_patrones_compra()

    print("\n--- Generación de Reporte ---")
    generar_reporte_clientes()

    print("\n--- Limpieza Anual de Datos ---")
    limpieza_anual()

    conn.close()