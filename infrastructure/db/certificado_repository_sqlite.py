from domain.entities.site import Site
from domain.entities.certificado import Certificado
from domain.repositories.i_certificado_repository import ICertificadoRepository
from infrastructure.db.database import Database
from typing import List, Optional

class CertificadoRepositorySQLite(ICertificadoRepository):
    def __init__(self, db: Database):
        self.db = db

    def save(self, certificado: Certificado) -> bool:
        try:
            with self.db.connect() as conn:

                conn.execute(
                    """
                    INSERT INTO Certificados 
                        (loja_id, cert_path, key_path, is_active, updated_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        certificado.loja_id,
                        certificado.cert_path,
                        certificado.key_path,
                        1 if certificado.is_active else 0,
                        certificado.updated_at
                    )
                )

            return True
        except Exception as e:
            print(f"Erro ao salvar certificado: {e}")
            return False

    def delete(self, loja_id: int) -> bool:
        """Deleta certificado e seus detalhes."""
        try:
            with self.db.connect() as conn:
                conn.execute("DELETE FROM Certificados WHERE loja_id = ?", (loja_id,))
            return True
        except Exception as e:
            print(f"Erro ao deletar certificado: {e}")
            return False

    def update(self, certificado: Certificado) -> bool:
        """Atualiza um certificado existente."""
        try:
            with self.db.connect() as conn:
                cursor = conn.execute(
                    """
                    UPDATE Certificados
                    SET cert_path = ?, key_path = ?, is_active = ?, updated_at = ?
                    WHERE loja_id = ?
                    """,
                    (
                        certificado.cert_path,
                        certificado.key_path,
                        certificado.is_active,
                        certificado.updated_at,
                        certificado.loja_id
                    )
                )
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar o certificado: {e}")
            return False

    def get_by_id(self, id: int) -> Optional[Certificado]:
        """Retorna um certificado completo pelo ID."""
        try:
            with self.db.connect() as conn:
                row = conn.execute("SELECT * FROM Certificados WHERE Id = ?", (id,)).fetchone()
                if not row:
                    return None

                return Certificado(
                    id=row[0],
                    loja_id=[1],
                    cert_path=row[2],
                    key_path=row[3],
                    is_active=row[4],
                    updated_at=row[6]
                    )
        except Exception as e:
            print(f"Erro ao buscar certificado: {e}")
            return None

    def get_by_loja_id(self, loja_id: int) -> Optional[Certificado]:
        """Retorna um Guia completo pelo ID."""
        try:
            with self.db.connect() as conn:
                row = conn.execute("SELECT * FROM Certificados WHERE loja_id = ?", (loja_id,)).fetchone()
                if not row:
                    return None

                return Certificado(
                    id=row[0],
                    loja_id=[1],
                    cert_path=row[2],
                    key_path=row[3],
                    is_active=row[4],
                    updated_at=row[6]
                    )
        except Exception as e:
            print(f"Erro ao buscar certificado: {e}")
            return None

    def list_all(self) -> List[Certificado]:
        """Lista todos os Guias."""
        try:
            with self.db.connect() as conn:
                rows = conn.execute("SELECT * FROM Certificados").fetchall()
                certificados = []
                for row in rows:
                    certificados.append(
                        Certificado(
                            id=row[0],
                            loja_id=[1],
                            cert_path=row[2],
                            key_path=row[3],
                            is_active=row[4],
                            updated_at=row[6]
                        )
                    )
            return certificados
        except Exception as e:
            print(f"Erro ao listar certificados: {e}")
            return []