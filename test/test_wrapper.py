import unittest
from pyaff4wrapper import Aff4Wrapper,Aff4WrapperException
from pathlib import Path
from hashlib import sha1
class TestWrapper(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_namelist(self):
        sample=str(Path(__file__).parent / "Base-Linear.aff4")
        wrapper=Aff4Wrapper(sample)
        namelist=wrapper.namelist()
        self.assertEqual(namelist,["aff4://c215ba20-5648-4209-a793-1f918c723610"])
    

    def test_open(self):
        sample=str(Path(__file__).parent / "Base-Linear.aff4")
        wrapper=Aff4Wrapper(sample)
        with wrapper.open("aff4://c215ba20-5648-4209-a793-1f918c723610") as fh:
            contents=fh.read()
            m=sha1()
            m.update(contents)
            self.assertEqual(len(contents),fh.size)
            self.assertEqual(m.hexdigest(),"fbac22cca549310bc5df03b7560afcf490995fbb")

    def test_open_invalid_name(self):
        sample=str(Path(__file__).parent / "Base-Linear.aff4")
        wrapper=Aff4Wrapper(sample)
        self.assertRaises(Aff4WrapperException,wrapper.open,"aff4://c215ba20-5648-4209-a793-1f918c723610/INVALID")

    def test_close(self):        
        sample=str(Path(__file__).parent / "Base-Linear.aff4")
        wrapper=Aff4Wrapper(sample)
        fh=wrapper.open("aff4://c215ba20-5648-4209-a793-1f918c723610")
        fh.close()
        self.assertTrue(True)
    
        