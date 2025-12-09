import json
from typing import Dict, List, Any
from pathlib import Path

DATA_FILE = "petshop_data.json"


class Tutor:
    def __init__(self, nome: str, cpf: str, telefone: str):
        self._nome = nome.strip()
        self._cpf = cpf.strip()
        self._telefone = telefone.strip()

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str):
        self._nome = valor.strip()

    @property
    def cpf(self) -> str:
        return self._cpf

    @property
    def telefone(self) -> str:
        return self._telefone

    @telefone.setter
    def telefone(self, valor: str):
        self._telefone = valor.strip()

    def __str__(self) -> str:
        return f"{self._nome} (CPF: {self._cpf}, Tel: {self._telefone})"

    def to_dict(self) -> Dict[str, Any]:
        return {"nome": self._nome, "cpf": self._cpf, "telefone": self._telefone}

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Tutor":
        return Tutor(d["nome"], d["cpf"], d.get("telefone", ""))


class Servico:
    def __init__(self, nome: str, preco: float):
        self._nome = nome.strip()
        self._preco = float(preco)

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def preco(self) -> float:
        return self._preco

    def __str__(self) -> str:
        return f"{self._nome} (R$ {self._preco:.2f})"

    def to_dict(self) -> Dict[str, Any]:
        return {"nome": self._nome, "preco": self._preco}

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Servico":
        return Servico(d["nome"], d["preco"])


class Animal:
    def __init__(self, nome: str, especie: str, raca: str, idade: int, tutor_cpf: str):
        self._nome = nome.strip()
        self._especie = especie.strip().lower()
        self._raca = raca.strip()
        self._idade = int(idade)
        self._tutor_cpf = tutor_cpf.strip()
        self._servicos_realizados: List[Servico] = []

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str):
        self._nome = valor.strip()

    @property
    def especie(self) -> str:
        return self._especie

    @property
    def raca(self) -> str:
        return self._raca

    @raca.setter
    def raca(self, valor: str):
        self._raca = valor.strip()

    @property
    def idade(self) -> int:
        return self._idade

    @idade.setter
    def idade(self, valor: int):
        self._idade = int(valor)

    @property
    def tutor_cpf(self) -> str:
        return self._tutor_cpf

    @property
    def servicos_realizados(self) -> List[Servico]:
        return list(self._servicos_realizados)

    def realizar_servico(self, servico: Servico):
        if not isinstance(servico, Servico):
            raise TypeError("servico precisa ser uma instância de Servico")
        self._servicos_realizados.append(servico)

    def __str__(self) -> str:
        return f"{self._nome} - {self._especie.title()} / {self._raca} / {self._idade} anos (Tutor CPF: {self._tutor_cpf})"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "class": self.__class__.__name__,
            "nome": self._nome,
            "especie": self._especie,
            "raca": self._raca,
            "idade": self._idade,
            "tutor_cpf": self._tutor_cpf,
            "servicos_realizados": [s.to_dict() for s in self._servicos_realizados],
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Animal":
        cls_name = d.get("class", "Animal")
        nome = d.get("nome", "")
        especie = d.get("especie", "outro")
        raca = d.get("raca", "")
        idade = d.get("idade", 0)
        tutor_cpf = d.get("tutor_cpf", "")
        if cls_name == "Cachorro":
            a = Cachorro(nome, raca, idade, tutor_cpf)
        elif cls_name == "Gato":
            a = Gato(nome, raca, idade, tutor_cpf)
        else:
            a = OutroAnimal(nome, raca, idade, tutor_cpf)
        servs = d.get("servicos_realizados", [])
        for sdict in servs:
            a._servicos_realizados.append(Servico.from_dict(sdict))
        return a


class Cachorro(Animal):
    def __init__(self, nome: str, raca: str, idade: int, tutor_cpf: str):
        super().__init__(nome, "cachorro", raca, idade, tutor_cpf)

    def late(self):
        return "Au au!"


class Gato(Animal):
    def __init__(self, nome: str, raca: str, idade: int, tutor_cpf: str):
        super().__init__(nome, "gato", raca, idade, tutor_cpf)

    def miar(self):
        return "Miau!"


class OutroAnimal(Animal):
    def __init__(self, nome: str, raca: str, idade: int, tutor_cpf: str):
        super().__init__(nome, "outro", raca, idade, tutor_cpf)


class PetShop:
    def __init__(self, data_file: str = DATA_FILE):
        self.data_file = data_file
        self.tutores: Dict[str, Tutor] = {}
        self.animais: List[Animal] = []
        self.servicos_catalogo: Dict[str, Servico] = {}
        self._inicializar_servicos_basicos()
        self.load_from_file()

    def _inicializar_servicos_basicos(self):
        if not self.servicos_catalogo:
            self.adicionar_servico_catalogo(Servico("Banho", 40.0))
            self.adicionar_servico_catalogo(Servico("Tosa", 60.0))
            self.adicionar_servico_catalogo(Servico("Consulta", 80.0))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tutores": [t.to_dict() for t in self.tutores.values()],
            "animais": [a.to_dict() for a in self.animais],
            "servicos_catalogo": [s.to_dict() for s in self.servicos_catalogo.values()],
        }

    def save_to_file(self, path: str = None):
        path = path or self.data_file
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Aviso: não foi possível salvar os dados em '{path}': {e}")

    def load_from_file(self, path: str = None):
        path = path or self.data_file
        p = Path(path)
        if not p.is_file():
            return  
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            self.tutores = {}
            for td in raw.get("tutores", []):
                t = Tutor.from_dict(td)
                self.tutores[t.cpf] = t
            self.servicos_catalogo = {}
            for sd in raw.get("servicos_catalogo", []):
                s = Servico.from_dict(sd)
                self.servicos_catalogo[s.nome.lower()] = s
            self.animais = []
            for ad in raw.get("animais", []):
                a = Animal.from_dict(ad)
                servs_restored: List[Servico] = []
                for sdict in ad.get("servicos_realizados", []):
                    nome_s = sdict.get("nome", "").strip().lower()
                    serv_cat = self.servicos_catalogo.get(nome_s)
                    if serv_cat:
                        servs_restored.append(serv_cat)
                    else:
                        servs_restored.append(Servico.from_dict(sdict))
                a._servicos_realizados = servs_restored
                self.animais.append(a)
        except Exception as e:
            print(f"Aviso: falha ao carregar dados de '{path}': {e}")

    def cadastrar_tutor(self, nome: str, cpf: str, telefone: str) -> bool:
        cpf = cpf.strip()
        if cpf in self.tutores:
            return False
        self.tutores[cpf] = Tutor(nome, cpf, telefone)
        self.save_to_file()
        return True

    def buscar_tutor(self, cpf: str) -> Tutor:
        return self.tutores.get(cpf.strip())

    def cadastrar_animal(self, nome: str, especie: str, raca: str, idade: int, tutor_cpf: str) -> bool:
        tutor_cpf = tutor_cpf.strip()
        if tutor_cpf not in self.tutores:
            return False
        especie_clean = especie.strip().lower()
        if especie_clean == "cachorro":
            animal = Cachorro(nome, raca, idade, tutor_cpf)
        elif especie_clean == "gato":
            animal = Gato(nome, raca, idade, tutor_cpf)
        else:
            animal = OutroAnimal(nome, raca, idade, tutor_cpf)
        self.animais.append(animal)
        self.save_to_file()
        return True

    def encontrar_animal_por_nome(self, nome: str) -> List[Animal]:
        nome = nome.strip().lower()
        return [a for a in self.animais if a.nome.strip().lower() == nome]

    def adicionar_servico_catalogo(self, servico: Servico):
        self.servicos_catalogo[servico.nome.lower()] = servico

        self.save_to_file()

    def obter_servico_por_nome(self, nome: str) -> Servico:
        return self.servicos_catalogo.get(nome.strip().lower())

    def agendar_servico_para_animal(self, nome_animal: str, nome_servico: str) -> bool:
        matches = self.encontrar_animal_por_nome(nome_animal)
        if not matches:
            return False
        servico = self.obter_servico_por_nome(nome_servico)
        if not servico:
            return False
        animal = matches[0]
        animal.realizar_servico(servico)
        self.save_to_file()
        return True

    def listar_todos_animais(self) -> List[str]:
        return [str(a) for a in self.animais]

    def listar_servicos_do_animal(self, nome_animal: str) -> List[str]:
        matches = self.encontrar_animal_por_nome(nome_animal)
        if not matches:
            return []
        animal = matches[0]
        return [str(s) for s in animal.servicos_realizados]

    def listar_tutores_e_animais(self) -> List[str]:
        linhas = []
        for cpf, tutor in self.tutores.items():
            linhas.append(str(tutor))
            animais_do_tutor = [a for a in self.animais if a.tutor_cpf == cpf]
            if animais_do_tutor:
                for a in animais_do_tutor:
                    linhas.append(f"  - {a.nome} ({a.especie.title()}, {a.raca}, {a.idade} anos)")
            else:
                linhas.append("  - (sem animais cadastrados)")
            linhas.append("")
        return linhas


def menu_principal():
    print("\nBem-vindo ao PetShop!\n")
    print("1 - Cadastrar Tutor")
    print("2 - Cadastrar Animal")
    print("3 - Agendar Serviço")
    print("4 - Relatórios")
    print("5 - Ver Catálogo de Serviços")
    print("6 - Adicionar Serviço ao Catálogo")
    print("7 - Salvar dados agora")
    print("8 - Sair\n")


def menu_relatorios():
    print("\n--- RELATÓRIOS ---")
    print("1 - Listar todos os animais cadastrados")
    print("2 - Listar serviços realizados por um animal")
    print("3 - Listar tutores e seus respectivos animais")
    print("4 - Voltar\n")


def main():
    petshop = PetShop()

    print(f"(Arquivo de dados: {petshop.data_file})")
    print("Dados carregados. Iniciando aplicação...")

    while True:
        menu_principal()
        opc = input("> ").strip()
        if opc == "1":
            print("\n-- Cadastrar Tutor --")
            nome = input("Nome do tutor: ").strip()
            cpf = input("CPF: ").strip()
            telefone = input("Telefone: ").strip()
            if petshop.cadastrar_tutor(nome, cpf, telefone):
                print("Tutor cadastrado com sucesso!")
            else:
                print("Erro: CPF já cadastrado. Use outro CPF ou atualize os dados.")
        elif opc == "2":
            print("\n-- Cadastrar Animal --")
            nome = input("Nome do animal: ").strip()
            especie = input("Espécie (Cachorro, Gato, Outro): ").strip()
            raca = input("Raça: ").strip()
            idade_raw = input("Idade (anos): ").strip()
            cpf = input("CPF do tutor: ").strip()
            try:
                idade = int(idade_raw)
                ok = petshop.cadastrar_animal(nome, especie, raca, idade, cpf)
                if ok:
                    print("Animal cadastrado com sucesso!")
                else:
                    print("Erro: Tutor com esse CPF não encontrado. Cadastre o tutor antes.")
            except ValueError:
                print("Idade inválida. Informe um número inteiro.")
        elif opc == "3":
            print("\n-- Agendar Serviço --")
            nome_animal = input("Nome do animal: ").strip()
            print("Serviços disponíveis:")
            for s in petshop.servicos_catalogo.values():
                print(f" - {s}")
            nome_servico = input("Serviço (nome exatamente como no catálogo): ").strip()
            ok = petshop.agendar_servico_para_animal(nome_animal, nome_servico)
            if ok:
                print(f"Serviço '{nome_servico}' realizado/agendado para '{nome_animal}'.")
            else:
                print("Erro: Verifique se o animal existe e se o serviço está no catálogo.")
        elif opc == "4":
            while True:
                menu_relatorios()
                r = input("> ").strip()
                if r == "1":
                    print("\n--- Todos os animais cadastrados ---")
                    todos = petshop.listar_todos_animais()
                    if not todos:
                        print("(nenhum animal cadastrado)")
                    else:
                        for linha in todos:
                            print("- " + linha)
                elif r == "2":
                    nome_animal = input("Nome do animal para ver serviços: ").strip()
                    servs = petshop.listar_servicos_do_animal(nome_animal)
                    if not servs:
                        print(f"(nenhum serviço registrado para '{nome_animal}' ou animal não encontrado)")
                    else:
                        print(f"\n--- Serviços realizados por {nome_animal} ---")
                        for s in servs:
                            print(f"- {s}")
                elif r == "3":
                    print("\n--- Tutores e seus respectivos animais ---")
                    linhas = petshop.listar_tutores_e_animais()
                    if not linhas:
                        print("(nenhum tutor cadastrado)")
                    else:
                        for l in linhas:
                            print(l)
                elif r == "4":
                    break
                else:
                    print("Opção inválida. Tente novamente.")
        elif opc == "5":
            print("\n--- Catálogo de Serviços ---")
            for s in petshop.servicos_catalogo.values():
                print(f"- {s}")
        elif opc == "6":
            print("\n-- Adicionar Serviço ao Catálogo --")
            nome_serv = input("Nome do serviço: ").strip()
            preco_raw = input("Preço (ex.: 45.50): ").strip()
            try:
                preco = float(preco_raw)
                if petshop.obter_servico_por_nome(nome_serv):
                    print("Serviço já existe no catálogo (use outro nome ou atualize).")
                else:
                    petshop.adicionar_servico_catalogo(Servico(nome_serv, preco))
                    print("Serviço adicionado ao catálogo.")
            except ValueError:
                print("Preço inválido.")
        elif opc == "7":
            petshop.save_to_file()
            print(f"Dados salvos em '{petshop.data_file}'.")
        elif opc == "8":
            petshop.save_to_file()
            print("Dados salvos. Saindo... Até mais!")
            break
        else:
            print("Opção inválida. Digite um número entre 1 e 8.")


if __name__ == "__main__":
    main()
