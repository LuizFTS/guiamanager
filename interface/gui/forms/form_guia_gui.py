# interface/gui/form_guia_gui.py

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from domain.entities.guia import Guia
from interface.controllers.guia_controller import GuiaController

class FormGuiaGUI(tk.Toplevel):
    def __init__(self, master=None, tree_panel=None, controller: GuiaController =None, edit=False):
        super().__init__(master)
        self.tree = tree_panel
        self.controller = controller  # UseCase/controller injetado
        self.edit = edit
        self.title("Adicionar Guia")

        # Campos do formulário
        self.filial = ttk.Combobox(self, state="readonly", width=5)
        self.periodo = ttk.Entry(self, width=10)
        self.vencimento = ttk.Entry(self, width=10)
        self.tipo = ttk.Combobox(self, state="readonly", width=5)
        self.valor = ttk.Entry(self, width=10)
        self.fcp = ttk.Entry(self, width=10)
        self.notas = ttk.Entry(self, width=20)
        self.fretes = ttk.Entry(self, width=20)

        self._setup_ui()

    def _setup_ui(self):
        # Layout simplificado; labels e inputs
        tk.Label(self, text="Filial:").grid(row=0, column=0, padx=10, pady=5)
        self.filial.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self, text="Período:").grid(row=1, column=0, padx=10, pady=5)
        self.periodo.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self, text="Vencimento:").grid(row=2, column=0, padx=10, pady=5)
        self.vencimento.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self, text="Tipo:").grid(row=3, column=0, padx=10, pady=5)
        self.tipo.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self, text="Valor:").grid(row=4, column=0, padx=10, pady=5)
        self.valor.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(self, text="FCP:").grid(row=5, column=0, padx=10, pady=5)
        self.fcp.grid(row=5, column=1, padx=10, pady=5)

        tk.Button(self, text="Salvar", command=self.salvar_formulario).grid(row=6, columnspan=2, pady=10)

    def salvar_formulario(self):
        # Validação mínima
        if not self.periodo.get() or not self.vencimento.get() or not self.valor.get():
            messagebox.showerror("Erro", "Campos obrigatórios!")
            return

        # Criação do objeto Guia (deve ser via controller/use case)
        guia_data = {
            "filial": self.filial.get(),
            "periodo": datetime.strptime("01/" + self.periodo.get(), "%d/%m/%Y"),
            "vencimento": datetime.strptime(self.vencimento.get(), "%d/%m/%Y"),
            "tipo": self.tipo.get(),
            "valor": self.valor.get().replace(",", "."),
            "fcp": self.fcp.get().replace(",", "."),
            "notas": self.notas.get() if self.tipo.get() in ("DIFAL", "ST", "ICAN") else [],  # Aqui você pode incluir lógica de parseamento
            "fretes": self.fretes.get() if self.tipo.get() in ("DIFAL", "ST") else []
        }

        guia = Guia(
            **guia_data
        )

        self.controller.gerar_guia(guia)
        self.controller.
        self.tree.adicionar_guia(guia)
        self.destroy()
