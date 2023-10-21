import argparse
import subprocess


class FileStats:

    def __init__(self, filename):
        self.filename = filename
        self.byte_count = None
        self.char_count = None
        self.word_count = None
        self.line_count = None

    def get_byte_count(self):
        if self.byte_count is None:
            self.byte_count = 0
            with open(self.filename, 'rb') as f:
                for line in f:
                    self.byte_count += len(line)
        return self.byte_count

    def get_char_count(self):
        if self.char_count is None:
            self.char_count = 0
            with open(self.filename, 'r') as f:
                for line in f:
                    self.char_count += len(line)
        return self.char_count

    def get_word_count(self):
        if self.word_count is None:
            self.word_count = 0
            with open(self.filename, 'r') as f:
                for line in f:
                    self.word_count += len(line.split())
        return self.word_count

    def get_line_count(self):
        if self.line_count is None:
            self.line_count = 0
            with open(self.filename, 'r') as f:
                self.line_count = f.read().count("\n")
        return self.line_count

    def test_with_ground_truth(self):
        #execute wc system command and compare with output
        wc_output = subprocess.check_output(['wc', self.filename])
        ground_truth = wc_output.decode('utf-8').strip()
        lc_gt, wc_gt, bc_gt, filename = ground_truth.split()
        print("ccwc_output=",self.get_byte_count(), self.get_line_count(), self.get_word_count(), self.filename)
        print("ground_truth=",wc_gt, lc_gt, bc_gt, filename)
        if self.word_count is not None:
            assert wc_gt == str(self.word_count)
        if self.line_count is not None:
            assert lc_gt == str(self.line_count)
        if self.byte_count is not None:
            assert bc_gt == str(self.byte_count)
        if self.byte_count == self.char_count:
            print("-m and -c are equivalent: the current locale does not support multibyte characters")
        else:
            print("multibyte characters not supported in the code")
            pass
        print('wc command output matches')

def main():
    parser = argparse.ArgumentParser(description='CCWC: A tool for calculating the word count of a file')
    parser.add_argument('filename', help='the file to calculate the word count of')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('-c', '--bytes', action='store_true', help='print the bytes counts')
    parser.add_argument('-w', '--word', action='store_true', help='print the word counts')
    parser.add_argument('-l', '--line', action='store_true', help='print the line counts')
    parser.add_argument('-m', '--char', action='store_true', help='print the character counts')


    args = parser.parse_args()
    fs = FileStats(args.filename)
    if args.bytes:
        bc = fs.get_char_count()
        fs.test_with_ground_truth()
        print(bc, args.filename)
    if args.word:
        wc = fs.get_word_count()
        fs.test_with_ground_truth()
        print(wc, args.filename)
    if args.line:
        lc = fs.get_line_count()
        fs.test_with_ground_truth()
        print(lc, args.filename)
    if args.char:
        cc = fs.get_char_count()
        fs.test_with_ground_truth()
        print(cc, args.filename)

    if not args.char and not args.word and not args.line and not args.bytes:
        bc = fs.get_byte_count()
        cc = fs.get_char_count()
        wc = fs.get_word_count()
        lc = fs.get_line_count()
        fs.test_with_ground_truth()

        print(bc, lc, wc, args.filename)


if __name__ == '__main__':
    main()