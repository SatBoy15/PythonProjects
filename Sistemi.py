class SistemiLineari():
    def __init__(self):
        print "Requisito:\n\nMettere il Sistema in forma Canonica ed ordinato.\n"
        print self.Resolve(raw_input('Scrivi i vari coefficienti ed il TN del primo sistema separati dalla virgola.\n\nes. 1,-2,6 (rispettivamente x,y,TN)\n\n---->'),raw_input('Scrivi i vari coefficienti ed il TN del secondo sistema separati dalla virgola.\n\nes. 1,-2,6 (rispettivamente x,y,TN)\n\n---->'))

    def Resolve(self,sys1,sys2):
        sysarray = [sys1.split(','),sys2.split(',')]
        print sysarray[0]
        print sysarray[1]
        D = (float(sysarray[0][0])*float(sysarray[1][1]))-(float(sysarray[1][0])*float(sysarray[0][1]))
        Dx =(float(sysarray[0][2])*float(sysarray[1][1]))-(float(sysarray[1][2])*float(sysarray[0][1]))
        Dy = (float(sysarray[0][0])*float(sysarray[1][2]))-(float(sysarray[1][0])*float(sysarray[0][2]))
        return '\n x vale '+str(Dx/D)+'\n\n y vale '+str(Dy/D)

if __name__ == '__main__':
    SistemiLineari()
