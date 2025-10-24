from domain.entities.guia import Guia
from domain.repositories.i_guia_repository import IGuiaRepository
from infrastructure.db.database import Database
from typing import List, Optional
from datetime import datetime

class GuiaRepositorySQLite(IGuiaRepository):
    def __init__(self, db: Database):
        self.db = db

    def save(self, guia: Guia, loja_id: int, site_id: int) -> bool:
        try:
            with self.db.connect() as conn:

                cursor = conn.execute(
                    """
                    INSERT INTO Guias 
                        (Loja_Id, Site_Id, Periodo, Vencimento, Tipo, Valor, Fcp)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        loja_id,
                        site_id,
                        guia.periodo.isoformat(),
                        guia.vencimento.isoformat(),
                        guia.tipo,
                        guia.valor,
                        guia.fcp
                    )
                )
                guia_id = cursor.lastrowid

                # Inserir notas
                for nota in guia.notas:
                    conn.execute(
                        "INSERT INTO NotasGuia (Numero, Guia_Id) VALUES (?, ?)",
                        (nota, guia_id)
                    )

                # Inserir fretes
                for frete in guia.fretes:
                    conn.execute(
                        "INSERT INTO FretesGuia (Numero, Guia_Id) VALUES (?, ?)",
                        (frete, guia_id)
                    )

            return guia_id
        except Exception as e:
            print(f"Erro ao salvar guia completo: {e}")
            return False
        
    def delete(self, guia_id: int) -> bool:
        """Deleta guia e seus detalhes."""
        try:
            with self.db.connect() as conn:
                conn.execute("DELETE FROM NotasGuia WHERE Guia_Id = ?", (guia_id,))
                conn.execute("DELETE FROM FretesGuia WHERE Guia_Id = ?", (guia_id,))
                cursor = conn.execute("DELETE FROM Guias WHERE Id = ?", (guia_id,))
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao deletar guia: {e}")
            return False
        
    def update(self, guia: Guia, loja_id: int, site_id: int) -> bool:
        """Atualiza um guia existente."""
        try:
            with self.db.connect() as conn:
                cursor = conn.execute(
                    """
                    UPDATE Guias
                    SET Loja_Id = ?, Site_Id = ?, Periodo = ?, Vencimento = ?,
                        Tipo = ?, Valor = ?, Fcp = ?
                    WHERE Id = ?
                    """,
                    (
                        loja_id,
                        site_id,
                        guia.periodo.isoformat(),
                        guia.vencimento.isoformat(),
                        guia.tipo,
                        guia.valor,
                        guia.fcp,
                        guia.id
                    )
                )

            return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar guia: {e}")
            return False
        
    def get_by_id(self, guia_id: int) -> Optional[Guia]:
        """Retorna um Guia completo pelo ID."""
        try:
            with self.db.connect() as conn:
                row = conn.execute("SELECT * FROM Guias WHERE Id = ?", (guia_id,)).fetchone()
                if not row:
                    return None

                notas = [r[0] for r in conn.execute("SELECT Numero FROM NotasGuia WHERE Guia_Id = ?", (guia_id,))]
                fretes = [r[0] for r in conn.execute("SELECT Numero FROM FretesGuia WHERE Guia_Id = ?", (guia_id,))]

                return Guia(
                    id=row[0],
                    filial="",  # preencher com dados de Loja se necessário
                    loja_id=row[1],
                    site_id=row[2],
                    cnpj="",
                    ie="",
                    uf="",
                    periodo=datetime.fromisoformat(row[3]),
                    vencimento=datetime.fromisoformat(row[4]),
                    tipo=row[5],
                    valor=row[6],
                    fcp=row[7],
                    site="",  # preencher com dados de Site se necessário
                    notas=notas,
                    fretes=fretes
                )
        except Exception as e:
            print(f"Erro ao buscar guia: {e}")
            return None
        
    def get_by_loja_id_and_tipo(self, loja_id: int, tipo: str ) -> Optional[Guia]:
        """Retorna um Guia completo pelo ID."""
        try:
            with self.db.connect() as conn:
                row = conn.execute("SELECT * FROM Guias WHERE Loja_Id = ? AND Tipo = ?", (loja_id, tipo)).fetchone()
                if not row:
                    return None

                notas = [r[0] for r in conn.execute("SELECT Numero FROM NotasGuia WHERE Guia_Id = ?", (row[0],))]
                fretes = [r[0] for r in conn.execute("SELECT Numero FROM FretesGuia WHERE Guia_Id = ?", (row[0],))]

                return Guia(
                    id=row[0],
                    loja_id=row[1],
                    site_id=row[2],
                    filial="",  # preencher com dados de Loja se necessário
                    cnpj="",
                    ie="",
                    uf="",
                    periodo=row[3],
                    vencimento=row[4],
                    tipo=row[5],
                    valor=row[6],
                    fcp=row[7],
                    site="",  # preencher com dados de Site se necessário
                    notas=notas,
                    fretes=fretes
                )
        except Exception as e:
            print(f"Erro ao buscar guia: {e}")
            return None

    def list_all(self) -> List[Guia]:
        """Lista todos os Guias."""
        try:
            with self.db.connect() as conn:
                rows = conn.execute("SELECT * FROM Guias").fetchall()
                guias = []
                for row in rows:
                    notas = [r[0] for r in conn.execute("SELECT Numero FROM NotasGuia WHERE Guia_Id = ?", (row[0],))]
                    fretes = [r[0] for r in conn.execute("SELECT Numero FROM FretesGuia WHERE Guia_Id = ?", (row[0],))]
                    guias.append(
                        Guia(
                            id=row[0],
                            loja_id=row[1],
                            site_id=row[2],
                            filial="",
                            cnpj="",
                            ie="",
                            uf="",
                            periodo=row[3],
                            vencimento=row[4],
                            tipo=row[5],
                            valor=row[6],
                            fcp=row[7],
                            site="",
                            notas=notas,
                            fretes=fretes
                        )
                    )
            return guias
        except Exception as e:
            print(f"Erro ao listar guias: {e}")
            return []
