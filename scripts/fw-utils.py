#/usr/bin/python3
import argparse
import copy


class ET312FirmwareUtils(object):

    KEYS = [0x65, 0xed, 0x83]
    IV = [0xb9, 0xfe, 0x8f]

    def __init__(self, input_file, output_file):
        self.iv = copy.copy(ET312FirmwareUtils.IV)
        with open(input_file, "rb") as f:
            self.input_file = f.read()
        self.output_file = open(output_file, "wb")

    def generate_crc(self):
        xor = 0
        add = 0
        for c in range(len(self.input_file) - 16):
            xor ^= ord(self.input_file[c])
            add += ord(self.input_file[c])
        return [xor, (add & 0xff), ((add >> 8) & 0xff)]

    def encrypt(self):
        pass

    def decrypt(self):
        funcs = {0: lambda x: ((x ^ 0x62) + 0x41) & 0xff,
                 1: lambda x: (n >> 4) | ((n & 0x0f) << 4),
                 2: lambda x: x}

        for i in range(0, len(self.input_file)):
            n = ord(self.input_file[i])
            choice = i % 3
            output = funcs[choice](n) ^ self.iv[choice] ^ self.KEYS[choice]
            self.output_file.write(output)
            self.iv[choice] = n

    def upload():
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input",
                        help="File to take action on")
    parser.add_argument("-o", "--output",
                        help="File to output, if needed by action")
    parser.add_argument("-d", "--decrypt",
                        help="Decrypt input file, store in output file")
    parser.add_argument("-e", "--encrypt",
                        help="Encrypt input file, store in output file."
                        " Adds checksum to output by default.")
    parser.add_argument("-u", "--upload",
                        help="Upload input file to box (requires serial and xmodem packages)")
    parser.add_argument("-c", "--crc",
                        help="Output xor/checksum for input file")
    parser.parse_args()


if __name__ == "__main__":
    main()
