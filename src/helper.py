class helper:
    @staticmethod
    def main(processor_path, input_path):
        import importlib.util

        spec = importlib.util.spec_from_file_location("Processor", processor_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Unable to load processor module from {processor_path}")
        processor_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(processor_module)

        processor = processor_module.Processor()

        spec_input = importlib.util.spec_from_file_location("Input", input_path)
        if spec_input is None or spec_input.loader is None:
            raise ImportError(f"Unable to load input module from {input_path}")
        input_module = importlib.util.module_from_spec(spec_input)
        spec_input.loader.exec_module(input_module)

        input_instance = input_module.Input()
        photo_path = input_instance.get_photo_path()

        processor.process_photo(photo_path)