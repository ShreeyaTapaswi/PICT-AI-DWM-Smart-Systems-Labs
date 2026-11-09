# PICT Coursework Labs: AI, Data Warehousing & Mining, Smart & Sustainable Systems

Lab projects from my coursework at Pune Institute of Computer Technology (PICT), covering classical AI, data mining and data warehousing, and streaming analytics.

**Tech stack:** Python, scikit-learn, pandas, NumPy, Streamlit, Apache Kafka, Apache Spark

**Live demo (AI projects):** `<add your deployed link here>`

---

## Projects at a glance

| Subject | Project | Techniques | Folder |
|---|---|---|---|
| AI | Sliding-tile puzzle (N×N) | Informed search (A*, heuristics) | [`AI/01_sliding_tile_puzzle`](AI/01_sliding_tile_puzzle) |
| AI | Tic-Tac-Toe agent | Minimax, Alpha-Beta pruning | [`AI/02_tictactoe_minimax_alphabeta`](AI/02_tictactoe_minimax_alphabeta) |
| AI | Indian-state map colouring | Constraint Satisfaction Problem (CSP) | [`AI/03_map_colouring_csp`](AI/03_map_colouring_csp) |
| AI | Reinforcement-learning game agent | Q-learning | [`AI/04_rl_game_agent`](AI/04_rl_game_agent) |
| DWM | Loan-approval classifier | Decision Tree, Naïve Bayes, SVM, KNN | [`DWM/01_loan_approval_classifiers`](DWM/01_loan_approval_classifiers) |
| DWM | Association rule mining | Apriori (support 40%, confidence 60%) | [`DWM/02_apriori_rules`](DWM/02_apriori_rules) |
| DWM | Retail data cube and sales data mart | ETL, OLAP | [`DWM/03_data_cube_data_mart_etl_olap`](DWM/03_data_cube_data_mart_etl_olap) |
| Smart Systems | Crop-yield prediction | ML on soil and weather data | [`Smart_Systems/01_crop_yield_prediction`](Smart_Systems/01_crop_yield_prediction) |
| Smart Systems | Energy and water consumption forecasting | Linear regression | [`Smart_Systems/02_energy_water_forecasting`](Smart_Systems/02_energy_water_forecasting) |
| Smart Systems | Real-time sensor data processing | Apache Kafka (streaming), Apache Spark (processing) | [`Smart_Systems/03_kafka_spark_streaming`](Smart_Systems/03_kafka_spark_streaming) |

---

## 1. Artificial Intelligence

- **Sliding-tile puzzle:** solves an N×N puzzle using informed search with admissible heuristics (e.g. Manhattan distance).
- **Tic-Tac-Toe:** an unbeatable agent using Minimax, with Alpha-Beta pruning to cut down the nodes explored.
- **Map colouring:** colours the Indian states so that no two neighbouring states share a colour, modelled as a CSP and solved with backtracking.
- **RL game agent:** an agent that learns to play through reward-based training.

## 2. Data Warehousing & Mining

- **Loan approval:** compares Decision Tree, Naïve Bayes, SVM and KNN on accuracy and other metrics.

  | Model | Accuracy |
  |---|---|
  | Decision Tree | `<fill in>` |
  | Naïve Bayes | `<fill in>` |
  | SVM | `<fill in>` |
  | KNN | `<fill in>` |

- **Apriori:** frequent itemsets and association rules with minimum support 40% and minimum confidence 60%.
- **Data cube and data mart:** a retail data cube and sales data mart, with an ETL process and OLAP operations (roll-up, drill-down, slice, dice).

## 3. Smart & Sustainable Systems

- **Crop-yield prediction:** predicts yield from soil and weather features.
- **Consumption forecasting:** linear-regression forecasts of energy and water usage.
- **Streaming pipeline:** simulated sensor data is published to **Apache Kafka** and processed in real time with **Apache Spark**.

---

## Repository structure

```
PICT-AI-DWM-Smart-Systems-Labs/
├── AI/
│   ├── 01_sliding_tile_puzzle/
│   ├── 02_tictactoe_minimax_alphabeta/
│   ├── 03_map_colouring_csp/
│   └── 04_rl_game_agent/
├── DWM/
│   ├── 01_loan_approval_classifiers/
│   ├── 02_apriori_rules/
│   └── 03_data_cube_data_mart_etl_olap/
├── Smart_Systems/
│   ├── 01_crop_yield_prediction/
│   ├── 02_energy_water_forecasting/
│   └── 03_kafka_spark_streaming/
├── requirements.txt
└── README.md
```

## Getting started

```bash
git clone https://github.com/ShreeyaTapaswi/PICT-AI-DWM-Smart-Systems-Labs.git
cd PICT-AI-DWM-Smart-Systems-Labs
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Run any project from its folder, for example:

```bash
cd AI/02_tictactoe_minimax_alphabeta
python main.py
```

### Running the streaming project

Requires Java, Apache Kafka and Apache Spark installed locally.

1. Start ZooKeeper and the Kafka broker.
2. Create the topic: `kafka-topics.sh --create --topic sensor-data --bootstrap-server localhost:9092`
3. Start the producer (simulated sensors): `python producer.py`
4. Start the Spark consumer: `spark-submit consumer.py`

Adjust file and topic names to match your code.

## Author

**Shreeya Tapaswi**, PICT, Pune
[GitHub](https://github.com/ShreeyaTapaswi)
