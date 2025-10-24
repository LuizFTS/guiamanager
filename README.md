# 🧾 GuiaManager

**GuiaManager** é um aplicativo desktop desenvolvido em **Python** para automação e gerenciamento de **guias fiscais**, com interface gráfica intuitiva, suporte a múltiplas lojas e geração automatizada de relatórios.  
O sistema segue princípios de **Domain-Driven Design (DDD)**, garantindo organização, escalabilidade e fácil manutenção do código.

---

## 🚀 Funcionalidades Principais

- 📂 **Importação de dados via Excel** — Leitura e tratamento de arquivos `.xlsx` com **Pandas**.  
- 🧱 **Metodologia DDD** — Separação clara entre domínio, aplicação, infraestrutura e interface.  
- 🪟 **Interface gráfica (Tkinter)** — Painel duplo para controle de guias, botões de geração e feedback visual.  
- ⚙️ **Banco de dados SQLite** — Estrutura local para armazenar informações de certificados, lojas e guias.  
- 🔁 **Execução paralela** — Threads para geração simultânea de múltiplas guias.  
- 🌐 **Automação com Selenium** — Abertura e preenchimento automático de portais de emissão de guias.  
- 📊 **Controle de status** — Marcação automática de guias em andamento, concluídas ou com erro.  

---

## 🧩 Funcionalidades em Desenvolvimento

- 🔐 **Configuração de certificado digital** — Interface para seleção e vinculação de certificados por loja. No momento para o estado do ES,
a importação do certificado digital inserido manualmente.
- 📁 **Path de download dinâmico** — Usuário poderá definir:
  - Diretório de destino;
  - Nome dinâmico do PDF utilizando variáveis como:
    - `{{numero_filial}}`
    - `{{mes_referencia}}`
    - `{{ano_referencia}}`
    - `{{tipo_guia}}`
  
  Exemplo:  
  ```
  C:/Guias/{{tipo_guia}}/{{ano_referencia}}/{{mes_referencia}}_{{numero_filial}}.pdf
  ```

---

## 🧱 Estrutura do Projeto

```
GuiaManager/
│
├── application/           # Casos de uso (use cases)
├── domain/                # Entidades e regras de negócio
├── infrastructure/        # Banco de dados, repositórios, automações
├── gui/                   # Interface gráfica (Tkinter)
│
├── main.py                # Ponto de entrada da aplicação
├── requirements.txt       # Dependências do projeto
└── README.md              # Este arquivo
```

---

## 🖥️ Interface Gráfica

A interface Tkinter é composta por:

- **Painel da esquerda:** lista de guias disponíveis.  
- **Painel da direita:** guias selecionadas para geração.  
- **Botão “Gerar Guias”** — executa o processo com feedback visual e bloqueio temporário do botão.  
- **Menu de configuração:** atualmente em desenvolvimento (centralizado automaticamente na tela).  

---

## ⚙️ Instalação e Execução

### 🔧 Requisitos

- Python **3.11+**
- Sistema operacional Windows (recomendado)

### 📦 Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/LuizFTS/guiamanager.git
   cd guiamanager
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Execute o aplicativo:

   ```bash
   python main.py
   ```

---

## 🧰 Principais Dependências

As bibliotecas estão listadas no `requirements.txt`.  
Algumas das principais:

- **Tkinter** — GUI nativa.  
- **Pandas** — leitura e manipulação de dados CSV.  
- **Selenium** — automação de processos web.  
- **PyAutoGUI** — controle de tela e automação de cliques.  
- **BeautifulSoup4** — parsing de HTML.  
- **SQLite3** — banco de dados local.

---

## 🧩 Estrutura do Banco de Dados

O banco SQLite contém tabelas como:

- `Certificados` — certificados digitais das lojas.  
- `Lojas` — informações das filiais.  
- `Guias` — dados de guias geradas.  
- `Sites` — Cadastro dos sites em que são geradas as guias.  

> ⚠️ As colunas utilizam `CapitalCase` (ex: `"Loja_Id"`, `"Cert_Path"`) para manter consistência com o ORM e o SQL gerado.

---

## 🔄 Fluxo de Geração das Guias

1. Importa dados via Excel.  
2. Exibe guias na interface (painel esquerdo).  
3. Usuário seleciona as guias desejadas.  
4. Ao clicar em “Gerar Guias”:
   - As guias são marcadas como *em andamento*.  
   - Threads são criadas para execução paralela.  
   - O progresso é exibido visualmente.  

## 🧑‍💻 Autor

Desenvolvido por **Luiz Tosta**  
💼 Projeto em desenvolvimento — parte do sistema **GuiaManager**.

---

## 📜 Licença

Este projeto está licenciado sob a **MIT License** — veja o arquivo [LICENSE](LICENSE) para mais detalhes.
