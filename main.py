# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import  os
from getpass import getpass
from Validation_Scritps.Health_Monitoring import  SSDValidation
from Validation_Scritps.Performance_Benchmarking import NVMePerformaceCheck

def main():
    print("Starting Comprehensive SSD Validation")

    # Define the directory where results will be saved
    results_dir = "/home/vamsimikkii/PycharmProjects/NVMe_Validation/SSD_Test_Results"
    os.makedirs(results_dir, exist_ok=True)

    # Prompt for the device path (e.g., /dev/nvme0n1)
    device = input("Enter the SSD device path (e.g., /dev/nvme0n1): ").strip()

    # Prompt for sudo password
    sudo_password = getpass("Enter your sudo password: ")

    # Initialize the SSDValidation instance
    validator = SSDValidation(device, sudo_password)

    peformace_Validator = NVMePerformaceCheck(device, sudo_password)

    # Run all tests for SSD_Validation HealthMonitoring
    print("\nRunning smartctl Tests...")
    validator.run_all_smartctl_tests()

    print("\nRunning nvme-cli Tests...")
    validator.run_all_nvmecli_tests()

    # Run all tests for SSD_Validation PerformaceBenchmarking
    print("\nRunning PerformaceBenchmarking Tests for Fio...")
    peformace_Validator.run_all_fio_tests()

    # Save results
    validator.save_results(results_dir)

    peformace_Validator.save_results(results_dir)

    print("\nSSD validation completed successfully!")

if __name__ == '__main__':
    main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
