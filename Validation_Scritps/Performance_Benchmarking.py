import os
import subprocess
from datetime import date
from select import error
from getpass import getpass


class NVMePerformaceCheck:
    def __init__(self, device, sudo_password):
        self.device = device
        self.sudo_password = sudo_password
        self.fio_results = {}
        self.IoPing_results = {}

    '''
    This is Common Function which can run all commands by using subprocess if there is any Errors in command
    it will return to user and it stores in LOG's'''

    def run_command(self, command):
        try:
            full_command = f"echo {self.sudo_password} | sudo -S {command}"
            result = subprocess.check_output(full_command, stderr=subprocess.STDOUT, shell=True,
                                             universal_newlines=True)
            return result
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {e.output}"

    # ---Fio Commands ---

    def fio_performance_test(self, name, ioengine, rw, bs, size, numjobs, runtime, iodepth=1):
        """
        Run an fio performance test with specified parameters.
        """
        command = (
            f"fio --name={name} "
            f"--ioengine={ioengine} "
            f"--rw={rw} "
            f"--bs={bs} "
            f"--size={size} "
            f"--numjobs={numjobs} "
            f"--runtime={runtime} "
            f"--iodepth={iodepth} "
            f"--group_reporting"
        )
        return self.run_command(command)

    def sequential_read_test(self):
        """
        Run a sequential read test using fio.
        """
        return self.fio_performance_test("seq_read", "libaio", "read", "128k", "1G", 1, 60)

    def random_write_test(self):
        """
        Run a random write test using fio.
        """
        return self.fio_performance_test("rand_write", "libaio", "randwrite", "4k", "1G", 4, 60)

    def high_iodepth_test(self):
        """
        Run a high I/O depth test using fio.
        """
        return self.fio_performance_test("high_iodepth", "libaio", "randrw", "4k", "1G", 4, 60, iodepth=32)


# IO_Ping Commands




    def run_all_fio_tests(self):
        self.fio_results['Sequential_Read__Info'] = self.sequential_read_test()
        self.fio_results['Random_Write_Info'] = self.random_write_test()
        self.fio_results['IO_depth_Info'] = self.high_iodepth_test()


    #Save The Results In Directory
    def save_results(self, base_dir):
        # Create folders for fio and IoPing results
        Fio_dir = os.path.join(base_dir, "Fio_Results")
        IoPing_dir = os.path.join(base_dir, "IoPing_Results")
        os.makedirs(Fio_dir, exist_ok=True)
        os.makedirs(IoPing_dir, exist_ok=True)

        # Save fio results
        for test_name, output in self.fio_results.items():
            file_name = f"{test_name.replace(' ', '_').lower()}.txt"
            file_path = os.path.join(Fio_dir, file_name)
            with open(file_path, "w") as file:
                file.write(f"{test_name}\n{'=' * 40}\n{output}")
            print(f"Saved {test_name} results to {file_path}")

        # Save IoPing results
        for test_name, output in self.IoPing_results.items():
            file_name = f"{test_name.replace(' ', '_').lower()}.txt"
            file_path = os.path.join(IoPing_dir, file_name)
            with open(file_path, "w") as file:
                file.write(f"{test_name}\n{'=' * 40}\n{output}")
            print(f"Saved {test_name} results to {file_path}")






