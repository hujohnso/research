from keras.optimizers import Adam

from Segmenter.CodeFromTrainedUnet.zf_unet_224_model import ZF_UNET_224, dice_coef_loss, dice_coef


class UnetLoader:
    model = None
    u_net_location = "./Segmenter/PreTrainedUnet/zf_unet_224.h5"

    def __init__(self):
        self.model = ZF_UNET_224(weights='generator')
        optim = Adam()
        self.model.compile(optimizer=optim, loss=dice_coef_loss, metrics=[dice_coef])
        self.model.load_weights(self.u_net_location)

    def load_unet(self):
        return self.model