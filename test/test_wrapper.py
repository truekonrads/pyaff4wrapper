import unittest
from pyaff4wrapper import Aff4Wrapper,Aff4WrapperException
from pathlib import Path
from hashlib import sha1
import tempfile

import pyaff4wrapper
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

    def test_extract(self):
        sample=str(Path(__file__).parent / "Base-Linear.aff4")
        wrapper=Aff4Wrapper(sample)
        tmpdir=tempfile.mkdtemp(self.__class__.__name__)
        member="aff4://c215ba20-5648-4209-a793-1f918c723610"
        try:
            wrapper.extract(member,tmpdir)
            fn=member.lstrip("aff4://")
            filepath=Path(tmpdir) / fn
            self.assertTrue(filepath.is_file())
            with open(filepath,"rb") as f:
                m=sha1()
                m.update(f.read())
                self.assertEqual(m.hexdigest(),"fbac22cca549310bc5df03b7560afcf490995fbb")
        finally:
            print(f"About to remove {tmpdir}")
            # os.rm
    

if __name__ == '__main__':
    print(f"Version is {pyaff4wrapper.__version__} ")
    unittest.main()        