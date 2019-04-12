
def load_config(config_path):
    configs = {}
    with open(config_path) as f:
        line = f.readline()
        while line:
            item = line.rstrip().split(": ")
            if item[0] == "N":
                configs[item[0]] = int(item[1])
                configs["nodes"] = []
            elif item[0].startswith("node"):
                addrs = item[1].split(":")
                configs["nodes"].append((addrs[0], addrs[1]))
            line = f.readline()
    return configs
