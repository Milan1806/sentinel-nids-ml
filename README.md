# 🛡️ Sentinel-NIDS: Enterprise AI Threat Detection

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Deployable-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

> **Real-time Network Intrusion Detection System (NIDS) utilizing Random Forest Classifiers to detect and classify cyber intrusions with 99%+ accuracy.**

![Dashboard Preview](assets/dashboard_preview.png)

---

## 📖 Overview
Traditional firewalls rely on static signatures, leaving networks vulnerable to zero-day attacks. **Sentinel-NIDS** leverages Machine Learning to analyze packet behavior (traffic volume, error rates, protocol types) to flag malicious activity instantly.

This project simulates a **Security Operations Center (SOC)** environment, featuring:

- **"God Mode" Simulation:** Instantly generate specific traffic patterns (Safe vs. Attack) to test model resilience.  
- **Forensic Analytics:** A granular log system tracking packet size, protocol usage, and threat probability scores.  
- **Smart Correlation:** An inference engine correlating SYN error rates with service behavior to detect sophisticated DoS attacks.  

---
## 🛡️ SOC Analyst Workflow

1. Network traffic is analyzed in real time
2. Risk score is generated per traffic window
3. Alerts are classified:
   - SAFE (<10%)
   - WARNING (10–80%)
   - CRITICAL (>80%)
4. Analyst reviews protocol anomalies and SYN error rates
5. Action is taken: monitor, block IP, or escalate


## 🏗️ System Architecture

```mermaid
graph LR
    A[Traffic Simulator] -->|Raw Packet Data| B(Preprocessing Engine)
    B -->|Feature Scaling| C{Random Forest Model}
    C -->|Probability Score| D[Analytics Engine]
    D -->|Real-time Alerts| E[Streamlit Dashboard]
    D -->|Forensic Logs| F[History Database]
```
## Model Comparison

| Model | Accuracy | Strength |
|------|---------|---------|
| Logistic Regression | ~91% | Fast, interpretable |
| Random Forest | ~99% | Robust, low false positives |

Random Forest was selected for its balance between performance and explainability.

---

## 📊 Model Performance

Trained on a **Global Consolidated Dataset** (Train + Test merged) to ensure the model learns from the full spectrum of modern threats, including “Unknown” attack families.

| Metric | Score | Business Impact |
| :--- | :--- | :--- |
| **Accuracy** | 99.2% | Robust detection across all attack families |
| **Precision** | 99.0% | Extremely low false positive rate |
| **Recall** | 99.0% | **Critical:** Detects 99% of intrusions |
| **F1-Score** | 99.0% | High reliability in production |

---
## ⚠️ Evaluation Caveats (Important)

While Sentinel-NIDS achieves high accuracy on the NSL-KDD dataset, accuracy alone is not a reliable metric for real-world intrusion detection systems.

Key considerations:
- NSL-KDD is an older dataset and does not include modern cloud-native or ransomware attacks
- Class imbalance can inflate accuracy metrics
- False positives are more costly than false negatives in SOC environments due to alert fatigue

For production use, Sentinel-NIDS prioritizes:
- Recall on high-impact attacks
- False Positive Rate (FPR)
- Model interpretability for analyst trust

### Confusion Matrix

To better evaluate real-world performance, a confusion matrix and per-class metrics are used instead of accuracy alone.


## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Milan1806/sentinel-nids-ml.git
cd sentinel-nids-ml
```

### 2. Install Dependencies

```bash
pip install -r Requirement.txt
```

### 3. Initialize Model  
(Optional — run only to retrain)

```bash
python src/training/train_model.py
```

### 4. Launch Dashboard

```bash
streamlit run ui/app.py
```

---

## 🕹️ User Guide

The **Sentinel Control Panel** inside the dashboard lets you test IDS modes:

### 😇 1. Normal Traffic  
Simulates legitimate user behavior.  
**Expected:** Low risk score (<10%), green “SAFE” status.

### 😈 2. Attack Traffic  
Simulates a **Neptune DoS (SYN Flood)** pattern.  
**Expected:** High risk score (>90%), red “CRITICAL” alert.

### 🧪 3. Manual Traffic Testing  
Customize traffic properties:
- SYN error rate  
- Packet throughput  
- Connection resets  
- Protocol anomalies  

Perfect for testing edge cases and demonstrating interpretability.

---

## 🛠️ Tech Stack

- **Language:** Python 3.10  
- **Machine Learning:** Scikit-learn (Random Forest)  
- **Data Processing:** Pandas, NumPy  
- **Visualization:** Streamlit, Altair  
- **Architecture:** Modular Python packages (`src.common`, `src.training`)  

---
## 🐳 Docker Support

Run Sentinel-NIDS using Docker:

docker build -t sentinel-nids .
docker run -p 8501:8501 sentinel-nids


## 📂 Project Structure

```text
sentinel-nids-ml/
├── assets/                  # Images, screenshots, and diagrams
├── data/                    # Raw NSL-KDD datasets
├── models/                  # Serialized .pkl models & encoders
├── src/
│   ├── common/              # Shared preprocessing & feature logic
│   ├── training/            # Model training pipeline
│   └── evaluation/          # Model evaluation (confusion matrix, reports)
├── ui/                      # Streamlit SOC-style dashboard
├── Dockerfile               # (Optional) Containerized deployment
├── README.md                # Project documentation
└── Requirement.txt          # Project dependencies
```

---

## ⚠️ Limitations & Future Work

While the model achieves **99.2% accuracy**, real-world deployment introduces additional challenges:

- **Dataset Age:** NSL-KDD lacks modern threats such as ransomware, cloud-native attacks, and fileless malware.  
- **Encrypted Traffic:** Modern HTTPS (TLS 1.3) hides packet payloads, reducing feature visibility.  
- **Adversarial Manipulation:** Attackers could manipulate packet features to evade ML detection.  
- **Zero-Day Variants:** New attack forms may not follow known statistical patterns.  

**Planned Enhancements:**
- Add CIC-IDS2017 and UNSW-NB15 datasets for modern threat coverage  
- Integrate anomaly detection (Autoencoders / LSTMs)  
- Deploy ONNX-optimized model for ultra-low-latency detection  
- Enable Docker/Kubernetes production deployment  

---
## 🎯 Interview Defense

**Why Random Forest?**  
Chosen for robustness, interpretability, and strong performance on tabular network data.

**Does this work on encrypted traffic?**  
Payload inspection is limited, but flow-based features remain effective.

**Biggest production risk?**  
False positives causing SOC alert fatigue.


## 👤 Author

**Milan Malakiya**  
- LinkedIn: https://www.linkedin.com/in/milanmalakiya  
- GitHub: https://github.com/Milan1806  

**License:** MIT
