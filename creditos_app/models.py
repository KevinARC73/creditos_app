from database import get_connection

def crear(cliente, monto, tasa_interes, plazo, fecha_otorgamiento):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                      INSERT INTO creditos (cliente, monto, tasa_interes, plazo, Fecha_otorgamiento) 
                      VALUES (?, ?, ?, ?, ?)"""
                      , (cliente, monto, tasa_interes, plazo, fecha_otorgamiento))
        conn.commit()
    return cursor.lastrowid

def obtener():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM creditos")
    return [dict(row) for row in cursor.fetchall()]

def actualizar(id, cliente, monto, tasa_interes, plazo, fecha_otorgamiento):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                      UPDATE creditos SET cliente=?, monto=?, tasa_interes=?, plazo=?, fecha_otorgamiento=?
                      WHERE id=?"""
                      , (cliente, monto, tasa_interes, plazo, fecha_otorgamiento, id))
        conn.commit()
    return cursor.rowcount > 0

def borrar(id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM creditos WHERE id=?", (id,))
        conn.commit()
    return cursor.rowcount>0