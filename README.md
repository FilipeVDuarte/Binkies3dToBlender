# Extraindo Geometria 3D do Binkies3D

Siga estes passos para extrair um modelo 3D de um projeto Live 3D no studio.binkies3d.com.

## Passos

### 1. Criar o Projeto
- Acesse [studio.binkies3d.com](https://studio.binkies3d.com).
- Crie um projeto *Live 3D* com o modelo desejado.

### 2. Acessar a Página de Embed
- Abra a página de *Embed* do projeto.

### 3. Substituir o JavaScript no Navegador
- Abra a página no Chrome/Chromium.
- Pressione **F12** para abrir as *Ferramentas do Desenvolvedor*.
- Vá para a aba **Sources**.
- Localize o arquivo `225.live3d-player.js` (ele será carregado pela página).
- Ative os *Local Overrides*:
  1. Em **Sources → Overrides**, escolha uma pasta local para armazenar os overrides.
  2. Clique com o botão direito em `225.live3d-player.js` e selecione **Save for overrides**.
- Abra o script substituído no editor.  
  Use **Ctrl+F** no editor para localizar:
  ```
  l = e(s, i)
  ```
- Insira uma linha logo após:
  ```javascript
  console.log(l);
  ```
- Recarregue a página. O JSON de geometria será impresso no console do navegador.

### 4. Exportar a Geometria
- Abra a aba *Console*.
- Copie o JSON exibido.
- Salve como `geometry.json` no seu diretório de trabalho.

### 5. Instalar Dependências
- Certifique-se de ter Python 3 e pip instalados.
- Instale os pacotes necessários:
  ```bash
  pip install numpy numpy-stl
  ```

### 6. Executar os Scripts de Conversão

> **Usuários Windows (PowerShell):** o operador `&&` não é suportado. Execute os comandos separadamente.

**Para exportar apenas a geometria (.stl):**
```bash
python filtr.py
python convert.py
```

**Para exportar com materiais e cores (.obj + .mtl):**
```bash
python filtr.py
python convert_obj.py
```

## Configurando a Cor no convert_obj.py

Abra o arquivo `convert_obj.py` e edite a variável `COLOR_OPTION` no topo:

```python
# Opções disponíveis: "Cosmic Orange", "Deep Blue", "Silver"
# Use None para exportar sem cor específica (materiais base)
COLOR_OPTION = "Cosmic Orange"
```

## Saída

| Script | Arquivo gerado | Descrição |
|--------|---------------|-----------|
| `convert.py` | `output_model.stl` | Apenas geometria (para impressão 3D) |
| `convert_obj.py` | `output_model.obj` + `output_model.mtl` | Geometria com materiais e cores |

Todos os arquivos são salvos no mesmo diretório dos scripts.

---

> Certifique-se de que todos os scripts e o arquivo `geometry.json` estejam na mesma pasta antes de começar.

---

## Solução de Problemas

### `&&` não é um separador de instruções válido
**Sistema:** Windows (PowerShell)  
**Causa:** O PowerShell não suporta o operador `&&` para encadear comandos.  
**Solução:** Execute os scripts separadamente:
```powershell
python filtr.py
python convert.py
```

---

### `python3` não é reconhecido como comando
**Sistema:** Windows  
**Causa:** No Windows, o Python geralmente é instalado como `python`, não `python3`.  
**Solução:** Substitua `python3` por `python` em todos os comandos:
```powershell
python filtr.py
python convert.py
```

---

### Modelo exportado sem cor ou com cor incorreta
**Causa:** O formato `.stl` não suporta materiais — armazena apenas geometria pura.  
**Solução:** Use o fluxo de exportação `.obj`:
```bash
python filtr.py
python convert_obj.py
```
Importe `output_model.obj` no Blender via **File → Import → Wavefront (.obj)** para carregar os materiais automaticamente.

---

### A cor desejada não aparece no modelo `.obj`
**Causa:** A variável `COLOR_OPTION` no `convert_obj.py` pode estar configurada para outra cor ou `None`.  
**Solução:** Abra `convert_obj.py` e edite a variável no topo:
```python
COLOR_OPTION = "Cosmic Orange"  # ou "Deep Blue", "Silver", None
```

---

### `geometry.json` não é gerado / console não exibe nada
**Causa:** O Local Override pode não estar ativo, ou a linha de código foi inserida no lugar errado.  
**Solução:**
1. Confirme que o override está ativo: em **Sources → Overrides**, o arquivo deve ter um ícone de ponto roxo.
2. Verifique que `console.log(l);` foi inserido **logo após** `l = e(s, i)`, não em outra linha.
3. Recarregue a página com o DevTools aberto e verifique a aba **Console**.

---

### Erro ao instalar dependências com `pip`
**Causa:** Conflito com o ambiente Python do sistema (comum no Linux/macOS).  
**Solução:** Use a flag `--break-system-packages`:
```bash
pip install numpy numpy-stl --break-system-packages
```

---
---

# Extracting 3D Geometry from Binkies3D

Follow these steps to extract a 3D model from a Live 3D project on studio.binkies3d.com.

## Steps

### 1. Create Project
- Go to [studio.binkies3d.com](https://studio.binkies3d.com).
- Create a *Live 3D project* with the desired model.

### 2. Access Embed Page
- Open the project's *Embed* page.

### 3. Override JavaScript in Browser
- Open the page in Chrome/Chromium.
- Press **F12** to open *Developer Tools*.
- Go to the **Sources** tab.
- Locate the file `225.live3d-player.js` (it will load from the page).
- Enable *Local Overrides*:
  1. In **Sources → Overrides**, pick a local folder to store overrides.
  2. Right-click on `225.live3d-player.js` and choose **Save for overrides**.
- Open the overridden script in the editor.  
  Use **Ctrl+F** in the editor to search for:
  ```
  l = e(s, i)
  ```
- When you find it, insert a line just after it:
  ```javascript
  console.log(l);
  ```
- Reload the page. Now the geometry JSON will be printed in the browser console.

### 4. Export Geometry
- Open the *Console* tab.
- Copy the logged JSON.
- Save it as `geometry.json` in your working directory.

### 5. Install Dependencies
- Make sure you have Python 3 and pip installed.
- Install required packages:
  ```bash
  pip install numpy numpy-stl
  ```

### 6. Run Conversion Scripts

> **Windows users (PowerShell):** the `&&` operator is not supported. Run commands separately.

**To export geometry only (.stl):**
```bash
python filtr.py
python convert.py
```

**To export with materials and colors (.obj + .mtl):**
```bash
python filtr.py
python convert_obj.py
```

## Configuring Color in convert_obj.py

Open `convert_obj.py` and edit the `COLOR_OPTION` variable at the top:

```python
# Available options: "Cosmic Orange", "Deep Blue", "Silver"
# Use None to export without a specific color (base materials only)
COLOR_OPTION = "Cosmic Orange"
```

## Output

| Script | Output file | Description |
|--------|-------------|-------------|
| `convert.py` | `output_model.stl` | Geometry only (for 3D printing) |
| `convert_obj.py` | `output_model.obj` + `output_model.mtl` | Geometry with materials and colors |

All files are saved in the same directory as the scripts.

---

> Ensure all scripts and `geometry.json` are in the same folder before starting.

---

## Troubleshooting

### `&&` is not a valid statement separator
**Platform:** Windows (PowerShell)  
**Cause:** PowerShell does not support the `&&` operator for chaining commands.  
**Fix:** Run the scripts separately:
```powershell
python filtr.py
python convert.py
```

---

### `python3` is not recognized as a command
**Platform:** Windows  
**Cause:** On Windows, Python is typically installed as `python`, not `python3`.  
**Fix:** Replace `python3` with `python` in all commands:
```powershell
python filtr.py
python convert.py
```

---

### Exported model has no color or wrong colors
**Cause:** The `.stl` format does not support materials — it stores geometry only.  
**Fix:** Use the `.obj` export workflow:
```bash
python filtr.py
python convert_obj.py
```
Import `output_model.obj` into Blender via **File → Import → Wavefront (.obj)** to load materials automatically.

---

### The desired color does not appear in the `.obj` model
**Cause:** The `COLOR_OPTION` variable in `convert_obj.py` may be set to a different color or `None`.  
**Fix:** Open `convert_obj.py` and edit the variable at the top:
```python
COLOR_OPTION = "Cosmic Orange"  # or "Deep Blue", "Silver", None
```

---

### `geometry.json` is not generated / nothing appears in the console
**Cause:** The Local Override may not be active, or the code line was inserted in the wrong place.  
**Fix:**
1. Confirm the override is active: in **Sources → Overrides**, the file should show a purple dot icon.
2. Make sure `console.log(l);` was inserted **immediately after** `l = e(s, i)`, not on a different line.
3. Reload the page with DevTools open and check the **Console** tab.

---

### Error installing dependencies with `pip`
**Cause:** Conflict with the system Python environment (common on Linux/macOS).  
**Fix:** Use the `--break-system-packages` flag:
```bash
pip install numpy numpy-stl --break-system-packages
```
