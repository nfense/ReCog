from scanners.portscanner import PortScanner
from scanners.servicescanner import ServiceScanner
from scanners.vulnscanner import VulnerabilityScanner
from utils.logger import Logger
import sys

vulnerabilities = VulnerabilityScanner(
    "https://raw.githubusercontent.com/nfense/vulndb/main/database/{type}/{product}.json")
servicescanner = ServiceScanner()
logger = Logger()

logger.print(f"""
\u001b[31;1m   ___      _____
\u001b[31;1m  / _ \___ / ___/__  ___ _
\u001b[31;1m / , _/ -_) /__/ _ \/ _ `/  \u001b[37mVersion 1.0 ({len(servicescanner.get_modules())} Modules)
\u001b[31;1m/_/|_|\__/\___/\___/\_, /   \u001b[37mPowered by Nfense (https://nfense.com)
\u001b[31;1m                   /___/
""")

if len(sys.argv) == 1:
    logger.critic(
        "{red}{bold}ERROR {reset}Please use python ./recog.py <target>")
    exit()

target = sys.argv[1]

logger.debug("---- Start ----")
logger.debug("Starting scan for target: " + target)
portscanner = PortScanner(target)

vuln_list = []


def end(services_scanned, _):
    logger.debug("---- Vulns ----")
    if len(vuln_list) == 0:
        logger.success("None")
    for vuln in vuln_list:
        if vuln["severity"] == 1:
            logger.log("{bold}" + vuln["name"] + ":")
            logger.print("    Severity: {cyan}LOW")
            logger.print("    Type: {b:cyan}" + vuln["type"])
            logger.print(
                "    Description: {b:cyan}" + vuln["message"])
            logger.print(
                "    Ref: {underline}{b:cyan}" + vuln["ref"])
        elif vuln["severity"] == 2:
            logger.warn("{bold}" + vuln["name"] + ":")
            logger.print("    Severity: {b:yellow}MEDIUM")
            logger.print("    Type: {b:yellow}" + vuln["type"])
            logger.print(
                "    Description: {b:yellow}" + vuln["message"])
            logger.print(
                "    Ref: {underline}{b:yellow}" + vuln["ref"])
        elif vuln["severity"] == 3:
            logger.critic("{bold}" + vuln["name"] + ":")
            logger.print("    Severity: {b:red}CRITICAL")
            logger.print("    Type: {b:red}" + vuln["type"])
            logger.print(
                "    Description: {b:red}" + vuln["message"])
            logger.print(
                "    Ref: {underline}{b:red}" + vuln["ref"])

    logger.debug("---- Extra ---")
    if len(servicescanner.variables) == 0:
        logger.success("None")
    for variable in servicescanner.variables:
        key = variable.split("=")[0]
        value = variable.split("=")[1]
        logger.debug("{cyan}" + key + ": {magenta}" + str(value))

    logger.debug("--- Summary ---")
    logger.debug("Services scanned: " + str(services_scanned))
    logger.debug("Vulnerabilities found: " +
                 str(vulnerabilities.get_founded()))


def scan_for_service(port, socket):
    scanner = servicescanner.get_scanner(port)
    result = scanner.recognition(target, socket)
    servicescanner.push_variables(scanner.variables)
    vulns = vulnerabilities.find(scanner.service, result.lower())
    isVulnerable = len(vulns) != 0

    if isVulnerable:
        result = "{red}" + result
    else:
        result = "{green}" + result

    logger.log("Running service " + scanner.service +
               " at port {blue}" + str(port) + " {reset}(" + result + "{reset})")

    if isVulnerable:
        for vuln in vulns:
            vulnerabilities.add_founded()
            vuln["port"] = str(port) + " " + scanner.service
            vuln_list.append(vuln)


portscanner.on("port_open", scan_for_service)
portscanner.on("end", end)
portscanner.scan_ports_async(servicescanner.get_ports())
