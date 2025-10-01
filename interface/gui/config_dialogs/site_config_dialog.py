# interface/gui/site_config_dialog.py

import tkinter as tk
from tkinter import ttk, messagebox
from interface.controllers.site_controller import SiteController
from domain.entities.site import Site

class SiteConfigDialog(tk.Toplevel):
    def __init__(self, master, controller: SiteController):
        super().__init__(master)
        self.title("Parâmetros - Sites por UF e tipo de imposto")
        self.transient(master)
        self.grab_set()
        self.controller = controller

        self.colunas = ("UF", "ICMS", "DIFAL", "ST", "ICAU", "FOT", "ICAN")
        self.criar_treeview()
        self.criar_botoes()
        self.atualizar_treeview()

    def criar_treeview(self):
        self.frame_tree = tk.Frame(self)
        self.frame_tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(self.frame_tree, columns=self.colunas, show="headings")
        for col in self.colunas:
            self.tree.heading(col, text=col)
            width = 50 if col == "UF" else 150
            self.tree.column(col, width=width, anchor="center")

        scroll_y = tk.Scrollbar(self.frame_tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scroll_y.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        self.frame_tree.rowconfigure(0, weight=1)
        self.frame_tree.columnconfigure(0, weight=1)

    def criar_botoes(self):
        frame = tk.Frame(self)
        frame.pack(pady=5)
        tk.Button(frame, text="Adicionar UF", command=self.adicionar, width=15).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Editar UF", command=self.editar, width=15).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Excluir UF", command=self.excluir, width=15).grid(row=0, column=2, padx=5)

    def atualizar_treeview(self):
        self.tree.delete(*self.tree.get_children())
        sites = self.controller.get_all()  # controller fornece os dados
        for site in sorted(sites, key=lambda s: s.uf):
            self.tree.insert("",
                              tk.END,
                                values=(site.uf, *[getattr(site, col.lower()) for col in self.colunas[1:]])
                            )
            
    def get_uf_selecionada(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma UF!")
            return None
        return self.tree.item(selecionado[0], "values")[0]

    def adicionar(self):
        self.abrir_formulario()

    def editar(self):
        uf = self.get_uf_selecionada()
        if uf:
            self.abrir_formulario(uf_existente=uf)

    def excluir(self):
        uf = self.get_uf_selecionada()
        if not uf:
            return
        if messagebox.askyesno("Confirmação", f"Deseja realmente excluir a UF {uf}?"):
            self.controller.delete(uf)
            self.atualizar_treeview()

    def abrir_formulario(self, uf_existente=None):
        popup = tk.Toplevel(self)
        popup.title("Cadastro de UF")
        self.entradas = {}
        for i, campo in enumerate(self.colunas):
            tk.Label(popup, text=campo, anchor="w").grid(row=i, column=0, padx=5, pady=5, sticky="w")
            self.entrada = tk.Entry(popup, width=40)
            self.entrada.grid(row=i, column=1, padx=5, pady=5)
            self.entradas[campo] = self.entrada

            if i == 0:
                self.entradas[campo].focus_set()

        if uf_existente:
            site = self.controller.find(uf_existente)
            self.entradas["UF"].insert(0, uf_existente)
            self.entradas["UF"].config(state="disabled")

            # Preencher apenas os Entry's
            for campo, entry in self.entradas.items():
                atributo = campo.lower()
                if hasattr(site, atributo):
                    entry.insert(0, getattr(site, atributo))

        tk.Button(popup, text="Salvar",
                command=lambda: self.salvar_formulario(self.entradas, popup, uf_existente),
                width=15).grid(row=len(self.colunas), columnspan=2, pady=10)

    def _clear_camps(self):
        for campo, entry in self.entradas.items():
            entry.delete(0, tk.END)
        self.entradas["UF"].focus_set()

    def salvar_formulario(self, entradas, popup, uf_existente):
        uf = entradas["UF"].get().strip().upper()
        if not uf:
            messagebox.showerror("Erro", "UF não pode ser vazia!")
            return

        dados_site = {
            campo.lower(): entradas[campo].get() 
            for campo in self.colunas[1:]
            }
        
        data = Site(
            uf,
            **dados_site
        )
        print(data)
        if uf_existente:
            self.controller.atualizar(data)
        else:
            self.controller.add(data)

        self.atualizar_treeview()
        self._clear_camps()
