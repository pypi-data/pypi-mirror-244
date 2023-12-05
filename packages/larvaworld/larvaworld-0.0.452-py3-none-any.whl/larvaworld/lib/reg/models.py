import typing
import numpy as np
import pandas as pd
import param

from .. import reg, aux
from ..aux import nam

__all__ = [
    'ModelRegistry',
]

bF, bT = {'dtype': bool, 'v0': False, 'v': False}, {'dtype': bool, 'v0': True, 'v': True}


def arrange_index_labels(index):
    ks = index.unique().tolist()
    Nks = index.value_counts(sort=False)

    def merge(k, Nk):
        Nk1 = int((Nk - 1) / 2)
        Nk2 = Nk - 1 - Nk1
        return [''] * Nk1 + [k.upper()] + [''] * Nk2

    new = aux.flatten_list([merge(k, Nks[k]) for k in ks])
    return new


def init_brain_modules():
    from ..model import modules
    def Tur0():
        NEUargs = {
            'base_activation': {'dtype': float, 'v0': 20.0, 'lim': (10.0, 40.0), 'dv': 0.1,
                                'disp': 'tonic input', 'sym': '$I_{T}^{0}$', 'k': 'I_T0',
                                'codename': 'turner_input_constant',
                                'h': 'The baseline activation/input of the TURNER module.'},
            'activation_range': {'dtype': typing.Tuple[float], 'v0': (10.0, 40.0),
                                 'lim': (0.0, 100.0), 'dv': 0.1,
                                 'k': 'I_T_r',
                                 'disp': 'input range',
                                 'sym': r'$[I_{T}^{min},I_{T}^{max}]$',
                                 'h': 'The activation/input range of the TURNER module.'},

            'tau': {'v0': 0.1, 'lim': (0.05, 0.5), 'dv': 0.01, 'disp': 'time constant', 'k': 'tau_T',
                    'sym': r'$\tau_{T}$',
                    'u': reg.units.s,
                    'h': 'The time constant of the neural oscillator.'},
            'm': {'dtype': int, 'v0': 100, 'lim': (50, 200), 'dv': 1, 'disp': 'maximum spike-rate',
                  'sym': '$SR_{max}$', 'k': 'SR_T',
                  'h': 'The maximum allowed spike rate.'},
            'n': {'v0': 2.0, 'lim': (1.5, 3.0), 'dv': 0.01, 'disp': 'spike response steepness', 'k': 'n_T',
                  'sym': '$n_{T}$',
                  'h': 'The neuron spike-rate response steepness coefficient.'},

        }

        Tamp = {'amp': {'lim': (0.1, 200.0), 'dv': 0.1, 'v0': 20.0,
                        'k': 'A_T0', 'codename': 'pause_front_orientation_velocity_mean',
                        'disp': 'output amplitude', 'sym': '$A_{T}^{0}$',
                        'h': 'The initial activity amplitude of the TURNER module.'},
                }

        SINargs = {**Tamp,
                   'freq': {'v0': 0.58, 'lim': (0.01, 2.0), 'dv': 0.01,
                            'k': 'f_T0',
                            'disp': 'bending frequency', 'sym': nam.tex.sub('f', 'T'), 'u_name': '$Hz$',
                            'u': reg.units.Hz, 'codename': 'front_orientation_velocity_freq',
                            'h': 'The initial frequency of the repetitive lateral bending behavior if this is hardcoded (e.g. sinusoidal mode).'},
                   }

        d = {'neural': {'args': NEUargs, 'class_func': modules.NeuralOscillator,
                        'variable': ['base_activation', 'tau', 'n']},
             'sinusoidal': {'args': SINargs, 'class_func': modules.SinOscillator, 'variable': ['amp', 'freq']},
             'constant': {'args': Tamp, 'class_func': modules.StepEffector, 'variable': ['amp']}
             }
        return aux.AttrDict(d)

    def Cr0():
        str_kws = {'stride_dst_mean': {'v0': 0.23, 'lim': (0.0, 1.1), 'dv': 0.01,
                                       'k': 'str_sd_mu',
                                       'disp': r'stride distance mean',
                                       'sym': nam.tex.sub(nam.tex.bar(nam.tex.mathring('d')), 'S'),
                                       'u_name': '$body-lengths$', 'codename': 'stride_scaled_dst_mean',
                                       'h': 'The mean displacement achieved in a single peristaltic stride as a fraction of the body length.'},
                   'stride_dst_std': {'v0': 0.04, 'lim': (0.0, 0.5),
                                      'k': 'str_sd_std',
                                      'disp': 'stride distance std',
                                      'sym': nam.tex.sub(nam.tex.tilde(nam.tex.mathring('d')), 'S'),
                                      'u_name': '$body-lengths$', 'codename': 'stride_scaled_dst_std',
                                      'h': 'The standard deviation of the displacement achieved in a single peristaltic stride as a fraction of the body length.'}}

        Camp = {'amp': {'lim': (0.0, 2.0), 'dv': 0.1, 'v0': 0.3,
                        'k': 'A_C0', 'codename': 'stride_scaled_velocity_mean',
                        'disp': 'output amplitude', 'sym': nam.tex.subsup('A', 'C', '0'),
                        'h': 'The initial output amplitude of the CRAWLER module.'}}
        Cfr = {'freq': {'v0': 1.42, 'lim': (0.5, 2.5), 'dv': 0.1,
                        'k': 'f_C0',
                        'disp': 'crawling frequency', 'sym': nam.tex.subsup('f', 'C', '0'), 'u': reg.units.Hz,
                        'codename': 'scaled_velocity_freq',
                        'h': 'The initial frequency of the repetitive crawling behavior.'}}

        SQargs = {
            'duty': {'v0': 0.6, 'lim': (0.0, 1.0), 'dv': 0.1,
                     'k': 'r_C',
                     'disp': 'square signal duty', 'sym': nam.tex.sub('r', 'C'),
                     'h': 'The duty parameter(%time at the upper end) of the square signal.'},
            **Cfr, **Camp

        }
        GAUargs = {
            'std': {'v0': 0.6, 'lim': (0.0, 1.0), 'dv': 0.1,
                    'k': 'r_C',
                    'disp': 'gaussian stride cycle std', 'sym': nam.tex.sub('r', 'C'),
                    'h': 'The std of the gaussian window.'},

            **Cfr, **Camp
        }
        Rargs = {'max_scaled_vel': {'v0': 0.51, 'lim': (0.0, 1.5), 'disp': 'maximum scaled velocity',
                                    'codename': 'stride_scaled_velocity_max', 'k': 'str_sv_max', 'dv': 0.1,
                                    'sym': nam.tex.sub(nam.tex.mathring('v'), 'max'), 'u': reg.units.s ** -1,
                                    'u_name': '$body-lengths/sec$',
                                    'h': 'The maximum scaled forward velocity.'},

                 'max_vel_phase': {'v0': 3.49, 'lim': (0.0, 2 * np.pi), 'disp': 'max velocity phase',
                                   'k': 'phi_v_max', 'dv': 0.1,
                                   'sym': nam.tex.subsup('$\phi$', 'C', 'v'), 'u_name': 'rad', 'u': reg.units.rad,
                                   'codename': 'phi_scaled_velocity_max',
                                   'h': 'The phase of the crawling oscillation cycle where forward velocity is maximum.'},
                 **Cfr
                 }

        d = {

            'gaussian': {'args': {**GAUargs, **str_kws}, 'class_func': modules.GaussOscillator,
                         'variable': ['stride_dst_mean', 'stride_dst_std', 'std', 'amp', 'freq']},
            'square': {'args': {**SQargs, **str_kws}, 'class_func': modules.SquareOscillator,
                       'variable': ['stride_dst_mean', 'stride_dst_std', 'duty', 'amp', 'freq']},
            'realistic': {'args': {**Rargs, **str_kws}, 'class_func': modules.PhaseOscillator,
                          'variable': ['stride_dst_mean', 'stride_dst_std', 'max_scaled_vel', 'max_vel_phase',
                                       'freq']},
            'constant': {'args': Camp, 'class_func': modules.StepEffector, 'variable': ['amp']}
        }
        return aux.AttrDict(d)

    def If0():
        IFargs = {
            'suppression_mode': {'dtype': str, 'v0': 'amplitude', 'vs': ['amplitude', 'oscillation', 'both'],
                                 'k': 'IF_target',
                                 'disp': 'suppression target', 'sym': '-',
                                 'h': 'CRAWLER:TURNER suppression target.'},
            'attenuation': {'v0': 1.0, 'lim': (0.0, 1.0), 'disp': 'suppression coefficient',
                            'sym': '$c_{CT}^{0}$', 'k': 'c_CT0', 'codename': 'attenuation_min',
                            'h': 'CRAWLER:TURNER baseline suppression coefficient'},
            'attenuation_max': {'v0': 0.0, 'lim': (0.0, 1.0),
                                'disp': 'suppression relief coefficient',
                                'sym': '$c_{CT}^{1}$', 'k': 'c_CT1', 'codename': 'attenuation_max',
                                'h': 'CRAWLER:TURNER suppression relief coefficient.'}
        }

        PHIargs = {
            'max_attenuation_phase': {'v0': 3.4, 'lim': (0.0, 2 * np.pi), 'disp': 'max relief phase',
                                      'codename': 'phi_attenuation_max',
                                      'sym': '$\phi_{C}^{\omega}$', 'u': reg.units.rad, 'k': 'phi_fov_max',
                                      'h': 'CRAWLER phase of minimum TURNER suppression.'},
            **IFargs
        }
        SQargs = {
            'crawler_phi_range': {'dtype': typing.Tuple[float], 'v0': (1.57, 3.14), 'lim': (0.0, 2 * np.pi),
                                  'disp': 'suppression relief phase interval',
                                  'sym': '$[\phi_{C}^{\omega_{0}},\phi_{C}^{\omega_{1}}]$',
                                  'u': reg.units.rad,
                                  'h': 'CRAWLER phase range for TURNER suppression lift.'},
            'feeder_phi_range': {'dtype': typing.Tuple[float], 'v0': (0.0, 0.0), 'lim': (0.0, 2 * np.pi),
                                 'disp': 'feeder suppression relief phase interval',
                                 'sym': '$[\phi_{F}^{\omega_{0}},\phi_{F}^{\omega_{1}}]$',
                                 'u': reg.units.rad,
                                 'h': 'FEEDER phase range for TURNER suppression lift.'},
            **IFargs

        }

        d = {'default': {'args': IFargs, 'class_func': modules.DefaultCoupling, 'variable': ['attenuation']},
             'square': {'args': SQargs, 'class_func': modules.SquareCoupling,
                        'variable': ['attenuation', 'attenuation_max', 'crawler_phi_range']},
             'phasic': {'args': PHIargs, 'class_func': modules.PhasicCoupling,
                        'variable': ['attenuation', 'attenuation_max', 'max_attenuation_phase']}
             }
        return aux.AttrDict(d)

    def Im0():
        dist_args = {k: reg.get_dist(k=k) for k in ['stridechain_dist', 'run_dist', 'pause_dist']}

        IMargs = {
            'run_mode': {'dtype': str, 'v0': 'stridechain', 'vs': ['stridechain', 'exec'],
                         'h': 'The generation mode of exec epochs.'},
            'EEB': {'v0': 0.0, 'lim': (0.0, 1.0), 'sym': 'EEB', 'k': 'EEB', 'disp': 'Exploitation:Exploration balance',
                    'h': 'The baseline exploitation-exploration balance. 0 means only exploitation, 1 only exploration.'},
            'EEB_decay': {'v0': 1.0, 'lim': (0.0, 2.0), 'sym': nam.tex.sub('c', 'EEB'),
                          'k': 'c_EEB', 'disp': 'EEB decay coefficient',
                          'h': 'The exponential decay coefficient of the exploitation-exploration balance when no food is detected.'},

            'feed_bouts': {**bF, 'disp': 'feeding bouts', 'k': 'epochs_F',
                           'h': 'Whether feeding bouts (feedchains) are generated.'},
            'crawl_freq': {'v0': 1.43, 'lim': (0.5, 2.5), 'k': 'f_C', 'dv': 0.01, 'u': reg.units.Hz,
                           'sym': nam.tex.sub('f', 'C'),
                           'disp': 'crawling frequency',
                           'h': 'The default frequency of the CRAWLER oscillator when simulating offline.'},
            'feed_freq': {'v0': 2.0, 'lim': (0.5, 4.0), 'dv': 0.01, 'k': 'f_F', 'u': reg.units.Hz,
                          'sym': nam.tex.sub('f', 'F'),
                          'disp': 'feeding frequency',
                          'h': 'The default frequency of the FEEDER oscillator when simulating offline.'},
            'feeder_reoccurence_rate': {'lim': (0.0, 1.0), 'disp': 'feed reoccurence', 'sym': nam.tex.sub('r', 'F'),
                                        'h': 'The default reoccurence rate of the feeding motion.'},
            **dist_args

        }

        BRargs = {
            'c': {'v0': 0.7, 'lim': (0.0, 1.0),
                  'disp': 'branch coefficient',
                  'sym': nam.tex.subsup('c', 'Im', 'br'),
                  'h': 'The ISING branching coef.'},
            'sigma': {'v0': 1.0, 'lim': (0.0, 10.0),
                      'disp': 'branch sigma',
                      'sym': nam.tex.subsup('s', 'Im', 'br'),
                      'h': 'The ISING branching coef.'},
            'beta': {'v0': 0.15, 'lim': (0.0, 10.0),
                     'disp': 'Exp beta',
                     'sym': nam.tex.subsup('b', 'Im', 'br'),
                     'h': 'The beta coef for the exponential bout generation.'},
            **IMargs

        }

        d = {'default': {'args': IMargs, 'class_func': modules.Intermitter,
                         'variable': ['stridechain_dist', 'run_dist', 'pause_dist']},
             'nengo': {'args': IMargs, 'class_func': modules.NengoIntermitter,
                       'variable': ['stridechain_dist', 'run_dist', 'pause_dist']},
             'branch': {'args': BRargs, 'class_func': modules.BranchIntermitter,
                        'variable': ['c', 'sigma', 'beta', 'stridechain_dist', 'run_dist', 'pause_dist']},
             }
        return aux.AttrDict(d)

    def sensor_kws(k0, l0):
        d = {
            'perception': {'dtype': str, 'v0': 'log', 'vs': ['log', 'linear', 'null'],
                           'disp': f'{l0} sensory transduction mode',
                           'k': f'mod_{k0}',
                           'sym': nam.tex.sub('mod', k0),
                           'h': 'The method used to calculate the perceived sensory activation from the current and previous sensory input.'},
            'decay_coef': {'v0': 0.1, 'lim': (0.0, 2.0), 'disp': f'{l0} output decay coef',
                           'sym': nam.tex.sub('c', k0), 'k': f'c_{k0}',
                           'h': f'The exponential decay coefficient of the {l0} sensory activation.'},
            'brute_force': {**bF, 'disp': 'ability to interrupt locomotion', 'sym': nam.tex.sub('bf', k0),
                            'k': f'bf_{k0}',
                            'h': 'Whether to apply direct rule-based modulation on locomotion or not.'},
        }
        return d

    def Olf0():
        args = {
            'gain_dict': {'dtype': dict, 'k': 'G_O', 'v0': {},
                          'sym': nam.tex.sub('G', 'O'), 'disp': 'gain per odor ID',
                          'h': 'The dictionary of the olfactory gains.'},
            **sensor_kws(k0='O', l0='olfaction')}
        d = {'default': {'args': args, 'class_func': modules.Olfactor,
                         'variable': ['perception', 'decay_coef', 'brute_force', 'gain_dict']},
             }
        return aux.AttrDict(d)

    def Tou0():
        args = {
            **sensor_kws(k0='T', l0='tactile'),
            'state_specific_best': {**bT, 'disp': 'state-specific or the global highest evaluated gain',
                                    'sym': nam.tex.sub('state_specific', 'T'),
                                    'k': 'state_specific',
                                    'h': 'Whether to use the state-specific or the global highest evaluated gain after the end of the memory training period.'},
            'initial_gain': {'v0': 40.0, 'lim': (-100.0, 100.0),
                             'disp': 'tactile sensitivity coef', 'sym': nam.tex.sub('G', 'T'), 'k': 'G_T',
                             'h': 'The initial gain of the tactile sensor.'},
            'touch_sensors': {'dtype': typing.List[int], 'lim': (0, 8), 'k': 'sens_touch',
                              'sym': nam.tex.sub('N', 'T'), 'disp': 'tactile sensor contour locations',
                              'h': 'The number of touch sensors existing on the larva body.'},
        }
        d = {'default': {'args': args, 'class_func': modules.Toucher,
                         'variable': ['perception', 'decay_coef', 'brute_force', 'initial_gain']},
             }
        return aux.AttrDict(d)

    def W0():
        args = {
            'weights': {
                'hunch_lin': {'v0': 10.0, 'lim': (-100.0, 100.0), 'disp': 'HUNCH->CRAWLER',
                              'sym': nam.tex.sub('w', 'HC'), 'k': 'w_HC',
                              'h': 'The connection weight between the HUNCH neuron ensemble and the CRAWLER module.'},
                'hunch_ang': {'v0': 0.0, 'lim': (-100.0, 100.0), 'disp': 'HUNCH->TURNER',
                              'sym': nam.tex.sub('w', 'HT'), 'k': 'w_HT',
                              'h': 'The connection weight between the HUNCH neuron ensemble and the TURNER module.'},
                'bend_lin': {'v0': 0.0, 'lim': (-100.0, 100.0), 'disp': 'BEND->CRAWLER',
                             'sym': nam.tex.sub('w', 'BC'), 'k': 'w_BC',
                             'h': 'The connection weight between the BEND neuron ensemble and the CRAWLER module.'},
                'bend_ang': {'v0': -10.0, 'lim': (-100.0, 100.0), 'disp': 'BEND->TURNER',
                             'sym': nam.tex.sub('w', 'BT'), 'k': 'w_BT',
                             'h': 'The connection weight between the BEND neuron ensemble and the TURNER module.'},
            },

            **sensor_kws(k0='W', l0='windsensor'),
        }
        d = {'default': {'args': args, 'class_func': modules.Windsensor,
                         'variable': ['perception', 'decay_coef', 'brute_force']},
             }
        return aux.AttrDict(d)

    def Th0():
        args = {'cool_gain': {'v0': 0.0, 'lim': (-1000.0, 1000.0),
                              'disp': 'cool thermosensing gain', 'sym': nam.tex.sub('G', 'cool'), 'k': 'G_cool',
                              'h': 'The gain of the cool thermosensor.'},
                'warm_gain': {'v0': 0.0, 'lim': (-1000.0, 1000.0),
                              'disp': 'warm thermosensing gain', 'sym': nam.tex.sub('G', 'warm'), 'k': 'G_warm',
                              'h': 'The gain of the warm thermosensor.'},

                **sensor_kws(k0='Th', l0='thermosensor'),
                }
        d = {'default': {'args': args, 'class_func': modules.Thermosensor,
                         'variable': ['perception', 'decay_coef', 'brute_force', 'cool_gain', 'warm_gain']},
             }
        return aux.AttrDict(d)

    def Fee0():
        Fargs = {
            'freq': {'v0': 2.0, 'lim': (0.0, 4.0), 'k': 'f_F0',
                     'disp': 'feeding frequency', 'sym': nam.tex.sub('f', 'F'), 'u': reg.units.Hz,
                     'h': 'The initial default frequency of the repetitive feeding behavior'},
            'feed_radius': {'v0': 0.1, 'lim': (0.1, 10.0), 'sym': nam.tex.sub('rad', 'F'),
                            'disp': 'feeding radius', 'k': 'rad_F',
                            'h': 'The radius around the mouth in which food is consumable as a fraction of the body length.'},
            'V_bite': {'v0': 0.001, 'lim': (0.0001, 0.01), 'dv': 0.0001,
                       'sym': nam.tex.sub('V', 'F'), 'disp': 'feeding volume ratio', 'k': 'V_F',
                       'h': 'The volume of food consumed on a single feeding motion as a fraction of the body volume.'}
        }

        d = {'default': {'args': Fargs, 'class_func': modules.Feeder, 'variable': ['freq']},
             }
        return aux.AttrDict(d)

    def Mem0():
        args0 = {
            'modality': {'dtype': str, 'v0': 'olfaction', 'vs': ['olfaction', 'touch'],
                         'h': 'The modality for which the memory module is used.'},
        }

        RLargs = {
            # 'modality': {'dtype': str, 'v0': 'olfaction', 'vs': ['olfaction', 'touch'],
            #              'h': 'The modality for which the memory module is used.'},
            'Delta': {'v0': 0.1, 'lim': (0.0, 10.0), 'h': 'The input sensitivity of the memory.'},
            'state_spacePerSide': {'dtype': int, 'v0': 0, 'lim': (0, 20), 'disp': 'state space dim',
                                   'h': 'The number of discrete states to parse the state space on either side of 0.'},
            'gain_space': {'dtype': typing.List[float], 'v0': [-300.0, -50.0, 50.0, 300.0], 'lim': (-1000.0, 1000.0),
                           'dv': 1.0, 'h': 'The possible values for memory gain to choose from.'},
            'update_dt': {'v0': 1.0, 'lim': (0.0, 10.0), 'dv': 1.0,
                          'h': 'The interval duration between gain switches.'},
            'alpha': {'v0': 0.05, 'lim': (0.0, 2.0), 'dv': 0.01,
                      'h': 'The alpha parameter of reinforcement learning algorithm.'},
            'gamma': {'v0': 0.6, 'lim': (0.0, 2.0),
                      'h': 'The probability of sampling a random gain rather than exploiting the currently highest evaluated gain for the current state.'},
            'epsilon': {'v0': 0.3, 'lim': (0.0, 2.0),
                        'h': 'The epsilon parameter of reinforcement learning algorithm.'},
            'train_dur': {'v0': 20.0, 'lim': (0.0, 100.0),
                          'h': 'The duration of the training period after which no further learning will take place.'},
            **args0
        }

        MBargs = {**args0}

        d = {'RL': {'args': RLargs, 'class_func': modules.RLOlfMemory,
                    'variable': ['Delta', 'update_dt', 'alpha', 'epsilon']},
             'MB': {'args': MBargs, 'class_func': modules.RemoteBrianModelMemory, 'variable': []},
             }
        return aux.AttrDict(d)

    kws = {'kwargs': {'dt': 0.1}}
    d0 = {}
    d0['turner'] = {'mode': Tur0(), 'pref': 'brain.turner_params.', **kws}
    d0['crawler'] = {'mode': Cr0(), 'pref': 'brain.crawler_params.', **kws}
    d0['intermitter'] = {'mode': Im0(), 'pref': 'brain.intermitter_params.', **kws}
    d0['interference'] = {'mode': If0(), 'pref': 'brain.interference_params.', 'kwargs': {}}
    d0['feeder'] = {'mode': Fee0(), 'pref': 'brain.feeder_params.', **kws}
    d0['olfactor'] = {'mode': Olf0(), 'pref': 'brain.olfactor_params.', **kws}
    d0['toucher'] = {'mode': Tou0(), 'pref': 'brain.toucher_params.', **kws}
    d0['thermosensor'] = {'mode': Th0(), 'pref': 'brain.thermosensor_params.', **kws}
    d0['windsensor'] = {'mode': W0(), 'pref': 'brain.windsensor_params.', **kws}
    d0['memory'] = {'mode': Mem0(), 'pref': 'brain.memory_params.', **kws}

    return aux.AttrDict(d0)


def init_aux_modules():
    return aux.AttrDict({
        'physics': {
            'args': {
                'torque_coef': {'v0': 0.5, 'lim': (0.1, 1.0), 'dv': 0.01, 'disp': 'torque coefficient',
                                'sym': nam.tex.sub('c', 'T'), 'u_name': nam.tex.sup('sec', '-2'),
                                'u': reg.units.s ** -2,
                                'h': 'Conversion coefficient from TURNER output to torque-per-inertia-unit.'},
                'ang_vel_coef': {'v0': 1.0, 'lim': (0.0, 5.0), 'dv': 0.01, 'disp': 'angular velocity coefficient',
                                 'h': 'Conversion coefficient from TURNER output to angular velocity.'},
                'ang_damping': {'v0': 1.0, 'lim': (0.1, 2.0), 'disp': 'angular damping', 'sym': 'z',
                                'u_name': nam.tex.sup('sec', '-1'), 'u': reg.units.s ** -1,
                                'h': 'Angular damping exerted on angular velocity.'},
                'lin_damping': {'v0': 1.0, 'lim': (0.0, 10.0), 'disp': 'linear damping', 'sym': 'zl',
                                'u_name': nam.tex.sup('sec', '-1'), 'u': reg.units.s ** -1,
                                'h': 'Linear damping exerted on forward velocity.'},
                'body_spring_k': {'v0': 1.0, 'lim': (0.0, 10.0), 'dv': 0.1, 'disp': 'body spring constant',
                                  'sym': 'k', 'u_name': nam.tex.sup('sec', '-2'), 'u': reg.units.s ** -2,
                                  'h': 'Larva-body torsional spring constant reflecting deformation resistance.'},
                'bend_correction_coef': {'v0': 1.0, 'lim': (0.8, 1.5), 'disp': 'bend correction coefficient',
                                         'sym': nam.tex.sub('c', 'b'),
                                         'h': 'Correction coefficient of bending angle during forward motion.'},
                'ang_mode': {'dtype': str, 'v0': 'torque', 'vs': ['torque', 'velocity'], 'disp': 'angular mode',
                             'h': 'Whether the Turner module output is equivalent to torque or angular velocity.'},
            },
            'variable': ['torque_coef', 'ang_damping', 'body_spring_k', 'bend_correction_coef']
        },
        'body': {
            'args': {
                'length': {'v0': 0.004, 'lim': (0.0, 0.01), 'dv': 0.0001,
                           'disp': 'length', 'sym': '$l$', 'u': reg.units.m, 'k': 'l0',
                           'h': 'The initial body length.'},

                'Nsegs': {'dtype': int, 'v0': 2, 'lim': (1, 12), 'disp': 'number of body segments',
                          'sym': nam.tex.sub('N', 'segs'),
                          'u_name': '# $segments$', 'k': 'Nsegs',
                          'h': 'The number of segments comprising the larva body.'},
                'segment_ratio': {'k': 'seg_r', 'lim': (0.0, 1.0),
                                  'h': 'The length ratio of the body segments. If null, equal-length segments are generated.'},

                'body_plan': {'dtype': str, 'v0': 'drosophila_larva', 'vs': ['drosophila_larva', 'zebrafish_larva'],
                              'k': 'body_shape', 'h': 'The body shape.'},
            },
            'variable': ['length', 'Nsegs']
        },
        'energetics': {
            'mode': {
                'gut': {
                    'args': {
                        'M_gm': {'v0': 10 ** -2, 'lim': (0.0, 10.0), 'disp': 'gut scaled capacity',
                                 'sym': 'M_gm',
                                 'k': 'M_gm',
                                 'h': 'Gut capacity in C-moles per unit of gut volume.'},
                        'y_P_X': {'v0': 0.9, 'disp': 'food->product yield',
                                  'sym': 'y_P_X', 'k': 'y_P_X',
                                  'h': 'Yield of product per unit of food.'},
                        'J_g_per_cm2': {'v0': 10 ** -2 / (24 * 60 * 60), 'lim': (0.0, 10.0),
                                        'disp': 'digestion secretion rate',
                                        'sym': 'J_g_per_cm2', 'k': 'J_g_per_cm2',
                                        'h': 'Secretion rate of enzyme per unit of gut surface per second.'},
                        'k_g': {'v0': 1.0, 'lim': (0.0, 10.0), 'disp': 'digestion decay rate', 'sym': 'k_g',
                                'k': 'k_g',
                                'h': 'Decay rate of digestive enzyme.'},
                        'k_dig': {'v0': 1.0, 'lim': (0.0, 10.0), 'disp': 'digestion rate', 'sym': 'k_dig',
                                  'k': 'k_dig',
                                  'h': 'Rate constant for digestion : k_X * y_Xg.'},
                        'f_dig': {'v0': 1.0, 'disp': 'digestion response',
                                  'sym': 'f_dig', 'k': 'f_dig',
                                  'h': 'Scaled functional response for digestion : M_X/(M_X+M_K_X)'},
                        'M_c_per_cm2': {'v0': 5 * 10 ** -8, 'lim': (0.0, 10.0), 'disp': 'carrier density',
                                        'sym': 'M_c_per_cm2', 'k': 'M_c_per_cm2',
                                        'h': 'Area specific amount of carriers in the gut per unit of gut surface.'},
                        'constant_M_c': {**bT, 'disp': 'constant carrier density', 'sym': 'constant_M_c',
                                         'k': 'constant_M_c',
                                         'h': 'Whether to assume a constant amount of carrier enzymes on the gut surface.'},
                        'k_c': {'v0': 1.0, 'lim': (0.0, 10.0), 'disp': 'carrier release rate', 'sym': 'k_c',
                                'k': 'gut_k_c',
                                'h': 'Release rate of carrier enzymes.'},
                        'k_abs': {'v0': 1.0, 'lim': (0.0, 10.0), 'disp': 'absorption rate', 'sym': 'k_abs',
                                  'k': 'gut_k_abs',
                                  'h': 'Rate constant for absorption : k_P * y_Pc.'},
                        'f_abs': {'v0': 1.0, 'lim': (0.0, 1.0), 'disp': 'absorption response',
                                  'sym': 'f_abs', 'k': 'f_abs',
                                  'h': 'Scaled functional response for absorption : M_P/(M_P+M_K_P)'},
                    },
                    'variable': ['k_abs', 'k_g']
                },
                'DEB': {
                    'args': {
                        'species': {'dtype': str, 'v0': 'default', 'vs': ['default', 'rover', 'sitter'],
                                    'disp': 'phenotype',
                                    'k': 'species',
                                    'h': 'The phenotype/species-specific fitted DEB model to use.'},
                        'f_decay': {'v0': 0.1, 'lim': (0.0, 1.0), 'dv': 0.1, 'sym': nam.tex.sub('c', 'DEB'),
                                    'k': 'c_DEB',
                                    'disp': 'DEB functional response decay coef',
                                    'h': 'The exponential decay coefficient of the DEB functional response.'},
                        'V_bite': {'v0': 0.0005, 'lim': (0.0, 0.1), 'dv': 0.0001,
                                   'sym': nam.tex.sub('V', 'bite'),
                                   'k': 'V_bite',
                                   'h': 'The volume of food consumed on a single feeding motion as a fraction of the body volume.'},
                        'hunger_as_EEB': {**bT,
                                          'h': 'Whether the DEB-generated hunger drive informs the exploration-exploitation balance.',
                                          'sym': 'hunger_as_EEB', 'k': 'hunger_as_EEB'},
                        'hunger_gain': {'v0': 0.0, 'lim': (0.0, 1.0), 'sym': nam.tex.sub('G', 'hunger'),
                                        'k': 'G_hunger', 'disp': 'hunger sensitivity to reserve reduction',
                                        'h': 'The sensitivy of the hunger drive in deviations of the DEB reserve density.'},
                        'assimilation_mode': {'dtype': str, 'v0': 'gut', 'vs': ['sim', 'gut', 'deb'],
                                              'sym': nam.tex.sub('m', 'ass'), 'k': 'ass_mod',
                                              'h': 'The method used to calculate the DEB assimilation energy flow.'},
                        'dt': {'lim': (0.0, 1000.0), 'disp': 'DEB timestep (sec)', 'v0': None,
                               'sym': nam.tex.sub('dt', 'DEB'),
                               'k': 'DEB_dt',
                               'h': 'The timestep of the DEB energetics module in seconds.'},
                        # 'gut_params':d['gut_params']
                    },
                    'variable': ['DEB_dt', 'hunger_gain']
                }
            }
        },
        'sensorimotor': {
            'mode': {
                'default': {
                    'args': {
                        'sensor_delta_direction': {'v0': 0.4, 'dv': 0.01, 'lim': (0.2, 1.2), 'k': 'sens_Dor',
                                                   'h': 'Sensor delta_direction'},
                        'sensor_saturation_value': {'dtype': int, 'v0': 40, 'lim': (0, 200), 'k': 'sens_c_sat',
                                                    'h': 'Sensor saturation value'},
                        'obstacle_sensor_error': {'v0': 0.35, 'dv': 0.01, 'lim': (0.0, 1.0), 'k': 'sens_err',
                                                  'h': 'Proximity sensor error'},
                        'sensor_max_distance': {'v0': 0.9, 'dv': 0.01, 'lim': (0.1, 1.5), 'k': 'sens_dmax',
                                                'h': 'Sensor max_distance'},
                        'motor_ctrl_coefficient': {'dtype': int, 'v0': 8770, 'lim': (0, 10000), 'k': 'c_mot',
                                                   'h': 'Motor ctrl_coefficient'},
                        'motor_ctrl_min_actuator_value': {'dtype': int, 'v0': 35, 'lim': (0, 50), 'k': 'mot_vmin',
                                                          'h': 'Motor ctrl_min_actuator_value'}
                    },
                    'class_func': None,
                    'variable': ['sensor_delta_direction', 'sensor_saturation_value', 'obstacle_sensor_error',
                                 'sensor_max_distance', 'motor_ctrl_coefficient',
                                 'motor_ctrl_min_actuator_value']
                }
            },
            'pref': 'sensorimotor.'
        }
    })


def build_aux_module_dict(d0):
    d = d0.get_copy()
    for k in d0.keys():
        if k in ['energetics', 'sensorimotor']:
            continue

        for p, vs in d0[k].args.items():
            d[k].args[p] = reg.build_LarvaworldParam(p=p, **vs)
    for k in ['energetics', 'sensorimotor']:
        for m, mdic in d0[k].mode.items():
            for p, vs in mdic.args.items():
                d[k].mode[m].args[p] = reg.build_LarvaworldParam(p=p, **vs)
    return d


def build_brain_module_dict(d0):
    d = d0.get_copy()
    for k in d0.keys():
        for m, mdic in d0[k].mode.items():
            for p, vs in mdic.args.items():
                d[k].mode[m].args[p] = reg.build_LarvaworldParam(p=p, **vs)
    return d


def build_confdicts():
    b0 = init_brain_modules()
    bm = build_brain_module_dict(b0)
    bd = aux.AttrDict({'init': b0, 'm': bm, 'keys': list(b0.keys())})

    a0 = init_aux_modules()
    am = build_aux_module_dict(a0)
    ad = aux.AttrDict({'init': a0, 'm': am, 'keys': list(a0.keys())})

    d0 = aux.AttrDict({**b0, **a0})

    d = aux.AttrDict({'init': d0, 'm': aux.AttrDict({**bm, **am}), 'keys': list(d0.keys())})
    return aux.AttrDict({'brain': bd, 'aux': ad, 'model': d})


class ModelRegistry:
    def __init__(self):
        self.dict = build_confdicts()
        self.full_dict = self.build_full_dict()

    @property
    def autostored_confs(self):
        return self.autogenerate_confs()

    @property
    def mkeys(self):
        return self.dict.model.keys

    def get_mdict(self, mkey, mode='default'):
        if mkey is None or mkey not in self.mkeys:
            raise ValueError('Module key must be one of larva-model configuration keys')
        else:
            D = self.dict
            if mkey in D.brain.keys + ['energetics']:
                return D.model.m[mkey].mode[mode].args
            elif mkey in D.aux.keys:
                return D.model.m[mkey].args

    def conf(self, mdict, **kwargs):
        C = aux.AttrDict()
        for d, p in mdict.items():
            if isinstance(p, param.Parameterized):
                C[d] = p.v
            else:
                C[d] = self.conf(mdict=p)
        C.update_existingdict(kwargs)
        return aux.AttrDict(C)

    def brainConf(self, modes=None, modkws={}, nengo=False):

        if modes is None:
            modes = {'crawler': 'realistic',
                     'turner': 'neural',
                     'interference': 'phasic',
                     'intermitter': 'default'}

        conf = aux.AttrDict()

        for mkey in self.dict.brain.keys:
            mlongkey = f'{mkey}_params'
            if mkey not in modes.keys():
                conf[mlongkey] = None
            else:
                mode = modes[mkey]
                mdict = self.dict.brain.m[mkey].mode[mode].args
                if mkey in modkws.keys():
                    mkws = modkws[mkey]
                else:
                    mkws = {}
                conf[mlongkey] = self.conf(mdict, **mkws)
                conf[mlongkey]['mode'] = mode

        conf.nengo = nengo
        return conf

    def larvaConf(self, modes=None, modkws={}, nengo=False):
        bconf = self.brainConf(modes, modkws, nengo=nengo)

        C = aux.AttrDict()
        C.brain = bconf

        for auxkey in self.dict.aux.keys:
            if auxkey == 'energetics':
                C[auxkey] = None
                continue
            elif auxkey == 'sensorimotor':
                continue
            else:
                C[auxkey] = self.conf(self.dict.aux.m[auxkey].args)

        #  TODO thsi

        C.Box2D_params = {
            'joint_types': {
                'friction': {'N': 0, 'args': {}},
                'revolute': {'N': 0, 'args': {}},
                'distance': {'N': 0, 'args': {}}
            }
        }

        return C

    def autogenerate_confs(self):
        from ..model import ModuleModeDict as MD
        from ..model.modules import Effector
        from ..model.deb import DEB, DEB_model, Gut
        from ..model.agents import LarvaRobot, ObstacleLarvaRobot
        from ..param import class_defaults as cd
        E = {}
        def new(id, id0, kws={}):
            try:
                E[id] = E[id0].new_dict(kws)
            except:
                pass
        def newexp(id, kws={}):
            new(id=id,id0='explorer', kws=kws)
        def newnav(id, kws={}):
            new(id=id,id0='navigator', kws=kws)
        def newfor(id, kws={}):
            new(id=id,id0='forager', kws=kws)


        def sensor_kws(sensor, mode='default', **kwargs):
            return {f'brain.{sensor}_params': cd(MD[sensor][mode], excluded=[Effector],included={'mode': mode},**kwargs)}

        def mem_kws(mode='RL', modality='olfaction', **kwargs):
            return {'brain.memory_params': cd(MD['memory'][mode][modality], excluded=['dt'],included={'mode': mode, 'modality':modality},**kwargs)}
        mem=aux.AttrDict({mode:mem_kws(mode) for mode in ['RL', 'MB']})


        olf = aux.AttrDict({mode: sensor_kws(sensor='olfactor',mode=mode) for mode in ['default', 'osn']})
        def olf_kws(g={'Odor': 150.0},mode='default', **kwargs):
            D=olf[mode].get_copy()
            D['brain.olfactor_params'].update({'gain_dict':g, **kwargs})
            return D
            # return sensor_kws(sensor='olfactor', mode=mode, gain_dict=g, **kwargs)


        def OD(gain_dict):
            return {'brain.olfactor_params.gain_dict': gain_dict}

        def EEB(v=0.9):
            return {'brain.intermitter_params.EEB': v}

        fee=aux.AttrDict({'brain.feeder_params': cd(MD.feeder.default, excluded=['dt', 'phi'], included={'mode': 'default'}),
                    'brain.intermitter_params.feed_bouts': True, **EEB(v=0.5)})
        def feed_kws(v=0.5):
            D = fee.get_copy()
            D['brain.intermitter_params.EEB']=v
            return D



        def extend(id0):
            for sg, g in zip(['', '0', '_x2'], [{'Odor': 150.0}, {'Odor': 0.0}, {'CS': 150.0, 'UCS': 0.0}]):
                for sb, br in zip(['', '_brute'], [False,True]):
                    idd=f'{id0}_nav{sg}{sb}'
                    o=olf_kws(g=g, brute_force=br)
                    new(id=idd, id0=id0,kws= o)
                    for k in ['RL', 'MB']:
                        new(id=f'{idd}_{k}', id0=id0, kws={**o, **mem[k]})

            for ss, eeb in zip(['', '_max'], [0.5, 0.9]):
                f = feed_kws(eeb)
                new(id=f'{id0}{ss}_feeder', id0=id0, kws=f)
                for sg, g in zip(['', '0', '_x2'], [{'Odor': 150.0}, {'Odor': 0.0}, {'CS': 150.0, 'UCS': 0.0}]):
                    # for sb, br in zip(['', '_brute'], [False, True]):
                    idd = f'{id0}{ss}_forager{sg}'
                    o = olf_kws(g=g)
                    new(id=idd, id0=id0, kws={**o, **f})
                    for k in ['RL', 'MB']:
                        new(id=f'{idd}_{k}', id0=id0, kws={**o, **f, **mem[k]})

            for mm in [f'{id0}_avg', f'{id0}_var', f'{id0}_var2']:
                if mm in reg.conf.Model.confIDs:
                    E[mm] = reg.conf.Model.getID(mm)
        kws = {'modkws': {'interference': {'attenuation': 0.1, 'attenuation_max': 0.6}}}
        kws2 = {'modkws': {'interference': {'attenuation': 0.0}, 'intermitter': {'run_mode': 'exec'}}}

        E['explorer'] = self.larvaConf(**kws)

        for id0, mkws in zip(['Levy', 'NEU_Levy', 'NEU_Levy_continuous'], [{'turner': 'sinusoidal', 'interference': 'default', 'intermitter': 'default'},
                                                                                     {'turner': 'neural', 'interference': 'default', 'intermitter': 'default'},
                                                                                     {'turner': 'neural', 'interference': 'default'}]):

            mkws2=kws2 if 'interference' in mkws else {}
            E[id0] = self.larvaConf(modes={'crawler': 'constant', **mkws}, **mkws2)
            extend(id0=id0)

        newexp('imitator', {'body.Nsegs': 11})
        newexp('zebrafish', {'body.body_plan': 'zebrafish_larva','Box2D_params': {'joint_types': {
                                          'revolute': {'N': 1, 'args': {'maxMotorTorque': 10 ** 5, 'motorSpeed': 1}}}}})
        newexp('thermo_navigator', sensor_kws('thermosensor'))


        mD = {'realistic': 'RE', 'square': 'SQ', 'gaussian': 'GAU', 'constant': 'CON',
              'default': 'DEF', 'neural': 'NEU', 'sinusoidal': 'SIN', 'nengo': 'NENGO', 'phasic': 'PHI',
              'branch': 'BR'}


        for Cm in MD.crawler.keylist:
            for Tm in MD.turner.keylist:
                for Ifm in MD.interference.keylist:
                    for IMm in MD.intermitter.keylist:
                        kkws = {
                            'modes': {'crawler': Cm, 'turner': Tm, 'interference': Ifm, 'intermitter': IMm},
                            'nengo': True if IMm == 'nengo' else False
                        }
                        if Ifm != 'default':
                            kkws.update(**kws)
                        id0=f'{mD[Cm]}_{mD[Tm]}_{mD[Ifm]}_{mD[IMm]}'
                        E[id0] = self.larvaConf(**kkws)
                        if Cm=='realistic' and IMm=='default' :
                            extend(id0=id0)

                        if id0=='RE_NEU_PHI_DEF':
                            E['navigator'] = E[f'{id0}_nav']
                            E['navigator_x2'] = E[f'{id0}_nav_x2']

                            E['noMB_untrained'] = E[f'{id0}_max_forager0']
                            E['noMB_trained'] = E[f'{id0}_max_forager']
                            E['MB_untrained'] = E[f'{id0}_max_forager0_MB']
                            E['MB_trained'] = E[f'{id0}_max_forager_MB']
                            E['forager'] = E[f'{id0}_forager']
                            E['forager_x2'] = E[f'{id0}_forager_x2']
                            E['max_forager'] = E[f'{id0}_max_forager']
                            E['feeder'] = E[f'{id0}_feeder']
                            E['max_feeder'] = E[f'{id0}_max_feeder']

                            E['RLnavigator'] = E[f'{id0}_nav_RL']
                            E['RLforager'] = E[f'{id0}_forager_RL']


        newexp('OSNnavigator', olf_kws(mode='osn'))
        newexp('OSNnavigator_x2', olf_kws({'CS': 150.0, 'UCS': 0.0}, mode='osn'))
        newexp('toucher', sensor_kws('toucher'))
        newexp('toucher_2', sensor_kws('toucher', touch_sensors=[0, 2]))
        newexp('toucher_brute', sensor_kws('toucher', brute_force=True))
        new('RLtoucher', 'toucher', mem_kws(modality='touch'))
        new('RLtoucher_2', 'toucher_2', mem_kws(modality='touch'))
        newfor('follower-R', OD({'Left_odor': 150.0, 'Right_odor': 0.0}))
        newfor('follower-L', OD({'Left_odor': 0.0, 'Right_odor': 150.0}))
        newfor('gamer', OD({'Flag_odor': 150.0, 'Left_base_odor': 0.0, 'Right_base_odor': 0.0}))
        newfor('gamer-5x', OD({'Flag_odor': 150.0, 'Left_base_odor': 0.0, 'Right_base_odor': 0.0, 'Left_odor': 0.0, 'Right_odor': 0.0}))

        newnav('immobile', {'brain.crawler_params': None, 'brain.turner_params': None,
                            'brain.intermitter_params': None, 'brain.interference_params': None,
                            **sensor_kws('toucher')})
        newnav('obstacle_avoider', {'sensorimotor': cd(ObstacleLarvaRobot, excluded=[LarvaRobot])})

        for id in ['explorer', 'navigator', 'feeder', 'forager']:
            new(f'{id}_sample', id, {k: 'sample' for k in [
                'brain.crawler_params.stride_dst_mean',
                'brain.crawler_params.stride_dst_std',
                'brain.crawler_params.max_scaled_vel',
                'brain.crawler_params.max_vel_phase',
                'brain.crawler_params.freq',
            ]})

        for sp, k_abs, eeb in zip(['rover', 'sitter'], [0.8, 0.4], [0.67, 0.37]):
            en_ws = {'energetics': aux.AttrDict({
                'DEB': cd(DEB, excluded=[DEB_model, 'substrate', 'id'], species=sp),
                'gut': cd(Gut, k_abs=k_abs)
            })}
            newexp(f'{sp}_explorer', en_ws)
            newnav(f'{sp}_navigator', en_ws)
            new(f'{sp}_feeder', 'feeder', {**en_ws, **EEB(eeb)})
            newfor(f'{sp}_forager', {**en_ws, **EEB(eeb)})
            new(sp, f'{sp}_feeder')

        return E

    def build_full_dict(self):
        D = self.dict
        FD = aux.AttrDict()

        def register(dic, k0):
            for k, p in dic.items():
                kk = f'{k0}.{k}'
                if isinstance(p, param.Parameterized):
                    FD[kk] = p
                else:
                    register(p, kk)

        for aux_key in D.aux.keys:
            if aux_key in ['energetics', 'sensorimotor']:
                continue
            register(D.aux.m[aux_key].args, aux_key)
        for aux_key in ['energetics', 'sensorimotor']:
            for m, mdic in D.aux.m[aux_key].mode.items():
                register(mdic.args, f'{aux_key}.{m}')

        for bkey in D.brain.keys:
            bdic = D.brain.m[bkey]
            for mod in bdic.mode.keys():
                register(bdic.mode[mod].args, f'brain.{bkey}_params')

        return FD

    def diff_df(self, mIDs, ms=None, dIDs=None):
        from ..model import ModuleColorDict
        dic = {}
        if dIDs is None:
            dIDs = mIDs
        if ms is None:
            ms = [reg.conf.Model.getID(mID) for mID in mIDs]
        ms = [m.flatten() for m in ms]
        ks = aux.unique_list(aux.flatten_list([m.keylist for m in ms]))

        for k in ks:
            entry = {dID: m[k] if k in m else None for dID, m in zip(dIDs, ms)}
            l = list(entry.values())
            if all([a == l[0] for a in l]):
                continue
            else:
                if k in self.full_dict:
                    k0 = self.full_dict[k].disp
                else:
                    k0 = k.split('.')[-1]
                k00 = k.split('.')[0]
                if k00 == 'brain':
                    k01 = k.split('.')[1]
                    k00 = k01.split('_')[0]
                entry['field'] = k00
                dic[k0] = entry
        df = pd.DataFrame.from_dict(dic).T
        df.index = df.index.set_names(['parameter'])
        df.reset_index(drop=False, inplace=True)
        df.set_index(['field'], inplace=True)
        df.sort_index(inplace=True)

        row_colors = [None] + [ModuleColorDict[ii] for ii in df.index.values]
        df.index = arrange_index_labels(df.index)

        return df, row_colors

    def adapt_crawler(self, e, mode='realistic'):
        mdict = self.dict.model.m['crawler'].mode[mode].args
        crawler_conf = aux.AttrDict({'mode': mode})
        for d, p in mdict.items():
            if isinstance(p, param.Parameterized) and p.codename in e.columns:
                crawler_conf[d] = np.round(e[p.codename].dropna().median(), 2)
        return crawler_conf

    def adapt_intermitter(self, e, c, conf, mode='default'):
        conf.stridechain_dist = c.bout_distros.run_count
        try:
            ll1, ll2 = conf.stridechain_dist.range
            conf.stridechain_dist.range = (int(ll1), int(ll2))
        except:
            pass

        conf.run_dist = c.bout_distros.run_dur
        try:
            ll1, ll2 = conf.run_dist.range
            conf.run_dist.range = (np.round(ll1, 2), np.round(ll2, 2))
        except:
            pass
        conf.pause_dist = c.bout_distros.pause_dur
        try:
            ll1, ll2 = conf.pause_dist.range
            conf.pause_dist.range = (np.round(ll1, 2), np.round(ll2, 2))
        except:
            pass
        conf.crawl_freq = np.round(e[reg.getPar('fsv')].dropna().median(), 2)
        conf.mode = mode
        return conf

    def adapt_mID(self, dataset, mID0, mID, space_mkeys=['turner', 'interference'], dir=None, **kwargs):
        s, e, c = dataset.data
        CM = reg.conf.Model
        print(f'Adapting {mID0} on {c.refID} as {mID} fitting {space_mkeys} modules')
        if dir is None:
            dir = f'{c.dir}/model/GAoptimization'
        m0 = CM.getID(mID0)
        if 'crawler' not in space_mkeys:
            m0.brain.crawler_params = self.adapt_crawler(e=e, mode=m0.brain.crawler_params.mode)
        if 'intermitter' not in space_mkeys:
            m0.brain.intermitter_params = self.adapt_intermitter(e=e, c=c, mode=m0.brain.intermitter_params.mode,
                                                                 conf=m0.brain.intermitter_params)
        m0.body.length = np.round(e[reg.getPar('l')].dropna().median(), 5)
        CM.setID(mID, m0)

        from ..sim.genetic_algorithm import optimize_mID, GAselector
        GAselector.param.objects()['base_model'].objects = CM.confIDs
        reg.generators.LarvaGroupMutator.param.objects()['modelIDs'].objects = CM.confIDs
        return optimize_mID(mID0=mID, space_mkeys=space_mkeys, dt=c.dt, refID=c.refID,
                            dataset=dataset, id=mID, dir=dir, **kwargs)

    def update_mdict(self, mdict, mmdic):
        if mmdic is None:
            return None
        else:
            for d, p in mdict.items():
                new_v = mmdic[d] if d in mmdic.keys() else None
                if isinstance(p, param.Parameterized):
                    if type(new_v) == list:
                        if p.parclass in [param.Range, param.NumericTuple, param.Tuple]:
                            new_v = tuple(new_v)
                    p.v = new_v
                else:
                    mdict[d] = self.update_mdict(mdict=p, mmdic=new_v)
            return mdict

    def variable_mdict(self, mkey, mode='default'):
        D = self.dict.model
        var_ks = D.init[mkey].mode[mode].variable
        d00 = D.m[mkey].mode[mode].args
        return aux.AttrDict({k: d00[k] for k in var_ks})

    def space_dict(self, mkeys, mConf0):
        mF = mConf0.flatten()
        dic = {}
        for mkey in mkeys:
            d0 = self.dict.model.init[mkey]
            if f'{d0.pref}mode' in mF.keys():
                mod_v = mF[f'{d0.pref}mode']
            else:
                mod_v = 'default'
            var_mdict = self.variable_mdict(mkey, mode=mod_v)
            for k, p in var_mdict.items():

                k0 = f'{d0.pref}{k}'

                if k0 in mF.keys():
                    dic[k0] = p
                    if type(mF[k0]) == list:
                        if dic[k0].parclass == param.Range:
                            mF[k0] = tuple(mF[k0])
                    dic[k0].v = mF[k0]
        return aux.AttrDict(dic)
