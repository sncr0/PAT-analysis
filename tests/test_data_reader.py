import pytest
import os
import pandas as pd
from core.data_readers.data_reader import DataReader
from core.data_readers.infrared_reader import InfraredReader
from core.data_formats.infrared_measurement import InfraredMeasurement, InfraredMeasurementSequence
from core.data_readers.mixins.csv_reader_mixin import CSVReaderMixin


class InfraredMockDataReader(DataReader):
    """Mock class for testing abstract DataReader."""
    def _read_file_impl(self, file_path: str, file_processor):
        return file_processor(file_path, InfraredMeasurement)

    def _read_folder_impl(self, folder_path, file_processor):
        return InfraredReader._read_folder_impl(folder_path, file_processor)


@pytest.fixture
def infrared_mock_data_reader():
    return InfraredMockDataReader()


def test_validate_file_path_exists(infrared_mock_data_reader, tmp_path):
    """Test that existing file passes validation."""
    file_path = tmp_path / "test.csv"
    file_path.write_text("Wavenumber cm-1,Intensities\n100,0.1\n200,0.2")

    infrared_mock_data_reader._validate_file_path(str(file_path))  # Should not raise


def test_validate_file_path_not_exists(infrared_mock_data_reader):
    """Test that missing file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        infrared_mock_data_reader._validate_file_path("non_existent.csv")


def test_get_file_extension(infrared_mock_data_reader):
    """Test file extension extraction."""
    assert infrared_mock_data_reader._get_file_extension("data/test.csv") == "csv"
    with pytest.raises(ValueError):
        infrared_mock_data_reader._get_file_extension("data/test")  # No extension


# ✅ _validate_file_path()
def test_validate_file_path_existing_file(infrared_mock_data_reader, tmp_path):
    """Ensure _validate_file_path() does not raise an error for an existing file."""
    file_path = tmp_path / "test.csv"
    file_path.write_text("Wavenumber cm-1,Intensities\n100,0.1\n200,0.2")

    infrared_mock_data_reader._validate_file_path(str(file_path))  # ✅ Should not raise error


def test_validate_file_path_non_existent_file_raises_error(infrared_mock_data_reader):
    """Ensure _validate_file_path() raises FileNotFoundError for missing file."""
    with pytest.raises(FileNotFoundError):
        infrared_mock_data_reader._validate_file_path("non_existent.csv")


def test_validate_file_path_is_directory_raises_error(infrared_mock_data_reader, tmp_path):
    """Ensure _validate_file_path() raises FileNotFoundError if the path is a directory."""
    os.makedirs(tmp_path / "test_dir")
    with pytest.raises(FileNotFoundError):
        infrared_mock_data_reader._validate_file_path(str(tmp_path / "test_dir"))


# ✅ _get_file_extension()
def test_get_file_extension_valid(infrared_mock_data_reader):
    """Ensure _get_file_extension() correctly extracts the file extension."""
    assert infrared_mock_data_reader._get_file_extension("data/test.csv") == "csv"


def test_get_file_extension_no_extension_raises_value_error(infrared_mock_data_reader):
    """Ensure _get_file_extension() raises ValueError when no extension is present."""
    with pytest.raises(ValueError):
        infrared_mock_data_reader._get_file_extension("data/test")


def test_get_file_extension_directory_raises_value_error(infrared_mock_data_reader, tmp_path):
    """Ensure _get_file_extension() raises ValueError if a directory is passed."""
    os.makedirs(tmp_path / "test_dir")
    with pytest.raises(ValueError):
        infrared_mock_data_reader._get_file_extension(str(tmp_path / "test_dir"))


def test_get_file_extension_unsupported_extension_raises_value_error(infrared_mock_data_reader):
    """Ensure _get_file_extension() raises ValueError if extension is not supported."""
    with pytest.raises(ValueError):
        infrared_mock_data_reader._get_file_extension("data/test.xyz")  # Assuming .xyz is not supported


# ✅ _get_file_processor()
def test_get_file_processor_valid(infrared_mock_data_reader):
    """Ensure _get_file_processor() returns the correct processor for a valid extension."""
    processor = infrared_mock_data_reader._get_file_processor("csv")
    assert callable(processor)


def test_get_file_processor_invalid_extension_raises_value_error(infrared_mock_data_reader):
    """Ensure _get_file_processor() raises ValueError for an unsupported extension."""
    with pytest.raises(ValueError):
        infrared_mock_data_reader._get_file_processor("xyz")  # Assuming .xyz is not in file_processors


# ✅ _validate_folder_path()
def test_validate_folder_path_existing_folder(infrared_mock_data_reader, tmp_path):
    """Ensure _validate_folder_path() does not raise an error for an existing folder."""
    os.makedirs(tmp_path / "test_dir")
    (tmp_path / "test_dir" / "file.csv").write_text("data")

    infrared_mock_data_reader._validate_folder_path(str(tmp_path / "test_dir"))  # ✅ Should not raise error


def test_validate_folder_path_non_existent_raises_error(infrared_mock_data_reader):
    """Ensure _validate_folder_path() raises FileNotFoundError for missing folders."""
    with pytest.raises(FileNotFoundError):
        infrared_mock_data_reader._validate_folder_path("non_existent_folder")


def test_validate_folder_path_is_file_raises_error(infrared_mock_data_reader, tmp_path):
    """Ensure _validate_folder_path() raises ValueError if a file is passed instead of a folder."""
    file_path = tmp_path / "test.csv"
    file_path.write_text("data")
    with pytest.raises(ValueError):
        infrared_mock_data_reader._validate_folder_path(str(file_path))


def test_validate_folder_path_empty_folder_raises_error(infrared_mock_data_reader, tmp_path):
    """Ensure _validate_folder_path() raises ValueError if the folder is empty."""
    os.makedirs(tmp_path / "empty_dir")
    with pytest.raises(ValueError):
        infrared_mock_data_reader._validate_folder_path(str(tmp_path / "empty_dir"))


def test_validate_folder_path_mixed_extensions_raises_error(infrared_mock_data_reader, tmp_path):
    """Ensure _validate_folder_path() raises ValueError if folder contains mixed file extensions."""
    os.makedirs(tmp_path / "test_dir")
    (tmp_path / "test_dir" / "file1.csv").write_text("data")
    (tmp_path / "test_dir" / "file2.txt").write_text("data")

    with pytest.raises(ValueError):
        infrared_mock_data_reader._validate_folder_path(str(tmp_path / "test_dir"))


# ✅ read_file()
def test_read_file_valid(infrared_mock_data_reader, tmp_path):
    """Ensure read_file() correctly calls _read_file_impl()."""
    file_path = tmp_path / "test.csv"
    file_path.write_text("Wavenumber cm-1,00:00:29\n100,0.1\n200,0.2")

    datapoint = infrared_mock_data_reader.read_file(str(file_path))
    assert isinstance(datapoint, InfraredMeasurement)


# def test_read_folder_valid(infrared_mock_data_reader, tmp_path):
#     """Ensure read_folder() correctly calls _read_folder_impl()."""
#     os.makedirs(tmp_path / "test_dir")
#     (tmp_path / "test_dir" / "file.csv").write_text("Wavenumber cm-1,00:00:29\n100,0.1\n200,0.2")

#     result = infrared_mock_data_reader._read_folder_impl((tmp_path / "test_dir"), CSVReaderMixin._process_csv)
#     assert isinstance(result, InfraredMeasurementSequence)  # Abstract, should use subclass in real test


def test_read_folder_invalid_extension_raises_value_error(infrared_mock_data_reader, tmp_path):
    """Ensure read_folder() raises ValueError if an invalid file extension is used."""
    os.makedirs(tmp_path / "test_dir")
    (tmp_path / "test_dir" / "file.xyz").write_text("Wavenumber cm-1,Intensities\n100,0.1\n200,0.2")

    with pytest.raises(ValueError):
        infrared_mock_data_reader.read_folder(str(tmp_path / "test_dir"))  # Assuming .xyz is not supported


def test_get_folder_extension_valid(tmp_path):
    """Ensure _get_folder_extension() returns the correct extension for a folder."""
    reader = InfraredMockDataReader()
    os.makedirs(tmp_path / "test_dir")
    (tmp_path / "test_dir" / "file.csv").write_text("data")
    assert reader._get_folder_extension(str(tmp_path / "test_dir")) == "csv"


def test_get_folder_extension_multiple_extensions(tmp_path):
    """Ensure _get_folder_extension() raises ValueError if folder contains mixed file extensions."""
    reader = InfraredMockDataReader()
    reader.file_processors.update({"txt": None})
    os.makedirs(tmp_path / "test_dir")
    (tmp_path / "test_dir" / "file1.csv").write_text("data")
    (tmp_path / "test_dir" / "file2.txt").write_text("data")

    with pytest.raises(ValueError, match="Inconsistent file extensions in folder"):
        # reader._get_folder_extension(str(tmp_path / "test_dir"))
        reader._validate_folder_path(str(tmp_path / "test_dir"))


def test_read_folder(tmp_path):
    reader = InfraredReader()
    os.makedirs(tmp_path / "test_dir")
    (tmp_path / "test_dir" / "file1.csv").write_text("Wavenumber cm-1,00:00:00\n100,0.1\n200,0.2")
    (tmp_path / "test_dir" / "file2.csv").write_text("Wavenumber cm-1,00:00:00\n100,0.1\n200,0.2")

    result = reader.read_folder(str(tmp_path / "test_dir"), reader.file_processors["csv"])
    assert isinstance(result, InfraredMeasurementSequence)
