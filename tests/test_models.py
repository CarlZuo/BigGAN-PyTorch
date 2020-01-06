import pytest

import torch

import utils
from models import BigGAN, biggan, biggan_deep

batch_size = 4
n_classes = 1000
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


@pytest.mark.skipif(device != torch.device('cuda'), reason="Need Cuda to run quickly")
@pytest.mark.parametrize('res', [128, 256, 512])
def test_biggan_generator(res):
    G = biggan.Generator(resolution=res).to(device)
    z_, y_ = utils.prepare_z_y(batch_size, G.dim_z, n_classes, device=device)
    G_z = G(z_, G.shared(y_))
    assert G_z.size() == torch.Size((batch_size, 3, res, res))


@pytest.mark.skipif(device != torch.device('cuda'), reason="Need Cuda to run quickly")
@pytest.mark.parametrize('res', [128, 256, 512])
def test_biggan(res):
    G = BigGAN(resolution=res).to(device)
    z_, y_ = utils.prepare_z_y(batch_size, G.dim_z, n_classes, device=device)
    G_z = G(z_, G.shared(y_))
    assert G_z.size() == torch.Size((batch_size, 3, res, res))


@pytest.mark.skipif(device != torch.device('cuda'), reason="Need Cuda to run quickly")
@pytest.mark.parametrize('res, pretrained, load_ema, tfhub', [
    (128, 'places365', False, False),
    (128, 'places365', True, False),
    (128, 'imagenet', False, False),
    (128, 'imagenet', True, False),
    (128, 'imagenet', True, True),
])
def test_pretrained_biggan(res, pretrained, load_ema, tfhub):
    G = BigGAN(resolution=res, pretrained=pretrained,
               load_ema=load_ema, tfhub=tfhub).to(device)
    z_, y_ = utils.prepare_z_y(batch_size, G.dim_z, n_classes, device=device)
    G_z = G(z_, G.shared(y_))
    assert G_z.size() == torch.Size((batch_size, 3, res, res))


@pytest.mark.skipif(device != torch.device('cuda'), reason="Need Cuda to run quickly")
@pytest.mark.parametrize('res', [128, 256, 512])
def test_biggan_deep_generator(res):
    G = biggan_deep.Generator(resolution=res, hier=True).to(device)
    z_, y_ = utils.prepare_z_y(batch_size, G.dim_z, n_classes, device=device)
    G_z = G(z_, G.shared(y_))
    assert G_z.size() == torch.Size((batch_size, 3, res, res))

