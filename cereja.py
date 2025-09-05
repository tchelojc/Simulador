# cereja_platform.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit.quantum_info import Statevector
import asyncio
import websockets
import json
from pathlib import Path  # <-- ADICIONE ISSO

# Configuração inicial DEVE SER A PRIMEIRA CHAMADA
st.set_page_config(
    page_title="Cereja Q-Platform",
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== SERVIÇOS QUÂNTICOS ==========
class QuantumSimulator:
    def __init__(self):
        self.backend = AerSimulator()
        self.available_gates = {
            'H': lambda qc, qubit: qc.h(qubit),
            'X': lambda qc, qubit: qc.x(qubit),
            'CX': lambda qc, qubits: qc.cx(qubits[0], qubits[1]),
            'RX': lambda qc, params: qc.rx(params[0], params[1]),
            'RY': lambda qc, params: qc.ry(params[0], params[1]),
            'RZ': lambda qc, params: qc.rz(params[0], params[1]),
            'Measure': lambda qc, qubit: qc.measure(qubit, qubit)
        }

    def create_circuit(self, num_qubits):
        return QuantumCircuit(num_qubits, num_qubits)

    def run_simulation(self, circuit, shots=1024):
        compiled = transpile(circuit, self.backend)
        job = self.backend.run(compiled, shots=shots)
        return job.result()

# ========== INTERFACE DO SIMULADOR ==========
def render_quantum_simulator():
    with st.container(border=True):
        st.header("⚛️ Simulador Quântico Avançado")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            num_qubits = st.slider("Número de Qubits", 1, 5, 2)
            shots = st.slider("Número de Medições", 1, 5000, 1024)
            qc = QuantumSimulator().create_circuit(num_qubits)
            
            # Seletor de portas quânticas
            gate_type = st.selectbox("Selecione a Porta", list(QuantumSimulator().available_gates.keys()))
            
            # Parâmetros dinâmicos baseados na porta selecionada
            if gate_type in ['CX']:
                qubits = st.multiselect("Qubits Alvo", options=range(num_qubits), max_selections=2)
            elif gate_type in ['RX', 'RY', 'RZ']:
                angle = st.slider("Ângulo (radianos)", 0.0, 2*np.pi, np.pi/2)
                qubit = st.selectbox("Qubit", options=range(num_qubits))
                params = (angle, qubit)
            else:
                qubit = st.selectbox("Qubit", options=range(num_qubits))
                params = qubit
            
            if st.button("Adicionar Porta"):
                if gate_type in ['CX'] and len(qubits) == 2:
                    QuantumSimulator().available_gates[gate_type](qc, qubits)
                elif gate_type in ['RX', 'RY', 'RZ']:
                    QuantumSimulator().available_gates[gate_type](qc, params)
                else:
                    QuantumSimulator().available_gates[gate_type](qc, qubit)
                st.success("Porta adicionada com sucesso!")
        
        with col2:
            st.subheader("Visualização do Circuito")
            st.code(str(qc.draw(output='text')))
            
            if st.button("Executar Simulação Completa"):
                result = QuantumSimulator().run_simulation(qc, shots)
                counts = result.get_counts()
                
                fig1 = plot_histogram(counts)
                st.pyplot(fig1)
                
                try:
                    statevector = Statevector.from_instruction(qc)
                    fig2 = plot_bloch_multivector(statevector)
                    st.pyplot(fig2)
                except Exception as e:
                    st.error(f"Erro na visualização do estado quântico: {str(e)}")

# ========== INTERFACE PRINCIPAL ==========
def main_interface():
    st.title("🌀 Cereja - Plataforma de Desenvolvimento Quântico")
    
    with st.sidebar:
        st.header("Navegação Quântica")
        menu_option = st.radio("Selecione o Modo:", [
            "🚀 Início Rápido",
            "🔧 Laboratório Quântico",
            "⚛️ Simulador Avançado"
        ])
    
    if menu_option == "⚛️ Simulador Avançado":
        render_quantum_simulator()
    else:
        st.write("Selecione um modo de operação na barra lateral")

    # Seção avançada (adicione outras seções aqui)
    with st.expander("⚡ Laboratório Avançado", expanded=False):
        st.write("Configurações avançadas de circuitos quânticos")
        # Adicione componentes avançados aqui

def run_quantum_simulation():
    """Cria e simula um circuito quântico básico"""
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0,1], [0,1])

    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    result = simulator.run(compiled_circuit, shots=1024).result()
    return result.get_counts(), qc

# ========== SERVIÇOS QUÂNTICOS AVANÇADADOS ==========
class QuantumServices:
    def __init__(self):
        self.simulator = AerSimulator()
        self.executor = ThreadPoolExecutor(max_workers=4)
        
    def run_quantum_circuit(self, circuit, shots=1024):
        """Executa circuito quântico com otimizações"""
        try:
            transpiled = transpile(circuit, self.simulator, optimization_level=3)
            job = self.simulator.run(transpiled, shots=shots)
            return job.result()
        except Exception as e:
            st.error(f"Erro quântico: {str(e)}")
            return None

    def real_time_visualization(self, result):
        """Gera visualizações avançadas dos resultados"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Histograma de resultados
        counts = result.get_counts()
        plot_histogram(counts, ax=ax1)
        ax1.set_title('Distribuição de Resultados')
        
        # Diagrama de fase quântica
        statevector = result.get_statevector()
        plot_bloch_multivector(statevector, ax=ax2)
        ax2.set_title('Representação de Estado Quântico')
        
        return fig

# ========== SISTEMA DE COLABORAÇÃO EM TEMPO REAL ==========
class QuantumCollaborationHub:
    def __init__(self):
        self.websocket_server = "ws://localhost:8765"
        self.rooms = {}
        
    async def handle_connection(self, websocket, path):
        async for message in websocket:
            data = json.loads(message)
            
            if data['type'] == 'join':
                await self._handle_join(websocket, data)
            elif data['type'] == 'code_update':
                await self._broadcast(data['room'], message)
            elif data['type'] == 'quantum_operation':
                await self._process_quantum_operation(data)

    async def _handle_join(self, websocket, data):
        room = data['room']
        if room not in self.rooms:
            self.rooms[room] = []
        self.rooms[room].append(websocket)
        await self._broadcast(room, json.dumps({
            'type': 'system',
            'message': f"👤 {data['user']} entrou na sala"
        }))

    async def _broadcast(self, room, message):
        if room in self.rooms:
            for conn in self.rooms[room]:
                try:
                    await conn.send(message)
                except websockets.exceptions.ConnectionClosed:
                    self.rooms[room].remove(conn)

    async def _process_quantum_operation(self, data):
        # Processamento quântico distribuído
        qc = QuantumCircuit.from_qasm_str(data['qasm'])
        result = QuantumServices().run_quantum_circuit(qc)
        await self._broadcast(data['room'], json.dumps({
            'type': 'quantum_result',
            'result': result.get_counts(),
            'operation_id': data['operation_id']
        }))

# ========== SISTEMA DE FUSÃO DE REALIDADES ==========
class RealityFuser:
    def __init__(self):
        self.quantum_service = QuantumServices()
        
    def quantum_entangle_projects(self, project_a, project_b):
        """Emaranhamento quântico de projetos usando superposição"""
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure([0,1], [0,1])
        
        result = self.quantum_service.run_quantum_circuit(qc)
        counts = result.get_counts()
        
        return self._create_superposition_project(project_a, project_b, counts)

    def _create_superposition_project(self, a, b, counts):
        merged = {
            'name': f"{a['name']}⊗{b['name']}",
            'files': list(set(a['files'] + b['files'])),
            'entanglement_ratio': len(counts)/sum(counts.values())
        }
        return merged

# ========== INTERFACE PRINCIPAL ==========
def main_interface():
    st.title("🌀 Cereja - Plataforma de Desenvolvimento Quântico")
    
    with st.sidebar:
        st.header("Navegação Quântica")
        menu_option = st.radio("Selecione o Modo:", [
            "🚀 Início Rápido",
            "🔧 Laboratório Quântico",
            "🌌 Sala de Colaboração",
            "⚛️ Simulador Avançado"
        ])
    
    if menu_option == "🚀 Início Rápido":
        render_quick_start()
    elif menu_option == "🔧 Laboratório Quântico":
        render_quantum_lab()
    elif menu_option == "🌌 Sala de Colaboração":
        render_collaboration_space()
    elif menu_option == "⚛️ Simulador Avançado":
        render_quantum_simulator()

# ========== COMPONENTES DE INTERFACE ==========
def render_quick_start():
    with st.expander("📦 Criar Novo Projeto Quântico", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            project_name = st.text_input("Nome do Projeto", "meu_projeto_quantico")
            qubits = st.slider("Número de Qubits", 1, 10, 2)
        with col2:
            quantum_features = st.multiselect("Recursos Quânticos", [
                "Superposição",
                "Emaraanhamento",
                "Teletransporte",
                "Correção de Erros"
            ])
            
        if st.button("Criar Projeto"):
            create_quantum_project(project_name, qubits, quantum_features)
            
    with st.expander("📊 Visualização Holográfica", expanded=False):
        st.write("Visualização 3D do Espaço de Estados Quânticos")
        render_quantum_hologram()

def render_quantum_lab():
    with st.container(border=True):
        st.subheader("🔬 Laboratório de Experimentos Quânticos")
        
        col1, col2 = st.columns([2, 3])
        with col1:
            st.write("### Configuração do Circuito")
            num_qubits = st.slider("Qubits", 1, 5, 2)
            num_classical = st.slider("Bits Clássicos", 1, 5, 2)
            qc = QuantumCircuit(num_qubits, num_classical)
            
            selected_gates = {}
            for i in range(num_qubits):
                gate_type = st.selectbox(
                    f"Porta para Qubit {i}",
                    ["H", "X", "Y", "Z", "CNOT"],
                    key=f"gate_{i}"
                )
                if gate_type == "CNOT":
                    target = st.number_input(
                        f"Qubit Alvo para CNOT {i}",
                        0, num_qubits-1, (i+1)%num_qubits,
                        key=f"target_{i}"
                    )
                    qc.cx(i, target)
                else:
                    getattr(qc, gate_type.lower())(i)
                
            qc.measure_all()
            
        with col2:
            st.write("### Visualização e Simulação")
            st.write(qc.draw(output='text'))
            
            if st.button("Executar no Simulador Quântico"):
                result = QuantumServices().run_quantum_circuit(qc)
                fig = QuantumServices().real_time_visualization(result)
                st.pyplot(fig)

def render_collaboration_space():
    with st.container(border=True):
        st.subheader("🧑💻 Espaço de Colaboração Quântica")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            room_name = st.text_input("Nome da Sala", "quantum-room-1")
            user_name = st.text_input("Seu Nome", "quantum_dev")
            if st.button("🔗 Conectar à Sala"):
                asyncio.run(connect_to_collab_room(room_name, user_name))
                
        with col2:
            if 'current_room' in st.session_state:
                st.write(f"**Sala Ativa:** {st.session_state.current_room}")
                code = st.text_area("Código Colaborativo", height=300)
                
                col_btns = st.columns(3)
                with col_btns[0]:
                    if st.button("📤 Compartilhar Código"):
                        asyncio.run(send_code_update(code))
                with col_btns[1]:
                    if st.button("⚛️ Executar no Quantum Cloud"):
                        asyncio.run(run_quantum_cloud(code))
                with col_btns[2]:
                    if st.button("📊 Visualizar Resultados"):
                        display_quantum_results()

# ========== FUNÇÕES DE APOIO AVANÇADAS ==========
def create_quantum_project(name, qubits, features):
    project_path = Path("projetos") / name
    project_path.mkdir(exist_ok=True)
    
    # Cria arquivos básicos
    (project_path / "quantum_circuit.py").write_text(
        f"# Circuito Quântico com {qubits} Qubits\n" +
        "from qiskit import QuantumCircuit\n\n" +
        f"qc = QuantumCircuit({qubits})\n"
    )
    
    # Adiciona features selecionadas
    if "Superposição" in features:
        (project_path / "superposição.qasm").touch()
    if "Emaraanhamento" in features:
        (project_path / "entanglement.qasm").touch()
        
    st.success(f"Projeto {name} criado com sucesso!")

def render_quantum_hologram():
    # Visualização 3D usando plotly
    try:
        import plotly.graph_objects as go
        fig = go.Figure(data=[
            go.Scatter3d(
                x=np.random.randn(100),
                y=np.random.randn(100),
                z=np.random.randn(100),
                mode='markers',
                marker=dict(
                    size=12,
                    color=np.random.randn(100),
                    colorscale='Viridis',
                    opacity=0.8
                )
            )
        ])
        st.plotly_chart(fig, use_container_width=True)
    except ImportError:
        st.warning("Instale plotly para visualização 3D completa: pip install plotly")

# ========== GERENCIAMENTO DE CONEXÕES ==========
async def connect_to_collab_room(room, user):
    async with websockets.connect(f"ws://localhost:8765/{room}") as ws:
        st.session_state['current_room'] = room
        st.session_state['current_user'] = user
        await ws.send(json.dumps({
            'type': 'join',
            'room': room,
            'user': user
        }))
        st.success(f"Conectado à sala {room} como {user}")

async def send_code_update(code):
    async with websockets.connect(f"ws://localhost:8765/{st.session_state.current_room}") as ws:
        await ws.send(json.dumps({
            'type': 'code_update',
            'content': code,
            'user': st.session_state.current_user
        }))

# ========== CONFIGURAÇÃO DO SERVIDOR ==========
def start_websocket_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server = websockets.serve(QuantumCollaborationHub().handle_connection, "localhost", 8765)
    loop.run_until_complete(server)
    loop.run_forever()

if __name__ == "__main__":
    # Configura ambiente
    if not Path("projetos").exists():
        Path("projetos").mkdir()
        
    # Inicia servidor WebSocket em thread separada
    from threading import Thread
    Thread(target=start_websocket_server, daemon=True).start()
    
    # Executa interface principal
    main_interface()