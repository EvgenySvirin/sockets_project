class IPSGenerator:
    def __init__(self, filename: str,
                 clients_amount_limit: int):
        self.filename = filename

        assert clients_amount_limit <= 70000, f"{clients_amount_limit} bigger than max suggestion in technical task"
        self.client_amount_limit = clients_amount_limit

    def generate(self):
        try:
            with open(self.filename, 'x') as file:
                for i in range(255):
                    for k in range(255):
                        if self.client_amount_limit < i * 255 + k:
                            return
                        file.write(f"127.1.{i}.{k}\n")
        except FileExistsError:
            print(f"File {self.filename} already exists, it shall not be generated")