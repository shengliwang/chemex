import importlib
import os

import numpy as np


def read_profiles(path, profile_filenames, experiment_details, res_incl=None, res_excl=None):
    experiment_type = experiment_details['type']
    experiment_details['experiment_name'] = name_experiment(experiment_details)
    experiment_module = importlib.import_module('.'.join(['chemex.experiments', experiment_type]))

    Profile = getattr(experiment_module, 'Profile')

    dtype = [('names', '|S20'), ('shifts', '<f8'), ('shifts_err', '<f8')]

    profiles = []

    filename = profile_filenames.get('file', '')
    full_path = os.path.join(path, filename)
    measurements = np.loadtxt(full_path, dtype=dtype)

    for measurement in measurements:
        profile_name = measurement['names']
        profile = Profile(profile_name, measurement, experiment_details)
        profiles.append(profile)

    if res_incl is not None:
        profiles = [
            profile
            for profile in profiles
            if profile.profile_name in res_incl]

    elif res_excl is not None:
        profiles = [
            profile
            for profile in profiles
            if profile.profile_name not in res_excl]

    ndata = sum(len(profile.val) for profile in profiles)

    return profiles, ndata


def name_experiment(experiment_details=None):
    if not experiment_details:
        experiment_details = dict()

    if 'experiment_name' in experiment_details:
        name = experiment_details['experiment_name'].strip().replace(' ', '_')

    else:
        exp_type = experiment_details['type'].replace('.', '_')
        h_larmor_frq = float(experiment_details['h_larmor_frq'])
        temperature = float(experiment_details['temperature'])
        time_t2 = float(experiment_details['time_t2'])

        name = '{:s}_{:.0f}ms_{:.0f}MHz_{:.0f}C'.format(
            exp_type,
            time_t2 * 1e3,
            h_larmor_frq,
            temperature
        ).lower()

    return name


def name_experiment(experiment_details=None):
    if not experiment_details:
        experiment_details = dict()

    if 'experiment_name' in experiment_details:
        name = experiment_details['experiment_name'].strip().replace(' ', '_')
    else:
        exp_type = experiment_details['type'].replace('.', '_')
        h_larmor_frq = float(experiment_details['h_larmor_frq'])
        temperature = float(experiment_details['temperature'])

        name = '{:s}_{:.0f}MHz_{:.0f}C'.format(exp_type, h_larmor_frq, temperature).lower()

    return name
