# Dashboard de Monitoramento de Cotações

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2.2-blue?style=for-the-badge)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7.1-orange?style=for-the-badge&logo=matplotlib)

Um aplicativo de desktop completo e personalizável para o monitoramento de cotações de moedas e criptomoedas, com sistema de login, gráficos históricos e interface dinâmica.

## 📸 Screenshots

| Tela de Login | Dashboard Principal |
| :---: | :---: |
| ![Tela de Login](https://i.imgur.com/NcH2PoH.png) | ![Dashboard Principal](https://i.imgur.com/r4wnrQM.png) |

## ✨ Funcionalidades

- **Sistema de Autenticação:** Tela de Login e Registro com senhas seguras (hashed) e banco de dados SQLite.
- **Dashboard Dinâmico:** Adicione ou delete moedas de sua preferência em tempo real, sem precisar fechar o programa.
- **Persistência de Dados:** Sua lista de moedas é salva localmente e carregada sempre que você abre o app.
- **Visualização Detalhada:** Cada moeda é exibida em um "card" com preço atual, variação percentual, máxima do dia e um gráfico histórico dos últimos 30 dias.
- **Gráficos Históricos:** Gerados com Matplotlib para uma análise visual rápida da tendência de cada ativo.
- **Interface Interativa:** Scroll horizontal automático na área dos cards para uma navegação fluida e moderna.
- **Atualizações Automáticas e Manuais:** As cotações são atualizadas periodicamente e também através de um botão de atualização manual.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Interface Gráfica:** CustomTkinter
- **Banco de Dados:** SQLite3 (para usuários)
- **Requisições HTTP:** Requests (para consumir a API)
- **Manipulação de Dados:** Pandas
- **Visualização de Dados:** Matplotlib
- **API de Cotações:** [AwesomeAPI](https://docs.awesomeapi.com.br/api-de-moedas)