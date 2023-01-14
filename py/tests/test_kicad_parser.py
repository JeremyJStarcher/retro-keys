import unittest
from kicad_parser import KiCadParser
from tests.test_filepaths import SAMPLE_PCB_FILENAME


def read_file():
    data_file = open(SAMPLE_PCB_FILENAME, "r")
    data = data_file.read()
    data_file.close()
    return data


class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual("foo".upper(), "FOO")

    def test_isupper(self):
        self.assertTrue("FOO".isupper())
        self.assertFalse("Foo".isupper())

    def test_split(self):
        s = "hello world"
        self.assertEqual(s.split(), ["hello", "world"])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_loadparser(self):
        parser = KiCadParser("     Hello")
        self.assertEqual(parser.idx, 0)

    def test_eatSpace(self):
        parser = KiCadParser("     Hello")
        parser.eatSpace()
        self.assertEqual(parser.idx, 5)
        self.assertEqual(parser.getNextCharacter(), "H")

    def test_eatSpaceWorksIfNoSpaces(self):
        parser = KiCadParser("Hello")
        parser.eatSpace()
        self.assertEqual(parser.idx, 0)
        self.assertEqual(parser.getNextCharacter(), "H")

    def test_eatSpaceIncludesOthers(self):
        parser = KiCadParser("  \r \n \t   Hello")
        parser.eatSpace()
        self.assertEqual(parser.idx, 10)
        self.assertEqual(parser.getNextCharacter(), "H")

    def test_eatNextCharacter(self):
        parser = KiCadParser("12335")
        self.assertEqual(parser.getNextCharacter(), "1")
        self.assertEqual(parser.getNextCharacter(), "2")

    def test_expectCharPass(self):
        parser = KiCadParser("  ()")
        parser.eatSpace()
        parser.expectCharacter("(")
        self.assertEqual(parser.getNextCharacter(), "(")

    def test_getNextToken1(self):
        parser = KiCadParser("(hello)")
        parser.eatNextCharacter()
        token = parser.getNextToken()
        self.assertEqual(token, "hello")

    def test_getNextToken2(self):
        parser = KiCadParser("(  hello   )")
        parser.eatNextCharacter()
        token = parser.getNextToken()
        self.assertEqual(token, "hello")

    def test_getNextToken3(self):
        parser = KiCadParser("(  hello   world )")
        parser.eatNextCharacter()
        token = parser.getNextToken()
        self.assertEqual(token, "hello")
        token = parser.getNextToken()
        self.assertEqual(token, "world")

    def test_getNextTokenNoToken(self):
        parser = KiCadParser("(   )")
        parser.eatNextCharacter()
        token = parser.getNextToken()
        self.assertEqual(token, "")

    def test_getNexTokenQuoted(self):
        parser = KiCadParser('("hello world")')
        parser.eatNextCharacter()
        token = parser.getNextToken()
        self.assertEqual(token, '"hello world"')

    def test_readFile(self):
        s = read_file()
        parser = KiCadParser(s)
        parser.expectCharacter("(")
        self.assertEqual(parser.getNextCharacter(), "(")

    def test_peekNextToken(self):
        s = read_file()
        parser = KiCadParser(s)
        parser.eatNextCharacter()
        token = parser.peekNextToken()
        self.assertEqual(token, "kicad_pcb")
        # Make sure the token was not eaten
        token = parser.peekNextToken()
        self.assertEqual(token, "kicad_pcb")

    def test_toListReturnList(self):
        parser = KiCadParser("()")
        a = parser.toList()
        self.assertTrue(hasattr(a, "__len__"))

    def test_toListParsesOneToken(self):
        parser = KiCadParser("(hello)")
        a = parser.toList()
        self.assertTrue(hasattr(a, "__len__"))
        self.assertEqual(a[0], "hello")

    def test_toListParsesMultipleTokens(self):
        parser = KiCadParser("(  hello   world  )")
        a = parser.toList()
        self.assertTrue(hasattr(a, "__len__"))
        self.assertEqual(a[0], "hello")
        self.assertEqual(a[1], "world")

    def test_toListParsesNestedTokens(self):
        parser = KiCadParser("(  (hello)   world  )")
        a = parser.toList()

        self.assertTrue(hasattr(a, "__len__"))
        self.assertEqual(a[0][0], "hello")
        self.assertEqual(a[1], "world")

    def test_toListFinal(self):
        s = read_file()
        parser = KiCadParser(s)
        root = parser.toList()
        l = parser.listToSexp(root)
        # print("\r\n".join(l))


if __name__ == "__main__":
    unittest.main()
