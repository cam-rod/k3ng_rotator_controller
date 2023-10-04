class K3NG:

    def __init__(self, ser_port):
        # Ensure we have r/w
        self.port = Path(ser_port)
        if not self.port.exists():
            raise FileNotFoundError(self.port)

        if not os.access(self.port, os.R_OK | os.W_OK, effective_ids=(os.access in os.supports_effective_ids)):
            # Attempt to chmod file
            if os.geteuid() != 0:
                print(
                    f"Unable to acquire read/write permissions on {self.port}.\n"
                    + "Please change permissions, or run this script as superuser."
                )
                sys.exit(1)

            print(f"Changing permissions on {self.port}")
            curr_mode: int = stat.S_IMODE(os.stat(self.port).st_mode)
            os.chmod(port_path, curr_mode | stat.S_IROTH | stat.S_IWOTH)
            self.modified_perms = True

        self.ser = serial.Serial(ser_port, 9600, timeout=2, inter_byte_timeout=0.5) 

    def read(self):
        return self.ser.read(1000)

    def write(self, cmd):
        self.ser.write(cmd + ARDUINO_LINESEP)
        self.ser.flush()

    def query(self, cmd):
        self.write(cmd)
        return self.read()

    def flush(self):
        self.write(ARDUINO_LINESEP)
        self.ser.flush()
        self.ser.reset_input_buffer()

    def get_version(self):
        retval = self.query("\\?CV")
        return retval[2:]

    def get_time(self):
        retval = self.query("\\C")
        return retval

    def set_time(self, time):
        if len(time) != 14:
            raise ValueError("Invalid time length")

            self.write("\\O" + time)

    def get_loc(self):
        pass

    def set_loc(self, loc):
        if len(loc) != 6:
            raise ValueError("Invalid location length")

        self.write("\\C" + loc)

    def 


