class TextFileReader:
    def __init__(self, path):
        self.file_path = path

    # Opens text file
    def read_file(self):
        """Opens a text file and returns all the text lines. """
        # Opens credentials file as read only
        with open(self.file_path, "r") as text_file:
            # Strips lines in the text file and creates a list
            text_lines = [line.strip() for line in text_file]
        return text_lines

    def read_first_line(self):
        """Opens a text file and returns the first line. """
        # Opens credentials file as read only
        with open(self.file_path, "r") as text_file:
            # Strips lines in the text file and creates a list
            text_lines = [line.strip() for line in text_file]
        return text_lines[0]
