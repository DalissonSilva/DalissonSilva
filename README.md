<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/DalissonSilva/DalissonSilva/main/dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/DalissonSilva/DalissonSilva/main/dark.svg">
  <img alt="Dálisson Silva — Engenheiro de Dados" src="https://raw.githubusercontent.com/DalissonSilva/DalissonSilva/main/dark.svg">
</picture>

</div>

<br/>

<div align="center">

<img width="100%" src="https://streak-stats.demolab.com/?user=DalissonSilva&hide_border=true&background=0A0A0F&stroke=00E5FF&ring=A78BFA&fire=10B981&currStreakLabel=00E5FF&sideLabels=94A3B8&currStreakNum=F8FAFC&sideNums=F8FAFC&dates=64748B&titleColor=00E5FF&card_width=1180" alt="streak" />

<br/><br/>

<img width="49%" src="https://github-readme-stats-eta-lilac-39.vercel.app/api?username=DalissonSilva&show_icons=true&count_private=true&include_all_commits=true&hide_rank=true&hide_border=true&title_color=00E5FF&icon_color=A78BFA&text_color=94A3B8&bg_color=0A0A0F&card_width=500" alt="stats" />
<img width="49%" src="https://github-readme-stats-eta-lilac-39.vercel.app/api/top-langs/?username=DalissonSilva&layout=compact&langs_count=8&hide_border=true&title_color=00E5FF&text_color=94A3B8&bg_color=0A0A0F&card_width=500" alt="top langs" />

</div>

<br/>

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/DalissonSilva/DalissonSilva/output/github-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/DalissonSilva/DalissonSilva/output/github-snake-dark.svg" />
  <img alt="Snake devorando minhas contribuições" src="https://raw.githubusercontent.com/DalissonSilva/DalissonSilva/output/github-snake-dark.svg" />
</picture>

</div>

---

### `quem sou eu`

> Profissional de dados **full-cycle** — da ingestão bruta à cultura de dados.
> Na **Unimed Maceió**, construo a arquitetura que transforma o operacional do Tasy em decisão estratégica.

```yaml
local:    Maceió, Alagoas — Brasil
empresa:  Unimed Maceió
dominio:  Saúde Suplementar & Hospitalar
foco:     Engenharia · Arquitetura · Governança · Analytics
```

---

### `pilares de atuação`

<table>
<tr>
<td width="50%" valign="top">

**`01` engenharia de dados**
*a fundação que move os dados*

```yaml
linguagens:
  - Python
  - SQL / PL/SQL
  - Shell Script
pipelines:
  - ETL end-to-end
  - Ingestão automatizada
  - Orquestração Airflow
infra:
  - Linux / Ubuntu
  - Cron Jobs
  - Oracle Database
  - Autonomous DB (OCI)
```

</td>
<td width="50%" valign="top">

**`02` arquitetura de dados**
*estrutura pensada para escalar*

```yaml
padroes:
  - Medallion Architecture
  - Bronze / Silver / Gold
  - Data Lakehouse
ambientes:
  - Data Lake
  - Data Warehouse
  - Data Mart
cloud:
  - Oracle Cloud (OCI)
  - GCP + Databricks
  - Compute VM
```

</td>
</tr>
<tr>
<td width="50%" valign="top">

**`03` governança de dados**
*confiabilidade do dado, do início ao fim*

```yaml
qualidade:
  - Validação e linhagem
  - Rastreabilidade (DL_DT_CARGA)
  - Monitoramento e SLA
seguranca:
  - Controle de acesso por role
  - Auditoria
  - LGPD
catalogo:
  - Dicionário de dados
  - Matriz de Data Owners
  - Documentação viva no Git
```

</td>
<td width="50%" valign="top">

**`04` analytics & BI**
*do dado ao insight estratégico*

```yaml
ferramentas:
  - Qlik Sense / QlikView
  - Power BI
  - Streamlit
entregas:
  - Dashboards interativos
  - KPIs estratégicos
  - Indicadores ANS / CFM
abordagem:
  - Self-service BI
  - Storytelling com dados
```

</td>
</tr>
</table>

---

### `fluxo medalhão`

```
   FONTES              BRONZE              SILVER               GOLD
 ┌──────────┐       ┌──────────┐       ┌──────────┐       ┌──────────┐
 │  Oracle  │──────▶│  Cópia   │──────▶│  Regras  │──────▶│ Parquet  │
 │  Tasy    │       │  fiel    │       │  de      │       │ por      │
 │  APIs    │       │  do ERP  │       │  negócio │       │ painel   │
 │  Files   │       │  Raw     │       │  Trusted │       │ Analytics│
 └──────────┘       └──────────┘       └──────────┘       └──────────┘
                          ▲                  ▲                  ▲
                    Engenharia          Arquitetura         Analytics
                    Rastreabilidade     Qualidade           Qlik · BI
                    ╰──────────────  Airflow · SLA · Log  ──────────────╯
```

O banco de produção é tocado **apenas** pela camada Bronze. Nenhuma ferramenta de BI conversa direto com o ERP.

---

### `stack`

<div align="center">

![Python](https://img.shields.io/badge/Python-0A0A0F?style=for-the-badge&logo=python&logoColor=00E5FF&labelColor=0A0A0F)
![Oracle](https://img.shields.io/badge/Oracle-0A0A0F?style=for-the-badge&logo=oracle&logoColor=F43F5E&labelColor=0A0A0F)
![SQL](https://img.shields.io/badge/SQL-0A0A0F?style=for-the-badge&logo=postgresql&logoColor=A78BFA&labelColor=0A0A0F)
![Airflow](https://img.shields.io/badge/Airflow-0A0A0F?style=for-the-badge&logo=apacheairflow&logoColor=10B981&labelColor=0A0A0F)
![Linux](https://img.shields.io/badge/Linux-0A0A0F?style=for-the-badge&logo=linux&logoColor=FBBF24&labelColor=0A0A0F)

![OCI](https://img.shields.io/badge/Oracle%20Cloud-0A0A0F?style=for-the-badge&logo=oracle&logoColor=F43F5E&labelColor=0A0A0F)
![Databricks](https://img.shields.io/badge/Databricks-0A0A0F?style=for-the-badge&logo=databricks&logoColor=00E5FF&labelColor=0A0A0F)
![Qlik](https://img.shields.io/badge/Qlik%20Sense-0A0A0F?style=for-the-badge&logo=qlik&logoColor=10B981&labelColor=0A0A0F)
![Power BI](https://img.shields.io/badge/Power%20BI-0A0A0F?style=for-the-badge&logo=powerbi&logoColor=FBBF24&labelColor=0A0A0F)
![Streamlit](https://img.shields.io/badge/Streamlit-0A0A0F?style=for-the-badge&logo=streamlit&logoColor=F43F5E&labelColor=0A0A0F)

</div>

---

### `vamos conversar`

<div align="center">

<a href="https://www.linkedin.com/in/dalisson-silva-a01a591a7/">
<img src="https://img.shields.io/badge/LinkedIn-0A0A0F?style=for-the-badge&labelColor=0A0A0F&logo=data:image/svg%2Bxml;base64,PHN2ZyByb2xlPSJpbWciIHZpZXdCb3g9IjAgMCAyNCAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiBmaWxsPSIjMDBFNUZGIj48cGF0aCBkPSJNMjAuNDQ3IDIwLjQ1MmgtMy41NTR2LTUuNTY5YzAtMS4zMjgtLjAyNy0zLjAzNy0xLjg1Mi0zLjAzNy0xLjg1MyAwLTIuMTM2IDEuNDQ1LTIuMTM2IDIuOTM5djUuNjY3SDkuMzUxVjloMy40MTR2MS41NjFoLjA0NmMuNDc3LS45IDEuNjM3LTEuODUgMy4zNy0xLjg1IDMuNjAxIDAgNC4yNjcgMi4zNyA0LjI2NyA1LjQ1NXY2LjI4NnpNNS4zMzcgNy40MzNjLTEuMTQ0IDAtMi4wNjMtLjkyNi0yLjA2My0yLjA2NSAwLTEuMTM4LjkyLTIuMDYzIDIuMDYzLTIuMDYzIDEuMTQgMCAyLjA2NC45MjUgMi4wNjQgMi4wNjMgMCAxLjEzOS0uOTI1IDIuMDY1LTIuMDY0IDIuMDY1em0xLjc4MiAxMy4wMTlIMy41NTVWOWgzLjU2NHYxMS40NTJ6TTIyLjIyNSAwSDEuNzcxQy43OTIgMCAwIC43NzQgMCAxLjcyOXYyMC41NDJDMCAyMy4yMjcuNzkyIDI0IDEuNzcxIDI0aDIwLjQ1MUMyMy4yIDI0IDI0IDIzLjIyNyAyNCAyMi4yNzFWMS43MjlDMjQgLjc3NCAyMy4yIDAgMjIuMjI1IDB6Ii8%2BPC9zdmc%2B" alt="LinkedIn" />
</a>
&nbsp;&nbsp;
<a href="https://DalissonSilva.github.io">
<img src="https://img.shields.io/badge/Portf%C3%B3lio-0A0A0F?style=for-the-badge&logo=github&logoColor=A78BFA&labelColor=0A0A0F" alt="Portfólio" />
</a>
&nbsp;&nbsp;
<a href="mailto:dalissonmuniz@outlook.com">
<img src="https://img.shields.io/badge/Email-0A0A0F?style=for-the-badge&logo=microsoftoutlook&logoColor=10B981&labelColor=0A0A0F" alt="Email" />
</a>

</div>
