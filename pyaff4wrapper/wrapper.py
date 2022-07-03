from pyaff4 import data_store
from pyaff4 import aff4_image
from pyaff4 import lexicon
from pyaff4 import rdfvalue
from pyaff4 import zip
import urllib.parse
import shlex
class Aff4Wrapper(object):
    def __init__(self,aff4file) -> None:
        self.aff4file=aff4file
        self._volume_path_urn = rdfvalue.URN.NewURNFromFilename(aff4file)
        self._resolver= data_store.MemoryDataStore()
        self._zip_volume=zip.ZipFile.NewZipFile(self._resolver,None, self._volume_path_urn)
    def __repr__(self) -> str:
        return f"{self.__class__}(\"{shlex.quote(self.aff4file)}\")"
    
    # @property
    # def _volume(self):
    #     if self._zip_volume is None:
            
    #     return self._zip_volume
    def namelist(self)->list[str]:
        names=[]
        for subject in self._resolver.QueryPredicateObject(None,
                lexicon.AFF4_TYPE, lexicon.AFF4_IMAGE_TYPE):
                # print(subject)
                names.append(urllib.parse.unquote(subject.value))
        return names
    
    def open(self,name) ->aff4_image.AFF4SImage:
        for subject in self._resolver.QueryPredicateObject(None,
                lexicon.AFF4_TYPE, lexicon.AFF4_IMAGE_TYPE):
                # print(subject)
                sn=urllib.parse.unquote(subject.value)
                if name==sn:
                    return self._resolver.AFF4FactoryOpen(subject)
