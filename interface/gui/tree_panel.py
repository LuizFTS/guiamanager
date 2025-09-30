# interface/gui/tree_panel.py

import tkinter as tk
from tkinter import ttk, messagebox
import locale
from domain.entities.guia import Guia
from interface.controllers.guia_controller import GuiaController

class TreePanel(ttk.Frame):
    def __init__(self, parent, guia_controller: GuiaController, alert_func=None):
        super().__init__(parent)
        
        self.guia_controller = guia_controller

        self.alert_func = alert_func or (lambda title, msg: messagebox.showwarning(title, msg))
        self.colunas = ("Filial", "UF", "Tipo", "Valor", "Status")
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

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
        
        self._initialize()
        
    def _initialize(self):
        guias = self.guia_controller.get_all()
        
        if guias:
            for guia in guias:
                self.adicionar_guia(guia)
                
    def reload(self):
        if len(self.tree_esquerda.get_children()) > 0:

            for item in self.tree_esquerda.get_children():
                self.tree_esquerda.delete(item)

            self._initialize()
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
        iid = guia.id
        emoji = {"ok": "✅", "erro": "❌"}.get(status, "⏳")

        def _update():
            if self.tree_direita.exists(iid):
                self.tree_direita.set(iid, "Status", emoji)
        self.after(0, _update)

    def marcar_todos_em_andamento(self):
        for iid in self.tree_direita.get_children():
            self.tree_direita.set(iid, "Status", "⏳")

    # ------------------------
    # Controle de dados
    # ------------------------
    def set_dados(self, lista_dados: list[int]):
        guias = {guia.id: guia for guia in self.guia_controller.get_all()}  # cria lookup por ID
        for id in lista_dados:
            guia = guias.get(id)
            if guia:
                valores = (guia.filial, guia.uf, guia.tipo, self._atualizar_valor(guia.valor))
                self.tree_esquerda.insert("", tk.END, values=valores, iid=guia.id)
                        

    def get_dados_direita(self) -> list[Guia]:
        dados = self.tree_direita.get_children()
        guias = []
        for d in dados:
            guia = self.guia_controller.find_by_id(d)
            if guia:
                guias.append(guia)
        return guias

    def get_dados_esquerda(self) -> list[Guia]:
        dados = self.tree_esquerda.get_children()
        guias = []
        for d in dados:
            guia = self.guia_controller.find_by_id(d)
            if guia:
                guias.append(guia)
        return guias

    def adicionar_guia(self, guia: Guia):
        valores = (guia.filial, guia.uf, guia.tipo, self._atualizar_valor(guia.valor))
        self.tree_esquerda.insert("", tk.END, values=valores, iid=guia.id)

    def deletar_guia(self, guia_id: str):
        items = list(self.tree_esquerda.get_children())
        if guia_id not in items:
            return False

        index = items.index(guia_id)

        # deleta o item
        self.tree_esquerda.delete(guia_id)

        # reordena a tree antes de definir o foco
        self._reordenar_tree(self.tree_esquerda)

        # obtém os itens atualizados
        items_atualizados = list(self.tree_esquerda.get_children())

        # escolhe próximo item ou anterior
        next_item = None
        if index < len(items_atualizados):
            next_item = items_atualizados[index]  # próximo na nova ordem
        elif index > 0:
            next_item = items_atualizados[index - 1]

        # foca no item escolhido
        if next_item:
            self.tree_esquerda.selection_set(next_item)
            self.tree_esquerda.focus(next_item)

        return True





    def deletar_todas_as_guias(self):
        guias = self.tree_esquerda.get_children()
        for g in guias:
            self.tree_esquerda.delete(g)
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
            guia = self.guia_controller.find_by_id(item_id)
            if guia is None:
                continue

            # remove do dicionário e da treeview esquerda
            self.tree_esquerda.delete(item_id)

            # adiciona na treeview direita
            valores = (
                guia.filial, 
                guia.uf, 
                guia.tipo, 
                self._atualizar_valor(guia.valor), 
                "-"
                )  # status = loading
            self.tree_direita.insert("", tk.END, iid=guia.id, values=valores)
            #self._objetos_direita[guia.id] = guia

            if next_item:
                self.tree_esquerda.selection_set(next_item)
                self.tree_esquerda.focus(next_item)

        self._reordenar_tree(self.tree_direita)

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
            guia = self.guia_controller.find_by_id(item_id)
            if guia is None:
                continue  # pula se já removido

            # remove do dicionário e da treeview direita
            self.tree_direita.delete(item_id)

            # remove do dicionário e da treeview direita

            # adiciona na treeview esquerda
            valores = (
                guia.filial, 
                guia.uf, 
                guia.tipo, 
                self._atualizar_valor(guia.valor)
                )
            
            self.tree_esquerda.insert("", tk.END, values=valores, iid=guia.id)
            #self._objetos_esquerda[novo_id] = guia


            if next_item:
                self.tree_direita.selection_set(next_item)
                self.tree_direita.focus(next_item)

        self._reordenar_tree(self.tree_esquerda)

    def mover_todos_para_direita(self):

        if len(self.tree_esquerda.get_children()) == 0:
            messagebox.showwarning("Aviso", "Nenhuma guia no quadro da esquerda.")
            return
        
        for item_id in self.tree_esquerda.get_children():

            guia = self.guia_controller.find_by_id(item_id)
            if not guia:
                continue # pula se já removido

            # remove da treeview direita
            self.tree_esquerda.delete(item_id)

            valores = (guia.filial, guia.uf, guia.tipo, self._atualizar_valor(guia.valor), "-")
            self.tree_direita.insert("", tk.END, values=valores, iid=guia.id)
        self._reordenar_tree(self.tree_direita)

    def mover_todos_para_esquerda(self):

        if len(self.tree_direita.get_children()) == 0:
            messagebox.showwarning("Aviso", "Nenhuma guia no quadro da direita.")
            return
        
        for item_id in self.tree_direita.get_children():

            guia = self.guia_controller.find_by_id(item_id)
            if not guia:
                continue # pula se já removido

            # remove da treeview direita
            self.tree_direita.delete(item_id)

            valores = (guia.filial, guia.uf, guia.tipo, self._atualizar_valor(guia.valor))
            self.tree_esquerda.insert("", tk.END, values=valores, iid=guia.id)
        self._reordenar_tree(self.tree_esquerda)

    # ------------------------
    # Auxiliares
    # ------------------------
    def _atualizar_valor(self, value):
        return locale.currency(float(value), grouping=True)

    def _reordenar_tree(self, tree):
        item_ids = tree.get_children()
        objetos = []
        for item_id in item_ids:
            obj = self.guia_controller.find_by_id(item_id)
            if obj:
                objetos.append((item_id, obj))

        objetos_ordenados = sorted(
            objetos,
            key=lambda t: (int(t[1].filial), t[1].uf)
        )

        tree.delete(*item_ids)

        # 5️⃣ Re-inserir os itens já ordenados
        for _, obj in objetos_ordenados:
            valores = (
                obj.filial,
                obj.uf,
                obj.tipo,
                self._atualizar_valor(obj.valor),
                "-"
            )
            tree.insert("", tk.END, iid=obj.id, values=valores)
