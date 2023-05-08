import re


# Parse data from the format required by Popper
# to the format required by Aleph
class BiasFileParser:

    def __init__(self, original_bias_file, translated_bias_file, new_bias_file, bk_file):
        self.original_bias_file = original_bias_file
        self.translated_bias_file = translated_bias_file
        self.new_bias_file = new_bias_file
        self.bk_file = bk_file
        self.load_original_bias_file()

    def load_original_bias_file(self):
        with open(self.original_bias_file, "r") as f:
            self.original_bias_data = f.read()
            
        self.max_vars = re.findall(r'max_vars\(([0-9]*)\)', self.original_bias_data)[0]        
        self.max_body = re.findall(r'max_body\(([0-9]*)\)', self.original_bias_data)[0]

        body_preds = re.findall(r'body_pred\((\w*),([0-9]*)\)', self.original_bias_data)
        head_preds = re.findall(r'head_pred\((\w*),([0-9]*)\)', self.original_bias_data)

        types = re.findall(r'type\((\w*),(\(.*\))\)', self.original_bias_data)
        types = [(pred, list(map(str, l.strip('()').split(',')))) for (pred, l) in types]

        directions = re.findall(r'direction\((\w*),(\(.*\))\)', self.original_bias_data)
        directions = [(pred, list(map(str, l.strip('()').split(',')))) for (pred, l) in directions]

        self.directions_dict = {}
        self.types_dict = {}
        self.body_pred_dict = {}
        self.head_pred_dict = {}

        for pred, s in body_preds:
            self.body_pred_dict[pred] = s

        for pred, s in head_preds:
            self.head_pred_dict[pred] = s

        for pred, l in directions:
            if l[-1] == "":
                l = l[:-1]
            self.directions_dict[pred] = l

        for pred, l in types:
            if l[-1] == "":
                l = l[:-1]
            self.types_dict[pred] = l

    def translate_bias_file(self):
        with open(self.translated_bias_file, "w") as f:

            f.write(":- use_module(library(aleph)).\n")
            f.write(":- aleph.\n")
            f.write(f":- aleph_set(i,{self.max_vars}).\n")

            func = lambda c: '+' if c == "in" else "-"

            for pred in self.body_pred_dict:

                dirs = list(map(func, self.directions_dict[pred]))

                dirs_and_types = [dirs[i] + self.types_dict[pred][i] for i in range(len(self.types_dict[pred]))]
                dirs_and_types = ",".join(dirs_and_types)
                f.write(f":- modeb(*,{pred}({dirs_and_types})).\n")

            for pred in self.head_pred_dict:

                dirs = list(map(func, self.directions_dict[pred]))

                dirs_and_types = [dirs[i] + self.types_dict[pred][i] for i in range(len(self.types_dict[pred]))]
                dirs_and_types = ",".join(dirs_and_types)
                f.write(f":- modeh(*,{pred}({dirs_and_types})).\n")

            for hpred in self.head_pred_dict:
                for bpred in self.body_pred_dict:
                    f.write(f":- determination({hpred}/{self.head_pred_dict[hpred]},{bpred}/{self.body_pred_dict[bpred]}).\n")

            bk_filename = '.'.join(self.bk_file.split('.')[:-1])
            f.write(f":- [{bk_filename}].\n")

    def write_new_bias(self, preds):
        with open(self.new_bias_file, "w") as f:
            f.write(f"max_vars({self.max_vars}).\nmax_body({self.max_body}).\n")

            for pred in preds:

                if pred in self.head_pred_dict:
                    f.write(f"head_pred({pred},{self.head_pred_dict[pred]}).\n")
                else:
                    f.write(f"body_pred({pred},{self.body_pred_dict[pred]}).\n")

                s = str(tuple(self.types_dict[pred])).replace("'", '')
                f.write(f"type({pred},{s}).\n")

                s = str(tuple(self.directions_dict[pred])).replace("'", '')
                f.write(f"direction({pred},{s}).\n")




