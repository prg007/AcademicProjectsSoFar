import unittest
import torch
from torch import tensor
from cnn import ConvLayer, Flatten
from cnn import create_window_column_matrix, create_kernel_row_matrix, pad, convolve
import torch.nn.functional as F
import math


DATA_DIR = './data'
STRIPES_CONFIG = './stripes.data.json'


def construct_test_conv2d(constructor, offset_setter):
    conv = constructor(3, 2, kernel_size=2, stride=1, padding=0)
    red_kernel1 = torch.tensor([[1., 0], [0, 0]])
    green_kernel1 = torch.tensor([[0., 0], [1, 0]])
    blue_kernel1 = torch.tensor([[-1., 0], [0, 0]])
    red_kernel2 = torch.tensor([[0., 1], [0, 0]])
    green_kernel2 = torch.tensor([[0., 0], [0, 1]])
    blue_kernel2 = torch.tensor([[0., 2], [0, -1]])
    with torch.no_grad():
        conv.weight[0,0] = red_kernel1
        conv.weight[0,1] = green_kernel1
        conv.weight[0,2] = blue_kernel1
        conv.weight[1,0] = red_kernel2
        conv.weight[1,1] = green_kernel2
        conv.weight[1,2] = blue_kernel2
        offset_setter(conv, [0,0])
    return conv

def set_torch_conv2d_offset(conv, offsets):
    conv.bias[0] = offsets[0]
    conv.bias[1] = offsets[1]

def set_my_conv2d_offset(conv, offsets):
    conv.offset[0,0,0] = offsets[0]
    conv.offset[1,0,0] = offsets[1]




def construct_test_images():
    return  tensor([[[[1., 0., 1.],
                      [0., 1., 0.],
                      [1., 0., 1.]],

                     [[1., 1., 0.],
                      [0., 0., 1.],
                      [1., 0., 1.]],

                     [[0., 0., 1.],
                      [0., 1., 0.],
                      [1., 0., 0.]]],


                    [[[1., 2., 1.],
                      [0., 1., 0.],
                      [1., 0., 1.]],

                     [[1., 1., 0.],
                      [0., 0., 1.],
                      [2., 0., 1.]],

                     [[0., 0., 1.],
                      [0., 1., 0.],
                      [1., 0., 2.]]]], requires_grad=True)

def construct_test_images2():
    red1 = torch.tensor([[2., 0., 1., 3], [0,-1,0, 2], [1,0,1, 0], [1,0,1, 0]], requires_grad=True)
    green1 = torch.tensor([[1., 3, 0, 6], [0,0,1,-1], [1,0,4,2], [1,0,4,2]], requires_grad=True)
    blue1 = torch.tensor([[0.,0,1,0], [0,5,0,7], [1,0,0,3], [1,0,0,3]], requires_grad=True)
    rgb1 = torch.stack([red1, green1, blue1])
    red2 = torch.tensor([[5., 1., 1., 3], [0,9,0, 2], [1,0,1, 0], [1,0,1, 0]], requires_grad=True)
    green2 = torch.tensor([[1., 3, 0, 6], [0,7,1,-1], [3,0,4,2], [1,6,4,2]], requires_grad=True)
    blue2 = torch.tensor([[8.,0,1,0], [0,5,6,7], [3,0,0,3], [1,0,5,3]], requires_grad=True)
    rgb2 = torch.stack([red2, green2, blue2])


    rgbs = torch.stack([rgb1, rgb2])
    return rgbs


class CnnTests(unittest.TestCase):

    def setUp(self):
        """Call before every test case."""
        pass

    def tearDown(self):
        """Call after every test case."""
        pass

    def test_kernel_row(self):
        red_kernel1 = torch.tensor([[1., 2], [3, 4]], requires_grad = True)
        green_kernel1 = torch.tensor([[5., 6], [7, 8]])
        blue_kernel1 = torch.tensor([[9., 10], [11, 12]])
        red_kernel2 = torch.tensor([[13., 14], [15, 16]])
        green_kernel2 = torch.tensor([[17., 18], [19, 20]])
        blue_kernel2 = torch.tensor([[21., 22], [23, 24]])
        kernel1 = torch.stack([red_kernel1, green_kernel1, blue_kernel1])
        kernel2 = torch.stack([red_kernel2, green_kernel2, blue_kernel2])
        kernels = torch.stack([kernel1, kernel2])

        # print(kernels.dim())
        # a,b,c,d = kernels.shape
        # print(kernels.reshape(a,b*c*d))


        result = create_kernel_row_matrix(kernels)

        expected = tensor([[ 1.,  2.,  3.,  4.,  5.,  6.,
                            7.,  8.,  9., 10., 11., 12.],
                           [13., 14., 15., 16., 17., 18.,
                            19., 20., 21., 22., 23., 24.]])
        assert torch.all(torch.eq(result, expected))
        out = 3 * result.sum()
        out.backward()
        expected = tensor([[3., 3.],
                           [3., 3.]])
        assert torch.all(torch.eq(red_kernel1.grad, expected))



    def test_window_column1(self):
        images = construct_test_images()
        # print(images)
        expected = tensor([ [1., 0., 0., 1., 1., 2., 0., 1.],
                            [0., 1., 1., 0., 2., 1., 1., 0.],
                            [0., 1., 1., 0., 0., 1., 1., 0.],
                            [1., 0., 0., 1., 1., 0., 0., 1.],
                            [1., 1., 0., 0., 1., 1., 0., 0.],
                            [1., 0., 0., 1., 1., 0., 0., 1.],
                            [0., 0., 1., 0., 0., 0., 2., 0.],
                            [0., 1., 0., 1., 0., 1., 0., 1.],
                            [0., 0., 0., 1., 0., 0., 0., 1.],
                            [0., 1., 1., 0., 0., 1., 1., 0.],
                            [0., 1., 1., 0., 0., 1., 1., 0.],
                            [1., 0., 0., 0., 1., 0., 0., 2.]])
        # print(expected)
        result = create_window_column_matrix(images,
                                         window_width = 2,
                                         stride=1)

        assert torch.all(torch.eq(result, expected))

    def test_window_column2(self):
        images = tensor([[[[ 1.,  2.,  3.],
                          [ 4.,  5.,  6.],
                          [ 7.,  8.,  9.]]],


                        [[[10., 11., 12.],
                          [13., 14., 15.],
                          [16., 17., 18.]]]], requires_grad=True)
        result = create_window_column_matrix(images,
                                             window_width = 2,
                                             stride=1)
        expected = tensor([  [ 1.,  2,  4,  5, 10, 11, 13, 14],
                             [ 2,  3,  5,  6, 11, 12, 14, 15],
                             [ 4,  5,  7,  8, 13, 14, 16, 17],
                             [ 5,  6,  8,  9, 14, 15, 17, 18]], requires_grad=True)
        assert torch.all(torch.eq(result, expected))
        out = 4 * result.sum()
        out.backward()
        expected = tensor([[[ [ 4.,  8.,  4.],
                              [ 8., 16.,  8.],
                              [ 4.,  8.,  4.]]],


                            [[[ 4.,  8.,  4.],
                              [ 8., 16.,  8.],
                              [ 4.,  8.,  4.]]]])
        assert torch.all(torch.eq(images.grad, expected))

    def test_window_column3(self):
        images = construct_test_images()
        result = create_window_column_matrix(images,
                                         window_width = 3,
                                         stride=1)
        expected = tensor([ [1., 1.],
                            [0., 2.],
                            [1., 1.],
                            [0., 0.],
                            [1., 1.],
                            [0., 0.],
                            [1., 1.],
                            [0., 0.],
                            [1., 1.],
                            [1., 1.],
                            [1., 1.],
                            [0., 0.],
                            [0., 0.],
                            [0., 0.],
                            [1., 1.],
                            [1., 2.],
                            [0., 0.],
                            [1., 1.],
                            [0., 0.],
                            [0., 0.],
                            [1., 1.],
                            [0., 0.],
                            [1., 1.],
                            [0., 0.],
                            [1., 1.],
                            [0., 0.],
                            [0., 2.]])
        assert torch.all(torch.eq(result, expected))

    def test_pad(self):
        images = construct_test_images()
        result = pad(images, padding=2)
        ex = tensor([[[[0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 1., 0., 1., 0., 0.],
                      [0., 0., 0., 1., 0., 0., 0.],
                      [0., 0., 1., 0., 1., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0.]],

                     [[0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 1., 1., 0., 0., 0.],
                      [0., 0., 0., 0., 1., 0., 0.],
                      [0., 0., 1., 0., 1., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0.]],

                     [[0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 1., 0., 0.],
                      [0., 0., 0., 1., 0., 0., 0.],
                      [0., 0., 1., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0.]]],


                    [[[0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 1., 2., 1., 0., 0.],
                      [0., 0., 0., 1., 0., 0., 0.],
                      [0., 0., 1., 0., 1., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0.]],

                     [[0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 1., 1., 0., 0., 0.],
                      [0., 0., 0., 0., 1., 0., 0.],
                      [0., 0., 2., 0., 1., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0.]],

                     [[0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 1., 0., 0.],
                      [0., 0., 0., 1., 0., 0., 0.],
                      [0., 0., 1., 0., 2., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0.]]]])
        assert torch.all(torch.eq(result, ex))
        images = construct_test_images()
        result = pad(images, padding=1)
        ex = tensor([[[[0., 0., 0., 0., 0.],
                      [0., 1., 0., 1., 0.],
                      [0., 0., 1., 0., 0.],
                      [0., 1., 0., 1., 0.],
                      [0., 0., 0., 0., 0.]],

                     [[0., 0., 0., 0., 0.],
                      [0., 1., 1., 0., 0.],
                      [0., 0., 0., 1., 0.],
                      [0., 1., 0., 1., 0.],
                      [0., 0., 0., 0., 0.]],

                     [[0., 0., 0., 0., 0.],
                      [0., 0., 0., 1., 0.],
                      [0., 0., 1., 0., 0.],
                      [0., 1., 0., 0., 0.],
                      [0., 0., 0., 0., 0.]]],


                    [[[0., 0., 0., 0., 0.],
                      [0., 1., 2., 1., 0.],
                      [0., 0., 1., 0., 0.],
                      [0., 1., 0., 1., 0.],
                      [0., 0., 0., 0., 0.]],

                     [[0., 0., 0., 0., 0.],
                      [0., 1., 1., 0., 0.],
                      [0., 0., 0., 1., 0.],
                      [0., 2., 0., 1., 0.],
                      [0., 0., 0., 0., 0.]],

                     [[0., 0., 0., 0., 0.],
                      [0., 0., 0., 1., 0.],
                      [0., 0., 1., 0., 0.],
                      [0., 1., 0., 2., 0.],
                      [0., 0., 0., 0., 0.]]]])
        assert torch.all(torch.eq(result, ex))
        out = 5 * result.sum()
        out.backward()
        expected = tensor([[[ [5., 5., 5.],
                              [5., 5., 5.],
                              [5., 5., 5.]],

                             [[5., 5., 5.],
                              [5., 5., 5.],
                              [5., 5., 5.]],

                             [[5., 5., 5.],
                              [5., 5., 5.],
                              [5., 5., 5.]]],


                            [[[5., 5., 5.],
                              [5., 5., 5.],
                              [5., 5., 5.]],

                             [[5., 5., 5.],
                              [5., 5., 5.],
                              [5., 5., 5.]],

                             [[5., 5., 5.],
                              [5., 5., 5.],
                              [5., 5., 5.]]]])
        assert torch.all(torch.eq(images.grad, expected))


    def test_conv1(self):
        kernels = tensor([[[[ 1.,  2.],
                          [ 3.,  4.]],

                         [[ 5.,  6.],
                          [ 7.,  8.]],

                         [[ 9., 10.],
                          [11., 12.]]],


                        [[[13., 14.],
                          [15., 16.]],

                         [[17., 18.],
                          [19., 20.]],

                         [[21., 22.],
                          [23., 24.]]]], requires_grad=True)
        images =    tensor([[[[ 1.,  2.,  3.],
                              [ 4.,  5.,  6.],
                              [ 7.,  8.,  9.]],

                             [[10., 11., 12.],
                              [13., 14., 15.],
                              [16., 17., 18.]],

                             [[19., 20., 21.],
                              [22., 23., 24.],
                              [25., 26., 27.]]],


                            [[[28., 29., 30.],
                              [31., 32., 33.],
                              [34., 35., 36.]],

                             [[37., 38., 39.],
                              [40., 41., 42.],
                              [43., 44., 45.]],

                             [[46., 47., 48.],
                              [49., 50., 51.],
                              [52., 53., 54.]]]], requires_grad=True)


        result = convolve(kernels, images, stride=1, padding=0)
        expected = tensor([[[ [1245., 1323.],
                              [1479., 1557.]],

                             [[2973., 3195.],
                              [3639., 3861.]]],


                            [[[3351., 3429.],
                              [3585., 3663.]],

                             [[8967., 9189.],
                              [9633., 9855.]]]])
        assert torch.all(torch.eq(result, expected))
        out = result.sum()
        out.backward()
        expected = tensor([[[ [132., 140.],
                              [156., 164.]],

                             [[204., 212.],
                              [228., 236.]],

                             [[276., 284.],
                              [300., 308.]]],


                            [[[132., 140.],
                              [156., 164.]],

                             [[204., 212.],
                              [228., 236.]],

                             [[276., 284.],
                              [300., 308.]]]])
        assert torch.all(torch.eq(kernels.grad, expected))
        expected = tensor([[[ [ 14.,  30.,  16.],
                              [ 32.,  68.,  36.],
                              [ 18.,  38.,  20.]],

                             [[ 22.,  46.,  24.],
                              [ 48., 100.,  52.],
                              [ 26.,  54.,  28.]],

                             [[ 30.,  62.,  32.],
                              [ 64., 132.,  68.],
                              [ 34.,  70.,  36.]]],


                            [[[ 14.,  30.,  16.],
                              [ 32.,  68.,  36.],
                              [ 18.,  38.,  20.]],

                             [[ 22.,  46.,  24.],
                              [ 48., 100.,  52.],
                              [ 26.,  54.,  28.]],

                             [[ 30.,  62.,  32.],
                              [ 64., 132.,  68.],
                              [ 34.,  70.,  36.]]]])
        assert torch.all(torch.eq(images.grad, expected))


    def test_conv2(self):
        conv = construct_test_conv2d(torch.nn.Conv2d, set_torch_conv2d_offset)
        myconv = construct_test_conv2d(ConvLayer, set_my_conv2d_offset)
        images = construct_test_images()
        images2 = construct_test_images()
        result = conv.forward(images)
        result2 = myconv.forward(images2)
        print("RESULT")
        print(result)
        print("RESULT2")
        print(result2)
        assert torch.all(torch.eq(result, result2))

        out = torch.sum(result)
        out2 = torch.sum(result2)
        out.backward()
        out2.backward()
        assert torch.all(torch.eq(conv.weight.grad, myconv.weight.grad))

    def test_conv3(self):
        kernels = tensor([[[[ 1.,  2.],
                          [ 3.,  4.]],

                         [[ 5.,  6.],
                          [ 7.,  8.]],

                         [[ 9., 10.],
                          [11., 12.]]]], requires_grad=True)
        images =    tensor([[[[ 1.,  2.,  3.],
                              [ 4.,  5.,  6.],
                              [ 7.,  8.,  9.]],

                             [[10., 11., 12.],
                              [13., 14., 15.],
                              [16., 17., 18.]],

                             [[19., 20., 21.],
                              [22., 23., 24.],
                              [25., 26., 27.]]],


                            [[[28., 29., 30.],
                              [31., 32., 33.],
                              [34., 35., 36.]],

                             [[37., 38., 39.],
                              [40., 41., 42.],
                              [43., 44., 45.]],

                             [[46., 47., 48.],
                              [49., 50., 51.],
                              [52., 53., 54.]]]], requires_grad=True)
        result = convolve(kernels, images, stride=1, padding=0)
        expected = tensor([[[ [1245., 1323.],
                              [1479., 1557.]]],


                            [[[3351., 3429.],
                              [3585., 3663.]]]])
        assert torch.all(torch.eq(result, expected))

    def test_flatten(self):
        images = construct_test_images()
        # print(images)
        flatten = Flatten()
        result = flatten.forward(images)
        expected = tensor([[1., 0., 1., 0., 1., 0., 1., 0., 1.,
                            1., 1., 0., 0., 0., 1., 1., 0., 1.,
                            0., 0., 1., 0., 1., 0., 1., 0., 0.],
                           [1., 2., 1., 0., 1., 0., 1., 0., 1.,
                            1., 1., 0., 0., 0., 1., 2., 0., 1.,
                            0., 0., 1., 0., 1., 0., 1., 0., 2.]])
        assert torch.all(torch.eq(result, expected))
        out = 6 * torch.sum(result)
        out.backward()
        expected = tensor([[[[ 6., 6., 6.],
                              [6., 6., 6.],
                              [6., 6., 6.]],

                             [[6., 6., 6.],
                              [6., 6., 6.],
                              [6., 6., 6.]],

                             [[6., 6., 6.],
                              [6., 6., 6.],
                              [6., 6., 6.]]],


                            [[[6., 6., 6.],
                              [6., 6., 6.],
                              [6., 6., 6.]],

                             [[6., 6., 6.],
                              [6., 6., 6.],
                              [6., 6., 6.]],

                             [[6., 6., 6.],
                              [6., 6., 6.],
                              [6., 6., 6.]]]])
        assert torch.all(torch.eq(images.grad, expected))

    def test_speed(self):
        images = torch.randn(32,16,64,64)
        kernels = torch.randn(16,16,3,3)
        convolve(kernels, images, stride=1, padding=0)


if __name__ == "__main__":
    unittest.main() # run all tests
