from copy import deepcopy
from slm_lab.experiment.control import Session, Trial, Experiment
from slm_lab.experiment import analysis
from slm_lab.lib import util
from slm_lab.spec import spec_util
import pandas as pd
import pytest


def test_session(test_spec, test_info_space):
    test_info_space.tick('trial')
    test_info_space.tick('session')
    analysis.save_spec(test_spec, test_info_space, unit='trial')
    session = Session(test_spec, test_info_space)
    session_data = session.run()
    assert isinstance(session_data, pd.DataFrame)


def test_session_total_t(test_spec, test_info_space):
    test_info_space.tick('trial')
    test_info_space.tick('session')
    analysis.save_spec(test_spec, test_info_space, unit='trial')
    spec = deepcopy(test_spec)
    env_spec = spec['env'][0]
    env_spec['max_tick'] = 30
    spec['meta']['max_tick_unit'] = 'total_t'
    session = Session(spec, test_info_space)
    assert session.env.max_tick_unit == 'total_t'
    session_data = session.run()
    assert isinstance(session_data, pd.DataFrame)


def test_trial(test_spec, test_info_space):
    test_info_space.tick('trial')
    analysis.save_spec(test_spec, test_info_space, unit='trial')
    trial = Trial(test_spec, test_info_space)
    trial_data = trial.run()
    assert isinstance(trial_data, pd.DataFrame)


def test_trial_demo(test_info_space):
    spec = spec_util.get('demo.json', 'dqn_cartpole')
    analysis.save_spec(spec, test_info_space, unit='experiment')
    spec = spec_util.override_test_spec(spec)
    spec['meta']['eval_frequency'] = 1
    test_info_space.tick('trial')
    trial_data = Trial(spec, test_info_space).run()
    assert isinstance(trial_data, pd.DataFrame)


def test_experiment(test_info_space):
    spec = spec_util.get('demo.json', 'dqn_cartpole')
    analysis.save_spec(spec, test_info_space, unit='experiment')
    spec = spec_util.override_test_spec(spec)
    test_info_space.tick('experiment')
    experiment_data = Experiment(spec, test_info_space).run()
    assert isinstance(experiment_data, pd.DataFrame)
