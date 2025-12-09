import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import traceback

try:
    from petshop_backend import PetShop, Servico
except Exception:
    messagebox.showerror("Import error", "Não foi possível importar petshop_backend.Por favor, coloque o backend no mesmo diretório.")
    raise

class PetShopGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PetShop - Interface Gráfica")
        self.geometry("800x500")
        self.resizable(True, True)

        self.petshop = PetShop()  

        self.create_widgets()
        self.refresh_animais()
        self.refresh_servicos()

    def create_widgets(self):
        sidebar = ttk.Frame(self)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=8)

        ttk.Button(sidebar, text="Cadastrar Tutor", command=self.cadastrar_tutor).pack(fill=tk.X, pady=4)
        ttk.Button(sidebar, text="Cadastrar Animal", command=self.cadastrar_animal).pack(fill=tk.X, pady=4)
        ttk.Button(sidebar, text="Agendar Serviço", command=self.agendar_servico).pack(fill=tk.X, pady=4)
        ttk.Button(sidebar, text="Atualizar listas", command=self.refresh_all).pack(fill=tk.X, pady=4)
        ttk.Button(sidebar, text="Salvar Agora", command=self.salvar_agora).pack(fill=tk.X, pady=4)
        ttk.Button(sidebar, text="Sair", command=self.on_close).pack(fill=tk.X, pady=12)

        main = ttk.Frame(self)
        main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.notebook = ttk.Notebook(main)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tab_animais = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_animais, text="Animais")

        self.tree_animais = ttk.Treeview(self.tab_animais, columns=("Especie","Raca","Idade","TutorCPF"), show="headings")
        for col,title in [("Especie","Espécie"),("Raca","Raça"),("Idade","Idade"),("TutorCPF","CPF Tutor")]:
            self.tree_animais.heading(col, text=title)
            self.tree_animais.column(col, width=120, anchor=tk.CENTER)
        self.tree_animais.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        detalhe_frame = ttk.Frame(self.tab_animais)
        detalhe_frame.pack(fill=tk.X, padx=6, pady=6)
        ttk.Button(detalhe_frame, text="Ver Serviços do Animal", command=self.ver_servicos_animal).pack(side=tk.LEFT)
        ttk.Button(detalhe_frame, text="Remover animal (não implementado)", command=lambda: messagebox.showinfo("Info","Remoção não implementada")).pack(side=tk.LEFT, padx=6)

        self.tab_tutores = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_tutores, text="Tutores")
        self.tree_tutores = ttk.Treeview(self.tab_tutores, columns=("Nome","CPF","Tel"), show="headings")
        for col,title in [("Nome","Nome"),("CPF","CPF"),("Tel","Telefone")]:
            self.tree_tutores.heading(col, text=title)
            self.tree_tutores.column(col, width=160, anchor=tk.CENTER)
        self.tree_tutores.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        self.tab_servicos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_servicos, text="Serviços")
        top_serv = ttk.Frame(self.tab_servicos)
        top_serv.pack(fill=tk.X, padx=6, pady=6)
        ttk.Button(top_serv, text="Adicionar Serviço ao Catálogo", command=self.adicionar_servico_catalogo).pack(side=tk.LEFT)
        self.tree_servicos = ttk.Treeview(self.tab_servicos, columns=("Nome","Preco"), show="headings")
        self.tree_servicos.heading("Nome", text="Nome")
        self.tree_servicos.heading("Preco", text="Preço (R$)")
        self.tree_servicos.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

    def cadastrar_tutor(self):
        try:
            nome = simpledialog.askstring("Nome", "Nome do tutor:", parent=self)
            if not nome: return
            cpf = simpledialog.askstring("CPF", "CPF (somente números):", parent=self)
            if not cpf: return
            tel = simpledialog.askstring("Telefone", "Telefone:", parent=self) or ""
            ok = self.petshop.cadastrar_tutor(nome, cpf, tel)
            if ok:
                messagebox.showinfo("Sucesso", "Tutor cadastrado com sucesso.")
                self.refresh_tutores()
            else:
                messagebox.showwarning("Erro", "CPF já cadastrado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao cadastrar tutor:\n{e}\n\n{traceback.format_exc()}")

    def cadastrar_animal(self):
        try:
            nome = simpledialog.askstring("Nome Animal", "Nome do animal:", parent=self)
            if not nome: return
            especie = simpledialog.askstring("Espécie", "Espécie (Cachorro,Gato,Outro):", parent=self) or "Outro"
            raca = simpledialog.askstring("Raça", "Raça:", parent=self) or ""
            idade = simpledialog.askinteger("Idade", "Idade (anos):", parent=self, minvalue=0, maxvalue=100)
            if idade is None: return
            cpf = simpledialog.askstring("CPF Tutor", "CPF do tutor:", parent=self)
            if not cpf: return
            ok = self.petshop.cadastrar_animal(nome, especie, raca, idade, cpf)
            if ok:
                messagebox.showinfo("Sucesso", "Animal cadastrado com sucesso.")
                self.refresh_animais()
            else:
                messagebox.showwarning("Erro", "Tutor não encontrado (verifique o CPF).")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao cadastrar animal:\n{e}")

    def adicionar_servico_catalogo(self):
        try:
            nome = simpledialog.askstring("Nome do Serviço", "Nome do serviço:", parent=self)
            if not nome: return
            preco = simpledialog.askfloat("Preço", "Preço (ex: 45.00):", parent=self, minvalue=0.0)
            if preco is None: return
            if self.petshop.obter_servico_por_nome(nome):
                messagebox.showwarning("Aviso","Serviço já existe no catálogo.")
                return
            self.petshop.adicionar_servico_catalogo(Servico(nome, preco))
            messagebox.showinfo("Sucesso","Serviço adicionado ao catálogo.")
            self.refresh_servicos()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao adicionar serviço:\n{e}")

    def agendar_servico(self):
        try:
            nomes = sorted({a.nome for a in self.petshop.animais})
            if not nomes:
                messagebox.showinfo("Info", "Nenhum animal cadastrado.")
                return
            nome_animal = simpledialog.askstring("Animal", f"Nome do animal (ex: {', '.join(nomes[:6])}...):", parent=self)
            if not nome_animal: return
            servs = list(self.petshop.servicos_catalogo.values())
            if not servs:
                messagebox.showinfo("Info", "Nenhum serviço no catálogo.")
                return
            nomes_serv = ", ".join([s.nome for s in servs])
            nome_servico = simpledialog.askstring("Serviço", f"Serviço (ex: {nomes_serv}):", parent=self)
            if not nome_servico: return
            ok = self.petshop.agendar_servico_para_animal(nome_animal, nome_servico)
            if ok:
                messagebox.showinfo("Sucesso", f"Serviço '{nome_servico}' agendado para '{nome_animal}'.")
                self.refresh_animais()
            else:
                messagebox.showwarning("Erro", "Falha ao agendar. Verifique nome do animal e nome do serviço.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao agendar serviço:\n{e}\n\n{traceback.format_exc()}")

    def ver_servicos_animal(self):
        sel = self.tree_animais.focus()
        if not sel:
            messagebox.showinfo("Info", "Selecione um animal na lista.")
            return
        vals = self.tree_animais.item(sel, "values")
        nome = self.tree_animais.item(sel, "text") 
        nome = nome or vals[0]
        servs = self.petshop.listar_servicos_do_animal(nome)
        if not servs:
            messagebox.showinfo("Serviços", f"Nenhum serviço registrado para '{nome}'.")
            return
        texto = "\n".join(servs)
        messagebox.showinfo(f"Serviços — {nome}", texto)

    def refresh_animais(self):
        for row in self.tree_animais.get_children():
            self.tree_animais.delete(row)
        for a in self.petshop.animais:
            iid = f"{a.nome}_{id(a)}"
            self.tree_animais.insert("", "end", iid, text=a.nome, values=(a.especie.title(), a.raca, a.idade, a.tutor_cpf))

    def refresh_tutores(self):
        for row in self.tree_tutores.get_children():
            self.tree_tutores.delete(row)
        for cpf, t in self.petshop.tutores.items():
            self.tree_tutores.insert("", "end", values=(t.nome, t.cpf, t.telefone))

    def refresh_servicos(self):
        for row in self.tree_servicos.get_children():
            self.tree_servicos.delete(row)
        for s in self.petshop.servicos_catalogo.values():
            self.tree_servicos.insert("", "end", values=(s.nome, f"R$ {s.preco:.2f}"))

    def refresh_all(self):
        self.petshop.load_from_file() 
        self.refresh_animais()
        self.refresh_tutores()
        self.refresh_servicos()
        messagebox.showinfo("Atualizado", "Listas atualizadas a partir dos dados salvos.")

    def salvar_agora(self):
        self.petshop.save_to_file()
        messagebox.showinfo("Salvo", f"Dados salvos no arquivo: {self.petshop.data_file}")

    def on_close(self):
        try:
            self.petshop.save_to_file()
        except Exception:
            pass
        self.destroy()

if __name__ == "__main__":
    app = PetShopGUI()
    app.mainloop()
