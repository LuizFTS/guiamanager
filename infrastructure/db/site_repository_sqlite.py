from domain.entities.site import Site
from domain.repositories.site_repository import ISiteRepository
from infrastructure.db.database import Database
from typing import List, Optional

class SiteRepositorySQLite(ISiteRepository):
    def __init__(self, db: Database):
        self.db = db

    def save(self, site: Site) -> bool:
        try:
            with self.db.connect() as conn:

                conn.execute(
                    """
                    INSERT INTO Sites 
                        (Uf, Icms, Difal, St, Icau, Fot, Ican)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        site.uf,
                        site.icms,
                        site.difal,
                        site.st,
                        site.icau,
                        site.fot,
                        site.ican,
                    )
                )

            return True
        except Exception as e:
            print(f"Erro ao salvar guia completo: {e}")
            return False
        
    def delete(self, id: int) -> bool:
        """Deleta guia e seus detalhes."""
        try:
            with self.db.connect() as conn:
                conn.execute("DELETE FROM Sites WHERE Id = ?", (id,))
            return True
        except Exception as e:
            print(f"Erro ao deletar guia: {e}")
            return False
        
    def update(self, site: Site) -> bool:
        """Atualiza um guia existente."""
        try:
            with self.db.connect() as conn:
                cursor = conn.execute(
                    """
                    UPDATE Sites
                    SET Icms = ?, Difal = ?, St = ?, Icau = ?, Fot = ?, Ican = ?
                    WHERE Id = ?
                    """,
                    (
                        site.icms,
                        site.difal,
                        site.st,
                        site.icau,
                        site.fot,
                        site.ican,
                        site.id
                    )
                )
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar guia: {e}")
            return False
        
    def get_by_id(self, id: int) -> Optional[Site]:
        """Retorna um Guia completo pelo ID."""
        try:
            with self.db.connect() as conn:
                row = conn.execute("SELECT * FROM Guias WHERE Id = ?", (id,)).fetchone()
                if not row:
                    return None

                return Site(
                    id=row["Id"],
                    icms=row["Icms"],
                    difal=row["Difal"],
                    st=row["St"],
                    icau=row["Icau"],
                    fot=row["Fot"],
                    ican=row["Ican"]
                )
        except Exception as e:
            print(f"Erro ao buscar guia: {e}")
            return None

    def list_all(self) -> List[Site]:
        """Lista todos os Guias."""
        try:
            with self.db.connect() as conn:
                rows = conn.execute("SELECT * FROM Sites").fetchall()
                sites = []
                for row in rows:
                    sites.append(
                        Site(
                            id=row["Id"],
                            icms=row["Icms"],
                            difal=row["Difal"],
                            st=row["St"],
                            icau=row["Icau"],
                            fot=row["Fot"],
                            ican=row["Ican"]
                        )
                    )
            return sites
        except Exception as e:
            print(f"Erro ao listar guias: {e}")
            return []
