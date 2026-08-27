{
  "project": {
    "name": "C880 VLSI Fault-Testing Project",
    "benchmark": "ISCAS'85 C880",
    "environment": "Python/Jupyter Notebook",
    "primary_notebook": "test.ipynb",
    "objective": "Evaluate and compare uniform random, weighted random, and future dynamically directed random test-generation strategies for stuck-at fault testing of the C880 combinational circuit.",
    "current_session_completed": true,
    "handoff_date": "2026-08-28"
  },

  "continuation_instructions": {
    "priority": "Continue from the existing notebook and files. Do not rebuild the project architecture from scratch.",
    "do_not_repeat_questions": [
      "Do not ask which benchmark is being used: it is C880.",
      "Do not ask whether the circuit is combinational: C880 is treated as combinational.",
      "Do not ask whether faults are stuck-at faults: SA0 and SA1 are used.",
      "Do not ask whether branch and stem faults are different: they are explicitly different.",
      "Do not ask which fault list defines coverage: the supplied collapsed fault file is the coverage universe.",
      "Do not ask whether good-circuit responses should be cached: they should be cached once per vector.",
      "Do not ask whether 1024 vectors is the initial limit: it is.",
      "Do not ask whether random seed 42 should be used for the initial reproducible experiments: it is.",
      "Do not replace the custom simulator before validating it.",
      "Do not redesign the circuit parser unless an actual correctness problem is found.",
      "Do not silently change PI or PO ordering.",
      "Do not use arbitrary PO integer magnitude as an observability metric without explicitly validating the concept first."
    ],
    "working_style": [
      "Use clear Jupyter cells.",
      "Prefer small testable functions.",
      "Preserve raw experimental data.",
      "Separate simulation from analysis.",
      "Validate optimizations against a simple reference implementation.",
      "Do not overwrite raw experimental results.",
      "Use deterministic seeds for reproducibility.",
      "Clearly distinguish experimental facts from proposed future methods."
    ]
  },

  "authoritative_files": {
    "circuit": "c880.bench",
    "collapsed_faults": "c880_collapsed_faults.txt",
    "scoap": "SCOAP.csv",
    "signal_impact": "signal_impact.csv",
    "po_backtrace": "c880_po_backtrace.json",
    "fanout_stems": "fanout_stems.md"
  },

  "current_file_tree": [
    "SCOAP.csv",
    "aux.md",
    "c880.bench",
    "c880.md",
    "c880_collapsed_faults.txt",
    "c880_collapsed_saf.csv",
    "c880_collapsed_saf.txt",
    "c880_complete_saf.csv",
    "c880_complete_saf.txt",
    "c880_equivalence_collapsed_saf.txt",
    "c880_fault_equivalence_classes.txt",
    "c880_po_backtrace.json",
    "c880_scenario1_coverage_curve.csv",
    "c880_scenario1_fault_simulation.csv",
    "c880_scenario1_fault_summary.csv",
    "c880_scenario1_good_circuit_results.csv",
    "c880_scenario1_po_values.csv",
    "c880_scenario2_coverage_curve.csv",
    "c880_scenario2_fault_simulation.csv",
    "c880_scenario2_fault_summary.csv",
    "c880_scenario2_weighted_vectors.csv",
    "c880_scenario2b_coverage_curve.csv",
    "c880_scenario2b_custom_po_weighted_vectors.csv",
    "c880_scenario2b_fault_simulation.csv",
    "c880_scenario2b_fault_summary.csv",
    "c880_uncollapsed_faults.txt",
    "fanout_stems.md",
    "signal_impact.csv",
    "test.ipynb"
  ],

  "circuit": {
    "name": "C880",
    "inputs": 60,
    "outputs": 26,
    "inverters": 63,
    "gates": 320,
    "gate_breakdown": {
      "AND": 143,
      "NAND": 150,
      "OR": 29,
      "NOR": 61,
      "BUFFER": 26
    },
    "authoritative_definition": "c880.bench",

    "primary_inputs": [
      "1", "8", "13", "17", "26", "29", "36", "42", "51", "55",
      "59", "68", "72", "73", "74", "75", "80", "85", "86", "87",
      "88", "89", "90", "91", "96", "101", "106", "111", "116",
      "121", "126", "130", "135", "138", "143", "146", "149", "152",
      "153", "156", "159", "165", "171", "177", "183", "189", "195",
      "201", "207", "210", "219", "228", "237", "246", "255", "259",
      "260", "261", "267", "268"
    ],

    "primary_outputs": [
      "388", "389", "390", "391", "418", "419", "420", "421", "422",
      "423", "446", "447", "448", "449", "450", "767", "768", "850",
      "863", "864", "865", "866", "874", "878", "879", "880"
    ],

    "ordering_rules": {
      "pi_order": "Use the exact PI order from c880.bench/circuit.inputs.",
      "po_order": "Use the exact PO order from c880.bench/circuit.outputs."
    }
  },

  "fault_model": {
    "type": "single stuck-at",
    "fault_values": [
      "SA0",
      "SA1"
    ],
    "coverage_universe": "c880_collapsed_faults.txt",
    "coverage_denominator": "Number of faults in the supplied collapsed fault file.",
    "do_not_use_uncollapsed_for_standard_coverage": true,

    "fault_examples": [
      "1/SA0",
      "1/SA1",
      "1->269/SA1",
      "101->303/SA0"
    ],

    "stem_fault": {
      "format": "signal/SA0 or signal/SA1",
      "semantics": "The signal itself is globally forced to the stuck value for all downstream uses."
    },

    "branch_fault": {
      "format": "source->destination/SA0 or source->destination/SA1",
      "semantics": "Only the specific source-to-destination connection is forced to the stuck value.",
      "critical_rule": "Never implement a branch fault as a global source-signal fault."
    }
  },

  "fanout_stem_information": {
    "source": "fanout_stems.md",
    "purpose": "Validate and understand branch faults and fanout structure.",
    "examples": {
      "1": ["269", "270", "276", "279", "280", "483"],
      "101": ["303", "304", "334", "506"],
      "106": ["303", "304", "335", "508"],
      "111": ["305", "306", "336", "511"],
      "116": ["305", "306", "338", "513"],
      "121": ["307", "308", "340", "515"],
      "126": ["307", "308", "517"],
      "13": ["269", "270", "280"],
      "130": ["498", "499", "518", "519"]
    }
  },

  "scoap": {
    "file": "SCOAP.csv",
    "columns": [
      "signal",
      "type",
      "CC0",
      "CC1",
      "CO",
      "CC_avg",
      "Testability",
      "is_PI",
      "is_PO"
    ],
    "interpretation": {
      "CC0": "Cost/difficulty to control signal to 0. Lower is easier.",
      "CC1": "Cost/difficulty to control signal to 1. Lower is easier.",
      "CO": "Observability cost. Lower is generally easier to observe.",
      "CC_avg": "Average controllability metric.",
      "Testability": "Combined testability-related metric."
    },
    "usage": "SCOAP is used for weighted generation and may later be used for dynamic fault-directed generation.",
    "warning": "Do not combine raw SCOAP values without normalization and careful consideration of direction."
  },

  "signal_impact": {
    "file": "signal_impact.csv",
    "columns": [
      "rank",
      "signal",
      "gate",
      "level",
      "fanout",
      "PO_count",
      "PO_impact",
      "PO_impact_%",
      "reachable_POs"
    ],
    "meaning": {
      "PO_count": "Number of primary outputs reachable from the signal.",
      "PO_impact": "PO_count divided by total PO count.",
      "PO_impact_%": "PO impact represented as percentage.",
      "reachable_POs": "Explicit list of reachable primary outputs."
    },
    "example": {
      "signal": "1",
      "PO_count": 15,
      "total_POs": 26,
      "PO_impact": 0.5769230769230769,
      "PO_impact_%": 57.692307692307686
    },
    "other_examples": {
      "29": 15,
      "42": 14,
      "59": 13,
      "13": 13
    }
  },

  "implementation_status": {
    "circuit_classes": "implemented",
    "bench_parser": "implemented",
    "topological_evaluation_order": "implemented",
    "circuit_validation": "implemented",
    "logic_evaluation": "implemented",
    "good_circuit_simulation": "implemented",
    "fault_dataclass": "implemented",
    "fault_parser": "implemented",
    "fault_validation": "implemented",
    "stem_fault_injection": "implemented",
    "branch_fault_injection": "implemented",
    "PO_extraction": "implemented",
    "PO_comparison": "implemented",
    "uniform_vector_generation": "implemented",
    "weighted_vector_generation": "implemented",
    "Scenario_1": "completed",
    "Scenario_2": "completed",
    "Scenario_2B": "implemented and experimental outputs exist",
    "Scenario_3": "not implemented",
    "dynamic_fault_directed_generation": "future work"
  },

  "core_functions_already_used": [
    "parse_bench_file",
    "build_evaluation_order",
    "validate_circuit_signals",
    "evaluate_gate",
    "simulate_circuit",
    "simulate_circuit_with_fault",
    "get_po_vector",
    "po_vector_to_string",
    "compare_po_vectors",
    "parse_fault_line",
    "load_fault_file",
    "validate_faults",
    "generate_random_vectors"
  ],

  "fault_representation": {
    "class": "Fault",
    "fields": [
      "fault_id",
      "source",
      "location",
      "fault_type",
      "is_branch"
    ],
    "name_property": "Returns the original fault representation such as 1/SA0 or 1->269/SA1."
  },

  "detection_definition": {
    "rule": "A fault is detected when at least one primary output differs between good and faulty circuit responses.",
    "formal": "detected(f,v)=1 if any PO differs, otherwise 0.",
    "record": [
      "detected",
      "mismatch_count",
      "mismatching_pos"
    ]
  },

  "experimental_parameters": {
    "random_seed": 42,
    "initial_vector_limit": 1024,
    "vector_length": 60,
    "total_primary_outputs": 26,
    "initial_generation": "uniform random",
    "vector_uniqueness": true,
    "initial_coverage_goal": "100% collapsed fault coverage or 1024 vectors, whichever occurs first depending on experiment mode."
  },

  "scenario_1": {
    "name": "Uniform Random",
    "generation": {
      "method": "Uniform random binary vectors",
      "P_0": 0.5,
      "P_1": 0.5,
      "seed": 42,
      "vectors": 1024,
      "unique": true
    },
    "purpose": [
      "Establish baseline fault coverage.",
      "Establish baseline runtime.",
      "Establish baseline detecting-vector behavior.",
      "Establish coverage versus vector count."
    ],
    "outputs": [
      "c880_scenario1_good_circuit_results.csv",
      "c880_scenario1_po_values.csv",
      "c880_scenario1_fault_simulation.csv",
      "c880_scenario1_fault_summary.csv",
      "c880_scenario1_coverage_curve.csv"
    ],
    "status": "completed"
  },

  "scenario_2": {
    "name": "Weighted Random",
    "status": "completed",
    "outputs": [
      "c880_scenario2_weighted_vectors.csv",
      "c880_scenario2_fault_simulation.csv",
      "c880_scenario2_fault_summary.csv",
      "c880_scenario2_coverage_curve.csv"
    ],
    "concept": {
      "basis": [
        "SCOAP",
        "signal/path PO impact"
      ],
      "goal": "Bias PI generation toward values/signals believed to improve testability."
    }
  },

  "scenario_2b": {
    "name": "Custom PO-Weighted Random",
    "status": "experimental_results_exist",
    "outputs": [
      "c880_scenario2b_custom_po_weighted_vectors.csv",
      "c880_scenario2b_fault_simulation.csv",
      "c880_scenario2b_fault_summary.csv",
      "c880_scenario2b_coverage_curve.csv"
    ],
    "vector_format": {
      "columns": [
        "vector_id",
        "input_vector",
        "PI_1",
        "PI_8",
        "PI_13",
        "PI_17",
        "PI_26",
        "PI_29",
        "PI_36",
        "PI_42",
        "PI_51",
        "PI_55",
        "PI_59",
        "PI_68",
        "PI_72",
        "PI_73",
        "PI_74",
        "PI_75",
        "PI_80",
        "PI_85",
        "PI_86",
        "PI_87",
        "PI_88",
        "PI_89",
        "PI_90",
        "PI_91",
        "PI_96",
        "PI_101",
        "PI_106",
        "PI_111",
        "PI_116",
        "PI_121",
        "PI_126",
        "PI_130",
        "PI_135",
        "PI_138",
        "PI_143",
        "PI_146",
        "PI_149",
        "PI_152",
        "PI_153",
        "PI_156",
        "PI_159",
        "PI_165",
        "PI_171",
        "PI_177",
        "PI_183",
        "PI_189",
        "PI_195",
        "PI_201",
        "PI_207",
        "PI_210",
        "PI_219",
        "PI_228",
        "PI_237",
        "PI_246",
        "PI_255",
        "PI_259",
        "PI_260",
        "PI_261",
        "PI_267",
        "PI_268"
      ]
    },
    "important_note": "The existence of Scenario 2B output files means it should be treated as an actual experimental configuration, not merely a future idea. Before drawing conclusions, inspect the generated CSVs and document the exact probability/weight formula used."
  },

  "current_fault_simulation_architecture": {
    "preferred_pattern": "Cache good-circuit response once per vector.",
    "good_simulations": "1024 for a 1024-vector experiment.",
    "fault_simulations": "number_of_vectors × number_of_collapsed_faults",
    "reason": "Avoid recomputing the good circuit separately for every fault.",
    "conceptual_flow": [
      "Generate vector",
      "Simulate good circuit once",
      "Extract 26-bit good PO response",
      "For every fault, simulate faulty circuit",
      "Extract faulty PO response",
      "Compare faulty and good PO responses",
      "Record detection and mismatch information"
    ]
  },

  "fault_simulation_record": {
    "per_vector_fault_fields": [
      "vector_id",
      "fault_id",
      "fault",
      "fault_type",
      "source",
      "location",
      "is_branch",
      "good_po",
      "faulty_po",
      "detected",
      "mismatch_count",
      "mismatching_pos"
    ],
    "fault_level_summary_should_include": [
      "fault_id",
      "fault",
      "fault_type",
      "source",
      "location",
      "is_branch",
      "detected",
      "detecting_vector_count",
      "first_detecting_vector",
      "total_po_mismatches"
    ],
    "optional_extended_statistics": [
      "per-PO mismatch counts",
      "PO_388 mismatch count",
      "PO_389 mismatch count",
      "PO_390 mismatch count",
      "PO_391 mismatch count",
      "PO_418 mismatch count",
      "etc."
    ]
  },

  "coverage": {
    "formula": "detected_collapsed_faults / total_collapsed_faults * 100",
    "denominator": "len(faults) from c880_collapsed_faults.txt",
    "standard_metric": "collapsed fault coverage",
    "do_not_silently_use_uncollapsed_faults": true,
    "coverage_curve": {
      "x": "number of test vectors",
      "y": "collapsed fault coverage percentage"
    }
  },

  "runtime_metrics": {
    "required": [
      "vector_generation_time",
      "good_circuit_simulation_time",
      "fault_simulation_time",
      "total_experiment_time"
    ],
    "preferred_formula": "T_total = T_generation + T_good + T_fault",
    "comparison_requirement": "Use the same hardware/environment when comparing scenarios."
  },

  "fault_dropping": {
    "status": "future optimization",
    "important_conflict": "Fault dropping prevents exact total detecting-vector counts after first detection.",
    "mode_A": {
      "name": "full_statistics",
      "drop_detected_faults": false,
      "purpose": "Exact detecting-vector and PO mismatch statistics."
    },
    "mode_B": {
      "name": "coverage_acceleration",
      "drop_detected_faults": true,
      "purpose": "Fastest route to coverage target."
    }
  },

  "po_weighting": {
    "status": "conceptually interesting but requires careful definition",
    "preferred_candidate": {
      "po_weight": "sum of weights of reachable POs",
      "mismatch_weight": "sum of weights of mismatching POs"
    },
    "recommended_formula": "POWeight(f) = sum(w_p for p in reachable_POs(f))",
    "mismatch_formula": "MismatchWeight(f,v) = sum(w_p for p in mismatching_POs(f,v))",
    "warning": [
      "Do not treat PO binary strings as arbitrary integers unless explicitly justified.",
      "PO numbering/order should not create artificial importance.",
      "One high-order bit should not automatically dominate multiple low-order mismatches."
    ]
  },

  "future_scenario_3": {
    "name": "Dynamic Fault-Directed Random Testing",
    "status": "not implemented",
    "do_not_implement_without_design_review": true,
    "proposed_flow": [
      "Load collapsed fault list",
      "Estimate fault difficulty",
      "Rank faults",
      "Select high-priority faults",
      "Generate targeted random vectors",
      "Simulate",
      "Update remaining fault set",
      "Update historical detection difficulty",
      "Repeat"
    ],
    "possible_priority_factors": [
      "CC0",
      "CC1",
      "CO",
      "reachable_PO_count",
      "PO_impact",
      "historical_detection_difficulty",
      "number_of_vectors_already_attempted"
    ],
    "potential_difficulty_formula": "ActivationCost + ObservationCost",
    "important": "The exact directed-generation algorithm has not been finalized."
  },

  "comparison_plan": {
    "scenarios": [
      "Scenario 1: Uniform Random",
      "Scenario 2: Weighted Random",
      "Scenario 2B: Custom PO-Weighted Random",
      "Scenario 3: Dynamic Fault-Directed Random"
    ],
    "metrics": [
      "vectors generated",
      "vector generation time",
      "good simulation time",
      "fault simulation time",
      "total runtime",
      "final collapsed fault coverage",
      "vectors required to reach target coverage",
      "undetected faults",
      "average detecting vectors per fault",
      "total PO mismatches"
    ],
    "primary_plot": {
      "x": "number of vectors",
      "y": "collapsed fault coverage percentage",
      "purpose": "Compare efficiency of test-generation strategies."
    },
    "secondary_analysis": [
      "fault detection distribution",
      "detecting-vector count per fault",
      "PO mismatch distribution",
      "fault difficulty versus actual detection difficulty",
      "runtime comparison"
    ]
  },

  "statistical_evaluation": {
    "initial_development": {
      "seed": 42,
      "vectors": 1024
    },
    "future_rigorous_experiment": {
      "suggested_seeds": [42, 43, 44, 45, 46],
      "metrics": [
        "mean coverage",
        "standard deviation",
        "mean vectors to target",
        "runtime",
        "confidence intervals where appropriate"
      ],
      "reason": "Random test-generation methods are stochastic, so one seed is appropriate for debugging but insufficient for strong statistical conclusions."
    }
  },

  "validation_requirements": {
    "mandatory": [
      "Validate actual collapsed fault list.",
      "Validate all fault references against circuit.",
      "Manually test at least one stem fault.",
      "Manually test at least one branch fault.",
      "Verify branch fault changes only the intended gate input.",
      "Verify good and faulty PO vectors are compared in identical PO order.",
      "Verify detected means at least one PO differs.",
      "Verify coverage denominator equals number of collapsed faults.",
      "Verify coverage curve is monotonically non-decreasing.",
      "Verify saved CSV row counts match expected vector/fault combinations."
    ],
    "branch_fault_test": {
      "example_fault": "1->269/SA1",
      "requirement": "The injection must affect gate 269's input from signal 1 without globally forcing signal 1 for gates 270, 276, 279, 280, or 483."
    }
  },

  "data_integrity": {
    "raw_results_should_be_preserved": true,
    "processed_summaries_should_not_replace_raw_results": true,
    "PI_order_must_be_stable": true,
    "PO_order_must_be_stable": true,
    "fault_ids_must_be_stable": true,
    "random_seed_should_be_recorded": true,
    "experimental_parameters_should_be_recorded": true
  },

  "known_implementation_issue_from_previous_session": {
    "problem": "A notebook cell attempted to use pi_weight_table before it had been created.",
    "error": "NameError: name 'pi_weight_table' is not defined",
    "cause": "Notebook execution order/state, not necessarily a formula error.",
    "lesson": "Future notebook cells should either create required variables explicitly or verify prerequisite cells have been executed."
  },

  "scenario_2b_previous_vector_example": {
    "file": "c880_scenario2b_custom_po_weighted_vectors.csv",
    "columns": [
      "vector_id",
      "input_vector",
      "PI_1",
      "PI_8",
      "PI_13",
      "PI_17",
      "PI_26",
      "PI_29",
      "PI_36",
      "PI_42",
      "PI_51",
      "PI_55",
      "PI_59",
      "PI_68",
      "PI_72",
      "PI_73",
      "PI_74",
      "PI_75",
      "PI_80",
      "PI_85",
      "PI_86",
      "PI_87",
      "PI_88",
      "PI_89",
      "PI_90",
      "PI_91",
      "PI_96",
      "PI_101",
      "PI_106",
      "PI_111",
      "PI_116",
      "PI_121",
      "PI_126",
      "PI_130",
      "PI_135",
      "PI_138",
      "PI_143",
      "PI_146",
      "PI_149",
      "PI_152",
      "PI_153",
      "PI_156",
      "PI_159",
      "PI_165",
      "PI_171",
      "PI_177",
      "PI_183",
      "PI_189",
      "PI_195",
      "PI_201",
      "PI_207",
      "PI_210",
      "PI_219",
      "PI_228",
      "PI_237",
      "PI_246",
      "PI_255",
      "PI_259",
      "PI_260",
      "PI_261",
      "PI_267",
      "PI_268"
    ],
    "vector_count_expected": 1024,
    "vector_width": 60
  },

  "future_analysis_tasks": [
    "Inspect Scenario 1 CSVs.",
    "Inspect Scenario 2 CSVs.",
    "Inspect Scenario 2B CSVs.",
    "Verify all scenarios use comparable vector counts and fault universes.",
    "Compare coverage curves.",
    "Compare final coverage.",
    "Compare vectors-to-coverage milestones.",
    "Compare runtime.",
    "Compare fault detection distributions.",
    "Compare PO mismatch behavior.",
    "Identify faults that remain difficult across all strategies.",
    "Determine whether Scenario 2B actually improves on Scenario 1 and/or Scenario 2.",
    "Document the exact Scenario 2 and Scenario 2B probability formulas.",
    "Only after baseline comparison, design Scenario 3."
  ],

  "recommended_next_session_start": {
    "first_action": "Inspect the existing Scenario 1, Scenario 2, and Scenario 2B CSV outputs rather than immediately writing new simulation code.",
    "second_action": "Verify that all three experiments used the same collapsed fault universe and comparable vector limits.",
    "third_action": "Generate a consolidated comparison table.",
    "fourth_action": "Generate/inspect coverage curves for Scenario 1, Scenario 2, and Scenario 2B.",
    "fifth_action": "Compare runtime and fault-level detection statistics.",
    "sixth_action": "Determine whether Scenario 2B provides measurable benefit.",
    "seventh_action": "Document the empirical findings.",
    "eighth_action": "Only then consider Scenario 3."
  },

  "expected_comparison_table": {
    "columns": [
      "scenario",
      "vectors_generated",
      "generation_time_s",
      "good_simulation_time_s",
      "fault_simulation_time_s",
      "total_time_s",
      "total_collapsed_faults",
      "detected_faults",
      "undetected_faults",
      "final_coverage_percent",
      "vectors_to_90_percent",
      "vectors_to_95_percent",
      "vectors_to_100_percent",
      "average_detecting_vectors_per_fault",
      "total_po_mismatches"
    ]
  },

  "important_conclusions": [
    "The .bench file is the authoritative circuit definition.",
    "The supplied collapsed fault list is the standard coverage universe.",
    "Stem and branch faults must be modeled differently.",
    "Branch faults must be injected at the specific gate-input connection.",
    "Good-circuit responses should be simulated once per vector and cached.",
    "Fault detection requires at least one PO mismatch.",
    "PO ordering must remain fixed.",
    "PI ordering must remain fixed.",
    "1024 vectors is the initial experimental limit.",
    "Seed 42 is the initial reproducibility seed.",
    "Raw experimental data should be preserved.",
    "Scenario 1 is the uniform baseline.",
    "Scenario 2 is weighted random.",
    "Scenario 2B is a custom PO-weighted experiment with existing output files.",
    "Scenario 3 remains a future design problem and should not be assumed finalized.",
    "The next stage should focus on analyzing and comparing existing experimental evidence before adding another generation algorithm."
  ],

  "handoff_message": "Continue the C880 fault-testing project from the existing test.ipynb and CSV outputs. The fundamental architecture, fault semantics, benchmark definition, coverage definition, PI/PO ordering, and initial experimental methodology are already decided. Do not repeat those questions. First inspect and validate the existing Scenario 1, Scenario 2, and Scenario 2B outputs, compare their coverage/runtime/fault-detection behavior, and document the empirical results. Only after that should the project move toward designing Scenario 3 dynamic fault-directed random testing."
}
