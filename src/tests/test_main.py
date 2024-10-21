import polars as pl
import pytest
from io import StringIO
from main import df_print


def test_df_print(capsys):
    data = {"column1": [1, 2, 3], "column2": [4, 5, 6]}

    # Call the function
    df_print(data)

    # Capture the output
    captured = capsys.readouterr()

    # Setup the expected DataFrame and capture its string representation
    expected_df = pl.DataFrame(data)
    expected_output = str(expected_df)

    # Assert the printed output matches the expected output
    assert captured.out.strip() == expected_output.strip()


if __name__ == "__main__":
    pytest.main()
