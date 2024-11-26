import subprocess
import os
from getpass import getpass
from click import command

class SSDValidation:
    def __init__(self, device, sudo_password):
        self.device = device
        self.sudo_password = sudo_password
        self.smartctl_results = {}
        self.nvmecli_results = {}

    '''
    This is Common Function which can run all commands by using subprocess if there is any Errors in command
    it will return to user and it stores in LOG's'''

    def run_command(self, command):
        try:
            full_command = f"echo {self.sudo_password} | sudo -S {command}"
            result = subprocess.check_output(full_command, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
            return result
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {e.output}"

    # --- smartctl Commands ---

    # Constructs a command to check the SMART health status of the device (/dev/nvme0n1).
    # The command returns a result like "PASSED" for a healthy device or "FAILED" for a problematic device.
    # The output must be parsed to determine the device's health status programmatically.
    def smart_overall_health(self):
        command = f"smartctl -H {self.device}"
        return self.run_command(command)

    # Constructs a command to retrieve detailed information about the specified device (/dev/nvme0n1).
    # The command "smartctl -i <nvme0n1>" provides details such as device model, serial number, and SMART support status.
    # Executes the command and returns the output, which can be used to inspect the device's properties.
    def smart_device_info(self):
        command = f"smartctl -i {self.device}"
        return self.run_command(command)

    # Constructs a command to retrieve detailed SMART attributes for the specified device (/dev/nvme0n1).
    # The command "smartctl -A </dev/nvme0n1>" provides vital health and usage statistics such as:
    # - Critical warnings, temperature, percentage used, and power-on hours.
    # - Data units read/written, host commands, and integrity errors.
    # - Useful for monitoring device performance, lifespan, and potential failures.
    def smart_attributes(self):
        command = f"smartctl -A {self.device}"
        return self.run_command(command)

    # This test retrieves the SMART thresholds, helping you monitor the limits
    # where a device might start failing or show early signs of failure (e.g., temperature, wear level, etc.).
    def smart_thresholds(self):
        command = f"smartctl -T {self.device}"
        return  self.run_command(command)

    # This longselfTest function detects potential Hardware Issues.
    def smart_long_selftest(self):
        command = f"smartctl -t long {self.device}"
        return self.run_command(command)

    # Constructs a command to retrieve the error log for the specified device (/dev/nvme0n1).
    # The command "smartctl -l error </dev/nvme0n1>" returns a list of recent errors encountered by the device.
    # It includes details about failed operations, error types, timestamps, and affected sectors (if any).
    # Useful for diagnosing hardware issues or identifying trends in device failures.
    def smart_error_log(self):
        command = f"smartctl -l error {self.device}"
        return self.run_command(command)

    # Constructs a command to retrieve the self-test log for the specified device (/dev/nvme0n1).
    # The command "smartctl -l selftest </dev/nvme0n1>" returns a list of results from the device's self-test operations.
    # It includes details about completed self-tests, their statuses, durations, and any failures.
    # Useful for diagnosing device health and determining if past self-tests have detected any issues.
    def smart_selftest_log(self):
        command = f"smartctl -l selftest {self.device}"
        return self.run_command(command)

    #This Function will stores the Maximum Data Transfer Size
    def smart_Maximum_Data_Transfer_Size(self):
        command = f"smartctl -a {self.device} | grep 'Maximum Data Transfer Size'"
        return self.run_command(command)

    #This Function will display the NVMe Version and model Number and SerialNumber of SSD
    def smart_Check_NVMe_version_Model_serialNo(self):
        command = f"smartctl -i {self.device} | grep -E 'NVMe Version|Model Number|Serial Number'"
        return self.run_command(command)

    #This will shows any Media Data Integrity Errors is there it will Logs the Data
    def smart_Media_Data_Integrity_Error_Check(self):
        command = f"smartctl -a {self.device} | grep 'Media and Data Integrity Errorsgrep'"
        return self.run_command(command)

    #This function will return Controller Busy Time
    def smart_Controller_busy_Time(self):
        command = f"smartctl -a {self.device} | grep 'Controller Busy Time'"
        return self.run_command(command)

    # --- nvme-cli Commands ---

    # Constructs a command to retrieve the controller information for the specified NVMe device (/dev/nvme0n1).
    # The command "nvme id-ctrl </dev/nvme0n1>" provides detailed information about the NVMe controller such as:
    # - Vendor ID (vid), model number (mn), firmware revision (fr), and serial number (sn).
    # - Power and temperature-related data (e.g., temperature, power cycles, power-on hours).
    # - Controller-specific attributes, error handling, capabilities, and status information.
    # This information is helpful for inspecting the controller's health, capabilities, and operational status.
    def nvme_device_info(self):
        command = f"nvme id-ctrl {self.device}"
        return self.run_command(command)

    # Constructs a command to retrieve the SMART log for the specified NVMe device (/dev/nvme0n1).
    # The command "nvme smart-log </dev/nvme0n1>" provides important health statistics for the NVMe drive such as:
    # - Critical warnings, temperature, available spare, and percentage used.
    # - Data units read/written, power cycles, power-on hours, and unsafe shutdowns.
    # - Media errors, error log entries, and thermal management data (sensor readings and temperature times).
    # This log is useful for assessing the health and performance of an NVMe device, tracking wear, and diagnosing potential issues.
    def nvme_health_log(self):
        command = f"nvme smart-log {self.device}"
        return self.run_command(command)

    # Constructs a command to retrieve the error log for the specified NVMe device (/dev/nvme0n1).
    # The command "nvme error-log </dev/nvme0n1>" returns detailed information about any errors the NVMe device has encountered.
    # This includes error counts, error types, and information related to the specific errors in the device's operation.
    # It is useful for diagnosing hardware issues, understanding failure patterns, and taking corrective actions if needed.
    def nvme_error_log(self):
        command = f"nvme error-log {self.device}"
        return self.run_command(command)

    #This function Fetches NVMe device features and their current settings.
    #Executes `nvme get-feature` to retrieve details like arbitration, power management,temperature thresholds, error recovery, and more
    def nvme_get_features(self):
        command = f"nvme get-feature {self.device} -f 1"
        return self.run_command(command)

    # Retrieves information about NVMe namespaces.
    # Executes the `nvme list-ns` command to list all namespaces associated with the specified NVMe device.
    # This function return namespace details
    def nvme_namespace_info(self):
        command = f"nvme list-ns {self.device}"
        return self.run_command(command)

    #Retrieve temperature from the NVMe device to check the operational status under stress.
    def nvme_temperature(self):
        command = f"nvme temperature {self.device}"
        return self.run_command(command)

    #Retrieve power cycle stats from the NVMe device to check the operational status under stress.
    def nvme_power_cycles(self):
        command = f"nvme power-cycles {self.device}"
        return self.run_command(command)

    #This Function will return Firmware Version
    def nvme_firmware_version(self):
        command = f"nvme id-ctrl {self.device} | grep 'fr'"
        return self.run_command(command)

    #This will shows SSD power On Hours
    def nvme_power_on_hours(self):
        """Fetch the total number of hours the NVMe device has been powered on."""
        command = f"nvme smart-log {self.device} | grep 'power_on_hours'"
        return self.run_command(command)

    #This Function return How many Data Units Written
    def nvme_data_written(self):
        """Fetch the total data written to the NVMe device."""
        command = f"nvme smart-log {self.device} | grep 'Data Units Written'"
        return self.run_command(command)

    #This Function return the Data Units Read
    def nvme_data_read(self):
        command = f"nvme smart-log {self.device} | grep 'Data Units Read'"
        return self.run_command(command)

    #This Funciton Show How much percentage Used.
    def nvme_percentage_used(self):
        command = f"nvme smart-log {self.device} | grep 'percentage_used'"
        return self.run_command(command)

    #This Function will display How many unsafe ShutDowns Done.
    def nvme_unsafe_shutdowns(self):
        command = f"nvme smart-log {self.device} | grep 'unsafe_shutdowns'"
        return self.run_command(command)

    #This will show Sensors Temperature
    def nvme_temperature_sensors(self):
        command = f"nvme {self.device} | grep 'Temperature Sensor'"
        return self.run_command(command)

    #This will show Any CriticalWarnings is found
    def nvme_critical_Warning_check(self):
        command = f"nvme smart-log {self.device} | grep -i 'critical_warning'"
        return self.run_command(command)

    def nvme_available_spareTest(self):
        command = f"nvme smart-log {self.device} | grep -i 'available_spare'"
        return self.run_command(command)

    def nvme_available_spare_threshold(self):
        command = f"nvme smart-log {self.device} | grep -i 'available_spare_threshold'"
        return self.run_command(command)

    def nvme_continuous_temperature_Monitor(self):
        command = f"watch -n 1 nvme smart-log {self.device} | grep 'temperature'"
        return self.run_command(command)




    # --- Test Runner ---

    # Executes a series of SMART-related tests and collects their results.
    ''' 
    - Retrieves the overall health status of the device using SMART data.
    - Collects general information about the storage device.
    - Fetches SMART attributes, which provide detailed metrics on device performance and reliability.
    - Retrieves the error log to identify any issues recorded by the device.
    - Fetches the self-test log to analyze results of self-diagnostic tests.'''
    # Results are stored in the `smartctl_results` dictionary, categorized by test type.

    def run_all_smartctl_tests(self):
        self.smartctl_results['Overall Health'] = self.smart_overall_health()
        self.smartctl_results['Device Info'] = self.smart_device_info()
        self.smartctl_results['SMART Attributes'] = self.smart_attributes()
        self.smartctl_results['Error Log'] = self.smart_error_log()
        self.smartctl_results['Self-Test Log'] = self.smart_selftest_log()
        self.smartctl_results['Thresholds Log'] = self.smart_thresholds()
        self.smartctl_results['Long_Self-Test Log'] = self.smart_long_selftest()
        self.smartctl_results['Maximum_Data_Transfer'] = self.smart_Maximum_Data_Transfer_Size()
        self.smartctl_results['NVMe_Device_Inforamation'] = self.smart_Check_NVMe_version_Model_serialNo()
        self.smartctl_results['Media_Data_Integrity'] = self.smart_Media_Data_Integrity_Error_Check()
        self.smartctl_results['Controller_BusyTime_Info'] = self.smart_Controller_busy_Time()


    # Executes a series of NVMe CLI commands to gather detailed information and diagnostics for the NVMe device.
    '''
    - Retrieves basic device information using NVMe CLI.
    - Collects the health log to monitor the device's status and endurance metrics.
    - Fetches the error log to identify and analyze any device-related errors.
    - Retrieves supported features and their current configuration for the device.
    - Collects namespace-related information for the NVMe device.'''
    #  Results are stored in the `nvmecli_results` dictionary, categorized by test type.

    def run_all_nvmecli_tests(self):
        self.nvmecli_results['Device Info'] = self.nvme_device_info()
        self.nvmecli_results['Health Log'] = self.nvme_health_log()
        self.nvmecli_results['Error Log'] = self.nvme_error_log()
        self.nvmecli_results['Get Features'] = self.nvme_get_features()
        self.nvmecli_results['Namespace Info'] = self.nvme_namespace_info()
        self.nvmecli_results['Temperature Info'] = self.nvme_temperature()
        self.nvmecli_results['Power-Cycles Info'] = self.nvme_power_cycles()
        self.nvmecli_results['Firmware_Version_Info'] = self.nvme_firmware_version()
        self.nvmecli_results['Power_On_Hours_Info'] = self.nvme_power_on_hours()
        self.nvmecli_results['Data_Written_Info'] = self.nvme_data_written()
        self.nvmecli_results['Data_Read_Info'] = self.nvme_data_read()
        self.nvmecli_results['Percentage_Used_Info'] = self.nvme_percentage_used()
        self.nvmecli_results['Unsafe_Shut_Down_Info'] = self.nvme_unsafe_shutdowns()
        self.nvmecli_results['Sensors_Temperature_Info'] = self.nvme_temperature_sensors()
        self.nvmecli_results['Critical_Warnings_Info'] = self.nvme_critical_Warning_check()


    # --- Save Results ---

    # Saves the results of the smartctl and NVMe CLI tests to organized folders as text files.
    '''
        Parameters:
        base_dir (str): The base directory where results will be saved.
         Steps:
            - Creates two subdirectories within the base directory:
            - "smartctl" for storing smartctl test results.
            - "nvme-cli" for storing NVMe CLI test results.
    - Iterates through the results of smartctl and nvme-cli tests:
        - For each test, constructs a filename based on the test name.
        - Saves the test output to a text file in the respective directory.
        - Ensures directories exist using `os.makedirs` with `exist_ok=True` to prevent errors.
        '''
    def save_results(self, base_dir):
        # Create folders for smartctl and nvme-cli results
        smartctl_dir = os.path.join(base_dir, "smartctl")
        nvmecli_dir = os.path.join(base_dir, "nvme-cli")
        os.makedirs(smartctl_dir, exist_ok=True)
        os.makedirs(nvmecli_dir, exist_ok=True)

        # Save smartctl results
        for test_name, output in self.smartctl_results.items():
            file_name = f"{test_name.replace(' ', '_').lower()}.txt"
            file_path = os.path.join(smartctl_dir, file_name)
            with open(file_path, "w") as file:
                file.write(f"{test_name}\n{'=' * 40}\n{output}")
            print(f"Saved {test_name} results to {file_path}")

        # Save nvme-cli results
        for test_name, output in self.nvmecli_results.items():
            file_name = f"{test_name.replace(' ', '_').lower()}.txt"
            file_path = os.path.join(nvmecli_dir, file_name)
            with open(file_path, "w") as file:
                file.write(f"{test_name}\n{'=' * 40}\n{output}")
            print(f"Saved {test_name} results to {file_path}")