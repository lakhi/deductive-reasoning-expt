from psychopy import visual, core, event
import os
import pandas as pd
from psychopy import data, hardware, logging, prefs, gui
from random import randint
from psychopy.constants import priority
from enum import Enum


class TrialType(Enum):
    IMPOSSIBLE = "impossible"
    GUESS = "guess"
    CORRECT_INF = "correct-inf"


# --- Setup global variables (available in all functions) ---
# device_manager = hardware.DeviceManager()

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
    # show participant info dialog
    dlg = gui.DlgFromDict(
        dictionary=exp_info, sortKeys=False, title=EXPT_NAME, alwaysOnTop=True
    )
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # return expInfo
    return exp_info


def setup_logging(filename):
    # set how much information should be printed to the console / app
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


def setup_window(exp_info):
    win = visual.Window(size=(800, 600), color=[0.5, 0.5, 0.5])
    return win


def run(exp_info, this_exp, win, global_clock=None):
    fam_trials(this_exp, win)
    test_trials(this_exp, win)


def collect_response(trial_onset_time, key_list):
    response = event.waitKeys(keyList=key_list)
    if response:
        return response[0], core.getTime() - trial_onset_time
    else:
        return None, 0


def fam_trials(this_exp, win):
    fam_conditions = data.importConditions("lists/fam_trials_list.csv")
    conditions = pd.DataFrame(fam_conditions)

    high_confidence_objects = conditions[conditions["is_high_confidence_object"] == 1]
    low_confidence_objects = conditions[conditions["is_high_confidence_object"] == 0]

    filtered_conditions = pd.concat(
        [
            high_confidence_objects.sample(n=1).reset_index(drop=True),
            low_confidence_objects.sample(n=1).reset_index(drop=True),
        ],
        ignore_index=True,
    )

    trial_handler = data.TrialHandler2(
        trialList=filtered_conditions.to_dict("records"),
        nReps=1,
        method="sequential",
        seed=None,
    )
    this_exp.addLoop(trial_handler)

    for trial_data in trial_handler:

        fam_video_filename = trial_data["fam_video_filename"]
        print(
            f" ------------------- Current video: {fam_video_filename} ------------------- "
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
        trial_onset_time = core.getTime()
        response, reaction_time = collect_response(trial_onset_time, ["1", "2", "3"])

        # Save data
        save_fam_data(trial_data, fam_video_filename, response, reaction_time)

        core.wait(1.0)

        this_exp.nextEntry()

""" FIX THE FOLLOWING ERROR!
Traceback (most recent call last):
  File "/Users/lakhi/Developer/MEiCogSci/deductive-reasoning-expt/disjunctive_concl.py", line 277, in <module>
    run(EXPT_INFO, this_exp, win, global_clock="float")
  File "/Users/lakhi/Developer/MEiCogSci/deductive-reasoning-expt/disjunctive_concl.py", line 111, in run
    test_trials(this_exp, win)
  File "/Users/lakhi/Developer/MEiCogSci/deductive-reasoning-expt/disjunctive_concl.py", line 193, in test_trials
    impossible_condition_rows.sample(n=1).reset_index(drop=True),
  File "/Applications/PsychoPy.app/Contents/Resources/lib/python3.10/pandas/core/generic.py", line 6118, in sample
    sampled_indices = sample.sample(obj_len, size, replace, weights, rs)
  File "/Applications/PsychoPy.app/Contents/Resources/lib/python3.10/pandas/core/sample.py", line 152, in sample
    return random_state.choice(obj_len, size=size, replace=replace, p=weights).astype(
  File "numpy/random/mtrand.pyx", line 945, in numpy.random.mtrand.RandomState.choice
ValueError: a must be greater than 0 unless no samples are taken
################ Experiment ended with exit code 1 [pid:46371] #################

"""


def test_trials(this_exp, win):
    trial_conditions = data.importConditions("lists/trial-conditions.csv")
    conditions = pd.DataFrame(trial_conditions)

    impossible_condition_rows = conditions[
        conditions["trial_type"] == TrialType.IMPOSSIBLE.value
    ]
    guess_condition_rows = conditions[conditions["trial_type"] == TrialType.GUESS.value]
    correct_inf_condition_rows = conditions[
        conditions["trial_type"] == TrialType.CORRECT_INF.value
    ]

    filtered_conditions = pd.concat(
        [
            impossible_condition_rows.sample(n=1).reset_index(drop=True),
            guess_condition_rows.sample(n=1).reset_index(drop=True),
            correct_inf_condition_rows.sample(n=1).reset_index(drop=True),
        ],
        ignore_index=True,
    )

    # Shuffle the order of the conditions
    filtered_conditions = filtered_conditions.sample(frac=1).reset_index(drop=True)

    trial_handler = data.TrialHandler2(
        trialList=filtered_conditions.to_dict("records"),
        nReps=1,
        method="sequential",
        seed=None,
    )
    this_exp.addLoop(trial_handler)

    for trial_data in trial_handler:

        fam_video_filename = trial_data["filename"]
        print(
            f" ------------------- Current video: {fam_video_filename} ------------------- "
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
        # TODO: replace key event with touch event Y/N image on screen
        trial_onset_time = core.getTime()
        response, reaction_time = collect_response(trial_onset_time, ["Y", "N"])

        # Save trial data
        save_fam_data(trial_data, fam_video_filename, response, reaction_time)

        core.wait(1.0)

        # CONFIDENCE MEAUSREMENT
        # TODO: replace key event with touch event on 1/2/3 STAR image on screen
        trial_onset_time = core.getTime()
        response, reaction_time = collect_response(trial_onset_time, ["1", "2", "3"])

        # Save trial data
        save_fam_data(trial_data, fam_video_filename, response, reaction_time)

        core.wait(1.0)

        this_exp.nextEntry()


def save_fam_data(trial_data, fam_video_filename, response, reaction_time):
    # response_data = {
    #         "participant_id": EXPT_INFO["participant"],
    #         "age": EXPT_INFO["age_yrs_mnths"],
    #         "fam_video_filename": fam_video_filename,
    #         "is_high_confidence_object": trial_data["is_high_confidence_object"],
    #         "child_response": response,
    #         "rt": reaction_time,
    #         "type": "familiarization",
    #     }

    print(
        f" ------------------- Response: {response}, Reaction Time: {reaction_time:.2f} seconds -------------------"
    )


# EXPT_INFO = show_exp_info_dlg(EXPT_INFO)
this_exp = setup_data(EXPT_INFO)
log_file = setup_logging(__this_dir + os.sep + "logs" + os.sep + EXPT_NAME)
win = setup_window(EXPT_INFO)
# setupDevices(expInfo=expInfo, thisExp=thisExp, win=win)
run(EXPT_INFO, this_exp, win, global_clock="float")
# saveData(thisExp=thisExp)
# quit(thisExp=thisExp, win=win)
