| Check | ACOs, No. | Spearman ρ | Median absolute error, % | Slope | Intercept, $ |
|:----------------------------------------|------------:|------------:|----------------:|--------:|------------:|
| Rebuilt 2022 benchmark, all | 101 | 0.94 | 1.6 | 0.944 | 664 |
|     ACOs at the first phase-in step | 62 | 0.93 | 2.0 | 0.917 | 886 |
|     ACOs at the second phase-in step | 39 | 0.96 | 0.9 | 1.017 | −47 |
| Own-spending part (step 1) vs CMS benchmark-year spending | 101 | 0.95 | 1.4 | 0.940 | 676 |

: eTable 1. Validation of the rebuilt benchmark against benchmarks CMS published for regular renewers

::: {.table-notes}
Validation sample: regular renewers whose 2022 benchmarks CMS publishes (101 of 111 eligible; the rest lack either the rebuilt or the published benchmark). Early renewers were excluded from the sample, and the 2022 results file was filtered as it was loaded. Registered pass rule: Spearman correlation at least 0.80 and median absolute percentage error at most 5%; calibration only if the slope of actual on rebuilt fell outside 0.9 to 1.1. Result: passed, no calibration. The error SD of the step-1 check sets the measurement-error SD of the own-spending component, σ = 4.38 pp.
:::
