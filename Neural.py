import numpy as np

def initialize_network(input_neu,output_neu):
    
    input_neurons=input_neu
    hidden_neurons=input_neurons+1
    output_neurons=output_neu
    
    n_hidden_layers=1
    
    net=list()
    
    for h in range(n_hidden_layers):
        if h!=0:
            input_neurons=len(net[-1])
            
        hidden_layer = [ { 'weights': np.random.uniform(size=input_neurons)} for i in range(hidden_neurons) ]
        net.append(hidden_layer)
    output_layer = [ { 'weights': np.random.uniform(size=hidden_neurons)} for i in range(output_neurons)]
    net.append(output_layer)
    
    return net

def activate_sigmoid(sum):
    return (1/(1+np.exp(-sum)))

def sigmoidDerivative(output):
    return output*(1.0-output)

def forward_propagation(net,input):
    row=input
    for layer in net:
        prev_input=np.array([])
        for neuron in layer:
            sum=neuron['weights'].T.dot(row)
#            
            result=activate_sigmoid(sum)
            neuron['result']=result
            
            prev_input=np.append(prev_input,[result])
        row =prev_input
    
    return row

def back_propagation(net,row,expected):
     for i in reversed(range(len(net))):
            layer=net[i]
            errors=np.array([])
            if i==len(net)-1:
                results=[neuron['result'] for neuron in layer]
                errors = expected-np.array(results) 
            else:
                for j in range(len(layer)):
                    herror=0
                    nextlayer=net[i+1]
                    for neuron in nextlayer:
                        herror+=(neuron['weights'][j]*neuron['delta'])
                    errors=np.append(errors,[herror])
            
            for j in range(len(layer)):
                neuron=layer[j]
                neuron['delta']=errors[j]*sigmoidDerivative(neuron['result'])

def updateWeights(net,input,lrate):
    
    for i in range(len(net)):
        inputs = input
        if i!=0:
            inputs=[neuron['result'] for neuron in net[i-1]]

        for neuron in net[i]:
            for j in range(len(inputs)):
                neuron['weights'][j] = neuron['weights'][j]+lrate*neuron['delta']*inputs[j]


def training(net,Feature,result,lrate,n_outputs):
    errors=[]
    for epoch in range(20):
        sum_error=0
        for i,row in enumerate(Feature):
            outputs=forward_propagation(net,row)
            expected = result[i]
            sum_error = sum_error + sum([(expected[j]-outputs[0])**2 for j in range(len(expected))])
            back_propagation(net,row,expected)
            updateWeights(net,row,lrate)
            
        print('>itr=%d,error=%.3f'%(epoch,sum_error))
        errors.append(sum_error)
    return errors
    
def predict(network, row):
    outputs = forward_propagation(network, row)
    return outputs
