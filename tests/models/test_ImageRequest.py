import json
import unittest
from models.ImageRequest import ImageRequest
from models.RequestTypes import RequestTypes
import time


class TestImageRequest(unittest.TestCase):
    def setUp(self):
        self.image_request = ImageRequest()

    def test_init(self):
        image_request = ImageRequest()

        self.assertEqual(
            image_request.prompt, "score_9, score_8_up, score_7_up, warning sign")
        self.assertEqual(image_request.negative_prompt,
                         "fewer digits, extra digits, score_6, score_5, score_4, watermark, ")
        self.assertGreater(image_request.seed, 0)
        self.assertEqual(image_request.enable_hr, False)
        self.assertEqual(image_request.hr_scale, 2)
        self.assertEqual(image_request.hr_upscaler, "")
        self.assertEqual(image_request.hr_second_pass_steps, 0)
        self.assertEqual(image_request.hr_resize_x, 0)
        self.assertEqual(image_request.hr_resize_y, 0)
        self.assertEqual(image_request.styles, [])
        self.assertEqual(image_request.batch_size, 1)
        self.assertEqual(image_request.steps, 20)
        self.assertEqual(image_request.cfg_scale, 7)
        self.assertEqual(image_request.width, 816)
        self.assertEqual(image_request.height, 1024)
        self.assertEqual(image_request.restore_faces, False)
        self.assertEqual(image_request.tiling, False)
        self.assertEqual(image_request.eta, 0)
        self.assertEqual(image_request.sampler_index, "DPM++ 2M")
        self.assertEqual(image_request.comments, {})
        self.assertEqual(image_request.send_images, True)
        self.assertEqual(image_request.save_images, True)
        self.assertEqual(image_request.request_type, RequestTypes.TXT2IMG)
        self.assertEqual(image_request.generation_time, None)

    def test_sets_prompt(self):
        new_prompt = "new prompt"
        self.image_request.set_prompt(new_prompt)
        new_prompt = self.image_request.easy_positive(new_prompt)
        self.assertEqual(self.image_request.prompt, new_prompt)

    def test_set_width(self):
        new_width = 512
        self.image_request.set_width(new_width)
        self.assertEqual(self.image_request.width, new_width)

    def test_set_height(self):
        new_height = 512
        self.image_request.set_height(new_height)
        self.assertEqual(self.image_request.height, new_height)

    def test_set_generation_time(self):
        new_generation_time = time.time()
        self.image_request.set_generation_time(new_generation_time)
        self.assertEqual(self.image_request.generation_time,
                         new_generation_time)

    def test_get_payload(self):
        payload = self.image_request.get_payload()
        try:
            json.loads(payload)
        except ValueError as e:
            self.fail(f"Invalid JSON: {e}")

    def test_dimension_clamp(self):
        for width in [-1, 0, 1, 512, 1025, 10000]:
            clamped_width = self.image_request.dimension_clamp(width)
            if width < 1:
                expected_result = 512
            elif width > 1024:
                expected_result = 1024
            else:
                expected_result = width
            self.assertEqual(clamped_width, expected_result)

    def test_easy_positive_does_NOT_add_if_already_there(self):
        original_prompt = "score_9, score_8_up, score_7_up, 1girl, solo"
        expected_result = original_prompt
        result = self.image_request.easy_positive(original_prompt)
        self.assertEqual(result, expected_result)

    def test_easy_positive_adds_string_if_missing(self):
        original_prompt = "original prompt without scores"
        expected_result = "score_9, score_8_up, score_7_up, original prompt without scores"
        result = self.image_request.easy_positive(original_prompt)
        self.assertEqual(result, expected_result)

    def test_easy_negative_does_NOT_add_if_already_there(self):
        original_negative_prompt = f"original negative prompt with {self.image_request.bad_qualities} 1boy"
        expected_result = original_negative_prompt
        result = self.image_request.easy_negative(original_negative_prompt)
        self.assertEqual(result, expected_result)

    def test_easy_negative_adds_string_if_missing(self):
        original_negative_prompt = "original negative prompt without negative"
        expected_result = f"{self.image_request.bad_qualities}, original negative prompt without negative"
        result = self.image_request.easy_negative(original_negative_prompt)
        self.assertEqual(result, expected_result)

    def test_get_prompt_without_qualities(self):
        expected_result = "1girl, solo"
        self.image_request.set_prompt(expected_result)
        result = self.image_request.get_prompt_without_qualities()
        self.assertEqual(result, expected_result)

    def test_get_negative_without_qualities(self):
        expected_result = "upper_body, smile"
        self.image_request.set_negative_prompt(expected_result)
        result = self.image_request.get_negative_without_qualities()
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
