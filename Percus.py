import sys
def getJson(fname):
    from json import loads
    with open(fname,"r") as fp:
        return loads(fp.read())
def intothelist(l,x):
    if(l.count(x) > 0):
        return True
    else:
        return False
class OrbitalMan:
    AllOrbitals = "1s2 2s2 2p6 3s2 3p6 3d10 4s2 4p6 4d10 5s2 5p6 4f14 5d10 6s2 6p6 5f14 6d10 7s2 7p6 6f14 7d10 7f14"
    Nobles = {"[He]":"1s2",
              "[Ne]":"1s2 2s2 sp6",
              "[Ar]":"1s2 2s2 2p6 3s2 3p6",
              "[Kr]":"1s2 2s2 2p6 3s2 3p6 3d10 4s2 4p6",
              "[Xe]":"1s2 2s2 2p6 3s2 3p6 3d10 4s2 4p6 4d10 5s2 5p6",
              "[Rn]":"1s2 2s2 2p6 3s2 3p6 3d10 4s2 4p6 4d10 5s2 5p6 4f14 5d10 6s2 6p6",
              "[Uuo]":"1s2 2s2 2p6 3s2 3p6 3d10 4s2 4p6 4d10 5s2 5p6 4f14 5d10 6s2 6p6 5f14 6d10 7s2 7p6"}
    AngularQuantumNumbers = {"number":{0:"s",1:"p",2:"d",3:"f"},
                             "name"  :{"s":0,"p":1,"d":2,"f":3}
                            }
    OrbitalAreas = {0:[1,2,3,4,5,6,7,8],
                    1:[2,3,4,5,6,7],
                    2:[3,4,5,6],
                    3:[4,5]}
    ElectronLimits = {0:2,
                      1:6,
                      2:10,
                      3:14}
    Errors = {
        120:"Principal Quantum Number Error",
        121:"Orbital Name Error",
        122:"Electron Number Error",
        123:"Angular Quantum Number Error",
        124:"Orbital Read Error",
        125:"Something missing into orbital",
        126:"Orbital Limit Error",
        }
    QuantumNumberLimit = (1,8)
    def CombineOrbitals(*args):
        return " ".join(args)
    def SplitOrbit(self,orbit):
        sep_orbit = [i for i in orbit]
        if(len(sep_orbit) > 4 or len(sep_orbit) < 3):
            raise NameError("\n%s :\n\tWrong orbital => '%s'"%(self.Errors[124],orbit))
        n = int(sep_orbit[0])
        if(n >= self.QuantumNumberLimit[0] and n <= self.QuantumNumberLimit[1]):
            pass
        else:
            raise NameError(self.Errors[120],sep_orbit[0])
        try:
            l = self.AngularQuantumNumbers["name"][sep_orbit[1]]
        except KeyError:
            raise NameError(self.Errors[123],"What is this ? (%s)=> '%s'"%(orbit,sep_orbit[1]))
        except IndexError:
            raise NameError(self.Errors[125],"Something missing into => '%s'"%(orbit))
        if(not intothelist(self.OrbitalAreas[l],n)):
            raise NameError(self.Errors[126],"n=%s orbital can not be in orbit %s"%(self.AngularQuantumNumbers["numbers"][l],n))
        try:
            electron_count = int("".join(sep_orbit[2:]))
        except ValueError:
            pass
        if(electron_count > self.ElectronLimits[l] or electron_count == 0):
            raise NameError(self.Errors[122],"The limit of %s orbital is exceeded"%(self.AngularQuantumNumbers["numbers"][l]))
        return {"raw":"".join(sep_orbit),
                "n":n,
                "l":l,
                "ec":electron_count,
                "ml":2*l+1,
                "energy":n+l
            }
    def SortByEnergy(self,OrbitalList):
        length = len(OrbitalList)
        for i in range(length-1, -1, -1):
            for j in range(i):
                if OrbitalList[j]["raw"] == OrbitalList[j+1]["raw"]:
                    raise NameError("\n%s"%(self.Errors[121]))
        length = len(OrbitalList)
        for i in range(length-1, -1, -1):
            for j in range(i):
                if OrbitalList[j]["energy"] > OrbitalList[j+1]["energy"]:
                    OrbitalList[j], OrbitalList[j+1] = OrbitalList[j+1], OrbitalList[j]
        length = len(OrbitalList)
        for i in range(length-1, -1, -1):
            for j in range(i):
                if(OrbitalList[j]["energy"] == OrbitalList[j+1]["energy"]):
                    if OrbitalList[j]["n"] > OrbitalList[j+1]["n"]:
                        OrbitalList[j], OrbitalList[j+1] = OrbitalList[j+1], OrbitalList[j]
        return OrbitalList
    def AnalyzeOrbital(self,orbital_string):
        sp_orbital = orbital_string.split(" ")
        start = ""
        try:
            start = self.Nobles[sp_orbital[0]]
            sp_orbital = "%s %s"%(start," ".join(sp_orbital[1:]))
            sp_orbital = sp_orbital.split(" ")
        except KeyError:
            OrbitalList = [self.SplitOrbit(i) for i in sp_orbital]
            OrbitalList = self.SortByEnergy(OrbitalList)
            return {
                    "OLD":OrbitalList,
                    "ECF":" ".join([i["raw"] for i in OrbitalList])
                    }
        except Exception,e:
            return {}
        OrbitalList = [self.SplitOrbit(i) for i in sp_orbital]
        OrbitalList = self.SortByEnergy(OrbitalList)
        return {
                "OLD":OrbitalList,
                "ECF":" ".join([i["raw"] for i in OrbitalList])
                }
    def __init__(self):
        pass
def GetPetable2():
    ptab = getJson("PETABLE2.json")
    return ptab
def main():
    ptab = GetPetable2()
    c = 10e+8
    min_lim = 380*10e-9
    max_lim = 750*10e-9
    PhotonLimit = (c/min_lim,c/max_lim)
    print PhotonLimit
    ob = OrbitalMan()
    for i in ptab:
        try:
            print "%s :\n\tOrbital : %s"%(i["name"],ob.AnalyzeOrbital(i["electronicConfiguration"])["ECF"])
        except:
            pass
if __name__ == '__main__':
    main()
