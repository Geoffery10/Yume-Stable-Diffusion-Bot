# tests/test_EmbedBuilder.py
import time
import unittest
from models.EmbedBuilder import EmbedBuilder
from models.ImageRequest import ImageRequest


class TestEmbedBuilder(unittest.IsolatedAsyncioTestCase):
    def test_build_description(self):
        img_request = ImageRequest(
            prompt="test prompt", negative_prompt="test negative prompt")
        builder = EmbedBuilder(img_request=img_request)
        description = builder.build_description()
        self.assertEqual(
            description, f"**prompt**: score_9, score_8_up, score_7_up, test prompt\n**negative**: fewer digits, extra digits, test negative prompt")

    def test_build_footer(self):
        img_request = ImageRequest(
            prompt="test prompt", seed=654321, width=512, height=512, steps=20, cfg_scale=7)
        builder = EmbedBuilder(img_request=img_request)
        footer = builder.build_footer()
        self.assertEqual(
            footer, "seed:654321 • width:512 • height:512 • steps:20 • cfg_scale:7")

    def test_build_footer_with_generation_time(self):
        img_request = ImageRequest(
            prompt="test prompt", seed=654321, width=512, height=512, steps=20, cfg_scale=7)
        img_request.set_generation_time((time.time()+10)-time.time())
        builder = EmbedBuilder(img_request=img_request)
        footer = builder.build_footer()
        self.assertIn(" • 10s", footer)
