#setting libraries
from datetime import *

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
            if '.bench' in bench_file_name:
                #setting time to Japan time (UTC+9)
                self.jpTime=datetime.now(timezone(timedelta(hours=9)))
                self.t0=self.jpTime.now() #sets starting time
                self.read_bench(bench_file_name)
                print("Information loaded")
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
            print(fault_free_circuit)
            return fault_free_circuit

    def SA_fault(self,signal:str, SA_value:int|str):

        if isinstance(SA_value,int):
            SA_value=str(SA_value)

        self.__log("Generating SA fault")
        test_vector=dict.fromkeys(list(set(self.signals[0])-set(self.line[signal])),'X')
        test_vector.update(self.__bin2int(self.line[signal]))
        print(f'Primary inputs associated: {self.line[signal]}')

        #fault free
        aux=self.circuit_code(test_vector,self.circuit)
        fault_free={x:y for x,y in aux.items() if x in self.signals[-1]}
        fault_free[signal]=aux[signal]
        
        #faulty circuit
        aux1=self.circuit_code(test_vector,self.circuit,{signal:int(SA_value*2**len(self.signals[0]),2)})
        faulty={x:y for x,y in aux1.items() if x in self.signals[-1]}
        faulty[signal]=aux1[signal]

        interest_vectors=[]
        if fault_free!=faulty:
            aux=self.__a12int(len(self.line[signal]),[fault_free[signal]^faulty[signal]])[0]
            aux1=[bin(x)[2:].zfill(len(self.line[signal])) for x,y in enumerate(bin(aux)[2:].zfill(2**len(self.line[signal]))) if y=='1']
            aux5=''
            for i in aux1:
                aux3=''
                for aux4 in self.signals[0]:
                    if aux4 in self.line[signal]:
                        aux5=i[self.line[signal].index(aux4)]
                    else:
                        aux5='X'
                    aux3+=aux5
                if aux3 not in interest_vectors:
                    interest_vectors.append(aux3)
        self.__log("Finished obtaining the test vectors that are able to detect the desired fault")
        return interest_vectors
        

    def paths_generations(self):
        """Generates the paths of signals withing a circuit

        Parameters
        --------
            circ_struct (list): the list of logic operations that relates inputs and outputs
            hierarchy (dict): the signal hierarchy of the circuit

        Returns
        --------
        line (list)
                A list with all the paths of the signals, all referenced to PIs
        """    
        self.__log("Begging path generation")
        t0=datetime.now()
        main_path=[[x] for x in self.signals[0]]    
        last_item=[x for x in self.signals[0]]
        fanout_path={}
        for g in self.circuit:
            output=g.split(' = ')[0]
            inputs=g.split(' = ')[1].split('(')[1][:-1].split(', ')
            for h in inputs:
                aux=last_item.count(h)
                if aux==0:
                    if h not in self.signals[0]: #if is a PI, disregard the fanout
                        fanout_path[h]=[]
                    main_path.append([h, output])
                    last_item.append(output)
                else:
                    aux1=0
                    while aux>0:
                        if h in last_item:
                            main_path[last_item.index(h,aux1)].append(output)
                            last_item[last_item.index(h,aux1)]=output
                            aux1+=1
                        aux-=1

        ##pending to fix, this function may result slow for large fanout data set. Think in implementing a 
        for g in fanout_path.keys():
            for h in main_path: #only analyze for the one in the PIs
                if g in h and h[0] in self.signals[0]:
                    fanout_path[g].append(h[0])#adding the PIs
        
        self.line={}
        for h in self.signals.keys():
            if h>0:
                for i in self.signals[h]:
                    conn_PIs=[]
                    if i in fanout_path.keys():# first check for the fanout branches
                        conn_PIs=fanout_path[i]
                    else: # check for the main paths
                        for j in main_path:
                            if i in j:
                                if j[0] in self.signals[0] and j[0] not in conn_PIs:
                                    conn_PIs.append(j[0])
                                elif j[0] in fanout_path.keys():
                                    for k in fanout_path[j[0]]:
                                        if k not in conn_PIs:
                                            conn_PIs.append(k)
                    self.line[i]=conn_PIs
        self.__log("Finished path generation")
        print(f"Time taken: {datetime.now()-t0}")
        return self.line
    #reading the bench file to assign the input, output and intermediate connections.
    #read only once (the rutine is the same for ALL the data)
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
                            y='0'
                            #getting gate inputs
                            for z in a.split(' = ')[1].split('(')[1][:-1].split(', '):
                                try: #try to convert to int
                                    y=max(int(y),int(z))
                                except: #works with string characters
                                    y=max(y,z)
                                for x in self.signals.values():
                                    if z in x:
                                        fanout_stems[z]+=1
                                if 'BUFF' not in a:
                                    gate_inputs+=1
                            ind=0
                            y=str(y)
                            
                            #setting signal hierarchy
                            #evaluates in string format
                            while ind<(len(self.signals)-1):                            
                                if y not in self.signals[ind]:
                                    ind+=1
                                else:
                                    break
                            ind+=1
                            if ind not in self.signals:
                                self.signals[ind]=[]
                            self.signals[ind].append(a.split(' = ')[0])
                            fanout_stems[a.split(' = ')[0]]=0
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
            z=self.paths_generations()
            return self.circuit, self.signals,z