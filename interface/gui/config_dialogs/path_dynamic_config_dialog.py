# interface/gui/path_dynamic_config_dialog.py
import tkinter as tk
from tkinter import messagebox

class PathDynamicConfigDialog(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.title("Configurar caminho")
        self.transient(master)
        self.grab_set()
        self.controller = controller

        # Template
        tk.Label(self, text="Definição do caminho em que as guias serão salvas:").pack()
        self.textbox = tk.Text(self, width=80, height=4, padx=10)
        self.textbox.insert(tk.INSERT, self.controller.get_path())
        self.textbox.pack()

        # Lista de variáveis
        self.variaveis = {
            "Filial": "guia.filial",
            "Ano Periodo": "guia.periodo.year",
            "Mes Periodo": "guia.periodo.month",
            "Mes Vencimento": "guia.vencimento.month",
            "Ano Vencimento": "guia.vencimento.year",
            "Tipo Guia": "tipo_destino",
            "CNPJ": "guia.cnpj",
            "IE": "guia.ie",
            "UF": "guia.uf"
        }

        tk.Label(self, text="Variáveis disponíveis:").pack()
        frame_vars = tk.Frame(self)
        frame_vars.pack()

        for var in self.variaveis:
            tk.Button(frame_vars, text=var, command=lambda v=var: self.inserir_variavel(v))\
                .pack(side=tk.LEFT, padx=5, pady=5)

        tk.Button(self, text="Salvar", command=self.salvar_path).pack(pady=10)

    def salvar_path(self):
        defined_path = self.textbox.get("1.0", "end-1c").strip()
        if not defined_path:
            messagebox.showerror("Erro", "O caminho não pode ser vazio!")
            return

        confirmar = messagebox.askyesno(
            "Confirmação", f"Tem certeza que deseja salvar o caminho:\n{defined_path}?")
        if confirmar:
            self.controller.set_path(defined_path)
            messagebox.showinfo("Sucesso", "Caminho salvo com sucesso!")
            self.destroy()
        else:
            messagebox.showinfo("Cancelado", "Operação cancelada.")

    def inserir_variavel(self, var):
        self.textbox.insert(tk.INSERT, f"({var})")
