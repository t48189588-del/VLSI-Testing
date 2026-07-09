Logs 

# Logs 

## C6288.bench on github codespace
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
## C6288.bench on local device 
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

## C67552.bench on local device
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