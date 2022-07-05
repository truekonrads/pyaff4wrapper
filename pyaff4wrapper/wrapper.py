from pyaff4 import data_store
from pyaff4 import aff4_image
from pyaff4 import lexicon
from pyaff4 import rdfvalue
from pyaff4 import zip
from pyaff4.aff4 import AFF4Stream
import urllib.parse
import shlex
class Aff4WrapperException(Exception): 
    pass
class Aff4Wrapper(object):
    def __init__(self,aff4file) -> None:
        self.aff4file=aff4file
        self._volume_path_urn = rdfvalue.URN.NewURNFromFilename(aff4file)
        self._resolver= data_store.MemoryDataStore()
        self._zip_volume=zip.ZipFile.NewZipFile(self._resolver,None, self._volume_path_urn)
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({shlex.quote(self.aff4file)})"


    def _subjects(self)->list:
        names={}
        for subject in self._resolver.QueryPredicateObject(None,
                lexicon.AFF4_TYPE, lexicon.AFF4_IMAGE_TYPE):
                # print(subject)
                names[urllib.parse.unquote(subject.value)]=subject
        for subject in self._resolver.QueryPredicateObject(None,
                lexicon.AFF4_TYPE, lexicon.AFF4_FILEIMAGE):
                # print(subject)
                names[urllib.parse.unquote(subject.value)]=subject
        return names
    def namelist(self)->list[str]:
        return list(self._subjects().keys())        
    
    def open(self,name) ->aff4_image.AFF4SImage:
        for sn,subject in self._subjects().items():
                if name==sn:
                    stream=self._resolver.AFF4FactoryOpen(subject)
                    fixed_stream=fix_read(stream)
                    return fixed_stream
        raise Aff4WrapperException(f"Unable to find {name} in the archive")



def fix_read(stream: AFF4Stream) -> AFF4Stream:
    def new_read(self,length=None):
        if length is None:
            length=self.size
        return self.Read(length)
    stream._old_read=stream.read
    stream.read=lambda length=None: new_read(stream,length)
    return stream

