from psychopy import visual, core, event
import os
import pandas as pd
from psychopy import data, logging, gui
from random import randint
from psychopy.constants import priority
from enum import Enum


class TrialType(Enum):
    IMPOSSIBLE = "impossible"
    GUESS = "guess"
    CORRECT_INF = "correct-inf"


# Constants and Configuration
WINDOW_SIZE = (800, 600)
WINDOW_COLOR = [0.5, 0.5, 0.5]
DATA_DIR = "data"
LISTS_DIR = "lists"
LOGS_DIR = "logs"

# Response keys
FAM_RESPONSE_KEYS = ["1", "2", "3"]
ACCURACY_RESPONSE_KEYS = ["y", "n"]
CONFIDENCE_RESPONSE_KEYS = ["1", "2", "3"]

# Timing constants
INTER_TRIAL_DELAY = 1.0
INTER_RESPONSE_DELAY = 1.0
DECIMAL_PRECISION = 2

# File paths
FAM_TRIALS_FILE = os.path.join(LISTS_DIR, "fam_trials_list.csv")
TRIAL_CONDITIONS_FILE = os.path.join(LISTS_DIR, "trial-conditions.csv")

# ensure that relative paths start from the same directory as this script
__this_dir = os.path.dirname(os.path.abspath(__file__))
PSYCHOPY_VERSION = "2024.2.4"
EXPT_NAME = "DisjunctiveConclusion"
EXPT_INFO = {
    "participant": f"{randint(0, 999999):06.0f}",
    "age_yrs_mnths": "",
    "date|hid": data.getDateStr(),
    "expName|hid": EXPT_NAME,
    "psychopyVersion|hid": PSYCHOPY_VERSION,
}


def show_exp_info_dlg(exp_info):
    dlg = gui.DlgFromDict(
        dictionary=exp_info, sortKeys=False, title=EXPT_NAME, alwaysOnTop=True
    )
    if dlg.OK == False:
        core.quit()  # user pressed cancel

    return exp_info


def load_conditions_safely(filename):
    """Load conditions file with error handling."""
    try:
        conditions = data.importConditions(filename)
        if not conditions:
            raise ValueError(f"No conditions found in {filename}")
        return pd.DataFrame(conditions)
    except FileNotFoundError:
        raise FileNotFoundError(f"Conditions file not found: {filename}")
    except Exception as e:
        raise RuntimeError(f"Error loading conditions from {filename}: {str(e)}")


def validate_trial_data(trial_data, required_fields):
    """Validate that trial data contains required fields."""
    missing_fields = [field for field in required_fields if field not in trial_data]
    if missing_fields:
        raise ValueError(f"Missing required fields in trial data: {missing_fields}")


def create_data_directory():
    """Ensure data directory exists."""
    os.makedirs(DATA_DIR, exist_ok=True)


def get_filename(participant_id, file_type):
    """Generate standardized filenames."""
    return os.path.join(DATA_DIR, f"{participant_id}_{file_type}_data.csv")


def save_to_csv(data, filename):
    """Generic CSV saving function."""
    create_data_directory()
    df = pd.DataFrame([data])

    if os.path.exists(filename):
        df.to_csv(filename, mode="a", header=False, index=False)
    else:
        df.to_csv(filename, mode="w", header=True, index=False)


def save_all_data_to_csv(data_list, filename):
    """Save all data from list to CSV in one operation."""
    create_data_directory()
    df = pd.DataFrame(data_list)

    if os.path.exists(filename):
        df.to_csv(filename, mode="a", header=False, index=False)
    else:
        df.to_csv(filename, mode="w", header=True, index=False)


def setup_logging(filename):
    log_file = logging.LogFile(filename + ".log")
    logging.console.setLevel(logging.WARNING)
    log_file.setLevel(logging.getLevel(logging.DEBUG))

    return log_file


def setup_data(exp_info, data_dir=None):
    """
    Make an ExperimentHandler to handle trials and saving.

    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about
        where to save it to.
    """
    # remove dialog-specific syntax from expInfo
    for key, val in exp_info.copy().items():
        new_key, _ = data.utils.parsePipeSyntax(key)
        exp_info[new_key] = exp_info.pop(key)

    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if data_dir is None:
        data_dir = __this_dir

    filename = (
        f"data/{str(exp_info['participant'])}_{EXPT_NAME}_{str(exp_info['date'])}"
    )

    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        data_dir = os.path.commonprefix([data_dir, filename])
        filename = os.path.relpath(filename, data_dir)

    # an ExperimentHandler isn't essential but helps with data saving
    this_exp = data.ExperimentHandler(
        name=EXPT_NAME,
        version="",
        extraInfo=exp_info,
        runtimeInfo=None,
        originPath="/Users/lakhi/Developer/MEiCogSci/deductive-reasoning-expt/experiment_lastrun.py",
        savePickle=True,
        saveWideText=True,
        dataFileName=data_dir + os.sep + filename,
        sortColumns="time",
    )
    this_exp.setPriority("thisRow.t", priority.CRITICAL)
    this_exp.setPriority("expName", priority.LOW)
    # return experiment handler
    return this_exp


def setup_window():
    win = visual.Window(size=WINDOW_SIZE, color=WINDOW_COLOR)
    return win


def run(this_exp, win):
    fam_trials(this_exp, win)
    test_trials(this_exp, win)


def collect_response(key_list: list, timeout: float = None) -> tuple:
    """
    Collect keyboard response from participant.

    Args:
        key_list: List of valid response keys
        timeout: Maximum wait time in seconds (None for no timeout)

    Returns:
        tuple: (response_key, reaction_time) or (None, 0) if no response
    """
    trial_onset_time = core.getTime()

    if timeout is None:
        response = event.waitKeys(keyList=key_list)
    else:
        response = event.waitKeys(keyList=key_list, maxWait=timeout)

    if response:
        return response[0], core.getTime() - trial_onset_time
    return None, 0


def filter_and_sample_conditions(
    conditions_df: pd.DataFrame, filter_dict: dict, n_samples: int = 1
) -> pd.DataFrame:
    """Filter conditions and sample n rows."""
    filtered = conditions_df.copy()

    for key, value in filter_dict.items():
        filtered = filtered[filtered[key] == value]

    if len(filtered) < n_samples:
        raise ValueError(
            f"Not enough rows matching filter criteria. Found {len(filtered)}, need {n_samples}"
        )

    return filtered.sample(n=n_samples).reset_index(drop=True)


def create_trial_handler(
    conditions: pd.DataFrame, experiment_handler
) -> data.TrialHandler2:
    """Create and register trial handler."""
    trial_handler = data.TrialHandler2(
        trialList=conditions.to_dict("records"),
        nReps=1,
        method="sequential",
        seed=None,
    )
    experiment_handler.addLoop(trial_handler)
    return trial_handler


def fam_trials(this_exp, win):
    conditions = load_conditions_safely(FAM_TRIALS_FILE)

    high_confidence_objects = filter_and_sample_conditions(
        conditions, {"is_high_confidence_object": 1}, n_samples=1
    )
    low_confidence_objects = filter_and_sample_conditions(
        conditions, {"is_high_confidence_object": 0}, n_samples=1
    )

    filtered_conditions = pd.concat(
        [high_confidence_objects, low_confidence_objects],
        ignore_index=True,
    )

    trial_handler = create_trial_handler(filtered_conditions, this_exp)
    this_exp.addLoop(trial_handler)

    # Collect all trial data in a list
    fam_data_list = []

    for trial_data in trial_handler:

        fam_video_filename = trial_data["fam_video_filename"]
        print(
            f" ------------------- Current FAM video: {fam_video_filename} ------------------- "
        )

        # video = visual.MovieStim(
        #     win, filename=fam_video_filename, movieLib='ffpyplayer',
        #     loop=False, volume=1.0, noAudio=False,
        #     pos=(0, 0), units=win.units,
        #     ori=0.0, anchor='center', opacity=None, contrast=1.0,
        # )
        # video.play()

        # while not video.isFinished:
        #     video.draw()
        #     win.flip()

        # video.stop()
        # video.unload()

        # TODO: replace key event with touch event on 1/2/3 STAR image on screen
        print(" ------------------- PRESS 1/2/3 ------------------- ")
        response, reaction_time = collect_response(FAM_RESPONSE_KEYS)

        # Collect data instead of saving immediately
        response_data = {
            "participant_id": EXPT_INFO["participant"],
            "age": EXPT_INFO["age_yrs_mnths"],
            "fam_video_filename": fam_video_filename,
            "is_high_confidence_object": trial_data["is_high_confidence_object"],
            "child_response": response,
            "rt": round(reaction_time, DECIMAL_PRECISION),
            "type": "familiarization",
        }
        fam_data_list.append(response_data)

        print(
            f" ------------------- Response: {response}, Reaction Time: {reaction_time:.2f} seconds -------------------"
        )

        core.wait(INTER_TRIAL_DELAY)
        this_exp.nextEntry()

    # Save all data at once
    if fam_data_list:
        filename = get_filename(EXPT_INFO["participant"], "familiarization")
        save_all_data_to_csv(fam_data_list, filename)


def test_trials(this_exp, win):
    conditions = load_conditions_safely(TRIAL_CONDITIONS_FILE)

    impossible_condition_rows = filter_and_sample_conditions(
        conditions, {"trial_type": TrialType.IMPOSSIBLE.value}, n_samples=1
    )
    guess_condition_rows = filter_and_sample_conditions(
        conditions, {"trial_type": TrialType.GUESS.value}, n_samples=1
    )
    correct_inf_condition_rows = filter_and_sample_conditions(
        conditions, {"trial_type": TrialType.CORRECT_INF.value}, n_samples=1
    )

    filtered_conditions = pd.concat(
        [impossible_condition_rows, guess_condition_rows, correct_inf_condition_rows],
        ignore_index=True,
    )

    # Shuffle the order of the conditions
    filtered_conditions = filtered_conditions.sample(frac=1).reset_index(drop=True)

    trial_handler = create_trial_handler(filtered_conditions, this_exp)

    # Collect all trial data in a list
    trial_data_list = []

    for trial_data in trial_handler:

        fam_video_filename = trial_data["filename"]
        print(
            f" ------------------- Current TRIAL video: {fam_video_filename} ------------------- "
        )

        # video = visual.MovieStim(
        #     win, filename=fam_video_filename, movieLib='ffpyplayer',
        #     loop=False, volume=1.0, noAudio=False,
        #     pos=(0, 0), units=win.units,
        #     ori=0.0, anchor='center', opacity=None, contrast=1.0,
        # )
        # video.play()

        # while not video.isFinished:
        #     video.draw()
        #     win.flip()

        # video.stop()
        # video.unload()

        # ACCURACY MEAUSREMENT
        print(" ------------------- PRESS y/n ------------------- ")

        # TODO: replace key event with touch event Y/N image on screen
        accuracy_response, accuracy_rt = collect_response(ACCURACY_RESPONSE_KEYS)

        core.wait(INTER_RESPONSE_DELAY)

        # CONFIDENCE MEAUSREMENT
        print(" ------------------- PRESS 1/2/3 ------------------- ")

        # TODO: replace key event with touch event on 1/2/3 STAR image on screen
        confidence_response, confidence_rt = collect_response(CONFIDENCE_RESPONSE_KEYS)

        # Collect data instead of saving immediately
        response_data = {
            "participant_id": EXPT_INFO["participant"],
            "age": EXPT_INFO["age_yrs_mnths"],
            "trial_video_filename": fam_video_filename,
            "color_layout": trial_data["color_layout"],
            "empty_box_location": trial_data["empty_box_location"],
            "open_box_color": trial_data["open_box_color"],
            "trial_type": trial_data["trial_type"],
            "accuracy_response": accuracy_response,
            "accuracy_rt": round(accuracy_rt, DECIMAL_PRECISION),
            "confidence_response": confidence_response,
            "confidence_rt": round(confidence_rt, DECIMAL_PRECISION),
            "type": "test_trial",
        }
        trial_data_list.append(response_data)

        print(
            f" ------------------- Accuracy: {accuracy_response} (RT: {accuracy_rt:.2f}s), Confidence: {confidence_response} (RT: {confidence_rt:.2f}s) -------------------"
        )

        core.wait(INTER_TRIAL_DELAY)
        this_exp.nextEntry()

    # Save all data at once
    if trial_data_list:
        filename = get_filename(EXPT_INFO["participant"], "trial")
        save_all_data_to_csv(trial_data_list, filename)


# Main execution
exp_info = EXPT_INFO  # Uncomment show_exp_info_dlg(EXPT_INFO) for production
this_exp = setup_data(exp_info)
log_file = setup_logging(os.path.join(__this_dir, LOGS_DIR, EXPT_NAME))
win = setup_window()
run(this_exp, win)
core.quit()
