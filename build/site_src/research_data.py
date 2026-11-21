"""Research page content. Facts come from the published papers (PDF/DOCX in Zaid's Research\\Publications folder)
and the publisher pages. Numbers are copied from the papers; do not round or invent."""

ME = "Md. Zaid Hossain"

B = {  # uploaded figure blobs (figures from Zaid's own papers; journal papers are CC BY 4.0)
    "wmsd3": "/_blob/3cfbfe082848302dd0bb3e4cb9ed5733",
    "wmsd10": "/_blob/b20c15f4003dabfb2d92fed529dfdffe",
    "array5": "/_blob/226fe7d046c4052974c5d22d5bf2c544",
    "qpain6": "/_blob/b4de2e72a9fa539f7970f8c75084330d",
    "sop2": "/_blob/037bb0ece90d77e32052dc8dfedd59a0",
    "wmsd1": "/_blob/c8245aec7923a6d6cbbb403af653929a",
    "array1": "/_blob/0da6374c6bee1ba8309dee649ad83ccc",
    "qpain1": "/_blob/b362cbabb64e9bdf3ee5be51b481b658",
    "sop1": "/_blob/d29e14b837e75ec50484340fc83ce7b5",
    "video": ("/_blob/3c9114ec1547ea77d65cc2c7f413c784", "/_blob/68d36bdc3ab43a793d0fc66ce81837cd"),  # thesis video + poster (same as Education)
}

# kind: "j" journal, "c" conference
PAPERS = [
    dict(key="wmsd", kind="j", year="2026", tags=["JOURNAL", "Q1", "1ST AUTHOR"],
         title="Leakage-controlled machine learning for work-related musculoskeletal disorder risk classification among garment sewing-machine operators",
         venue="Results in Engineering 32 (2026) 113789 · Elsevier · open access",
         authors="Md. Zaid Hossain, Md. Golam Kibria, Borhan Ul Arif, Shahriar Hasan Ratul",
         doi="10.1016/j.rineng.2026.113789", metric=("9.4", "8.8"),
         q="Can posture scores taken from task videos, together with worker data, sort sewing operators into low, medium and high WMSD risk without the outcome leaking into the model?",
         m="Bilateral task videos of 60 operators, frame-wise joint angles turned into time-weighted RULA scores. A modified Nordic questionnaire gave the SEP-based MSD Index used as the label. Eight classifiers in ten repeats of nested stratified five-fold cross-validation, with all preprocessing and tuning inside the training folds.",
         f="Gradient-boosted trees did best: balanced accuracy 0.940, MCC 0.906. Non-postural variables carried most of the signal. An internal proof of concept that still needs external validation.",
         nums=[("60", "operators"), ("8", "classifiers"), ("0.940", "balanced accuracy"), ("91.7%", "report neck pain")],
         video="video", vidcap="Two-camera recording of a sewing task with joint-angle markers, faces blurred", how="wmsd1", howcap="FIG. 1 · Leakage-controlled WMSD risk-classification workflow", fig="wmsd10", figcap="FIG. 10 · Mean balanced accuracy of the eight classifiers", look="Gradient-boosted trees (top bar) scored highest, but most classifiers are close.",
         abstract="Work-related musculoskeletal disorders (WMSDs) impose a substantial occupational-health burden in labour-intensive industries, while practical tools for systematic workplace risk stratification remain limited. This cross-sectional study developed and internally evaluated a leakage-controlled machine-learning framework using 60 analytical records from Bangladeshi garment sewing-machine operators. Bilateral task videos were processed through a semi-automated workflow to derive time-weighted Rapid Upper Limb Assessment (RULA) scores. A modified Nordic Musculoskeletal Questionnaire was used to calculate the Severity-Exposure-Probability (SEP)-based MSD Index, which defined low-, medium-, and high-risk strata. Eight classifiers were evaluated using ten repeats of nested stratified five-fold cross-validation, with preprocessing and hyperparameter tuning restricted to training partitions. Gradient-boosted trees had the highest observed mean balanced accuracy among the eight classifiers, with repeat-level mean accuracy of 0.950 (95 % CI 0.928 to 0.972), balanced accuracy of 0.940 (0.909 to 0.971), macro-F1 of 0.951 (0.925 to 0.977), and MCC of 0.906 (0.863 to 0.949). Among the Holm-adjusted paired comparisons, only the comparison between gradient-boosted trees and k-nearest neighbours remained significant; the other six comparisons with gradient-boosted trees were not significant. Non-postural variables yielded numerically higher mean performance than the combined feature set (difference not formally tested), while postural variables alone provided moderate discrimination; consequently, an incremental classification benefit from adding dynamic RULA was not demonstrated. These internal proof-of-concept findings, based on a Low-risk class of only six records, require external validation before deployment or population-level performance claims; the present implementation is offline and semi-automated, and a real-machine computational benchmark remains outstanding."),
    dict(key="array", kind="j", year="2026", tags=["JOURNAL", "Q1"],
         title="A simulation-based context-aware multimodal ML framework for proactive worker safety monitoring in resource-constrained factories",
         venue="Array 31 (2026) 101198 · Elsevier · open access",
         authors="Nasif Morshed, Md. Saiful Islam Seam, Md. Zaid Hossain, Md Al Amin",
         doi="10.1016/j.array.2026.101198", metric=("5.3", "10.1"),
         q="Can a low-cost design that joins several kinds of factory data flag unsafe situations early, in factories with little money for safety technology?",
         m="One decision design joins environmental sensors, camera-based PPE detection (YOLOv8, proposed), RFID zone tracking and incident history, with a rule table and a supervisor review step. Six classifiers on 300 simulated observations, cross-validation plus a held-out test, and an ablation by data source.",
         f="The classifiers learned the expert safety policy well: Random Forest and XGBoost both reached 0.833 accuracy on the held-out set. Sensor and zone data carried most of the signal. Real-factory validation is the next step.",
         nums=[("300", "simulated observations"), ("6", "classifiers"), ("0.833", "held-out accuracy"), ("4", "data sources")],
         how="array1", howcap="FIG. 1 · Workflow of the proposed multimodal safety monitoring framework", fig="array5", figcap="FIG. 5 · Ablation by data source: weighted F1 for each sensor mix", look="Sensor and zone data (fifth bar) are almost as good as all data together (green).",
         abstract="Occupational safety monitoring in resource-constrained factories remains dominated by manual and reactive inspection. This study presents a simulation-based proof-of-concept evaluation of a context-aware safety decision architecture that integrates three sensing modalities (environmental measurements, proposed image-based PPE detection, and RFID zone tracking) together with incident-history context, an explicit rule table, and a designed human-in-the-loop (HITL) review layer. The evaluation uses 300 simulated observations. Because the target classes were generated by the same expert-defined rule table that maps sensor risk, PPE status, and zone level to No Alert, Warning, or High Risk, the supervised classifiers approximate that policy rather than predict independently observed accidents. Six classifiers were compared using stratified cross-validation and a held-out test partition. At the original seed-42 split, Random Forest and XGBoost produced identical held-out results (accuracy and weighted F1 = 0.833; macro F1 = 0.829; balanced accuracy = 0.800; Cohen's kappa = 0.718; High-Risk recall = 0.700). A supplementary reconstructed fixed-dataset analysis across seeds 0, 1, 42, 123, and 999 yielded held-out weighted F1 of 0.836±0.022 for Random Forest and 0.859±0.027 for XGBoost. Across five seed-level cross-validation means, the Full and Sensor + Zone configurations differed by only 0.003±0.012 weighted F1, with no significant difference detected in an exploratory paired test (W = 5.0, p = 0.625). The proposed YOLOv8 and HITL components were not empirically validated. The results therefore demonstrate policy-approximation feasibility under simulation and identify sensor and zone information as the dominant contributors, while real-factory validation remains essential."),
    dict(key="qpain", kind="c", year="2025", tags=["CONFERENCE", "IEEE", "1ST AUTHOR"],
         title="AI-Driven Early Warning System for Industrial Shutdowns on High-Risk Pollution Days: A Case Study on Dhaka Air Quality",
         venue="2025 IEEE QPAIN · BAUST, Saidpur, Bangladesh · 31 Jul to 2 Aug 2025",
         authors="Md. Zaid Hossain, Nasif Morshed, Md. Saiful Islam Seam",
         doi="10.1109/QPAIN66474.2025.11171883", metric=None,
         q="Can machine learning predict high-risk pollution days in Dhaka early enough for authorities to plan industrial shutdowns?",
         m="Air-quality data from 2000 to 2025 (SO₂, NO₂, O₃, CO, PM2.5, PM10, temperature, humidity). Seven models built and compared in RapidMiner Studio with 10-fold cross-validation.",
         f="Random Forest was best, with 98.34% accuracy and R² 0.921. Pollution peaks in the cooler, drier months; the forecast feeds an industry-specific shutdown protocol.",
         nums=[("25", "years of data"), ("7", "models"), ("98.34%", "accuracy"), ("0.921", "R²")],
         how="qpain1", howcap="FIG. 1 · Workflow diagram", fig="qpain6", figcap="FIG. 6 · Accuracy (%) of the seven models", look="Random Forest and Gradient Boosted Trees score highest, at 98.34%.",
         abstract="Rapid urbanization and industrial activities, coupled with a failure by policymakers and governance agencies to address air pollution, has led to a pressing yet urgent and proactive need for immediate action to tackle the continuous air pollution crisis in Dhaka. The goal of this study is to create an AI-based early warning system to predict high risk pollution days and recommend industrial shutdowns as a measure of lowering exposure. With a dataset spanning 2000 to 2025, the seven machine learning models implement data points including SO₂, NO₂, O₃, CO, PM2.5, PM10, Temperature, and Humidity on Decision Tree, Random Forest, Gradient Boosted Trees, k-NN, AdaBoost, Support Vector Machine (SVM), and Linear Regression. RapidMiner Studio was chosen to perform a 10-fold cross validation process to evaluate model. The best performance was achieved by Random Forest model with accuracy of 98.34% and R² value of 0.921 among all. The reason for the pollution peak were the cooler and drier months. The proposed system delivers authorities a practical solution to back their public health risk reduction decisions using industry-specific shutdown protocols. The solution brings its technology to intense air quality challenges in urban areas through the use of predictive insights for generating policy-triggered action plans."),
    dict(key="sop", kind="c", year="2025", tags=["CONFERENCE", "IEOM"],
         title="SOP-Driven Improvements in Efficiency, Quality and On-Time Delivery: Evidence from Bangladesh's RMG Sewing Industry",
         venue="8th IEOM Bangladesh International Conference · Dhaka · 20 to 21 Dec 2025 · IEOM Society",
         authors="Md. Tanjid Hossen Irfan, Md. Ismail Hossain, Md. Zaid Hossain, Nasif Morshed, Md. Saiful Islam Seam",
         doi="10.46254/BA08.20250288", metric=None, pdf="https://ieomsociety.org/proceedings/bangladesh2025/288.pdf",
         q="What changes on the sewing floor of a large Bangladeshi RMG factory when the lines run on standard operating procedures alone, without a wider quality framework?",
         m="One month before (July) and one month after (August) SOP go-live on the sewing lines. Daily efficiency, performance, non-production time (NPT), defects per hundred units (DHU) and handover on time (HOT), tested at p &lt; 0.05.",
         f="Line efficiency rose from 67.9% to 77.9%, NPT fell from 32% to 22.05%, DHU from 9.96% to 5.21%, and handover on time reached 100%. One factory and the sewing section only, with no control group.",
         nums=[("67.9 → 77.9%", "line efficiency"), ("32 → 22%", "non-production time"), ("9.96 → 5.21%", "DHU"), ("100%", "handover on time")],
         how="sop1", howcap="FIG. 1 · Factory process flow; the study covers the sewing stage", fig="sop2", figcap="FIG. 2 · Daily line efficiency before and after SOP go-live", look="Look at the step up on the day SOPs started, and how it stays up.",
         abstract=None),
]

ONGOING = [
    dict(tag="MANUSCRIPT IN PREPARATION", title="Explainable machine learning for cardiovascular disease prediction: a systematic multi-paradigm benchmark with cross-method feature importance analysis",
         who="Md. Shahriar Islam Ratul, Md. Zaid Hossain",
         text="Fifteen models from five families (classical ML, gradient boosting, stacking, tabular deep learning, self-supervised) trained on one cleaned cohort of 68,534 records, compared with bootstrap confidence intervals and DeLong tests, and explained with five feature-importance methods.",
         nums=[("15", "models"), ("68,534", "records"), ("0.80", "best AUC"), ("5", "explanation methods")],
         note="Performance levels off near AUC 0.80, which points to a limit in the data rather than in model complexity. Systolic blood pressure and age matter most across every method."),
]

# ---- real site: the lists above are replaced by content/*.yml (build/content_io.py) ----
import content_io as _C
globals().update(_C.load_research())
