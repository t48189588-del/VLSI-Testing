#setting libraries
from datetime import *
import random

class SA_faults:
    def __init__(self, bench_file_name:str=''):
        """Initializes the class

        Args:
            bench_file_name (str): Provide the path of the file to extract the information
        """
        if bench_file_name!='':
            self.logs=[]
            self.signals={}
            self.circuit=[]
            self.primary_outputs=[] #to show all the primary outputs
            self.primary_inputs=[] #to show all the primary inputs
            self.gates={}
            self.implications={
    "AND":['000','010','0X0','0D0','0E0','111','1XX','1DD','1EE','XXX','XDX','XEX','DDD','DE0','EEE'], #input(a)input(b)output
    "NAND":['001','011','0X1','0D1','0E1','110','1XX','1DE','1ED','XXX','XDX','XEX','DDE','DE1','EED'],
    "OR":['000','011','0XX','0DD','0EE','111','1X1','1D1','1E1','XXX','XDX','XEX','DDD','DE1','EEE'],
    "NOR":['001','010','0XX','0DE','0ED','110','1X0','1D0','1E0','XXX','XDX','XEX','DDE','DE0','EED'],
    "XOR":['000','011','0XX','0DD','0EE','110','1XX','1DE','1ED','XXX','XDX','XEX','DD0','DE1','EE0'],
    "XNOR":['001','010','0XX','0DE','0ED','111','1XX','1DD','1EE','XXX','XDX','XEX','DD1','DE0','EE1'],
    "NOT":['0-1','1-0','X-X','D-E','E-D'],
    "BUFF":['0-0','1-1','X-X','D-D','E-E']
}
            if '.bench' in bench_file_name:
                #setting time to Japan time (UTC+9)
                self.jpTime=datetime.now(timezone(timedelta(hours=9)))
                self.t0=self.jpTime.now() #sets starting time
                self.read_bench(bench_file_name)
                print("Information loaded")
                try:
                    self.test(bench_file_name.replace('bench','tests'))
                except:
                    print("No test file found")
            else:
                print("The provided file does not match the bench file pattern")
        
    def __log(self, msg:str):
        '''
        :param str msg: the message to appear in the log
        '''
        delta=self.jpTime.now()-self.t0 #show the running time since program start
        self.logs.append([str(delta),msg]) # global time, duration, 
        print(f'{delta}...{msg}')

    def logic_gate(self, gate:str, inputs:list): 

        '''defining the logic gate functioning 

        Params
        ------
            gate(str): 'NAND', 'AND', 'OR', 'NOT', 'NOR', 'BUFF', 'XOR', 'XNOR' name of gates in bench files 
            inputs(list): defines the inputs for the gate [A,B,C...], the number of elements in the function will determine the amount of pins for the logic gate.EXCEPT for NOT gates it will take ONLY the first element 

        Returns
        -------
        output(bool): 
            a single logic value to assign to the corresponding  

        ''' 

        #verifying that the input list is just integers 0/1 

        aux,inputs=inputs,[] 
        try: #typical inputs of 0 or 1
            inputs=[int(x) for x in aux] 
            holder=inputs[0] 
            if gate.upper()=='NAND': 
                [holder:=holder&x for x in inputs] 
                holder= ~holder
            elif gate.upper()=="AND":
                [holder:=holder&x for x in inputs] 
            elif gate.upper()=="OR": 
                holder =0 
                [holder:=holder|x for x in inputs] 
            elif gate.upper()=="NOT":
                holder = ~holder
            elif gate.upper()=="NOR": 
                holder =0 
                [holder:=holder|x for x in inputs] 
                holder=~holder
            elif gate.upper()=="XOR": 
                holder=0 
                [holder:=holder^x for x in inputs] 
            elif gate.upper()=="XNOR": 
                holder=0 
                [holder:=holder^x for x in inputs] 
                holder=~holder
        except: #for forward implication (having X, D, -D)
            if 'X' in aux or 'x' in aux:
                if gate.upper()=='NAND': 
                    if 0 in aux or '0' in aux:
                        holder=1
                    else:
                        holder='X'
                elif gate.upper()=="AND":
                    if 0 in aux or '0' in aux:
                        holder=0
                    else:
                        holder='X'
                elif gate.upper()=="OR": 
                    if 1 in aux or '1' in aux:
                        holder=1
                    else:
                        holder='X'
                elif gate.upper()=="NOR": 
                    if 1 in aux or '1' in aux:
                        holder=0
                    else:
                        holder='X'
                elif gate.upper()=="NOT" or gate.upper()=="BUFF":
                    holder = 'X'
                elif gate.upper()=="XOR" or gate.upper()=="XNOR":
                    holder='X'
        return holder
    #circuit code
    def circuit_code(self, signal_line:dict, circ_struc:list, stuck_at:dict={}):
        """This runs the circuit in fault-free mode and stuck-at fault

        Args:
            signal_line (dict): Imports what the signal logic value must be
            circ_struc (list): Which logic gate and the relationship between inputs and outputs
            stuck_at (dict): If provided, these values are flipped to whichever value is in this dict #key=signal index value=logic value to be stuck at
        Returns:
            signal_line (dict): returns the updated signal logic value for any situation (fault-free or stuck-at fault)
        """   
        for a in circ_struc:
            output_signal=a.split(' = ')[0]
            gate=a.split(' = ')[1].split('(')[0]
            input_signal_index=a.split(' = ')[1].split('(')[1][:-1]

            input_signals=[]
            for x in input_signal_index.split(', '):
                if x in stuck_at:
                    input_signals.append(stuck_at[x.strip()])
                else:
                    input_signals.append(signal_line[x.strip()])
            signal_line[output_signal]=self.logic_gate(gate,input_signals)
            # if stuck_at and (output_signal in stuck_at.keys()):
            if stuck_at:
                if (output_signal in stuck_at.keys()): #continue with the SA fault
                    signal_line[output_signal]=stuck_at[output_signal]
        return signal_line

    def __bin2int(self, primary_inputs:list):
        """Transforms the binary functional truth table to unsigned integer for PPSFP application

        Args:
            primary_inputs (list): primary inputs of the circuit

        Returns:
            representative_int(dict): Key:primary input Value:integer representation
        """    
        representative_int={}
        for a in primary_inputs:
            representative_int[a]=[]
        for a in range(2**len(primary_inputs)):
            aux=0
            c=bin(a)[2:].zfill(len(primary_inputs)) #transform to binary 
            while aux<len(primary_inputs):
                representative_int[primary_inputs[aux]].append(c[aux])
                aux+=1
        for a in representative_int.keys():
            representative_int[a]=int(''.join(representative_int[a]),2)
        return representative_int

    def __a12int(self, primary_inputs:int|list, results:list):
        """transform the a1 complement to an unsigned integer

        Args:
            primary_inputs (int|list): the circuit primary inputs
            results (list): the a1 result from the logic gates operations

        Returns:
            results (list): a list of unsigned integers
        """    
        if isinstance(primary_inputs,list):
            nbits=len(primary_inputs)
        else:
            nbits=primary_inputs
        bit_mask=int('1'*2**nbits,2)
        for a,b in enumerate(results):
            if b<0:
                results[a]=b&bit_mask
        return results

    def truth_table(self, primary_inputs:list, primary_outputs:list,circ_struc:list):
        '''
        Params:
            primary_inputs(list): A list of the primary input signals index
            primary_outputs(list): A list of the primary output signals index
            circ_struct(list): A list with the relationships between inputs and outputs
        Returns:
            fault_free_circuit(dict): key:binary input for primary inputs value:fault-free output
        '''
        if len(self.signals[0])>10:
            print("The circuit is too big, truth table is not being generated")
            return
        else:
            self.__log("Beginning truth table generation")
            t0=datetime.now()
            b=self.__bin2int(primary_inputs)
            normal_output=self.circuit_code(b,circ_struc)
            fault_free_circuit=self.__a12int(primary_inputs,[normal_output[x] for x in primary_outputs])
            self.__log("Finished generating truth table")
            print(f'Time take bit logic vector: {datetime.now()-t0}')
            return fault_free_circuit
    
    def generate_test_vector(self, limit:int=100):
        "Tries to generate test vector to detect ALL SA faults"
        t0=datetime.now()
        self.__log("Starting to generate test vectors")
        test_vector=[]
        finish=False
        for x,y in self.signals.items():
            if x>=0:
                for u in y:
                    for t in ['0','1']: #considering single SA fault
                        z=self.singleSA(u,t)
                        for t in z:
                            if t not in test_vector:
                                if len(test_vector)>=limit:
                                    finish=True
                                    break
                                test_vector.append(t)
                        print()
                        if finish:
                            break
                    if finish:
                        break
                    print('*'*100)
                if finish:
                    break
        print("For this circuit, this vectors may detect all SA faults")
        print("Total: ",len(test_vector))
        for z in test_vector:
            print(z)
        self.__log("Finished generating test vectors")
        print(f'Time take to determine:{datetime.now()-t0}')
        return 

    def read_bench(self, bench_file:str):
        """Reads the bench file and determines the generation of truth table or paths generation

        Args
        -------
            bench_file : str
                the path of the bench file to evaluate

        Returns
        -------
            circ_struct: list
                relationship input, gate and output

            signal_hierarchy: dict
                signals map of the circuit
            
            truth table: dict
                ONLY if the circuit has 8 or less inputs, the truth table is generated
        """      
        t0=datetime.now()
        aux=0        
        self.signals[-1]=[]
        self.signals[0]=[] #[0]=PI [-1]=PO
        gates={}
        fanout_stems={}
        gate_inputs=0
        n_inv=0
        logic_gate_operations=0
        with open(bench_file) as f:
            while True:
                a=f.readline().strip()
                if aux>3:
                    break
                if not(a):
                    aux+=1
                    continue
                else:
                    if "#" in a:
                        continue
                    else:
                        if 'INPUT' in a or 'OUTPUT' in a: #connections for primary input and primary output
                            b=a.split('(')[1][:-1]
                            if 'INPUT' in a:
                                self.signals[0].append(b)
                                fanout_stems[b]=0
                            else:
                                self.signals[-1].append(b)
                        else: # signal = gate (input signal)
                            self.circuit.append(a)
                            logic_gate_operations+=1
                            if 'NOT' in a: #getting the number of inverters
                                n_inv+=1
                            gate=a.split(' = ')[1].split('(')[0].strip()
                            if gate not in gates:
                                gates[gate]=0
                            gates[gate]+=1
                            
                            for z in a.split(' = ')[1].split('(')[1][:-1].split(','):
                                ind=0
                                while ind<(len(self.signals)-1):
                                    if z in self.signals[ind]:
                                        ind+=1
                                        break
                                    ind+=1
                                for x in self.signals.values():
                                    if z in x:
                                        fanout_stems[z]+=1
                                if 'BUFF' not in a:
                                    gate_inputs+=1
                            if ind not in self.signals:
                                self.signals[ind]=[]
                            self.signals[ind].append(a.split('=')[0].strip())
                            fanout_stems[a.split('=')[0].strip()]=0
        f.close()
        #sets the variables to show
        self.primary_inputs=self.signals[0]
        self.primary_outputs=self.signals[-1]
        self.gates=gates

        self.__log (f"Finished reading bench file: {bench_file}")
        stems=0
        for y,z in fanout_stems.items():
            if z>1:
                stems+=1
        aux=0
        for z in self.signals.values():
            aux+=len(z)
        self.__log (f'There area {aux*2} possible faulty circuits under the single-fault assumption')
        print(f'Number of PIs: {len(self.signals[0])}')
        print(f'Number of POs: {len(self.signals[-1])}')
        print(f'Number of fanout stems: {stems}')
        print(f'Number of gate inputs {gate_inputs}')
        print(f'Number of inverters: {n_inv}')
        print(f'Number of logic gate operations: {logic_gate_operations}')
        print(f'Number of collapsed faults: {2*(len(self.signals[-1])+stems)+gate_inputs-n_inv}')

        print(f'time taken: {datetime.now()-t0}')
        if len(self.signals[0])<8: #it was chosen 8, in order to use an 8 switch input from wokwi
            self.__log(f'circuit is small enough to perform a functional testing, generating truth table')
            z=self.truth_table(self.signals[0],self.signals[-1],self.circuit)
            return self.circuit, self.signals,z
        else:
            self.__log(f'circuit has over 10  inputs, too large to perfom a functional testing, a list with line justification is returned instead')
            return self.circuit, self.signals
    
    def __justification(self,signal:str, value:str ='0',needed_PIs:dict={}):
        """_summary_

        Args:
            signal (str): desired signal to justify the value
            value (str, optional): _description_. Defaults to '0'.
            needed_PIs (dict, optional): PIs values extracted from previous justifications that generate the signal where to activate the fault. Defaults to {}.

        Returns:
            testing_signal_values (dict): A dictionary with all the signals needed to activate and detect the fault
        """        
        circ=self.circuit #open to modification, not to disturb the data extracted from the bench file
        mid_signals=[signal] 
        circ.sort(reverse=True)
        for y in circ:
            output_signal=y.split(' = ')[0]
            if output_signal in mid_signals:
                [mid_signals.append(x) for x in y.split(' = ')[1].split('(')[1][:-1].split(', ') if x not in mid_signals]
        mid_signals.sort()
        mid_circ=[]
        
        for x in circ:
            #only check the output of the logic gate
            v=x.split(' = ')[0].strip()
            if v in mid_signals:
                if x not in mid_circ:
                    mid_circ.append(x)
                    print(x)
        mid_circ.sort(reverse=True)

        testing_signal_values={} #key=siganl #value=expected value (0/1)&(weak[can change]/strong[cant change])
        testing_signal_values[signal]=value+'s'
        for operation in mid_circ:
            output_signal=operation.split(' = ')[0]
            gate=operation.split(' = ')[1].split('(')[0]
            input_signal=operation.split(' = ')[1].split('(')[1][:-1].split(', ')
            value=testing_signal_values[output_signal]

            #analyze, what happens when the previous signal is 'w'??
            if gate.upper()=='AND':
                if value[0]=='1':
                    to_assign_value='1s' #value can NOT change
                else:
                    to_assign_value='0w' #value can change

            elif gate.upper()=='NAND': # or gate.upper()=='XOR' 
                if value[0]=='0':
                    to_assign_value='1s' #value can NOT change
                else:
                    to_assign_value='0w' #value can change

            elif gate.upper()=='OR':
                if value[0]=='0':
                    to_assign_value='0s' #value can NOT change
                else:
                    to_assign_value='1w' #value can change
            
            elif gate.upper()=='NOR':
                if value[0]=='0':
                    to_assign_value='1s' #value can NOT change
                else:
                    to_assign_value='0w' #value can change

            elif gate.upper()=='XOR' or gate.upper()=='XNOR': #pending to test, because all inputs in this gate must be equals
                if value[0]=='0':
                    to_assign_value='0s' #value can NOT change?
                else:
                    to_assign_value='1s' #value can change?

            elif gate.upper()=='NOT':
                if value[0]=='1':
                    to_assign_value='0'
                else:
                    to_assign_value='1'
                to_assign_value+=value[1] #the weak and strong is transfered 
            
            elif gate.upper()=='BUFF':
                if value[0]=='0':
                    to_assign_value='0'
                else:
                    to_assign_value='1'
                to_assign_value+=value[1] #the weak and strong is transfered 

            for x in input_signal:
                if x in needed_PIs and to_assign_value!=needed_PIs[x] and needed_PIs[x]!='X':
                    print("This input is being forced from a previous line justification")
                    #try to change the weak signal 
                    for y,z in testing_signal_values.items():
                        print(f'Signal:{y},Value:{z}')
                else:
                # if testing_signal_values[x][1]=='w': #pending to analyze when to 's' intervene
                    testing_signal_values[x]=to_assign_value+value[1] #it adds the information from the output to consider
        return testing_signal_values
    
    def __propagation(self,signal,value):

        circuit=self.circuit
        desired_signal=[]
        desired_signal.append(signal)
        circuit.sort()
        
        mid_circ=[]
        for x in circuit:
            #only check the input of the logic gate
            v=x.split(' = ')[1].split('(')[1][:-1].split(', ') #is a list
            aux=0
            while aux<len(v):
                if v[aux] in desired_signal:
                    mid_circ.append(x)
                    desired_signal.append(x.split(' = ')[0].strip()) #get the output for the next             
                    break
                aux+=1
        
        testing_signal_values={} #key=siganl #value=expected value (0/1)&(weak[can change]/strong[cant change])
        testing_signal_values[signal]=value
        pending_testing={}#needed signals to test in order to propagate the fault
        
        for operation in mid_circ:
            output_signal=operation.split(' = ')[0]
            gate=operation.split(' = ')[1].split('(')[0]
            input_signal=operation.split(' = ')[1].split('(')[1][:-1].split(', ')

            for z in input_signal:
                    if z in testing_signal_values:
                        value=testing_signal_values[z]
                    for y in self.implications[gate]:
                        if value in y[:-1] and y[-1] in ['D','E']:
                            next_output=y[-1]
                            if z!=signal and z not in testing_signal_values: #prevents multiple assignment in fanout circuits
                                if z not in pending_testing:# and z not in testing_signal_values: #for testing the other input, this information will need to have line justification
                                    pending_testing[z]=[]
                                for x in y[:-1]:
                                    if x not in pending_testing[z] and x not in ['D','E']:# and z not in testing_signal_values: #this ensures a single stuck at fault
                                        pending_testing[z].append(x)
                            else:
                                continue
            testing_signal_values[output_signal]=next_output#assign the corresponding SA fault propagation to the output signal 
            signal=output_signal
        return pending_testing 
    
    def singleSA (self, signal:str, SA_value:str='0'):
        PIs=dict.fromkeys(self.signals[0],'X')
        if SA_value=='0':
            z=self.__propagation(signal, 'D')
            aux='1'
        elif SA_value=='1':
            z=self.__propagation(signal, 'E')
            aux='0'
        
        #first testing the solicited signal 
        y=self.__justification(signal,aux)
        print(f"PIs that activate SA@{SA_value} in signal:{signal}")
        for x in PIs:
            if x in y:
                PIs[x]=y[x]
        print(PIs)
        print(f'Pending to test: {z}')
        
        #then run the other needed testing obtained from the propagation self.circuit
        pending_testing=z#needed signals to test in order to propagate the fault
        
        test_vector=[]
        #aggregate the posibilities from the other signals to be tested
        for y,z in pending_testing.items():
            for x in z:
                u=self.__justification(y,x,PIs)
                print(u)
                aux=''
                for t,s in PIs.items():
                    if s =='X': #looking to replace 
                        if t in u:
                            print(f'{t}:{u[t][0]}',end=" ")
                            aux+=u[t][0]
                        else:
                            print(f'{t}:X',end=" ")
                            aux+='X'
                    else:
                        print(f'{t}:{s[0]}',end=" ")
                        aux+=s[0]
                print(aux)
                if len(test_vector)<100:
                    test_vector.append(aux)
                else:
                    return test_vector
                print()
        return test_vector

    def test(self, test_file:str=''):
        """reads the test vector form the test file and return the yield of the tests
        Args:
            test_file (str): file with test vectors

        Returns:
            _type_: _description_
        """
        self.__log("Beggining circuit test")
        t0=datetime.now()
        signal_line={x:[] for x in self.signals[0]}
        aux=0
        if test_file:
            with open(test_file) as f:
                while True:
                    line=f.readline().strip()
                    if not(line):
                        break
                    else: #I assume the data is organized in the bench stated order
                        [signal_line[y].append(line[x]) for x,y in enumerate(self.signals[0])]
                        aux+=1
            f.close()
            for x in signal_line:
                signal_line[x]=int(''.join(signal_line[x]),2)
        #generate signal line from the recommended test vectors from the singleSA function

        ####
        fault_free=self.circuit_code(signal_line,self.circuit)#fault free
        aux3={x:y for x,y in fault_free.items() if x in self.signals[-1]}

        aux1=0
        aux2=0
        for u in self.signals.values():
            for x in u:
                for y in ['0','1']:                
                    SA_fault=self.circuit_code(signal_line,self.circuit,{x:int(y*aux,2)})
                    for z in self.signals[-1]:
                        if aux3[z]!=SA_fault[z]:
                            aux2+=1
                        aux1+=1
        print("*"*100)
        print(f"Detected faults: {aux2}")
        print(f'Total # of faults: {aux1}')
        print(f'Detection percentage: {aux2/aux1*100:.2f}%')
        self.__log(f"Finished running test file {test_file}")
        print(f'Time taken: {datetime.now()-t0}')
        return
    
    def __logic_gate_diagram(self, gate:str,number:int,top:int,left:int):
        '''Writes the code for the logic gates 
        Params
        -------
            gate(str): the logic gate desired
            number(int): the number for id
            top(int): top value for wokwi reference system
            left(int): left value for wokwi reference system
        Returns
        -------
            part_json(str): the corresponding json to draw the circuit on Wokwi
            output_json(str): the correspondin json to indicate the ouput\
        '''
        if gate=='NAND':
            type="wokwi-gate-nand-2"
        elif gate=='AND':
            type="wokwi-gate-and-2"
        elif gate=='NOR':
            type= "wokwi-gate-nor-2"
        elif gate=='OR':
            type="wokwi-gate-or-2"
        elif gate=='XOR':
            type="wokwi-gate-xor-2"
        elif gate=='XNOR':
            type="wokwi-gate-xnor-2"
        elif gate=='NOT':
            type="wokwi-gate-not"
        elif gate=='BUFF':
            type="wokwi-gate-buffer"
            
        return f'"type": "{type}", "id":"{gate.lower()}{str(number)}","top":{top},"left":{left}'

    def __gate_left_top(self):
        """Determines the top and left coordinates of the logic gates and text labels

        Returns:
            rel_pos (dict): A dictionary with the following structure 
                Key:signal
                Value (list):[left coordinate, top coordinate]
        """
        rel_pos={} #key: signal #value[left,top]
        for y,z in self.signals.items():
            if y>=0:
                for u,x in enumerate(z):
                    rel_pos[x]=[y,u]
        
        self.circuit.sort() #orden the circuits

        for s in self.circuit:
            #logic gates
            aux=s.split('=')[0].strip()#output
            aux1=s.split('=')[1].split('(')[1][:-1].split(',')#inputs
            w=0      
            for x in aux1:
                w+=rel_pos[x.strip()][1]
            rel_pos[aux][1]+=(w/len(aux1))

        return rel_pos

    def __lines(self, gates:dict,circ, connections:list=[]):
        '''creates the lines conecting the logic gates
        gates=the Key: signal, value:[gateid, color]
        circ= the relationship between the signals
        '''
        aux1=['A','B']
        g_out=circ.split(' = ')[0]#output
        g_in=circ.split(' = ')[1].split('(')[1][:-1].split(',') #inputs
        if g_out in gates:
            for x in g_in:
                if len(g_in)>1: #2 signals inputs
                    aux3=aux1[g_in.index(x)]
                else:
                    aux3='IN'
                aux4=''
                if 'sw'not in gates[x.strip()][0]:
                    aux4=':OUT'
                connections.append(f'["{gates[x.strip()][0]}{aux4}","{gates[g_out][0]}:{aux3}","{gates[x.strip()][1]}"],')#prints logic gate connection and color
        return connections

    def generate_diagram(self):
        '''Generates wokwi diagram for circuits under 10PIs
        '''
        if len(self.circuit)>100 or len(self.signals)>10:
            print("Circuit is too large, problems to ")
            return
        
        
        rel_pos=self.__gate_left_top()
        aux={}#key:signal value=[gate, color]
        parts=[]
        connections=[]
        for y,z in self.signals.items():#establishing the inputs connection with the PIs and signals coloring
            if y>=0:
                aux1=1
                for x in z:
                    if y==0:
                        aux[x]=['sw1:'+str(aux1)+'b']
                        aux1+=1
                    else:
                        aux[x]=[]
                    #generating color for the signal
                    hex_color_code='#'
                    for _ in range(6):
                        hex_color_code+=random.choice('0123456789abcdef')
                    aux[x].append(hex_color_code)
        for y,z in aux.items():
            print(f'Signal:{y}, gate and color:{z}')
        print('*'*100)

        for d,e in enumerate(self.circuit): # establishing logic gates for corresponding signals
            gate=e.split(' = ')[1].split('(')[0]
            g_out=e.split(' = ')[0]
            aux[g_out].insert(0,gate.lower()+str(d))

        for d,e in enumerate(self.circuit): # for logic gates
            gate=e.split(' = ')[1].split('(')[0]
            g_out=e.split(' = ')[0]
            parts.append(f'"type": "wokwi-text","id":"text{str(d)}","top":{rel_pos[g_out][1]*100},"left":{rel_pos[g_out][0]*120+100},"attrs":{'{'}"text":"{g_out}"{'}'}') #text labels
            parts.append(self.__logic_gate_diagram(gate,d,rel_pos[g_out][1]*100,rel_pos[g_out][0]*120))#logic gate
            connections=self.__lines(aux,e,connections)

        print('"parts":[')
        for z in parts:
            print("{",end="")
            print(z,end="")
            print("},")
        print('{"type": "wokwi-dip-switch-8", "id": "sw1", "top": 0, "left": 0, "rotate": 90}')#adding a switch for the ipnuts
        print("],")
        print('"connections":[')
        for z in connections:
            print(z)
        print("]")
        print(f'Try out the circuit in the following website: https://wokwi.com/projects/354858054593504257')
        