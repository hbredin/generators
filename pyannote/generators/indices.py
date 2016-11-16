#!/usr/bin/env python
# encoding: utf-8

# The MIT License (MIT)

# Copyright (c) 2016 CNRS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# AUTHORS
# Hervé BREDIN - http://herve.niderb.fr


import warnings
import numpy as np


def random_label_index(y, per_label=3, return_label=False):
    """
    a 'for' loop is worth a thousand words:

    >>> y = [1, 1, 2, 1, 3, 3, 3, 1, 1, 1, 2, 2, 2, 4, 4, 3, 3, 4]
    >>> iterable = random_label_sequence(y, per_label=2)
    >>> for _ in range(10):
    ...     i = next(iterable)
    ...     print i, '==>', y[i]
    2 ==> 2
    10 ==> 2
    13 ==> 4
    14 ==> 4
    4 ==> 3
    5 ==> 3
    0 ==> 1
    1 ==> 1
    11 ==> 2
    12 ==> 2
    """

    # unique labels
    unique, y, counts = np.unique(y, return_inverse=True, return_counts=True)
    n_labels = len(unique)

    # warn that some labels have very few training samples
    too_few_samples = np.sum(counts < per_label)
    if too_few_samples > 0:
        msg = '{n} labels (out of {N}) have less than {per_label} training samples.'
        warnings.warn(msg.format(n=too_few_samples,
                                 N=n_labels,
                                 per_label=per_label))

    shuffled_sequences = [np.where(y == label)[0] for label in range(n_labels)]
    consumed = [0 for label in range(n_labels)]

    # infinite loop
    while True:

        # consume all labels in random order
        for label in np.random.choice(n_labels, size=n_labels, replace=False):

            # consume 'per_label' sequences from current label
            # using pre-shuffled order
            for _ in range(per_label):

                i = shuffled_sequences[label][consumed[label]]
                if return_label:
                    yield i, unique[label]
                else:
                    yield i

                consumed[label] += 1

                # if all sequences from current label have been consumed
                # reshuffle them and start fresh
                if consumed[label] + 1 > counts[label]:
                    consumed[label] = 0
                    np.random.shuffle(shuffled_sequences[label])
