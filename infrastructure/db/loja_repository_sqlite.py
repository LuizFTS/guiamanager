from domain.entities.loja import Loja
from domain.repositories.i_loja_repository import ILojaRepository
from infrastructure.db.database import Database
from typing import List, Optional

class LojaRepositorySQLite(ILojaRepository):
    def __init__(self, db: Database):
        self.db = db

    def save(self, loja: Loja, site_id: int) -> bool:
        try:
            with self.db.connect() as conn:

                conn.execute(
                    """
                    INSERT INTO Lojas 
                        (Filial, Uf, Cnpj, Ie, Site_Id)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        loja.filial,
                        loja.uf,
                        loja.cnpj,
                        loja.ie,
                        site_id
                    )
                )

            return True
        except Exception as e:
            print(f"Erro ao salvar Loja completo: {e}")
            return False
        
    def delete(self, filial: str) -> bool:
        """Deleta Loja e seus detalhes."""
        try:
            with self.db.connect() as conn:
                conn.execute("DELETE FROM Lojas WHERE Filial = ?", (filial,))
            return True
        except Exception as e:
            print(f"Erro ao deletar guia: {e}")
            return False
        
    def update(self, loja: Loja, site_id: int) -> bool:
        """Atualiza um guia existente."""
        try:
            with self.db.connect() as conn:
                cursor = conn.execute(
                    """
                    UPDATE Lojas
                    SET Uf = ?, Cnpj = ?, Ie = ?, Site_Id = ?
                    WHERE Filial = ?
                    """,
                    (
                        loja.uf,
                        loja.cnpj,
                        loja.ie,
                        site_id,
                        loja.filial
                    )
                )
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar Loja: {e}")
            return False
        
    def get_by_id(self, id: int) -> Optional[Loja]:
        """Retorna um Lojas completo pelo ID."""
        try:
            with self.db.connect() as conn:
                row = conn.execute("SELECT * FROM Lojas WHERE Id = ?", (id,)).fetchone()
                if not row:
                    return None

                return Loja(
                    id=row[0],
                    filial=row[1],
                    uf=row[2],  # preencher com dados de Loja se necessário
                    cnpj=row[3],
                    ie=row[4],
                    site=""
                )
        except Exception as e:
            print(f"Erro ao buscar loja: {e}")
            return None
        
    def get_by_filial(self, filial: str) -> Optional[Loja]:
        """Retorna um loja completo pelo ID."""
        try:
            with self.db.connect() as conn:
                row = conn.execute("SELECT * FROM Lojas WHERE Filial = ?", (filial,)).fetchone()
                if not row:
                    return None

                return Loja(
                    id=row[0],
                    filial=row[1],
                    uf=row[2],  # preencher com dados de Loja se necessário
                    cnpj=row[3],
                    ie=row[4],
                    site=""
                )
        except Exception as e:
            print(f"Erro ao buscar loja: {e}")
            return None

    def list_all(self) -> List[Loja]:
        """Lista todos os Lojas."""
        try:
            with self.db.connect() as conn:
                rows = conn.execute("SELECT * FROM Lojas").fetchall()
                lojas = []
                for row in rows:
                    lojas.append(
                        Loja(
                            id=row[0],
                            filial=row[1],
                            uf=row[2],  # preencher com dados de Loja se necessário
                            cnpj=row[3],
                            ie=row[4],
                            site=""
                        )
                    )
            return lojas
        except Exception as e:
            print(f"Erro ao listar lojas: {e}")
            return []
