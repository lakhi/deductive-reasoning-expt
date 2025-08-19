# Deductive Reasoning Experiment

A PsychoPy-based psychological experiment investigating deductive reasoning abilities through visual stimuli and response collection.

## Overview

This experiment consists of two main phases:
1. **Familiarization trials**: Participants view videos and provide confidence ratings
2. **Test trials**: Participants make accuracy judgments and confidence ratings for different trial types

## Files Structure

```
deductive-reasoning-expt/
├── disjunctive_concl.py           # Main experiment script
├── crossbalancing_list_generation.py  # Generate counterbalanced trial conditions
├── .gitignore                     # Git ignore patterns
├── readme.md                      # This file
├── data/                          # Participant data files (CSV, log, psydat)
├── lists/                         # Condition files
│   ├── fam_trials_list.csv       # Familiarization trial conditions
│   └── trial-conditions.csv      # Test trial conditions
└── logs/                          # Experiment log files
```

## Requirements

- Python 3.7+
- PsychoPy 2024.2.4
- pandas
- Required packages listed in requirements (if available)

## Setup

1. **Install Dependencies**:
   ```bash
   pip install psychopy pandas
   ```

2. **Generate Trial Conditions**:
   ```bash
   python crossbalancing_list_generation.py
   ```
   This creates the `lists/trial-conditions.csv` file with counterbalanced experimental conditions.

3. **Prepare Familiarization Trials**:
   Ensure `lists/fam_trials_list.csv` exists with the required columns:
   - `fam_video_filename`: Path to familiarization videos
   - `is_high_confidence_object`: Binary indicator (0/1)

## Experimental Design

### Factors

The experiment uses a mixed design with:

**Between-subjects factors**:
- `trial_type`: impossible, guess, correct-inf

**Within-subjects factors**:
- `color_layout`: BRG, RGB, GBR
- `empty_box_location`: left, right  
- `open_box_color`: red, green, blue

### Trial Types

1. **Impossible**: not A, therefore X (yellow box)
2. **Guess**: not A, therefore B (any of the two open boxes)
3. **Correct-inf**: not A & B => C

## Running the Experiment

### Quick Start
**Recommended**: Open and run the experiment directly in PsychoPy:
1. Launch PsychoPy
2. Open `disjunctive_concl.py` in the PsychoPy Coder
3. Run the script from within PsychoPy

This approach ensures:
- Console logs are visible for debugging
- No dependency conflicts with PsychoPy installation
- Proper integration with PsychoPy's environment

**Alternative**: Command line execution:
```bash
python disjunctive_concl.py
```

### Configuration

Key constants in `disjunctive_concl.py`:
- `WINDOW_SIZE`: Display resolution (default: 800x600)
- `FAM_RESPONSE_KEYS`: Familiarization response keys ["1", "2", "3"]
- `ACCURACY_RESPONSE_KEYS`: Accuracy judgment keys ["y", "n"]
- `CONFIDENCE_RESPONSE_KEYS`: Confidence rating keys ["1", "2", "3"]

### Participant Information

The experiment collects:
- Participant ID (auto-generated 6-digit number)
- Age (years and months)
- Date and time
- PsychoPy version

## Data Collection

### Familiarization Phase
- Video stimulus presentation
- Confidence ratings (1-3 scale)
- Reaction times
- Object confidence level

### Test Phase
- Video stimulus presentation  
- Accuracy judgments (y/n)
- Confidence ratings (1-3 scale)
- Reaction times for both responses
- Trial condition information

### Output Files

Data is saved in the `data/` directory:
- `{participant_id}_familiarization_data.csv`: Familiarization trial data
- `{participant_id}_trial_data.csv`: Test trial data
- `{participant_id}_{experiment_name}_{date}.csv`: Combined experiment data
- `{participant_id}_{experiment_name}_{date}.log`: Detailed log file
- `{participant_id}_{experiment_name}_{date}.psydat`: PsychoPy data file

## Code Structure

### Main Components

1. **Configuration & Constants**: Centralized settings and file paths
2. **Data Management**: CSV operations with error handling and batch saving
3. **Stimulus Presentation**: Video playback and response collection
4. **Trial Logic**: Condition filtering, sampling, and randomization
5. **Logging**: Comprehensive experiment logging

### Key Functions

- `fam_trials()`: Runs familiarization phase with confidence ratings
- `test_trials()`: Runs test phase with accuracy and confidence judgments  
- `collect_response()`: Handles keyboard input with timing
- `load_conditions_safely()`: Robust condition file loading
- `save_all_data_to_csv()`: Batch data saving for performance

### Design Patterns

- **Error Handling**: Comprehensive exception management
- **Type Hints**: Function signatures with type annotations
- **Constants**: Centralized configuration management
- **Batch Operations**: Optimized data saving to reduce I/O overhead
- **Separation of Concerns**: Modular function design

## Customization

### Adding New Trial Types

1. Update the `TrialType` enum in `disjunctive_concl.py`
2. Modify the factors in `crossbalancing_list_generation.py`
3. Regenerate condition files
4. Update trial filtering logic in `test_trials()`

### Modifying Response Keys

Update the response key constants:
```python
FAM_RESPONSE_KEYS = ["1", "2", "3"]
ACCURACY_RESPONSE_KEYS = ["y", "n"] 
CONFIDENCE_RESPONSE_KEYS = ["1", "2", "3"]
```

### Timing Adjustments

Modify timing constants:
```python
INTER_TRIAL_DELAY = 1.0      # Delay between trials
INTER_RESPONSE_DELAY = 1.0   # Delay between responses
```

## Troubleshooting

### Video Integration

Currently, video playback is commented out for testing. To enable:
1. Uncomment video-related code in `fam_trials()` and `test_trials()`
2. Ensure video files are available in the specified paths
3. Install required video codecs for PsychoPy

### Touch Interface

The code includes TODO comments for implementing touch-based responses:
- Replace keyboard input with touch events
- Implement star rating interface for confidence
- Add Y/N touch buttons for accuracy judgments

## Development Notes

### Performance Optimizations

- Batch data saving eliminates I/O bottlenecks during trials
- Efficient condition filtering and sampling
- Minimal memory footprint with streaming data processing

### Code Quality

- Comprehensive error handling and validation
- Type hints for better code documentation
- Modular design for easy maintenance and testing
- Following PEP 8 style guidelines

## License

MIT License

Copyright (c) 2025 Akshay Lakhi

## Contact

**Akshay Lakhi**  
Email: lakhia92@univie.ac.at

For questions, issues, or contributions to this research project, please feel free to reach out.