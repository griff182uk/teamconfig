import abc

class Runnable( abc.ABC ) :
    @abc.abstractclassmethod
    def run(self):
        pass