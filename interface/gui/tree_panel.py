# interface/gui/tree_panel.py

import tkinter as tk
from tkinter import ttk, messagebox
import locale
import uuid
from domain.entities.guia import Guia

class TreePanel(ttk.Frame):
    def __init__(self, parent, alert_func=None):
        super().__init__(parent)

        self.alert_func = alert_func or (lambda title, msg: messagebox.showwarning(title, msg))
        self.colunas = ("Filial", "UF", "Tipo", "Valor", "Status")
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

        # Dicionários para mapear item_id -> objeto Guia
        self._objetos_esquerda = {}
        self._objetos_direita = {}

        self.style = ttk.Style()
        self.style.configure("Treeview", rowheight=30)

        # Labels
        self.label_esquerda = ttk.Label(self, text="Dados disponíveis", font=("Arial", 11, "bold"))
        self.label_esquerda.grid(row=0, column=0, pady=(0, 5))

        self.tree_esquerda = self._criar_treeview()
        self.tree_esquerda.grid(row=1, column=0, padx=10)

        self.frame_botoes = ttk.Frame(self)
        self.frame_botoes.grid(row=1, column=1, padx=10)

        ttk.Button(self.frame_botoes, text="≫", command=self.mover_todos_para_direita).pack(pady=5)
        ttk.Button(self.frame_botoes, text="→", command=self.mover_para_direita).pack(pady=5)
        ttk.Button(self.frame_botoes, text="←", command=self.mover_para_esquerda).pack(pady=5)
        ttk.Button(self.frame_botoes, text="≪", command=self.mover_todos_para_esquerda).pack(pady=5)

        self.label_direita = ttk.Label(self, text="Dados selecionados", font=("Arial", 11, "bold"))
        self.label_direita.grid(row=0, column=2, pady=(0, 5))

        self.tree_direita = self._criar_treeview()
        self.tree_direita.grid(row=1, column=2, padx=10)

    # ------------------------
    # Criação da TreeView
    # ------------------------
    def _criar_treeview(self):
        tree = ttk.Treeview(self, columns=self.colunas, show="headings", height=7)
        tree.column("#0", width=60, anchor="center")
        tree.heading("#0", text="Status")
        for col in self.colunas:
            tree.heading(col, text=col)
            tree.column(col, width=55 if col in ("Filial","UF") else 105, anchor="center")
        return tree

    # ------------------------
    # Funções de atualização
    # ------------------------
    def atualizar_status(self, guia: Guia, status: str):
        iid = str(guia.id)
        if iid not in self._objetos_direita:
            return
        emoji = {"ok": "✅", "erro": "❌"}.get(status, "⏳")
        def _update():
            if self.tree_direita.exists(iid):
                self.tree_direita.set(iid, "Status", emoji)
        self.after(0, _update)

    def marcar_todos_em_andamento(self):
        for iid in self._objetos_direita.keys():
            if self.tree_direita.exists(iid):
                self.tree_direita.set(iid, "Status", "⏳")

    # ------------------------
    # Controle de dados
    # ------------------------
    def set_dados(self, lista_dados: list[Guia]):
        self.tree_esquerda.delete(*self.tree_esquerda.get_children())
        self._objetos_esquerda.clear()
        for d in lista_dados:
            valores = (d.filial, d.uf, d.tipo, self._atualizar_valor(d.valor))
            d.id = str(uuid.uuid4())
            item_id = self.tree_esquerda.insert("", tk.END, values=valores, iid=d.id)
            self._objetos_esquerda[item_id] = d

    def get_dados_direita(self) -> list[Guia]:
        return [obj for obj in self._objetos_direita.values()]

    def get_dados_esquerda(self) -> list[Guia]:
        return [obj for obj in self._objetos_esquerda.values()]

    def adicionar_guia(self, guia: Guia):
        valores = (guia.filial, guia.uf, guia.tipo, self._atualizar_valor(guia.valor))
        item_id = self.tree_esquerda.insert("", tk.END, values=valores, iid=guia.id)
        self._objetos_esquerda[item_id] = guia

    def deletar_guia(self, guia_id: str):
        if guia_id in self._objetos_esquerda:
            if self.tree_esquerda.exists(guia_id):
                self.tree_esquerda.delete(guia_id)
            del self._objetos_esquerda[guia_id]
            self._reordenar_tree(self.tree_esquerda, self._objetos_esquerda)
            return True
        return False

    # ------------------------
    # Funções de movimentação
    # ------------------------
    def mover_para_direita(self):
        selecao = self.tree_esquerda.selection()
        if len(selecao) == 0:
            messagebox.showwarning("Aviso", "Nenhuma guia selecionada.")
            return
        
        for item_id in selecao:


            next_item = self.tree_esquerda.next(item_id) or self.tree_esquerda.prev(item_id)

            # verifica se o item ainda existe
            guia: Guia = self._objetos_esquerda.pop(item_id, None)
            if guia is None:
                continue  # pula se já removido

            # remove do dicionário e da treeview esquerda
            self.tree_esquerda.delete(item_id)

            # adiciona na treeview direita
            valores = (guia.filial, guia.uf, guia.tipo, self._atualizar_valor(guia.valor), "-")  # status = loading
            self.tree_direita.insert("", tk.END, iid=guia.id, values=valores)
            self._objetos_direita[guia.id] = guia

            if next_item:
                self.tree_esquerda.selection_set(next_item)
                self.tree_esquerda.focus(next_item)

        self._reordenar_tree(self.tree_direita, self._objetos_direita)

    def mover_para_esquerda(self):
        selecao = self.tree_direita.selection()

        if len(selecao) == 0:
            messagebox.showwarning("Aviso", "Nenhuma guia selecionada.")
            return
        
        for item_id in selecao:

            next_item = self.tree_direita.next(item_id)
            if not next_item:
                next_item = self.tree_direita.prev(item_id)
            
            # verifica se o item ainda existe
            guia: Guia = self._objetos_direita.pop(item_id, None)
            if guia is None:
                continue  # pula se já removido

            # remove do dicionário e da treeview direita
            self.tree_direita.delete(item_id)

            # remove do dicionário e da treeview direita

            # adiciona na treeview esquerda
            valores = (guia.filial, guia.uf, guia.tipo, self._atualizar_valor(guia.valor))
            novo_id = self.tree_esquerda.insert("", tk.END, values=valores, iid=guia.id)
            self._objetos_esquerda[novo_id] = guia


            if next_item:
                self.tree_direita.selection_set(next_item)
                self.tree_direita.focus(next_item)

        self._reordenar_tree(self.tree_esquerda, self._objetos_esquerda)

    def mover_todos_para_direita(self):

        if len(self.tree_esquerda.get_children()) == 0:
            messagebox.showwarning("Aviso", "Nenhuma guia no quadro da esquerda.")
            return
        
        for item_id in self.tree_esquerda.get_children():

            obj = self._objetos_esquerda.get(item_id)
            if not obj:
                continue # pula se já removido

            # remove do dicionário e da treeview direita
            self._objetos_esquerda.pop(item_id)
            self.tree_esquerda.delete(item_id)

            valores = (obj.filial, obj.uf, obj.tipo, self._atualizar_valor(obj.valor), "-")
            novo_id = self.tree_direita.insert("", tk.END, values=valores)
            self._objetos_direita[novo_id] = obj
        self._reordenar_tree(self.tree_direita, self._objetos_direita)

    def mover_todos_para_esquerda(self):

        if len(self.tree_direita.get_children()) == 0:
            messagebox.showwarning("Aviso", "Nenhuma guia no quadro da direita.")
            return
        
        for item_id in self.tree_direita.get_children():

            obj = self._objetos_direita.get(item_id)
            if not obj:
                continue # pula se já removido

            # remove do dicionário e da treeview direita
            self._objetos_direita.pop(item_id)
            self.tree_direita.delete(item_id)

            valores = (obj.filial, obj.uf, obj.tipo, self._atualizar_valor(obj.valor))
            novo_id = self.tree_esquerda.insert("", tk.END, values=valores)
            self._objetos_esquerda[novo_id] = obj
        self._reordenar_tree(self.tree_esquerda, self._objetos_esquerda)

    # ------------------------
    # Auxiliares
    # ------------------------
    def _atualizar_valor(self, value):
        return locale.currency(float(value), grouping=True)

    def _reordenar_tree(self, tree, objetos_dict):
        items = [(item_id, objetos_dict[item_id]) for item_id in tree.get_children()]
        items_ordenados = sorted(items, key=lambda t: (int(t[1].filial), t[1].uf))
        tree.delete(*tree.get_children())
        for _, obj in items_ordenados:
            valores = (obj.filial, obj.uf, obj.tipo, self._atualizar_valor(obj.valor), "-")
            novo_id = tree.insert("", tk.END, iid=obj.id, values=valores)
            objetos_dict[novo_id] = obj
