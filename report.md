Logs 
# summary table
For performance stats gfs/s = gates * faults * patterns/second
|test|[Github](#github-codespace-specs)|[Local](#local-device)|
|---|---|---|
|c6288<br>SAFSimSimple|1.03e+09 gfp/s|7.68e+08 gfp/s|
|c6288<br>SAFSimIncremental|2.73e+09 gfp/s|1.01e+09 gfp/s|
|c6288<br>SAFSimPPSFP|1.21e+10 gfp/s|4.88e+09 gfp/s|
|[polito-itc99-b15-sky130<br>SAFSimple](#simple-2)||6.05e+08 gfp/s|
[polito-itc99-b15-sky130<br>SAFSimIncremental](#incremental-2)||2.84e+09 gfp/s|
[polito-itc99-b15-sky130<br>SAFSimPPSFP](#ppsfp-2)||3.16e+10 gfp/s|
|c7522<br>SAFSimSimple|7.86e+08 gfp/s|2.95e+08 gfp/s|
|c7522<br>SAFSimIncremental|3.08e+09 gfp/s|1.09e+09 gfp/s|
|c7522<br>SAFSimPPSFP|1.91e+10 gfp/s|6.95e+09 gfp/s|




# Logs 
## C6288.bench on github codespace
### simple 
```
# 0000000.649 W Cuda unavailable. Falling back to pure Python.
# 0000003.321 - loading tests/c6288.bench ...
# 0000003.540 - circuit stats={'node': 4864, 'cell': 2416, 'fork': 2448, 'io': 64, 'line': 7216, 'comb': 2416, 'dff': 0, 'latch': 0, 'seq': 0}
# 0000003.565 - line role stats={'lout': 7216}
# 0000003.661 - fault sites: 6256
# 0000003.661 - uncollapsed stuck-at fault count: 12512
# 0000003.661 - collapsed stuck-at fault count: 7680
# 0000003.668 - FFR count: 1456
# 0000003.787 - simple safsim.sim={name: "tests/c6288.bench", sims: 1024, c_bytes: 928e3}
# 0000032.427 : DS:2121 NO:14 - 28% done 5s elapsed 12s remaining
# 0000039.427 : DS:5015 NO:22 - 66% done 12s elapsed 6s remaining
# 0000045.925 - safsim.timers={startup: 23.64, sim: 18.50, sim_prop: 11.19, sim_eval: 3.05, sim_eval2: 2.20}
# 0000045.925 - fsim performance: 1.03e+09 gfp/s
# 0000045.925 - detected by simulation (collapsed): 7646/7680  -  99.56%
```
### Incremental
```
# 0000000.375 W Cuda unavailable. Falling back to pure Python.
# 0000002.505 - loading tests/c6288.bench ...
# 0000002.613 - circuit stats={'node': 4864, 'cell': 2416, 'fork': 2448, 'io': 64, 'line': 7216, 'comb': 2416, 'dff': 0, 'latch': 0, 'seq': 0}
# 0000002.628 - line role stats={'lout': 7216}
# 0000002.698 - fault sites: 6256
# 0000002.698 - uncollapsed stuck-at fault count: 12512
# 0000002.698 - collapsed stuck-at fault count: 7680
# 0000002.705 - FFR count: 1456
# 0000002.786 - incr safsim.sim={name: "tests/c6288.bench", sims: 1024, c_bytes: 928e3}
# 0000026.600 :  - 74% done 5s elapsed 1s remaining
# 0000028.565 - safsim.timers={startup: 18.81, sim: 6.96, sim_incr_prop: 6.48, sim_incr_reset: 0.30, sim_incr_eval: 0.14, sim_full_prop: 0.00}
# 0000028.565 - fsim performance: 2.73e+09 gfp/s
# 0000028.565 - detected by simulation (collapsed): 7646/7680  -  99.56%
```
### PPSFP
```
# 0000000.325 W Cuda unavailable. Falling back to pure Python.
# 0000002.405 - loading tests/c6288.bench ...
# 0000002.530 - circuit stats={'node': 4864, 'cell': 2416, 'fork': 2448, 'io': 64, 'line': 7216, 'comb': 2416, 'dff': 0, 'latch': 0, 'seq': 0}
# 0000002.542 - line role stats={'lout': 7216}
# 0000002.608 - fault sites: 6256
# 0000002.608 - uncollapsed stuck-at fault count: 12512
# 0000002.608 - collapsed stuck-at fault count: 7680
# 0000002.616 - FFR count: 1456
# 0000002.709 - ppsfp safsim.sim={name: "tests/c6288.bench", sims: 1024, c_bytes: 928e3}
# 0000022.989 - safsim.timers={startup: 18.71, sim: 1.57, sim_ffr_prop: 1.37, sim_ffr_reset: 0.06, sim_sens: 0.05, sim_ffr_out_reduce: 0.03, sim_full_prop: 0.00}
# 0000022.989 - fsim performance: 1.21e+10 gfp/s
# 0000022.989 - detected by simulation (collapsed): 7646/7680  -  99.56%
```
## C6288.bench on local device 
### simple
```
# 0000000.529 W Cuda unavailable. Falling back to pure Python.
# 0000002.747 - loading tests/c6288.bench ...
# 0000002.867 - circuit stats={'node': 4864, 'cell': 2416, 'fork': 2448, 'io': 64, 'line': 7216, 'comb': 2416, 'dff': 0, 'latch': 0, 'seq': 0}
# 0000002.882 - line role stats={'lout': 7216}
# 0000002.964 - fault sites: 6256
# 0000002.964 - uncollapsed stuck-at fault count: 12512
# 0000002.964 - collapsed stuck-at fault count: 7680
# 0000002.973 - FFR count: 1456
# 0000003.062 - simple safsim.sim={name: "tests/c6288.bench", sims: 1024, c_bytes: 928e3}
# 0000033.610 : DS:1503 NO:11 - 20% done 5s elapsed 20s remaining
# 0000040.610 : DS:3601 NO:19 - 47% done 12s elapsed 13s remaining
# 0000050.611 : DS:6791 NO:32 - 89% done 22s elapsed 2s remaining
# 0000053.338 - safsim.timers={startup: 25.55, sim: 24.73, sim_prop: 14.84, sim_eval2: 3.67, sim_eval: 3.52}
# 0000053.338 - fsim performance: 7.68e+08 gfp/s
# 0000053.338 - detected by simulation (collapsed): 7646/7680  -  99.56%
```
### incremental
```
# 0000000.738 W Cuda unavailable. Falling back to pure Python.
# 0000004.677 - loading tests/c6288.bench ...
# 0000004.938 - circuit stats={'node': 4864, 'cell': 2416, 'fork': 2448, 'io': 64, 'line': 7216, 'comb': 2416, 'dff': 0, 'latch': 0, 'seq': 0}
# 0000004.963 - line role stats={'lout': 7216}
# 0000005.107 - fault sites: 6256
# 0000005.107 - uncollapsed stuck-at fault count: 12512
# 0000005.107 - collapsed stuck-at fault count: 7680
# 0000005.122 - FFR count: 1456
# 0000005.295 - incr safsim.sim={name: "tests/c6288.bench", sims: 1024, c_bytes: 928e3}
# 0000052.474 :  - 27% done 5s elapsed 13s remaining
# 0000059.475 :  - 62% done 12s elapsed 7s remaining
# 0000066.304 - safsim.timers={startup: 42.18, sim: 18.83, sim_incr_prop: 17.59, sim_incr_reset: 0.71, sim_incr_eval: 0.41, sim_full_prop: 0.00}
# 0000066.304 - fsim performance: 1.01e+09 gfp/s
# 0000066.304 - detected by simulation (collapsed): 7646/7680  -  99.56%
```
### ppsfp
```
# 0000000.583 W Cuda unavailable. Falling back to pure Python.
# 0000004.596 - loading tests/c6288.bench ...
# 0000004.844 - circuit stats={'node': 4864, 'cell': 2416, 'fork': 2448, 'io': 64, 'line': 7216, 'comb': 2416, 'dff': 0, 'latch': 0, 'seq': 0}
# 0000004.868 - line role stats={'lout': 7216}
# 0000005.013 - fault sites: 6256
# 0000005.013 - uncollapsed stuck-at fault count: 12512
# 0000005.013 - collapsed stuck-at fault count: 7680
# 0000005.027 - FFR count: 1456
# 0000005.219 - ppsfp safsim.sim={name: "tests/c6288.bench", sims: 1024, c_bytes: 928e3}
# 0000048.860 - safsim.timers={startup: 39.74, sim: 3.90, sim_ffr_prop: 3.38, sim_ffr_reset: 0.14, sim_sens: 0.13, sim_ffr_out_reduce: 0.07, sim_full_prop: 0.00}
# 0000048.861 - fsim performance: 4.88e+09 gfp/s
# 0000048.861 - detected by simulation (collapsed): 7646/7680  -  99.56%
```
## polito itc99-b15-sky130 on local
### simple
```
# 0000000.982 W Cuda unavailable. Falling back to pure Python.
# 0001745.539 - loading /nix/store/87l6ny2dcww3514v6wn292yli8ni0iz6-polito-itc99-b15-sky130/b15/nl/b15.nl.v ...
# 0001747.527 - circuit stats={'node': 22209, 'cell': 16576, 'fork': 5633, 'io': 108, 'line': 19876, 'comb': 16044, 'dff': 424, 'output': 70, 'input': 38, 'latch': 0, 'seq': 424}
# 0001747.622 - line role stats={'none': 44, 'lout': 210, 'lseq': 17545, 'lout|lseq': 69, 'clk': 543, 'rst': 1465}
# 0001748.273 - fault sites: 15100
# 0001748.273 - uncollapsed stuck-at fault count: 30200
# 0001748.273 - collapsed stuck-at fault count: 23782
# 0001748.318 - FFR count: 2982
# 0001748.835 - simple safsim.sim={name: "b15", sims: 1024, c_bytes: 3e6}
# 0001787.885 : DS:118 NO:66 - 1% done 5s elapsed 10m40s remaining
# 0001794.910 : DS:311 NO:131 - 2% done 12s elapsed 10m34s remaining
# 0001804.913 : DS:569 NO:240 - 3% done 22s elapsed 10m25s remaining
# 0001819.929 : DS:984 NO:377 - 6% done 37s elapsed 10m10s remaining
# 0001841.956 : DS:1566 NO:606 - 9% done 59s elapsed 9m47s remaining
# 0001874.960 : DS:2444 NO:941 - 14% done 1m32s elapsed 9m14s remaining
# 0001923.985 : DS:3762 NO:1426 - 22% done 2m21s elapsed 8m25s remaining
# 0001996.993 : DS:5691 NO:2184 - 33% done 3m34s elapsed 7m12s remaining
# 0002106.006 : DS:8572 NO:3316 - 50% done 5m23s elapsed 5m23s remaining
# 0002269.025 : DS:12932 NO:4966 - 75% done 8m6s elapsed 2m39s remaining
# 0002428.728 - safsim.timers={sim: 645.86, sim_prop: 202.39, sim_eval: 155.34, sim_eval2: 133.71, startup: 34.03}
# 0002428.728 - fsim performance: 6.05e+08 gfp/s
# 0002428.728 - detected by simulation (collapsed): 17178/23782  -  72.23%
```
### incremental
```
# 0000000.836 W Cuda unavailable. Falling back to pure Python.
# 0000016.056 - loading /nix/store/87l6ny2dcww3514v6wn292yli8ni0iz6-polito-itc99-b15-sky130/b15/nl/b15.nl.v ...
# 0000018.065 - circuit stats={'node': 22209, 'cell': 16576, 'fork': 5633, 'io': 108, 'line': 19876, 'comb': 16044, 'dff': 424, 'output': 70, 'input': 38, 'latch': 0, 'seq': 424}
# 0000018.139 - line role stats={'none': 44, 'lout': 210, 'lseq': 17545, 'lout|lseq': 69, 'clk': 543, 'rst': 1465}
# 0000018.637 - fault sites: 15100
# 0000018.637 - uncollapsed stuck-at fault count: 30200
# 0000018.637 - collapsed stuck-at fault count: 23782
# 0000018.680 - FFR count: 2982
# 0000019.186 - incr safsim.sim={name: "b15", sims: 1024, c_bytes: 3e6}
# 0000060.780 :  - 4% done 5s elapsed 2m12s remaining
# 0000067.783 :  - 9% done 12s elapsed 2m5s remaining
# 0000077.786 :  - 16% done 22s elapsed 1m55s remaining
# 0000092.791 :  - 27% done 37s elapsed 1m40s remaining
# 0000114.791 :  - 43% done 59s elapsed 1m18s remaining
# 0000147.795 :  - 67% done 1m32s elapsed 45s remaining
# 0000193.138 - safsim.timers={sim: 137.36, sim_incr_prop: 128.46, startup: 36.59, sim_incr_reset: 6.61, sim_incr_eval: 1.97, sim_full_prop: 0.01}
# 0000193.138 - fsim performance: 2.84e+09 gfp/s
# 0000193.138 - detected by simulation (collapsed): 17178/23782  -  72.23%
```
### PPSFP
```
# 0000000.587 W Cuda unavailable. Falling back to pure Python.
# 0000004.636 - loading /nix/store/87l6ny2dcww3514v6wn292yli8ni0iz6-polito-itc99-b15-sky130/b15/nl/b15.nl.v ...
# 0000006.500 - circuit stats={'node': 22209, 'cell': 16576, 'fork': 5633, 'io': 108, 'line': 19876, 'comb': 16044, 'dff': 424, 'output': 70, 'input': 38, 'latch': 0, 'seq': 424}
# 0000006.574 - line role stats={'none': 44, 'lout': 210, 'lseq': 17545, 'lout|lseq': 69, 'clk': 543, 'rst': 1465}
# 0000007.193 - fault sites: 15100
# 0000007.193 - uncollapsed stuck-at fault count: 30200
# 0000007.193 - collapsed stuck-at fault count: 23782
# 0000007.236 - FFR count: 2982
# 0000007.751 - ppsfp safsim.sim={name: "b15", sims: 1024, c_bytes: 3e6}
# 0000050.606 :  - 9% done 5s elapsed 48s remaining
# 0000057.607 :  - 74% done 12s elapsed 4s remaining
# 0000057.977 - safsim.timers={startup: 37.85, sim: 12.37, sim_ffr_prop: 10.79, sim_ffr_reset: 0.63, sim_sens: 0.49, sim_ffr_out_reduce: 0.17, sim_full_prop: 0.01}
# 0000057.977 - fsim performance: 3.16e+10 gfp/s
# 0000057.977 - detected by simulation (collapsed): 17178/23782  -  72.23%

```
## C7552.bench on github
### simple
```
# 0000000.529 W Cuda unavailable. Falling back to pure Python.
# 0000003.104 - loading tests/c7552.bench ...
# 0000003.117 W input-output passthrough, renaming output: 241 -> 241~o
# 0000003.283 - circuit stats={'node': 7344, 'cell': 3568, 'fork': 3776, 'io': 315, 'line': 9769, 'comb': 3568, 'dff': 0, 'latch': 0, 'seq': 0}
# 0000003.302 - line role stats={'lout': 9769}
# 0000003.392 - fault sites: 7531
# 0000003.392 - uncollapsed stuck-at fault count: 15062
# 0000003.392 - collapsed stuck-at fault count: 7452
# 0000003.405 - FFR count: 1300
# 0000003.515 - simple safsim.sim={name: "tests/c7552.bench", sims: 1024, c_bytes: 1e6}
# 0000027.768 : DS:1031 NO:74 - 15% done 5s elapsed 28s remaining
# 0000034.773 : DS:2407 NO:190 - 35% done 12s elapsed 22s remaining
# 0000044.774 : DS:4394 NO:364 - 64% done 22s elapsed 12s remaining
# 0000057.411 - safsim.timers={sim: 34.65, startup: 19.25, sim_prop: 12.02, sim_eval: 6.73, sim_eval2: 6.70}
# 0000057.411 - fsim performance: 7.86e+08 gfp/s
# 0000057.411 - detected by simulation (collapsed): 6893/7452  -  92.50%
```
### incremental
```
# 0000000.404 W Cuda unavailable. Falling back to pure Python.
# 0000002.797 - loading tests/c7552.bench ...
# 0000002.811 W input-output passthrough, renaming output: 241 -> 241~o
# 0000002.956 - circuit stats={'node': 7344, 'cell': 3568, 'fork': 3776, 'io': 315, 'line': 9769, 'comb': 3568, 'dff': 0, 'latch': 0, 'seq': 0}
# 0000002.979 - line role stats={'lout': 9769}
# 0000003.093 - fault sites: 7531
# 0000003.093 - uncollapsed stuck-at fault count: 15062
# 0000003.093 - collapsed stuck-at fault count: 7452
# 0000003.107 - FFR count: 1300
# 0000003.255 - incr safsim.sim={name: "tests/c7552.bench", sims: 1024, c_bytes: 1e6}
# 0000028.838 :  - 56% done 5s elapsed 3s remaining
# 0000032.689 - safsim.timers={startup: 20.58, sim: 8.85, sim_incr_prop: 8.22, sim_incr_reset: 0.40, sim_incr_eval: 0.19, sim_full_prop: 0.00}
# 0000032.689 - fsim performance: 3.08e+09 gfp/s
# 0000032.689 - detected by simulation (collapsed): 6893/7452  -  92.50%
```
### PPSFP
```
# 0000000.508 W Cuda unavailable. Falling back to pure Python.
# 0000003.157 - loading tests/c7552.bench ...
# 0000003.168 W input-output passthrough, renaming output: 241 -> 241~o
# 0000003.305 - circuit stats={'node': 7344, 'cell': 3568, 'fork': 3776, 'io': 315, 'line': 9769, 'comb': 3568, 'dff': 0, 'latch': 0, 'seq': 0}
# 0000003.324 - line role stats={'lout': 9769}
# 0000003.415 - fault sites: 7531
# 0000003.415 - uncollapsed stuck-at fault count: 15062
# 0000003.415 - collapsed stuck-at fault count: 7452
# 0000003.427 - FFR count: 1300
# 0000003.548 - ppsfp safsim.sim={name: "tests/c7552.bench", sims: 1024, c_bytes: 1e6}
# 0000024.227 - safsim.timers={startup: 19.26, sim: 1.42, sim_ffr_prop: 1.21, sim_ffr_reset: 0.06, sim_sens: 0.06, sim_ffr_out_reduce: 0.02, sim_full_prop: 0.00}
# 0000024.227 - fsim performance: 1.91e+10 gfp/s
# 0000024.227 - detected by simulation (collapsed): 6893/7452  -  92.50%
```

## C7552.bench on local device
### Simple
```
# 0000000.573 W Cuda unavailable. Falling back to pure Python.
# 0000004.258 - loading tests/c7552.bench ...
# 0000004.277 W input-output passthrough, renaming output: 241 -> 241~o
# 0000004.540 - circuit stats={'node': 7344, 'cell': 3568, 'fork': 3776, 'io': 315, 'line': 9769, 'comb': 3568, 'dff': 0, 'latch': 0, 'seq': 0}
# 0000004.576 - line role stats={'lout': 9769}
# 0000004.756 - fault sites: 7531
# 0000004.756 - uncollapsed stuck-at fault count: 15062
# 0000004.756 - collapsed stuck-at fault count: 7452
# 0000004.780 - FFR count: 1300
# 0000005.010 - simple safsim.sim={name: "tests/c7552.bench", sims: 1024, c_bytes: 1e6}
# 0000048.118 : DS:380 NO:33 - 6% done 5s elapsed 1m25s remaining
# 0000055.120 : DS:900 NO:68 - 13% done 12s elapsed 1m20s remaining
# 0000065.120 : DS:1651 NO:124 - 24% done 22s elapsed 1m10s remaining
# 0000080.121 : DS:2738 NO:226 - 40% done 37s elapsed 56s remaining
# 0000102.123 : DS:4422 NO:366 - 64% done 59s elapsed 32s remaining
# 0000135.129 : DS:6876 NO:557 - 100% done 1m32s elapsed 0s remaining
# 0000135.364 - safsim.timers={sim: 92.25, startup: 38.11, sim_prop: 30.52, sim_eval2: 25.83, sim_eval: 12.92}
# 0000135.364 - fsim performance: 2.95e+08 gfp/s
# 0000135.364 - detected by simulation (collapsed): 6893/7452  -  92.50%
```
### Incremental
```
# 0000001.148 W Cuda unavailable. Falling back to pure Python.
# 0000005.550 - loading tests/c7552.bench ...
# 0000005.573 W input-output passthrough, renaming output: 241 -> 241~o
# 0000005.877 - circuit stats={'node': 7344, 'cell': 3568, 'fork': 3776, 'io': 315, 'line': 9769, 'comb': 3568, 'dff': 0, 'latch': 0, 'seq': 0}
# 0000005.921 - line role stats={'lout': 9769}
# 0000006.132 - fault sites: 7531
# 0000006.132 - uncollapsed stuck-at fault count: 15062
# 0000006.132 - collapsed stuck-at fault count: 7452
# 0000006.157 - FFR count: 1300
# 0000006.412 - incr safsim.sim={name: "tests/c7552.bench", sims: 1024, c_bytes: 1e6}
# 0000053.225 :  - 22% done 5s elapsed 17s remaining
# 0000060.225 :  - 49% done 12s elapsed 12s remaining
# 0000070.226 :  - 87% done 22s elapsed 3s remaining
# 0000073.167 - safsim.timers={startup: 41.81, sim: 24.94, sim_incr_prop: 23.02, sim_incr_reset: 1.21, sim_incr_eval: 0.57, sim_full_prop: 0.00}
# 0000073.167 - fsim performance: 1.09e+09 gfp/s
# 0000073.167 - detected by simulation (collapsed): 6893/7452  -  92.50%
```

### PPSFP
```
# 0000000.733 W Cuda unavailable. Falling back to pure Python.
# 0000004.889 - loading tests/c7552.bench ...
# 0000004.906 W input-output passthrough, renaming output: 241 -> 241~o
# 0000005.206 - circuit stats={'node': 7344, 'cell': 3568, 'fork': 3776, 'io': 315, 'line': 9769, 'comb': 3568, 'dff': 0, 'latch': 0, 'seq': 0}
# 0000005.246 - line role stats={'lout': 9769}
# 0000005.446 - fault sites: 7531
# 0000005.446 - uncollapsed stuck-at fault count: 15062
# 0000005.446 - collapsed stuck-at fault count: 7452
# 0000005.469 - FFR count: 1300
# 0000005.804 - ppsfp safsim.sim={name: "tests/c7552.bench", sims: 1024, c_bytes: 1e6}
# 0000053.717 - safsim.timers={startup: 43.99, sim: 3.92, sim_ffr_prop: 3.41,sim_ffr_reset: 0.15, sim_sens: 0.13, sim_ffr_out_reduce: 0.07, sim_full_prop:0.00}
# 0000053.717 - fsim performance: 6.95e+09 gfp/s
# 0000053.717 - detected by simulation (collapsed): 6893/7452  -  92.50%
```
## Installation ocurrences
cloning repo
```
git clone https://git.vlab.cse.kyutech.ac.jp/stefan/fsim.git
```
update submodule
`git submodule update --init --recursive
`
returned
```
Submodule 'kyupy' (git@git.vlab.cse.kyutech.ac.jp:stefan/kyupy.git) registered for path 'kyupy'
Cloning into '/workspaces/VLSI-Testing/fsim/kyupy'...
The authenticity of host 'git.vlab.cse.kyutech.ac.jp (131.206.36.218)' can't be established.
ED25519 key fingerprint is SHA256:+5XnHikE+Iv+tgYM3n/LaIdy9//VPJkXxETwef6HmU0.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'git.vlab.cse.kyutech.ac.jp' (ED25519) to the list of known hosts.
git@git.vlab.cse.kyutech.ac.jp: Permission denied (publickey).
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
fatal: clone of 'git@git.vlab.cse.kyutech.ac.jp:stefan/kyupy.git' into submodule path '/workspaces/VLSI-Testing/fsim/kyupy' failed
Failed to clone 'kyupy'. Retry scheduled
Cloning into '/workspaces/VLSI-Testing/fsim/kyupy'...
git@git.vlab.cse.kyutech.ac.jp: Permission denied (publickey).
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
fatal: clone of 'git@git.vlab.cse.kyutech.ac.jp:stefan/kyupy.git' into submodule path '/workspaces/VLSI-Testing/fsim/kyupy' failed
Failed to clone 'kyupy' a second time, aborting
```
made changes in [.gitmodules](.gitmodules)
|original|new change|
|---|---|
|`url = git@git.vlab.cse.kyutech.ac.jp:stefan/kyupy.git`|`url = https://git.vlab.cse.kyutech.ac.jp/stefan/kyupy.git`|
ran
```
git submodule sync
git submodule update --init --recursive
```
returned
```
      Built kyupy @ file:///workspaces/VLSI-Testing/fsim/kyupy
Uninstalled 1 package in 4ms
░░░░░░░░░░░░░░░░░░░░ [0/1] Installing wheels...                                              warning: Failed to hardlink files; falling back to full copy. This may lead to degraded performance.
         If the cache and target directories are on different filesystems, hardlinking may not be supported.
         If this is intentional, set `export UV_LINK_MODE=copy` or use `--link-mode=copy` to suppress this warning.
Installed 1 package in 6ms
==================================== test session starts ====================================
platform linux -- Python 3.13.14, pytest-9.1.1, pluggy-1.6.0
rootdir: /workspaces/VLSI-Testing/fsim
configfile: pyproject.toml
plugins: anyio-4.14.0
collected 83 items                                                                          

kyupy/tests/test_atalanta.py ..                                                       [  2%]
kyupy/tests/test_bench.py ..                                                          [  4%]
kyupy/tests/test_circuit.py .......                                                   [ 13%]
kyupy/tests/test_logic.py ....                                                        [ 18%]
kyupy/tests/test_logic_sim.py .................                                       [ 38%]
kyupy/tests/test_sdf.py ....                                                          [ 43%]
kyupy/tests/test_stil.py .                                                            [ 44%]
kyupy/tests/test_verilog.py ....                                                      [ 49%]
kyupy/tests/test_wave_sim.py ......                                                   [ 56%]
tests/test_fault_set.py .......                                                       [ 65%]
tests/test_line_roles.py ....                                                         [ 69%]
tests/test_safsim.py .........................                                        [100%]

===================================== warnings summary ======================================
kyupy/tests/test_stil.py::test_b15
  /workspaces/VLSI-Testing/fsim/kyupy/src/kyupy/stil.py:144: DeprecationWarning: LogicSim is deprecated; use LogicSim2V, LogicSim4V, or LogicSim6V instead.
    sim8v = LogicSim(circuit_resolved, init.shape[-1], m=8)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
========================= 83 passed, 1 warning in 138.27s (0:02:18) =========================
```
### when builiding codespace from scratch 
Run command `curl -LsSf https:/        /astral.sh/uv/install.sh | sh` to ensure uv command run well

### checking nix
to run only inside the directory where flake.nix is located
```
which nix
nix --version

nix flake show

nix develop --command bash -c "echo OK"

uv run main.py polito-itc99-b15-sky130
```

# Github Codespace specs
## CPU
```
Architecture:                            x86_64
CPU op-mode(s):                          32-bit, 64-bit
Address sizes:                           48 bits physical, 48 bits virtual
Byte Order:                              Little Endian
CPU(s):                                  2
On-line CPU(s) list:                     0,1
Vendor ID:                               AuthenticAMD
Model name:                              AMD EPYC 7763 64-Core Processor
CPU family:                              25
Model:                                   1
Thread(s) per core:                      2
Core(s) per socket:                      1
Socket(s):                               1
Stepping:                                1
BogoMIPS:                                4890.85
Flags:                                   fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx mmxext fxsr_opt pdpe1gb rdtscp lm constant_tsc rep_good nopl tsc_reliable nonstop_tsc cpuid extd_apicid aperfmperf tsc_known_freq pni pclmulqdq ssse3 fma cx16 pcid sse4_1 sse4_2 movbe popcnt aes xsave avx f16c rdrand hypervisor lahf_lm cmp_legacy svm cr8_legacy abm sse4a misalignsse 3dnowprefetch osvw topoext vmmcall fsgsbase bmi1 avx2 smep bmi2 erms invpcid rdseed adx smap clflushopt clwb sha_ni xsaveopt xsavec xgetbv1 xsaves user_shstk clzero xsaveerptr rdpru arat npt nrip_save tsc_scale vmcb_clean flushbyasid decodeassists pausefilter pfthreshold v_vmsave_vmload umip vaes vpclmulqdq rdpid fsrm
Virtualization:                          AMD-V
Hypervisor vendor:                       Microsoft
Virtualization type:                     full
L1d cache:                               32 KiB (1 instance)
L1i cache:                               32 KiB (1 instance)
L2 cache:                                512 KiB (1 instance)
L3 cache:                                32 MiB (1 instance)
NUMA node(s):                            1
NUMA node0 CPU(s):                       0,1
Vulnerability Gather data sampling:      Not affected
Vulnerability Indirect target selection: Not affected
Vulnerability Itlb multihit:             Not affected
Vulnerability L1tf:                      Not affected
Vulnerability Mds:                       Not affected
Vulnerability Meltdown:                  Not affected
Vulnerability Mmio stale data:           Not affected
Vulnerability Reg file data sampling:    Not affected
Vulnerability Retbleed:                  Not affected
Vulnerability Spec rstack overflow:      Vulnerable: Safe RET, no microcode
Vulnerability Spec store bypass:         Vulnerable
Vulnerability Spectre v1:                Mitigation; usercopy/swapgs barriers and __user pointer sanitization
Vulnerability Spectre v2:                Mitigation; Retpolines; STIBP disabled; RSB filling; PBRSB-eIBRS Not affected; BHI Not affected
Vulnerability Srbds:                     Not affected
Vulnerability Tsa:                       Vulnerable: Clear CPU buffers attempted, no microcode
Vulnerability Tsx async abort:           Not affected
Vulnerability Vmscape:                   Not affected
```
## LSIPC
```
RESOURCE DESCRIPTION                                              LIMIT USED  USE%
MSGMNI   Number of message queues                                 32000    0 0.00%
MSGMAX   Max size of message (bytes)                                 8K    -     -
MSGMNB   Default max size of queue (bytes)                          16K    -     -
SHMMNI   Shared memory segments                                    4096    0 0.00%
SHMALL   Shared memory pages                       18446744073692774399    0 0.00%
SHMMAX   Max size of shared memory segment (bytes)                  16E    -     -
SHMMIN   Min size of shared memory segment (bytes)                   1B    -     -
SEMMNI   Number of semaphore identifiers                          32000    0 0.00%
SEMMNS   Total number of semaphores                          1024000000    0 0.00%
SEMMSL   Max semaphores per semaphore set.                        32000    -     -
SEMOPM   Max number of operations per semop(2)                      500    -     -
SEMVMX   Semaphore max value                                      32767    -     -
```
# Local device
## OS info
Linux Lenovo 6.17.0-35-generic #35~24.04.1-Ubuntu SMP PREEMPT_DYNAMIC Tue May 26 19:30:42 UTC 2 x86_64 x86_64 x86_64 GNU/Linux

## CPU
```
Architecture:                            x86_64
CPU op-mode(s):                          32-bit, 64-bit
Address sizes:                           39 bits physical, 48 bits virtual
Byte Order:                              Little Endian
CPU(s):                                  8
On-line CPU(s) list:                     0-7
Vendor ID:                               GenuineIntel
Model name:                              Intel(R) Core(TM) i5-8265U CPU @ 1.60GHz
CPU family:                              6
Model:                                   142
Thread(s) per core:                      2
Core(s) per socket:                      4
Socket(s):                               1
Stepping:                                11
CPU(s) scaling MHz:                      28%
CPU max MHz:                             3900.0000
CPU min MHz:                             400.0000
BogoMIPS:                                3600.00
Flags:                                   fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc cpuid aperfmperf pni pclmulqdq dtes64 monitor ds_cpl est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm 3dnowprefetch cpuid_fault epb ssbd ibrs ibpb stibp fsgsbase tsc_adjust sgx bmi1 avx2 smep bmi2 erms invpcid mpx rdseed adx smap clflushopt intel_pt xsaveopt xsavec xgetbv1 xsaves dtherm ida arat pln pts hwp hwp_notify hwp_act_window hwp_epp md_clear flush_l1d arch_capabilities
L1d cache:                               128 KiB (4 instances)
L1i cache:                               128 KiB (4 instances)
L2 cache:                                1 MiB (4 instances)
L3 cache:                                6 MiB (1 instance)
NUMA node(s):                            1
NUMA node0 CPU(s):                       0-7
Vulnerability Gather data sampling:      Vulnerable
Vulnerability Ghostwrite:                Not affected
Vulnerability Indirect target selection: Not affected
Vulnerability Itlb multihit:             KVM: Mitigation: VMX unsupported
Vulnerability L1tf:                      Not affected
Vulnerability Mds:                       Mitigation; Clear CPU buffers; SMT vulnerable
Vulnerability Meltdown:                  Not affected
Vulnerability Mmio stale data:           Mitigation; Clear CPU buffers; SMT vulnerable
Vulnerability Old microcode:             Not affected
Vulnerability Reg file data sampling:    Not affected
Vulnerability Retbleed:                  Mitigation; IBRS
Vulnerability Spec rstack overflow:      Not affected
Vulnerability Spec store bypass:         Mitigation; Speculative Store Bypass disabled via prctl
Vulnerability Spectre v1:                Mitigation; usercopy/swapgs barriers and __user pointer sanitization
Vulnerability Spectre v2:                Mitigation; IBRS; IBPB conditional; STIBP conditional; RSB filling; PBRSB-eIBRS Not affected; BHI Not affected
Vulnerability Srbds:                     Mitigation; Microcode
Vulnerability Tsa:                       Not affected
Vulnerability Tsx async abort:           Not affected
Vulnerability Vmscape:                   Mitigation; IBPB before exit to userspace
```
## Memory
```
RANGE                                  SIZE  STATE REMOVABLE BLOCK
0x0000000000000000-0x000000004fffffff  1.3G online       yes   0-9
0x0000000100000000-0x00000002a7ffffff  6.6G online       yes 32-84

Memory block size:       128M
Total online memory:     7.9G
Total offline memory:      0B
```
## LSIPC
```
RESOURCE DESCRIPTION                                              LIMIT USED  USE%
MSGMNI   Number of message queues                                 32000    0 0.00%
MSGMAX   Max size of message (bytes)                                 8K    -     -
MSGMNB   Default max size of queue (bytes)                          16K    -     -
SHMMNI   Shared memory segments                                    4096    0 0.00%
SHMALL   Shared memory pages                       18446744073692774399    0 0.00%
SHMMAX   Max size of shared memory segment (bytes)                  16E    -     -
SHMMIN   Min size of shared memory segment (bytes)                   1B    -     -
SEMMNI   Number of semaphore identifiers                          32000    0 0.00%
SEMMNS   Total number of semaphores                          1024000000    0 0.00%
SEMMSL   Max semaphores per semaphore set.                        32000    -     -
SEMOPM   Max number of operations per semop(2)                      500    -     -
SEMVMX   Semaphore max value                                      32767    -     -
```