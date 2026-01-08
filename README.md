🧠 Behavioral Authentication System (Keystroke Dynamics)

📌 Overview  

This project implements a continuous behavioral authentication system using keystroke dynamics.
Instead of trusting a user based on a single login event, the system continuously evaluates trust by analyzing how a user types over time.

The system is explainable, adaptive, and defensive by design, focusing on risk modeling rather than blind classification.

🎯 Motivation

Traditional authentication mechanisms (passwords, OTPs, biometrics) suffer from:

one-time verification

session hijacking risks

poor detection of insider threats

Behavioral authentication addresses this gap by answering:

“Is the current user still the legitimate user?”

This project explores that question using typing behavior, modeled carefully to handle uncertainty, natural drift, and adversarial attempts.

🧩 Key Features
🔹 Keystroke Dynamics Capture

Key press & release events

High-resolution timestamps

Stored as structured CSV logs

🔹 Behavioral Feature Extraction

Mean key hold time

Mean inter-key delay

Typing speed (keys/sec)

Variance of hold time & delay (stability analysis)

🔹 Personalized Baseline

Learns what “normal” behavior looks like for a specific user

No global model, no population assumptions

🔹 Risk-Based Decision Making

Normalized deviation scoring

Three trust states:

NORMAL

UNCERTAIN

SUSPICIOUS

🔹 Risk Fusion Engine (V2)

Final risk score is computed by fusing:

Mean behavior drift

Stability (variance) loss

Session-level risk memory

This avoids single-signal domination and mirrors real security engines.

🔹 Continuous Session Monitoring

Sliding window over recent interactions

Trust accumulates or decays over time

Prevents snap judgments

🔹 Defensive Adaptive Learning

Baseline updates only under high confidence

Learning freeze when risk is elevated

Protects against slow poisoning attacks

🛡️ Security-Oriented Design Choices

Explainability over black-box ML

No hard lockouts; progressive trust degradation

Conservative learning strategy

Explicit handling of uncertainty

Designed as a secondary authentication layer, not a replacement

🏗️ System Architecture (Logical Flow)
Keystroke Events
      ↓
Feature Extraction
      ↓
Baseline Comparison
      ↓
Risk Fusion Engine
      ↓
Session Monitor
      ↓
Adaptive Learning Control
      ↓
Authentication Decision

🧪 How It Works (High Level)

Capture typing behavior

Extract behavioral features

Compare against user baseline

Compute risk scores

Fuse risks across signals

Monitor session-level trust

Adapt baseline only when safe

📂 Project Structure
behavioral-auth/
│
├── capture_keystrokes.py       # Keystroke logger
├── extract_features.py         # Feature extraction
├── compare_to_baseline.py      # Risk engine & decision logic
├── session_monitor.py          # Sliding window session analysis
├── samples/                    # Baseline samples
├── test_sample.csv             # Current session sample
├── requirements.txt
└── README.md

⚠️ Limitations

Behavioral patterns vary with fatigue, stress, and environment

Short samples may reduce confidence

Single-modality (keystrokes only)

Not intended as standalone identity proof

These limitations are acknowledged and expected in behavioral biometrics.

🔮 Future Enhancements

Multi-modal fusion (mouse dynamics, scrolling)

Persistent adaptive baselines

Key-pair (digraph) timing analysis

Visualization dashboard

Enterprise policy integration

📌 Key Takeaway

Behavioral authentication is probabilistic, not absolute.
This system models trust over time rather than making one-time identity claims.

👤 Author

Built with a focus on security engineering principles, explainability, and realistic threat modeling.
