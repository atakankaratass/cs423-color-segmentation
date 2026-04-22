from cs423_segmentation.cli import build_parser, main


def test_parser_defaults_to_scaffold_mode() -> None:
    parser = build_parser()
    args = parser.parse_args([])
    assert args.mode == "scaffold"


def test_main_returns_success() -> None:
    assert main() == 0
