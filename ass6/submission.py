import numpy as np
import operator


def gaussian_prob(x, para_tuple):
    """Compute the probability of a given x value

    Args:
        x (float): observation value
        para_tuple (tuple): contains two elements, (mean, standard deviation)

    Return:
        Probability of seeing a value "x" in a Gaussian distribution.

    Note:
        We simplify the problem so you don't have to take care of integrals.
        Theoretically speaking, the returned value is not a probability of x,
        since the probability of any single value x from a continuous 
        distribution should be zero, instead of the number outputed here.
        By definition, the Gaussian percentile of a given value "x"
        is computed based on the "area" under the curve, from left-most to x. 
        The proability of getting value "x" is zero bcause a single value "x"
        has zero width, however, the probability of a range of value can be
        computed, for say, from "x - 0.1" to "x + 0.1".

    """
    if para_tuple == (None, None):
        return 0.0

    mean, std = para_tuple
    gaussian_percentile = (2 * np.pi * std**2)**-0.5 * \
                          np.exp(-(x - mean)**2 / (2 * std**2))
    return gaussian_percentile


def part_1_a():
    """Provide probabilities for the word HMMs outlined below.
    Word ALLIGATOR, NUTS, and SLEEP.
    Review Udacity Lesson 8 - Video #29. HMM Training
    Returns:
        tuple() of
        (prior probabilities for all states for word ALLIGATOR,
         transition probabilities between states for word ALLIGATOR,
         emission parameters tuple(mean, std) for all states for word ALLIGATOR,
         prior probabilities for all states for word NUTS,
         transition probabilities between states for word NUTS,
         emission parameters tuple(mean, std) for all states for word NUTS,
         prior probabilities for all states for word SLEEP,
         transition probabilities between states for word SLEEP,
         emission parameters tuple(mean, std) for all states for word SLEEP)
        Sample Format (not complete):
        (
            {'A1': prob_of_starting_in_A1, 'A2': prob_of_starting_in_A2, ...},
            {'A1': {'A1': prob_of_transition_from_A1_to_A1,
                    'A2': prob_of_transition_from_A1_to_A2,
                    'A3': prob_of_transition_from_A1_to_A3,
                    'Aend': prob_of_transition_from_A1_to_Aend},
             'A2': {...}, ...},
            {'A1': tuple(mean_of_A1, standard_deviation_of_A1),
             'A2': tuple(mean_of_A2, standard_deviation_of_A2), ...},
            {'N1': prob_of_starting_in_N1, 'N2': prob_of_starting_in_N2, ...},
            {'N1': {'N1': prob_of_transition_from_N1_to_N1,
                    'N2': prob_of_transition_from_N1_to_N2,
                    'N3': prob_of_transition_from_N1_to_N3,
                    'Nend': prob_of_transition_from_N1_to_Nend},
             'N2': {...}, ...}
            {'N1': tuple(mean_of_N1, standard_deviation_of_N1),
             'N2': tuple(mean_of_N2, standard_deviation_of_N2), ...},
            {'S1': prob_of_starting_in_S1, 'S2': prob_of_starting_in_S2, ...},
            {'S1': {'S1': prob_of_transition_from_S1_to_S1,
                    'S2': prob_of_transition_from_S1_to_S2,
                    'S3': prob_of_transition_from_S1_to_S3,
                    'Send': prob_of_transition_from_S1_to_Send},
             'S2': {...}, ...}
            {'S1': tuple(mean_of_S1, standard_deviation_of_S1),
             'S2': tuple(mean_of_S2, standard_deviation_of_S2), ...} 
        )
    """

    # TODO: complete this function.͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
    raise NotImplementedError()

    """Word ALLIGATOR"""
    a_prior_probs = {
        'A1': 0.,
        'A2': 0.,
        'A3': 0.,
        'Aend': 0.
    }
    a_transition_probs = {
        'A1': {'A1': 0., 'A2': 0., 'A3': 0., 'Aend': 0.},
        'A2': {'A3': 0., 'A2': 0., 'A1': 0., 'Aend': 0.},
        'A3': {'A1': 0., 'A2': 0., 'A3': 0., 'Aend': 0.},
        'Aend': {'A1': 0., 'A2': 0., 'A3': 0., 'Aend': 0.}
    }
    # Parameters for end state is not required͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
    a_emission_paras = {
        'A1': (None, None),
        'A2': (None, None),
        'A3': (None, None),
        'Aend': (None, None)
    }

    """Word NUTS"""
    n_prior_probs = {
        'N1': 0.,
        'N2': 0.,
        'N3': 0.,
        'Nend': 0.
    }
    # Probability of a state changing to another state.͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
    n_transition_probs = {
        'N1': {'N1': 0., 'N3': 0., 'N2': 0., 'Nend': 0.},
        'N2': {'N3': 0., 'N2': 0., 'N1': 0., 'Nend': 0.},
        'N3': {'N1': 0., 'N3': 0., 'N2': 0., 'Nend': 0.},
        'Nend': {'N3': 0., 'N2': 0., 'N1': 0., 'Nend': 0.}
    }
    # Parameters for end state is not required͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
    n_emission_paras = {
        'N1': (None, None),
        'N2': (None, None),
        'N3': (None, None),
        'Nend': (None, None)
    }

    """Word SLEEP"""
    s_prior_probs = {
        'S1': 0.,
        'S2': 0.,
        'S3': 0.,
        'Send': 0.
    }
    s_transition_probs = {
        'S1': {'S3': 0., 'S1': 0., 'S2': 0., 'Send': 0.},
        'S2': {'S3': 0., 'S1': 0., 'S2': 0., 'Send': 0.},
        'S3': {'S3': 0., 'S2': 0., 'S1': 0., 'Send': 0.},
        'Send': {'S1': 0., 'S2': 0., 'S3': 0., 'Send': 0.}
    }
    # Parameters for end state is not required͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
    s_emission_paras = {
        'S1': (None, None),
        'S2': (None, None),
        'S3': (None, None),
        'Send': (None, None)
    }

    return (a_prior_probs, a_transition_probs, a_emission_paras,
            n_prior_probs, n_transition_probs, n_emission_paras,
            s_prior_probs, s_transition_probs, s_emission_paras)



def viterbi(evidence_vector, states, prior_probs,
            transition_probs, emission_paras):
    """Viterbi Algorithm to calculate the most likely states give the evidence.
    Args:
        evidence_vector (list): List of right hand Y-axis positions (integer).
        states (list): List of all states in a word. No transition between words.
                       example: ['A1', 'A2', 'A3', 'Aend', 'N1', 'N2', 'N3', 'Nend']
        prior_probs (dict): prior distribution for each state.
                            example: {'X1': 0.25,
                                      'X2': 0.25,
                                      'X3': 0.25,
                                      'Xend': 0.25}
        transition_probs (dict): dictionary representing transitions from each
                                 state to every other valid state such as for the above 
                                 states, there won't be a transition from 'A1' to 'N1'
        emission_paras (dict): parameters of Gaussian distribution 
                                from each state.
    Return:
        tuple of
        ( A list of states the most likely explains the evidence,
          probability this state sequence fits the evidence as a float )
    Note:
        You are required to use the function gaussian_prob to compute the
        emission probabilities.
    """
    
    # TODO: complete this function.͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
    raise NotImplementedError()

    sequence = []
    probability = 0.0

    return sequence, probability


def part_2_a():
    """Provide probabilities for the word HMMs outlined below.
    Now, at each time frame you are given 2 observations (right hand Y
    position & right thumb Y position). Use the result you derived in
    part_1_a, accompany with the provided probability for right thumb, create
    a tuple of (right-hand-y, right-thumb-y) to represent high-dimension transition & 
    emission probabilities.
    """

     # TODO: complete this function.͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
    raise NotImplementedError()

    """Word ALLIGATOR"""
    a_prior_probs = {
        'A1': 0.,
        'A2': 0.,
        'A3': 0.,
        'Aend': 0.
    }
    # example: {'A1': {'A1' : (right-hand Y, right-thumb Y), ... }͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
    a_transition_probs = {
        'A1': {'A1': (0., 0.), 'A2': (0., 0.), 'A3': (0., 0.), 'Aend': (0., 0.)},
        'A2': {'A1': (0., 0.), 'A2': (0., 0.), 'A3': (0., 0.), 'Aend': (0., 0.)},
        'A3': {'A3': (0., 0.), 'A2': (0., 0.), 'A1': (0., 0.), 'Aend': (0., 0.)},
        'Aend': {'A2': (0., 0.), 'A1': (0., 0.), 'A3': (0., 0.), 'Aend': (0., 0.)}
    }
    # example: {'A1': [(right-hand-mean, right-hand-std), (right-thumb-mean, right-thumb-std)] ...}͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
    a_emission_paras = {
        'A1': [(None, None), (None, None)],
        'A2': [(None, None), (None, None)],
        'A3': [(None, None), (None, None)],
        'Aend': [(None, None), (None, None)]
    }

    """Word NUTS"""
    n_prior_probs = {
        'N1': 0.,
        'N2': 0.,
        'N3': 0.,
        'Nend': 0.
    }
    n_transition_probs = {
        'N1': {'N2': (0., 0.), 'N3': (0., 0.), 'N1': (0., 0.), 'Nend': (0., 0.)},
        'N2': {'N1': (0., 0.), 'N3': (0., 0.), 'N2': (0., 0.), 'Nend': (0., 0.)},
        'N3': {'N1': (0., 0.), 'N2': (0., 0.), 'N3': (0., 0.), 'Nend': (0., 0.)},
        'Nend': {'N2': (0., 0.), 'N3': (0., 0.), 'N1': (0., 0.), 'Nend': (0., 0.)}
    }
    n_emission_paras = {
        'N1': [(None, None), (None, None)],
        'N2': [(None, None), (None, None)],
        'N3': [(None, None), (None, None)],
        'Nend': [(None, None), (None, None)]
    }

    """Word SLEEP"""
    s_prior_probs = {
        'S1': 0.,
        'S2': 0.,
        'S3': 0.,
        'Send': 0.
    }
    s_transition_probs = {
        'S1': {'S1': (0., 0.), 'S2': (0., 0.), 'S3': (0., 0.), 'Send': (0., 0.)},
        'S2': {'S3': (0., 0.), 'S2': (0., 0.), 'S1': (0., 0.), 'Send': (0., 0.)},
        'S3': {'S1': (0., 0.), 'S2': (0., 0.), 'S3': (0., 0.), 'Send': (0., 0.)},
        'Send': {'S1': (0., 0.), 'S2': (0., 0.), 'S3': (0., 0.), 'Send': (0., 0.)}
    }
    s_emission_paras = {
        'S1': [(None, None), (None, None)],
        'S2': [(None, None), (None, None)],
        'S3': [(None, None), (None, None)],
        'Send': [(None, None), (None, None)]
    }

    return (a_prior_probs, a_transition_probs, a_emission_paras,
            n_prior_probs, n_transition_probs, n_emission_paras,
            s_prior_probs, s_transition_probs, s_emission_paras)


def multidimensional_viterbi(evidence_vector, states, prior_probs,
                             transition_probs, emission_paras):
    """Decode the most likely word phrases generated by the evidence vector.

    States, prior_probs, transition_probs, and emission_probs will now contain
    all the words from part_2_a.
    """
    # TODO: complete this function.͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
    raise NotImplementedError()

    sequence = []
    probability = 0.0

    return sequence, probability


def return_your_name():
    """Return your name
    """
    # TODO: finish this͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
    raise NotImplementedError()

