## Executive Summary

- **Objective**: Translate model results into decisions; expose assumptions and sensitivity.
- **Key Finding**: Under winsor 10 90, R² = 0.668, MAE = 18.13.
  Coefficients → const: -62.16, feature_1: 4.00, feature_2: 2.60
- **Sensitivity**: Alternatives → none (R² 0.820, MAE 17.63); winsor 05 95 (R² 0.733, MAE 16.78).
- **Decision**: Winsorize at 10th/90th percentiles — *Why*: Reduces undue leverage from extreme points while retaining overall distribution shape.. 
  Alternatives considered: None; Winsorize at 5th/95th.
  Risks: If extreme values represent true business conditions, we may understate risk/volatility..