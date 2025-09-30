# interface/gui/form_guia_gui.py

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from domain.entities.guia import Guia
from interface.controllers.guia_controller import GuiaController
from interface.controllers.loja_controller import LojaController
from interface.controllers.site_controller import SiteController

class FormGuiaGUI(tk.Toplevel):
    def __init__(self, master=None, tree_panel=None, site_controller: SiteController=None, loja_controller: LojaController = None, guia_controller: GuiaController = None, edit=False):
        super().__init__(master)
        self.tree = tree_panel
        self.loja_controller = loja_controller  # UseCase/controller injetado
        self.guia_controller = guia_controller  # UseCase/controller injetado
        self.site_controller = site_controller
        self.edit = edit
        self.title("Adicionar Guia")
        
        # Validade
        self.vcmd_periodo = (self.register(self._validar_periodo), "%P")
        self.vcmd_vencimento = (self.register(self._validar_vencimento), "%P")
        self.vcmd_valor = (self.register(self._validar_valor), "%P")
        self.vcmd_notas = (self.register(self._validar_notas), "%P")


        # StringVar()
        self.filiais_var = tk.StringVar()
        self.tipos_var = tk.StringVar()

        # Campos do formulário
        self.filial = ttk.Combobox(self, textvariable=self.filiais_var, state="readonly", width=5)
        self.periodo = ttk.Entry(self, width=10, validate="key", validatecommand=self.vcmd_periodo)
        self.vencimento = ttk.Entry(self, width=10, validate="key", validatecommand=self.vcmd_vencimento)
        self.tipo = ttk.Combobox(self, textvariable=self.tipos_var, state="readonly", width=5)
        self.valor = ttk.Entry(self, width=10, validate="key", validatecommand=self.vcmd_valor)
        self.fcp = ttk.Entry(self, width=10)
        self.notas = ttk.Entry(self, width=20, validate="key", validatecommand=self.vcmd_notas)
        self.fretes = ttk.Entry(self, width=20, validate="key", validatecommand=self.vcmd_notas)
        
        

        self._setup_ui()
        self._combobox_values()
        self._binding()
        self._editing()
        

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

        self.notas_label = tk.Label(self, text="Notas:")
        self.notas_label.grid(row=6, column=0, padx=10, pady=5)
        self.notas.grid(row=6, column=1, padx=10, pady=5)

        self.fretes_label = tk.Label(self, text="Fretes:")
        self.fretes_label.grid(row=7, column=0, padx=10, pady=5)
        
        self.fretes.grid(row=7, column=1, padx=10, pady=5)

        self.salvar_formulario_btn = tk.Button(self, text="Salvar", command=self.salvar_formulario)
        self.salvar_formulario_btn.grid(row=8, columnspan=2, pady=10)

    def _combobox_values(self):
        lojas = self.loja_controller.get_all()
        lojas = sorted([loja.filial for loja in lojas], key=int)
        
        self.filial['values'] = lojas
        
        self.tipo['values'] = sorted(["ICMS", "DIFAL", "ICAN", "ST", "ICAU", "FOT"])
        
    def _binding(self):
        self.periodo.bind("<FocusOut>", self._formatar_periodo)
        self.vencimento.bind("<FocusOut>", self._formatar_data)
        self.tipo.bind("<<ComboboxSelected>>", self._on_tipo_change)
        
        self.filial.current(0)
        self.filial.focus_set()
        self.tipo.current(0)
        
    def _formatar_data(self, event):
        texto = self.vencimento.get().strip()
        if len(texto) == 8 and texto.isdigit():
            data_formatada = f"{texto[:2]}/{texto[2:4]}/{texto[4:]}"
            self.vencimento.delete(0, tk.END)
            self.vencimento.insert(0, data_formatada)
    def _formatar_periodo(self, event):
        texto = self.periodo.get().strip()
        if len(texto) == 6 and texto.isdigit():
            data_formatada = f"{texto[:2]}/{texto[2:]}"
            self.periodo.delete(0, tk.END)
            self.periodo.insert(0, data_formatada)
    def _on_tipo_change(self, event):
        self._ajustar_layout_com_difal_ou_st_ou_ican()
    def _validar_periodo(self, texto):
        # Retorna True se o texto for vazio ou contiver apenas números e até 8 caracteres
        if len(texto) > 7:
            return False
        for c in texto:
            if not (c.isdigit() or c == "/"):
                return False
        return True
    def _validar_vencimento(self, texto):
        if len(texto) > 10:
            return False
        for c in texto:
            if not (c.isdigit() or c == "/"):
                return False
        return True
    def _validar_valor(self, texto):
        # só pode conter dígitos ou vírgula
        for c in texto:
            if not (c.isdigit() or c == ","):
                return False
        # não pode ter mais de uma vírgula
        if texto.count(",") > 1:
            return False
        # verificar casas decimais
        if "," in texto:
            parte_inteira, parte_decimal = texto.split(",")
            if len(parte_decimal) > 2:
                return False
        return True
    def _validar_notas(self, texto):
        # só pode conter dígitos ou vírgula
        for c in texto:
            if not (c.isdigit() or c == "," or c == " "):
                return False
        return True
    def _split_values(self, value):
        return [v.strip() for v in str(value).split(",") if v.strip()]
    def _parse_datetime(self, value: str) -> datetime:
        """Converte string de data em datetime, assumindo formato padrão."""
        return datetime.strptime(value, "%d/%m/%Y")
    def _ajustar_layout_com_difal_ou_st_ou_ican(self):
        valor = self.tipos_var.get()
        if valor in ["DIFAL", "ST"]:
            self.notas_label.grid(row=6, column=0, padx=10, pady=5)
            self.notas.grid(row=6, column=1, padx=10, pady=5)

            self.fretes_label.grid(row=7, column=0, padx=10, pady=5)
            self.fretes.grid(row=7, column=1, padx=10, pady=5)

            self.salvar_formulario_btn.grid_remove()
            self.salvar_formulario_btn.grid(row=8, columnspan=2, pady=10)
        elif valor == "ICAN":
            self.notas.grid_remove()
            self.notas_label.grid_remove()

            self.fretes.grid_remove()
            self.fretes_label.grid_remove()

            self.salvar_formulario_btn.grid_remove()

            self.notas_label.grid(row=6, column=0, padx=10, pady=5)
            self.notas.grid(row=6, column=1, padx=10, pady=5)

            self.salvar_formulario_btn.grid(row=7, columnspan=2, pady=10)
        else:
            self.notas.grid_remove()
            self.notas_label.grid_remove()

            self.fretes.grid_remove()
            self.fretes_label.grid_remove()

            self.salvar_formulario_btn.grid_remove()
            self.salvar_formulario_btn.grid(row=6, columnspan=2, pady=10)
    def _editing(self):
        if self.edit:
            id = self.tree.tree_esquerda.selection()[0]
            guia = self.guia_controller.find_by_id(id)
            
            index = self.filial['values'].index(guia.filial)
            self.filial.current(index)
            self.filial.config(state="disabled")
            
            self.periodo.insert(0, guia.periodo.strftime("%m/%Y"))
            
            self.vencimento.insert(0, guia.vencimento.strftime("%d/%m/%Y"))
            
            index = self.tipo['values'].index(guia.tipo)
            self.tipo.current(index)
            
            self.valor.insert(0, f"{float(guia.valor):.2f}".replace(".", ","))
            
            self.fcp.insert(0, f"{float(guia.fcp):.2f}".replace(".",","))
            
            if guia.tipo in ("DIFAL", "ST"):
                self.salvar_formulario_btn.grid(row=8, columnspan=2, pady=10)
            if guia.tipo == "ICAN":
                self.salvar_formulario_btn.grid(row=7, columnspan=2, pady=10)


            if guia.tipo in ("DIFAL", "ST"):
                self._ajustar_layout_com_difal_ou_st_ou_ican()
                if len(guia.fretes) > 1:
                    self.fretes.insert(0, ", ".join(guia.fretes))
                elif len(guia.fretes) == 1:
                    self.fretes.insert(0, guia.fretes)
            
            if guia.tipo in ("DIFAL", "ST", "ICAN"):
                self._ajustar_layout_com_difal_ou_st_ou_ican()
                if len(guia.notas) > 1:
                    self.notas.insert(0, ", ".join(guia.notas))
                elif len(guia.notas) == 1:
                    self.notas.insert(0, guia.notas)
                
            self._ajustar_layout_com_difal_ou_st_ou_ican()

        

    def salvar_formulario(self):
        # Validação mínima
        if not self.periodo.get() or not self.vencimento.get() or not self.valor.get():
            messagebox.showerror("Erro", "Campos obrigatórios!")
            return

        lojainfo = self.loja_controller.find(self.filial.get())
        site_url = self.site_controller.find_url(lojainfo.uf, self.tipo.get())
        siteinfo = self.site_controller.find(lojainfo.uf)
        
        # Criação do objeto Guia (deve ser via controller/use case)
        guia_data = {
            "filial": self.filial.get(),
            "periodo": datetime.strptime("01/" + self.periodo.get(), "%d/%m/%Y"),
            "vencimento": datetime.strptime(self.vencimento.get(), "%d/%m/%Y"),
            "tipo": self.tipo.get(),
            "valor": self.valor.get().replace(",", "."),
            "fcp": self.fcp.get().replace(",", "."),
            "notas": self.notas.get() if self.tipo.get() in ("DIFAL", "ST", "ICAN") else [],  # Aqui você pode incluir lógica de parseamento
            "fretes": self.fretes.get() if self.tipo.get() in ("DIFAL", "ST") else [],
            "cnpj": lojainfo.cnpj,
            "ie": lojainfo.ie,
            "uf": lojainfo.uf,
            "site": site_url,
            "loja_id": lojainfo.id,
            "site_id": siteinfo.id
        }

        guia = Guia(
            **guia_data
        )
        
        if self.edit:
            search_guia = self.guia_controller.find(guia.filial, guia.tipo)
            guia.id = search_guia.id
            self.guia_controller.update(guia)
            self.tree.reload()
            self.destroy()
        else:
            adicionou = self.guia_controller.add(guia)
            
            if adicionou:
                created_guia = self.guia_controller.find(guia.filial, guia.tipo)                
                guia.id = created_guia.id
                
                self.tree.adicionar_guia(guia)
                self.destroy()
            else:
                messagebox.showerror('Aviso', "Já existe uma guia dessa filial e desse tipo na listagem.")
            
