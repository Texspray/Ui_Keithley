# 🇺🇸 About the Project
The goal of this Technological Initiation project was to automate a measurement instrument for the Physics Laboratory at UTFPR - Toledo Campus.

The equipment is a **Keithley 2614B** (*Source Measure Unit* - SMU), capable of measuring extremely low currents (nanoamperes). 
* **Firmware:** The instrument's internal programming was developed in **Lua**.
* **Communication:** External communication was established using Python and the **PyVISA** library.

Once communication with the device was established, a User Interface (UI) was implemented to accept user input for measurements and handle real-time data plotting.

## 🛠 Technologies Used
* **GUI:** PyQt and PyQtGraph (chosen for its efficiency in engineering applications and high performance in real-time charting).
* **Data Processing:** NumPy.
* **Hardware Communication:** PyVISA.
* **Storage:** OpenPyXL (data export).

## Automatização de Instrumento de Medição (Keithley 2614B)

> **Iniciação Tecnológica (2021-2022)** > Universidade Tecnológica Federal do Paraná (UTFPR) - Campus Toledo

### 🇧🇷 Sobre o Projeto
O objetivo desta Iniciação Tecnológica foi realizar a automatização de um equipamento de medição para o laboratório de física da UTFPR.

O equipamento em questão é um **Keithley 2614B** (*Source Measure Unit* - SMU), capaz de medir baixas correntes (na ordem de nanoamperes). 
* **Firmware:** A programação interna do equipamento foi realizada em **Lua** (TSB).
* **Comunicação:** A comunicação externa foi estabelecida via **Python**, utilizando a biblioteca **PyVISA**.

Após estabelecer a comunicação, foi implementada uma interface de usuário (GUI) capaz de receber parâmetros, realizar as medições e plotar os dados em tempo real.

#### 🛠 Tecnologias Utilizadas
* **Interface Gráfica:** PyQt e PyQtGraph (escolhido pela alta performance em atualizações de gráficos em tempo real para engenharia).
* **Processamento de Dados:** NumPy.
* **Comunicação de Hardware:** PyVISA.
* **Armazenamento:** OpenPyXL (exportação de dados).

---

