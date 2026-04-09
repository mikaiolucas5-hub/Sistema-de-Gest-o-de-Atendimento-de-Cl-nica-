import customtkinter as ctk
import json
import os
from datetime import datetime
ctk.set_appearance_mode("light")
CORES = {
    "bg": "#F0F4F8",
    "card": "#FFFFFF",
    "sidebar": "#1E293B",
    "sidebar_hover": "#334155",
    "sidebar_active": "#2A9D8F",
    "primary": "#2A9D8F",
    "primary_hover": "#23867A",
    "primary_light": "#D1FAE5",
    "text": "#1E293B",
    "text_light": "#FFFFFF",
    "muted": "#6B7280",
    "border": "#E2E8F0",
    "row_alt": "#F8FBFF",
    "hover": "#E6F4FF",
    "danger": "#E76F51",
    "danger_hover": "#D4533B",
    "danger_light": "#FEE2E2",
    "info": "#38BDF8",
    "info_light": "#DBEAFE",
    "warning": "#F59E0B",
    "warning_light": "#FEF3C7",
    "success": "#10B981",
    "success_light": "#D1FAE5",
    "input_bg": "#F9FAFB",
    "input_border": "#D1D5DB",
    "divider": "#374151",
}
FONT_TITLE = ("Segoe UI", 28, "bold")
FONT_SUBTITLE = ("Segoe UI", 14)
FONT_HEADING = ("Segoe UI", 18, "bold")
FONT_BODY = ("Segoe UI", 13)
FONT_BODY_BOLD = ("Segoe UI", 13, "bold")
FONT_SMALL = ("Segoe UI", 11)
FONT_SMALL_BOLD = ("Segoe UI", 11, "bold")
FONT_SIDEBAR = ("Segoe UI", 14)
FONT_SIDEBAR_TITLE = ("Segoe UI", 20, "bold")
FONT_BIG_NUMBER = ("Segoe UI", 36, "bold")
FONT_BUTTON = ("Segoe UI", 13, "bold")
PATH_PACIENTES = "data/pacientes.json"
PATH_ATENDIMENTOS = "data/atendimentos.json"

def alert(master, msg, tipo="ok"):
    cor_bg = CORES["success_light"] if tipo == "ok" else CORES["danger_light"]
    cor_text = CORES["success"] if tipo == "ok" else CORES["danger"]
    icone = "  " if tipo == "ok" else "  "
    frame = ctk.CTkFrame(master, fg_color=cor_bg, corner_radius=10, height=40)
    frame.pack(fill="x", pady=(0, 10), padx=5)
    frame.pack_propagate(False)
    ctk.CTkLabel(
        frame, text=f"{icone}{msg}",
        text_color=cor_text, font=FONT_BODY_BOLD,
        anchor="w"
    ).pack(side="left", padx=15, pady=8)
    master.after(3000, frame.destroy)
# ================= DB =================
class DB:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        for path in [PATH_PACIENTES, PATH_ATENDIMENTOS]:
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8") as f:
                    json.dump([], f)
    def get(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    def save(self, path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
# ================= ATENDIMENTO MODEL =================
class AtendimentoModel:
    def __init__(self, db):
        self.db = db
    def listar(self):
        return self.db.get(PATH_ATENDIMENTOS)
    def registrar(self, paciente_id, descricao, prioridade):
        if not paciente_id or not descricao.strip():
            return False, "Preencha todos os dados do atendimento"
        atendimentos = self.db.get(PATH_ATENDIMENTOS)
        novo = {
            "id": len(atendimentos) + 1,
            "paciente_id": int(paciente_id),
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "descricao": descricao.strip(),
            "prioridade": prioridade or "Normal",
        }
        atendimentos.append(novo)
        self.db.save(PATH_ATENDIMENTOS, atendimentos)
        return True, "Atendimento registrado com sucesso"
    def filtrar_por_paciente(self, paciente_id):
        todos = self.db.get(PATH_ATENDIMENTOS)
        return [a for a in todos if a["paciente_id"] == int(paciente_id)]
    def deletar(self, atendimento_id):
        data = self.db.get(PATH_ATENDIMENTOS)
        novo = [a for a in data if a["id"] != atendimento_id]
        for i, a in enumerate(novo):
            a["id"] = i + 1
        self.db.save(PATH_ATENDIMENTOS, novo)
        return True, "Atendimento excluido"
# ================= PACIENTE MODEL =================
class PacienteModel:
    def __init__(self, db):
        self.db = db
    def listar(self):
        return self.db.get(PATH_PACIENTES)
    def buscar_por_id(self, pid):
        data = self.db.get(PATH_PACIENTES)
        for p in data:
            if p["id"] == int(pid):
                return p
        return None
    def add(self, nome, nasc, tel, email, doc):
        if not nome or not doc:
            return False, "Nome e documento sao obrigatorios"
        data = self.db.get(PATH_PACIENTES)
        if any(p["documento"] == doc for p in data):
            return False, "Documento ja cadastrado"
        data.append(
            {
                "id": len(data) + 1,
                "nome": nome,
                "nascimento": nasc,
                "telefone": tel,
                "email": email,
                "documento": doc,
                "data_cadastro": datetime.now().strftime("%d/%m/%Y"),
            }
        )
        self.db.save(PATH_PACIENTES, data)
        return True, "Paciente cadastrado com sucesso"
    def deletar(self, paciente_id):
        data = self.db.get(PATH_PACIENTES)
        novo = [p for p in data if p["id"] != paciente_id]
        for i, p in enumerate(novo):
            p["id"] = i + 1
        self.db.save(PATH_PACIENTES, novo)
        return True, "Paciente excluido"
def make_card(master, pad_x=25, pad_y=18):
    
    frm = ctk.CTkFrame(
        master,
        fg_color=CORES["card"],
        corner_radius=14,
        border_width=1,
        border_color=CORES["border"],
    )
    return frm
def make_entry(master, placeholder="", width=260):
    return ctk.CTkEntry(
        master,
        placeholder_text=placeholder,
        width=width,
        height=42,
        corner_radius=10,
        border_width=1,
        border_color=CORES["input_border"],
        fg_color=CORES["input_bg"],
        text_color=CORES["text"],
        placeholder_text_color=CORES["muted"],
        font=FONT_BODY,
    )
def make_button(master, text, command, color=None, hover_color=None, width=140, icon=None):
    fg = color or CORES["primary"]
    hv = hover_color or CORES["primary_hover"]
    btn_text = f"{icon}  {text}" if icon else text
    return ctk.CTkButton(
        master,
        text=btn_text,
        command=command,
        fg_color=fg,
        hover_color=hv,
        text_color=CORES["text_light"],
        corner_radius=10,
        height=40,
        width=width,
        font=FONT_BUTTON,
    )
def make_label(master, text, font=None, color=None):
    return ctk.CTkLabel(
        master,
        text=text,
        font=font or FONT_BODY,
        text_color=color or CORES["text"],
    )
def priority_badge(master, prioridade):
    
    configs = {
        "Normal": (CORES["info_light"], CORES["info"], "Normal"),
        "Urgente": (CORES["danger_light"], CORES["danger"], "Urgente"),
        "Alta": (CORES["warning_light"], CORES["warning"], "Alta"),
    }
    bg, fg, label = configs.get(prioridade, configs["Normal"])
    badge = ctk.CTkLabel(
        master,
        text=f"  {label}  ",
        fg_color=bg,
        text_color=fg,
        corner_radius=8,
        font=FONT_SMALL_BOLD,
        height=26,
    )
    return badge
# ================= APP =================
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.db = DB()
        self.paciente_model = PacienteModel(self.db)
        self.atendimento_model = AtendimentoModel(self.db)
        self.title("MedSync Pro")
        self.geometry("1280x800")
        self.minsize(1000, 650)
        self.configure(fg_color=CORES["bg"])
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.active_page = None
        # Sidebar
        self.sidebar = ctk.CTkFrame(
            self, width=240, fg_color=CORES["sidebar"], corner_radius=0
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        # Main content area
        self.main = ctk.CTkFrame(self, fg_color="transparent")
        self.main.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(0, weight=1)
        self.build_sidebar()
        self.show_dashboard()
    # --------- SIDEBAR ---------
    def build_sidebar(self):
        # Logo area
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(fill="x", padx=20, pady=(30, 10))
        ctk.CTkLabel(
            logo_frame,
            text="MedSync",
            font=FONT_SIDEBAR_TITLE,
            text_color=CORES["primary"],
        ).pack(anchor="w")
        ctk.CTkLabel(
            logo_frame,
            text="Sistema de Gestao Clinica",
            font=FONT_SMALL,
            text_color="#94A3B8",
        ).pack(anchor="w", pady=(2, 0))
       
        ctk.CTkFrame(
            self.sidebar, fg_color=CORES["divider"], height=1
        ).pack(fill="x", padx=20, pady=(15, 20))
      
        ctk.CTkLabel(
            self.sidebar,
            text="MENU",
            font=("Segoe UI", 11, "bold"),
            text_color="#64748B",
        ).pack(anchor="w", padx=25, pady=(0, 8))
        
        self.sidebar_buttons = {}
        menu = [
            ("Dashboard", "dashboard", self.show_dashboard),
            ("Pacientes", "pacientes", self.show_pacientes),
            ("Novo Paciente", "novo", self.show_form_paciente),
            ("Atendimentos", "atendimentos", self.show_atendimentos),
            ("Novo Atendimento", "novo_atend", self.show_form_atendimento),
        ]
        for label, key, cmd in menu:
            btn = ctk.CTkButton(
                self.sidebar,
                text=f"   {label}",
                fg_color="transparent",
                text_color="#CBD5E1",
                hover_color=CORES["sidebar_hover"],
                anchor="w",
                height=42,
                corner_radius=10,
                font=FONT_SIDEBAR,
                command=lambda k=key, c=cmd: self._nav(k, c),
            )
            btn.pack(fill="x", padx=12, pady=2)
            self.sidebar_buttons[key] = btn
      
        spacer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        spacer.pack(fill="both", expand=True)
        ctk.CTkFrame(
            self.sidebar, fg_color=CORES["divider"], height=1
        ).pack(fill="x", padx=20, pady=(0, 10))
        ctk.CTkLabel(
            self.sidebar,
            text="MedSync Pro v2.0",
            font=FONT_SMALL,
            text_color="#64748B",
        ).pack(pady=(0, 20))
    def _nav(self, key, cmd):
        
        self.active_page = key
        for k, btn in self.sidebar_buttons.items():
            if k == key:
                btn.configure(
                    fg_color=CORES["sidebar_active"],
                    text_color=CORES["text_light"],
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color="#CBD5E1",
                )
        cmd()
    
    def clear(self):
        for w in self.main.winfo_children():
            w.destroy()
    def _content_area(self):
        
        scroll = ctk.CTkScrollableFrame(
            self.main, fg_color="transparent", corner_radius=0,
            scrollbar_button_color=CORES["border"],
            scrollbar_button_hover_color=CORES["muted"],
        )
        scroll.pack(fill="both", expand=True, padx=30, pady=20)
        scroll.grid_columnconfigure(0, weight=1)
        return scroll
    def header(self, parent, title, subtitle):
        hdr = ctk.CTkFrame(parent, fg_color="transparent")
        hdr.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(
            hdr, text=title, font=FONT_TITLE, text_color=CORES["text"]
        ).pack(anchor="w")
        if subtitle:
            ctk.CTkLabel(
                hdr, text=subtitle, font=FONT_SUBTITLE, text_color=CORES["muted"]
            ).pack(anchor="w", pady=(2, 0))
        # Separator line
        ctk.CTkFrame(parent, fg_color=CORES["border"], height=1).pack(
            fill="x", pady=(0, 15)
        )
    # ================================================================
    # DASHBOARD
    # ================================================================
    def show_dashboard(self):
        self.clear()
        self.active_page = "dashboard"
        self._highlight_sidebar("dashboard")
        area = self._content_area()
        self.header(area, "Dashboard", "Resumo geral do sistema")
        # Stats row
        stats_frame = ctk.CTkFrame(area, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 20))
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        total_p = len(self.paciente_model.listar())
        total_a = len(self.atendimento_model.listar())
        atendimentos = self.atendimento_model.listar()
        urgentes = sum(1 for a in atendimentos if a.get("prioridade") == "Urgente")
        hoje = datetime.now().strftime("%d/%m/%Y")
        hoje_count = sum(1 for a in atendimentos if a.get("data", "").startswith(hoje))
        stats = [
            ("Total Pacientes", str(total_p), CORES["primary"], CORES["primary_light"]),
            ("Total Atendimentos", str(total_a), CORES["info"], CORES["info_light"]),
            ("Urgentes", str(urgentes), CORES["danger"], CORES["danger_light"]),
            ("Hoje", str(hoje_count), CORES["success"], CORES["success_light"]),
        ]
        for i, (label, value, color, bg_color) in enumerate(stats):
            stat_card = ctk.CTkFrame(
                stats_frame,
                fg_color=CORES["card"],
                corner_radius=14,
                border_width=1,
                border_color=CORES["border"],
            )
            stat_card.grid(row=0, column=i, padx=8, pady=5, sticky="nsew")
            inner = ctk.CTkFrame(stat_card, fg_color="transparent")
            inner.pack(fill="both", expand=True, padx=20, pady=20)
            
            indicator = ctk.CTkFrame(
                inner, fg_color=color, width=4, height=50, corner_radius=2
            )
            indicator.pack(side="left", padx=(0, 15))
            text_frame = ctk.CTkFrame(inner, fg_color="transparent")
            text_frame.pack(side="left", fill="both", expand=True)
            ctk.CTkLabel(
                text_frame, text=label, font=FONT_SMALL, text_color=CORES["muted"]
            ).pack(anchor="w")
            ctk.CTkLabel(
                text_frame, text=value, font=FONT_BIG_NUMBER, text_color=color
            ).pack(anchor="w")
        
        recent_card = make_card(area)
        recent_card.pack(fill="x", pady=(10, 0))
        rc_inner = ctk.CTkFrame(recent_card, fg_color="transparent")
        rc_inner.pack(fill="x", padx=25, pady=20)
        ctk.CTkLabel(
            rc_inner, text="Atendimentos Recentes", font=FONT_HEADING, text_color=CORES["text"]
        ).pack(anchor="w", pady=(0, 15))
        recentes = atendimentos[-5:][::-1] if atendimentos else []
        if not recentes:
            ctk.CTkLabel(
                rc_inner,
                text="Nenhum atendimento registrado ainda.",
                font=FONT_BODY,
                text_color=CORES["muted"],
            ).pack(anchor="w", pady=10)
        else:
            for idx, a in enumerate(recentes):
                pac = self.paciente_model.buscar_por_id(a["paciente_id"])
                pac_nome = pac["nome"] if pac else f"ID {a['paciente_id']}"
                row_bg = CORES["card"] if idx % 2 == 0 else CORES["row_alt"]
                row = ctk.CTkFrame(rc_inner, fg_color=row_bg, corner_radius=8, height=45)
                row.pack(fill="x", pady=2)
                row.pack_propagate(False)
                ctk.CTkLabel(
                    row, text=pac_nome, font=FONT_BODY_BOLD, text_color=CORES["text"]
                ).pack(side="left", padx=(15, 10), pady=8)
                ctk.CTkLabel(
                    row, text=a.get("descricao", "")[:60], font=FONT_SMALL, text_color=CORES["muted"]
                ).pack(side="left", padx=5)
                ctk.CTkLabel(
                    row, text=a["data"], font=FONT_SMALL, text_color=CORES["muted"]
                ).pack(side="right", padx=15)
                priority_badge(row, a.get("prioridade", "Normal")).pack(
                    side="right", padx=5
                )
    # ================================================================
    # PACIENTES - LISTA
    # ================================================================
    def show_pacientes(self):
        self.clear()
        self.active_page = "pacientes"
        self._highlight_sidebar("pacientes")
        area = self._content_area()
        self.header(area, "Pacientes", "Gerenciamento de pacientes cadastrados")
       
        top_bar = ctk.CTkFrame(area, fg_color="transparent")
        top_bar.pack(fill="x", pady=(0, 15))
        self.search_pac = make_entry(top_bar, placeholder="Buscar por nome...", width=300)
        self.search_pac.pack(side="left")
        self.search_pac.bind("<KeyRelease>", lambda e: self._filter_pacientes())
        make_button(
            top_bar, "Novo Paciente", self.show_form_paciente, width=160
        ).pack(side="right")
      
        table_header = ctk.CTkFrame(
            area, fg_color=CORES["sidebar"], corner_radius=10, height=45
        )
        table_header.pack(fill="x", pady=(0, 5))
        table_header.pack_propagate(False)
        cols = ["ID", "Nome", "Documento", "Telefone", "Cadastro", "Acoes"]
        widths = [60, 200, 130, 130, 100, 180]
        for col, w in zip(cols, widths):
            ctk.CTkLabel(
                table_header,
                text=col,
                font=FONT_SMALL_BOLD,
                text_color=CORES["text_light"],
                width=w,
            ).pack(side="left", padx=10, pady=10)
        
        self.pac_list_frame = ctk.CTkFrame(area, fg_color="transparent")
        self.pac_list_frame.pack(fill="x")
        self._render_pacientes()
    def _render_pacientes(self, filtro=""):
        for w in self.pac_list_frame.winfo_children():
            w.destroy()
        pacientes = self.paciente_model.listar()
        if filtro:
            pacientes = [p for p in pacientes if filtro.lower() in p["nome"].lower()]
        if not pacientes:
            ctk.CTkLabel(
                self.pac_list_frame,
                text="Nenhum paciente encontrado.",
                font=FONT_BODY,
                text_color=CORES["muted"],
            ).pack(pady=30)
            return
        for idx, p in enumerate(pacientes):
            row_bg = CORES["card"] if idx % 2 == 0 else CORES["row_alt"]
            row = ctk.CTkFrame(
                self.pac_list_frame,
                fg_color=row_bg,
                corner_radius=8,
                border_width=1,
                border_color=CORES["border"],
                height=50,
            )
            row.pack(fill="x", pady=3)
            row.pack_propagate(False)
            ctk.CTkLabel(
                row, text=str(p["id"]), font=FONT_BODY, text_color=CORES["muted"], width=60
            ).pack(side="left", padx=10)
            ctk.CTkLabel(
                row, text=p["nome"], font=FONT_BODY_BOLD, text_color=CORES["text"], width=200, anchor="w"
            ).pack(side="left", padx=10)
            ctk.CTkLabel(
                row, text=p.get("documento", ""), font=FONT_BODY, text_color=CORES["text"], width=130
            ).pack(side="left", padx=10)
            ctk.CTkLabel(
                row, text=p.get("telefone", "-"), font=FONT_BODY, text_color=CORES["muted"], width=130
            ).pack(side="left", padx=10)
            ctk.CTkLabel(
                row, text=p.get("data_cadastro", ""), font=FONT_SMALL, text_color=CORES["muted"], width=100
            ).pack(side="left", padx=10)
          
            btn_frame = ctk.CTkFrame(row, fg_color="transparent")
            btn_frame.pack(side="right", padx=10)
            ctk.CTkButton(
                btn_frame,
                text="Atender",
                fg_color=CORES["primary"],
                hover_color=CORES["primary_hover"],
                text_color=CORES["text_light"],
                corner_radius=8,
                height=32,
                width=80,
                font=FONT_SMALL_BOLD,
                command=lambda pid=p["id"]: self.modal_atendimento(pid),
            ).pack(side="left", padx=3)
            ctk.CTkButton(
                btn_frame,
                text="Excluir",
                fg_color=CORES["danger"],
                hover_color=CORES["danger_hover"],
                text_color=CORES["text_light"],
                corner_radius=8,
                height=32,
                width=80,
                font=FONT_SMALL_BOLD,
                command=lambda pid=p["id"]: self._deletar_paciente(pid),
            ).pack(side="left", padx=3)
    def _filter_pacientes(self):
        filtro = self.search_pac.get()
        self._render_pacientes(filtro)
    def _deletar_paciente(self, pid):
        ok, m = self.paciente_model.deletar(pid)
        self.show_pacientes()
        self.after(100, lambda: alert(self.pac_list_frame, m))
    # ================================================================
    # PACIENTES - FORMULARIO
    # ================================================================
    def show_form_paciente(self):
        self.clear()
        self.active_page = "novo"
        self._highlight_sidebar("novo")
        area = self._content_area()
        self.header(area, "Novo Paciente", "Preencha os dados para cadastrar um paciente")
        form_card = make_card(area)
        form_card.pack(fill="x", pady=(0, 15))
        form_inner = ctk.CTkFrame(form_card, fg_color="transparent")
        form_inner.pack(fill="x", padx=30, pady=25)
        
        form_inner.grid_columnconfigure((0, 1), weight=1)
        fields = {}
        field_defs = [
            ("Nome Completo *", "nome", "Digite o nome completo", 0, 0),
            ("Documento (CPF) *", "documento", "000.000.000-00", 0, 1),
            ("Data de Nascimento", "nascimento", "DD/MM/AAAA", 1, 0),
            ("Telefone", "telefone", "(00) 00000-0000", 1, 1),
            ("E-mail", "email", "email@exemplo.com", 2, 0),
        ]
        for label, key, placeholder, row, col in field_defs:
            grp = ctk.CTkFrame(form_inner, fg_color="transparent")
            grp.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            ctk.CTkLabel(
                grp, text=label, font=FONT_SMALL_BOLD, text_color=CORES["text"]
            ).pack(anchor="w", pady=(0, 5))
            entry = make_entry(grp, placeholder=placeholder, width=0)
            entry.pack(fill="x")
            fields[key] = entry
        
        self.form_alert = ctk.CTkFrame(form_inner, fg_color="transparent")
        self.form_alert.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(5, 0))
        
        btn_row = ctk.CTkFrame(form_inner, fg_color="transparent")
        btn_row.grid(row=4, column=0, columnspan=2, pady=(15, 0), sticky="e")
        ctk.CTkButton(
            btn_row,
            text="Cancelar",
            fg_color=CORES["border"],
            hover_color="#CBD5E1",
            text_color=CORES["text"],
            corner_radius=10,
            height=42,
            width=120,
            font=FONT_BUTTON,
            command=self.show_pacientes,
        ).pack(side="left", padx=(0, 10))
        def salvar():
            ok, m = self.paciente_model.add(
                fields["nome"].get(),
                fields["nascimento"].get(),
                fields["telefone"].get(),
                fields["email"].get(),
                fields["documento"].get(),
            )
            if ok:
                alert(self.form_alert, m, "ok")
                self.after(1500, self.show_pacientes)
            else:
                alert(self.form_alert, m, "erro")
        make_button(btn_row, "Salvar Paciente", salvar, width=180).pack(side="left")
    # ================================================================
    # ATENDIMENTOS - LISTA
    # ================================================================
    def show_atendimentos(self):
        self.clear()
        self.active_page = "atendimentos"
        self._highlight_sidebar("atendimentos")
        area = self._content_area()
        self.header(area, "Atendimentos", "Historico de atendimentos realizados")
        
        top_bar = ctk.CTkFrame(area, fg_color="transparent")
        top_bar.pack(fill="x", pady=(0, 15))
        self.search_atend = make_entry(top_bar, placeholder="Filtrar por nome do paciente...", width=300)
        self.search_atend.pack(side="left")
        self.search_atend.bind("<KeyRelease>", lambda e: self._filter_atendimentos())
        
        self.filter_prio = ctk.CTkComboBox(
            top_bar,
            values=["Todas", "Normal", "Urgente", "Alta"],
            width=150,
            height=42,
            corner_radius=10,
            border_width=1,
            border_color=CORES["input_border"],
            fg_color=CORES["input_bg"],
            button_color=CORES["primary"],
            button_hover_color=CORES["primary_hover"],
            font=FONT_BODY,
            command=lambda v: self._filter_atendimentos(),
        )
        self.filter_prio.pack(side="left", padx=10)
        self.filter_prio.set("Todas")
        make_button(
            top_bar, "Novo Atendimento", self.show_form_atendimento, width=180
        ).pack(side="right")
      
        self.atend_list_frame = ctk.CTkFrame(area, fg_color="transparent")
        self.atend_list_frame.pack(fill="x")
        self._render_atendimentos()
    def _render_atendimentos(self, filtro_nome="", filtro_prio="Todas"):
        for w in self.atend_list_frame.winfo_children():
            w.destroy()
        atendimentos = self.atendimento_model.listar()[::-1]
        if filtro_nome:
            filtered = []
            for a in atendimentos:
                pac = self.paciente_model.buscar_por_id(a["paciente_id"])
                if pac and filtro_nome.lower() in pac["nome"].lower():
                    filtered.append(a)
            atendimentos = filtered
        if filtro_prio and filtro_prio != "Todas":
            atendimentos = [a for a in atendimentos if a.get("prioridade") == filtro_prio]
        if not atendimentos:
            empty_frame = ctk.CTkFrame(
                self.atend_list_frame, fg_color=CORES["card"], corner_radius=14,
                border_width=1, border_color=CORES["border"]
            )
            empty_frame.pack(fill="x", pady=10)
            ctk.CTkLabel(
                empty_frame,
                text="Nenhum atendimento encontrado.",
                font=FONT_BODY,
                text_color=CORES["muted"],
            ).pack(pady=40)
            return
        for idx, a in enumerate(atendimentos):
            pac = self.paciente_model.buscar_por_id(a["paciente_id"])
            pac_nome = pac["nome"] if pac else f"Paciente ID {a['paciente_id']}"
           
            a_card = ctk.CTkFrame(
                self.atend_list_frame,
                fg_color=CORES["card"],
                corner_radius=12,
                border_width=1,
                border_color=CORES["border"],
            )
            a_card.pack(fill="x", pady=4)
            
            content = ctk.CTkFrame(a_card, fg_color="transparent")
            content.pack(fill="x", padx=20, pady=15)
            
            prio = a.get("prioridade", "Normal")
            prio_colors = {
                "Urgente": CORES["danger"],
                "Alta": CORES["warning"],
                "Normal": CORES["info"],
            }
            indicator = ctk.CTkFrame(
                content,
                fg_color=prio_colors.get(prio, CORES["info"]),
                width=4,
                corner_radius=2,
            )
            indicator.pack(side="left", fill="y", padx=(0, 15))
            
            info_frame = ctk.CTkFrame(content, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True)
            
            top_row = ctk.CTkFrame(info_frame, fg_color="transparent")
            top_row.pack(fill="x")
            ctk.CTkLabel(
                top_row, text=pac_nome, font=FONT_BODY_BOLD, text_color=CORES["text"]
            ).pack(side="left")
            priority_badge(top_row, prio).pack(side="left", padx=10)
            ctk.CTkLabel(
                top_row, text=a["data"], font=FONT_SMALL, text_color=CORES["muted"]
            ).pack(side="right")
            
            ctk.CTkLabel(
                info_frame,
                text=a.get("descricao", ""),
                font=FONT_BODY,
                text_color=CORES["muted"],
                anchor="w",
                wraplength=600,
                justify="left",
            ).pack(anchor="w", pady=(5, 0))
            
            ctk.CTkButton(
                content,
                text="Excluir",
                fg_color=CORES["danger"],
                hover_color=CORES["danger_hover"],
                text_color=CORES["text_light"],
                corner_radius=8,
                height=32,
                width=80,
                font=FONT_SMALL_BOLD,
                command=lambda aid=a["id"]: self._deletar_atendimento(aid),
            ).pack(side="right", padx=(10, 0))
    def _filter_atendimentos(self):
        filtro_nome = self.search_atend.get()
        filtro_prio = self.filter_prio.get()
        self._render_atendimentos(filtro_nome, filtro_prio)
    def _deletar_atendimento(self, aid):
        ok, m = self.atendimento_model.deletar(aid)
        self.show_atendimentos()
        self.after(100, lambda: alert(self.atend_list_frame, m))
    # ================================================================
    # ATENDIMENTOS - FORMULARIO (PAGINA DEDICADA)
    # ================================================================
    def show_form_atendimento(self):
        self.clear()
        self.active_page = "novo_atend"
        self._highlight_sidebar("novo_atend")
        area = self._content_area()
        self.header(area, "Novo Atendimento", "Registrar um novo atendimento para um paciente")
        form_card = make_card(area)
        form_card.pack(fill="x", pady=(0, 15))
        form_inner = ctk.CTkFrame(form_card, fg_color="transparent")
        form_inner.pack(fill="x", padx=30, pady=25)
        
        ctk.CTkLabel(
            form_inner, text="Paciente *", font=FONT_SMALL_BOLD, text_color=CORES["text"]
        ).pack(anchor="w", pady=(0, 5))
        pacientes = self.paciente_model.listar()
        pac_options = [f"{p['id']} - {p['nome']}" for p in pacientes]
        if not pac_options:
            ctk.CTkLabel(
                form_inner,
                text="Nenhum paciente cadastrado. Cadastre um paciente primeiro.",
                font=FONT_BODY,
                text_color=CORES["danger"],
            ).pack(anchor="w", pady=10)
            make_button(
                form_inner, "Cadastrar Paciente", self.show_form_paciente, width=200
            ).pack(anchor="w", pady=10)
            return
        pac_combo = ctk.CTkComboBox(
            form_inner,
            values=pac_options,
            width=400,
            height=42,
            corner_radius=10,
            border_width=1,
            border_color=CORES["input_border"],
            fg_color=CORES["input_bg"],
            button_color=CORES["primary"],
            button_hover_color=CORES["primary_hover"],
            font=FONT_BODY,
        )
        pac_combo.pack(anchor="w", pady=(0, 15))
        if pac_options:
            pac_combo.set(pac_options[0])
       
        ctk.CTkLabel(
            form_inner, text="Prioridade", font=FONT_SMALL_BOLD, text_color=CORES["text"]
        ).pack(anchor="w", pady=(0, 5))
        prio_combo = ctk.CTkComboBox(
            form_inner,
            values=["Normal", "Alta", "Urgente"],
            width=200,
            height=42,
            corner_radius=10,
            border_width=1,
            border_color=CORES["input_border"],
            fg_color=CORES["input_bg"],
            button_color=CORES["primary"],
            button_hover_color=CORES["primary_hover"],
            font=FONT_BODY,
        )
        prio_combo.pack(anchor="w", pady=(0, 15))
        prio_combo.set("Normal")

        ctk.CTkLabel(
            form_inner, text="Descricao do Atendimento *", font=FONT_SMALL_BOLD, text_color=CORES["text"]
        ).pack(anchor="w", pady=(0, 5))
        desc_text = ctk.CTkTextbox(
            form_inner,
            height=150,
            corner_radius=10,
            border_width=1,
            border_color=CORES["input_border"],
            fg_color=CORES["input_bg"],
            text_color=CORES["text"],
            font=FONT_BODY,
        )
        desc_text.pack(fill="x", pady=(0, 15))
        
        form_alert = ctk.CTkFrame(form_inner, fg_color="transparent")
        form_alert.pack(fill="x", pady=(0, 5))
        
        btn_row = ctk.CTkFrame(form_inner, fg_color="transparent")
        btn_row.pack(fill="x", pady=(5, 0))
        ctk.CTkButton(
            btn_row,
            text="Cancelar",
            fg_color=CORES["border"],
            hover_color="#CBD5E1",
            text_color=CORES["text"],
            corner_radius=10,
            height=42,
            width=120,
            font=FONT_BUTTON,
            command=self.show_atendimentos,
        ).pack(side="right", padx=(10, 0))
        def salvar():
            selected = pac_combo.get()
            try:
                pid = int(selected.split(" - ")[0])
            except (ValueError, IndexError):
                alert(form_alert, "Selecione um paciente valido", "erro")
                return
            descricao = desc_text.get("1.0", "end").strip()
            prioridade = prio_combo.get()
            ok, m = self.atendimento_model.registrar(pid, descricao, prioridade)
            if ok:
                alert(form_alert, m, "ok")
                self.after(1500, self.show_atendimentos)
            else:
                alert(form_alert, m, "erro")
        make_button(btn_row, "Registrar Atendimento", salvar, width=200).pack(side="right")
    # ================================================================
    # MODAL ATENDIMENTO RAPIDO (from patient list)
    # ================================================================
    def modal_atendimento(self, pid):
        pac = self.paciente_model.buscar_por_id(pid)
        pac_nome = pac["nome"] if pac else f"Paciente {pid}"
        modal = ctk.CTkToplevel(self)
        modal.title("Registrar Atendimento")
        modal.geometry("500x480")
        modal.resizable(False, False)
        modal.configure(fg_color=CORES["bg"])
        modal.grab_set()
       
        modal.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - 250
        y = self.winfo_y() + (self.winfo_height() // 2) - 240
        modal.geometry(f"+{x}+{y}")
     
        header_frame = ctk.CTkFrame(modal, fg_color=CORES["primary"], corner_radius=0, height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        ctk.CTkLabel(
            header_frame,
            text=f"Atendimento - {pac_nome}",
            font=FONT_HEADING,
            text_color=CORES["text_light"],
        ).pack(side="left", padx=20, pady=15)
        
        form_frame = ctk.CTkFrame(modal, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=25, pady=20)
        
        ctk.CTkLabel(
            form_frame, text="Prioridade", font=FONT_SMALL_BOLD, text_color=CORES["text"]
        ).pack(anchor="w", pady=(0, 5))
        cb = ctk.CTkComboBox(
            form_frame,
            values=["Normal", "Alta", "Urgente"],
            width=200,
            height=42,
            corner_radius=10,
            border_width=1,
            border_color=CORES["input_border"],
            fg_color=CORES["input_bg"],
            button_color=CORES["primary"],
            button_hover_color=CORES["primary_hover"],
            font=FONT_BODY,
        )
        cb.pack(anchor="w", pady=(0, 15))
        cb.set("Normal")
        
        ctk.CTkLabel(
            form_frame, text="Descricao *", font=FONT_SMALL_BOLD, text_color=CORES["text"]
        ).pack(anchor="w", pady=(0, 5))
        txt = ctk.CTkTextbox(
            form_frame,
            height=140,
            corner_radius=10,
            border_width=1,
            border_color=CORES["input_border"],
            fg_color=CORES["input_bg"],
            text_color=CORES["text"],
            font=FONT_BODY,
        )
        txt.pack(fill="x", pady=(0, 10))
        
        modal_alert = ctk.CTkFrame(form_frame, fg_color="transparent")
        modal_alert.pack(fill="x")
        
        btn_row = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_row.pack(fill="x", pady=(10, 0))
        ctk.CTkButton(
            btn_row,
            text="Cancelar",
            fg_color=CORES["border"],
            hover_color="#CBD5E1",
            text_color=CORES["text"],
            corner_radius=10,
            height=42,
            width=120,
            font=FONT_BUTTON,
            command=modal.destroy,
        ).pack(side="left")
        def salvar():
            descricao = txt.get("1.0", "end").strip()
            prioridade = cb.get()
            ok, m = self.atendimento_model.registrar(pid, descricao, prioridade)
            if ok:
                modal.destroy()
                self.show_atendimentos()
                self.after(100, lambda: alert(
                    self.atend_list_frame if hasattr(self, 'atend_list_frame') else self.main, m
                ))
            else:
                alert(modal_alert, m, "erro")
        make_button(btn_row, "Salvar", salvar, width=140).pack(side="right")
    
    def _highlight_sidebar(self, key):
        for k, btn in self.sidebar_buttons.items():
            if k == key:
                btn.configure(
                    fg_color=CORES["sidebar_active"],
                    text_color=CORES["text_light"],
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color="#CBD5E1",
                )
if __name__ == "__main__":
    app = App()
    app.mainloop()