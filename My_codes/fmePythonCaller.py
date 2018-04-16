import fme
import fmeobjects
# Template Function interface:
# When using this function, make sure its name is set as the value of
# the 'Class or Function to Process Features' transformer parameter
def processFeature(feature):
    pass

# Template Class Interface:
# When using this class, make sure its name is set as the value of
# the 'Class or Function to Process Features' transformer parameter
class FeatureProcessor(object):
    def __init__(self):
        pass
    def input(self,feature):
        self.pyoutput(feature)
    def close(self):
        pass