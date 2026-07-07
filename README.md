# 🛡️ AI-Hybrid-WAF-IPS

An intelligent, lightweight Hybrid Web Application Firewall (WAF) and Intrusion Prevention System (IPS) designed for SME (Small and Medium-sized Enterprises) environments. This system combines classic Machine Learning for real-time anomaly detection, active firewall mitigation, and Generative AI for executive security reporting.

## 🎯 Project Objective

Traditional security solutions are often too resource-heavy or complex for SME environments. This project aims to build an autonomous, adaptive defense system that:
1. Detects network and application-layer attacks in real-time.
2. Applies targeted active defense mechanisms (not just blocking everything, but mitigating specific threats gracefully).
3. Generates readable, actionable incident reports for non-technical managers.

## 🏗️ System Architecture

The project is divided into four highly modular components:

- **🧠 The Brain (ML Detection):** A Random Forest classifier trained on the `CIC-IDS2017` dataset. It analyzes incoming traffic metadata and HTTP payloads to classify threats (e.g., DDoS, SQL Injection, XSS, Port Scanning) in milliseconds with minimal CPU overhead.
- **🛡️ The Core (Active Defense):** A Python/Scapy traffic sniffer that feeds data to the ML model. Based on the classification, it triggers specific mitigation scripts using Linux `iptables` (e.g., temporary bans for port scans, targeted port blocking for web attacks, complete drops for DDoS).
- **🪤 The Web Honeypot:** A lightweight, intentionally vulnerable Flask application used as a decoy to attract, detect, and analyze Layer 7 attacks (SQLi, XSS) in a controlled environment.
- **📊 The Reporter (GenAI):** An automated reporting module powered by local LLMs (Llama 3 via Ollama) that reads the SQLite alert database and generates executive summaries of daily security events.

## 🛠️ Tech Stack

* **Data Science & ML:** Python, Scikit-Learn, Pandas, NumPy
* **Network & Security:** Scapy, Linux `iptables`, TCP/IP
* **Web Environment:** Flask, HTML/CSS
* **Generative AI:** Ollama, Llama 3
* **Database:** SQLite

## 🗺️ Roadmap & Development Phases

- [x] **Phase 0:** System Architecture & Repository Structure Design
- [ ] **Phase 1 (Ongoing):** Data preparation and Machine Learning model training (Random Forest + CIC-IDS2017 dataset).
- [ ] **Phase 2:** Development of the Core defense scripts, traffic sniffing, and dynamic firewall management.
- [ ] **Phase 3:** Integration of the Flask Honeypot to capture and mitigate web-specific attacks (Layer 7).
- [ ] **Phase 4:** Implementation of the Generative AI automated reporting module.
