import unittest
from discord import ui
import buttons
from models.EmbedButton import EmbedButtons


class TestEmbedButtons(unittest.IsolatedAsyncioTestCase):
    async def test_view_init(self):
        view = EmbedButtons()
        self.assertEqual(len(view.children), 4)

    async def test_view_add_items(self):
        view = EmbedButtons()
        try_again_button = next(
            button for button in view.children if isinstance(button, buttons.TryAgain))
        edit_button = next(button for button in view.children if isinstance(
            button, buttons.EditButton))
        delete_button = next(button for button in view.children if isinstance(
            button, buttons.DeleteButton))
        upscale_button = next(button for button in view.children if isinstance(
            button, buttons.UpscaleButton))
        self.assertIsNotNone(try_again_button)
        self.assertIsNotNone(edit_button)
        self.assertIsNotNone(delete_button)
        self.assertIsNotNone(upscale_button)

    async def test_view_has_try_again_button(self):
        view = EmbedButtons()
        try_again_button = next((button for button in view.children if isinstance(
            button, buttons.TryAgain)), None)
        self.assertIsNotNone(try_again_button)


if __name__ == '__main__':
    unittest.main()
