from domain.entities.site import Site
from domain.repositories.i_site_repository import ISiteRepository
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
        
    def delete(self, uf: str) -> bool:
        """Deleta guia e seus detalhes."""
        try:
            with self.db.connect() as conn:
                conn.execute("DELETE FROM Sites WHERE Uf = ?", (uf,))
            return True
        except Exception as e:
            print(f"Erro ao deletar site: {e}")
            return False
        
    def update(self, site: Site) -> bool:
        """Atualiza um guia existente."""
        try:
            with self.db.connect() as conn:
                cursor = conn.execute(
                    """
                    UPDATE Sites
                    SET Icms = ?, Difal = ?, St = ?, Icau = ?, Fot = ?, Ican = ?
                    WHERE Uf = ?
                    """,
                    (
                        site.icms,
                        site.difal,
                        site.st,
                        site.icau,
                        site.fot,
                        site.ican,
                        site.uf
                    )
                )
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar site: {e}")
            return False
        
    def get_by_id(self, id: int) -> Optional[Site]:
        """Retorna um Guia completo pelo ID."""
        try:
            with self.db.connect() as conn:
                row = conn.execute("SELECT * FROM Sites WHERE Id = ?", (id,)).fetchone()
                if not row:
                    return None

                return Site(
                    id=row[0],
                    uf=row[1],
                    icms=row[2],
                    difal=row[3],
                    st=row[4],
                    icau=row[5],
                    fot=row[6],
                    ican=row[7]
                    )
        except Exception as e:
            print(f"Erro ao buscar site: {e}")
            return None
    
    def get_by_uf(self, uf: str) -> Optional[Site]:
        """Retorna um Guia completo pelo ID."""
        try:
            with self.db.connect() as conn:
                row = conn.execute("SELECT * FROM Sites WHERE Uf = ?", (uf,)).fetchone()
                if not row:
                    return None

                return Site(
                    id=row[0],
                    uf=row[1],
                    icms=row[2],
                    difal=row[3],
                    st=row[4],
                    icau=row[5],
                    fot=row[6],
                    ican=row[7]
                )
        except Exception as e:
            print(f"Erro ao buscar site: {e}")
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
                            id=row[0],
                            uf=row[1],
                            icms=row[2],
                            difal=row[3],
                            st=row[4],
                            icau=row[5],
                            fot=row[6],
                            ican=row[7]
                        )
                    )
            return sites
        except Exception as e:
            print(f"Erro ao listar sites: {e}")
            return []
