from pathlib import Path
from unittest import TestCase

import hcl2
import hcl2.builder


HELPERS_DIR = Path(__file__).absolute().parent.parent / "helpers"
HCL2_DIR = HELPERS_DIR / "terraform-config"
JSON_DIR = HELPERS_DIR / "terraform-config-json"
HCL2_FILES = [str(file.relative_to(HCL2_DIR)) for file in HCL2_DIR.iterdir()]


class TestVariableBlockType(TestCase):
    """Test building hcl files with variable block types"""

    # print any differences fully to the console
    maxDiff = None

    def test_builder_with_complex_floats(self):
        builder = hcl2.Builder()

        builder.block(
            "variable",
            ["some_string_variable"],
            type="string",
            default="some_value"
        )

        builder.block(
            "variable",
            ["some_number_variable"],
            type="number",
            default=42
        )

        self.compare_filenames(builder, "variables_type.tf")

    def compare_filenames(self, builder: hcl2.Builder, filename: str):
        hcl_dict = builder.build()
        hcl_ast = hcl2.reverse_transform(hcl_dict)
        hcl_content_built = hcl2.writes(hcl_ast)

        hcl_path = (HCL2_DIR / filename).absolute()
        with hcl_path.open("r") as hcl_file:
            hcl_file_content = hcl_file.read()
            self.assertMultiLineEqual(
                hcl_content_built,
                hcl_file_content,
                f"file {filename} does not match its programmatically built version.",
            )
