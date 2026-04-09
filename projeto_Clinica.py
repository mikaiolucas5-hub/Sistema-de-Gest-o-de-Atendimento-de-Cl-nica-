# ================ MODELO PARA APRESENTAÇÃO DE PROJETO DE GESTÃO HOSPITALAR COM PYTHON E CUSTOMTKINTER ===============
import customtkinter as ctk
import json, os
from datetime import datetime

ctk.set_appearance_mode("light")

# ================= DESIGN SISTEMATIZADO =================
CORES = {
    "bg": "#F1F5F9",
    "card": "#FFFFFF",
    "sidebar": "#0F172A",
    "sidebar_hover": "#1E293B",
    "primary": "#2A9D8F",
    "primary_hover": "#23867A",
    "text": "#1E293B",
    "muted": "#64748B",
    "border": "#E2E8F0",
    "danger": "#E76F51",
    "accent": "#38BDF8"
}

PATH = "data/db.json"

# ================= DATABASE MANAGER =================
class DB:
    def __init__(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(PATH):
            self.save({"pacientes": [], "atendimentos": []})

    def load(self):
        try:
            with open(PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"pacientes": [], "atendimentos": []}

    def save(self, data):
        with open(PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

db_manager = DB()

# ================= MODELS (LÓGICA) =================
class PacienteModel:
    def listar(self):
        return db_manager.load().get("pacientes", [])

    def cadastrar(self, nome, cpf, tel, email):
        if not nome or not cpf: return False
        data = db_manager.load()
        pacientes = data.get("pacientes", [])
        new_id = max([p["id"] for p in pacientes], default=0) + 1
        
        pacientes.append({
            "id": new_id, "nome": nome, "cpf": cpf, 
            "telefone": tel, "email": email
        })
        data["pacientes"] = pacientes
        db_manager.save(data)
        return True

    def buscar(self, termo):
        termo = termo.lower()
        return [p for p in self.listar() if termo in p["nome"].lower() or termo in p["cpf"]]

    def deletar(self, pid):
        data = db_manager.load()
        data["pacientes"] = [p for p in data.get("pacientes", []) if p["id"] != pid]
        data["atendimentos"] = [a for a in data.get("atendimentos", []) if a["paciente_id"] != pid]
        db_manager.save(data)

class AtendimentoModel:
    def listar(self, paciente_id=None):
        atendimentos = db_manager.load().get("atendimentos", [])
        if paciente_id:
            return [a for a in atendimentos if a["paciente_id"] == int(paciente_id)]
        return atendimentos

    def registrar(self, pid, desc):
        if not desc or not pid: return False
        data = db_manager.load()
        atendimentos = data.get("atendimentos", [])
        new_id = max([a["id"] for a in atendimentos], default=0) + 1
        
        atendimentos.append({
            "id": new_id,
            "paciente_id": int(pid),
            "descricao": desc,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M")
        })
        data["atendimentos"] = atendimentos
        db_manager.save(data)
        return True

    def hoje(self):
        hoje_str = datetime.now().strftime("%d/%m/%Y")
        return [a for a in self.listar() if a["data"].startswith(hoje_str)]

# Instâncias
paciente_model = PacienteModel()
atendimento_model = AtendimentoModel()

# ================= INTERFACE (VIEW) =================
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MedSync Pro - Gestão Hospitalar")
        self.geometry("1250x800")
        self.configure(fg_color=CORES["bg"])

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=260, fg_color=CORES["sidebar"], corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        
        # Main Content Area
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew")
        
        self.main = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent", corner_radius=0)
        self.main.pack(fill="both", expand=True, padx=40, pady=30)

        self.build_sidebar()
        self.tela_dashboard()

    def build_sidebar(self):
        ctk.CTkLabel(self.sidebar, text="🏥 MedSync", font=("Inter", 26, "bold"), text_color=CORES["primary"]).pack(pady=(40, 10))
        
        menu = [
            ("Dashboard", self.tela_dashboard),
            ("Pacientes", self.tela_pacientes),
            ("Novo Paciente", self.tela_cadastro),
            ("Atendimentos", self.tela_atendimentos),
            ("Novo Atendimento", self.tela_novo_atendimento)
        ]

        for text, cmd in menu:
            btn = ctk.CTkButton(self.sidebar, text=f"  {text}", font=("Inter", 14), fg_color="transparent",
                                text_color="#F8FAFC", hover_color=CORES["sidebar_hover"], anchor="w",
                                height=45, command=cmd)
            btn.pack(fill="x", padx=20, pady=5)

    def clear(self):
        for w in self.main.winfo_children(): w.destroy()

    def header(self, title, subtitle):
        ctk.CTkLabel(self.main, text=title, font=("Inter", 32, "bold"), text_color=CORES["text"]).pack(anchor="w")
        ctk.CTkLabel(self.main, text=subtitle, font=("Inter", 14), text_color=CORES["muted"]).pack(anchor="w", pady=(0, 30))

    def create_card(self, master):
        card = ctk.CTkFrame(master, fg_color=CORES["card"], corner_radius=15, border_width=1, border_color=CORES["border"])
        card.pack(fill="x", pady=10)
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=25, pady=20)
        return inner

    # --- TELAS ---
    def tela_dashboard(self):
        self.clear()
        self.header("Dashboard", "Visão geral da clínica")
        
        row = ctk.CTkFrame(self.main, fg_color="transparent")
        row.pack(fill="x")

        stats = [
            ("Atendimentos Hoje", len(atendimento_model.hoje()), CORES["primary"]),
            ("Total Pacientes", len(paciente_model.listar()), CORES["accent"]),
            ("Total Atendimentos", len(atendimento_model.listar()), "#818CF8")
        ]

        for t, v, c in stats:
            card = ctk.CTkFrame(row, fg_color=CORES["card"], corner_radius=15, height=120, border_width=1, border_color=CORES["border"])
            card.pack(side="left", expand=True, fill="x", padx=10)
            card.pack_propagate(False)
            ctk.CTkLabel(card, text=t, font=("Inter", 12, "bold"), text_color=CORES["muted"]).pack(pady=(20, 0), padx=20, anchor="w")
            ctk.CTkLabel(card, text=str(v), font=("Inter", 36, "bold"), text_color=c).pack(padx=20, anchor="w")

    def tela_pacientes(self):
        self.clear()
        self.header("Pacientes", "Gerenciamento de registros")

        search_entry = ctk.CTkEntry(self.main, placeholder_text="🔍 Buscar nome ou CPF...", height=40)
        search_entry.pack(fill="x", pady=(0, 20))

        lista = ctk.CTkFrame(self.main, fg_color="transparent")
        lista.pack(fill="both", expand=True)

        def render(data):
            for w in lista.winfo_children(): w.destroy()
            for p in data:
                row = self.create_card(lista)
                txt_info = ctk.CTkLabel(row, text=p["nome"], font=("Inter", 16, "bold"))
                txt_info.pack(side="left", anchor="w")
                
                sub_info = ctk.CTkLabel(row, text=f"  |  CPF: {p['cpf']}", text_color=CORES["muted"])
                sub_info.pack(side="left", anchor="w")

                btns = ctk.CTkFrame(row, fg_color="transparent")
                btns.pack(side="right")
                
                ctk.CTkButton(btns, text="Atender", width=80, command=lambda i=p["id"]: self.tela_novo_atendimento(i)).pack(side="left", padx=5)
                ctk.CTkButton(btns, text="Excluir", width=80, fg_color="#FEE2E2", text_color=CORES["danger"], 
                              command=lambda i=p["id"]: [paciente_model.deletar(i), self.tela_pacientes()]).pack(side="left")

        search_entry.bind("<KeyRelease>", lambda e: render(paciente_model.buscar(search_entry.get())))
        render(paciente_model.listar())

    def tela_cadastro(self):
        self.clear()
        self.header("Novo Paciente", "Cadastro no sistema")
        container = self.create_card(self.main)
        
        inputs = {}
        for campo in ["Nome", "CPF", "Telefone", "Email"]:
            ctk.CTkLabel(container, text=campo, font=("Inter", 12, "bold")).pack(anchor="w", pady=(10,0))
            e = ctk.CTkEntry(container, height=35)
            e.pack(fill="x", pady=5)
            inputs[campo] = e

        def salvar():
            if paciente_model.cadastrar(inputs["Nome"].get(), inputs["CPF"].get(), inputs["Telefone"].get(), inputs["Email"].get()):
                self.tela_pacientes()

        ctk.CTkButton(container, text="Salvar Cadastro", height=40, fg_color=CORES["primary"], command=salvar).pack(pady=20, fill="x")

    def tela_atendimentos(self, pid=None):
        self.clear()
        self.header("Atendimentos", "Histórico de consultas")
        
        atendimentos = atendimento_model.listar(pid)
        pacientes = {p["id"]: p["nome"] for p in paciente_model.listar()}

        if not atendimentos:
            ctk.CTkLabel(self.main, text="Nenhum atendimento registrado.", text_color=CORES["muted"]).pack(pady=20)
            return

        for a in reversed(atendimentos):
            row = self.create_card(self.main)
            nome = pacientes.get(a["paciente_id"], "Paciente Excluído")
            ctk.CTkLabel(row, text=f"{nome} - {a['data']}", font=("Inter", 14, "bold"), text_color=CORES["primary"]).pack(anchor="w")
            ctk.CTkLabel(row, text=a["descricao"], wraplength=700, justify="left").pack(anchor="w", pady=5)

    def tela_novo_atendimento(self, pid_pre=None):
        self.clear()
        self.header("Novo Atendimento", "Registro de queixa e evolução")
        container = self.create_card(self.main)

        pacientes = paciente_model.listar()
        opcoes = [f"{p['id']} - {p['nome']}" for p in pacientes]
        
        ctk.CTkLabel(container, text="Paciente:", font=("Inter", 12, "bold")).pack(anchor="w")
        combo = ctk.CTkComboBox(container, values=opcoes, width=400)
        combo.pack(anchor="w", pady=10)

        if pid_pre:
            for opt in opcoes:
                if opt.startswith(f"{pid_pre} -"):
                    combo.set(opt)

        ctk.CTkLabel(container, text="Descrição:", font=("Inter", 12, "bold")).pack(anchor="w")
        txt = ctk.CTkTextbox(container, height=150)
        txt.pack(fill="x", pady=10)

        def salvar():
            try:
                pid = int(combo.get().split(" - ")[0])
                if atendimento_model.registrar(pid, txt.get("1.0", "end").strip()):
                    self.tela_atendimentos()
            except: pass

        ctk.CTkButton(container, text="Registrar", height=40, fg_color=CORES["primary"], command=salvar).pack(fill="x", pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()