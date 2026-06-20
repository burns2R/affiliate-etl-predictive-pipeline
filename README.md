# From Reactive to Proactive: Re-Engineering Affiliate Partner Strategy

> **Project Summary:** Led a cross-functional initiative to automate affiliate performance tracking, shifting the business from reactive monthly reviews to real-time, data-driven optimization.

### 📈 Key Result: 21% MoM revenue increase sustained over 5 months.

---

## 🎯 The Challenge (Situation & Task)
Managing 15+ click campaigns across four distinct affiliate partner portals created a massive data visibility gap. Because the team lacked a centralized view, performance reviews were limited to a reactive monthly cadence, leading to delayed optimization and missed opportunities to maximize lead volume ROI.

During a team transition, I stepped in to lead affiliate partner management. My mandate was to reduce manual overhead, eliminate the reactive management cycle, and implement a data-driven strategy to maximize campaign earnings.

## 💡 The Solution (Action & Result)
I spearheaded the project by securing API access across all partners and engineering a custom ETL pipeline to centralize disparate data. I built a consolidated reporting platform with drill-down capabilities (organized by marketing campaign and sub-campaign) and deployed a predictive ML model to recommend optimal traffic weights based on historical and real-time performance.

This shift from reactive monthly reviews to proactive, daily optimizations drove a sustained 21% MoM revenue increase over five months. I successfully transitioned the process from a manual burden to an automated, scalable framework, allowing for a seamless handoff to the marketing team.

---

## 🏗️ System Architecture
```mermaid
graph TD
    A[Partner Portals] -->|Data Ingestion| B(FastAPI Mock Servers)
    B -->|ETL Pipeline| C(PostgreSQL Warehouse)
    C -->|Analytics Layer| D[Predictive ML Model & Dashboard]

# Affiliate ETL & Predictive Pipeline

### 🚀 Key Features
- ...
![Dashboard Preview](assets/dashboard_preview.png)
