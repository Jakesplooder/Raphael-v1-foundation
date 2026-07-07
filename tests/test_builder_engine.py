import unittest
from unittest.mock import patch, MagicMock
from raphael_core.builder_engine import BuilderEngine

class BuilderEngineTests(unittest.TestCase):
    @patch('raphael_core.builder_engine.OllamaProvider')
    def test_request_build_blueprint_parses_json(self, MockProvider):
        # Setup mock LLM response
        mock_provider_instance = MockProvider.return_value
        mock_result = MagicMock()
        mock_result.response = '''
```json
{
  "src/App.jsx": "export default function App() { return <h1>Test</h1>; }",
  "index.html": "<!DOCTYPE html><html></html>"
}
```
'''
        mock_provider_instance.reason.return_value = mock_result
        
        engine = BuilderEngine()
        files = engine.request_build_blueprint("A test app", "TestApp", "react")
        
        self.assertEqual(len(files), 2)
        self.assertIn("src/App.jsx", files)
        self.assertEqual(files["index.html"], "<!DOCTYPE html><html></html>")
        
    @patch('raphael_core.builder_engine.OllamaProvider')
    def test_request_build_blueprint_handles_invalid_json(self, MockProvider):
        mock_provider_instance = MockProvider.return_value
        mock_result = MagicMock()
        mock_result.response = 'This is just some text, not JSON.'
        mock_provider_instance.reason.return_value = mock_result
        
        engine = BuilderEngine()
        with self.assertRaises(RuntimeError) as context:
            engine.request_build_blueprint("A test app", "TestApp", "react")
        self.assertIn("Builder failed to parse JSON from LLM", str(context.exception))

if __name__ == '__main__':
    unittest.main()
