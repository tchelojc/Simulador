from qiskit import QuantumCircuit, transpile, execute, Aer

# Criação do circuito
qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

# Selecionar o simulador
simulator = Aer.get_backend('qasm_simulator')

# Transpilar e executar
compiled_circuit = transpile(qc, simulator)
job = execute(compiled_circuit, backend=simulator)

# Resultados
result = job.result()
counts = result.get_counts()
print("Resultado da simulação:", counts)
