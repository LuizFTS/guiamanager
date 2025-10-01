# interface/gui/loja_config_dialog.py

import tkinter as tk
from tkinter import ttk, messagebox
from interface.controllers.loja_controller import LojaController
from domain.entities.loja import Loja

class LojaConfigDialog(tk.Toplevel):
    def __init__(self, master, controller: LojaController):
        super().__init__(master)
        self.title("Parâmetros - Filiais cadastradas")
        self.transient(master)
        self.grab_set()
        self.controller = controller

        self.colunas = ("Número", "UF", "CNPJ", "IE")

        self.criar_treeview()
        self.criar_botoes()
        self.atualizar_treeview()

    # --------------------
    # UI
    # --------------------
    def criar_treeview(self):
        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(frame, columns=self.colunas, show="headings")
        for col in self.colunas:
            self.tree.heading(col, text=col)
            width = 80 if col in ("Número", "UF") else 150
            self.tree.column(col, width=width, anchor="center")

        scroll_y = tk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        scroll_x = tk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=scroll_y.set, xscroll=scroll_x.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

    def criar_botoes(self):
        frame = tk.Frame(self)
        frame.pack(pady=5)
        tk.Button(frame, text="Adicionar Filial", command=self.adicionar, width=15).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Editar Filial", command=self.editar, width=15).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Excluir Filial", command=self.excluir, width=15).grid(row=0, column=2, padx=5)

    # --------------------
    # CRUD via controller
    # --------------------
    def atualizar_treeview(self):
        self.tree.delete(*self.tree.get_children())
        filiais = self.controller.get_all()

        # Mapeamento coluna -> atributo
        col_attr_map = {
            "Número": "filial",
            "UF": "uf",
            "CNPJ": "cnpj",
            "IE": "ie"
        }
        
        for f in sorted(filiais, key=lambda x: (int(x.filial), x.uf)):
            valores = [getattr(f, col_attr_map[col]) for col in self.colunas]
            self.tree.insert("", tk.END, values=valores)

    def get_filial_selecionada(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma filial!")
            return None
        return self.tree.item(selecionado[0], "values")[0]

    def adicionar(self):
        self.abrir_formulario()

    def editar(self):
        numero = self.get_filial_selecionada()
        if numero:
            self.abrir_formulario(numero_existente=numero)

    def excluir(self):
        numero = self.get_filial_selecionada()
        print(numero)
        if not numero:
            return
        if messagebox.askyesno("Confirmação", f"Deseja realmente excluir a filial {numero}?"):
            self.controller.delete(numero)
            self.atualizar_treeview()

    # --------------------
    # Formulário popup
    # --------------------
    def abrir_formulario(self, numero_existente=None):
        popup = tk.Toplevel(self)
        popup.title("Filial")

        popup.focus_force()
        self.entradas = {}
        for i, campo in enumerate(self.colunas):
            tk.Label(popup, text=campo, anchor="w").grid(row=i, column=0, padx=5, pady=5, sticky="w")
            self.entrada = tk.Entry(popup, width=30)
            self.entrada.grid(row=i, column=1, padx=5, pady=5)
            self.entradas[campo] = self.entrada

            if i == 0:
                primeiro_entry = self.entrada
        
        if primeiro_entry:
            primeiro_entry.focus_set()

        if numero_existente:
            filial = self.controller.find(numero_existente)
            self.entradas["Número"].insert(0, numero_existente)
            self.entradas["Número"].config(state="disabled")

            for campo, entry in self.entradas.items():
                atributo = 'filial' if campo == "Número" else campo.lower()

                if hasattr(filial, atributo):
                    entry.insert(0, getattr(filial, atributo))


        tk.Button(popup, text="Salvar",
                  command=lambda: self.salvar_formulario(self.entradas, popup, numero_existente),
                  width=15).grid(row=len(self.colunas), columnspan=2, pady=10)
        
        primeiro_entry.focus_set()

    def _clear_camps(self):
        for campo, entry in self.entradas.items():
            entry.delete(0, tk.END)
        self.entradas["Número"].focus_set()


    def salvar_formulario(self, entradas, popup, numero_existente):
        dados = {campo: entradas[campo].get().strip() for campo in self.colunas}
        dados["UF"] = dados["UF"].upper()
        dados["Número"] = dados["Número"].zfill(2)

        # Validação
        if any(not v for v in dados.values()):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return

        if not numero_existente and self.controller.find(dados["Número"]):
            messagebox.showerror("Erro", f"A filial {dados['Número']} já existe!")
            return

        
        dados_formatados = Loja(
            **{('filial' if k == 'Número' else k.lower()): v for k, v in dados.items()},
            site=""
        )
        

        if numero_existente:
            self.controller.atualizar(dados_formatados)
        else:
            self.controller.add(dados_formatados)

        self.atualizar_treeview()
        self._clear_camps()
        