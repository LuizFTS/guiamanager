import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import threading
import asyncio
from domain.entities.guia import Guia
from interface.controllers.guia_controller import GuiaController
from interface.controllers.excel_controller import ExcelController
from interface.controllers.site_controller import SiteController
from interface.controllers.loja_controller import LojaController
from interface.controllers.path_dynamic_controller import PathDynamicController

from interface.gui.tree_panel import TreePanel
from interface.gui.config_dialogs.menu_config import MenuConfig
from interface.gui.forms.form_guia_gui import FormGuiaGUI


class GuiaApp(tk.Tk):
    def __init__(self, guia_controller: GuiaController,site_controller: SiteController, loja_controller: LojaController, path_dynamic_controller: PathDynamicController):
        super().__init__()
        self.title("Gerador de Guias")
        self.guia_controller = guia_controller
        #self.excel_controller = excel_controller
        self.site_controller = site_controller
        self.loja_controller = loja_controller
        self.path_dynamic_controller = path_dynamic_controller

        style = ttk.Style()
        style.configure("Red.TFrame", background="red")

        # Botão importar Excel
        btn_excel = ttk.Button(self, text="📂 Importar Excel")
        btn_excel.pack(pady=(0, 10))

        # Painel de visualização (TreePanel)
        self.tree_panel = TreePanel(self)
        self.tree_panel.pack(fill="both", expand=True, pady=10)

        # Botões CRUD (Adicionar / Editar / Excluir)
        frame_buttons_guia_crud = ttk.Frame(self)
        frame_buttons_guia_crud.pack(fill="x", expand=True, pady=0, padx=6)

        self.addNewGuiaBtn = ttk.Button(frame_buttons_guia_crud, text="Adicionar", command=self.adicionar)
        self.addNewGuiaBtn.grid(row=2, column=0, sticky="w", pady=0, padx=4)

        self.editGuiaBtn = ttk.Button(frame_buttons_guia_crud, text="Editar", command=self.editar_guia)
        self.editGuiaBtn.grid(row=2, column=1, sticky="w", pady=0, padx=4)

        deleteGuiaBtn = ttk.Button(frame_buttons_guia_crud, text="Excluir", command=self.delete_guia)
        deleteGuiaBtn.grid(row=2, column=2, sticky="w", pady=0, padx=4)

        # Botão gerar guias
        frame_buttons = ttk.Frame(self)
        frame_buttons.pack(fill="x", expand=True, pady=10, padx=10)

        # Centralizar botão gerar
        frame_center = ttk.Frame(frame_buttons)
        frame_center.pack(side="top", expand=True)
        self.btn_gerar = ttk.Button(frame_center, text="🚀 Gerar guias", command=self.gerar_guias)
        self.btn_gerar.pack()

        # Botão de configuração (canto direito)
        frame_right = ttk.Frame(frame_buttons)
        frame_right.pack(side="right")
        self.icon_config = ImageTk.PhotoImage(Image.open("shared/resources/settings.png").resize((24, 24)))
        self.btn_config = ttk.Button(frame_right, image=self.icon_config, command=self.open_config)
        self.btn_config.pack(padx=10)

    # ==========================
    # Funções de integração com UseCases via Controller
    # ==========================
    """ def importar_excel(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if path:
            dados = self.excel_controller.importar_excel(path)
            dados = sorted(dados, key=lambda d: (int(d.filial), d.uf))
            self.tree_panel.set_dados(dados) """

    def gerar_guias(self):
        guias: list[Guia] = self.tree_panel.get_dados_direita()
        if not guias:
            messagebox.showwarning("Aviso", "Nenhuma guia no quadro da direita!")
            return

        self.btn_gerar.config(state="disabled")
        self.tree_panel.marcar_todos_em_andamento()
        self.threads = []

        semaforo_geral = threading.Semaphore(5)
        semaforo_pa = threading.Semaphore(1)

        def wrapper(guia: Guia):
            sem = semaforo_pa if guia.uf == "PA" else semaforo_geral
            with sem:
                self.processar_pdf_thread(guia)

        for guia in guias:
            t = threading.Thread(target=wrapper, args=(guia,), daemon=True)
            t.start()
            self.threads.append(t)

        self.check_threads_completion()

    def processar_pdf_thread(self, guia: Guia):
        pdf_generated = asyncio.run(self.controller.gerar_guia(guia))
        status = "ok" if pdf_generated else "erro"
        self.tree_panel.after(0, lambda: self.tree_panel.atualizar_status(guia, status))

    def check_threads_completion(self):
        if all(not t.is_alive() for t in self.threads):
            messagebox.showinfo("Aviso", "Processo concluído!")
            self.btn_gerar.config(state="enable")
        else:
            self.after(100, self.check_threads_completion)

    # ==========================
    # Funções de CRUD Guias (interface)
    # ==========================
    def adicionar(self):
        self._abrir_form_guia(edit=False)

    def editar_guia(self):
        selecionado = self.tree_panel.tree_esquerda.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma guia!")
            return
        self._abrir_form_guia(edit=True)

    def delete_guia(self):
        selecionado = self.tree_panel.tree_esquerda.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma guia!")
            return
        result = self.tree_panel.deletar_guia(selecionado[0])
        if not result:
            messagebox.showwarning("Aviso", "Erro ao excluir guia.")

    # ==========================
    # Funções de Dialog / Config
    # ==========================
    def open_config(self):
        dialog = MenuConfig(self, self.loja_controller, self.site_controller, self.path_dynamic_controller)
        dialog.transient(self)
        dialog.grab_set()
        self._centralizar_dialog(dialog)

    def _abrir_form_guia(self, edit: bool):
        dialog = FormGuiaGUI(self, self.tree_panel, edit=edit)
        self._centralizar_dialog(dialog)

    def _centralizar_dialog(self, dialog):
        dialog.update_idletasks()
        largura, altura = dialog.winfo_width(), dialog.winfo_height()
        root_x, root_y = self.winfo_x(), self.winfo_y()
        root_w, root_h = self.winfo_width(), self.winfo_height()
        x = root_x + (root_w - largura) // 2
        y = root_y + (root_h - altura) // 2
        dialog.geometry(f"+{x}+{y}")
