from pathlib import Path
import datetime
import pickle


def now():
    return datetime.datetime.now().strftime("%H:%M:%S")


def print_info(text):
    if text:
        print(f"{now()} Info: " + text)


def print_error(text):
    if text:
        print(f"{now()} Error: " + text)


###
# RENAME
###

# Die Klassen aus NF-UQ-NIDSv2 wurden umbenannt.
def rename_attack(name):
    d = {
    'Infilteration':"Infiltration",
    'injection':"Injection",
    'Reconnaissance':"Scanning",
    'scanning':"Scanning",
    'password':"Password",
    'Brute Force': "Password",
    'xss':"XSS"
    }
    result = d.get(name)
    return result if result else name


def rename_dataset(name):
    d = {
    'NF-BoT-IoT-v2':"BoT-IoT",
    'NF-CSE-CIC-IDS2018-v2':"CSE-CIC-IDS2018",
    'NF-ToN-IoT-v2':"TON-IoT",
    'NF-UNSW-NB15-v2':"UNSW-NB15"
    }
    result = d.get(name)
    return result if result else name


def rename_model(name):
    d = {
        "cart":"CART",
        "extra": "Extra Trees",
        "idtree":"IntruDTree",
        "idforest": "InturDForest",
        "xgboost": "XGBoost"
    }
    result = d.get(name)
    return result if result else name

# Featurenamen werden für die Abbildung 5.3 abgekürzt.
def rename_feature(name):
    d = {'CLIENT_TCP_FLAGS':"CLT_TCP_FLAGS",
         'DST_TO_SRC_AVG_THROUGHPUT':"DST_TO_SRC_AVG_TP",
         'DST_TO_SRC_SECOND_BYTES':"DST_TO_SRC_SEC_BYT",
         'FLOW_DURATION_MILLISECONDS':"FLOW_DUR_MSEC",
         'FTP_COMMAND_RET_CODE':"FTP_CMD_RET_CODE",
         'LONGEST_FLOW_PKT':"LONG_FLOW_PKT",
         'NUM_PKTS_1024_TO_1514_BYTES':"PKTS_1024-1514_BYT",
         'NUM_PKTS_128_TO_256_BYTES':"PKTS_128-256_BYT",
         'NUM_PKTS_256_TO_512_BYTES':"PKTS_256-512_BYT",
         'NUM_PKTS_512_TO_1024_BYTES':"PKTS_512-1024_BYT",
         'NUM_PKTS_UP_TO_128_BYTES':"PKTS_UP_TO_128_BYT",
         'RETRANSMITTED_IN_BYTES':"RETRANS_IN_BYT",
         'RETRANSMITTED_IN_PKTS':"RETRANS_IN_PKTS",
         'RETRANSMITTED_OUT_BYTES':"RETRANS_OUT_BYT",
         'RETRANSMITTED_OUT_PKTS':"RETRANS_OUT_PKTS",
         'SERVER_TCP_FLAGS':"SRVR_TCP_FLAGS",
         'SHORTEST_FLOW_PKT':"SHORT_FLOW_PKT",
         'SRC_TO_DST_AVG_THROUGHPUT':"SRC_TO_DST_AVG_TP",
         'SRC_TO_DST_SECOND_BYTES':"SRC_TO_DST_SEC_BYT"
    }
    result = d.get(name)
    return result if result else name


def rename_attack_fhswfcnl(value):
    if value == "Recon":
        return "Scanning"
    return value


def rename_attack_ids2017(value):
    if value == "BENIGN":
        return "Benign"
    if value == "PortScan":
        return "Scanning"
    if value.endswith("Brute Force") or value == "FTP-Patator" or value == "SSH-Patator":
        return "Password"
    if value.endswith("XSS"):
        return "XSS"
    if value.startswith("DoS"):
        return "DoS"
    return value


def rename_attack_ddos2019(value):
    return "Benign" if value == "BENIGN" else "DDoS"


def get_datasets():
    file_names = ["fhswfcnl", "cicids2017", "cicddos2019"]
    title_names = ["FH-SWF-CNL", "CIC-IDS2017", "CIC-DDoS2019"]
    return {a:b for a,b in zip(file_names, title_names)}

def get_modelnames():
    file_names = ["cart", "idtree", "extra", "idforest", "xgboost"]
    title_names = ["CART", "IntruDTree", "Extra-Trees", "IntruDForest", "XGBoost"]
    return {a:b for a,b in zip(file_names, title_names)}

###
# Features
###


def get_modifications():
    return ["int", "ext", "red", "rex"]


def get_features(columns, mod):
    features = [x for x in columns if x not in ("IPV4_DST_ADDR", "IPV4_SRC_ADDR", "Attack", "Dataset", "Label")]
    return modify_features(features, mod)


def modify_features(features, mod):
    if mod == "ext":
        features.remove("IPV4_DST_ADDR_INT")
        features.remove("IPV4_SRC_ADDR_INT")
        features.remove("DNS_QUERY_ID")
        pass
    elif mod == "red":
        features.remove("IPV4_DST_ADDR_INT")
        features.remove("IPV4_SRC_ADDR_INT")
        features.remove("IPV4_DST_ADDR_EX")
        features.remove("IPV4_SRC_ADDR_EX")
        features.remove("L4_DST_PORT")
        features.remove("L4_SRC_PORT")
        features.remove("L7_PROTO")
        features.remove("DNS_QUERY_ID")
        pass
    elif mod == "rex":
        features.remove("IPV4_DST_ADDR_INT")
        features.remove("IPV4_SRC_ADDR_INT")
        features.remove("L4_DST_PORT")
        features.remove("L4_SRC_PORT")
        features.remove("L7_PROTO")
        features.remove("DNS_QUERY_ID")
        pass
    elif mod == "int":
        features.remove("IPV4_DST_ADDR_EX")
        features.remove("IPV4_SRC_ADDR_EX")
    else:
        raise Exception("No modification level set.")
    return features


def save_model(id_, model):
    Path("model").mkdir(parents=True, exist_ok=True)
    print_info("Pickling model.")
    with open(f"model/{id_.as_file()}.pkl", "wb") as file:
        pickle.dump(model, file)


def load_model(id_):
    print_info(f"Loading model: {id_}.")
    with open(f"model/{id_.as_file()}.pkl", "rb") as file:
        result = pickle.load(file)
    return result


###
# Classes
###

# Hilfsobjekt zur einheitlichen Namensgebung der erzeugten Modelle und Berechnungen
class Identifier:
    mod = ""
    name = ""
    title = ""

    def as_file(self):
        return f"{self.name}_{self.title}_{self.mod}"

    def __str__(self):
        return f"[Model <{self.name}> trained on Data set <{self.title}> with Modification <{self.mod}>]"