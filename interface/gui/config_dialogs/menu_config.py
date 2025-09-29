import tkinter as tk
from tkinter import ttk
from interface.gui.config_dialogs.site_config_dialog import SiteConfigDialog
from interface.gui.config_dialogs.loja_config_dialog import LojaConfigDialog
from interface.gui.config_dialogs.path_dynamic_config_dialog import PathDynamicConfigDialog

from interface.controllers.loja_controller import LojaController
from interface.controllers.site_controller import SiteController
from interface.controllers.path_dynamic_controller import PathDynamicController

class MenuConfig(tk.Toplevel):
    def __init__(self, master, loja_controller: LojaController, site_controller: SiteController, path_dynamic_controller: PathDynamicController):
        super().__init__(master)
        self.title("Menu configurações")

        self.loja_controller = loja_controller
        self.site_controller = site_controller
        self.path_dynamic_controller = path_dynamic_controller
        
        # Impede interação com a janela principal (modal)
        self.transient(master)
        self.grab_set()

        # Conteúdo do diálogo
        ttk.Label(self, text="Configurações").pack(padx=20, pady=10)
        ttk.Button(self, text="Sites", command=self._open_siteConfigModal).pack(padx=20, pady=5)
        ttk.Button(self, text="Lojas", command=self._open_lojaConfigModal).pack(padx=20, pady=5)
        ttk.Button(self, text="Configurar pasta de salvamento", command=self._open_PathDynamicConfigModal).pack(fill="x", padx=20, pady=5)

        ttk.Button(self, text="Fechar", command=self.destroy).pack(pady=45)

    
    def _open_siteConfigModal(self):
        dialog = SiteConfigDialog(self.master, self.site_controller)
        self.centralizar_janela(dialog, self.master)
        self.destroy()
        
    def _open_lojaConfigModal(self):
        dialog = LojaConfigDialog(self.master, self.loja_controller)
        self.centralizar_janela(dialog, self.master)
        self.destroy()
    
    def _open_PathDynamicConfigModal(self):
        # Cria o dialogo sem width/height
        dialog = PathDynamicConfigDialog(self.master, self.path_dynamic_controller)
        self.centralizar_janela(dialog, self.master)

        self.destroy()

    def centralizar_janela(self, janela, parent):
        janela.update_idletasks()  # força cálculo de tamanho

        janela.transient(self)
        janela.grab_set()

        # Força atualização para calcular tamanho
        parent.update_idletasks()
        janela.update_idletasks()

        largura = janela.winfo_width()
        altura = janela.winfo_height()

        # posição centralizada em relação à janela pai
        root_x = parent.winfo_x()
        root_y = parent.winfo_y()
        root_w = parent.winfo_width()
        root_h = parent.winfo_height()

        x = root_x + (root_w - largura) // 2
        y = root_y + (root_h - altura) // 2

        janela.geometry(f"+{x}+{y}")

