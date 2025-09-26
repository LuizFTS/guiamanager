# GuiaManager - Arquitetura e Passo a Passo de Desenvolvimento

Este documento descreve a **organização do projeto**, seguindo **Clean Architecture** e princípios **SOLID**, e serve como guia para desenvolvimento, refatoração e expansão.

---

## 1. Camadas do Projeto

| Camada | O que contém | Observações |
|--------|-------------|-------------|
| **Domain** | Entities, Interfaces de Repositories | Não conhece infra, apenas contratos. |
| **Infrastructure** | Implementações de Repositories, Database, Selenium, Excel, Email | Depende de detalhes de armazenamento e serviços externos. |
| **Application (UseCases/Services)** | Casos de uso, orquestração da lógica de negócio | Recebe entities e repositories, aplica regras de negócio. |
| **GUI** | Tkinter Forms, TreeViews, Botões | Apenas interage com UseCases, não acessa banco ou Selenium diretamente. |

---

## 2. Estrutura de Pastas Sugerida

```text
GuiaManager/
│
├─ domain/
│  ├─ entities/
│  │  ├─ guia.py
│  │  ├─ loja.py
│  │  └─ site.py
│  └─ repositories/
│     ├─ i_guia_repository.py
│     ├─ i_loja_repository.py
│     └─ i_site_repository.py
│
├─ infrastructure/
│  ├─ db/
│  │  ├─ database.py
│  │  ├─ guia_repository_sqlite.py
│  │  ├─ loja_repository_sqlite.py
│  │  └─ site_repository_sqlite.py
│  ├─ selenium/
│  ├─ excel/
│  ├─ email/
│  └─ utils/
│
├─ application/
│  ├─ usecases/
│  │  ├─ importar_guias_excel.py
│  │  ├─ emitir_guia.py
│  │  ├─ atualizar_guia.py
│  │  ├─ excluir_guia.py
│  │  └─ listar_guias.py
│
├─ gui/
│  ├─ forms/
│  │  ├─ form_guia_gui.py
│  │  └─ config_dialogs/
│  ├─ tree_panel.py
│  └─ app.py
│
├─ data/          # arquivos .json, certificado etc
├─ img/
├─ main.py
└─ README.md
---

## 3. Passo a Passo de Desenvolvimento

### 3.1 Criar Database
1. Criar `Database` na pasta `infrastructure/db/database.py`.
2. Criar script de migrations (tabelas `Sites`, `Lojas`, `Guias`, `NotasGuia`, `FretesGuia`).
3. Testar conexão e criação de tabelas.

### 3.2 Criar Entities (Domain Layer)
- `Guia`, `Loja`, `Site` como dataclasses ou classes Python.
- Incluir atributos conforme necessidade da aplicação.

### 3.3 Criar Interfaces de Repositories (Domain Layer)
- Ex.: `IGuiaRepository` com métodos:
  - `save(guia, loja_id, site_id) -> bool`
  - `update(guia, loja_id, site_id) -> bool`
  - `delete(guia_id) -> bool`
  - `get_by_id(guia_id) -> Optional[Guia]`
  - `list_all() -> List[Guia]`
- Interfaces não conhecem detalhes do banco.

### 3.4 Criar Repositories Concretos (Infrastructure Layer)
- Ex.: `GuiaRepositorySQLite`
- Implementa a interface do domínio, acessando SQLite.
- Trata erros, retorna `bool` em operações de escrita.
- Popula notas e fretes separadamente.

### 3.5 Criar UseCases / Services (Application Layer)
- Orquestram a lógica de negócio.
- Chamam os repositories e serviços externos (Excel, Selenium, Email).
- Exemplo de fluxo:
  1. Recebe `Guia` do Excel.
  2. Resolve IDs de Loja e Site.
  3. Busca valor correto do Site de acordo com `guia.tipo`.
  4. Salva no banco.
  5. Emite guia via Selenium (se necessário).

### 3.6 Integrar GUI
- Tkinter chama apenas **UseCases**, nunca acessa o banco ou Selenium diretamente.
- Ex.: botão “Importar Excel” chama `ImportarGuiasExcel.execute(file_path)`.

### 3.7 Testes Unitários
- Testar UseCases com mocks de repositories.
- Testar repositories com banco de teste (SQLite in-memory).
- Garantir que regras de negócio funcionem corretamente.

---

## 4. Boas práticas

- **SOLID**
  - Single Responsibility: cada classe faz uma única coisa.
  - Dependency Inversion: UseCases dependem de interfaces, não de implementações.
- **Clean Architecture**
  - Camadas separadas.
  - Domínio não conhece infraestrutura.
- **Tratamento de erros**
  - Repositories retornam `bool` ou lançam exceção customizada.
  - UseCases lidam com erros e decidem se notifica GUI.

---
