import numpy

import cv2

from Segmenter.UnetLoader import UnetLoader


class ImageStreamCreator:
    folder_with_original_images = None
    u_net_required_dim = 224
    root_path_for_segmented_images = "../Segmenter/Images/SegmentedImages"
    video_name = None

    def __init__(self, folder_with_images, video_name):
        self.folder_with_original_images = folder_with_images
        self.video_name = video_name

    # This logic is simular to the logic in Frame AutoEncoder.  Consider making a util for this
    def get_segmented_image_stream(self):
        if self.check_to_see_if_segmented_image_folder_exists(
                self.root_path_for_segmented_images + "/" + self.video_name):
            return self.load_images_from_a_file(self.root_path_for_segmented_images + "/" + self.video_name, False)
        else:
            return self.load_original_images_and_segment()

    def check_to_see_if_segmented_image_folder_exists(self, filename):
        if cv2.os.path.isdir(filename) and len(cv2.os.listdir(filename)) > 0:
            return True
        return False

    def load_original_images_and_segment(self):
        matrix = self.load_images_from_a_file(self.folder_with_original_images, True)
        matrix = self.segment_image_stream(matrix)
        self.save_segmented_images(matrix, self.root_path_for_segmented_images, self.video_name)
        return matrix

    def load_images_from_a_file(self, folder_path, is_in_color):
        matrix = None
        num_in_matrix = 0
        file_names = cv2.os.listdir(folder_path)
        file_names.sort()
        for filename in file_names:
            if not filename.endswith(".png") and not filename.endswith(".jpg"):
                continue
            if is_in_color:
                image = cv2.imread(folder_path + "/" + filename, 1)
            else:
                image = cv2.imread(folder_path + "/" + filename, 0)
            image = cv2.resize(image, (self.u_net_required_dim, self.u_net_required_dim))
            if num_in_matrix == 0:
                if is_in_color:
                    matrix = numpy.empty([len(cv2.os.listdir(folder_path)),
                                          self.u_net_required_dim,
                                          self.u_net_required_dim, 3])
                else:
                    matrix = numpy.empty([len(cv2.os.listdir(folder_path)),
                                          self.u_net_required_dim,
                                          self.u_net_required_dim])
                if is_in_color:
                    matrix[num_in_matrix, :, :, :] = image
                else:
                    matrix[num_in_matrix, :, :] = image
            num_in_matrix += 1
        return matrix

    def segment_image_stream(self, original_image_matrix):
        u_net_loader = UnetLoader()
        u_net = u_net_loader.load_unet()
        return u_net.predict(original_image_matrix)

    # Not necessary but it makes iterations faster
    def save_segmented_images(self, segmented_matrix, folder_path, video_name):
        num_saved = 0
        cv2.os.mkdir(folder_path + "/" + video_name)
        for image in segmented_matrix:
            cv2.imwrite(folder_path + "/" + video_name + "/%d.jpg" % num_saved, image)
            num_saved += 1
