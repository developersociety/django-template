from django.test import SimpleTestCase

from pages import blocks


class TestBlockRendering(SimpleTestCase):
    def test_render_link_block(self):
        block = blocks.LinkBlock()
        value = block.to_python({"link_to": "custom_url", "custom_url": "https://dev.ngo"})
        result = block.render(value)
        self.assertIn("https://dev.ngo", result)

    def test_render_richtexteditor_block(self):
        block = blocks.RichTextEditorBlock()
        value = block.to_python({"content": "<b>testing</b>"})
        result = block.render(value)
        self.assertIn("<b>testing</b>", result)

    def test_render_button_block(self):
        block = blocks.ButtonBlock()
        value = block.to_python(
            {
                "link": {"link_to": "custom_url", "custom_url": "https://dev.ngo"},
                "link_text": "Test text",
            }
        )
        result = block.render(value)
        self.assertIn("https://dev.ngo", result)
        self.assertIn("Test text", result)

    def test_render_quote_block(self):
        block = blocks.QuoteBlock()
        value = block.to_python(
            {"quote": "This is a great quote", "citation": "_DEV developer", "role": "developer"}
        )
        result = block.render(value)
        self.assertIn("This is a great quote", result)
        self.assertIn("_DEV developer", result)
        self.assertIn("developer", result)

    def test_render_download_block(self):
        block = blocks.DownloadBlock()
        value = block.to_python({"title": "THIS IS AWESOME!!", "summary": "Yes it is!"})
        result = block.render(value)
        self.assertIn("THIS IS AWESOME", result)
        self.assertIn("Yes it is!", result)

    def test_render_tile_block(self):
        block = blocks.TileBlock()
        value = block.to_python(
            {
                "link": {"link_to": "custom_url", "custom_url": "https://dev.ngo"},
                "title": "Tile title",
                "summary": "Tile summary",
                "link_text": "Tile link text",
            }
        )
        result = block.render(value)
        self.assertIn("https://dev.ngo", result)
        self.assertIn("Tile title", result)
        self.assertIn("Tile summary", result)
        self.assertIn("Tile link text", result)

    def test_render_tilegrid_block(self):
        block = blocks.TileGridBlock()
        value = block.to_python(
            {
                "links": [
                    {
                        "type": "link",
                        "value": {
                            "link": {"link_to": "custom_url", "custom_url": "https://dev.ngo"},
                            "title": "Tile title",
                            "summary": "Tile summary",
                            "link_text": "Tile link text",
                        },
                    },
                    {
                        "type": "link",
                        "value": {
                            "link": {"link_to": "custom_url", "custom_url": "https://dev.ngo"},
                            "title": "Tile title",
                            "summary": "Tile summary",
                            "link_text": "Tile link text",
                        },
                    },
                    {
                        "type": "link",
                        "value": {
                            "link": {"link_to": "custom_url", "custom_url": "https://dev.ngo"},
                            "title": "Tile title",
                            "summary": "Tile summary",
                            "link_text": "Tile link text",
                        },
                    },
                ]
            }
        )
        result = block.render(value)
        self.assertIn("https://dev.ngo", result)
        self.assertIn("Tile title", result)
        self.assertIn("Tile summary", result)
        self.assertIn("Tile link text", result)
        self.assertEqual(result.count('class="tile"'), 3)

    def test_render_twocolumn_block(self):
        block = blocks.TwoColumnBlock()
        value = block.to_python(
            {
                "column_one": [{"type": "text", "value": {"content": "<b>testing</b>"}}],
                "column_two": [{"type": "text", "value": {"content": "<b>testing</b>"}}],
            }
        )
        result = block.render(value)
        self.assertIn("<b>testing</b>", result)
        self.assertEqual(result.count("<b>testing</b>"), 2)
