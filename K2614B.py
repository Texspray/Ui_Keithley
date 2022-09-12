import pyvisa
import numpy as np
import Janela2 as jn2
import sys
import time

k2614 = None

class K2614B:
    id1=[]
    vd1=[]

    ig2=[]
    vg2= []
    range = 0
    range2 = 0
    #variveis canal A
    ViniA = 0
    VfinA =  0
    VstepA = 1
    #variaveis canal B
    ViniB = 0
    VfinB = 0
    VstepB = 1
    breaker = 0
    curva = 0
    resetPlot = 0
    tempo = 0

    def __init__(self):
        #self.k2614 = pyvisa.ResourceManager().open_resource("USB0::0x05E6::0x2614::4321994::INSTR")
        pass


    def reset(self):
        self.k2614.write("smua.reset()")
        self.k2614.write("smub.reset()")
        self.vd1 = []
        self.id1 = []
        self.ig2 = []
        self.vg2 = []
        self.curva = 0
    def promptoff(self):
        self.k2614.write("*rst")
        self.k2614.write("*cls")
        self.k2614.write("localnode.prompts = 0")
    def setValores(self, va, vfa, stpA, vb, vfb, stpB, range0, range1):
        self.ViniA = float(va)
        self.VfinA = float(vfa)
        self.VstepA = float(stpA)
        self.ViniB = float(vb)
        self.VfinB = float(vfb)
        self.VstepB = float(stpB)
        self.range = range0
        self.range2 = range1
        self.resetPlot = 0
        self.breaker = 1
    def setChannels(self, vd, vg, range0, range1):
        self.k2614.write("smub.source.levelv =", str(vd))
        self.k2614.write("smua.source.levelv =", str(vg))
        self.k2614.write("smua.source.func = smub.OUTPUT_DCVOLTS")
        self.k2614.write("smub.source.func = smub.OUTPUT_DCVOLTS")
        self.range = range0
        self.range2 = range1
        if (self.range == "smua.AUTORANGE_ON"):

            self.k2614.write("smua.measure.autorangei = smua.AUTORANGE_ON")
            print(self.range+'rola')
        else:
            self.k2614.write("smua.measure.rangei = {}".format(self.range))
            print("{} ligado 1".format((self.range)))
        if (self.range2 == "smua.AUTORANGE_ON"):
            self.k2614.write("smub.measure.autorangei = smub.AUTORANGE_ON")
            print(self.range2+'rola')
        else:
            self.k2614.write("smub.measure.rangei = {}".format(self.range2))
            print("{} ligado 2".format((self.range2)))


        self.k2614.write("smua.source.output = smua.OUTPUT_ON")
        self.k2614.write("smub.source.output = smub.OUTPUT_ON")
    def setChannelA(self, vd):
        self.k2614.write("smua.source.levelv =", str(vd))
    def setChannelB(self, vg):
        self.k2614.write("smub.source.levelv =", str(vg))
    def getCurrent(self, vd, vg):
        self.id1.append(float(self.k2614.query("print(smua.measure.i())")))
        self.ig2.append(float(self.k2614.query("print(smub.measure.i())")))
        #self.vd1.append(vd)
        #self.vg2.append(vg)


    def display(self):
        self.k2614.write("display.smub.measure.func = display.MEASURE_DCAMPS")
        self.k2614.write("display.smua.measure.func = display.MEASURE_DCAMPS")

    def Sweep(self, transfer, out, IdaVv, IdaVs, delay, compliance, limiteV, media):

        idavoltav = IdaVv
        if out == 2 and transfer == 0:
            saida = True
            transfer = False
        elif out == 0 and transfer == 2:
            saida = False
            transfer = True

        if saida == True and transfer == False:
            smuX = "smua"
            smuY = "smub"
        elif saida == False and transfer == True:
            smuX = "smub"
            smuY = "smua"
        else:
            print("Escolha um tipo de medida: saída ou transfer")
            sys.exit()

        # colocar limite de tensão por causa do rele <30V


        self.k2614.write("{}.source.limiti =".format(smuX), str(compliance))  # Limita corente máx medida pg567
        self.k2614.write("{}.source.limiti =".format(smuX), str(compliance))  # Limita corente máx medida pg567

        if abs(self.ViniA) > abs(limiteV) or abs(self.VfinA) > abs(limiteV):
            print("O limite máximo de tensão é", limiteV, "V")
            sys.exit()

        # Configurando canal 1 para varredura "Vvarr" no dreno-fonte (Vd)

        Npointsv = int(1 + abs(round(((self.VfinA - self.ViniA) / self.VstepA))))
        # print(Npointsv)
        Vidav = np.linspace(self.ViniA, self.VfinA, num=Npointsv)
        # print(Vidav)
        Vvoltav = np.linspace(self.VfinA, self.ViniA, num=Npointsv)
        Vvoltav = np.delete(Vvoltav, 0)
        # print(Vvoltav)

        if idavoltav == 2:
            Vvarr = np.concatenate((Vidav, Vvoltav))
            # print(Vvarr)
        else:
            Vvarr = Vidav
            # print(Vvarr)

        # Configurando canal 2 para stepper "Vstepper" no gate (Vg)

        idavoltaB = IdaVs
        Npointss = int(1 + abs(round(((self.VfinB - self.ViniB) / self.VstepB))))
        # print(Npointss)
        VidaB = np.linspace(self.ViniB, self.VfinB, num=Npointss)
        # print(Vidas)
        VvoltaB = np.linspace(self.VfinB, self.ViniB, num=Npointss)
        VvoltaB = np.delete(VvoltaB, 0)


        if idavoltaB == 2:
            Vstepper = np.concatenate((VidaB, VvoltaB))
            # print(Vstepper)
        else:
            Vstepper = VidaB
            # print(Vstepper)

        self.vd1 =[[]for y in range(len(Vstepper))]
        self.id1 =[[]for y in range(len(Vstepper))]
        self.ig2 =[[]for y in range(len(Vstepper))]



        # Proteção (rele e fio Ag/AgCl) medidas eletroquímicas Canal 2

        if abs(self.ViniB) > abs(limiteV) or abs(self.VfinB) > abs(limiteV):
            print("O limite máximo de tensão é", limiteV, "V")
            sys.exit()

        # Configuração comum de medida Canal (Vd)

        self.k2614.write("display.smua.measure.func = display.MEASURE_DCAMPS")  # pg424 muda tela p medida corrente
        self.k2614.write("smua.source.func = smua.OUTPUT_DCVOLTS")  # Sets the source function of SMU
        if (self.range == "smua.AUTORANGE_ON"):

            self.k2614.write("smua.measure.autorangei = smua.AUTORANGE_ON")
            print(self.range+'rola')
        else:
            self.k2614.write("smua.measure.rangei = {}".format(self.range))
            print("{} ligado 1".format((self.range)))

        self.k2614.write("smua.measure.filter.enable = smua.FILTER_ON")  # pg547
        self.k2614.write("smua.measure.filter.count = {}".format(media))  # testar bem essa função pg547

        # Configuração comum de medida Gate (Vg)

        self.k2614.write("display.smub.measure.func = display.MEASURE_DCAMPS")  # pg424 muda tela p medida corrente
        self.k2614.write("smub.source.func = smub.OUTPUT_DCVOLTS")  # Sets the source function of SMU
        if (self.range2 == "smua.AUTORANGE_ON"):
            self.k2614.write("smub.measure.autorangei = smub.AUTORANGE_ON")
            print(self.range2+'rola')
        else:
            self.k2614.write("smub.measure.rangei = {}".format(self.range2))
            print("{} ligado 2".format((self.range2)))
        self.k2614.write("smub.measure.filter.enable = smub.FILTER_ON")  # pg547
        self.k2614.write("smub.measure.filter.count = 5")  # testar bem essa função pg547

        for k in range(0, len(Vstepper)):
            # APLICAÇÃO DE TENSÃO GATE

            self.k2614.write("{}.source.levelv =".format(smuY), str(Vstepper[k]))
            self.k2614.write("{}.source.output = smub.OUTPUT_ON".format(smuY))
            jn2.Ui_MainWindow.setValues(jn2.Ui_MainWindow)
            self.vg2.append(Vstepper[k])
            print(self.curva)
            self.curva = (self.curva) + 1
            for l in range (0,len(Vvarr)):
                if self.breaker ==0:
                    break
                self.k2614.write("{}.source.levelv =".format(smuX), str(Vvarr[l]))
                self.k2614.write("{}.source.output = smua.OUTPUT_ON".format(smuX))
                time.sleep(delay)

                # MEDIDA DE CORRENTE CANAL
                jn2.mutex.lock() # SINCRONIZA COM A TELA COMECO
                leitura1 = self.k2614.query("print({}.measure.i())".format('smua'))
                self.id1[k].append(float(leitura1))
                self.vd1[k].append(Vvarr[l])

                # MEDIDA DE CORRENTE GATE
                leitura2 = self.k2614.query("print({}.measure.i())".format('smub'))
                self.ig2[k].append(float(leitura2))

                jn2.mutex.unlock() # SINCRONIZA COM A TELA FIM

        self.breaker=0
        self.k2614.write("smua.source.output = smua.OUTPUT_OFF")
        self.k2614.write("smub.source.output = smub.OUTPUT_OFF")
        self.resetPlot = 1

    def voltaMetria(self, sCircuit, preVolt, preTime, Vi, Vf, scanRate, delay, checkShort, checkPre):
        if checkShort == 2 and checkPre == 2:
            for i in range(10):
                self.k2614.write("smua.source.levelv =", str(0))
                while(i != scanRate):
                    self.id1.append(float(self.k2614.query("print(smua.measure.i())")))
                    time.sleep(sCircuit/10)
                i = 0
                self.k2614.write("smua.source.levelv =", str(preVolt))
                while(i != scanRate):
                    self.id1.append(float(self.k2614.query("print(smua.measure.i())")))
                    time.sleep(preTime/10)
        elif checkPre == 0 and checkShort == 2:
            for i in range(10):
                self.k2614.write("smua.source.levelv =", str(0))
                while (i != scanRate):
                    self.id1.append(float(self.k2614.query("print(smua.measure.i())")))
                    time.sleep(sCircuit/ 10)
        #nPontos = (Vf-Vi/scanRate)





        pass



        # k2614.write("beeper.beep(0.5, 2400)")
        #tabela_resultados = np.array([self.vd1, self.id1, self.vg2, self.ig2], dtype=float).T
        #print(tabela_resultados)
