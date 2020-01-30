# MIT License
#
# Copyright (C) IBM Corporation 2018
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import unittest

from os.path import dirname, join
import numpy as np

import tensorflow as tf

tf.compat.v1.disable_eager_execution()
from tensorflow.keras.models import load_model

from art.attacks import FunctionallyEquivalentExtraction
from art.classifiers import KerasClassifier

from tests.utils import TestBase, master_seed

logger = logging.getLogger(__name__)


@unittest.skipIf(tf.__version__[0] != '2' or (tf.__version__[0] == '1' and tf.__version__.split('.')[1] != '15'),
                 reason='Skip unittests if not TensorFlow v2 or 1.15 because of pre-trained model.')
class TestFastGradientMethodImages(TestBase):

    @classmethod
    def setUpClass(cls):
        master_seed(seed=1234, set_tensorflow=True)
        super().setUpClass()

        cls.n_train = 100
        cls.n_test = 11
        cls.x_train_mnist = cls.x_train_mnist[0:cls.n_train]
        cls.y_train_mnist = cls.y_train_mnist[0:cls.n_train]
        cls.x_test_mnist = cls.x_test_mnist[0:cls.n_test]
        cls.y_test_mnist = cls.y_test_mnist[0:cls.n_test]

        model = load_model(join(join(join(dirname(dirname(dirname(__file__))), 'data'), 'test_models'),
                                'model_test_functionally_equivalent_extraction.h5'))

        np.random.seed(0)
        num_neurons = 16
        img_rows = 28
        img_cols = 28
        num_channels = 1

        x_train = cls.x_train_mnist.reshape(cls.n_train, img_rows, img_cols, num_channels)
        x_test = cls.x_test_mnist.reshape(cls.n_test, img_rows, img_cols, num_channels)

        x_train = x_train.reshape((x_train.shape[0], num_channels * img_rows * img_cols)).astype('float64')
        x_test = x_test.reshape((x_test.shape[0], num_channels * img_rows * img_cols)).astype('float64')

        mean = np.mean(x_train)
        std = np.std(x_train)

        x_test = (x_test - mean) / std

        classifier = KerasClassifier(model=model, use_logits=True, clip_values=(0, 1))

        cls.fee = FunctionallyEquivalentExtraction(classifier=classifier, num_neurons=num_neurons)
        cls.fee.extract(x_test[0:100])

    def setUp(self):
        master_seed(seed=1234, set_tensorflow=True)
        super().setUp()

    def test_critical_points(self):
        critical_points_expected_15 = np.array([[3.61953106e+00, 9.77733178e-01, 3.03710564e+00,
                                                 3.88522344e+00, -3.42297003e+00, -1.13835691e+00,
                                                 -1.99857599e+00, -3.46220468e-01, -3.59475588e+00,
                                                 5.51705510e+00, -3.19797872e+00, -2.04326002e+00,
                                                 1.05123266e+00, -4.06901743e+00, -1.20838338e+00,
                                                 -2.89548673e+00, 6.98455648e+00, 2.85218553e+00,
                                                 8.94698139e-02, -2.37621231e+00, 1.10785852e+00,
                                                 2.23015480e+00, 2.80221937e+00, -8.44071720e-01,
                                                 -4.29867814e+00, -1.89193948e+00, -2.02601143e+00,
                                                 2.32254653e+00, 5.46957626e+00, -1.09054547e+00,
                                                 1.97730390e+00, 7.13198416e+00, -3.48566995e+00,
                                                 4.56309251e+00, -3.66508619e+00, 2.45678983e-01,
                                                 1.18692621e+00, 1.24711887e+00, -3.64649874e+00,
                                                 -2.60243153e+00, -3.64646660e+00, -1.47897557e-01,
                                                 -4.22195494e-01, 1.06113047e+01, 4.82448414e+00,
                                                 -2.42173234e+00, 1.11818199e-02, 4.65699866e+00,
                                                 -1.49483467e+00, -4.83696263e-01, -6.94802825e-01,
                                                 3.76123427e+00, -3.81138399e+00, -2.44772137e+00,
                                                 1.80214210e+00, 1.64008567e+00, 9.98667003e-01,
                                                 -1.13632143e+00, 3.14954375e+00, 7.93954578e+00,
                                                 9.08789028e-01, -1.11114990e+00, 2.12722866e+00,
                                                 -3.82389751e+00, -2.73941016e+00, -2.74131238e-01,
                                                 -1.16791406e+01, -4.02691717e+00, -2.26112102e+00,
                                                 -5.21371365e+00, -3.28863610e+00, -1.57028321e+00,
                                                 -5.25291961e+00, -2.81473806e+00, -1.68024547e+00,
                                                 -5.85965502e-01, 3.61981141e+00, 9.23169673e-02,
                                                 -2.29606074e-01, 4.43114931e-01, -2.80427895e-01,
                                                 -3.05502037e+00, 1.91036227e-02, -3.34978609e-01,
                                                 -3.84499306e+00, 5.26390356e+00, 5.38611250e+00,
                                                 -2.63643293e+00, -2.00973074e+00, -2.36234227e+00,
                                                 2.31791770e+00, -2.90647524e+00, -6.57321096e-01,
                                                 -2.36517907e+00, 5.54615295e-01, -6.27427313e+00,
                                                 5.17139277e+00, -1.96714440e+00, 3.59945621e-01,
                                                 -4.24878604e-01, -1.08202458e+00, -4.80186427e+00,
                                                 2.37278089e+00, -1.07572442e+00, -1.18075753e-01,
                                                 -1.17477993e+00, -2.93162165e+00, 1.08992730e+00,
                                                 5.54290231e+00, 7.98407506e-01, -3.66473517e+00,
                                                 8.67953522e+00, -4.19382044e+00, -4.08782220e+00,
                                                 9.82618000e+00, -7.69520713e-01, -4.73994274e+00,
                                                 -2.81408385e+00, 2.04409418e+00, 1.66265593e+00,
                                                 -2.93741552e+00, 5.99230900e+00, -1.73108306e+00,
                                                 -3.28289962e+00, 3.04322254e+00, 5.02137877e+00,
                                                 -3.61579148e+00, -3.60298823e+00, 4.68144302e+00,
                                                 -7.55810404e+00, -5.54235927e+00, 4.30331267e+00,
                                                 -8.89694006e-01, -9.95076143e-01, 7.36865058e-01,
                                                 8.20305695e-02, -4.47623746e+00, 4.75655495e+00,
                                                 5.55126730e+00, -2.94169700e-01, -1.31565371e+00,
                                                 9.54222010e+00, -9.08849702e-01, -3.74910292e-01,
                                                 3.80123979e+00, 6.66898337e+00, 5.28420510e+00,
                                                 1.10982206e-01, -1.16276421e-01, -5.82332350e+00,
                                                 -1.28205374e+00, -1.55599314e+00, -4.66205671e+00,
                                                 5.71610805e+00, -3.18101923e+00, -2.73180879e+00,
                                                 2.55005165e+00, 3.96954509e+00, 7.24416286e-01,
                                                 1.02980621e+01, -7.88544755e-01, 2.93612566e+00,
                                                 2.02170626e+00, 5.67092866e+00, 7.48089944e-01,
                                                 3.92145589e-01, -4.68662954e+00, -5.93709701e-01,
                                                 6.64027217e+00, -1.27973863e+00, 2.97883110e+00,
                                                 1.27642013e+00, 4.21654506e+00, -3.78209823e+00,
                                                 8.09590708e+00, -4.29526503e+00, -2.22566713e+00,
                                                 2.96030699e+00, 6.98973613e-01, 3.24672410e+00,
                                                 -2.28418990e+00, -1.66599664e+00, -5.96027162e-01,
                                                 3.88214888e+00, 3.31149846e+00, 1.49757160e+00,
                                                 -3.66419049e+00, 3.82181754e+00, 1.38112419e-01,
                                                 6.94779206e+00, 6.54329012e+00, -9.26489313e-01,
                                                 -1.62009512e+00, -4.52985187e+00, -3.53512243e-02,
                                                 -1.65790094e+00, 2.17052203e+00, 2.61034940e-01,
                                                 7.56353874e-01, 5.47853217e+00, -4.01821256e+00,
                                                 1.44572322e+00, -4.79746586e-01, 3.47357980e+00,
                                                 6.02979833e+00, -2.79622692e+00, 1.69161006e+00,
                                                 -4.23976729e-02, -2.83040527e+00, 8.38686737e-01,
                                                 2.03506626e+00, 1.92358357e+00, 1.44131202e-02,
                                                 -9.99430943e-02, -5.40948077e+00, -1.80337181e+00,
                                                 2.14607550e+00, 3.85151903e+00, 6.16199609e-01,
                                                 3.65155968e-01, -6.86530386e-02, 4.37920573e-01,
                                                 1.64040341e+00, -6.59215215e+00, -1.73270323e+00,
                                                 9.93275152e-01, -3.73550020e+00, 6.74519312e+00,
                                                 3.12660362e-02, 5.84485063e+00, -4.49976578e+00,
                                                 -4.02337192e+00, 3.29641448e-01, -6.11525876e+00,
                                                 -3.19811199e-01, 1.15945105e+00, 5.44615523e+00,
                                                 6.57571553e-01, -1.19802935e+00, -3.59314573e+00,
                                                 6.02466561e+00, -3.47917071e+00, -4.20072539e+00,
                                                 -4.51866361e+00, 4.03811078e+00, -3.69489996e+00,
                                                 -1.78012256e+00, 1.61533135e+00, -1.61852848e+00,
                                                 -4.10470488e+00, 3.45463564e+00, 3.56905786e+00,
                                                 3.97554912e+00, 2.66454239e+00, 2.25804254e+00,
                                                 -6.21473638e+00, 5.76899253e+00, -2.08408059e-01,
                                                 7.83228855e-01, 4.94838720e+00, 4.38791606e+00,
                                                 1.12105376e+00, 1.09827474e+00, -2.38398204e+00,
                                                 -1.80753680e+00, -3.13452494e+00, -2.27719704e+00,
                                                 -3.38822700e+00, -9.17931670e-01, 4.17912953e+00,
                                                 1.27364259e+01, -2.03530245e+00, -3.29038740e+00,
                                                 5.31179109e+00, -1.82267486e+00, -2.96119740e+00,
                                                 1.31020764e+00, -4.94302867e+00, -1.16514227e+00,
                                                 1.72064832e+00, 2.72220374e-01, 2.50415711e+00,
                                                 -4.29456275e-01, 1.59994399e+00, 1.39253228e+00,
                                                 2.22505196e+00, -5.05846429e+00, -4.35255236e+00,
                                                 4.50001673e-01, -4.27252846e+00, -2.87526989e-01,
                                                 3.17137548e+00, 4.66601910e+00, -5.13815490e+00,
                                                 -3.48299127e+00, 2.41422025e+00, -1.46361301e+00,
                                                 -6.49063866e-01, 1.92294782e+00, -3.47120162e+00,
                                                 -2.86761934e+00, -1.45476737e+00, -4.17669035e+00,
                                                 -4.01483069e+00, 3.30219967e+00, -2.59101087e-01,
                                                 -4.75482758e+00, -2.24586949e+00, -5.68236958e+00,
                                                 -3.01268930e+00, 8.22969417e+00, 7.26630125e-01,
                                                 1.71985527e+00, -9.85474778e-01, 9.69749700e-01,
                                                 2.67490406e+00, -4.33992693e+00, -4.07251552e-01,
                                                 6.08129826e+00, -3.20237632e+00, -2.92346407e+00,
                                                 -2.01013404e+00, 1.32121409e+00, 1.15139410e+00,
                                                 3.77379044e+00, 1.63111624e+00, -3.99098443e-01,
                                                 7.15579205e+00, 2.03479958e+00, -4.87601164e+00,
                                                 1.05765834e+01, 5.69732614e+00, 1.18778294e-01,
                                                 2.86462296e-01, 2.49353875e+00, -6.36657921e-02,
                                                 1.08570479e+00, 4.74854161e+00, -4.63241582e+00,
                                                 -6.83954662e-01, 4.65345281e+00, 1.33951496e+00,
                                                 2.90639747e+00, -1.72986262e+00, -1.56536140e+00,
                                                 -8.05650496e+00, -4.82346198e+00, 3.39824919e-01,
                                                 3.78664395e+00, 2.41632152e+00, -1.26309772e+00,
                                                 -2.49517893e+00, 2.20951730e+00, -3.85151265e-01,
                                                 4.81240175e+00, 4.85709334e-02, -7.60618498e+00,
                                                 -5.42914323e+00, 5.42941370e+00, -3.93630082e+00,
                                                 3.67290378e+00, -1.04039267e+00, 2.71366140e-01,
                                                 -1.81908310e-01, 4.73638654e+00, -5.89365669e-01,
                                                 -3.20289542e-01, -6.35077950e+00, 5.36441669e-01,
                                                 9.38127137e-01, 1.21089054e+00, 4.44570135e+00,
                                                 1.05628764e+00, 9.13779419e-01, 6.46336488e+00,
                                                 -5.53683667e+00, -1.13017499e+00, 3.97816303e+00,
                                                 3.43531407e+00, 3.51956691e+00, 1.54150627e+00,
                                                 1.65980399e+00, 4.09252687e+00, 4.47248858e-01,
                                                 9.71886644e-01, -1.03825118e+00, -2.35130810e-01,
                                                 -5.97346695e+00, 4.64660911e+00, -3.43276914e-01,
                                                 7.65585441e+00, -5.17010009e-01, 1.28424404e+00,
                                                 -6.57013775e-01, -2.72570553e+00, 3.09863582e+00,
                                                 8.26999588e+00, 1.08360782e+00, 2.97499462e-01,
                                                 -5.28765957e-01, -7.96130693e+00, -1.80771840e+00,
                                                 1.74322693e+00, 4.46006209e+00, 1.96673988e+00,
                                                 -1.26500012e+00, -2.62521339e-01, 4.43172806e+00,
                                                 -8.59953375e-01, -2.79203135e+00, 3.97136669e+00,
                                                 4.83725475e+00, -2.36000818e-01, -2.54368931e+00,
                                                 -6.09494471e+00, 2.97887357e+00, -3.11669990e+00,
                                                 -7.49438171e+00, 7.68609007e+00, 4.24065149e+00,
                                                 -3.50205849e+00, -4.14267291e+00, 1.29406661e+00,
                                                 -3.29221719e+00, 4.91285113e+00, 2.49242470e+00,
                                                 3.03079368e+00, -1.16511988e+00, 1.75569959e-01,
                                                 3.69572816e+00, -2.23354575e+00, -1.08249093e+00,
                                                 3.79457820e+00, 2.46730808e+00, -5.62046536e+00,
                                                 -1.63213742e+00, 1.80517373e+00, -1.58217893e+00,
                                                 7.70526692e+00, -1.45138939e+00, -1.02637577e+00,
                                                 1.83421798e+00, 1.20008006e+00, -3.70929508e-01,
                                                 -2.06747283e+00, 1.05799974e+00, 4.50025041e+00,
                                                 8.99414047e-01, -3.81032447e+00, 6.64691827e+00,
                                                 -6.68286008e+00, -5.33754112e+00, 4.20039092e+00,
                                                 1.15777816e+00, -1.79904165e+00, -2.25318912e+00,
                                                 8.56072151e+00, -1.74587332e+00, 2.27772815e+00,
                                                 1.18619882e+00, 1.17419760e+00, 1.12252724e+00,
                                                 2.41046828e+00, -1.27854741e+00, -1.63751443e+00,
                                                 -4.36138109e+00, -3.99645147e+00, 2.61707008e-01,
                                                 1.77727481e+00, 2.58218034e+00, -3.34194564e+00,
                                                 -5.45410857e+00, -1.10816013e+01, 3.77134811e+00,
                                                 -5.53653174e-01, -7.50458024e-01, 1.83105453e+00,
                                                 -6.35106143e+00, -2.32310964e-01, 8.36876665e+00,
                                                 2.73772575e+00, 2.42717722e+00, -7.06580844e+00,
                                                 8.30491238e+00, -4.67310265e+00, 4.82361105e+00,
                                                 -6.71576571e+00, 6.02101751e+00, 6.24969448e+00,
                                                 -2.98703859e+00, 6.14207232e-01, 1.78015104e+00,
                                                 -2.06596331e+00, -4.34009099e+00, -2.43064707e+00,
                                                 2.03098762e+00, -9.89714067e-01, -2.70977210e+00,
                                                 2.74338316e+00, 1.89889595e+00, -2.55656260e+00,
                                                 -4.70778279e+00, 3.13221251e+00, -2.32580294e+00,
                                                 3.85278333e-02, 5.55167173e+00, 3.21784728e-01,
                                                 -4.92260843e+00, -5.54069995e-01, -2.40504807e+00,
                                                 7.15357191e+00, -8.09982416e-01, -5.25778915e-01,
                                                 -7.71322963e-01, -4.04571082e-02, -7.44434946e+00,
                                                 -5.12893117e+00, -7.11996760e-01, 1.52709995e+00,
                                                 1.20660824e+00, -3.94659988e+00, -6.15942263e+00,
                                                 -3.24356676e+00, -2.71168115e+00, 2.23742176e+00,
                                                 -2.15833449e+00, 3.28171007e+00, -9.01288903e-01,
                                                 -3.36544690e+00, -4.90099212e-01, -5.28357599e+00,
                                                 2.83366162e+00, -1.94060483e+00, -1.96470570e+00,
                                                 -1.56417735e+00, -5.63317405e+00, -1.52587686e+00,
                                                 -2.94973969e+00, -1.71309668e+00, -3.43045944e-01,
                                                 -2.89876104e+00, -2.06482721e+00, 4.84964575e+00,
                                                 1.41788617e+00, 4.07125067e+00, 9.04277262e-01,
                                                 4.09024059e+00, -5.57238878e+00, 1.58954316e+00,
                                                 -1.10885879e-01, -2.21962753e+00, -3.10507445e+00,
                                                 -4.85573938e+00, 5.55346782e+00, -4.46137455e+00,
                                                 6.53561699e+00, -4.18305953e+00, -3.33538699e+00,
                                                 1.07412314e+00, -3.21736541e+00, 4.22297199e+00,
                                                 -1.33947330e+00, 2.06426759e+00, -5.54850513e+00,
                                                 2.50551073e+00, 2.09512318e+00, -3.22334697e+00,
                                                 1.08998132e+01, 2.11009614e+00, 9.43857355e+00,
                                                 6.67997823e+00, -2.56444394e+00, -1.56702883e+00,
                                                 -8.01844888e-01, -6.53025150e+00, -3.07115943e+00,
                                                 1.54471353e-01, 4.81876388e+00, -3.13769415e+00,
                                                 4.56491640e+00, -6.82529587e+00, -2.94109962e+00,
                                                 -2.92035453e+00, 2.23157087e+00, 1.22495482e+00,
                                                 3.27356600e+00, 2.78216232e+00, 1.39149304e+00,
                                                 1.12641226e+00, 3.13438737e+00, -1.44455956e+00,
                                                 3.45329504e+00, -7.25452537e+00, 5.16350338e-01,
                                                 -1.52840925e+00, 3.89239288e-01, 3.57665297e+00,
                                                 4.23851729e-01, 2.51386164e+00, 5.55541927e+00,
                                                 -3.65730975e-02, 4.97351340e+00, -2.21492629e+00,
                                                 2.06160783e-01, -3.43932949e+00, 3.46787764e+00,
                                                 1.50062470e+00, -3.63420781e+00, 7.16921221e-01,
                                                 3.67330490e+00, -1.89513701e+00, -4.99527599e+00,
                                                 1.11835198e+00, -6.81027303e+00, 2.85916379e+00,
                                                 -1.23450647e+00, -1.60211378e+00, 3.73671094e+00,
                                                 -4.02548447e+00, 6.06862004e+00, -1.19202728e+00,
                                                 -2.41783262e+00, 3.74904207e+00, 2.45508616e+00,
                                                 9.16190491e+00, -2.04793984e+00, -2.85129492e-01,
                                                 -4.08466337e+00, -1.34825047e+00, -2.80827325e+00,
                                                 -2.43332648e+00, -6.90362325e+00, 6.92712787e+00,
                                                 -5.88185198e+00, -1.13563946e+01, -4.22056384e+00,
                                                 -3.26737627e+00, -4.22009802e+00, 5.09351493e+00,
                                                 8.23654694e-01, 8.38630810e-03, 3.74246157e+00,
                                                 2.14720496e+00, 2.81112013e+00, -5.53460662e+00,
                                                 -2.43520405e+00, 3.62002815e+00, -9.93353240e+00,
                                                 -5.95111730e+00, 3.50146440e+00, -1.58161073e+00,
                                                 1.32153944e+00, 3.46545576e+00, -4.14140504e+00,
                                                 1.80779810e+00, 5.12518371e+00, 5.06350579e-01,
                                                 -5.12143943e+00, 3.05075730e+00, 1.52664403e+00,
                                                 1.17840650e+00, 1.52245045e+00, -1.11987154e+01,
                                                 3.52537880e+00, 6.58677184e+00, 1.04950075e+00,
                                                 7.26431734e-01, 3.78884361e+00, -6.88274613e-01,
                                                 2.91277585e+00, -5.39988722e-01, -4.86762086e+00,
                                                 -5.85324299e+00, -4.79646945e+00, -5.12261654e+00,
                                                 -3.76122380e+00, 5.91361431e+00, 3.95099716e+00,
                                                 -1.00882397e+00, -1.12282264e+00, -1.53472669e-01,
                                                 -1.42612392e+00, 1.01808498e+00, 3.89284850e+00,
                                                 -7.95528695e-01, -1.52721085e+00, 5.56588266e+00,
                                                 -2.66966726e+00, 1.07227282e+00, 1.17704332e+00,
                                                 2.19578871e-01, -3.14188532e-01, -3.56008185e+00,
                                                 -1.10180252e+00, 1.67156722e+00, 1.65997958e+00,
                                                 1.59415822e+00, -3.66572332e+00, -4.48543103e+00,
                                                 2.70453532e+00, 1.23141468e+00, -1.01656226e+00,
                                                 4.45616246e+00, 4.62624155e+00, 1.06641760e+01,
                                                 1.35086342e+00, -2.94979670e+00, -2.91476126e+00,
                                                 -9.35116602e-01, 2.06360252e+00, -9.10136499e+00,
                                                 5.81008956e+00, -1.62736303e+00, -1.25060209e+00,
                                                 -2.87164090e+00, -5.45701288e-01, -7.51629139e-01,
                                                 -9.38791436e-01, 2.34097570e+00, -2.84663470e+00,
                                                 -3.87224043e+00, 1.62309927e+00, 5.67813073e-01,
                                                 3.81686799e-01, 2.51854400e+00, -4.86569414e+00,
                                                 -4.26029143e+00, 6.13481084e+00, -4.95681203e+00,
                                                 -4.50729853e+00, 2.67671425e+00, 1.10979053e-01,
                                                 -9.80886696e-02, -1.40850133e+00, 2.61885371e+00,
                                                 -2.60370423e+00, 5.83765852e+00, -2.83363576e+00,
                                                 -7.32202969e-01, 5.99369850e+00, -1.07059637e+00,
                                                 7.54395772e+00, 1.34653938e+00, 5.18724237e+00,
                                                 -7.20618474e+00, 1.15357476e+00, -6.15439595e+00,
                                                 4.00557024e+00, -6.54318747e+00, 1.40767219e+00,
                                                 -3.25250711e-01, -6.16784426e+00, -5.85228332e+00,
                                                 -2.92134516e-01, 6.75744660e+00, -3.20462659e-01,
                                                 4.23922397e+00, -9.29443606e-01, 3.45086639e+00,
                                                 -8.67499798e+00, -2.01999643e+00, 3.95956040e+00,
                                                 8.79209638e-02, -3.11761297e-01, -9.54823660e-01,
                                                 3.36900880e+00, 1.05584820e+00, 1.90557798e-01,
                                                 4.35153735e+00, 2.07445269e+00, 3.28100342e-01,
                                                 6.04041984e+00, -1.15367544e+00, 1.27468974e+00,
                                                 -2.86660450e+00, -1.20727102e+00, 6.11895125e+00,
                                                 -2.82027924e+00, -6.04291722e+00, 3.81097996e+00,
                                                 9.10548304e-01, 8.94829367e-01, 4.36403895e-01,
                                                 -1.03365614e+00]])
        np.testing.assert_array_almost_equal(self.fee.critical_points[15], critical_points_expected_15)

    def test_layer_0_biases(self):
        layer_0_biases_expected = np.array([[3.52880724],
                                            [1.04879517],
                                            [1.50037751],
                                            [1.28102357],
                                            [-0.12998148],
                                            [1.31377369],
                                            [-0.37855184],
                                            [0.31751928],
                                            [-0.83950368],
                                            [1.00915159],
                                            [-0.22809063],
                                            [-0.09700302],
                                            [0.20176007],
                                            [-0.48283775],
                                            [0.15261177],
                                            [0.40842637]])
        np.testing.assert_array_almost_equal(self.fee.b_0, layer_0_biases_expected)

    def test_layer_1_biases(self):
        layer_1_biases_expected = np.array([[0.3580238],
                                            [0.16528493],
                                            [-0.4548632],
                                            [-1.52886227],
                                            [0.23741153],
                                            [-1.2571574],
                                            [-0.75966823],
                                            [-1.02489274],
                                            [-0.48252173],
                                            [1.92286191]])
        np.testing.assert_array_almost_equal(self.fee.b_1, layer_1_biases_expected, decimal=4)


if __name__ == '__main__':
    unittest.main()
