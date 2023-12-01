import io, sys, socket, os


class StdStreamProxy(io.StringIO):
    def __init__(self, stat_stream, original_stdout=None):
        super().__init__()
        self.stat_stream = stat_stream
        self.original_stdout = original_stdout
        self.hostname = socket.gethostname()

    def write(self, data):
        if data.strip():
            if data.startswith("\r"):
                data = f"\r{self.hostname}: "+data[1:]
            else:
                data = f"{self.hostname}: "+data
        self.stat_stream.write(data)
        self.stat_stream.flush()

    def close(self):
        self.original_stdout.close()
        self.stat_stream.close()


megamind_job_path = os.environ.get("MEGAMIND_JOB_PATH")
if not megamind_job_path and sys.argv[0].startswith("/workspace/megamind"):
    megamind_job_path = os.path.dirname(sys.argv[0])
if megamind_job_path:
    sys.stdout = StdStreamProxy(open(megamind_job_path+"/stdout.log", "a", encoding="utf-8"), sys.stdout)
    sys.stderr = StdStreamProxy(open(megamind_job_path+"/stderr.log", "a", encoding="utf-8"), sys.stderr)
