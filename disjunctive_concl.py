from psychopy import visual, core
import os
import pandas as pd
from psychopy import data, hardware, logging, prefs, gui
from random import randint
from psychopy.constants import priority

# --- Setup global variables (available in all functions) ---
# device_manager = hardware.DeviceManager()

# ensure that relative paths start from the same directory as this script
__this_dir = os.path.dirname(os.path.abspath(__file__))
PSYCHOPY_VERSION = "2024.2.4"
EXPT_NAME = "DisjunctiveConclusion"
EXPT_INFO = {
    "participant": f"{randint(0, 999999):06.0f}",
    "age (yrs)": "",
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
    """
    Setup a log file and tell it what level to log at.

    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.

    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # set how much information should be printed to the console / app
    log_file = logging.LogFile(filename + ".log")
    logging.console.setLevel(logging.DEBUG)
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


def fam_trials(this_exp, win):
    fam_conditions = data.importConditions("lists/fam_trials_list.csv")
    conditions = pd.DataFrame(fam_conditions)
    rep_number = 0

    # Create a trial handler for all trials
    trial_handler = data.TrialHandler2(
        trialList=conditions.to_dict("records"), nReps=2, method="sequential", seed=None
    )
    this_exp.addLoop(trial_handler)

    for _ in trial_handler:
        if rep_number == 0:
            filtered_conditions = conditions[conditions['is_high_confidence_object'] == 1]
        else:
            filtered_conditions = conditions[conditions['is_high_confidence_object'] == 0]

        # trial.trialList = filtered_conditions.to_dict('records')

        # ITS PLAYING 4 TIMES -- fixx this!!!
        
        random_row = filtered_conditions.sample(n=1).iloc[0]
        fam_video_filename = random_row["fam_video_filename"]

        video = visual.MovieStim(
            win, filename=fam_video_filename, movieLib='ffpyplayer',
            loop=False, volume=1.0, noAudio=False,
            pos=(0, 0), units=win.units,
            ori=0.0, anchor='center', opacity=None, contrast=1.0,
        )
        print(f"Current video: {filtered_conditions['fam_video_filename']}")
        video.play()

        while not video.isFinished:
            video.draw()
            win.flip()

        video.stop()
        video.unload()
        # win.close()  # Do not close the window after each trial
        rep_number += 1

        this_exp.nextEntry()

    this_exp.endLoop(trial_handler)


EXPT_INFO = show_exp_info_dlg(EXPT_INFO)
this_exp = setup_data(EXPT_INFO)
log_file = setup_logging(__this_dir + os.sep + "logs" + os.sep + EXPT_NAME)
win = setup_window(EXPT_INFO)
# setupDevices(expInfo=expInfo, thisExp=thisExp, win=win)
run(EXPT_INFO, this_exp, win, global_clock="float")
# saveData(thisExp=thisExp)
# quit(thisExp=thisExp, win=win)
